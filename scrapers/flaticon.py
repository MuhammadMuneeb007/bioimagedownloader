"""Flaticon scraper - https://www.flaticon.com/"""

import os
import time
from urllib.parse import urljoin, quote
from bs4 import BeautifulSoup
from .utils import get_driver, download_file, save_links


def scrape_flaticon(keyword, folder):
    """Scrape Flaticon for icons - images and links."""
    print(f"\n[Flaticon] Searching for: {keyword}")
    driver = None
    try:
        driver = get_driver()
        
        # Use the correct Flaticon URL format
        url = f"https://www.flaticon.com/search?word={quote(keyword)}"
        print(f"  Loading: {url}")
        driver.get(url)
        time.sleep(5)  # Wait for results to load
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        downloaded = 0
        icon_links = []
        image_urls = []
        
        # Find the search-result section container
        search_results = soup.find_all('section', class_='search-result')
        
        for section in search_results:
            # Find all icon cards/items within the search-result section
            # Look for images and links
            images = section.find_all('img', src=True)
            links = section.find_all('a', href=True)
            
            # Extract image URLs
            for i, img in enumerate(images[:10]):
                img_src = img.get('src') or img.get('data-src')
                if img_src:
                    # Handle relative URLs
                    if img_src.startswith('/'):
                        img_url = urljoin("https://www.flaticon.com", img_src)
                    elif img_src.startswith('http'):
                        img_url = img_src
                    else:
                        img_url = urljoin("https://www.flaticon.com/", img_src)
                    
                    # Skip placeholder/loading images
                    if 'placeholder' in img_src.lower() or 'loading' in img_src.lower():
                        continue
                    
                    image_urls.append(img_url)
                    
                    # Try to download image
                    ext = '.svg' if '.svg' in img_src.lower() else '.png'
                    filename = f"flaticon_{keyword}_{downloaded + 1}{ext}"
                    filepath = os.path.join(folder, filename)
                    if download_file(img_url, filepath):
                        downloaded += 1
            
            # Extract icon page links
            for link in links:
                href = link.get('href')
                if href and ('/free-icon/' in href or '/premium-icon/' in href):
                    if href.startswith('/'):
                        icon_url = urljoin("https://www.flaticon.com", href)
                    elif href.startswith('http'):
                        icon_url = href
                    else:
                        icon_url = urljoin("https://www.flaticon.com/", href)
                    
                    if icon_url not in icon_links:
                        icon_links.append(icon_url)
        
        # Limit to first 10 links
        icon_links = icon_links[:10]
        
        # Save links if we didn't download much or as additional reference
        if downloaded == 0 and icon_links:
            save_links(os.path.join(folder, "flaticon_links.txt"), icon_links, "Flaticon")
        elif downloaded > 0:
            print(f"  Downloaded {downloaded} images from Flaticon")
            # Also save links for reference
            if icon_links:
                filepath = os.path.join(folder, "flaticon_links.txt")
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"Flaticon links for: {keyword}\n")
                    f.write("="*50 + "\n\n")
                    for link in icon_links:
                        f.write(f"{link}\n")
                print(f"  Saved {len(icon_links)} icon page links")
        else:
            print("  No results found for Flaticon")
            
    except Exception as e:
        print(f"  Flaticon error: {e}")
    finally:
        if driver:
            driver.quit()

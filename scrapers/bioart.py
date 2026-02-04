"""BioArt scraper - science visuals."""

import os
import time
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup
from .utils import get_driver, download_file, save_links


def scrape_bioart(keyword, folder):
    """Scrape BioArt for science visuals."""
    print(f"\n[BioArt] Searching for: {keyword}")
    driver = None
    try:
        driver = get_driver()
        
        # Use the correct BioArt URL format
        url = f"https://bioart.niaid.nih.gov/discover?q={quote(keyword)}&sort=relevance"
        print(f"  Loading: {url}")
        driver.get(url)
        time.sleep(5)
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        downloaded = 0
        detail_links = []
        image_urls = []
        
        # Find all MUI cards (results)
        cards = soup.find_all('div', class_=lambda x: x and 'MuiCard-root' in x)
        
        for i, card in enumerate(cards[:10]):
            # Find image in card
            img = card.find('img', src=True)
            if img:
                img_src = img.get('src')
                if img_src and '/api/bioarts/' in img_src:
                    # Convert relative URL to full URL
                    if img_src.startswith('/'):
                        img_url = urljoin("https://bioart.niaid.nih.gov", img_src)
                    else:
                        img_url = img_src
                    
                    image_urls.append(img_url)
                    
                    # Try to download image
                    ext = '.png' if '.png' in img_src.lower() else '.jpg' if '.jpg' in img_src.lower() else '.png'
                    filename = f"bioart_{keyword}_{i+1}{ext}"
                    filepath = os.path.join(folder, filename)
                    if download_file(img_url, filepath):
                        downloaded += 1
            
            # Find detail page link
            link = card.find('a', href=True)
            if link:
                href = link.get('href')
                if href and '/bioart/' in href:
                    if href.startswith('/'):
                        detail_url = urljoin("https://bioart.niaid.nih.gov", href)
                    else:
                        detail_url = href
                    if detail_url not in detail_links:
                        detail_links.append(detail_url)
        
        # Save links if we didn't download much
        if downloaded == 0 and detail_links:
            save_links(os.path.join(folder, "bioart_links.txt"), detail_links[:20], "BioArt")
        elif downloaded > 0:
            print(f"  Downloaded {downloaded} images from BioArt")
            # Also save detail links
            if detail_links:
                filepath = os.path.join(folder, "bioart_links.txt")
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"BioArt detail links for: {keyword}\n")
                    f.write("="*50 + "\n\n")
                    for link in detail_links[:20]:
                        f.write(f"{link}\n")
                print(f"  Saved {min(len(detail_links), 20)} detail links")
        else:
            print("  No results found")
            
    except Exception as e:
        print(f"  BioArt error: {e}")
    finally:
        if driver:
            driver.quit()

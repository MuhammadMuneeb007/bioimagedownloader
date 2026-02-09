"""Noun Project scraper - https://thenounproject.com/"""

import os
import time
from urllib.parse import urljoin, quote
from bs4 import BeautifulSoup
from . import utils
from .utils import download_file, save_links


def scrape_nounproject(keyword, folder):
    """Scrape Noun Project for icons - images and links."""
    print(f"\n[NounProject] Searching for: {keyword}")
    driver = None
    try:
        driver = utils.get_driver()
        
        # Use the correct NounProject URL format
        url = f"https://thenounproject.com/search/icons/?q={quote(keyword)}"
        print(f"  Loading: {url}")
        driver.get(url)
        time.sleep(5)  # Wait for results to load
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        downloaded = 0
        icon_links = []
        
        # Find the grid container (browse-page-1)
        grid_container = soup.find('div', id='browse-page-1')
        if not grid_container:
            # Fallback: find by class containing GridContainer
            grid_container = soup.find('div', class_=lambda x: x and 'GridContainer' in x)
        
        if grid_container:
            # Find all grid items
            grid_items = grid_container.find_all('div', class_=lambda x: x and 'GridItem' in x)
            
            for i, item in enumerate(grid_items[:10]):  # Limit to first 10 items
                # Extract image URL
                img_tag = item.find('img', src=True)
                if img_tag:
                    img_src = img_tag.get('src')
                    if img_src and 'static.thenounproject.com' in img_src:
                        # Try to download image
                        filename = f"nounproject_{keyword}_{i+1}.png"
                        filepath = os.path.join(folder, filename)
                        if download_file(img_src, filepath):
                            downloaded += 1
                
                # Extract icon page link
                link_tag = item.find('a', href=True)
                if link_tag:
                    href = link_tag.get('href')
                    if href and '/icon/' in href:
                        if href.startswith('/'):
                            icon_url = urljoin("https://thenounproject.com", href)
                        elif href.startswith('http'):
                            icon_url = href
                        else:
                            icon_url = urljoin("https://thenounproject.com/", href)
                        
                        if icon_url not in icon_links:
                            icon_links.append(icon_url)
        else:
            # Fallback: search for links in the whole page
            for a in soup.find_all('a', href=True):
                href = a.get('href')
                if href and '/icon/' in href:
                    if href.startswith('/'):
                        icon_url = urljoin("https://thenounproject.com", href)
                    elif href.startswith('http'):
                        icon_url = href
                    else:
                        icon_url = urljoin("https://thenounproject.com/", href)
                    
                    if icon_url not in icon_links:
                        icon_links.append(icon_url)
        
        # Limit to first 10 links
        icon_links = icon_links[:10]
        
        # Save links if we didn't download much or as additional reference
        if downloaded == 0 and icon_links:
            save_links(os.path.join(folder, "nounproject_links.txt"), icon_links, "NounProject")
        elif downloaded > 0:
            print(f"  Downloaded {downloaded} images from NounProject")
            # Also save links for reference
            if icon_links:
                filepath = os.path.join(folder, "nounproject_links.txt")
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"NounProject links for: {keyword}\n")
                    f.write("="*50 + "\n\n")
                    for link in icon_links:
                        f.write(f"{link}\n")
                print(f"  Saved {len(icon_links)} icon page links")
        else:
            print("  No results found for NounProject")
            
    except Exception as e:
        print(f"  NounProject error: {e}")
    finally:
        if driver:
            driver.quit()

"""Pixabay scraper - https://pixabay.com/"""

import os
import time
from urllib.parse import urljoin, quote
from bs4 import BeautifulSoup
from . import utils
from .utils import download_file, save_links


def scrape_pixabay(keyword, folder):
    """Scrape Pixabay for icons - download if possible."""
    print(f"\n[Pixabay] Searching for: {keyword}")
    driver = None
    try:
        driver = utils.get_driver()
        url = f"https://pixabay.com/vectors/search/{quote(keyword)}/"
        driver.get(url)
        time.sleep(3)
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        downloaded = 0
        links_found = []
        
        # Find image elements
        for img in soup.find_all('img', src=True):
            src = img['src']
            if 'pixabay.com' in src and any(ext in src.lower() for ext in ['.png', '.jpg', '.svg']):
                # Try to get higher resolution
                img_url = src.replace('__340', '__480').replace('_340', '_480')
                ext = '.png' if '.png' in src.lower() else '.svg' if '.svg' in src.lower() else '.jpg'
                filename = f"pixabay_{keyword}_{downloaded+1}{ext}"
                filepath = os.path.join(folder, filename)
                if download_file(img_url, filepath):
                    downloaded += 1
                if downloaded >= 10:
                    break
        
        # Find detail page links
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '/vectors/' in href and href.startswith('/'):
                full_url = urljoin("https://pixabay.com", href)
                if full_url not in links_found:
                    links_found.append(full_url)
        
        if downloaded == 0 and links_found:
            save_links(os.path.join(folder, "links.txt"), links_found[:10], "Pixabay")
        elif downloaded > 0:
            print(f"  Downloaded {downloaded} images from Pixabay")
            
    except Exception as e:
        print(f"  Pixabay error: {e}")
    finally:
        if driver:
            driver.quit()

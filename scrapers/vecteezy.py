"""Vecteezy scraper - https://www.vecteezy.com/"""

import os
import time
from urllib.parse import urljoin, quote
from bs4 import BeautifulSoup
from . import utils


def scrape_vecteezy(keyword, folder):
    """Scrape Vecteezy for icon links - links only."""
    print(f"\n[Vecteezy] Searching for: {keyword}")
    driver = None
    try:
        driver = utils.get_driver()
        url = f"https://www.vecteezy.com/free-vector/{quote(keyword)}"
        driver.get(url)
        time.sleep(4)
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '/vector-art/' in href or '/free-vector/' in href:
                full_url = urljoin("https://www.vecteezy.com", href)
                if full_url not in links:
                    links.append(full_url)
        
        links = links[:10]
        if links:
            filepath = os.path.join(folder, "vecteezy_links.txt")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Vecteezy links for: {keyword}\n")
                f.write("="*50 + "\n\n")
                for link in links:
                    f.write(f"{link}\n")
            print(f"  Saved {len(links)} links to vecteezy_links.txt")
        else:
            print("  No links found")
            
    except Exception as e:
        print(f"  Vecteezy error: {e}")
    finally:
        if driver:
            driver.quit()

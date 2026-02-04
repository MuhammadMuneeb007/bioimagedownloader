"""Freepik scraper - https://www.freepik.com/"""

import os
import time
from urllib.parse import urljoin, quote
from bs4 import BeautifulSoup
from .utils import get_driver


def scrape_freepik(keyword, folder):
    """Scrape Freepik for icon links - links only."""
    print(f"\n[Freepik] Searching for: {keyword}")
    driver = None
    try:
        driver = get_driver()
        url = f"https://www.freepik.com/search?format=search&query={quote(keyword)}+icon"
        driver.get(url)
        time.sleep(4)
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '/free-vector/' in href or '/free-icon/' in href or '/premium-vector/' in href:
                full_url = urljoin("https://www.freepik.com", href)
                if full_url not in links:
                    links.append(full_url)
        
        links = links[:10]
        if links:
            filepath = os.path.join(folder, "freepik_links.txt")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Freepik links for: {keyword}\n")
                f.write("="*50 + "\n\n")
                for link in links:
                    f.write(f"{link}\n")
            print(f"  Saved {len(links)} links to freepik_links.txt")
        else:
            print("  No links found")
            
    except Exception as e:
        print(f"  Freepik error: {e}")
    finally:
        if driver:
            driver.quit()

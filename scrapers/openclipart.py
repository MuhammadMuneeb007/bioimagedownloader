"""OpenClipart scraper - https://openclipart.org/"""

import os
import time
from urllib.parse import urljoin, quote
from bs4 import BeautifulSoup
from .utils import get_driver, download_file, save_links


def scrape_openclipart(keyword, folder):
    """Scrape OpenClipart for clipart - download if possible."""
    print(f"\n[OpenClipart] Searching for: {keyword}")
    driver = None
    try:
        driver = get_driver()
        url = f"https://openclipart.org/search/?query={quote(keyword)}"
        driver.get(url)
        time.sleep(3)
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        downloaded = 0
        links_found = []
        
        # Find clipart detail pages
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '/detail/' in href:
                full_url = urljoin("https://openclipart.org", href)
                if full_url not in links_found:
                    links_found.append(full_url)
        
        # Try to download from detail pages
        for i, link in enumerate(links_found[:10]):
            try:
                driver.get(link)
                time.sleep(2)
                page_soup = BeautifulSoup(driver.page_source, 'lxml')
                
                # Find SVG download link
                for a in page_soup.find_all('a', href=True):
                    href = a['href']
                    if '.svg' in href.lower():
                        svg_url = urljoin("https://openclipart.org", href)
                        filename = f"openclipart_{keyword}_{i+1}.svg"
                        filepath = os.path.join(folder, filename)
                        if download_file(svg_url, filepath):
                            downloaded += 1
                            break
                
                # Check for PNG
                if downloaded <= i:
                    for a in page_soup.find_all('a', href=True):
                        href = a['href']
                        if '.png' in href.lower():
                            png_url = urljoin("https://openclipart.org", href)
                            filename = f"openclipart_{keyword}_{i+1}.png"
                            filepath = os.path.join(folder, filename)
                            if download_file(png_url, filepath):
                                downloaded += 1
                                break
                                
            except Exception as e:
                print(f"  Error processing clipart: {e}")
        
        if downloaded == 0 and links_found:
            save_links(os.path.join(folder, "links.txt"), links_found[:10], "OpenClipart")
        else:
            print(f"  Downloaded {downloaded} files from OpenClipart")
            
    except Exception as e:
        print(f"  OpenClipart error: {e}")
    finally:
        if driver:
            driver.quit()

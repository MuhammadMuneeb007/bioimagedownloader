"""BioIcons scraper - https://bioicons.com/"""

import os
import time
from urllib.parse import urljoin, quote

from bs4 import BeautifulSoup
from .utils import get_driver, download_file, save_links


def scrape_bioicons(keyword, folder):
    """Scrape bioicons.com for SVG icons."""
    print(f"\n[BioIcons] Searching for: {keyword}")
    driver = None
    try:
        driver = get_driver()

        # Directly load the URL with query parameter
        url = f"https://bioicons.com/?query={quote(keyword)}"
        print(f"  Loading: {url}")
        driver.get(url)
        
        # Wait for results to load
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "lxml")

        # 4) Find SVG images directly from the results grid
        # Results are in #infiniteScroll #app-grid with <article> tags containing <img> with src pointing to SVG
        downloaded = 0
        icon_links = []
        
        # Look for images in the app-grid container
        app_grid = soup.find("div", id="app-grid")
        if app_grid:
            images = app_grid.find_all("img", src=True)
            for i, img in enumerate(images[:10]):
                src = img.get("src") or img.get("data-src")
                if src and ".svg" in src.lower():
                    # Handle relative URLs
                    if src.startswith("/"):
                        svg_url = urljoin("https://bioicons.com", src)
                    elif src.startswith("http"):
                        svg_url = src
                    else:
                        svg_url = urljoin("https://bioicons.com/", src)
                    
                    # Skip placeholder/loading images
                    if "loading" in src.lower() or "static" in src.lower():
                        continue
                    
                    filename = f"bioicons_{keyword}_{i+1}.svg"
                    filepath = os.path.join(folder, filename)
                    if download_file(svg_url, filepath):
                        downloaded += 1
                        icon_links.append(svg_url)
        
        # Fallback: look for icon detail page links if direct download didn't work
        if downloaded == 0:
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "/icon/" in href or "/icons/" in href:
                    full_url = urljoin("https://bioicons.com", href)
                    if full_url not in icon_links:
                        icon_links.append(full_url)
            
            icon_links = icon_links[:10]
            if icon_links:
                save_links(os.path.join(folder, "links.txt"), icon_links, "BioIcons")

    except Exception as e:
        print(f"  BioIcons error: {e}")
    finally:
        if driver:
            driver.quit()

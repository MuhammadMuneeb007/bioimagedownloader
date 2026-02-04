"""SciDraw scraper - https://scidraw.io/"""

import os
import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from .utils import get_driver, download_file, save_links


def _find_search_input(driver, timeout: int = 15):
    """Try several common selectors to locate the SciDraw search input."""
    wait = WebDriverWait(driver, timeout)
    selectors = [
        (By.CSS_SELECTOR, "input[type='search']"),
        (By.CSS_SELECTOR, "input[placeholder*='search' i]"),
        (By.CSS_SELECTOR, "input[name='q']"),
        (By.TAG_NAME, "input"),
    ]
    for by, value in selectors:
        try:
            element = wait.until(EC.presence_of_element_located((by, value)))
            if element:
                return element
        except Exception:
            continue
    return None


def scrape_scidraw(keyword, folder):
    """Scrape scidraw.io for scientific drawings using real on-page search."""
    print(f"\n[SciDraw] Searching for: {keyword}")
    driver = None
    try:
        driver = get_driver()

        # 1) Open homepage
        driver.get("https://scidraw.io/")

        # 2) Find the search input on the page
        search_input = _find_search_input(driver)
        if not search_input:
            print("  Could not locate SciDraw search input.")
            return

        # 3) Type the keyword and submit
        try:
            search_input.clear()
        except Exception:
            pass
        search_input.send_keys(keyword)
        search_input.send_keys(Keys.ENTER)

        # 4) Wait a bit for results to load
        time.sleep(4)

        # Optionally wait until at least one result image shows up
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img"))
            )
        except Exception:
            # If this fails, we still try to parse whatever is loaded
            pass

        soup = BeautifulSoup(driver.page_source, "lxml")

        # 5) Narrow down to the main results container if present
        container = soup.find("div", class_="grid-container-container")
        search_scope = container if container is not None else soup

        # Find image/SVG elements only inside the results grid
        downloaded = 0
        images = search_scope.find_all("img", src=True)

        for i, img in enumerate(images[:10]):
            src = img["src"]
            if any(ext in src.lower() for ext in [".svg", ".png", ".jpg", ".jpeg"]):
                img_url = urljoin("https://scidraw.io", src)
                ext = ".svg" if ".svg" in src.lower() else ".png"
                filename = f"scidraw_{keyword}_{i+1}{ext}"
                filepath = os.path.join(folder, filename)
                if download_file(img_url, filepath):
                    downloaded += 1

        # 6) Also look for inline SVG elements directly
        svgs = search_scope.find_all("svg")
        for i, svg in enumerate(svgs[:5]):
            if downloaded >= 10:
                break
            svg_content = str(svg)
            if len(svg_content) > 100:  # Not tiny inline SVGs
                filename = f"scidraw_svg_{keyword}_{i+1}.svg"
                filepath = os.path.join(folder, filename)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(svg_content)
                downloaded += 1

        # 7) If nothing downloaded, at least save some result links
        if downloaded == 0:
            links = []
            for a in search_scope.find_all("a", href=True):
                href = a["href"]
                if keyword.lower() in href.lower():
                    links.append(href)
            links = links[:10]
            if links:
                save_links(os.path.join(folder, "links.txt"), links, "SciDraw")

    except Exception as e:
        print(f"  SciDraw error: {e}")
    finally:
        if driver:
            driver.quit()

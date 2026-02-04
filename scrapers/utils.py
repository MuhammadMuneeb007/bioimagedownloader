"""Shared utility functions for all scrapers."""

import os
import requests
import undetected_chromedriver as uc


def get_driver(headless: bool = True):
    """Create and return an undetected Chrome driver.

    Args:
        headless (bool): If True, run browser in headless mode. Defaults to True.

    Returns:
        Chrome driver instance.
    """
    options = uc.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if headless:
        # Run without opening a visible browser window
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
    else:
        # Useful for debugging locally
        options.add_argument("--start-maximized")

    driver = uc.Chrome(options=options)
    return driver


def download_file(url, filepath, headers=None):
    """Download a file from URL to filepath."""
    try:
        if headers is None:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36"
            }
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(resp.content)
            print(f"  Downloaded: {os.path.basename(filepath)}")
            return True
    except Exception as e:
        print(f"  Failed to download {url}: {e}")
    return False


def save_links(filepath, links, source_name):
    """Save links to a text file."""
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"\n=== {source_name} ===\n")
        for link in links:
            f.write(f"{link}\n")
    print(f"  Saved {len(links)} links from {source_name}")


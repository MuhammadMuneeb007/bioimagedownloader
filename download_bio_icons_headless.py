#!/usr/bin/env python3
"""
download_bio_icons_headless.py

Headless version - Downloads biology/science icons from multiple websites.
Runs without showing browser windows.

Usage:
    python download_bio_icons_headless.py DNA, neuron, protein, mitochondria

Install requirements:
    pip install undetected-chromedriver selenium requests beautifulsoup4 lxml
"""

import os
import re
import shutil
import subprocess
import sys
import time
from scrapers import (
    scrape_bioicons,
    scrape_scidraw,
    scrape_bioart,
    scrape_flaticon,
    scrape_nounproject,
    scrape_freepik,
    scrape_vecteezy,
    scrape_pixabay,
    scrape_svgrepo,
    scrape_openclipart,
)

# Import and patch utils to use headless mode
from scrapers import utils

# Store original get_driver
_original_get_driver = utils.get_driver


def detect_chrome_version():
    """Detect the installed Chrome/Chromium major version."""
    # 1) Try Windows registry first (most reliable on Windows)
    try:
        import winreg
        for root_key in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
            try:
                key = winreg.OpenKey(root_key, r"Software\Google\Chrome\BLBeacon")
                version_str, _ = winreg.QueryValueEx(key, "version")
                winreg.CloseKey(key)
                version = int(version_str.split(".")[0])
                print(f"  Detected Chrome version {version} from Windows registry")
                return version
            except (FileNotFoundError, OSError):
                continue
    except ImportError:
        pass  # Not on Windows

    candidates = []

    # 2) Try common CLI names
    for name in ("google-chrome", "google-chrome-stable", "chromium-browser", "chromium"):
        path = shutil.which(name)
        if path:
            candidates.append(path)

    # 3) macOS default location
    mac_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if os.path.exists(mac_path):
        candidates.append(mac_path)

    # 4) Common Windows locations
    for win_path in (
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
    ):
        if os.path.exists(win_path):
            candidates.append(win_path)

    for binary in candidates:
        try:
            output = subprocess.check_output(
                [binary, "--version"], stderr=subprocess.DEVNULL, timeout=5
            ).decode().strip()
            match = re.search(r"(\d+)\.\d+\.\d+", output)
            if match:
                version = int(match.group(1))
                print(f"  Detected Chrome version {version} from: {binary}")
                return version
        except (subprocess.SubprocessError, OSError):
            continue

    print("  WARNING: Could not detect Chrome version.")
    return None


def _create_chrome_options():
    """Create fresh ChromeOptions for headless mode."""
    import undetected_chromedriver as uc
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    return options


def get_driver_headless():
    """Create headless Chrome driver with the correct version."""
    import undetected_chromedriver as uc

    version = detect_chrome_version()

    # Always create fresh options - cannot reuse ChromeOptions objects
    options = _create_chrome_options()
    
    kwargs = {
        "options": options,
        "use_subprocess": True,
    }
    
    if version is not None:
        kwargs["version_main"] = version

    try:
        driver = uc.Chrome(**kwargs)
        return driver
    except Exception as e:
        print(f"  Driver creation failed: {e}")
        # Create fresh options for retry
        options2 = _create_chrome_options()
        print("  Retrying with fresh options...")
        driver = uc.Chrome(options=options2, use_subprocess=True)
        return driver


# Patch the utils module
utils.get_driver = get_driver_headless


def main():
    """Main function to run all scrapers in headless mode."""
    print("=" * 60)
    print("  BIO IMAGE DOWNLOADER (HEADLESS MODE)")
    print("  Downloads biology/science icons from multiple sources")
    print("=" * 60)

    # Get keywords from command line arguments
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        keywords = [k.strip() for k in user_input.split(",") if k.strip()]
    else:
        print("\nUsage: python download_bio_icons_headless.py DNA, neuron, protein")
        print("No keywords provided. Exiting.")
        return

    if not keywords:
        print("No keywords provided. Exiting.")
        return

    print(f"\nProcessing {len(keywords)} keyword(s): {', '.join(keywords)}")
    print("Running in HEADLESS mode (no browser windows will appear)")

    # Create base output folder
    base_folder = "Output"
    os.makedirs(base_folder, exist_ok=True)

    # Process each keyword
    for keyword in keywords:
        print(f"\n{'=' * 60}")
        print(f"  Processing keyword: {keyword}")
        print("=" * 60)

        keyword_folder = os.path.join(base_folder, keyword)
        os.makedirs(keyword_folder, exist_ok=True)

        scrapers = [
            scrape_bioicons,
            scrape_scidraw,
            scrape_bioart,
            scrape_flaticon,
            scrape_nounproject,
            scrape_svgrepo,
        ]

        for scraper in scrapers:
            try:
                scraper(keyword, keyword_folder)
            except Exception as e:
                print(f"  Error in {scraper.__name__}: {e}")
            time.sleep(2)

    print(f"\n{'=' * 60}")
    print("  DONE! Check the Output folder for results.")
    print("=" * 60)


if __name__ == "__main__":
    main()
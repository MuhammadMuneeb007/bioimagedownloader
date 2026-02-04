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

# Override to always use headless mode
def get_driver_headless():
    """Create headless Chrome driver."""
    return _original_get_driver(headless=True)

# Patch the utils module
utils.get_driver = get_driver_headless


def main():
    """Main function to run all scrapers in headless mode."""
    print("="*60)
    print("  BIO IMAGE DOWNLOADER (HEADLESS MODE)")
    print("  Downloads biology/science icons from multiple sources")
    print("="*60)
    
    # Get keywords from command line arguments
    if len(sys.argv) > 1:
        # Join all arguments and split by comma
        user_input = ' '.join(sys.argv[1:])
        keywords = [k.strip() for k in user_input.split(',') if k.strip()]
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
        print(f"\n{'='*60}")
        print(f"  Processing keyword: {keyword}")
        print("="*60)
        
        # Create keyword folder
        keyword_folder = os.path.join(base_folder, keyword)
        os.makedirs(keyword_folder, exist_ok=True)
        
        # Call all scrapers
        scrapers = [
            scrape_bioicons,
            scrape_scidraw,
            scrape_bioart,
            scrape_flaticon,
            scrape_nounproject,
            scrape_svgrepo
        ]
        
        for scraper in scrapers:
            try:
                scraper(keyword, keyword_folder)
            except Exception as e:
                print(f"  Error in {scraper.__name__}: {e}")
            time.sleep(2)  # Small delay between scrapers
    
    print(f"\n{'='*60}")
    print("  DONE! Check the Output folder for results.")
    print("="*60)


if __name__ == "__main__":
    main()

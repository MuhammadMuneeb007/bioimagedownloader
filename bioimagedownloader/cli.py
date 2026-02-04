#!/usr/bin/env python3
"""
Command-line interface for BioImageDownloader.

This is the entry point used by the `bioimagedownloader` console script.
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


def main():
    """Main function to run all scrapers."""
    print("=" * 60)
    print("  BIO IMAGE DOWNLOADER")
    print("  Downloads biology/science icons from multiple sources")
    print("=" * 60)

    # Get keywords from command line arguments
    if len(sys.argv) > 1:
        # Join all arguments and split by comma
        user_input = " ".join(sys.argv[1:])
        keywords = [k.strip() for k in user_input.split(",") if k.strip()]
    else:
        print("\nUsage: bioimagedownloader DNA, neuron, protein")
        print("No keywords provided. Exiting.")
        return

    if not keywords:
        print("No keywords provided. Exiting.")
        return

    print(f"\nProcessing {len(keywords)} keyword(s): {', '.join(keywords)}")

    # Create base output folder
    base_folder = "Output"
    os.makedirs(base_folder, exist_ok=True)

    # Process each keyword
    for keyword in keywords:
        print(f"\n{'=' * 60}")
        print(f"  Processing keyword: {keyword}")
        print("=" * 60)

        # Create keyword folder
        keyword_folder = os.path.join(base_folder, keyword)
        os.makedirs(keyword_folder, exist_ok=True)

        # Call selected scrapers
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
            time.sleep(2)  # Small delay between scrapers

    print(f"\n{'=' * 60}")
    print("  DONE! Check the Output folder for results.")
    print("=" * 60)


if __name__ == "__main__":
    main()


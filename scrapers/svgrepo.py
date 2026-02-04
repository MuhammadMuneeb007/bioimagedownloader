"""SVGRepo scraper - https://www.svgrepo.com/"""

import os
import time
from urllib.parse import urljoin, quote
from bs4 import BeautifulSoup
from .utils import get_driver, download_file, save_links


def scrape_svgrepo(keyword, folder):
    """Scrape SVGRepo for SVG icons - images and links."""
    print(f"\n[SVGRepo] Searching for: {keyword}")
    driver = None
    try:
        driver = get_driver()
        
        # Use the correct SVGRepo URL format
        url = f"https://www.svgrepo.com/vectors/{quote(keyword)}/"
        print(f"  Loading: {url}")
        driver.get(url)
        time.sleep(5)  # Wait for results to load
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        downloaded = 0
        icon_links = []
        
        # Find the node listing container
        node_listing = soup.find('div', class_=lambda x: x and 'nodeListing' in x)
        if not node_listing:
            # Fallback: search for nodes directly
            node_listing = soup
        
        # Find all node items
        nodes = node_listing.find_all('div', class_=lambda x: x and 'Node__' in x)
        
        for i, node in enumerate(nodes[:10]):  # Limit to first 10 nodes
            # Find the NodeImage container
            node_image = node.find('div', class_=lambda x: x and 'NodeImage' in x)
            if node_image:
                # Extract SVG image URL from img tag
                img_tag = node_image.find('img', src=True)
                if img_tag:
                    img_src = img_tag.get('src')
                    if img_src and '.svg' in img_src.lower() and 'svgrepo.com' in img_src:
                        # Download SVG directly
                        filename = f"svgrepo_{keyword}_{i+1}.svg"
                        filepath = os.path.join(folder, filename)
                        if download_file(img_src, filepath):
                            downloaded += 1
                
                # Extract detail page link from a tag
                link_tag = node_image.find('a', href=True)
                if link_tag:
                    href = link_tag.get('href')
                    if href and '/svg/' in href:
                        if href.startswith('/'):
                            icon_url = urljoin("https://www.svgrepo.com", href)
                        elif href.startswith('http'):
                            icon_url = href
                        else:
                            icon_url = urljoin("https://www.svgrepo.com/", href)
                        
                        if icon_url not in icon_links:
                            icon_links.append(icon_url)
        
        # Fallback: if no nodes found, search for images directly
        if downloaded == 0:
            images = soup.find_all('img', src=True)
            for i, img in enumerate(images[:10]):
                img_src = img.get('src')
                if img_src and '.svg' in img_src.lower() and 'svgrepo.com/show/' in img_src:
                    filename = f"svgrepo_{keyword}_{i+1}.svg"
                    filepath = os.path.join(folder, filename)
                    if download_file(img_src, filepath):
                        downloaded += 1
        
        # Save links if we didn't download much or as additional reference
        if downloaded == 0 and icon_links:
            save_links(os.path.join(folder, "svgrepo_links.txt"), icon_links, "SVGRepo")
        elif downloaded > 0:
            print(f"  Downloaded {downloaded} SVGs from SVGRepo")
            # Also save links for reference
            if icon_links:
                filepath = os.path.join(folder, "svgrepo_links.txt")
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"SVGRepo links for: {keyword}\n")
                    f.write("="*50 + "\n\n")
                    for link in icon_links:
                        f.write(f"{link}\n")
                print(f"  Saved {len(icon_links)} icon page links")
        else:
            print("  No results found for SVGRepo")
            
    except Exception as e:
        print(f"  SVGRepo error: {e}")
    finally:
        if driver:
            driver.quit()

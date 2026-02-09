# BioImageDownloader

A Python package to download biology and science icons/images from multiple websites including BioIcons, BioArt, Flaticon, NounProject, SVGRepo, and more.

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🔍 **Multiple Sources**: Download from 10+ icon/image websites
- 🤖 **Headless Mode**: Runs in background (default)
- 📦 **Auto-Organization**: Files organized by keyword automatically
- 🔗 **Link Fallback**: Saves links when direct download fails
- 🛡️ **Bot Detection Bypass**: Uses undetected Chrome driver

## Supported Websites

- **BioIcons** (bioicons.com) - Biology-focused SVG icons
- **BioArt** (bioart.niaid.nih.gov) - Science visuals from NIAID
- **Flaticon** (flaticon.com) - General icon library
- **NounProject** (thenounproject.com) - Icon collection
- **SVGRepo** (svgrepo.com) - SVG icon repository
 

---

## 📦 Installation

### Prerequisites

- **Python**: 3.7 or higher
- **Chrome Browser**: Must be installed on your system
- **pip**: Python package manager (usually comes with Python)

### Installation Methods

#### Method 1: Install from GitHub (Recommended)

```bash
# Clone the repository
git clone https://github.com/muhammadmuneeb007/bioimagedownloader.git
cd bioimagedownloader

# Install dependencies
pip install -r requirements.txt

# Install the package in editable mode
pip install -e .
```

**What this does:**
- Downloads all source code
- Installs all required dependencies
- Installs the package in "editable" mode (changes to code are immediately available)

#### Method 2: Build and Install Locally

```bash
# Clone the repository
git clone https://github.com/muhammadmuneeb007/bioimagedownloader.git
cd bioimagedownloader

# Build and install automatically
python build_package.py
```

**What this does:**
1. Checks for build tools (`build`, `wheel`)
2. Installs them if missing
3. Builds source and wheel distributions
4. Automatically installs the wheel into your environment

#### Method 3: Install from PyPI (After Upload)

Once the package is published to PyPI:

```bash
pip install bioimagedownloader
```

#### Method 4: Install from GitHub URL

Install directly from GitHub without cloning:

```bash
pip install git+https://github.com/muhammadmuneeb007/bioimagedownloader.git
```

### Verify Installation

After installation, verify it worked:

```bash
# Check installation
pip show bioimagedownloader

# Test command line interface
bioimagedownloader DNA

# Test Python import
python -c "from scrapers import scrape_bioicons; scrape_bioicons('DNA', 'test_output')"
```

### Dependencies

The following dependencies are automatically installed with the package:

- `undetected-chromedriver` - Chrome driver that bypasses bot detection
- `selenium` - Web browser automation
- `requests` - HTTP library for downloading files
- `beautifulsoup4` - HTML parsing
- `lxml` - XML/HTML parser backend

### Troubleshooting Installation

**"Command not found" after installation:**
- Make sure your Python Scripts directory is in PATH
- Try: `python -m bioimagedownloader DNA` instead
- Or use: `python download_bio_icons.py DNA`

**"Module not found" error:**
- Verify installation: `pip show bioimagedownloader`
- Reinstall: `pip install --force-reinstall -e .`
- Check Python version: `python --version` (needs 3.7+)

**Chrome driver issues:**
- Ensure Chrome browser is installed and up to date
- The package uses `undetected-chromedriver` which auto-downloads the driver

---

## 🚀 Usage / Execution

### Command Line Usage

#### Basic Syntax

```bash
bioimagedownloader <keyword1>, <keyword2>, <keyword3>, ...
```

#### Examples

```bash
# Single keyword
bioimagedownloader DNA

# Multiple keywords (comma-separated)
bioimagedownloader DNA, neuron, protein

# With spaces in keywords
bioimagedownloader "cell membrane", "DNA helix", neuron

# Many keywords at once
bioimagedownloader DNA, RNA, protein, cell, mitochondria, neuron, synapse

# Or use the Python script directly
python download_bio_icons.py DNA, neuron, protein, mitochondria
```

### Python API Usage

#### Quick Start

```python
from scrapers import scrape_bioicons, scrape_bioart, scrape_flaticon

# Download icons for a keyword
keyword = "DNA"
folder = "output/DNA"

scrape_bioicons(keyword, folder)
scrape_bioart(keyword, folder)
scrape_flaticon(keyword, folder)
```
 

### Advanced Usage Examples

#### Example 1: Batch Processing Multiple Keywords

```python
from scrapers import scrape_bioicons
import os

keywords = ["DNA", "RNA", "protein", "cell", "mitochondria"]
base_folder = "biology_icons"

for keyword in keywords:
    folder = os.path.join(base_folder, keyword)
    os.makedirs(folder, exist_ok=True)
    scrape_bioicons(keyword, folder)
    print(f"Completed: {keyword}")
```

#### Example 2: Custom Output Directory

```python
from scrapers import scrape_bioicons
import os

# Custom output location
custom_output = "C:/MyIcons/DNA"
os.makedirs(custom_output, exist_ok=True)

scrape_bioicons("DNA", custom_output)
```

#### Example 3: Error Handling

```python
from scrapers import scrape_bioicons, scrape_bioart
import os

keyword = "DNA"
folder = "output/DNA"
os.makedirs(folder, exist_ok=True)

scrapers = [scrape_bioicons, scrape_bioart]

for scraper in scrapers:
    try:
        scraper(keyword, folder)
        print(f"✓ {scraper.__name__} completed")
    except Exception as e:
        print(f"✗ {scraper.__name__} failed: {e}")
        continue
```

### Output Structure

After running, your files will be organized like this:

```
Output/
├── DNA/
│   ├── bioicons_DNA_1.svg
│   ├── bioicons_DNA_2.svg
│   ├── bioart_DNA_1.png
│   ├── flaticon_DNA_1.png
│   ├── nounproject_links.txt
│   ├── svgrepo_DNA_1.svg
│   └── ...
├── neuron/
│   └── ...
└── protein/
    └── ...
```
 

### Configuration

#### Headless Mode

**By default, all scrapers run in headless mode** (no browser window). To disable headless mode (show browser), modify `scrapers/utils.py`:

```python
def get_driver(headless=False):  # Change to False
    ...
```

#### Custom Output Directory

Modify the `base_folder` variable in `download_bio_icons.py`:

```python
base_folder = "MyCustomOutput"  # Change this
```

#### Custom Scraper Selection

Edit the `scrapers` list in `download_bio_icons.py`:

```python
scrapers = [
    scrape_bioicons,      # Enable
    # scrape_scidraw,     # Disable
    scrape_bioart,        # Enable
    # ... etc
]
```

### Troubleshooting Usage

**No results found:**
- Try different keywords
- Check internet connection
- Wait a few minutes and try again (rate limiting)

**Files not downloading:**
- Check `*_links.txt` files for URLs
- Try downloading manually from links
- Check network connection

**Browser errors:**
- Install/update Chrome browser
- Try disabling headless mode
- Check Chrome version compatibility

---

## API Reference

### Core Utility Functions

#### `get_driver(headless=True)`

Creates and returns an undetected Chrome driver instance.

```python
from scrapers.utils import get_driver

driver = get_driver(headless=True)
driver.get("https://example.com")
driver.quit()
```

#### `download_file(url, filepath, headers=None)`

Downloads a file from URL to filepath.

```python
from scrapers.utils import download_file

success = download_file("https://example.com/image.svg", "output/image.svg")
```

#### `save_links(filepath, links, source_name)`

Saves a list of links to a text file.

```python
from scrapers.utils import save_links

links = ["https://example.com/1", "https://example.com/2"]
save_links("output/links.txt", links, "Example")
```

---

## Tips and Best Practices

1. **Use specific keywords**: More specific keywords yield better results
   - Good: "DNA helix", "neuron synapse", "protein structure"
   - Less ideal: "biology", "science", "icon"

2. **Check output folder**: Always check the `Output/` folder after running
   - Some scrapers save links instead of files
   - Check `*_links.txt` files for URLs

3. **Handle errors gracefully**: Wrap scrapers in try-except blocks

4. **Respect websites**: Don't run too many requests too quickly

---

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/muhammadmuneeb007/bioimagedownloader.git
cd bioimagedownloader

# Install in editable mode
pip install -e .

# Install development dependencies
pip install -r requirements.txt
```

### Building the Package

```bash
# Build source and wheel distributions
python build_package.py

# Or manually
python -m build
```

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Adding a New Scraper

1. Create a new file in `scrapers/` directory (e.g., `scrapers/newsite.py`)
2. Implement the scraper function:
   ```python
   def scrape_newsite(keyword, folder):
       """Scrape newsite.com for icons."""
       driver = get_driver()
       try:
           # Your scraping logic
           pass
       finally:
           driver.quit()
   ```
3. Add to `scrapers/__init__.py`
4. Add to `download_bio_icons.py` scrapers list

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational and research purposes only. Please respect the terms of service of the websites you're scraping from. Always check the licensing requirements of downloaded images/icons before commercial use.

## Acknowledgments

- Thanks to all the icon/image providers
- Built with [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver) for bypassing bot detection

## Support

For issues and questions:
- Open an issue on [GitHub Issues](https://github.com/muhammadmuneeb007/bioimagedownloader/issues)
- Check existing issues for solutions

---

**Made with ❤️ for the scientific community**

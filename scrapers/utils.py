"""Shared utility functions for all scrapers."""

import os
import platform
import re
import shutil
import subprocess
import requests
import undetected_chromedriver as uc


def detect_chrome_version():
    """Detect the installed Chrome major version (Windows, macOS, Linux).

    Returns:
        int or None: The major version number, or None if detection fails.
    """
    system = platform.system()

    # ----- Windows -----
    if system == "Windows":
        try:
            import winreg
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Google\Chrome\BLBeacon",
                )
                version, _ = winreg.QueryValueEx(key, "version")
                winreg.CloseKey(key)
                major = int(version.split(".")[0])
                print(f"[utils] Detected Chrome version {major} (Windows registry)")
                return major
            except (FileNotFoundError, OSError):
                pass
        except ImportError:
            pass

        # Fall back to running chrome.exe --version
        win_paths = [
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
        ]
        for chrome_path in win_paths:
            ver = _version_from_binary(chrome_path)
            if ver:
                return ver

    # ----- macOS -----
    elif system == "Darwin":
        mac_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            os.path.expanduser(
                "~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            ),
        ]
        for path in mac_paths:
            ver = _version_from_binary(path)
            if ver:
                return ver

    # ----- Linux (also used as final fallback for other OSes) -----
    linux_names = [
        "google-chrome",
        "google-chrome-stable",
        "google-chrome-beta",
        "google-chrome-dev",
        "chromium-browser",
        "chromium",
    ]
    for name in linux_names:
        binary = shutil.which(name)
        if binary:
            ver = _version_from_binary(binary)
            if ver:
                return ver

    print("[utils] Could not auto-detect Chrome version on any platform.")
    return None


def _version_from_binary(binary_path):
    """Run ``<binary> --version`` and return the major version int, or None."""
    if not os.path.exists(binary_path):
        return None
    try:
        result = subprocess.run(
            [binary_path, "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        output = result.stdout.strip() or result.stderr.strip()
        match = re.search(r"(\d+)\.\d+\.\d+", output)
        if match:
            major = int(match.group(1))
            print(f"[utils] Detected Chrome version {major} from: {binary_path}")
            return major
    except (subprocess.SubprocessError, OSError) as e:
        print(f"[utils] Failed to get version from {binary_path}: {e}")
    return None


def _create_chrome_options(headless: bool = True):
    """Create fresh ChromeOptions - cannot be reused."""
    options = uc.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")

    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
    else:
        options.add_argument("--start-maximized")

    return options


def get_driver(headless: bool = True):
    """Create and return an undetected Chrome driver.

    Args:
        headless (bool): If True, run browser in headless mode. Defaults to True.

    Environment:
        CHROME_VERSION_MAIN (optional): Chrome *major* version to force, e.g. ``144``.
        Set this if you see errors like
        \"This version of ChromeDriver only supports Chrome version XXX\".

    Returns:
        Chrome driver instance.
    """
    # Allow overriding Chrome major version via environment variable.
    version_main_env = os.getenv("CHROME_VERSION_MAIN")
    version_main = None

    if version_main_env:
        try:
            version_main = int(version_main_env)
            print(
                f"[utils.get_driver] Using Chrome major version "
                f"{version_main} from CHROME_VERSION_MAIN"
            )
        except ValueError:
            print(
                "[utils.get_driver] Warning: CHROME_VERSION_MAIN is not a valid "
                "integer, ignoring it."
            )
    else:
        version_main = detect_chrome_version()

    # Create fresh options - ChromeOptions cannot be reused
    options = _create_chrome_options(headless)
    driver_kwargs = {"options": options, "use_subprocess": True}
    
    if version_main:
        driver_kwargs["version_main"] = version_main

    try:
        driver = uc.Chrome(**driver_kwargs)
        return driver
    except Exception as e:
        print(f"[utils.get_driver] Driver creation failed: {e}")
        # Create fresh options for retry - cannot reuse ChromeOptions
        options2 = _create_chrome_options(headless)
        print("[utils.get_driver] Retrying with fresh options...")
        driver = uc.Chrome(options=options2, use_subprocess=True)
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
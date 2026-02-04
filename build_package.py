#!/usr/bin/env python3
"""
Build script for creating distribution packages and installing locally.

Usage (from project root):
    python build_package.py

This will:
  1. Build source and wheel distributions into the dist/ folder
  2. Automatically install the built wheel into the current environment
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def clean_build():
    """Clean previous build artifacts."""
    print("Cleaning previous builds...")
    for name in ("build", "dist"):
        p = Path(name)
        if p.exists():
            shutil.rmtree(p, ignore_errors=True)
            print(f"  Removed {p}/")

    # Remove *.egg-info directories
    for item in Path(".").iterdir():
        if item.name.endswith(".egg-info") and item.is_dir():
            shutil.rmtree(item, ignore_errors=True)
            print(f"  Removed {item}/")


def build_and_install():
    """Build the package and install the wheel locally."""
    print("=" * 60)
    print("Building BioImageDownloader package...")
    print("=" * 60)

    clean_build()

    # Ensure build is available (you already installed build & wheel)
    try:
        import build  # noqa: F401
    except ImportError:
        print("Installing 'build' module...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "build"],
        )

    # Run python -m build
    print("\nRunning: python -m build\n")
    result = subprocess.run(
        [sys.executable, "-m", "build"],
        text=True,
    )
    if result.returncode != 0:
        print("\n✗ Build failed")
        sys.exit(1)

    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("\n✗ dist/ directory not found after build")
        sys.exit(1)

    print("\nFiles in 'dist/':")
    wheel_path = None
    for file in sorted(dist_dir.iterdir()):
        size_kb = file.stat().st_size / 1024
        print(f"  - {file.name} ({size_kb:.1f} KB)")
        if file.suffix == ".whl":
            wheel_path = file

    if wheel_path is None:
        print("\n✗ No wheel (.whl) file found in dist/ to install.")
        sys.exit(1)

    # Install the wheel into the current environment
    print(f"\nInstalling wheel locally: {wheel_path.name}\n")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", str(wheel_path)]
        )
        print(f"\n✓ Installed {wheel_path.name} successfully.")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Failed to install wheel: {e}")
        print("You can try installing manually with:")
        print(f"  pip install {wheel_path}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Local build and install complete.")
    print("You can now import and use 'bioimagedownloader' in this environment.")
    print("=" * 60)


if __name__ == "__main__":
    build_and_install()


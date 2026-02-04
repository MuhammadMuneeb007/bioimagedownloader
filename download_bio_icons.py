#!/usr/bin/env python3
"""
Legacy script entry point for BioImageDownloader.

You can now use the `bioimagedownloader` console command instead:

    bioimagedownloader DNA, neuron, protein
"""

from bioimagedownloader.cli import main


if __name__ == "__main__":
    main()


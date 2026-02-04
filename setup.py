"""Setup script for BioImageDownloader package."""

from setuptools import setup, find_packages
import os

# Read README for long description
readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = ""
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()

# Read requirements
requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
requirements = []
if os.path.exists(requirements_path):
    with open(requirements_path, 'r', encoding='utf-8') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='bioimagedownloader',
    version='1.0.0',
    description='Download biology/science icons from multiple websites',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/muhammadmuneeb007/bioimagedownloader',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.7',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'bioimagedownloader=bioimagedownloader.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

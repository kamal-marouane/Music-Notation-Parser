"""
Setup script for installing the Music Notation Parser package.
"""

from setuptools import setup, find_packages

setup(
    name="music_notation_parser",
    version="0.1.0",
    description="A parser for music notation from Excel spreadsheets",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "openpyxl>=3.0.0",
        "openpyxl-image-loader>=1.0.0",
        "pillow>=9.0.0",
        "imagehash>=4.0.0",
        "moviepy>=1.0.0",
        "pygame>=2.0.0",
        "python-dotenv>=0.15.0",
    ],
    entry_points={
        "console_scripts": [
            "music-parser=src.main:main",
        ],
    },
    python_requires=">=3.7",
)
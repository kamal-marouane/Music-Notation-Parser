"""
Configuration management module for MusicNotationParser.

This module loads environment variables and provides configuration settings
for the entire application.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = Path(__file__).resolve().parent

# Input file configuration
EXCEL_FILE_PATH = os.getenv('EXCEL_FILE_PATH', '')
EXCEL_SHEET_NAME = os.getenv('EXCEL_SHEET_NAME', 'Feuil1')

# Image paths
NOTES_DIR = os.getenv('NOTES_DIR', '')
REFERENCE_IMAGES_PATH = os.getenv('REFERENCE_IMAGES_PATH', os.path.join(NOTES_DIR, 'reference_images'))
TEMP_IMAGE_PATH = os.getenv('TEMP_IMAGE_PATH', os.path.join(NOTES_DIR, 'temp'))

# Audio paths
MUSIC_DIR = os.getenv('MUSIC_DIR', '')
OUTPUT_DIR = os.getenv('OUTPUT_DIR', '')

# Reference images
REFERENCE_IMAGES = [
    "Note_H1.JPG", "Note_H2.JPG", "Note_H3.JPG", "Note_H4.JPG",
    "Note_H5.JPG", "Note_H6.JPG", "Note_H7.JPG", "Note_H8.JPG",
    "Note_H9.JPG", "Note_H10.JPG", "Note_H11.JPG", "Note_H12.JPG",
    "Note_H13.JPG", "Note_H14.JPG", "Note_H15.JPG", "Note_H16.JPG",
    "Note_PAUSE.JPG", "Note_DEMI_PAUSE.JPG", "BATON_MESURE.JPG",
    "Alteration_BEMOL.JPG", "Alteration_DIESE.JPG", 
    "Note_CLE_SOL.JPG", "Note_CLE_FA.JPG", "BATON_FIN_PORTEE.JPG"
]

# Token mappings
SOL_TOKENS = ["", "SOL_TOKEN_DO_MILIEU", "SOL_TOKEN_RE_L", "SOL_TOKEN_MI_L", 
              "SOL_TOKEN_FA_L", "SOL_TOKEN_SOL_L", "SOL_TOKEN_LA_L", "SOL_TOKEN_SI_L", 
              "SOL_TOKEN_DO_H", "SOL_TOKEN_RE_H", "SOL_TOKEN_MI_H", "SOL_TOKEN_FA_H", 
              "SOL_TOKEN_SOL_H", "SOL_TOKEN_LA_H", "FA_TOKEN_SI_H", "FA_TOKEN_DO_H"]

FA_TOKENS = ["FA_TOKEN_DO_L", "FA_TOKEN_RE_L", "FA_TOKEN_MI_L", "FA_TOKEN_FA_L", 
             "FA_TOKEN_SOL_L", "FA_TOKEN_LA_L", "FA_TOKEN_SI_L", "FA_TOKEN_DO_H", 
             "FA_TOKEN_RE_H", "FA_TOKEN_MI_H", "FA_TOKEN_FA_H", "FA_TOKEN_SOL_H", 
             "FA_TOKEN_LA_H", "FA_TOKEN_SI_H", "FA_TOKEN_DO_MILIEU", ""]

SOL_SHARP_TOKENS = ["FA_TOKEN_DO_L_SHARP", "FA_TOKEN_RE_L_SHARP", "", "FA_TOKEN_FA_L_SHARP", 
                     "FA_TOKEN_SOL_L_SHARP", "FA_TOKEN_LA_L_SHARP", "", "FA_TOKEN_DO_H_SHARP", 
                     "FA_TOKEN_RE_H_SHARP", "", "FA_TOKEN_FA_H_SHARP", "FA_TOKEN_SOL_H_SHARP", 
                     "FA_TOKEN_LA_H_SHARP", "", "FA_TOKEN_DO_MILIEU_SHARP", ""]

FA_SHARP_TOKENS = ["", "SOL_TOKEN_DO_MILIEU_SHARP", "SOL_TOKEN_RE_L_SHARP", "", 
                    "SOL_TOKEN_FA_L_SHARP", "SOL_TOKEN_SOL_L_SHARP", "SOL_TOKEN_LA_L_SHARP", "", 
                    "SOL_TOKEN_DO_H_SHARP", "SOL_TOKEN_RE_H_SHARP", "", "SOL_TOKEN_FA_H_SHARP", 
                    "SOL_TOKEN_SOL_H_SHARP", "SOL_TOKEN_LA_H_SHARP", "", ""]

FA_BEMOL_TOKENS = ["", "FA_TOKEN_RE_L_BEMOL", "FA_TOKEN_MI_L_BEMOL", "", 
                    "FA_TOKEN_SOL_L_BEMOL", "FA_TOKEN_LA_L_BEMOL", "FA_TOKEN_SI_L_BEMOL", "", 
                    "FA_TOKEN_RE_H_BEMOL", "FA_TOKEN_MI_H_BEMOL", "FA_TOKEN_FA_H", 
                    "FA_TOKEN_SOL_H_BEMOL", "FA_TOKEN_LA_H_BEMOL", "FA_TOKEN_SI_SI_BEMOL", "", ""]

SOL_BEMOL_TOKENS = ["", "", "SOL_TOKEN_RE_L_BEMOL", "SOL_TOKEN_MI_L_BEMOL", "", 
                     "SOL_TOKEN_SOL_L_BEMOL", "SOL_TOKEN_LA_L_BEMOL", "SOL_TOKEN_SI_L_BEMOL", "", 
                     "SOL_TOKEN_RE_H_BEMOL", "SOL_TOKEN_MI_H_BEMOL", "", "SOL_TOKEN_SOL_H_BEMOL", 
                     "SOL_TOKEN_LA_H_BEMOL", "FA_TOKEN_SI_H_BEMOL", ""]

# Function to ensure directories exist
def ensure_directories():
    """Ensure all required directories exist."""
    directories = [NOTES_DIR, TEMP_IMAGE_PATH, MUSIC_DIR, OUTPUT_DIR]
    for directory in directories:
        if directory:
            os.makedirs(directory, exist_ok=True)
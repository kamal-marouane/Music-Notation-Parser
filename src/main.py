"""
Main entry point for the Music Notation Parser.

This module provides the main functionality to parse musical
notation from Excel and generate audio output.
"""

import os
import sys
import logging
import argparse
from typing import Dict, Any, Optional, Tuple

from .config import (
    EXCEL_FILE_PATH, EXCEL_SHEET_NAME, NOTES_DIR, 
    MUSIC_DIR, OUTPUT_DIR, ensure_directories
)
from .parsers.excel_parser import ExcelReader
from .parsers.image_parser import NotationImageParser
from .parsers.music_parser import MusicNotationParser
from .audio.audio_generator import AudioGenerator


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("music_parser.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        Parsed command line arguments
    """
    parser = argparse.ArgumentParser(description='Music Notation Parser')
    
    parser.add_argument(
        '--excel', 
        type=str, 
        default=EXCEL_FILE_PATH,
        help='Path to the Excel file containing music notation'
    )
    
    parser.add_argument(
        '--sheet', 
        type=str, 
        default=EXCEL_SHEET_NAME,
        help='Name of the sheet in the Excel file'
    )
    
    parser.add_argument(
        '--notes-dir', 
        type=str, 
        default=NOTES_DIR,
        help='Directory containing music notation images'
    )
    
    parser.add_argument(
        '--music-dir', 
        type=str, 
        default=MUSIC_DIR,
        help='Directory containing note audio files'
    )
    
    parser.add_argument(
        '--output-dir', 
        type=str, 
        default=OUTPUT_DIR,
        help='Directory for output files'
    )
    
    parser.add_argument(
        '--play', 
        action='store_true',
        help='Play the generated audio after parsing'
    )
    
    return parser.parse_args()


def validate_paths(args: argparse.Namespace) -> bool:
    """
    Validate the required paths from arguments.
    
    Args:
        args: Command line arguments
        
    Returns:
        True if all paths are valid, False otherwise
    """
    # Check Excel file
    if not args.excel or not os.path.exists(args.excel):
        logger.error(f"Excel file not found: {args.excel}")
        return False
        
    # Check directories
    for dir_path, dir_name in [
        (args.notes_dir, "Notes directory"),
        (args.music_dir, "Music directory")
    ]:
        if not dir_path or not os.path.isdir(dir_path):
            logger.error(f"{dir_name} not found: {dir_path}")
            return False
            
    # Create output directory if it doesn't exist
    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
    
    return True


def initialize_components(args: argparse.Namespace) -> Tuple[ExcelReader, NotationImageParser, MusicNotationParser, AudioGenerator]:
    """
    Initialize the main components of the system.
    
    Args:
        args: Command line arguments
        
    Returns:
        Tuple of initialized components
    """
    # Initialize Excel reader
    excel_reader = ExcelReader(args.excel, args.sheet)
    
    # Initialize image parser
    image_parser = NotationImageParser(args.notes_dir)
    
    # Initialize music parser
    music_parser = MusicNotationParser(excel_reader, image_parser)
    
    # Initialize audio generator
    audio_generator = AudioGenerator(args.music_dir, args.output_dir)
    
    return excel_reader, image_parser, music_parser, audio_generator


def main() -> int:
    """
    Main entry point for the music notation parser.
    
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    logger.info("Starting Music Notation Parser")
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Ensure all required directories exist
    ensure_directories()
    
    # Validate paths
    if not validate_paths(args):
        return 1
        
    try:
        # Initialize components
        _, _, music_parser, audio_generator = initialize_components(args)
        
        # Parse the music notation
        success = music_parser.parse()
        
        if not success:
            logger.error(f"Parsing failed: {music_parser.error_message}")
            return 1
            
        # Get parsed notes
        fa_tokens, sol_tokens = music_parser.get_notes()
        
        if not fa_tokens and not sol_tokens:
            logger.warning("No notes were parsed")
            return 1
            
        # Generate audio
        fa_path, sol_path = audio_generator.generate_audio(fa_tokens, sol_tokens)
        
        logger.info(f"Generated audio files: {fa_path}, {sol_path}")
        
        # Play audio if requested
        if args.play:
            audio_generator.play_audio(fa_path, sol_path)
            
        logger.info("Music Notation Parser completed successfully")
        return 0
        
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
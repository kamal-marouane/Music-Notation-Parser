"""
Image parser module for recognizing musical notation images.

This module handles the recognition of musical notation from images.
"""

import os
import logging
from typing import Optional, Dict, Any

from ..config import (
    REFERENCE_IMAGES, REFERENCE_IMAGES_PATH,
    SOL_TOKENS, FA_TOKENS, SOL_SHARP_TOKENS, FA_SHARP_TOKENS,
    SOL_BEMOL_TOKENS, FA_BEMOL_TOKENS
)
from ..models.token import Token, TokenType, ClefType, AlterationType
from ..utils.image_utils import find_closest_match

logger = logging.getLogger(__name__)


class NotationImageParser:
    """
    Parser for music notation images.
    
    This class identifies musical symbols from images extracted from Excel.
    """
    
    def __init__(self, reference_dir: str = REFERENCE_IMAGES_PATH):
        """
        Initialize the image parser.
        
        Args:
            reference_dir: Directory containing reference images
        """
        self.reference_dir = reference_dir
        self.current_clef = ClefType.NONE
        self.current_alteration = AlterationType.NONE
        
    def reset_state(self) -> None:
        """Reset the parser state."""
        self.current_clef = ClefType.NONE
        self.current_alteration = AlterationType.NONE
        
    def parse_image(self, image_path: str) -> Optional[Token]:
        """
        Parse a musical notation image and identify the token.
        
        Args:
            image_path: Path to the image to parse
            
        Returns:
            A Token object representing the identified musical notation
        """
        if not os.path.exists(image_path):
            logger.error(f"Image file not found: {image_path}")
            return None
            
        # Find the closest matching reference image
        matched_image = find_closest_match(image_path, self.reference_dir, REFERENCE_IMAGES)
        
        if not matched_image:
            logger.warning(f"No match found for image: {image_path}")
            return self._create_unknown_token()
            
        # Identify the token based on the matched image
        return self._identify_token_from_match(matched_image)
        
    def _create_unknown_token(self) -> Token:
        """Create an unknown token."""
        return Token(
            type=TokenType.UNKNOWN,
            clef=self.current_clef,
            alteration=self.current_alteration
        )
        
    def _identify_token_from_match(self, matched_image: str) -> Token:
        """
        Identify a token based on the matched reference image.
        
        Args:
            matched_image: The filename of the matched reference image
            
        Returns:
            A Token object corresponding to the matched image
        """
        # Handle special case tokens
        if matched_image == "Note_CLE_SOL.JPG":
            self.current_clef = ClefType.SOL
            return Token(type=TokenType.CLEF_SOL, clef=self.current_clef)
            
        elif matched_image == "Note_CLE_FA.JPG":
            self.current_clef = ClefType.FA
            return Token(type=TokenType.CLEF_FA, clef=self.current_clef)
            
        elif matched_image == "Note_PAUSE.JPG":
            return Token(type=TokenType.PAUSE, clef=self.current_clef)
            
        elif matched_image == "Note_DEMI_PAUSE.JPG":
            return Token(type=TokenType.HALF_PAUSE, clef=self.current_clef)
            
        elif matched_image == "BATON_MESURE.JPG":
            return Token(type=TokenType.MEASURE_BAR, clef=self.current_clef)
            
        elif matched_image == "Alteration_BEMOL.JPG":
            self.current_alteration = AlterationType.BEMOL
            return Token(type=TokenType.ALTERATION_BEMOL, clef=self.current_clef)
            
        elif matched_image == "Alteration_DIESE.JPG":
            self.current_alteration = AlterationType.DIESE
            return Token(type=TokenType.ALTERATION_DIESE, clef=self.current_clef)
            
        elif matched_image == "BATON_FIN_PORTEE.JPG":
            return Token(type=TokenType.END_STAFF_BAR, clef=self.current_clef)
            
        # Handle note tokens based on current clef and alteration
        try:
            image_index = REFERENCE_IMAGES.index(matched_image)
            note_token = None
            
            # Determine the appropriate note token based on clef and alteration
            if self.current_clef == ClefType.SOL:
                if self.current_alteration == AlterationType.NONE:
                    note_token = SOL_TOKENS[image_index]
                elif self.current_alteration == AlterationType.DIESE:
                    note_token = SOL_SHARP_TOKENS[image_index]
                elif self.current_alteration == AlterationType.BEMOL:
                    note_token = SOL_BEMOL_TOKENS[image_index]
            elif self.current_clef == ClefType.FA:
                if self.current_alteration == AlterationType.NONE:
                    note_token = FA_TOKENS[image_index]
                elif self.current_alteration == AlterationType.DIESE:
                    note_token = FA_SHARP_TOKENS[image_index]
                elif self.current_alteration == AlterationType.BEMOL:
                    note_token = FA_BEMOL_TOKENS[image_index]
                    
            # Reset alteration after applying it
            self.current_alteration = AlterationType.NONE
            
            if note_token and note_token != "":
                return Token(
                    type=TokenType.NOTE, 
                    value=note_token,
                    clef=self.current_clef
                )
                
        except (ValueError, IndexError) as e:
            logger.warning(f"Error processing matched image {matched_image}: {e}")
            
        # Default to unknown token if not identified
        return self._create_unknown_token()
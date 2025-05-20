"""
Test cases for the image parser component.
"""

import os
import unittest
from unittest.mock import patch, MagicMock

from src.models.token import Token, TokenType, ClefType, AlterationType
from src.parsers.image_parser import NotationImageParser
from src.utils.image_utils import find_closest_match


class TestNotationImageParser(unittest.TestCase):
    """Test cases for the NotationImageParser class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.parser = NotationImageParser()
        
    def test_parser_initialization(self):
        """Test parser initialization."""
        self.assertEqual(self.parser.current_clef, ClefType.NONE)
        self.assertEqual(self.parser.current_alteration, AlterationType.NONE)
        
    def test_reset_state(self):
        """Test resetting parser state."""
        # Set some state
        self.parser.current_clef = ClefType.SOL
        self.parser.current_alteration = AlterationType.DIESE
        
        # Reset state
        self.parser.reset_state()
        
        # Verify reset
        self.assertEqual(self.parser.current_clef, ClefType.NONE)
        self.assertEqual(self.parser.current_alteration, AlterationType.NONE)
        
    @patch('src.utils.image_utils.find_closest_match')
    def test_parse_clef_sol(self, mock_find_closest_match):
        """Test parsing G clef image."""
        # Mock find_closest_match to return a G clef
        mock_find_closest_match.return_value = "Note_CLE_SOL.JPG"
        
        # Parse a mock image
        token = self.parser.parse_image("mock_image.jpg")
        
        # Verify the result
        self.assertEqual(token.type, TokenType.CLEF_SOL)
        self.assertEqual(self.parser.current_clef, ClefType.SOL)
        
    @patch('src.utils.image_utils.find_closest_match')
    def test_parse_clef_fa(self, mock_find_closest_match):
        """Test parsing F clef image."""
        # Mock find_closest_match to return an F clef
        mock_find_closest_match.return_value = "Note_CLE_FA.JPG"
        
        # Parse a mock image
        token = self.parser.parse_image("mock_image.jpg")
        
        # Verify the result
        self.assertEqual(token.type, TokenType.CLEF_FA)
        self.assertEqual(self.parser.current_clef, ClefType.FA)
        
    @patch('src.utils.image_utils.find_closest_match')
    def test_parse_alteration_diese(self, mock_find_closest_match):
        """Test parsing sharp alteration image."""
        # Mock find_closest_match to return a sharp alteration
        mock_find_closest_match.return_value = "Alteration_DIESE.JPG"
        
        # Parse a mock image
        token = self.parser.parse_image("mock_image.jpg")
        
        # Verify the result
        self.assertEqual(token.type, TokenType.ALTERATION_DIESE)
        self.assertEqual(self.parser.current_alteration, AlterationType.DIESE)
        
    @patch('src.utils.image_utils.find_closest_match')
    def test_parse_alteration_bemol(self, mock_find_closest_match):
        """Test parsing flat alteration image."""
        # Mock find_closest_match to return a flat alteration
        mock_find_closest_match.return_value = "Alteration_BEMOL.JPG"
        
        # Parse a mock image
        token = self.parser.parse_image("mock_image.jpg")
        
        # Verify the result
        self.assertEqual(token.type, TokenType.ALTERATION_BEMOL)
        self.assertEqual(self.parser.current_alteration, AlterationType.BEMOL)
        
    @patch('src.utils.image_utils.find_closest_match')
    def test_parse_note(self, mock_find_closest_match):
        """Test parsing note image."""
        # Set up clef context
        self.parser.current_clef = ClefType.SOL
        
        # Mock find_closest_match to return a note
        mock_find_closest_match.return_value = "Note_H1.JPG"
        
        # Parse a mock image
        token = self.parser.parse_image("mock_image.jpg")
        
        # Verify the result
        self.assertEqual(token.type, TokenType.NOTE)
        
    @patch('src.utils.image_utils.find_closest_match')
    def test_parse_unknown(self, mock_find_closest_match):
        """Test parsing unknown image."""
        # Mock find_closest_match to return None (no match)
        mock_find_closest_match.return_value = None
        
        # Parse a mock image
        token = self.parser.parse_image("mock_image.jpg")
        
        # Verify the result
        self.assertEqual(token.type, TokenType.UNKNOWN)
        
    @patch('os.path.exists')
    def test_nonexistent_image(self, mock_exists):
        """Test parsing nonexistent image."""
        # Mock os.path.exists to return False
        mock_exists.return_value = False
        
        # Parse a nonexistent image
        token = self.parser.parse_image("nonexistent.jpg")
        
        # Verify the result is None
        self.assertIsNone(token)


if __name__ == '__main__':
    unittest.main()
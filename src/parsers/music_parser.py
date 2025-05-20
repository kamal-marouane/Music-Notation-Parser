"""
Music parser module for analyzing musical notation.

This module provides the grammar and syntax parser for musical notation.
"""

import os
import logging
from typing import List, Dict, Optional, Tuple, Union

from ..models.token import Token, TokenType, ClefType, AlterationType
from ..parsers.excel_parser import ExcelReader
from ..parsers.image_parser import NotationImageParser

logger = logging.getLogger(__name__)


class MusicNotationParser:
    """
    Parser for musical notation.
    
    This class implements the grammar rules and syntax analysis
    for parsing musical notation.
    """
    
    def __init__(self, excel_reader: ExcelReader, image_parser: NotationImageParser):
        """
        Initialize the music parser.
        
        Args:
            excel_reader: Excel reader for extracting content
            image_parser: Image parser for identifying notation symbols
        """
        self.excel_reader = excel_reader
        self.image_parser = image_parser
        self.current_token = None
        self.has_error = False
        self.error_message = ""
        self.partition_name = ""
        self.instrument_name = ""
        self.meter_value = -1
        self.meter_controller = -1
        self.note_tokens_fa = []
        self.note_tokens_sol = []
        
    def reset_state(self) -> None:
        """Reset the parser state."""
        self.current_token = None
        self.has_error = False
        self.error_message = ""
        self.partition_name = ""
        self.instrument_name = ""
        self.meter_value = -1
        self.meter_controller = -1
        self.note_tokens_fa = []
        self.note_tokens_sol = []
        self.image_parser.reset_state()
        
    def parse(self) -> bool:
        """
        Parse the musical notation.
        
        Returns:
            True if parsing was successful, False otherwise
        """
        self.reset_state()
        self._read_next_token()
        
        try:
            self._parse_partition()
            return not self.has_error
        except Exception as e:
            logger.error(f"Parsing error: {e}")
            self.has_error = True
            self.error_message = f"Unexpected error during parsing: {e}"
            return False
            
    def get_notes(self) -> Tuple[List[str], List[str]]:
        """
        Get the parsed note tokens.
        
        Returns:
            A tuple containing lists of FA and SOL note tokens
        """
        return self.note_tokens_fa, self.note_tokens_sol
        
    def _read_next_token(self) -> None:
        """Read the next token from the source."""
        if self.excel_reader.has_text_content():
            self._process_text_content()
        elif self.excel_reader.has_image_content():
            self._process_image_content()
        else:
            # No content in current cell, move to next one
            self.excel_reader.move_to_next_empty_cell()
            self._read_next_token()
            
    def _process_text_content(self) -> None:
        """Process text content from the current cell."""
        char = self.excel_reader.read_next_char()
        
        if char is None:
            self._read_next_token()
            return
            
        # Skip whitespace
        while char and char.isspace():
            char = self.excel_reader.read_next_char()
            if char is None:
                self._read_next_token()
                return
        
        # Parse tokens based on the first character
        if char == ':':
            self.current_token = Token(type=TokenType.COLON)
        elif char == '.':
            self.current_token = Token(type=TokenType.PERIOD)
        elif char == ';':
            self.current_token = Token(type=TokenType.SEMICOLON)
        elif char and char.isdigit():
            # Parse meter value
            value = int(char)
            self.meter_value = value
            self.meter_controller = value
            self.current_token = Token(type=TokenType.METER, value=value)
        elif char and char.isalpha():
            # Parse keyword or identifier
            keyword = char
            next_char = self.excel_reader.read_next_char()
            
            while next_char and (next_char.isalpha() or next_char.isdigit()):
                keyword += next_char
                next_char = self.excel_reader.read_next_char()
                
            if keyword == "Nom":
                self.current_token = Token(type=TokenType.NAME)
            elif keyword == "Instrument":
                self.current_token = Token(type=TokenType.INSTRUMENT)
            elif keyword == "FIN":
                self.current_token = Token(type=TokenType.END_OF_PARTITION)
            else:
                # Save identifier value for later use
                self.current_token = Token(type=TokenType.IDENTIFIER, value=keyword)
        else:
            # Unknown token
            self.current_token = Token(type=TokenType.UNKNOWN, value=char if char else "")
            
    def _process_image_content(self) -> None:
        """Process image content from the current cell."""
        image_path = self.excel_reader.read_image()
        
        if not image_path:
            self._read_next_token()
            return
            
        # Parse the image using the image parser
        self.current_token = self.image_parser.parse_image(image_path)
        
        if not self.current_token:
            self.current_token = Token(type=TokenType.UNKNOWN)
            
    def _error(self, context: str) -> None:
        """
        Record a parsing error.
        
        Args:
            context: Error context description
        """
        self.has_error = True
        self.error_message = f"Syntax error in {context}: Unexpected token {self.current_token}"
        logger.error(self.error_message)
        
    def _expect(self, expected_type: TokenType, context: str) -> bool:
        """
        Check if the current token matches the expected type.
        
        Args:
            expected_type: The expected token type
            context: Error context description
            
        Returns:
            True if the token matches, False otherwise
        """
        if self.current_token.type != expected_type:
            self._error(f"{context} (expected {expected_type.name}, got {self.current_token.type.name})")
            return False
            
        self._read_next_token()
        return True
        
    def _parse_partition(self) -> None:
        """Parse the top-level partition structure."""
        logger.info("Parsing partition")
        
        # Expect "Nom" token
        if not self._expect(TokenType.NAME, "partition name declaration"):
            return
            
        # Expect colon
        if not self._expect(TokenType.COLON, "partition name declaration"):
            return
            
        # Expect partition name (identifier)
        if not self._expect(TokenType.IDENTIFIER, "partition name"):
            return
        else:
            self.partition_name = self.current_token.value
            
        # Expect semicolon
        if not self._expect(TokenType.SEMICOLON, "partition name terminator"):
            return
            
        # Expect "Instrument" token
        if not self._expect(TokenType.INSTRUMENT, "instrument declaration"):
            return
            
        # Expect colon
        if not self._expect(TokenType.COLON, "instrument declaration"):
            return
            
        # Expect instrument name (identifier)
        if not self._expect(TokenType.IDENTIFIER, "instrument name"):
            return
        else:
            self.instrument_name = self.current_token.value
            
        # Expect period
        if not self._expect(TokenType.PERIOD, "instrument declaration terminator"):
            return
            
        # Parse staff notation
        self._parse_multiple_staffs()
        
        # Expect end of partition
        if not self._expect(TokenType.END_OF_PARTITION, "end of partition"):
            return
            
    def _parse_multiple_staffs(self) -> None:
        """Parse multiple music staffs."""
        logger.info("Parsing multiple staffs")
        
        if self.current_token.type == TokenType.END_OF_PARTITION:
            return
            
        if self.current_token.type in [TokenType.CLEF_SOL, TokenType.CLEF_FA]:
            self._parse_staff()
            self.meter_value = -1
            self.meter_controller = -1
            self._parse_multiple_staffs()
        else:
            self._error("multiple staffs")
            
    def _parse_staff(self) -> None:
        """Parse a single music staff."""
        logger.info("Parsing staff")
        
        # We already know we have a clef (checked in _parse_multiple_staffs)
        clef = self.current_token.type
        self._read_next_token()
        
        # Parse meter if present
        self._parse_meter()
        
        # Parse measures
        self._parse_measures()
        
    def _parse_meter(self) -> None:
        """Parse the meter (time signature)."""
        logger.info("Parsing meter")
        
        if self.current_token.type == TokenType.METER:
            self._read_next_token()
        elif self.current_token.type in [
            TokenType.ALTERATION_DIESE, TokenType.ALTERATION_BEMOL,
            TokenType.PAUSE, TokenType.HALF_PAUSE, TokenType.NOTE
        ]:
            # No meter specified, continue with other symbols
            pass
        else:
            self._error("meter")
            
    def _parse_measures(self) -> None:
        """Parse music measures."""
        logger.info("Parsing measures")
        
        self._parse_measure()
        self._parse_additional_measures()
        
        if not self._expect(TokenType.END_STAFF_BAR, "end of staff"):
            return
            
    def _parse_measure(self) -> None:
        """Parse a single music measure."""
        logger.info("Parsing measure")
        
        self._parse_symbols()
        
        # Validate measure content against meter
        if self.meter_value != -1 and self.meter_controller != 0:
            logger.warning(f"Semantic error: Measure content does not match meter value {self.meter_value}")
            # Reset meter controller for next measure
            self.meter_controller = self.meter_value
            
    def _parse_symbols(self) -> None:
        """Parse musical symbols within a measure."""
        logger.info("Parsing symbols")
        
        self._parse_symbol()
        self._parse_additional_symbols()
        
    def _parse_symbol(self) -> None:
        """Parse a single musical symbol."""
        logger.info(f"Parsing symbol: {self.current_token}")
        
        # Decrement meter counter for each symbol
        if self.meter_controller > 0:
            self.meter_controller -= 1
            
        if (self.current_token.type in [TokenType.ALTERATION_DIESE, TokenType.ALTERATION_BEMOL, TokenType.NOTE]):
            self._parse_note()
        elif self.current_token.type in [TokenType.PAUSE, TokenType.HALF_PAUSE]:
            self._parse_silence()
        else:
            self._error("symbol")
            
        self._read_next_token()
        
    def _parse_note(self) -> None:
        """Parse a musical note."""
        logger.info("Parsing note")
        
        # Parse alteration if present
        self._parse_alteration()
        
        # Parse note height
        self._parse_note_height()
        
    def _parse_alteration(self) -> None:
        """Parse note alteration (sharp/flat)."""
        logger.info("Parsing alteration")
        
        if self.current_token.type in [TokenType.ALTERATION_DIESE, TokenType.ALTERATION_BEMOL]:
            self._read_next_token()
        elif self.current_token.type != TokenType.NOTE:
            self._error("alteration")
            
    def _parse_note_height(self) -> None:
        """Parse note height."""
        logger.info("Parsing note height")
        
        if self.current_token.type == TokenType.NOTE:
            note_token = self.current_token.value
            if note_token:  # Add note to appropriate list based on clef
                if note_token.startswith("FA_TOKEN"):
                    note_with_instrument = f"{note_token}_{self.instrument_name}"
                    self.note_tokens_fa.append(note_with_instrument)
                else:
                    note_with_instrument = f"{note_token}_{self.instrument_name}"
                    self.note_tokens_sol.append(note_with_instrument)
        else:
            self._error("note height")
            
    def _parse_silence(self) -> None:
        """Parse a silence (rest)."""
        logger.info("Parsing silence")
        
        # Add silence to both clef lists to maintain synchronization
        # This could be enhanced to be more specific to the current clef
        silence_type = self.current_token.type.name
        if self.current_token.clef == ClefType.FA:
            self.note_tokens_fa.append(silence_type)
        else:
            self.note_tokens_sol.append(silence_type)
            
    def _parse_additional_symbols(self) -> None:
        """Parse additional symbols in a measure."""
        logger.info("Parsing additional symbols")
        
        symbol_types = [
            TokenType.ALTERATION_DIESE, TokenType.ALTERATION_BEMOL,
            TokenType.PAUSE, TokenType.HALF_PAUSE, TokenType.NOTE
        ]
        
        if self.current_token.type in symbol_types:
            self._parse_symbol()
            self._parse_additional_symbols()
        elif self.current_token.type not in [
            TokenType.END_STAFF_BAR, TokenType.MEASURE_BAR,
            TokenType.CLEF_SOL, TokenType.CLEF_FA, TokenType.END_OF_PARTITION
        ]:
            self._error("additional symbols")
            
    def _parse_additional_measures(self) -> None:
        """Parse additional measures in a staff."""
        logger.info("Parsing additional measures")
        
        if self.current_token.type == TokenType.MEASURE_BAR:
            self._read_next_token()
            self._parse_measure()
            self._parse_additional_measures()
        elif self.current_token.type != TokenType.END_STAFF_BAR:
            self._error("additional measures")
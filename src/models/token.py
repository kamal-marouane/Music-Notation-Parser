"""
Token model definitions for the music notation parser.

This module contains the token model and related enumerations.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, Union


class TokenType(Enum):
    """Enumeration of token types used in the music notation parser."""
    # Special tokens
    UNKNOWN = auto()
    END_OF_PARTITION = auto()
    
    # Text tokens
    NAME = auto()
    IDENTIFIER = auto()
    INSTRUMENT = auto()
    COLON = auto()
    SEMICOLON = auto()
    PERIOD = auto()
    METER = auto()
    
    # Clef tokens
    CLEF_SOL = auto()
    CLEF_FA = auto()
    
    # Music symbols
    NOTE = auto()
    PAUSE = auto()
    HALF_PAUSE = auto()
    ALTERATION_BEMOL = auto()
    ALTERATION_DIESE = auto()
    MEASURE_BAR = auto()
    END_STAFF_BAR = auto()


class ClefType(Enum):
    """Enumeration of musical clef types."""
    NONE = auto()
    SOL = auto()
    FA = auto()


class AlterationType(Enum):
    """Enumeration of musical alteration types."""
    NONE = auto()
    DIESE = auto()
    BEMOL = auto()


@dataclass
class Token:
    """
    Represents a token in the music notation parser.
    
    Attributes:
        type: The type of token
        value: The value associated with the token (if any)
        clef: The current clef context
        alteration: The current alteration context
        line: The line number in the source file
        column: The column number in the source file
    """
    type: TokenType
    value: Optional[Union[str, int]] = None
    clef: ClefType = ClefType.NONE
    alteration: AlterationType = AlterationType.NONE
    line: int = 0
    column: str = ""
    
    def __str__(self) -> str:
        """String representation of the token."""
        if self.value is not None:
            return f"Token({self.type.name}, {self.value})"
        return f"Token({self.type.name})"


def get_token_type_from_string(token_str: str) -> TokenType:
    """
    Map a string token name to its TokenType enum value.
    
    Args:
        token_str: The string representation of the token
        
    Returns:
        The corresponding TokenType enum value
    """
    token_mapping = {
        "TOKEN_INCONNU": TokenType.UNKNOWN,
        "TOKEN_EO_PARTITION": TokenType.END_OF_PARTITION,
        "TOKEN_NOM": TokenType.NAME,
        "TOKEN_ID": TokenType.IDENTIFIER,
        "TOKEN_INSTRUMENT": TokenType.INSTRUMENT,
        "TOKEN_DP": TokenType.COLON,
        "TOKEN_PV": TokenType.SEMICOLON,
        "TOKEN_PT": TokenType.PERIOD,
        "TOKEN_METER": TokenType.METER,
        "TOKEN_CLE_SOL": TokenType.CLEF_SOL,
        "TOKEN_CLE_FA": TokenType.CLEF_FA,
        "TOKEN_PAUSE": TokenType.PAUSE,
        "TOKEN_DEMI_PAUSE": TokenType.HALF_PAUSE,
        "TOKEN_ALT_BEMOL": TokenType.ALTERATION_BEMOL,
        "TOKEN_ALT_DIESE": TokenType.ALTERATION_DIESE,
        "TOKEN_BATON_MESURE": TokenType.MEASURE_BAR,
        "TOKEN_BATON_FIN_PORTEE": TokenType.END_STAFF_BAR
    }
    
    # Check if it's a standard token
    if token_str in token_mapping:
        return token_mapping[token_str]
    
    # If it's a note token
    if token_str.startswith("SOL_TOKEN") or token_str.startswith("FA_TOKEN"):
        return TokenType.NOTE
        
    # Default to unknown
    return TokenType.UNKNOWN
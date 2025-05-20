"""
File utility functions for the music notation parser.

This module provides helper functions for file operations.
"""

import os
import logging
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


def ensure_file_exists(file_path: str) -> bool:
    """
    Check if file exists and is accessible.
    
    Args:
        file_path: Path to the file to check
        
    Returns:
        True if the file exists, False otherwise
        
    Raises:
        FileNotFoundError: If the file does not exist
    """
    if not file_path:
        raise ValueError("File path is empty")
        
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    if not os.path.isfile(file_path):
        raise ValueError(f"Path exists but is not a file: {file_path}")
        
    return True


def ensure_directory_exists(dir_path: str) -> bool:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        dir_path: Path to the directory
        
    Returns:
        True if the directory exists or was created successfully
    """
    if not dir_path:
        raise ValueError("Directory path is empty")
        
    try:
        os.makedirs(dir_path, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {dir_path}: {e}")
        return False


def list_files_with_extension(directory: str, extension: str) -> List[str]:
    """
    List all files in a directory with a specific extension.
    
    Args:
        directory: Path to the directory to search
        extension: File extension to filter by (e.g., '.jpg')
        
    Returns:
        List of file paths matching the extension
    """
    if not os.path.exists(directory) or not os.path.isdir(directory):
        logger.warning(f"Directory does not exist: {directory}")
        return []
        
    if not extension.startswith('.'):
        extension = f'.{extension}'
        
    try:
        return [os.path.join(directory, f) for f in os.listdir(directory) 
                if f.lower().endswith(extension.lower())]
    except Exception as e:
        logger.error(f"Error listing files in {directory}: {e}")
        return []


def get_file_name_without_extension(file_path: str) -> str:
    """
    Get file name without extension from a file path.
    
    Args:
        file_path: Path to the file
        
    Returns:
        The file name without extension
    """
    return os.path.splitext(os.path.basename(file_path))[0]


def join_paths(*args) -> str:
    """
    Join path components safely.
    
    Args:
        *args: Path components to join
        
    Returns:
        The joined path
    """
    return os.path.join(*args)
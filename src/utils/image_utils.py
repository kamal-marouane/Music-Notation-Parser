"""
Image processing utilities for music notation recognition.

This module provides image comparison and matching functionality
for recognizing musical notation symbols.
"""

import os
import logging
from typing import List, Tuple, Optional
from PIL import Image
import imagehash
from ..config import REFERENCE_IMAGES_PATH, REFERENCE_IMAGES

logger = logging.getLogger(__name__)


def calculate_image_hash(image_path: str) -> Optional[imagehash.ImageHash]:
    """
    Calculate the perceptual hash of an image.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        The perceptual hash of the image or None if failed
    """
    try:
        img = Image.open(image_path)
        return imagehash.average_hash(img)
    except Exception as e:
        logger.error(f"Failed to calculate hash for image {image_path}: {e}")
        return None


def find_closest_match(image_path: str, reference_dir: str = REFERENCE_IMAGES_PATH, 
                       reference_images: List[str] = REFERENCE_IMAGES) -> Optional[str]:
    """
    Find the closest matching reference image for a given image.
    
    Args:
        image_path: Path to the image to match
        reference_dir: Directory containing reference images
        reference_images: List of reference image filenames
        
    Returns:
        The filename of the closest matching reference image or None if failed
    """
    try:
        input_hash = calculate_image_hash(image_path)
        if input_hash is None:
            return None
            
        closest_images = []
        closest_distance = float("inf")
        
        for ref_image in reference_images:
            ref_path = os.path.join(reference_dir, ref_image)
            if not os.path.exists(ref_path):
                logger.warning(f"Reference image not found: {ref_path}")
                continue
                
            reference_hash = calculate_image_hash(ref_path)
            if reference_hash is None:
                continue
                
            distance = input_hash - reference_hash
            
            if distance < closest_distance:
                closest_distance = distance
                closest_images = [ref_image]
            elif distance == closest_distance:
                closest_images.append(ref_image)
                
        if closest_images:
            logger.debug(f"Closest match for {image_path}: {closest_images[0]} (distance: {closest_distance})")
            return closest_images[0]
        else:
            logger.warning(f"No match found for {image_path}")
            return None
            
    except Exception as e:
        logger.error(f"Error matching image {image_path}: {e}")
        return None


def get_hash_distance(image1_path: str, image2_path: str) -> Optional[int]:
    """
    Calculate the perceptual hash distance between two images.
    
    Args:
        image1_path: Path to the first image
        image2_path: Path to the second image
        
    Returns:
        The distance between the image hashes or None if failed
    """
    try:
        hash1 = calculate_image_hash(image1_path)
        hash2 = calculate_image_hash(image2_path)
        
        if hash1 is None or hash2 is None:
            return None
            
        return hash1 - hash2
    except Exception as e:
        logger.error(f"Error calculating hash distance: {e}")
        return None
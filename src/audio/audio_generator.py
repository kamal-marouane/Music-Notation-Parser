"""
Audio generator module for creating music from parsed notation.

This module handles the creation and playback of audio from parsed notation.
"""

import os
import logging
from typing import List, Tuple, Optional
import pygame
from moviepy.editor import concatenate_audioclips, AudioFileClip

from ..config import MUSIC_DIR, OUTPUT_DIR
from ..utils.file_utils import ensure_directory_exists

logger = logging.getLogger(__name__)


class AudioGenerator:
    """
    Generator for audio from parsed music notation.
    
    This class creates and plays audio from parsed music notation tokens.
    """
    
    def __init__(self, music_dir: str = MUSIC_DIR, output_dir: str = OUTPUT_DIR):
        """
        Initialize the audio generator.
        
        Args:
            music_dir: Directory containing note audio files
            output_dir: Directory for output audio files
        """
        self.music_dir = music_dir
        self.output_dir = output_dir
        ensure_directory_exists(self.output_dir)
        
    def generate_audio(self, fa_tokens: List[str], sol_tokens: List[str]) -> Tuple[str, str]:
        """
        Generate audio files from parsed music tokens.
        
        Args:
            fa_tokens: List of F-clef (bass) note tokens
            sol_tokens: List of G-clef (treble) note tokens
            
        Returns:
            Tuple of paths to generated FA and SOL audio files
        """
        logger.info(f"Generating audio from {len(fa_tokens)} FA tokens and {len(sol_tokens)} SOL tokens")
        
        fa_clips = self._prepare_audio_clips(fa_tokens)
        sol_clips = self._prepare_audio_clips(sol_tokens)
        
        # Generate FA audio file
        fa_output_path = os.path.join(self.output_dir, "output_fa.mp3")
        self._create_audio_file(fa_clips, fa_output_path)
        
        # Generate SOL audio file
        sol_output_path = os.path.join(self.output_dir, "output_sol.mp3")
        self._create_audio_file(sol_clips, sol_output_path)
        
        return fa_output_path, sol_output_path
        
    def _prepare_audio_clips(self, tokens: List[str]) -> List[AudioFileClip]:
        """
        Prepare audio clips from token list.
        
        Args:
            tokens: List of note tokens
            
        Returns:
            List of AudioFileClip objects
        """
        clips = []
        
        for token in tokens:
            # Find the appropriate audio file for the token
            audio_path = self._get_audio_path(token)
            
            if audio_path and os.path.exists(audio_path):
                try:
                    # Load the audio clip and trim any silence at the end
                    clip = AudioFileClip(audio_path).subclip(0, -1.3)
                    clips.append(clip)
                except Exception as e:
                    logger.error(f"Error loading audio clip {audio_path}: {e}")
            else:
                logger.warning(f"Audio file not found for token: {token}")
                
        return clips
        
    def _get_audio_path(self, token: str) -> Optional[str]:
        """
        Get the audio file path for a token.
        
        Args:
            token: Note token
            
        Returns:
            Path to the corresponding audio file or None if not found
        """
        audio_filename = f"{token}.mp3"
        audio_path = os.path.join(self.music_dir, audio_filename)
        
        if not os.path.exists(audio_path):
            logger.warning(f"Audio file not found: {audio_path}")
            return None
            
        return audio_path
        
    def _create_audio_file(self, clips: List[AudioFileClip], output_path: str) -> bool:
        """
        Create an audio file from a list of clips.
        
        Args:
            clips: List of audio clips
            output_path: Path to save the output file
            
        Returns:
            True if successful, False otherwise
        """
        if not clips:
            logger.warning("No audio clips to concatenate")
            return False
            
        try:
            final_clip = concatenate_audioclips(clips)
            final_clip.write_audiofile(output_path, logger=None)
            logger.info(f"Audio file created: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error creating audio file {output_path}: {e}")
            return False
            
    def play_audio(self, fa_path: str, sol_path: str) -> None:
        """
        Play the generated audio files.
        
        Args:
            fa_path: Path to the FA audio file
            sol_path: Path to the SOL audio file
        """
        logger.info("Playing audio")
        
        try:
            # Initialize pygame mixer
            pygame.mixer.init()
            
            # Load and play the FA audio file
            pygame.mixer.music.load(fa_path)
            pygame.mixer.music.play()
            
            # Load and play the SOL audio file simultaneously
            sound = pygame.mixer.Sound(sol_path)
            sound.play()
            
            logger.info("Audio playback started")
        except Exception as e:
            logger.error(f"Error playing audio: {e}")
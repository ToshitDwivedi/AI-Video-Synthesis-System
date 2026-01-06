"""
Simple TTS Generator using pyttsx3 (Windows built-in voices)
Lightweight alternative to Coqui TTS - no compilation needed
"""

import logging
from pathlib import Path
from typing import Dict
import pyttsx3

logger = logging.getLogger('video_synthesis.simple_tts')


class SimpleTTSGenerator:
    """Generate speech audio using pyttsx3 (Windows SAPI5)."""
    
    def __init__(self, config: dict):
        """Initialize TTS generator."""
        self.config = config
        self.output_dir = Path(config['output']['audio_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize pyttsx3 engine
        try:
            self.engine = pyttsx3.init()
            
            # Configure voice settings
            voices = self.engine.getProperty('voices')
            if voices:
                # Use first available voice (usually Microsoft David/Zira)
                self.engine.setProperty('voice', voices[0].id)
            
            # Set speech rate (words per minute)
            rate = self.engine.getProperty('rate')
            self.engine.setProperty('rate', rate - 20)  # Slightly slower for clarity
            
            logger.info("SimpleTTS initialized with Windows SAPI5 voices")
        except Exception as e:
            logger.error(f"Failed to initialize pyttsx3: {e}")
            self.engine = None
    
    def generate_narration(self, script: Dict, topic: str) -> Dict:
        """
        Generate audio narration for all scenes.
        
        Args:
            script: Script dictionary with scenes
            topic: Topic name for file naming
            
        Returns:
            Dictionary mapping scene_id to audio file path
        """
        if not self.engine:
            logger.warning("TTS engine not available")
            return {}
        
        logger.info(f"Generating narration for {len(script['scenes'])} scenes")
        
        audio_files = {}
        
        for i, scene in enumerate(script['scenes'], 1):
            scene_id = scene.get('scene_id', i)
            text = scene.get('narration', '')
            
            if not text:
                logger.warning(f"Scene {scene_id} has no narration, skipping")
                continue
            
            logger.info(f"Generating audio for scene {scene_id}")
            audio_path = self._generate_scene_audio(topic, scene_id, text)
            if audio_path:
                audio_files[scene_id] = str(audio_path)
        
        # Generate combined narration
        logger.info("Generating combined narration")
        full_narration = ' '.join(
            scene.get('narration', '') for scene in script['scenes']
        )
        combined_path = self._generate_combined_audio(topic, full_narration)
        if combined_path:
            audio_files['combined'] = str(combined_path)
        
        logger.info(f"Generated {len(audio_files)} audio files")
        return audio_files
    
    def _generate_scene_audio(self, topic: str, scene_id: int, text: str) -> Path:
        """Generate audio for a single scene."""
        try:
            filename = f"{self._sanitize_filename(topic)}_scene_{scene_id}.wav"
            output_path = self.output_dir / filename
            
            # Clean text
            text = self._clean_text(text)
            
            # Generate audio
            self.engine.save_to_file(text, str(output_path))
            self.engine.runAndWait()
            
            logger.debug(f"Audio saved to: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to generate audio for scene {scene_id}: {e}")
            return None
    
    def _generate_combined_audio(self, topic: str, text: str) -> Path:
        """Generate combined audio for entire script."""
        try:
            filename = f"{self._sanitize_filename(topic)}_full.wav"
            output_path = self.output_dir / filename
            
            text = self._clean_text(text)
            
            self.engine.save_to_file(text, str(output_path))
            self.engine.runAndWait()
            
            logger.debug(f"Combined audio saved to: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to generate combined audio: {e}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """Clean text for TTS."""
        text = text.strip('"\'')
        text = ' '.join(text.split())
        text = text.replace('[', '').replace(']', '')
        return text
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize filename."""
        return name.lower().replace(' ', '_').replace('/', '_')

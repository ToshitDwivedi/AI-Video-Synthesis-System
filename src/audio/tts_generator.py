"""
TTS Generator - Text-to-Speech using Coqui TTS (open-source)
"""

import logging
from pathlib import Path
from typing import List, Dict

# Make TTS optional for testing
try:
    from TTS.api import TTS
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("Warning: TTS not installed. Audio generation will be disabled.")

logger = logging.getLogger('video_synthesis.tts')


class TTSGenerator:
    """Generate speech audio from text using Coqui TTS."""
    
    def __init__(self, config: dict):
        """
        Initialize TTS generator.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.tts_config = config['tts']
        self.output_dir = Path(config['output']['audio_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        if not TTS_AVAILABLE:
            logger.warning("TTS not available - audio generation disabled")
            self.tts = None
            return
        
        # Initialize TTS model
        model_name = self.tts_config['model']
        logger.info(f"Loading TTS model: {model_name}")
        
        try:
            self.tts = TTS(model_name=model_name, progress_bar=False)
            logger.info("TTS model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load TTS model: {e}")
            logger.info("Using default English model as fallback")
            self.tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
    
    def generate_narration(self, script: Dict, topic: str) -> Dict:
        """
        Generate audio narration for all scenes in the script.
        
        Args:
            script: Script dictionary with scenes
            topic: Topic name for file naming
            
        Returns:
            Dictionary mapping scene_id to audio file path
        """
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
            audio_files[scene_id] = str(audio_path)
        
        # Also generate a combined audio file
        logger.info("Generating combined narration")
        full_narration = self._combine_narrations(script['scenes'])
        combined_path = self._generate_combined_audio(topic, full_narration)
        audio_files['combined'] = str(combined_path)
        
        logger.info(f"Generated {len(audio_files)} audio files")
        return audio_files
    
    def _generate_scene_audio(self, topic: str, scene_id: int, text: str) -> Path:
        """Generate audio for a single scene."""
        filename = f"{self._sanitize_filename(topic)}_scene_{scene_id}.wav"
        output_path = self.output_dir / filename
        
        # Clean text for TTS
        text = self._clean_text_for_tts(text)
        
        # Generate audio
        self.tts.tts_to_file(
            text=text,
            file_path=str(output_path),
            speed=self.tts_config.get('voice_speed', 1.0)
        )
        
        logger.debug(f"Audio saved to: {output_path}")
        return output_path
    
    def _generate_combined_audio(self, topic: str, text: str) -> Path:
        """Generate combined audio for entire script."""
        filename = f"{self._sanitize_filename(topic)}_full.wav"
        output_path = self.output_dir / filename
        
        text = self._clean_text_for_tts(text)
        
        self.tts.tts_to_file(
            text=text,
            file_path=str(output_path),
            speed=self.tts_config.get('voice_speed', 1.0)
        )
        
        logger.debug(f"Combined audio saved to: {output_path}")
        return output_path
    
    def _combine_narrations(self, scenes: List[Dict]) -> str:
        """Combine all scene narrations into one text."""
        narrations = [scene['narration'] for scene in scenes]
        return ' '.join(narrations)
    
    def _clean_text_for_tts(self, text: str) -> str:
        """Clean and prepare text for TTS."""
        # Remove quotes
        text = text.strip('"\'')
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove problematic characters
        text = text.replace('[', '').replace(']', '')
        
        return text
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize filename."""
        return name.lower().replace(' ', '_').replace('/', '_')

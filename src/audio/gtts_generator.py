"""
Google TTS Generator - Fast and reliable alternative
Uses Google's Text-to-Speech API (requires internet)
"""

import logging
from pathlib import Path
from typing import Dict
from gtts import gTTS

logger = logging.getLogger('video_synthesis.gtts')


class GoogleTTSGenerator:
    """Generate speech audio using Google TTS."""
    
    def __init__(self, config: dict):
        """Initialize TTS generator."""
        self.config = config
        self.output_dir = Path(config['output']['audio_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Google TTS initialized")
    
    def generate_narration(self, script: Dict, topic: str) -> Dict:
        """Generate audio narration for all scenes."""
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
        
        logger.info(f"Generated {len(audio_files)} audio files")
        return audio_files
    
    def _generate_scene_audio(self, topic: str, scene_id: int, text: str) -> Path:
        """Generate audio for a single scene."""
        try:
            filename = f"{self._sanitize_filename(topic)}_scene_{scene_id}.mp3"
            output_path = self.output_dir / filename
            
            # Clean text
            text = self._clean_text(text)
            
            # Generate audio using Google TTS
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(str(output_path))
            
            logger.info(f"Audio saved to: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to generate audio for scene {scene_id}: {e}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """Clean text for TTS."""
        text = text.strip('"\'')
        text = ' '.join(text.split())
        text = text.replace('[', '').replace(']', '')
        # Remove unicode characters that might cause issues
        text = text.replace('–', '-').replace('—', '-')
        return text
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize filename."""
        return name.lower().replace(' ', '_').replace('/', '_')

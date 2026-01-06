"""
Video Generator - Component 3: Blueprint to MP4
Generates final video with audio and animations.
"""

import logging
from pathlib import Path
from typing import Dict

# Use Google TTS - faster and more reliable
from .audio.gtts_generator import GoogleTTSGenerator
from .renderers.simple_renderer import SimpleVideoRenderer

logger = logging.getLogger('video_synthesis.video_generator')


class VideoGenerator:
    """Generates final MP4 video from blueprint."""
    
    def __init__(self, config: dict):
        """Initialize video generator."""
        self.config = config
        self.output_dir = Path(config['output']['videos_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.tts = GoogleTTSGenerator(config)
        self.renderer = SimpleVideoRenderer(config)
    
    def generate_video(self, script: Dict, blueprint: Dict, topic: str) -> Path:
        """
        Generate complete video from blueprint and script.
        
        Args:
            script: Script dictionary with narrations
            blueprint: Animation blueprint
            topic: Topic name
            
        Returns:
            Path to final MP4 video file
        """
        logger.info(f"Starting video generation for: {topic}")
        
        # Step 1: Generate narration audio
        logger.info("Step 1: Generating narration audio")
        audio_files = self.tts.generate_narration(script, topic)
        
        # Step 2: Render video scenes
        logger.info("Step 2: Rendering video scenes")
        frame_paths = self.renderer.render_blueprint(blueprint, audio_files)
        
        # Step 3: Combine into final video
        logger.info("Step 3: Creating final MP4")
        
        # Get audio paths in order - handle missing entries properly
        audio_paths = []
        for i, scene in enumerate(script['scenes'], 1):
            scene_id = scene.get('scene_id', i)
            audio_file = audio_files.get(scene_id, '')
            if audio_file and audio_file != '':
                audio_path = Path(audio_file)
                audio_paths.append(audio_path if audio_path.exists() and audio_path.is_file() else None)
            else:
                audio_paths.append(None)
        
        # Output path
        safe_topic = topic.lower().replace(' ', '_').replace('/', '_')
        output_path = self.output_dir / f"{safe_topic}.mp4"
        
        # Create video
        final_video = self.renderer.create_video_from_frames(
            frame_paths,
            audio_paths,
            output_path
        )
        
        if final_video:
            logger.info(f"Video generation complete: {final_video}")
            return final_video
        else:
            raise Exception("Failed to generate video")

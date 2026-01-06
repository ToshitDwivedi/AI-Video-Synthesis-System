"""
End-to-End Pipeline - Orchestrates the complete video synthesis pipeline
Topic → Script → Blueprint → MP4
"""

import logging
from pathlib import Path
from typing import Optional, Dict

from .script_generator import ScriptGenerator
from .blueprint_generator import BlueprintGenerator
from .video_generator import VideoGenerator
from .utils import load_config, setup_logging, load_style_profile

logger = logging.getLogger('video_synthesis.pipeline')


class VideoSynthesisPipeline:
    """Complete pipeline from topic to video."""
    
    def __init__(
        self, 
        config_path: str = "config.yaml",
        style_profile_path: Optional[str] = None
    ):
        """
        Initialize the pipeline.
        
        Args:
            config_path: Path to configuration file
            style_profile_path: Optional path to style profile JSON
        """
        # Load configuration
        self.config = load_config(config_path)
        
        # Setup logging
        self.logger = setup_logging(self.config)
        
        # Load style profile if provided
        self.style_profile = None
        if style_profile_path:
            self.style_profile = load_style_profile(style_profile_path)
            logger.info(f"Loaded style profile from: {style_profile_path}")
        
        # Initialize components
        self.script_generator = ScriptGenerator(self.config, self.style_profile)
        self.blueprint_generator = BlueprintGenerator(self.config, self.style_profile)
        self.video_generator = VideoGenerator(self.config)
        
        logger.info("Pipeline initialized successfully")
    
    def generate(
        self, 
        topic: str, 
        output_path: Optional[str] = None
    ) -> Path:
        """
        Generate video from topic.
        
        Args:
            topic: The topic to create a video about
            output_path: Optional custom output path for video
            
        Returns:
            Path to generated video file
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Starting video synthesis pipeline")
        logger.info(f"Topic: {topic}")
        logger.info(f"{'='*60}\n")
        
        try:
            # Component 1: Topic → Script
            logger.info("COMPONENT 1: Topic -> Script")
            script = self.script_generator.generate_script(topic)
            logger.info(f"[OK] Script generated ({script['scene_count']} scenes, {script['total_duration']}s)")
            
            # Component 2: Script → Blueprint
            logger.info("\nCOMPONENT 2: Script -> Blueprint")
            blueprint = self.blueprint_generator.generate_blueprint(script)
            logger.info(f"[OK] Blueprint generated")
            
            # Component 3: Blueprint → MP4
            logger.info("\nCOMPONENT 3: Blueprint -> MP4 Video")
            video_path = self.video_generator.generate_video(script, blueprint, topic)
            logger.info(f"[OK] Video generated: {video_path}")
            
            # Optionally move to custom output path
            if output_path:
                final_path = Path(output_path)
                final_path.parent.mkdir(parents=True, exist_ok=True)
                video_path.rename(final_path)
                video_path = final_path
            
            logger.info(f"\n{'='*60}")
            logger.info(f"[SUCCESS] PIPELINE COMPLETE")
            logger.info(f"Video: {video_path}")
            logger.info(f"{'='*60}\n")
            
            return video_path
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            raise
    
    def get_summary(self) -> Dict:
        """Get pipeline summary information."""
        return {
            'config': self.config,
            'has_style_profile': self.style_profile is not None,
            'llm_provider': self.config['llm']['provider'],
            'tts_model': self.config['tts']['model'],
            'output_dir': self.config['output']['videos_dir']
        }

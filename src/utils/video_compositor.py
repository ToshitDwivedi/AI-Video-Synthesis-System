"""
Video Compositor - Combines rendered scenes and audio using FFMPEG
"""

import logging
import subprocess
from pathlib import Path
from typing import List, Dict
import ffmpeg

logger = logging.getLogger('video_synthesis.compositor')


class VideoCompositor:
    """Composites video scenes and audio into final MP4."""
    
    def __init__(self, config: dict):
        """
        Initialize video compositor.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.output_dir = Path(config['output']['videos_dir'])
        self.temp_dir = Path(config['output']['temp_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def composite_video(
        self, 
        video_files: List[Path], 
        audio_file: Path, 
        topic: str
    ) -> Path:
        """
        Composite video scenes and audio into final video.
        
        Args:
            video_files: List of video file paths (one per scene)
            audio_file: Path to narration audio file
            topic: Topic name for output filename
            
        Returns:
            Path to final composited video
        """
        logger.info(f"Compositing video for: {topic}")
        
        # Step 1: Concatenate video scenes if multiple
        if len(video_files) > 1:
            logger.info(f"Concatenating {len(video_files)} video scenes")
            concatenated_video = self._concatenate_videos(video_files, topic)
        else:
            concatenated_video = video_files[0]
        
        # Step 2: Add audio to video
        logger.info("Adding audio track")
        final_video = self._add_audio(concatenated_video, audio_file, topic)
        
        logger.info(f"Final video created: {final_video}")
        return final_video
    
    def _concatenate_videos(self, video_files: List[Path], topic: str) -> Path:
        """Concatenate multiple video files."""
        # Create concat file list
        concat_file = self.temp_dir / f"{self._sanitize(topic)}_concat.txt"
        
        with open(concat_file, 'w') as f:
            for video_file in video_files:
                f.write(f"file '{video_file.absolute()}'\n")
        
        # Output file
        output_file = self.temp_dir / f"{self._sanitize(topic)}_concatenated.mp4"
        
        # Use FFMPEG to concatenate
        try:
            (
                ffmpeg
                .input(str(concat_file), format='concat', safe=0)
                .output(str(output_file), c='copy')
                .overwrite_output()
                .run(quiet=True, capture_stdout=True, capture_stderr=True)
            )
            
            logger.info(f"Concatenated video: {output_file}")
            return output_file
            
        except ffmpeg.Error as e:
            logger.error(f"FFMPEG error during concatenation: {e.stderr.decode()}")
            # Fallback: return first video
            return video_files[0]
    
    def _add_audio(self, video_file: Path, audio_file: Path, topic: str) -> Path:
        """Add audio track to video."""
        output_file = self.output_dir / f"{self._sanitize(topic)}.mp4"
        
        try:
            # Get video input
            video = ffmpeg.input(str(video_file))
            
            # Get audio input
            audio = ffmpeg.input(str(audio_file))
            
            # Combine and output
            (
                ffmpeg
                .output(
                    video, 
                    audio, 
                    str(output_file),
                    vcodec='libx264',
                    acodec='aac',
                    strict='experimental',
                    shortest=None  # Use shortest stream duration
                )
                .overwrite_output()
                .run(quiet=True, capture_stdout=True, capture_stderr=True)
            )
            
            logger.info(f"Audio added to video: {output_file}")
            return output_file
            
        except ffmpeg.Error as e:
            logger.error(f"FFMPEG error adding audio: {e.stderr.decode()}")
            # Fallback: return video without audio
            return video_file
    
    def _sanitize(self, name: str) -> str:
        """Sanitize filename."""
        return name.lower().replace(' ', '_').replace('/', '_')

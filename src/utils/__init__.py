"""
Utility package for video synthesis system.
"""

from .config import load_config, setup_logging, load_style_profile
from .video_compositor import VideoCompositor

__all__ = ['load_config', 'setup_logging', 'load_style_profile', 'VideoCompositor']

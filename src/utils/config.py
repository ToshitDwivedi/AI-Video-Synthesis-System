"""
Utility functions for loading configuration and setting up logging.
"""

import os
import yaml
import logging
from pathlib import Path
from dotenv import load_dotenv

def load_config(config_path: str = "config.yaml") -> dict:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to the config file
        
    Returns:
        Configuration dictionary with environment variables substituted
    """
    # Load environment variables
    load_dotenv()
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Substitute environment variables
    config = _substitute_env_vars(config)
    
    # Create output directories
    _create_output_dirs(config)
    
    return config


def _substitute_env_vars(config: dict) -> dict:
    """Recursively substitute ${VAR} with environment variables."""
    if isinstance(config, dict):
        return {k: _substitute_env_vars(v) for k, v in config.items()}
    elif isinstance(config, list):
        return [_substitute_env_vars(item) for item in config]
    elif isinstance(config, str) and config.startswith("${") and config.endswith("}"):
        var_name = config[2:-1]
        return os.getenv(var_name, config)
    return config


def _create_output_dirs(config: dict):
    """Create output directories if they don't exist."""
    output_config = config.get('output', {})
    for key, path in output_config.items():
        if key.endswith('_dir'):
            Path(path).mkdir(parents=True, exist_ok=True)
    
    # Also create logs directory
    log_file = config.get('logging', {}).get('file', './logs/video_synthesis.log')
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)


def setup_logging(config: dict) -> logging.Logger:
    """
    Set up logging configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Configured logger instance
    """
    log_config = config.get('logging', {})
    log_level = getattr(logging, log_config.get('level', 'INFO'))
    log_file = log_config.get('file', './logs/video_synthesis.log')
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # Set up root logger
    logger = logging.getLogger('video_synthesis')
    logger.setLevel(log_level)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


def load_style_profile(profile_path: str) -> dict:
    """
    Load style profile from JSON file.
    
    Args:
        profile_path: Path to the style profile JSON
        
    Returns:
        Style profile dictionary
    """
    import json
    
    with open(profile_path, 'r') as f:
        return json.load(f)

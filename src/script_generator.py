"""
Script Generator - Component 1: Topic → Script
Generates narration scripts and scene concepts from topics.
"""

import json
import logging
from typing import Dict, List, Optional
from pathlib import Path

from .llm_client import LLMClient
from .prompts import (
    SCRIPT_GENERATION_SYSTEM_PROMPT,
    get_topic_analysis_prompt,
    get_script_generation_prompt
)

logger = logging.getLogger('video_synthesis.script_generator')


class ScriptGenerator:
    """Generates video scripts from topics using LLM."""
    
    def __init__(self, config: dict, style_profile: Optional[dict] = None):
        """
        Initialize script generator.
        
        Args:
            config: Configuration dictionary
            style_profile: Optional style profile from Part A analysis
        """
        self.config = config
        self.style_profile = style_profile or {}
        self.llm = LLMClient(config['llm'])
        self.output_dir = Path(config['output']['scripts_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_script(self, topic: str) -> Dict:
        """
        Generate complete video script for a topic.
        
        Args:
            topic: The topic to create a video about
            
        Returns:
            Dictionary containing:
                - topic: Original topic
                - outline: Topic analysis and outline
                - scenes: List of scene dictionaries with narration and visuals
                - total_duration: Total video duration in seconds
        """
        logger.info(f"Generating script for topic: {topic}")
        
        # Step 1: Analyze topic and create outline
        logger.info("Step 1: Analyzing topic structure")
        outline = self._analyze_topic(topic)
        
        # Step 2: Generate full script with scenes
        logger.info("Step 2: Generating narration script")
        scenes = self._generate_scenes(topic)
        
        # Step 3: Parse and structure the script
        logger.info("Step 3: Structuring script data")
        structured_script = self._structure_script(topic, outline, scenes)
        
        # Save the script
        self._save_script(topic, structured_script)
        
        logger.info(f"Script generated with {len(structured_script['scenes'])} scenes")
        return structured_script
    
    def _analyze_topic(self, topic: str) -> str:
        """Analyze topic and create outline."""
        prompt = get_topic_analysis_prompt(topic)
        outline = self.llm.generate(prompt, SCRIPT_GENERATION_SYSTEM_PROMPT)
        return outline
    
    def _generate_scenes(self, topic: str) -> str:
        """Generate scene-by-scene script."""
        prompt = get_script_generation_prompt(topic, self.style_profile)
        scenes_text = self.llm.generate(prompt, SCRIPT_GENERATION_SYSTEM_PROMPT)
        return scenes_text
    
    def _structure_script(self, topic: str, outline: str, scenes_text: str) -> Dict:
        """Parse and structure the generated script."""
        scenes = self._parse_scenes(scenes_text)
        
        # Calculate total duration with safe fallback
        total_duration = sum(scene.get('duration', 10) for scene in scenes)
        
        return {
            'topic': topic,
            'outline': outline,
            'scenes': scenes,
            'total_duration': total_duration,
            'scene_count': len(scenes)
        }
    
    def _parse_scenes(self, scenes_text: str) -> List[Dict]:
        """
        Parse scene text into structured format.
        
        Expected format:
        SCENE 1 [0:00-0:10]
        NARRATION: "..."
        VISUAL: [...]
        """
        scenes = []
        current_scene = {}
        
        lines = scenes_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            
            if not line:
                # Empty line might separate scenes
                if current_scene and 'narration' in current_scene:
                    scenes.append(current_scene)
                    current_scene = {}
                continue
            
            # Check for scene header
            if line.upper().startswith('SCENE'):
                # Save previous scene if exists
                if current_scene and 'narration' in current_scene:
                    scenes.append(current_scene)
                
                # Parse scene number and timing
                scene_num, timing = self._parse_scene_header(line)
                current_scene = {
                    'scene_id': scene_num,
                    'start_time': timing[0],
                    'end_time': timing[1],
                    'duration': timing[1] - timing[0]
                }
            
            elif line.upper().startswith('NARRATION:'):
                narration = line.split(':', 1)[1].strip().strip('"')
                current_scene['narration'] = narration
            
            elif line.upper().startswith('VISUAL:'):
                visual = line.split(':', 1)[1].strip()
                # Remove brackets if present
                visual = visual.strip('[]')
                current_scene['visual_description'] = visual
        
        # Don't forget the last scene
        if current_scene and 'narration' in current_scene:
            scenes.append(current_scene)
        
        # If parsing failed, create default structure
        if not scenes:
            logger.warning("Could not parse scenes, creating default structure")
            scenes = self._create_default_scenes(scenes_text)
        
        return scenes
    
    def _parse_scene_header(self, header: str) -> tuple:
        """Parse scene header to extract number and timing."""
        import re
        
        # Extract scene number
        scene_match = re.search(r'SCENE\s+(\d+)', header, re.IGNORECASE)
        scene_num = int(scene_match.group(1)) if scene_match else 1
        
        # Extract timing [0:00-0:10]
        timing_match = re.search(r'\[(\d+):(\d+)-(\d+):(\d+)\]', header)
        if timing_match:
            start_min, start_sec, end_min, end_sec = map(int, timing_match.groups())
            start_time = start_min * 60 + start_sec
            end_time = end_min * 60 + end_sec
        else:
            # Default to 10-second scenes
            start_time = (scene_num - 1) * 10
            end_time = scene_num * 10
        
        return scene_num, (start_time, end_time)
    
    def _create_default_scenes(self, text: str) -> List[Dict]:
        """Create default scene structure if parsing fails."""
        # Split text into roughly equal parts (aim for ~10 sec scenes)
        words = text.split()
        words_per_scene = len(words) // 6  # Aim for 6 scenes
        
        scenes = []
        for i in range(6):
            start_idx = i * words_per_scene
            end_idx = (i + 1) * words_per_scene if i < 5 else len(words)
            
            chunk = ' '.join(words[start_idx:end_idx])
            scenes.append({
                'scene_id': i + 1,
                'start_time': i * 10,
                'end_time': (i + 1) * 10,
                'duration': 10,
                'narration': chunk,
                'visual_description': 'Visual elements based on narration'
            })
        
        return scenes
    
    def _save_script(self, topic: str, script: Dict):
        """Save script to JSON file."""
        filename = topic.lower().replace(' ', '_').replace('/', '_')
        filepath = self.output_dir / f"{filename}_script.json"
        
        with open(filepath, 'w') as f:
            json.dump(script, f, indent=2)
        
        logger.info(f"Script saved to: {filepath}")

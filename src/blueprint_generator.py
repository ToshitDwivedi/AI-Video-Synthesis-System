"""
Blueprint Generator - Component 2: Script → Animation Blueprint
Converts scripts into detailed animation blueprints for video generation.
"""

import json
import logging
from typing import Dict, List
from pathlib import Path

from .llm_client import LLMClient

logger = logging.getLogger('video_synthesis.blueprint_generator')


class BlueprintGenerator:
    """Generates animation blueprints from scripts."""
    
    def __init__(self, config: dict, style_profile: dict = None):
        """
        Initialize blueprint generator.
        
        Args:
            config: Configuration dictionary
            style_profile: Style profile from Part A
        """
        self.config = config
        self.style_profile = style_profile or self._get_default_style()
        self.llm = LLMClient(config['llm'])
        self.output_dir = Path(config['output']['blueprints_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_blueprint(self, script: Dict) -> Dict:
        """
        Generate animation blueprint from script.
        
        Args:
            script: Script dictionary from ScriptGenerator
            
        Returns:
            Blueprint dictionary following blueprint_schema.json
        """
        logger.info(f"Generating blueprint for: {script['topic']}")
        
        blueprint = {
            'topic': script['topic'],
            'total_duration': script['total_duration'],
            'style_profile': self.style_profile,
            'scenes': []
        }
        
        # Process each scene
        for i, scene_data in enumerate(script['scenes'], 1):
            scene_id = scene_data.get('scene_id', i)
            logger.info(f"Processing scene {scene_id}")
            blueprint_scene = self._create_scene_blueprint(scene_data)
            blueprint['scenes'].append(blueprint_scene)
        
        # Save blueprint
        self._save_blueprint(script['topic'], blueprint)
        
        logger.info(f"Blueprint generated with {len(blueprint['scenes'])} scenes")
        return blueprint
    
    def _create_scene_blueprint(self, scene_data: Dict) -> Dict:
        """Create detailed blueprint for a single scene."""
        # Extract visual elements from description
        elements = self._extract_visual_elements(
            scene_data.get('visual_description', ''),
            scene_data.get('narration', '')
        )
        
        # Generate animations for elements
        duration = scene_data.get('duration', 10)
        animations = self._generate_animations(elements, duration)
        
        # Determine transition
        transition = self._get_transition()
        
        return {
            'scene_id': scene_data.get('scene_id', 1),
            'start_time': scene_data.get('start_time', 0),
            'duration': duration,
            'narration': scene_data.get('narration', ''),
            'visual_description': scene_data.get('visual_description', ''),
            'elements': elements,
            'animations': animations,
            'transitions': transition
        }
    
    def _extract_visual_elements(self, visual_desc: str, narration: str) -> List[Dict]:
        """
        Extract visual elements from descriptions.
        This is a simplified version - could use LLM for more sophistication.
        """
        elements = []
        element_counter = 0
        
        # Common technical video elements
        keywords = {
            'client': 'box',
            'server': 'box',
            'database': 'box',
            'arrow': 'arrow',
            'connection': 'arrow',
            'request': 'arrow',
            'response': 'arrow',
            'user': 'box',
            'api': 'box',
            'data': 'text'
        }
        
        text_lower = (visual_desc + ' ' + narration).lower()
        
        # Detect elements based on keywords
        detected = set()
        for keyword, elem_type in keywords.items():
            if keyword in text_lower and keyword not in detected:
                detected.add(keyword)
                
                element = {
                    'element_id': f'elem_{element_counter}',
                    'type': elem_type,
                    'label': keyword.capitalize(),
                    'position': self._get_element_position(element_counter),
                    'color': self._get_element_color(elem_type),
                }
                
                if elem_type == 'box':
                    element['size'] = {'width': 2, 'height': 1.5}
                
                elements.append(element)
                element_counter += 1
        
        # Always include title text
        elements.insert(0, {
            'element_id': 'title_text',
            'type': 'text',
            'label': narration[:50] + '...' if len(narration) > 50 else narration,
            'position': {'x': 0, 'y': 3},
            'color': self.style_profile.get('color_palette', {}).get('text', '#2C3E50')
        })
        
        return elements
    
    def _get_element_position(self, index: int) -> Dict:
        """Get position for element based on index."""
        positions = [
            {'x': -3, 'y': 0},   # Left
            {'x': 3, 'y': 0},    # Right
            {'x': 0, 'y': 1},    # Center-up
            {'x': 0, 'y': -1},   # Center-down
            {'x': -2, 'y': 1},   # Top-left
            {'x': 2, 'y': 1},    # Top-right
        ]
        return positions[index % len(positions)]
    
    def _get_element_color(self, elem_type: str) -> str:
        """Get color for element type based on style profile."""
        colors = self.style_profile.get('color_palette', {})
        
        color_map = {
            'box': colors.get('primary', '#2E86DE'),
            'arrow': colors.get('accent', '#FF6B6B'),
            'text': colors.get('text', '#2C3E50'),
            'circle': colors.get('secondary', '#5F27CD')
        }
        
        return color_map.get(elem_type, colors.get('primary', '#2E86DE'))
    
    def _generate_animations(self, elements: List[Dict], duration: float) -> List[Dict]:
        """Generate animations for elements."""
        animations = []
        
        # Stagger element appearances
        delay_per_element = min(0.3, duration / (len(elements) + 1))
        
        for i, element in enumerate(elements):
            # Fade in animation
            animations.append({
                'element_id': element['element_id'],
                'animation_type': 'fade_in',
                'timing': {
                    'start': i * delay_per_element,
                    'duration': 0.5
                },
                'parameters': {}
            })
            
            # Arrows get growth animation
            if element['type'] == 'arrow':
                animations.append({
                    'element_id': element['element_id'],
                    'animation_type': 'grow',
                    'timing': {
                        'start': i * delay_per_element + 0.2,
                        'duration': 0.6
                    },
                    'parameters': {'direction': 'horizontal'}
                })
        
        return animations
    
    def _get_transition(self) -> Dict:
        """Get transition to next scene."""
        transition_type = self.style_profile.get('animation', {}).get('transition_speed', 'smooth')
        
        transition_map = {
            'smooth': {'type': 'fade', 'duration': 0.5},
            'snappy': {'type': 'cut', 'duration': 0.1},
            'professional': {'type': 'fade', 'duration': 0.3}
        }
        
        return transition_map.get(transition_type, {'type': 'fade', 'duration': 0.5})
    
    def _get_default_style(self) -> Dict:
        """Get default style profile if none provided."""
        return {
            'visualization_style': {
                'primary': 'flowchart_animation',
                'secondary': ['2d_explainer']
            },
            'color_palette': {
                'primary': '#2E86DE',
                'secondary': '#5F27CD',
                'background': '#FFFFFF',
                'text': '#2C3E50',
                'accent': '#FF6B6B'
            },
            'animation': {
                'transition_speed': 'smooth'
            }
        }
    
    def _save_blueprint(self, topic: str, blueprint: Dict):
        """Save blueprint to JSON file."""
        filename = topic.lower().replace(' ', '_').replace('/', '_')
        filepath = self.output_dir / f"{filename}_blueprint.json"
        
        with open(filepath, 'w') as f:
            json.dump(blueprint, f, indent=2)
        
        logger.info(f"Blueprint saved to: {filepath}")

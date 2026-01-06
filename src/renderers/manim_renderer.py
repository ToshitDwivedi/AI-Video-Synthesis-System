"""
Manim Renderer - Generates animations using Manim Community Edition
"""

import logging
from pathlib import Path
from typing import Dict, List

# Make Manim optional for testing
try:
    from manim import *
    MANIM_AVAILABLE = True
except ImportError:
    MANIM_AVAILABLE = False
    print("Warning: Manim not installed. Video rendering will be disabled.")
    # Create dummy base class
    class Scene:
        pass
    import numpy as np

logger = logging.getLogger('video_synthesis.manim_renderer')


class TechnicalScene(Scene):
    """Base scene for technical animations."""
    
    def __init__(self, scene_data: Dict, style_profile: Dict, **kwargs):
        super().__init__(**kwargs)
        self.scene_data = scene_data
        self.style_profile = style_profile
        self.elements_map = {}
    
    def construct(self):
        """Construct the scene based on blueprint data."""
        # Set background color
        bg_color = self.style_profile.get('color_palette', {}).get('background', '#FFFFFF')
        self.camera.background_color = bg_color
        
        # Create all visual elements
        self._create_elements()
        
        # Apply animations
        self._apply_animations()
    
    def _create_elements(self):
        """Create all visual elements for the scene."""
        elements_data = self.scene_data.get('elements', [])
        
        for elem_data in elements_data:
            element = self._create_element(elem_data)
            if element:
                self.elements_map[elem_data['element_id']] = element
    
    def _create_element(self, elem_data: Dict):
        """Create a single visual element."""
        elem_type = elem_data['type']
        label = elem_data.get('label', '')
        position = elem_data.get('position', {'x': 0, 'y': 0})
        color_hex = elem_data.get('color', '#2E86DE')
        
        # Parse position
        pos = np.array([position['x'], position['y'], 0])
        
        # Create based on type
        if elem_type == 'box':
            size = elem_data.get('size', {'width': 2, 'height': 1.5})
            rect = Rectangle(
                width=size['width'],
                height=size['height'],
                color=color_hex,
                fill_opacity=0.3
            )
            rect.move_to(pos)
            
            # Add label
            if label:
                text = Text(label, font_size=24, color=color_hex)
                text.move_to(rect.get_center())
                group = VGroup(rect, text)
                return group
            
            return rect
        
        elif elem_type == 'circle':
            circle = Circle(radius=0.5, color=color_hex, fill_opacity=0.3)
            circle.move_to(pos)
            
            if label:
                text = Text(label, font_size=20, color=color_hex)
                text.move_to(circle.get_center())
                return VGroup(circle, text)
            
            return circle
        
        elif elem_type == 'arrow':
            # Arrow connecting positions (simplified)
            arrow = Arrow(
                start=LEFT * 1.5 + pos,
                end=RIGHT * 1.5 + pos,
                color=color_hex,
                stroke_width=4
            )
            
            if label:
                text = Text(label, font_size=16, color=color_hex)
                text.next_to(arrow, UP, buff=0.1)
                return VGroup(arrow, text)
            
            return arrow
        
        elif elem_type == 'text':
            text = Text(label, font_size=28, color=color_hex)
            text.move_to(pos)
            return text
        
        elif elem_type == 'line':
            line = Line(
                start=LEFT * 2 + pos,
                end=RIGHT * 2 + pos,
                color=color_hex
            )
            return line
        
        return None
    
    def _apply_animations(self):
        """Apply all animations to elements."""
        animations_data = self.scene_data.get('animations', [])
        
        # Group animations by timing
        timed_animations = {}
        
        for anim_data in animations_data:
            timing = anim_data['timing']
            start_time = timing['start']
            
            if start_time not in timed_animations:
                timed_animations[start_time] = []
            
            timed_animations[start_time].append(anim_data)
        
        # Play animations in sequence
        for start_time in sorted(timed_animations.keys()):
            animations = timed_animations[start_time]
            manim_anims = []
            
            for anim_data in animations:
                anim = self._create_animation(anim_data)
                if anim:
                    manim_anims.append(anim)
            
            # Play all animations at this timestamp
            if manim_anims:
                self.play(*manim_anims)
            
            # Small wait between animation groups
            if start_time != max(timed_animations.keys()):
                self.wait(0.2)
        
        # Final wait
        self.wait(1)
    
    def _create_animation(self, anim_data: Dict):
        """Create a Manim animation from blueprint data."""
        elem_id = anim_data['element_id']
        anim_type = anim_data['animation_type']
        duration = anim_data['timing']['duration']
        
        # Get the element
        element = self.elements_map.get(elem_id)
        if not element:
            return None
        
        # Create animation based on type
        if anim_type == 'fade_in':
            return FadeIn(element, run_time=duration)
        
        elif anim_type == 'fade_out':
            return FadeOut(element, run_time=duration)
        
        elif anim_type == 'slide_in':
            direction = anim_data.get('parameters', {}).get('direction', 'left')
            dir_map = {'left': LEFT, 'right': RIGHT, 'up': UP, 'down': DOWN}
            return element.animate(run_time=duration).shift(dir_map.get(direction, LEFT) * 3)
        
        elif anim_type == 'grow':
            return GrowFromCenter(element, run_time=duration)
        
        elif anim_type == 'shrink':
            return ShrinkToCenter(element, run_time=duration)
        
        elif anim_type == 'move':
            target = anim_data.get('parameters', {}).get('target', {'x': 0, 'y': 0})
            target_pos = np.array([target['x'], target['y'], 0])
            return element.animate(run_time=duration).move_to(target_pos)
        
        elif anim_type == 'rotate':
            angle = anim_data.get('parameters', {}).get('angle', 90)
            return Rotate(element, angle=angle * DEGREES, run_time=duration)
        
        return None


class ManimRenderer:
    """Renders blueprints to videos using Manim."""
    
    def __init__(self, config: dict):
        """
        Initialize Manim renderer.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.manim_config = config['manim']
        self.output_dir = Path(config['output']['temp_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def render_blueprint(self, blueprint: Dict) -> Path:
        """
        Render blueprint to video file.
        
        Args:
            blueprint: Animation blueprint
            
        Returns:
            Path to rendered video file
        """
        logger.info(f"Rendering blueprint for: {blueprint['topic']}")
        
        # Configure Manim
        quality = self.manim_config['quality']
        fps = self.manim_config['fps']
        
        # Set quality flags
        quality_flag = f"-q{quality[0]}"  # -ql, -qm, -qh, -qp
        
        # Create scene files and render
        video_files = []
        
        for scene_data in blueprint['scenes']:
            logger.info(f"Rendering scene {scene_data['scene_id']}")
            video_file = self._render_scene(scene_data, blueprint['style_profile'], quality_flag)
            video_files.append(video_file)
        
        # For now, return the first scene video
        # The compositor will combine all scenes
        return video_files[0] if video_files else None
    
    def _render_scene(self, scene_data: Dict, style_profile: Dict, quality: str) -> Path:
        """Render a single scene."""
        # Manim rendering happens through CLI in practice
        # This is a simplified version for demonstration
        
        # In a real implementation, you'd dynamically create scene classes
        # and use Manim's rendering pipeline
        
        scene = TechnicalScene(scene_data, style_profile)
        
        # Output would be rendered to media/videos/...
        # Return path to the rendered video
        
        output_path = self.output_dir / f"scene_{scene_data['scene_id']}.mp4"
        
        logger.info(f"Scene rendered to: {output_path}")
        return output_path

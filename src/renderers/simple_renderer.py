"""
Simple Video Renderer - Creates MP4 videos from blueprints
Uses PIL for image generation and moviepy for video creation
"""

import logging
from pathlib import Path
from typing import Dict, List
from PIL import Image, ImageDraw, ImageFont
import json

logger = logging.getLogger('video_synthesis.simple_renderer')


class SimpleVideoRenderer:
    """Generate videos using PIL + moviepy with enhanced animations."""
    
    def __init__(self, config: dict):
        self.config = config
        self.output_dir = Path(config['output']['temp_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.width = 1280
        self.height = 720
        self.fps = 30  # Frames per second for animations
        
        # Visualization styles supported
        self.viz_styles = [
            '2d_explainer',
            'line_based_animation',
            'flowchart_arrows',
            'whiteboard_doodle',
            'kinetic_typography',
            'infographic_motion'
        ]
        
    def render_blueprint(self, blueprint: Dict, audio_files: Dict) -> List[Path]:
        """
        Render blueprint as video scenes.
        
        Args:
            blueprint: Animation blueprint
            audio_files: Dict of audio file paths by scene_id
            
        Returns:
            List of video file paths
        """
        logger.info(f"Rendering {len(blueprint['scenes'])} scenes")
        
        video_files = []
        
        for scene_data in blueprint['scenes']:
            scene_id = scene_data.get('scene_id', 1)
            logger.info(f"Rendering scene {scene_id}")
            
            # Get scene duration from audio or default
            duration = scene_data.get('duration', 10)
            
            # Create scene video
            video_path = self._render_scene(scene_data, duration, blueprint.get('style_profile', {}))
            if video_path:
                video_files.append(video_path)
        
        logger.info(f"Rendered {len(video_files)} video files")
        return video_files
    
    def _render_scene(self, scene_data: Dict, duration: float, style: Dict) -> Path:
        """Render a single scene with animations and transitions."""
        try:
            scene_id = scene_data.get('scene_id', 1)
            narration = scene_data.get('narration', '')
            viz_style = scene_data.get('visualization_style', '2d_explainer')
            transition = scene_data.get('transition', {'type': 'fade', 'duration': 0.5})
            
            # Create base image with gradient background
            img = Image.new('RGB', (self.width, self.height), color='#0f0f1e')
            draw = ImageDraw.Draw(img)
            
            # Add gradient overlay
            for y in range(self.height):
                alpha = int(30 * (y / self.height))
                color = (15 + alpha, 15 + alpha, 30 + alpha)
                draw.rectangle([(0, y), (self.width, y+1)], fill=color)
            
            # Load fonts
            try:
                font_title = ImageFont.truetype("arial.ttf", 48)
                font_large = ImageFont.truetype("arial.ttf", 40)
                font_medium = ImageFont.truetype("arial.ttf", 34)
                font_small = ImageFont.truetype("arial.ttf", 26)
            except:
                font_title = ImageFont.load_default()
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Create meaningful title from narration (first 8 words)
            if narration:
                title_words = narration.split()[:8]
                scene_title = ' '.join(title_words)
                if len(narration.split()) > 8:
                    scene_title += "..."
            else:
                scene_title = f"Scene {scene_id}"
            
            # Draw title bar at top
            title_bar_height = 100
            draw.rectangle([0, 0, self.width, title_bar_height], 
                         fill='#1a2332', outline='#00d4ff', width=3)
            
            # Draw centered title text
            bbox = draw.textbbox((0, 0), scene_title, font=font_title)
            text_width = bbox[2] - bbox[0]
            draw.text(((self.width - text_width) // 2, 25), 
                     scene_title, fill='#00d4ff', font=font_title)
            
            # Get visual elements
            elements = scene_data.get('elements', [])
            has_visual_elements = any(e.get('type') in ['box', 'arrow', 'circle'] for e in elements)
            
            # CENTERED NARRATION TEXT (when no visual elements, or always show)
            if narration:
                words = narration.split()
                lines = []
                current_line = []
                max_width = self.width - 160
                
                for word in words:
                    test_line = ' '.join(current_line + [word])
                    bbox = draw.textbbox((0, 0), test_line, font=font_medium)
                    if bbox[2] - bbox[0] <= max_width:
                        current_line.append(word)
                    else:
                        if current_line:
                            lines.append(' '.join(current_line))
                        current_line = [word]
                if current_line:
                    lines.append(' '.join(current_line))
                
                # Position narration - centered vertically if no visuals
                if has_visual_elements:
                    text_y = 150
                else:
                    # Center vertically
                    line_height = 55
                    total_text_height = len(lines[:5]) * line_height
                    text_y = (self.height - total_text_height) // 2
                
                # Draw narration lines (centered horizontally)
                for i, line in enumerate(lines[:5]):
                    bbox = draw.textbbox((0, 0), line, font=font_medium)
                    line_width = bbox[2] - bbox[0]
                    x_pos = (self.width - line_width) // 2
                    draw.text((x_pos, text_y + i * 55), line, 
                             fill='#ffffff', font=font_medium)
            
            # RENDER VISUAL ELEMENTS (boxes, arrows)
            if has_visual_elements:
                logger.info(f"Scene {scene_id}: Rendering {len(elements)} elements")
                
                for idx, elem in enumerate(elements):
                    elem_type = elem.get('type', 'text')
                    label = elem.get('label', '')
                    pos = elem.get('position', {})
                    
                    if elem_type == 'box':
                        # Box rendering
                        x = int(pos.get('x', 0) * 120 + 640)
                        y = int(pos.get('y', 0) * 100 + 450)
                        width = elem.get('size', {}).get('width', 2) * 110
                        height = elem.get('size', {}).get('height', 1.5) * 70
                        
                        # Shadow
                        draw.rectangle([x - width//2 + 6, y - height//2 + 6, 
                                      x + width//2 + 6, y + height//2 + 6],
                                     fill='#000000')
                        
                        # Box
                        draw.rectangle([x - width//2, y - height//2, x + width//2, y + height//2],
                                     fill='#1e3a5f', outline='#00d4ff', width=5)
                        
                        # Label
                        if label:
                            bbox = draw.textbbox((0, 0), label, font=font_large)
                            lbl_width = bbox[2] - bbox[0]
                            lbl_height = bbox[3] - bbox[1]
                            draw.text((x - lbl_width//2, y - lbl_height//2), 
                                    label, fill='#00ffff', font=font_large)
                        
                        logger.info(f"  Rendered box '{label}' at ({x}, {y})")
                    
                    elif elem_type == 'arrow':
                        # Arrow rendering - HORIZONTAL RED ARROW
                        x = int(pos.get('x', 0) * 120 + 640)
                        y = int(pos.get('y', 0) * 100 + 450)
                        
                        # Draw horizontal arrow (200px long)
                        arrow_length = 200
                        start_x = x - arrow_length // 2
                        end_x = x + arrow_length // 2
                        
                        # Arrow line (THICK RED)
                        draw.line([start_x, y, end_x, y], 
                                fill='#FF3333', width=8)
                        
                        # Arrowhead (triangle at end)
                        arrow_size = 30
                        arrow_pts = [
                            (end_x, y),
                            (end_x - arrow_size, y - 15),
                            (end_x - arrow_size, y + 15)
                        ]
                        draw.polygon(arrow_pts, fill='#FF3333')
                        
                        # Label above arrow
                        if label:
                            bbox = draw.textbbox((0, 0), label, font=font_small)
                            lbl_width = bbox[2] - bbox[0]
                            draw.text((x - lbl_width//2, y - 45), 
                                    label, fill='#FFaa33', font=font_small)
                        
                        logger.info(f"  Rendered ARROW '{label}' at ({x}, {y})")
            
            # NO VISUAL DESCRIPTION AT BOTTOM (removed completely)
            
            # Save frame
            frame_path = self.output_dir / f"scene_{scene_id}_frame.png"
            img.save(frame_path)
            
            logger.info(f"Scene {scene_id} rendered: {frame_path}")
            return frame_path
            
        except Exception as e:
            logger.error(f"Failed to render scene {scene_data.get('scene_id')}: {e}", exc_info=True)
            return None
    
    def _render_animated_scene(self, scene_data: Dict, duration: float, style: Dict) -> List[Path]:
        """Render multiple frames for animated scene with transitions."""
        scene_id = scene_data.get('scene_id', 1)
        frames = []
        num_frames = int(duration * self.fps)
        transition_type = scene_data.get('transition', {}).get('type', 'fade')
        
        for frame_idx in range(num_frames):
            progress = frame_idx / num_frames
            frame_path = self._render_frame(scene_data, frame_idx, progress, style, transition_type)
            if frame_path:
                frames.append(frame_path)
        
        return frames
    
    def _render_frame(self, scene_data: Dict, frame_idx: int, progress: float, style: Dict, transition: str) -> Path:
        """Render individual frame with animation effects."""
        try:
            scene_id = scene_data.get('scene_id', 1)
            narration = scene_data.get('narration', '')
            
            # Create base image
            img = Image.new('RGB', (self.width, self.height), color='#0f0f1e')
            draw = ImageDraw.Draw(img)
            
            # Apply transition effect
            if transition == 'fade' and progress < 0.2:
                # Fade in at start
                alpha = int(255 * (progress / 0.2))
                overlay = Image.new('RGBA', (self.width, self.height), (15, 15, 30, 255 - alpha))
                img.paste(overlay, (0, 0), overlay)
            elif transition == 'slide' and progress < 0.3:
                # Slide in from left
                offset = int(self.width * (1 - progress / 0.3))
                img = img.transform(img.size, Image.AFFINE, (1, 0, -offset, 0, 1, 0))
            
            # Load fonts
            try:
                font_title = ImageFont.truetype("arial.ttf", 48)
                font_medium = ImageFont.truetype("arial.ttf", 34)
            except:
                font_title = ImageFont.load_default()
                font_medium = ImageFont.load_default()
            
            # Add gradient background
            for y in range(self.height):
                alpha = int(30 * (y / self.height))
                color = (15 + alpha, 15 + alpha, 30 + alpha)
                draw.rectangle([(0, y), (self.width, y+1)], fill=color)
            
            # Draw title with kinetic typography effect
            if progress < 0.5:
                title_scale = progress / 0.5
            else:
                title_scale = 1.0
            
            scene_title = narration.split()[:6] if narration else f"Scene {scene_id}"
            scene_title = ' '.join(scene_title) if isinstance(scene_title, list) else scene_title
            
            draw.rectangle([0, 0, self.width, 100], fill='#1a2332', outline='#00d4ff', width=3)
            bbox = draw.textbbox((0, 0), scene_title[:50], font=font_title)
            text_width = bbox[2] - bbox[0]
            draw.text(((self.width - text_width) // 2, 25), 
                     scene_title[:50], fill='#00d4ff', font=font_title)
            
            # Render elements with animation
            elements = scene_data.get('elements', [])
            for elem in elements:
                elem_progress = min(1.0, progress * 1.5)  # Stagger element animations
                self._render_animated_element(draw, elem, elem_progress, font_medium)
            
            # Add text overlay for narration
            if narration:
                self._draw_text_overlay(draw, narration, font_medium, progress)
            
            # Save frame
            frame_path = self.output_dir / f"scene_{scene_id}_frame_{frame_idx:04d}.png"
            img.save(frame_path)
            
            return frame_path
            
        except Exception as e:
            logger.error(f"Failed to render frame {frame_idx}: {e}")
            return None
    
    def _render_animated_element(self, draw, elem: Dict, progress: float, font):
        """Render animated visual element."""
        elem_type = elem.get('type', 'box')
        label = elem.get('label', '')
        pos = elem.get('position', {})
        
        x = int(pos.get('x', 0) * 120 + 640)
        y = int(pos.get('y', 0) * 100 + 450)
        
        # Apply grow animation
        scale = progress
        
        if elem_type == 'box':
            width = elem.get('size', {}).get('width', 2) * 110 * scale
            height = elem.get('size', {}).get('height', 1.5) * 70 * scale
            
            # Draw box with shadow
            draw.rectangle([x - width//2 + 4, y - height//2 + 4, 
                          x + width//2 + 4, y + height//2 + 4],
                         fill='#000000')
            draw.rectangle([x - width//2, y - height//2, x + width//2, y + height//2],
                         fill='#1e3a5f', outline='#00d4ff', width=5)
            
            if label and progress > 0.5:
                bbox = draw.textbbox((0, 0), label, font=font)
                lbl_width = bbox[2] - bbox[0]
                draw.text((x - lbl_width//2, y - 15), label, fill='#00ffff', font=font)
        
        elif elem_type == 'arrow':
            arrow_length = 200 * progress
            start_x = x - arrow_length // 2
            end_x = x + arrow_length // 2
            
            draw.line([start_x, y, end_x, y], fill='#FF3333', width=8)
            
            # Arrowhead
            if progress > 0.7:
                arrow_pts = [(end_x, y), (end_x - 30, y - 15), (end_x - 30, y + 15)]
                draw.polygon(arrow_pts, fill='#FF3333')
            
            if label and progress > 0.8:
                bbox = draw.textbbox((0, 0), label, font=font)
                lbl_width = bbox[2] - bbox[0]
                draw.text((x - lbl_width//2, y - 45), label, fill='#FFaa33', font=font)
        
        elif elem_type == 'circle':
            radius = 50 * scale
            draw.ellipse([x - radius, y - radius, x + radius, y + radius],
                        fill='#1e3a5f', outline='#00ffaa', width=4)
            
            if label and progress > 0.6:
                bbox = draw.textbbox((0, 0), label, font=font)
                lbl_width = bbox[2] - bbox[0]
                draw.text((x - lbl_width//2, y - 10), label, fill='#00ffaa', font=font)
    
    def _draw_text_overlay(self, draw, narration: str, font, progress: float):
        """Draw animated text overlay for narration."""
        # Split narration into lines
        words = narration.split()
        visible_words = int(len(words) * progress)
        text_to_show = ' '.join(words[:visible_words])
        
        # Wrap text
        lines = []
        current_line = []
        max_width = self.width - 160
        
        for word in text_to_show.split():
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw lines
        text_y = 150
        for i, line in enumerate(lines[:4]):
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
            x_pos = (self.width - line_width) // 2
            
            # Add semi-transparent background for readability
            padding = 10
            draw.rectangle([x_pos - padding, text_y + i * 50 - padding,
                          x_pos + line_width + padding, text_y + i * 50 + 35 + padding],
                         fill=(0, 0, 0, 128))
            
            draw.text((x_pos, text_y + i * 50), line, fill='#ffffff', font=font)
    
    def create_video_from_frames(self, frame_paths: List[Path], audio_paths: List[Path], output_path: Path) -> Path:
        """Combine frames and audio into final video with transitions."""
        try:
            from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip
            from moviepy.video.fx import fadeout, fadein
            
            clips = []
            
            for i, frame_path in enumerate(frame_paths):
                # Get audio duration if available
                if i < len(audio_paths) and audio_paths[i] and audio_paths[i].exists():
                    try:
                        audio = AudioFileClip(str(audio_paths[i]))
                        duration = audio.duration
                        audio.close()
                    except:
                        duration = 5
                else:
                    duration = 5
                
                # Create video clip from image
                clip = ImageClip(str(frame_path), duration=duration)
                
                # Add fade transitions
                if i > 0:  # Fade in for all clips except first
                    clip = fadein(clip, 0.5)
                if i < len(frame_paths) - 1:  # Fade out for all clips except last
                    clip = fadeout(clip, 0.5)
                
                # Add audio if available
                if i < len(audio_paths) and audio_paths[i] and audio_paths[i].exists():
                    try:
                        audio_clip = AudioFileClip(str(audio_paths[i]))
                        clip = clip.set_audio(audio_clip)
                    except Exception as e:
                        logger.warning(f"Could not add audio to scene {i+1}: {e}")
                
                clips.append(clip)
            
            # Concatenate all clips
            final_clip = concatenate_videoclips(clips, method="compose")
            
            # Write to file
            final_clip.write_videofile(
                str(output_path),
                fps=24,
                codec='libx264',
                audio_codec='aac',
                logger=None  # Suppress moviepy logs
            )
            
            # Clean up
            final_clip.close()
            for clip in clips:
                clip.close()
            
            logger.info(f"Final video created: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to create video: {e}")
            return None

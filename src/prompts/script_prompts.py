"""
Prompt templates for script generation.
"""

SCRIPT_GENERATION_SYSTEM_PROMPT = """You are an expert technical content creator who creates engaging educational video scripts. 
You specialize in explaining complex technical concepts in a clear, structured way suitable for video animation.

Your scripts should:
- Break down concepts into digestible segments
- Use analogies and examples
- Follow a logical progression
- Include visual cues for animation
- Be engaging but professional
"""


def get_topic_analysis_prompt(topic: str) -> str:
    """Generate prompt for analyzing and structuring the topic."""
    return f"""Analyze the topic "{topic}" and create a structured outline for a technical explainer video.

Provide:
1. A brief introduction (what problem/concept this addresses)
2. 3-5 main concepts to cover
3. Logical flow/sequence of explanation
4. A conclusion/summary

Keep it concise and suitable for a 60-90 second video.

Format your response as:
## Introduction
[Your introduction]

## Main Concepts
1. [Concept 1]
2. [Concept 2]
...

## Flow
[Explanation sequence]

## Conclusion
[Summary]
"""


def get_script_generation_prompt(topic: str, style_profile: dict) -> str:
    """Generate prompt for creating the full narration script."""
    
    style_desc = _format_style_profile(style_profile)
    
    return f"""Create a detailed narration script for a technical explainer video about "{topic}".

Style Profile:
{style_desc}

Requirements:
1. Write a complete voice-over script (narration)
2. Break it into 5-7 distinct scenes
3. Each scene should be 8-12 seconds long
4. Include timing markers [0:00-0:10] for each scene
5. Add visual cues in [brackets] describing what should be shown
6. Use clear, engaging language

Format your response as:

SCENE 1 [0:00-0:10]
NARRATION: "Your narration text here..."
VISUAL: [Description of what's shown: e.g., "Two boxes labeled Client and Server appear"]

SCENE 2 [0:10-0:22]
NARRATION: "..."
VISUAL: [...]

... continue for all scenes ...

Make sure the total duration is around 60 seconds.
"""


def get_scene_concept_prompt(scene_narration: str, style_profile: dict) -> str:
    """Generate prompt for detailed scene visualization."""
    
    return f"""Given this narration for a video scene:
"{scene_narration}"

And this visual style profile:
{_format_style_profile(style_profile)}

Create a detailed visual storyboard for this scene including:
1. Main visual elements (shapes, arrows, text, etc.)
2. Animation sequence (what appears when)
3. Color usage
4. Text overlays
5. Transitions

Be specific and technical so an animation engine can execute it.
"""


def _format_style_profile(style_profile: dict) -> str:
    """Format style profile for inclusion in prompts."""
    if not style_profile:
        return "Standard technical explainer style with clean graphics and smooth animations."
    
    viz_style = style_profile.get('visualization_style', {})
    colors = style_profile.get('color_palette', {})
    anim = style_profile.get('animation', {})
    elements = style_profile.get('visual_elements', {})
    
    parts = []
    
    if viz_style:
        parts.append(f"Visual Style: {viz_style.get('primary', 'technical')}")
    
    if colors:
        parts.append(f"Colors: Primary={colors.get('primary', '#2E86DE')}, Background={colors.get('background', '#FFFFFF')}")
    
    if elements:
        enabled = [k for k, v in elements.items() if v]
        parts.append(f"Elements: {', '.join(enabled)}")
    
    if anim:
        parts.append(f"Animation: {anim.get('transition_speed', 'smooth')} transitions")
    
    return " | ".join(parts) if parts else "Default technical style"

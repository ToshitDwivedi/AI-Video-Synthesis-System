"""
Test moviepy video creation directly
"""

from pathlib import Path
try:
    from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
except ImportError:
    # Try alternative import for moviepy 2.x
    from moviepy import ImageClip, concatenate_videoclips, AudioFileClip

print("Testing moviepy video creation...")

# Paths
temp_dir = Path("output/temp")
audio_dir = Path("output/audio")
output_path = Path("output/videos/dns_test.mp4")
output_path.parent.mkdir(parents=True, exist_ok=True)

# Get frames
frames = sorted(list(temp_dir.glob("scene_*_frame.png")))
print(f"Found {len(frames)} frames")

# Get audio
audios = sorted(list(audio_dir.glob("what_is_dns_scene_*.mp3")))[:7]  # Match frame count
print(f"Found {len(audios)} audio files")

try:
    clips = []
    
    for i, frame_path in enumerate(frames):
        print(f"\nProcessing scene {i+1}...")
        
        # Get duration from audio
        if i < len(audios):
            try:
                audio = AudioFileClip(str(audios[i]))
                duration = audio.duration
                print(f"  Audio duration: {duration}s")
                audio.close()
            except Exception as e:
                print(f"  Audio error: {e}, using 5s default")
                duration = 5
        else:
            duration = 5
        
        # Create clip
        clip = ImageClip(str(frame_path), duration=duration)
        
        # Add audio by directly assigning to audio property
        if i < len(audios):
            try:
                audio_clip = AudioFileClip(str(audios[i]))
                clip.audio = audio_clip  # Direct property assignment
                print(f"  Audio added successfully")
            except Exception as e:
                print(f"  Could not add audio: {e}")
        
        clips.append(clip)
    
    print("\nConcatenating clips...")
    final_clip = concatenate_videoclips(clips, method="compose")
    
    print(f"\nWriting video to: {output_path}")
    final_clip.write_videofile(
        str(output_path),
        fps=24,
        codec='libx264',
        audio_codec='aac',
        audio=True  # Ensure audio is included
    )
    
    # Clean up
    final_clip.close()
    for clip in clips:
        clip.close()
    
    print(f"\n✅ SUCCESS! Video created: {output_path}")
    print(f"Size: {output_path.stat().st_size / 1024:.1f} KB")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

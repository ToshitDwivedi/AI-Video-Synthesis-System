"""
Main entry point - CLI interface for video synthesis system
"""

import sys
import logging
import argparse
from pathlib import Path

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from src.utils.config import load_config
from src.pipeline import VideoSynthesisPipeline


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Visual Learning Pattern Analysis + AI Video Synthesis System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate video with default settings
  python main.py --topic "How DNS works"
  
  # Use custom style profile from Part A analysis
  python main.py --topic "How WebSockets work" --style style_profile.json
  
  # Specify output location
  python main.py --topic "What is HTTP" --output ./my_videos/http_explained.mp4
  
  # Use Ollama instead of Groq
  python main.py --topic "REST APIs" --llm ollama
        """
    )
    
    parser.add_argument(
        '--topic',
        type=str,
        required=True,
        help='Topic to create video about'
    )
    
    parser.add_argument(
        '--style',
        type=str,
        default=None,
        help='Path to style profile JSON file from Part A analysis'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Custom output path for the video file'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    
    parser.add_argument(
        '--duration',
        type=int,
        default=None,
        help='Target video duration in seconds (approximate)'
    )
    
    parser.add_argument(
        '--llm',
        type=str,
        choices=['groq', 'ollama'],
        default=None,
        help='Override LLM provider (groq or ollama)'
    )
    
    args = parser.parse_args()
    
    # Validate config exists
    if not Path(args.config).exists():
        print(f"[ERROR] Error: Config file not found: {args.config}")
        print("Run: cp config.yaml.example config.yaml")
        sys.exit(1)
    
    # Validate style profile if provided
    if args.style and not Path(args.style).exists():
        print(f"[ERROR] Error: Style profile not found: {args.style}")
        sys.exit(1)
    
    # Initialize pipeline
    print("\n[INIT] Initializing Video Synthesis Pipeline...")
    print(f"[TOPIC] Topic: {args.topic}")
    
    if args.style:
        print(f"[STYLE] Style Profile: {args.style}")
    
    try:
        pipeline = VideoSynthesisPipeline(
            config_path=args.config,
            style_profile_path=args.style
        )
        
        # Override LLM if specified
        if args.llm:
            pipeline.config['llm']['provider'] = args.llm
            print(f"[AI] LLM Provider: {args.llm}")
        
        # Print summary
        summary = pipeline.get_summary()
        print(f"[AI] LLM: {summary['llm_provider']}")
        print(f"[TTS] TTS: {summary['tts_model'].split('/')[-1]}")
        print(f"[OUTPUT] Output: {summary['output_dir']}")
        print()
        
        # Generate video
        video_path = pipeline.generate(
            topic=args.topic,
            output_path=args.output
        )
        
        print(f"\n[SUCCESS] SUCCESS!")
        print(f"[VIDEO] Video generated: {video_path}")
        print()
        
        # Provide next steps
        print("Next steps:")
        print(f"  1. Watch the video: {video_path}")
        print(f"  2. Compare with reference video style")
        print(f"  3. Iterate on style profile if needed")
        print()
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n[WARNING]  Process interrupted by user")
        return 1
        
    except Exception as e:
        print(f"\n[ERROR] ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())


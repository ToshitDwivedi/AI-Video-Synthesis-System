"""
Quick test script - Tests script generation without full pipeline
This bypasses TTS and Manim for quick testing of LLM components
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_config():
    """Test config loading."""
    print("="*60)
    print("TEST 1: Configuration Loading")
    print("="*60)
    
    try:
        from src.utils import load_config
        config = load_config('config.yaml')
        print("[PASS] Config loaded successfully")
        print(f"  LLM Provider: {config['llm']['provider']}")
        print(f"  Output Dir: {config['output']['videos_dir']}")
        return True
    except Exception as e:
        print(f"[FAIL] Config loading failed: {e}")
        return False


def test_llm_client():
    """Test LLM client initialization."""
    print("\n" + "="*60)
    print("TEST 2: LLM Client")
    print("="*60)
    
    try:
        from src.utils import load_config
        from src.llm_client import LLMClient
        
        config = load_config('config.yaml')
        client = LLMClient(config['llm'])
        print(f"[OK] LLM Client initialized")
        print(f"  Provider: {client.provider}")
        print(f"  Model: {client.model}")
        
        # Try a simple generation
        print("\n  Testing simple generation...")
        response = client.generate("Say 'Hello' in one word")
        print(f"  Response: {response[:50]}...")
        print("[OK] LLM generation works!")
        
        return True
    except Exception as e:
        print(f"[X] LLM client failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_script_generator():
    """Test script generator."""
    print("\n" + "="*60)
    print("TEST 3: Script Generator")
    print("="*60)
    
    try:
        from src.utils import load_config
        from src.script_generator import ScriptGenerator
        
        config = load_config('config.yaml')
        generator = ScriptGenerator(config)
        
        print("[OK] Script generator initialized")
        
        # Generate a simple script
        print("\n  Generating script for 'What is HTTP'...")
        script = generator.generate_script("What is HTTP")
        
        print(f"[OK] Script generated!")
        print(f"  Scenes: {script['scene_count']}")
        print(f"  Duration: {script['total_duration']}s")
        print(f"\n  First scene narration:")
        print(f"  '{script['scenes'][0]['narration'][:100]}...'" if len(script['scenes']) > 0 else "  No scenes")
        
        return True
    except Exception as e:
        print(f"[X] Script generator failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_blueprint_generator():
    """Test blueprint generator."""
    print("\n" + "="*60)
    print("TEST 4: Blueprint Generator")
    print("="*60)
    
    try:
        from src.utils import load_config
        from src.blueprint_generator import BlueprintGenerator
        
        config = load_config('config.yaml')
        generator = BlueprintGenerator(config)
        
        # Create a simple mock script
        mock_script = {
            'topic': 'Test Topic',
            'total_duration': 10,
            'scene_count': 1,
            'scenes': [{
                'scene_id': 1,
                'start_time': 0,
                'end_time': 10,
                'duration': 10,
                'narration': 'This shows a client connecting to a server',
                'visual_description': 'Client and server boxes with arrow'
            }]
        }
        
        print("[OK] Blueprint generator initialized")
        print("\n  Generating blueprint from mock script...")
        
        blueprint = generator.generate_blueprint(mock_script)
        
        print(f"[OK] Blueprint generated!")
        print(f"  Scenes: {len(blueprint['scenes'])}")
        print(f"  Elements in scene 1: {len(blueprint['scenes'][0]['elements'])}")
        print(f"  Animations in scene 1: {len(blueprint['scenes'][0]['animations'])}")
        
        return True
    except Exception as e:
        print(f"[X] Blueprint generator failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("QUICK TEST SUITE - Core Components")
    print("="*60)
    print("\nNote: This tests LLM and blueprint generation only.")
    print("Full video generation requires TTS and Manim installation.\n")
    
    results = []
    
    results.append(("Config Loading", test_config()))
    results.append(("LLM Client", test_llm_client()))
    results.append(("Script Generator", test_script_generator()))
    results.append(("Blueprint Generator", test_blueprint_generator()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for name, passed in results:
        status = "[OK] PASS" if passed else "[X] FAIL"
        print(f"{status}: {name}")
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    print(f"\nPassed: {passed_count}/{total_count}")
    
    if passed_count == total_count:
        print("\n[SUCCESS] All core components working!")
        print("\nNext steps:")
        print("  1. Install TTS: pip install TTS (requires Python < 3.12)")
        print("  2. Install Ollama or get Groq API key")
        print("  3. Run full pipeline: python main.py --topic 'Your Topic'")
        return 0
    else:
        print("\n[WARNING]  Some tests failed. Check errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())


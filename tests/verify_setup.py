"""
Setup verification script - Tests all components are properly installed
"""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check Python version."""
    print("Checking Python version...")
    version = sys.version_info
    
    if version.major >= 3 and version.minor >= 9:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor} (need 3.9+)")
        return False


def check_ffmpeg():
    """Check if FFmpeg is installed."""
    print("\nChecking FFmpeg...")
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"  ✓ {version}")
            return True
        else:
            print("  ✗ FFmpeg not found")
            return False
    except Exception as e:
        print(f"  ✗ FFmpeg not found: {e}")
        print("    Install from: https://ffmpeg.org/download.html")
        return False


def check_package(package_name, import_name=None):
    """Check if a Python package is installed."""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"  ✓ {package_name}")
        return True
    except ImportError:
        print(f"  ✗ {package_name} not installed")
        return False


def check_python_packages():
    """Check if required packages are installed."""
    print("\nChecking Python packages...")
    
    packages = [
        ('manim', 'manim'),
        ('groq', 'groq'),
        ('Coqui TTS', 'TTS'),
        ('pyyaml', 'yaml'),
        ('ffmpeg-python', 'ffmpeg'),
        ('python-dotenv', 'dotenv'),
    ]
    
    all_ok = True
    for package_name, import_name in packages:
        if not check_package(package_name, import_name):
            all_ok = False
    
    return all_ok


def check_config():
    """Check if configuration files exist."""
    print("\nChecking configuration...")
    
    config_file = Path("config.yaml")
    if config_file.exists():
        print(f"  ✓ config.yaml found")
        config_ok = True
    else:
        print(f"  ✗ config.yaml not found")
        print(f"    Copy from config.yaml.example")
        config_ok = False
    
    env_file = Path(".env")
    if env_file.exists():
        print(f"  ✓ .env found")
    else:
        print(f"  ⚠ .env not found (optional if using Ollama)")
        print(f"    Copy .env.example to .env and add Groq API key")
    
    return config_ok


def check_groq_connection():
    """Test Groq API connection."""
    print("\nTesting Groq API connection...")
    
    try:
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        api_key = os.getenv('GROQ_API_KEY')
        
        if not api_key:
            print("  ⚠ GROQ_API_KEY not set (using Ollama?)")
            return True  # Not an error if using Ollama
        
        try:
            from groq import Groq
            client = Groq(api_key=api_key)
            
            # Try a simple completion
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            
            print("  ✓ Groq API connection successful")
            return True
            
        except Exception as e:
            print(f"  ✗ Groq API error: {e}")
            return False
            
    except Exception as e:
        print(f"  ⚠ Could not test Groq: {e}")
        return True


def check_tts():
    """Test TTS installation."""
    print("\nTesting Coqui TTS...")
    
    try:
        from TTS.api import TTS
        print("  ✓ Coqui TTS installed")
        
        # Try listing models
        print("  ℹ Available TTS models will download on first use")
        return True
        
    except Exception as e:
        print(f"  ✗ TTS error: {e}")
        return False


def check_manim():
    """Test Manim installation."""
    print("\nTesting Manim...")
    
    try:
        import manim
        print(f"  ✓ Manim {manim.__version__} installed")
        return True
    except Exception as e:
        print(f"  ✗ Manim error: {e}")
        return False


def main():
    """Run all checks."""
    print("="*60)
    print("Video Synthesis System - Setup Verification")
    print("="*60)
    
    checks = [
        ("Python version", check_python_version),
        ("FFmpeg", check_ffmpeg),
        ("Python packages", check_python_packages),
        ("Configuration", check_config),
        ("Groq API", check_groq_connection),
        ("Coqui TTS", check_tts),
        ("Manim", check_manim),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n  ✗ Error checking {name}: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    all_passed = all(results.values())
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\nChecks passed: {passed}/{total}")
    
    if all_passed:
        print("\n✅ All checks passed! System is ready.")
        print("\nNext steps:")
        print("  1. Review config.yaml settings")
        print("  2. Run a test: python main.py --topic 'What is HTTP'")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please resolve issues above.")
        print("\nFor help, see SETUP.md")
        return 1


if __name__ == "__main__":
    sys.exit(main())

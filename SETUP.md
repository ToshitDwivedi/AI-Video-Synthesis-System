# Open-Source Tools Setup Guide

This guide covers installation and setup for all the free/open-source tools used in this project.

## Prerequisites

- Python 3.9 or higher
- FFmpeg installed on your system
- At least 4GB RAM (8GB recommended for video rendering)
- Git

## 1. System Dependencies

### Windows
```powershell
# Install FFmpeg via chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg libcairo2-dev pkg-config python3-dev
```

### macOS
```bash
brew install ffmpeg cairo pkg-config
```

## 2. Python Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

## 3. Install Manim (Animation Framework)

```bash
# Install Manim Community Edition
pip install manim

# Verify installation
manim --version
```

## 4. Install Coqui TTS (Text-to-Speech)

```bash
# Install Coqui TTS
pip install TTS

# List available models
tts --list_models

# Download a recommended model (will auto-download on first use)
# English multi-speaker model is good for variety
```

**Recommended Models:**
- `tts_models/en/ljspeech/tacotron2-DDC` - Fast, good quality
- `tts_models/en/vctk/vits` - Multiple voices, high quality
- `tts_models/multilingual/multi-dataset/xtts_v2` - Best quality, slower

## 5. LLM Setup (Choose One)

### Option A: Groq API (Free, Cloud-based)

1. Create account at https://groq.com
2. Get your free API key from console
3. Add to environment variables:

```bash
# Windows PowerShell
$env:GROQ_API_KEY = "your-groq-api-key-here"

# Linux/macOS
export GROQ_API_KEY="your-groq-api-key-here"
```

**Available Free Models:**
- `llama-3.3-70b-versatile` - Best for complex reasoning
- `llama-3.1-8b-instant` - Fastest, good for scripts
- `mixtral-8x7b-32768` - Great for long context

### Option B: Ollama (100% Local, Offline)

```bash
# Install Ollama
# Visit: https://ollama.ai/download

# Pull a model (one-time)
ollama pull llama3.1

# Verify
ollama list
```

**Recommended Models:**
- `llama3.1:8b` - Fast, balanced (4.7GB)
- `llama3.1:70b` - Better quality, slower (40GB)
- `mistral` - Good alternative (4.1GB)

## 6. Install Project Dependencies

```bash
# Navigate to project directory
cd "d:\Test\ATG_Group Assignment\Assignment2"

# Install all dependencies
pip install -r requirements.txt
```

## 7. Configuration

Create `config.yaml` in project root:

```yaml
# LLM Configuration
llm:
  provider: "groq"  # or "ollama"
  
  # For Groq
  groq:
    api_key: "${GROQ_API_KEY}"  # Will read from environment variable
    model: "llama-3.1-8b-instant"
  
  # For Ollama
  ollama:
    model: "llama3.1:8b"
    base_url: "http://localhost:11434"

# TTS Configuration
tts:
  model: "tts_models/en/ljspeech/tacotron2-DDC"
  voice_speed: 1.0
  
# Manim Configuration
manim:
  quality: "high_quality"  # low_quality, medium_quality, high_quality, production_quality
  fps: 30
  resolution: "1080p"  # 480p, 720p, 1080p, 1440p, 2160p

# Output Configuration
output:
  videos_dir: "./output/videos"
  temp_dir: "./output/temp"
  blueprints_dir: "./output/blueprints"
```

## 8. Verify Installation

Run the test script to verify all components:

```bash
# This will test each component
python tests/verify_setup.py
```

Expected output:
```
✓ FFmpeg detected: 4.4.2
✓ Manim installed: 0.18.0
✓ Coqui TTS installed: 0.22.0
✓ Groq API connection successful
✓ TTS model ready
✓ All systems operational!
```

## 9. First Run

Generate a simple test video:

```bash
# Simple topic to test the pipeline
python main.py --topic "What is HTTP" --duration 20 --output test.mp4
```

## Resource Requirements

**Minimum:**
- CPU: Quad-core
- RAM: 4GB
- Disk: 10GB free space

**Recommended:**
- CPU: 6+ cores
- RAM: 8GB
- Disk: 20GB free space
- GPU: Optional, speeds up Manim rendering

## Troubleshooting

### FFmpeg not found
```bash
# Verify FFmpeg is in PATH
ffmpeg -version

# If not found, add to PATH or reinstall
```

### Coqui TTS slow download
Models auto-download on first use. Be patient for the initial download (can be 500MB-2GB).

### Ollama connection error
```bash
# Start Ollama service
ollama serve

# In another terminal, test
ollama run llama3.1 "Hello"
```

### Manim rendering errors
Ensure Cairo and other system dependencies are installed for your OS.

## Optional: GPU Acceleration

For faster TTS and potential video rendering:

```bash
# Install PyTorch with CUDA support (if you have NVIDIA GPU)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## Cost Summary

**Total Cost: $0** ✨

All tools are completely free and open-source. Groq API has generous free tier limits that are sufficient for this project.

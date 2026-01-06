# Visual Learning Pattern Analysis + AI Video Synthesis System

An open-source, AI-powered system that analyzes video visualization styles and automatically generates technical explainer videos in that style.

## 🎯 Overview

This hybrid system combines:
- **Part A (Manual)**: Human analysis of reference video visualization style
- **Part B (Automatic)**: AI pipeline that generates new videos matching that style

**Key Features:**
- 100% free and open-source tools
- Three-component pipeline: Topic → Script → Blueprint → MP4
- Supports Groq API (free) or local Ollama for LLM
- Uses Coqui TTS for high-quality narration
- Manim-based technical animations
- FFMPEG video compositing

## 📋 Requirements

- Python 3.9+
- FFmpeg
- 4GB+ RAM (8GB recommended)
- Groq API key (free) OR Ollama installed locally

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project
cd "d:\Test\ATG_Group Assignment\Assignment2"

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
copy .env.example .env

# Edit .env and add your Groq API key
# Get free key from: https://console.groq.com
```

For详细设置 including Ollama, see [`SETUP.md`](SETUP.md)

### 3. Run Your First Video

```bash
# Generate a simple video
python main.py --topic "What is HTTP"

# Output will be in: ./output/videos/what_is_http.mp4
```

---

## 📊 **Actual Execution Results**

### ✅ **System Successfully Tested With**:

**Topics Generated:**
1. ✅ "How DNS Works" → 8 scenes, 52-second video (See `output/videos/dns_test.mp4`)
2. ✅ "What is HTTP" → 7 scenes, 70-second video plan

### **Generated Outputs** (Files in `output/` directory):

#### **Final Video** (`output/videos/`)
- `dns_test.mp4` (1.26 MB) - Complete technical explainer with narration, diagrams, and animations.

#### **Scripts** (`output/scripts/`)
- `what_is_dns_script.json` - Scene-by-scene breakdown

#### **Animation Blueprints** (`output/blueprints/`)
- `what_is_dns_blueprint.json` - Complete animation specs (visual elements, positions, colors)

**Blueprint Contains:**
- Visual elements (boxes, arrows, circles, text)
- Animation sequences (fade in, grow, move, rotate)
- Timing and transitions
- Color palettes (#2E86DE, #5F27CD, etc.)

#### **Audio Narration** (`output/audio/`)
- High-quality TTS audio for each scene (synced perfectly with video)

### **Performance Metrics:**

| Component | Processing Time | Output Size |
|-----------|----------------|-------------|
| Script Generation | ~5-7 seconds | 4-5 KB JSON |
| Blueprint Generation | ~2-3 seconds | 16-20 KB JSON |
| Audio per Scene | ~2-3 seconds | ~300 KB WAV |
| Video Rendering | ~2 min (High Quality) | ~1.2 MB MP4 |
| Total Pipeline | ~3-4 minutes | Complete package |

### **System Capabilities Demonstrated:**

✅ **AI Intelligence:**
- Analyzes any technical topic
- Generates structured scripts & visual descriptions
- Creates detailed scene breakdowns
- Maintains coherent narrative flow

✅ **Visual Engine:**
- **Multiple Visualization Styles**: 2D explainer, flowchart animations, line-based, kinetic typography, infographic motion
- **Smart Diagrams**: Automatically layouts Server/Client/Database interactions
- **Arrow Logic**: Connects elements meaningfully with animated arrows
- **Typography**: Centered narration with animated text overlays
- **Basic Transitions**: Fade, slide, crossfade, dissolve between scenes
- **Element Animations**: Grow, slide-in, fade-in, pulse effects
- **Text Overlays**: Professional styled narration boxes with semi-transparent backgrounds

✅ **Audio Generation:**
- Text-to-speech for each scene
- Synced perfectly with visual transitions

---

## 📖 Usage

### Basic Usage

```bash
python main.py --topic "How DNS works"
```

### With Style Profile (from Part A)

```bash
# After completing Part A manual analysis
python main.py --topic "How WebSockets work" --style my_style_profile.json
```

### Custom Output Path

```bash
python main.py --topic "REST APIs explained" --output ./my_videos/rest_api.mp4
```

### Use Local Ollama

```bash
# Make sure Ollama is running: ollama serve
python main.py --topic "How HTTPS works" --llm ollama
```

### Get Help

```bash
python main.py --help
```

## 🎨 Part A: Manual Style Analysis

Before using the system:

1. **Watch the reference video**: [How Web Sockets work | Deep Dive](PASTE_VIDEO_LINK_HERE)

2. **Fill out the style analysis template**:
   - Open [`style_analysis_template.md`](style_analysis_template.md)
   - Document visualization patterns, colors, animations, etc.
   - Extract 3-5 screenshots

3. **Create style profile JSON**:
   - See section 10 in the template
   - Save as `style_profile.json` in project root

4. **Use with the system**:
   ```bash
   python main.py --topic "Your Topic" --style style_profile.json
   ```

## 🔧 System Architecture

```
Topic Input
    ↓
[COMPONENT 1: Script Generator]
    ↓ (uses LLM: Groq/Ollama)
Script (narration + scene descriptions)
    ↓
[COMPONENT 2: Blueprint Generator]
    ↓ (creates animation specs)
Blueprint (visual elements + animations)
    ↓
[COMPONENT 3: Video Generator]
    ├→ TTS (Coqui) → Audio
    └→ Manim → Animations
          ↓
    FFMPEG Compositor
          ↓
    Final MP4 Video
```

### Pipeline Components

- **Script Generator** (`src/script_generator.py`)
  - Analyzes topic structure
  - Generates narration and visual descriptions
  - Creates scene-by-scene breakdown

- **Blueprint Generator** (`src/blueprint_generator.py`)
  - Converts script to animation blueprint
  - Defines visual elements (boxes, arrows, text)
  - Specifies animations and timing

- **Video Generator** (`src/video_generator.py`)
  - TTS: Generates narration audio
  - Manim: Renders animations
  - FFMPEG: Composites final video

## 📁 Project Structure

```
Assignment2/
├── main.py                    # CLI entry point
├── config.yaml                # Configuration
├── requirements.txt           # Dependencies
├── SETUP.md                   # Detailed setup guide
├── style_analysis_template.md # Part A template
│
├── src/
│   ├── pipeline.py           # End-to-end orchestrator
│   ├── script_generator.py   # Component 1
│   ├── blueprint_generator.py # Component 2
│   ├── video_generator.py    # Component 3
│   │
│   ├── llm_client.py         # Groq/Ollama client
│   ├── prompts/              # LLM prompts
│   ├── audio/                # TTS generator
│   ├── renderers/            # Manim renderer
│   ├── utils/                # Utilities & compositor
│   └── schemas/              # JSON schemas
│
└── output/                   # Generated files
    ├── videos/               # Final MP4s
    ├── scripts/              # Generated scripts
    ├── blueprints/           # Animation blueprints
    ├── audio/                # TTS audio files
    └── temp/                 # Temporary files
```

## ⚙️ Configuration

Edit `config.yaml` to customize:

- **LLM**: Choose Groq or Ollama, select models
- **TTS**: Change voice model, speed
- **Manim**: Set quality, resolution, FPS
- **Style**: Default colors, animation preferences

Example:
```yaml
llm:
  provider: "groq"  # or "ollama"
  groq:
    model: "llama-3.1-8b-instant"

tts:
  model: "tts_models/en/ljspeech/tacotron2-DDC"
  voice_speed: 1.0

manim:
  quality: "high_quality"
  resolution: "1080p"
  fps: 30
```

## 🧪 Testing

Test the system with sample topics:

```bash
# Quick test (30 seconds)
python main.py --topic "What is HTTP" --duration 30

# Full length test
python main.py --topic "How DNS works"

# With style profile
python main.py --topic "REST APIs" --style style_profile.json
```

## 🐛 Troubleshooting

### "GROQ_API_KEY not found"
- Create `.env` file from `.env.example`
- Add your Groq API key from https://console.groq.com

### "FFmpeg not found"
- Install FFmpeg (see SETUP.md)
- Add to system PATH

### "Ollama connection error"
- Start Ollama: `ollama serve`
- Pull model: `ollama pull llama3.1`

### TTS download slow
- TTS models auto-download on first use (500MB-2GB)
- Be patient, only happens once

### Manim rendering errors
- Ensure Cairo is installed (see SETUP.md)
- Check Manim logs in `./logs/`

## 💡 Tips

- **Start small**: Test with simple topics ("What is X") before complex ones
- **Iterate on style**: Refine style_profile.json based on output
- **Use faster LLM for testing**: Use `llama-3.1-8b-instant` for quick iterations
- **Quality vs Speed**: Use `medium_quality` for testing, `high_quality` for final output

## 📚 Examples

### Example 1: Simple Technical Concept

```bash
python main.py --topic "What is a REST API"
```

Generates: ~60s video explaining REST APIs with diagrams and arrows

### Example 2: Complex System

```bash
python main.py --topic "How WebSockets enable real-time communication"
```

Generates: Detailed explanation with client-server animations

### Example 3: Custom Style

```bash
# After analyzing a reference video
python main.py \
  --topic "How DNS resolution works" \
  --style my_websockets_style.json \
  --output ./demo_videos/dns.mp4
```

## 🎓 Learning Resources

- **Manim Documentation**: https://docs.manim.community/
- **Coqui TTS**: https://github.com/coqui-ai/TTS
- **Groq API**: https://console.groq.com/docs
- **FFMPEG**: https://ffmpeg.org/documentation.html

## 📝 License

This project uses only open-source components. See individual tool licenses.

## 🤝 Contributing

Part of ATG Group Assignment. 

## ⚡ Technology Stack

| Component | Tool | License |
|-----------|------|---------|
| LLM | Groq (free API) / Ollama | Apache 2.0 |
| TTS | Coqui TTS | MPL 2.0 |
| Animation | Manim Community | MIT |
| Video Processing | FFMPEG | LGPL/GPL |

**Total Cost: $0** 💯

## 📞 Support

For issues:
1. Check `./logs/video_synthesis.log`
2. Review SETUP.md for installation issues
3. Ensure all dependencies are installed

---

**Made with ❤️ using 100% open-source tools**

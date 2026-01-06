# Visual Learning Pattern Analysis + AI Video Synthesis System

**Reference Video**: [How Web Sockets work | Deep Dive](https://www.youtube.com/watch?v=your_video_link)

An open-source, AI-powered system that analyzes video visualization styles and automatically generates technical explainer videos in that style for any topic.

## 🎯 Project Objective

Create a hybrid system where:
- **Manual Step**: Engineers watch a reference video and identify the visualization style
- **Automatic Step**: AI generates new MP4 videos in that style for any topic

## 🏗️ System Overview

This hybrid system is divided into two major parts:

### **PART A — Manual Research Task** 
Human analysis of the reference video to create a style foundation:
- **Visualization Style Identification**: Document the visual patterns (2D explainer, line-based animation, flowchart + arrows, character-based, whiteboard/doodle, UI walkthrough, kinetic typography, infographic motion graphics, storytelling scenes)
- **Report Generation**: Create comprehensive Google Docs report with style analysis
- **Style Profile Creation**: Extract reusable style parameters for the AI system

### **PART B — Automatic System (Prototype)**
AI-powered pipeline that generates videos automatically:
1. **Topic → Script (AI Automatic)**: Generate narration script, scene-by-scene concepts, short explanations, voice-over text
2. **Script → Animation Blueprint (AI Automatic)**: Convert script + style profile into storyboard, element list, animation instructions, timing, transitions, prompts for asset generation
3. **Blueprint → MP4 Video (AI Automatic)**: Generate final video with visuals, text overlays, basic transitions, and optional AI TTS narration

**Key Features:**
- 100% free and open-source tools
- Three-stage automatic pipeline: Topic → Script → Blueprint → MP4
- Supports Groq API (free) or local Ollama for LLM
- Multiple TTS options (Coqui TTS, gTTS, pyttsx3)
- Manim-based technical animations
- FFMPEG video compositing
- Style-aware generation based on manual analysis

## 📋 Requirements

- Python 3.9+
- FFmpeg
- 4GB+ RAM (8GB recommended)
- Groq API key (free) OR Ollama installed locally

## 🚀 Quick Start

See [QUICKSTART.md](QUICKSTART.md) for detailed step-by-step execution guide.

### Quick Installation

```bash
# Navigate to project
cd "d:\Test\ATG_Group Assignment\Assignment2"

# Activate virtual environment (Windows)
venv311\Scripts\activate

# Verify dependencies are installed
pip install -r requirements.txt
```

### Quick Run

```bash
# Set up API key (first time only)
# Edit .env file and add: GROQ_API_KEY=your_key_here
# Get free key from: https://console.groq.com

# Generate your first video
python main.py --topic "What is HTTP"

# Output: ./output/videos/what_is_http.mp4
```

For complete prerequisites and troubleshooting, see [QUICKSTART.md](QUICKSTART.md).

---

## 📖 PART A: Manual Research Task

Before running the automatic system, you must complete the manual analysis:

### Step 1: Watch the Reference Video
Watch: [How Web Sockets work | Deep Dive](https://www.youtube.com/watch?v=your_video_link)

### Step 2: Identify Visualization Style
Document which style category the video uses:

| Style Category | Description |
|----------------|-------------|
| **2D Explainer** | Flat design, simple shapes, clean backgrounds |
| **Line-based Animation** | Sketch/drawing style, paths revealing over time |
| **Flowchart + Arrow Animations** | Boxes connected with animated arrows showing data flow |
| **Character-based** | Animated characters explaining concepts |
| **Whiteboard/Doodle** | Hand-drawn aesthetic, sketch-like elements |
| **UI Walkthrough** | Screen recordings, interface demonstrations |
| **Kinetic Typography** | Text-focused, dynamic text animations |
| **Infographic Motion Graphics** | Data visualization, charts, stats |
| **Storytelling Scenes** | Narrative-driven with scene transitions |

### Step 3: Create Google Docs Report
Document your findings in a comprehensive report including:
- Video title and link
- Primary visualization style identified
- Visual elements observed (shapes, colors, transitions)
- Animation techniques used
- Typography and text style
- Color palette
- Pacing and timing patterns
- Screenshots (3-5 key frames)

**Template available**: `style_analysis_template.md`

### Step 4: Create Style Profile JSON
Convert your analysis into a machine-readable format:

```json
{
  "video_reference": "How Web Sockets work | Deep Dive",
  "primary_style": "flowchart_arrow_animations",
  "secondary_styles": ["2d_explainer", "kinetic_typography"],
  "color_palette": {
    "primary": "#2E86DE",
    "secondary": "#5F27CD",
    "background": "#1E1E1E",
    "text": "#FFFFFF"
  },
  "animation_preferences": {
    "transition_type": "fade",
    "element_animation": "slide_in",
    "arrow_style": "curved",
    "text_animation": "fade_in_words"
  },
  "visual_elements": [
    "boxes_for_components",
    "arrows_for_data_flow",
    "labels_with_icons",
    "centered_narration_text"
  ]
}
```

Save as: `style_profile.json`

---

## ⚙️ PART B: Automatic System (Prototype)

### Stage 1: Topic → Script (AI Automatic)

Given any topic, the AI automatically generates:
- **Narration script**: Complete voice-over text
- **Scene-by-scene concepts**: Visual description for each scene
- **Short explanations**: Bite-sized concept breakdowns
- **Timing**: Duration and pacing for each scene

**Example output**: `output/scripts/what_is_http_script.json`

```json
{
  "topic": "What is HTTP",
  "total_scenes": 7,
  "estimated_duration": "70 seconds",
  "scenes": [
    {
      "scene_number": 1,
      "narration": "HTTP stands for Hypertext Transfer Protocol...",
      "visual_description": "Show large text 'HTTP' with subtitle...",
      "duration": 8
    }
  ]
}
```

### Stage 2: Script → Animation Blueprint (AI Automatic)

AI converts script + style profile into detailed animation specs:
- **Storyboard**: Frame-by-frame visual plan
- **Element list**: All visual objects (boxes, arrows, text)
- **Animation instructions**: Movement, fades, transitions
- **Timing**: Precise start/end times
- **Transitions**: Scene-to-scene effects
- **Asset prompts**: Descriptions for any generated assets

**Example output**: `output/blueprints/what_is_http_blueprint.json`

```json
{
  "blueprint_id": "http_explainer_20260106",
  "based_on_style": "flowchart_arrow_animations",
  "total_scenes": 7,
  "scenes": [
    {
      "scene_id": 1,
      "visual_elements": [
        {
          "type": "box",
          "label": "Client Browser",
          "position": [0, 2],
          "color": "#2E86DE",
          "animation": "fade_in"
        },
        {
          "type": "arrow",
          "from": "client",
          "to": "server",
          "label": "HTTP Request",
          "animation": "grow"
        }
      ],
      "animations": [
        {
          "element": "box_1",
          "type": "fade_in",
          "start_time": 0.5,
          "duration": 1.0
        }
      ]
    }
  ]
}
```

### Stage 3: Blueprint → MP4 Video (AI Automatic)

The system generates the final video using:

**Allowed Tools:**
- **Manim**: Mathematical animation engine for technical diagrams
- **FFMPEG**: Video compositing and encoding
- **Lottie**: JSON-based animation (optional)
- **Pika/Runway API**: AI video generation (optional, API-based)
- Any internal or open-source animation framework

**Final MP4 Includes:**
- ✅ Visuals based on the blueprint
- ✅ Text overlays (narration, labels, annotations)
- ✅ Basic transitions (fade, crossfade, slide)
- ✅ Optional narration (AI TTS: Coqui/gTTS/pyttsx3)

**Example output**: `output/videos/what_is_http.mp4`

---

## 📊 System Execution Results

### ✅ Successfully Tested Topics:

| Topic | Scenes | Duration | Output File |
|-------|--------|----------|-------------|
| "How DNS Works" | 8 | 52 sec | `dns_test.mp4` (1.26 MB) |
| "What is HTTP" | 7 | 70 sec | `what_is_http.mp4` |

### Generated Output Files

**Directory structure** (`output/`):

```
output/
├── videos/              # Final MP4 videos
│   └── dns_test.mp4                (1.26 MB, complete with narration & animations)
├── scripts/             # AI-generated scripts
│   └── what_is_dns_script.json     (4.6 KB, scene-by-scene breakdown)
├── blueprints/          # Animation specifications
│   └── what_is_dns_blueprint.json  (16.8 KB, visual elements + timing)
├── audio/               # TTS narration files
│   ├── what_is_dns_scene_1.wav     (277 KB)
│   ├── what_is_dns_scene_2.wav     (297 KB)
│   └── ... (additional scene audio files)
└── temp/                # Temporary rendering files
```

### Performance Metrics

| Pipeline Stage | Processing Time | Output Size |
|----------------|-----------------|-------------|
| Script Generation | 5-7 seconds | 4-5 KB JSON |
| Blueprint Generation | 2-3 seconds | 16-20 KB JSON |
| Audio per Scene | 2-3 seconds | ~300 KB WAV |
| Video Rendering (Manim) | ~2 minutes | ~1.2 MB MP4 |
| **Total Pipeline** | **3-4 minutes** | **Complete video package** |

### System Capabilities Demonstrated

✅ **AI Intelligence:**
- Analyzes any technical topic
- Generates structured scripts with scene-by-scene breakdowns
- Creates detailed visual descriptions
- Maintains coherent narrative flow across scenes
- Adapts content structure to topic complexity

✅ **Visual Engine:**
- **Multiple Visualization Styles**: 2D explainer, flowchart animations, line-based, kinetic typography, infographic motion
- **Smart Diagrams**: Automatically layouts Server/Client/Database interactions with spatial awareness
- **Arrow Logic**: Connects elements meaningfully with animated directional arrows
- **Typography**: Centered narration with animated text overlays
- **Transitions**: Fade, slide, crossfade, dissolve between scenes
- **Element Animations**: Grow, slide-in, fade-in, pulse, rotate effects
- **Text Overlays**: Professional styled narration boxes with semi-transparent backgrounds
- **Color Consistency**: Uses defined palettes from style profiles

✅ **Audio Generation:**
- High-quality text-to-speech for each scene
- Multiple TTS engine support (Coqui, gTTS, pyttsx3)
- Audio-visual synchronization
- Proper pacing aligned with scene duration

---

## 📖 Usage Guide

### Basic Usage

```bash
# Generate video for any topic
python main.py --topic "How DNS works"
```

### With Style Profile (Recommended after Part A)

```bash
# Use your manually analyzed style
python main.py --topic "How WebSockets work" --style style_profile.json
```

### Custom Output Path

```bash
python main.py --topic "REST APIs explained" --output ./my_videos/rest_api.mp4
```

### Use Local LLM (Ollama)

```bash
# Ensure Ollama is running: ollama serve
python main.py --topic "How HTTPS works" --llm ollama
```

### Full Command Reference

```bash
python main.py --help

# Options:
#   --topic TEXT        Topic to generate video about (required)
#   --output PATH       Custom output path (default: output/videos/)
#   --style PATH        Style profile JSON from Part A (optional)
#   --llm TEXT          LLM provider: groq|ollama (default: groq)
#   --duration INT      Target video duration in seconds (optional)
```
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

## 🎨 Part A: Creating Style Profiles

### Step-by-Step Guide

#### 1. Watch & Analyze Reference Video
- Reference: [How Web Sockets work | Deep Dive](https://www.youtube.com/watch?v=your_video_link)
- Watch multiple times, taking notes on visual patterns
- Take 3-5 screenshots of key frames

#### 2. Document in Google Docs Report
Create a comprehensive analysis document with these sections:

**Report Structure:**
```
1. Video Information
   - Title, link, duration, creator

2. Primary Visualization Style
   - Main category identified
   - Supporting evidence (timestamps)

3. Visual Elements Inventory
   - Shapes used (boxes, circles, arrows)
   - Text styles (fonts, sizes, animations)
   - Icons and graphics

4. Color Analysis
   - Primary colors (hex codes)
   - Background colors
   - Text/contrast colors
   - Color usage patterns

5. Animation Techniques
   - Element entrance/exit methods
   - Transition effects between scenes
   - Arrow animations
   - Text reveals

6. Layout & Composition
   - Element positioning
   - Screen divisions
   - Visual hierarchy

7. Timing & Pacing
   - Average scene duration
   - Animation speeds
   - Narration timing

8. Audio-Visual Sync
   - How visuals support narration
   - Key sync points

9. Screenshots
   - 3-5 annotated key frames

10. Style Profile JSON
    - Machine-readable configuration
```

#### 3. Generate Style Profile JSON

Based on your analysis, create `style_profile.json`:

```json
{
  "metadata": {
    "video_reference": "How Web Sockets work | Deep Dive",
    "analyzed_by": "Engineer Name",
    "analysis_date": "2026-01-06",
    "reference_url": "https://youtube.com/watch?v=..."
  },
  
  "visualization_style": {
    "primary": "flowchart_arrow_animations",
    "secondary": ["2d_explainer", "kinetic_typography"],
    "complexity": "medium"
  },
  
  "color_palette": {
    "primary": "#2E86DE",
    "secondary": "#5F27CD",
    "accent": "#FF6348",
    "background": "#1E1E1E",
    "text": "#FFFFFF",
    "text_secondary": "#B0B0B0"
  },
  
  "visual_elements": {
    "shapes": ["boxes", "rounded_rectangles", "circles"],
    "connectors": ["curved_arrows", "straight_lines"],
    "text_elements": ["title_cards", "labels", "callouts"],
    "icons": true,
    "diagrams": ["flowcharts", "system_architecture"]
  },
  
  "animation_preferences": {
    "transition_type": "fade",
    "transition_duration": 0.5,
    "element_entrance": "fade_in",
    "element_exit": "fade_out",
    "arrow_animation": "grow_from_start",
    "text_animation": "fade_in_words",
    "animation_speed": "moderate"
  },
  
  "layout": {
    "title_position": "top_center",
    "main_content_area": "center",
    "narration_text_position": "bottom_center",
    "label_style": "above_element",
    "spacing": "comfortable"
  },
  
  "typography": {
    "title_font": "Arial Bold",
    "body_font": "Arial",
    "narration_font": "Arial",
    "title_size": 48,
    "body_size": 24,
    "narration_size": 20
  },
  
  "timing": {
    "average_scene_duration": 8,
    "min_scene_duration": 5,
    "max_scene_duration": 12,
    "transition_gap": 0.3
  }
}
```

#### 4. Test Style Profile

```bash
# Test with a different topic using your style
python main.py --topic "How DNS works" --style style_profile.json

# Compare output to reference video
# Iterate and refine style_profile.json as needed
```

---

## 🔧 System Architecture

### Complete Pipeline Flow

```
┌─────────────────────────────────────────────────────┐
│                   USER INPUT                         │
│  Topic + Optional Style Profile                     │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│         STAGE 1: Script Generator                   │
│  ┌───────────────────────────────────────────────┐  │
│  │  LLM Client (Groq API / Ollama)              │  │
│  │  - Analyzes topic structure                   │  │
│  │  - Generates narration                        │  │
│  │  - Creates scene descriptions                 │  │
│  └───────────────────────────────────────────────┘  │
│  Output: JSON Script (4-5 KB)                       │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│         STAGE 2: Blueprint Generator                │
│  ┌───────────────────────────────────────────────┐  │
│  │  LLM Client + Style Profile                  │  │
│  │  - Converts script to visual specs           │  │
│  │  - Applies style preferences                 │  │
│  │  - Defines animations & timing               │  │
│  └───────────────────────────────────────────────┘  │
│  Output: JSON Blueprint (16-20 KB)                  │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│         STAGE 3: Video Generator                    │
│  ┌──────────────────┐    ┌────────────────────────┐ │
│  │  TTS Generator   │    │  Manim Renderer        │ │
│  │  - Coqui TTS     │    │  - Creates animations  │ │
│  │  - gTTS          │    │  - Renders scenes      │ │
│  │  - pyttsx3       │    │  - Applies blueprint   │ │
│  └────────┬─────────┘    └──────────┬─────────────┘ │
│           │                          │               │
│           └──────────┬───────────────┘               │
│                      ▼                               │
│            ┌──────────────────────┐                  │
│            │  FFMPEG Compositor   │                  │
│            │  - Merges audio+video│                  │
│            │  - Adds transitions  │                  │
│            │  - Encodes final MP4 │                  │
│            └──────────────────────┘                  │
│  Output: Final MP4 Video (~1-2 MB)                   │
└─────────────────────────────────────────────────────┘
```

### Component Details

#### **Script Generator** (`src/script_generator.py`)
- **Input**: Topic string + optional style hints
- **Process**: 
  - Analyzes topic structure and complexity
  - Generates narrative flow
  - Creates scene-by-scene breakdown with narration
  - Describes visual concepts for each scene
- **Output**: Structured JSON with scenes, narration, visual descriptions, timing

#### **Blueprint Generator** (`src/blueprint_generator.py`)
- **Input**: Script JSON + style_profile.json
- **Process**:
  - Extracts visual elements from descriptions
  - Maps elements to coordinates
  - Defines animation sequences
  - Applies style preferences (colors, transitions)
  - Calculates timing and sync points
- **Output**: Detailed blueprint JSON with render-ready specs

#### **Video Generator** (`src/video_generator.py`)
- **Input**: Blueprint JSON + style preferences
- **Process**:
  - **Audio Track**: Generates TTS for each scene's narration
  - **Visual Track**: Renders animations with Manim
  - **Composition**: Merges audio+video with FFMPEG
  - **Enhancement**: Adds transitions, overlays, effects
- **Output**: Final MP4 video file

---

## 📁 Project Structure

```
Assignment2/
│
├── main.py                          # CLI entry point
├── config.yaml                      # System configuration
├── requirements.txt                 # Python dependencies
├── .env                            # API keys (create from .env.example)
│
├── README.md                        # This file (complete documentation)
├── QUICKSTART.md                    # Step-by-step execution guide
├── style_analysis_template.md       # Part A: Manual analysis template
│
├── src/                            # Source code
│   ├── pipeline.py                 # End-to-end orchestrator
│   │
│   ├── script_generator.py         # Stage 1: Topic → Script
│   ├── blueprint_generator.py      # Stage 2: Script → Blueprint
│   ├── video_generator.py          # Stage 3: Blueprint → Video
│   │
│   ├── llm_client.py              # LLM interface (Groq/Ollama)
│   │
│   ├── prompts/                    # LLM prompt templates
│   │   ├── script_prompts.py
│   │   └── blueprint_prompts.py
│   │
│   ├── audio/                      # TTS implementations
│   │   ├── tts_generator.py        # Main TTS interface
│   │   ├── gtts_generator.py       # Google TTS
│   │   └── simple_tts.py           # pyttsx3 fallback
│   │
│   ├── renderers/                  # Animation renderers
│   │   ├── manim_renderer.py       # Manim integration
│   │   └── simple_renderer.py      # Basic renderer
│   │
│   ├── schemas/                    # JSON validation schemas
│   │   └── blueprint_schema.json
│   │
│   └── utils/                      # Utilities
│       ├── config.py               # Config loader
│       └── video_compositor.py     # FFMPEG wrapper
│
├── output/                         # Generated files
│   ├── videos/                     # Final MP4 videos
│   ├── scripts/                    # Generated script JSONs
│   ├── blueprints/                 # Animation blueprint JSONs
│   ├── audio/                      # TTS audio files (.wav)
│   └── temp/                       # Temporary render files
│
├── logs/                           # Application logs
│   └── video_synthesis.log
│
├── tests/                          # Testing utilities
│   ├── quick_test.py
│   └── verify_setup.py
│
└── venv311/                        # Python virtual environment
```

## 🧪 Testing Examples

### Example 1: Simple Technical Concept
```bash
python main.py --topic "What is a REST API"
```
**Expected**: ~60s video explaining REST APIs with HTTP method diagrams and client-server arrows

### Example 2: Complex System Interaction
```bash
python main.py --topic "How WebSockets enable real-time communication"
```
**Expected**: Detailed explanation with bidirectional communication animations

### Example 3: With Custom Style Profile
```bash
# After completing Part A analysis
python main.py \
  --topic "How DNS resolution works" \
  --style my_websockets_style.json \
  --output ./demo_videos/dns.mp4
```
**Expected**: Video matching the visual style from your reference analysis

### Example 4: Using Local LLM
```bash
# Ensure Ollama is running
ollama serve

# Use local model instead of API
python main.py --topic "HTTPS encryption explained" --llm ollama
```

---

## ⚙️ Configuration

### config.yaml Structure

```yaml
# LLM Configuration
llm:
  provider: "groq"              # Options: groq, ollama
  groq:
    api_key_env: "GROQ_API_KEY"
    model: "llama-3.1-8b-instant"
    temperature: 0.7
    max_tokens: 2000
  ollama:
    base_url: "http://localhost:11434"
    model: "llama3.1"
    temperature: 0.7

# Text-to-Speech Configuration
tts:
  provider: "gtts"              # Options: coqui, gtts, pyttsx3
  voice_speed: 1.0
  language: "en"
  coqui:
    model: "tts_models/en/ljspeech/tacotron2-DDC"
  pyttsx3:
    rate: 150
    volume: 1.0

# Manim Animation Configuration
manim:
  quality: "high_quality"       # Options: low_quality, medium_quality, high_quality
  resolution: "1080p"           # Options: 480p, 720p, 1080p, 1440p, 2160p
  fps: 30
  background_color: "#1E1E1E"
  
# Style Configuration
style:
  default_colors:
    primary: "#2E86DE"
    secondary: "#5F27CD"
    accent: "#FF6348"
    background: "#1E1E1E"
    text: "#FFFFFF"
  
  animation_defaults:
    transition_duration: 0.5
    element_animation_speed: 1.0
    
# Output Configuration
output:
  video_format: "mp4"
  audio_format: "wav"
  keep_temp_files: false
```

### Environment Variables (.env)

```bash
# Required for Groq API
GROQ_API_KEY=gsk_your_api_key_here

# Optional: Ollama configuration
OLLAMA_BASE_URL=http://localhost:11434

# Optional: Custom paths
OUTPUT_DIR=./output
TEMP_DIR=./output/temp
```

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### "GROQ_API_KEY not found"
**Solution**: 
```bash
# Create .env file in project root
copy .env.example .env
# Edit .env and add: GROQ_API_KEY=your_key_here
# Get free key from: https://console.groq.com
```

#### "FFmpeg not found"
**Solution**:
```bash
# Download FFmpeg from: https://ffmpeg.org/download.html
# Add ffmpeg.exe to system PATH
# Verify: ffmpeg -version
```

#### "Ollama connection error"
**Solution**:
```bash
# Start Ollama server
ollama serve

# Pull required model
ollama pull llama3.1

# Verify model is available
ollama list
```

#### TTS Download Slow / Coqui Issues
**Issue**: First-time TTS model downloads can be 500MB-2GB  
**Solution**: 
- Be patient, only happens once
- Use `gtts` or `pyttsx3` as fallback:
  ```yaml
  # In config.yaml
  tts:
    provider: "gtts"  # or "pyttsx3"
  ```

#### Manim Rendering Errors
**Solution**:
```bash
# Check Cairo installation (Windows)
pip install pycairo

# Verify Manim
python -c "import manim; print(manim.__version__)"

# Check logs
type logs\video_synthesis.log
```

#### Unicode Errors in Console (Windows)
**Status**: Cosmetic only - pipeline still works  
**Cause**: Windows console encoding limitations  
**Impact**: No effect on output files  
**Optional Fix**: Use UTF-8 compatible terminal (Windows Terminal)

#### "Module not found" Errors
**Solution**:
```bash
# Ensure virtual environment is activated
venv311\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

---

## 💡 Tips & Best Practices

### For Part A (Manual Analysis)
- Watch the reference video **multiple times** focusing on different aspects each time
- **Screenshot key frames** for visual reference in your report
- Use **color picker tools** to extract exact hex codes
- **Time stamp** important animation techniques in your notes
- Compare with other videos in same style category to identify patterns

### For Part B (System Usage)
- **Start small**: Test with simple topics ("What is X") before complex ones ("How X and Y interact in Z systems")
- **Iterate on style**: Generate, review, refine style_profile.json based on output
- **Use faster LLM for testing**: `llama-3.1-8b-instant` for iterations, larger models for final output
- **Quality vs Speed tradeoff**: 
  - Testing: `medium_quality` Manim + `gtts` TTS (30-60 sec/video)
  - Production: `high_quality` Manim + `coqui` TTS (3-5 min/video)
- **Monitor outputs**: Check intermediate JSON files to debug issues early

### Performance Optimization
```yaml
# Fast iteration config (testing)
manim:
  quality: "low_quality"
  fps: 15
tts:
  provider: "gtts"  # Fastest

# High quality config (final)
manim:
  quality: "high_quality"
  fps: 30
tts:
  provider: "coqui"  # Best quality
```

---

## 🎓 Learning Resources

| Resource | Purpose | Link |
|----------|---------|------|
| **Manim Documentation** | Animation framework reference | https://docs.manim.community/ |
| **Coqui TTS** | Text-to-speech guide | https://github.com/coqui-ai/TTS |
| **Groq API Docs** | LLM API reference | https://console.groq.com/docs |
| **FFMPEG Guide** | Video processing | https://ffmpeg.org/documentation.html |
| **Lottie Files** | Animation examples | https://lottiefiles.com/ |

---

## ⚡ Technology Stack

| Component | Tool | License | Cost |
|-----------|------|---------|------|
| **LLM** | Groq API | Commercial | Free tier |
| **LLM (Alternative)** | Ollama | MIT | Free |
| **TTS** | Coqui TTS | MPL 2.0 | Free |
| **TTS (Alternative)** | gTTS / pyttsx3 | MIT | Free |
| **Animation** | Manim Community | MIT | Free |
| **Video Processing** | FFMPEG | LGPL/GPL | Free |
| **Python** | CPython 3.9+ | PSF | Free |

**Total Cost: $0** 💯 (100% open-source + free APIs)

### Allowed Tools (Per Assignment Requirements)
✅ **Manim**: Primary animation engine  
✅ **FFMPEG**: Video compositing and encoding  
✅ **Lottie**: Optional JSON-based animations  
✅ **Pika/Runway API**: Optional AI video generation (API-based)  
✅ **Any open-source animation framework**: Extensible architecture

---

## 📊 Project Deliverables

### Part A Deliverables (Manual)
- [ ] Google Docs report with comprehensive style analysis
- [ ] 3-5 annotated screenshots from reference video
- [ ] `style_profile.json` file with extracted parameters
- [ ] Identification of primary visualization style category

### Part B Deliverables (Automatic)
- [ ] Working Python pipeline (3 stages: Script → Blueprint → Video)
- [ ] Generated MP4 video demonstrating system capabilities
- [ ] JSON outputs (script, blueprint) for transparency
- [ ] Documentation (README.md, QUICKSTART.md)
- [ ] Configuration files (config.yaml, .env.example)

---

## 🤝 Contributing

Part of **ATG Group Assignment 2**  
Visual Learning Pattern Analysis + AI Video Synthesis System

**Team Members**: [List team members]  
**Course**: [Course name]  
**Date**: January 2026

---

## 📞 Support

### Debug Checklist
1. ✅ Check `./logs/video_synthesis.log` for detailed error messages
2. ✅ Verify `.env` file exists with valid `GROQ_API_KEY`
3. ✅ Ensure virtual environment is activated (`venv311\Scripts\activate`)
4. ✅ Confirm all dependencies installed (`pip list`)
5. ✅ Test FFmpeg (`ffmpeg -version`)
6. ✅ Verify Python version (`python --version` should show 3.9+)

### Getting Help
- Review [QUICKSTART.md](QUICKSTART.md) for step-by-step execution
- Check `tests/verify_setup.py` to validate installation
- Examine output JSON files to debug pipeline stages
- Compare your `config.yaml` with defaults

---

**Made with ❤️ using 100% open-source tools**  
**No paid subscriptions required | Full transparency | Extensible architecture**

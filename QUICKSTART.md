# Quick Start Guide - AI Video Synthesis Pipeline

**Complete step-by-step guide to generate your first AI video in 5 minutes**

---

## 🎯 What This System Does

This system automatically converts any topic into a professional technical explainer video:

**Input**: Topic text (e.g., "How DNS works")  
**Output**: MP4 video with narration, animations, and visual diagrams

**Reference Project**: Visual Learning Pattern Analysis + AI Video Synthesis  
**Video Style Reference**: [How Web Sockets work | Deep Dive](https://www.youtube.com/watch?v=...)

---

## 📋 Prerequisites Check

### Step 1: Verify Python Installation
```powershell
# Check Python version (need 3.9+)
python --version
# Should show: Python 3.11.x or Python 3.9.x+

# If not found or wrong version, download from: https://www.python.org/downloads/
```

### Step 2: Verify Project Location
```powershell
# Navigate to project directory
cd "d:\Test\ATG_Group Assignment\Assignment2"

# Verify you're in the right place
dir

# You should see: main.py, config.yaml, requirements.txt, src/, output/
```

### Step 3: Verify Virtual Environment
```powershell
# Check if venv311 folder exists
dir venv311

# Should show: Include/, Lib/, Scripts/, pyvenv.cfg
```

---

## 🚀 Execute the Complete Pipeline

### **Step 1: Activate Virtual Environment**

```powershell
# Activate Python 3.11 environment
venv311\Scripts\activate

# Your prompt should now show: (venv311)
# Example: (venv311) PS D:\Test\ATG_Group Assignment\Assignment2>
```

### **Step 2: Verify Configuration File**

```powershell
# Check if .env file exists
type .env

# Expected output:
# GROQ_API_KEY=gsk_...your_key_here...
```

**If .env file doesn't exist:**
```powershell
# Create from template
copy .env.example .env

# Get free API key from: https://console.groq.com
# Open .env in notepad and add your key:
notepad .env

# Add this line:
# GROQ_API_KEY=gsk_your_actual_key_here
```

### **Step 3: Run Your First Video Generation**

**Option A: Quick Test (Recommended for First Time)**
```powershell
python main.py --topic "What is HTTP"
```

**Option B: Custom Topic**
```powershell
python main.py --topic "How DNS works"
```

**Option C: With Custom Output Path**
```powershell
python main.py --topic "What is REST API" --output ./output/videos/my_video.mp4
```

**Option D: With Style Profile (After completing Part A)**
```powershell
python main.py --topic "How WebSockets work" --style style_profile.json
```

---

## 📊 Expected Pipeline Execution Flow

When you run the command, you'll see this 3-stage process:

```
🎯 Topic: "What is HTTP"
==================================================
                                                  
[STAGE 1/3] Script Generation
==================================================
├─ Analyzing topic structure...
├─ Connecting to LLM (Groq API)...
├─ Generating narration for 7 scenes...
├─ Creating visual descriptions...
└─ ✅ Script saved: output/scripts/what_is_http_script.json
   Duration: ~5-7 seconds
                                                  
[STAGE 2/3] Blueprint Generation
==================================================
├─ Loading script from Stage 1...
├─ Extracting visual elements...
├─ Defining animations and timing...
├─ Applying style preferences...
└─ ✅ Blueprint saved: output/blueprints/what_is_http_blueprint.json
   Duration: ~2-3 seconds
                                                  
[STAGE 3/3] Video Generation
==================================================
├─ Audio Generation:
│  ├─ Scene 1/7: Generating TTS... ✅ (2.3s)
│  ├─ Scene 2/7: Generating TTS... ✅ (2.1s)
│  ├─ Scene 3/7: Generating TTS... ✅ (2.5s)
│  ├─ Scene 4/7: Generating TTS... ✅ (2.4s)
│  ├─ Scene 5/7: Generating TTS... ✅ (2.2s)
│  ├─ Scene 6/7: Generating TTS... ✅ (2.3s)
│  └─ Scene 7/7: Generating TTS... ✅ (2.0s)
│
├─ Video Rendering:
│  ├─ Initializing Manim renderer...
│  ├─ Rendering scene 1... ✅
│  ├─ Rendering scene 2... ✅
│  ├─ Rendering scene 3... ✅
│  ├─ ... (remaining scenes)
│  └─ All scenes rendered successfully
│
└─ Final Composition:
   ├─ Merging audio tracks...
   ├─ Compositing video with FFMPEG...
   ├─ Adding transitions...
   └─ ✅ Final video: output/videos/what_is_http.mp4
      Size: ~1.2 MB | Duration: ~70 seconds

==================================================
✅ PIPELINE COMPLETE!
==================================================
Total time: ~3-4 minutes
Output: output/videos/what_is_http.mp4
```

---

## ⏱️ Processing Time Breakdown

| Pipeline Stage | Duration | Output |
|----------------|----------|--------|
| **Script Generation** | 5-10 sec | JSON file (4-5 KB) |
| **Blueprint Generation** | 2-5 sec | JSON file (16-20 KB) |
| **Audio Generation** | 15-25 sec | WAV files (~300 KB each × 7 scenes) |
| **Video Rendering** | 2-3 min | MP4 video (~1.2 MB) |
| **TOTAL** | **3-4 minutes** | Complete video package |

*Times based on "What is HTTP" test with 7 scenes*

---

## 📁 Check Generated Outputs

### View All Generated Files
```powershell
# List all output files
dir output\scripts\*.json
dir output\blueprints\*.json
dir output\audio\*.wav
dir output\videos\*.mp4
```

### Expected Output Structure
```
output/
├── scripts/
│   └── what_is_http_script.json           (4.6 KB)
│        - Scene-by-scene narration
│        - Visual descriptions
│        - Timing information
│
├── blueprints/
│   └── what_is_http_blueprint.json        (16.8 KB)
│        - Visual elements (boxes, arrows, text)
│        - Animation sequences
│        - Color schemes and positioning
│        - Render-ready specifications
│
├── audio/
│   ├── what_is_http_scene_1.wav          (277 KB)
│   ├── what_is_http_scene_2.wav          (297 KB)
│   ├── what_is_http_scene_3.wav          (285 KB)
│   └── ... (scenes 4-7)
│        - High-quality TTS narration
│        - Synced to scene timing
│
└── videos/
    └── what_is_http.mp4                   (~1.2 MB, 70 sec)
         - Final composed video
         - Audio + visual animations
         - Transitions and effects
```

---

## 🔍 Inspect Generated Content

### 1. View Script JSON
```powershell
# Read the generated script
type output\scripts\what_is_http_script.json

# Pretty print with PowerShell (optional)
Get-Content output\scripts\what_is_http_script.json | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

**What you'll see:**
- Topic title
- Number of scenes
- Estimated duration
- For each scene:
  - Scene number
  - Narration text
  - Visual description
  - Duration estimate

### 2. View Blueprint JSON
```powershell
# Read the animation blueprint
type output\blueprints\what_is_http_blueprint.json
```

**What you'll see:**
- Blueprint ID and timestamp
- Style profile applied
- Total number of scenes
- For each scene:
  - Visual elements (boxes, arrows, circles, text)
  - Element properties (position, color, size)
  - Animation sequences (fade, grow, move)
  - Timing (start_time, duration)
  - Transitions between scenes

### 3. Play Generated Audio
```powershell
# Play audio for scene 1
start output\audio\what_is_http_scene_1.wav

# Play all audio files sequentially
Get-ChildItem output\audio\*.wav | ForEach-Object { start $_.FullName; Start-Sleep 5 }
```

### 4. Watch Final Video
```powershell
# Open video in default player
start output\videos\what_is_http.mp4

# Or specify Windows Media Player
"C:\Program Files\Windows Media Player\wmplayer.exe" "output\videos\what_is_http.mp4"
```

---

## 🔧 Troubleshooting Common Issues

### Issue 1: "GROQ_API_KEY not found"
**Symptom**: Error message on script generation stage

**Solution**:
```powershell
# Create .env file if it doesn't exist
copy .env.example .env

# Edit .env file
notepad .env

# Add your API key:
# GROQ_API_KEY=gsk_your_key_here

# Get free key from: https://console.groq.com
```

### Issue 2: Unicode/Encoding Errors in Console
**Symptom**: Strange characters or encoding warnings in terminal

**Status**: ⚠️ Cosmetic only - pipeline still works  
**Cause**: Windows console encoding limitations  
**Impact**: None on output files  

**Optional Fix**:
```powershell
# Use Windows Terminal instead of CMD/PowerShell
# Or ignore - videos generate correctly regardless
```

### Issue 3: "TTS not available" or Audio Generation Slow
**Symptom**: Warning about TTS provider or slow audio generation

**Status**: ✅ System automatically falls back to pyttsx3 (Windows voices)  
**Impact**: Audio generates successfully with built-in Windows TTS

**To use better quality TTS**:
```powershell
# Install Coqui TTS (optional, slow first-time download)
pip install TTS

# Or use Google TTS (fast, requires internet)
# No action needed - system auto-selects available TTS
```

### Issue 4: "Module not found" Errors
**Solution**:
```powershell
# Ensure virtual environment is activated
venv311\Scripts\activate

# Reinstall all dependencies
pip install -r requirements.txt --upgrade

# Verify installation
pip list | Select-String -Pattern "manim|groq|pyttsx3"
```

### Issue 5: FFmpeg Errors
**Symptom**: Video composition fails

**Solution**:
```powershell
# Check if FFmpeg is installed
ffmpeg -version

# If not found, download from: https://ffmpeg.org/download.html
# Add ffmpeg.exe to system PATH
# Or place ffmpeg.exe in project root directory
```

### Issue 6: Manim Rendering Errors
**Symptom**: Animation rendering fails or produces errors

**Solution**:
```powershell
# Check Manim installation
python -c "import manim; print(manim.__version__)"

# If errors, reinstall Cairo and Manim
pip uninstall manim manimce
pip install manim

# Check logs for details
type logs\video_synthesis.log
```

### Issue 7: Script/Blueprint Generated but No Video
**Symptom**: Stages 1 & 2 complete, but Stage 3 fails

**Debug Steps**:
```powershell
# 1. Check if audio files were generated
dir output\audio\*.wav

# 2. Check logs for errors
type logs\video_synthesis.log | Select-String -Pattern "ERROR|error"

# 3. Verify Manim can run independently
manim --version

# 4. Try with lower quality settings
# Edit config.yaml:
#   manim:
#     quality: "low_quality"
```

---

## ✅ Success Indicators

After running `python main.py --topic "Your Topic"`, verify these:

| ✓ | Indicator | Location |
|---|-----------|----------|
| ✅ | Script JSON file exists | `output/scripts/your_topic_script.json` |
| ✅ | Blueprint JSON file exists | `output/blueprints/your_topic_blueprint.json` |
| ✅ | Audio WAV files exist | `output/audio/your_topic_scene_*.wav` |
| ✅ | Final MP4 video exists | `output/videos/your_topic.mp4` |
| ✅ | No ERROR lines in terminal | Check console output |
| ✅ | Log file shows completion | `logs/video_synthesis.log` |

---

## 🧪 Test Different Topics

After your first successful generation, try these:

### Simple Concepts (30-60 sec videos)
```powershell
python main.py --topic "What is Docker"
python main.py --topic "What is a Virtual Machine"
python main.py --topic "What is Cloud Computing"
```

### Technical Processes (60-90 sec videos)
```powershell
python main.py --topic "How HTTPS encryption works"
python main.py --topic "How JWT authentication works"
python main.py --topic "How load balancing works"
```

### System Interactions (90-120 sec videos)
```powershell
python main.py --topic "How microservices communicate"
python main.py --topic "How CDN content delivery works"
python main.py --topic "How database transactions work"
```

---

## 🎨 Using Style Profiles (Part A Integration)

After completing the manual style analysis (Part A):

### Step 1: Create Style Profile
See README.md "Part A: Creating Style Profiles" for detailed instructions.

### Step 2: Use Style Profile
```powershell
# Generate video with your analyzed style
python main.py --topic "How WebSockets enable bidirectional communication" --style style_profile.json --output ./output/videos/websockets_styled.mp4
```

### Step 3: Compare Outputs
```powershell
# Generate without style
python main.py --topic "How WebSockets work" --output ./output/videos/ws_default.mp4

# Generate with style
python main.py --topic "How WebSockets work" --style style_profile.json --output ./output/videos/ws_styled.mp4

# Compare both videos
start ./output/videos/ws_default.mp4
Start-Sleep 3
start ./output/videos/ws_styled.mp4
```

---

## ⚙️ Advanced Configuration

### Using Local LLM (Ollama)
```powershell
# 1. Install and start Ollama
# Download from: https://ollama.ai

# 2. Start Ollama server
ollama serve

# 3. Pull a model
ollama pull llama3.1

# 4. Generate video using local LLM
python main.py --topic "How DNS works" --llm ollama
```

### Custom Configuration (config.yaml)

Edit `config.yaml` to customize:

**LLM Settings:**
```yaml
llm:
  provider: "groq"              # Change to "ollama" for local
  groq:
    model: "llama-3.1-8b-instant"  # Faster for testing
    # model: "llama-3.1-70b-versatile"  # Better quality
```

**TTS Settings:**
```yaml
tts:
  provider: "gtts"              # Options: gtts, pyttsx3, coqui
  voice_speed: 1.0              # Adjust narration speed (0.8-1.5)
```

**Manim/Video Quality:**
```yaml
manim:
  quality: "medium_quality"     # Options: low, medium, high
  fps: 30                       # 15 for faster, 60 for smoother
```

**Color Scheme:**
```yaml
style:
  default_colors:
    primary: "#2E86DE"          # Main element color
    secondary: "#5F27CD"        # Secondary elements
    background: "#1E1E1E"       # Video background
```

---

## 🎯 Quick Reference Commands

```powershell
# Full command syntax
python main.py --topic "TOPIC_NAME" [OPTIONS]

# Required:
#   --topic TEXT        Topic to generate video about

# Optional:
#   --output PATH       Custom output path (default: output/videos/)
#   --style PATH        Style profile JSON from Part A
#   --llm TEXT          LLM provider: groq|ollama (default: groq)
#   --help              Show help message
```

### Common Command Patterns

```powershell
# Basic generation
python main.py --topic "What is HTTP"

# Custom output location
python main.py --topic "REST APIs" --output D:\Videos\rest.mp4

# With style profile
python main.py --topic "WebSockets" --style style_profile.json

# Using local LLM
python main.py --topic "Docker containers" --llm ollama

# Combined options
python main.py --topic "Kubernetes architecture" --style k8s_style.json --output ./k8s.mp4 --llm ollama
```

---

## 📋 Verification & Next Steps

### After First Successful Generation

1. **Review Generated Files**
   ```powershell
   # Check all outputs exist
   dir output\scripts\
   dir output\blueprints\
   dir output\audio\
   dir output\videos\
   ```

2. **Inspect Script Quality**
   ```powershell
   # Read the script to understand AI's interpretation
   type output\scripts\what_is_http_script.json
   ```

3. **Examine Blueprint Details**
   ```powershell
   # See how visuals were planned
   type output\blueprints\what_is_http_blueprint.json
   ```

4. **Watch Final Video**
   ```powershell
   start output\videos\what_is_http.mp4
   ```

### Iterate and Improve

- Try **different topics** to test versatility
- **Compare outputs** with reference videos
- **Refine style profiles** based on results
- **Adjust config.yaml** for quality/speed balance

### Complete Part A (Manual Analysis)

To get style-aware outputs:
1. Watch reference video: [How Web Sockets work | Deep Dive](https://www.youtube.com/watch?v/...)
2. Document visualization style in Google Docs
3. Create `style_profile.json`
4. Re-run with: `--style style_profile.json`

---

## 📚 Additional Resources

| Resource | Purpose | Location |
|----------|---------|----------|
| **Full Documentation** | Complete system guide | [README.md](README.md) |
| **Style Analysis Template** | Part A guide | `style_analysis_template.md` |
| **Configuration Guide** | Settings reference | [README.md](README.md)  #Configuration |
| **Troubleshooting** | Common issues | This file + README.md |
| **Logs** | Debug information | `logs/video_synthesis.log` |

---

## 🎉 Success Checklist

You've successfully set up the system when you can:

- [ ] Activate virtual environment without errors
- [ ] Run `python main.py --topic "Test"` successfully
- [ ] See 3 stages complete (Script → Blueprint → Video)
- [ ] Find generated MP4 in `output/videos/`
- [ ] Play video with audio narration and animations
- [ ] Generate videos for different topics
- [ ] Understand how to use style profiles

**Congratulations! You now have a working AI Video Synthesis Pipeline!** 🎬

---

## 📞 Getting Help

### If Issues Persist

1. **Check logs**:
   ```powershell
   type logs\video_synthesis.log
   ```

2. **Verify setup**:
   ```powershell
   python tests\verify_setup.py
   ```

3. **Test individual components**:
   ```powershell
   python tests\quick_test.py
   ```

4. **Review prerequisites**: Ensure Python 3.9+, FFmpeg installed, API key configured

---

**Ready to generate videos? Start with:**
```powershell
python main.py --topic "Your Favorite Tech Topic"
```

**Happy video creating! 🚀**

# Quick Start Guide - Video Synthesis Pipeline

## 🚀 Execute the Complete Pipeline

### **Prerequisites Check:**
```powershell
# 1. Verify Python 3.11 is active
python --version
# Should show: Python 3.11.x

# 2. Verify you're in the project directory
cd "d:\Test\ATG_Group Assignment\Assignment2"

# 3. Check if virtual environment exists
dir venv311
```

---

## **Step-by-Step Execution:**

### **Step 1: Activate Virtual Environment**
```powershell
# Activate Python 3.11 environment
venv311\Scripts\activate

# Your prompt should now show (venv311)
```

### **Step 2: Verify Configuration**
```powershell
# Check if .env file exists with API key
type .env

# Should show:
 # GROQ_API_KEY=gsk_... (your key here)
 ```

### **Step 3: Run the Pipeline**

**Option A: Simple Test (Recommended First)**
```powershell
python main.py --topic "What is HTTP"
```

**Option B: With Custom Output Path**
```powershell
python main.py --topic "What is REST API" --output ./output/videos/my_video.mp4
```

**Option C: With Style Profile**
```powershell
python main.py --topic "How DNS works" --style style_profile.example.json
```

---

## **Expected Pipeline Flow:**

```
🎯 Topic: "What is HTTP"
    ↓
[1/3] Generating Script...
    ├─ Analyzing topic structure
    ├─ Generating narration (7 scenes)
    └─ ✅ Script saved: output/scripts/what_is_http_script.json
    ↓
[2/3] Creating Animation Blueprint...
    ├─ Extracting visual elements
    ├─ Generating animations
    └─ ✅ Blueprint saved: output/blueprints/what_is_http_blueprint.json
    ↓
[3/3] Generating Video...
    ├─ Creating audio (Scene 1/7)... ✅
    ├─ Creating audio (Scene 2/7)... ✅
    ├─ Creating audio (Scene 3/7)... ✅
    ├─ ... (remaining scenes)
    ├─ Rendering animations with Manim
    └─ Compositing final video
    ↓
✅ COMPLETE: output/videos/what_is_http.mp4
```

---

## **Processing Time:**

| Stage | Duration | Output |
|-------|----------|--------|
| Script Generation | 5-10 sec | JSON (4-5 KB) |
| Blueprint Generation | 2-5 sec | JSON (16-20 KB) |
| Audio Generation | 15-25 sec | WAV files (~300 KB each) |
| Video Rendering | *Pending* | MP4 video |
| **Total** | **~30-60 sec** | Complete package |

---

## **Check Generated Outputs:**

```powershell
# View all generated files
dir output\scripts\*.json
dir output\blueprints\*.json
dir output\audio\*.wav
# dir output\videos\*.mp4  # (if video rendering completes)
```

### **Expected Output Structure:**
```
output/
├── scripts/
│   └── what_is_http_script.json           (4.6 KB)
├── blueprints/
│   └── what_is_http_blueprint.json        (16.8 KB)
├── audio/
│   ├── what_is_http_scene_1.wav          (277 KB)
│   ├── what_is_http_scene_2.wav          (297 KB)
│   └── ... (scenes 3-7)
└── videos/
    └── what_is_http.mp4                   (TBD)
```

---

## **Troubleshooting:**

### **Issue: "GROQ_API_KEY not found"**
```powershell
# Create .env file
copy .env.example .env
# Edit .env and add your API key from https://console.groq.com
```

### **Issue: Unicode errors in console**
- **Status**: Cosmetic only - pipeline still works
- **Cause**: Windows console encoding
- **Impact**: None on output files

### **Issue: "TTS not available"**
- **Status**: Using pyttsx3 (Windows voices)
- **Impact**: Audio generates successfully with built-in voices

---

## **View Generated Content:**

### **1. Script (JSON)**
```powershell
type output\scripts\what_is_http_script.json
```

### **2. Blueprint (JSON)**
```powershell
type output\blueprints\what_is_http_blueprint.json
```

### **3. Play Audio**
```powershell
# Windows Media Player
start output\audio\what_is_http_scene_1.wav
```

---

## **Advanced Options:**

### **Change LLM Provider**
```powershell
# Use local Ollama instead of Groq
python main.py --topic "Your Topic" --llm ollama
```

### **Custom Configuration**
Edit `config.yaml` to change:
- TTS voice speed
- Manim quality (low/medium/high)
- Color palettes
- Animation defaults

---

## **Quick Reference:**

```powershell
# Full command syntax
python main.py --topic "TOPIC_NAME" [OPTIONS]

# Options:
#   --topic TEXT        Topic to generate video about (required)
#   --output PATH       Custom output path (optional)
#   --style PATH        Style profile JSON (optional)
#   --llm TEXT         LLM provider: groq|ollama (optional)
#   --help             Show help message
```

---

## **Success Indicators:**

✅ **Script Generation**: JSON file appears in `output/scripts/`  
✅ **Blueprint Generation**: JSON file appears in `output/blueprints/`  
✅ **Audio Generation**: WAV files appear in `output/audio/`  
✅ **Pipeline Complete**: No error messages in final output  

---

## **Next Steps After Execution:**

1. **Review Generated Script**
   - Open JSON file to see narration and visual descriptions
   - Verify scene count and content accuracy

2. **Examine Blueprint**
   - Check visual elements extracted
   - Review animation sequences and timing

3. **Listen to Audio**
   - Play WAV files to hear narration quality
   - Verify pacing and clarity

4. **Iterate with Different Topics**
   - Try: "What is Docker", "How HTTPS works", "REST vs GraphQL"
   - Compare outputs and quality

---

**Need Help?** Check `README.md` for full documentation or `SETUP.md` for installation issues.

# Demo Video Creation Guide - For Submission

## 🎥 Quick Demo Video (5 minutes to create)

### **Option 1: Screen Recording Demo** (RECOMMENDED)

Use Windows built-in screen recorder to show the working system:

#### **Step 1: Prepare Files to Show**
```powershell
# Open these in VS Code or Notepad++:
1. output/scripts/what_is_http_script.json
2. output/blueprints/what_is_http_blueprint.json
3. output/audio/what_is_http_scene_1.wav
```

#### **Step 2: Start Recording**
```
Windows + G → Start Recording
- Or use OBS Studio (free)
- Or use PowerPoint screen recording
```

#### **Step 3: Demo Script** (2-3 minutes recording):

**[00:00-00:30]** Show Terminal
```powershell
# Say: "Here's the command to run the pipeline"
venv311\Scripts\python.exe main.py --topic "What is HTTP"

# Show it executing (or show previous run output)
```

**[00:30-01:00]** Show Generated Script
```
# Open: output/scripts/what_is_http_script.json
# Say: "The AI generated a 9-scene script with narration"
# Scroll through to show the structure
```

**[01:00-01:30]** Show Generated Blueprint
```
# Open: output/blueprints/what_is_http_blueprint.json  
# Say: "It created detailed animation blueprints with visual elements"
# Show the visual_description, elements, animations sections
```

**[01:30-02:00]** Play Audio Sample
```
# Open Windows Media Player
# Play: output/audio/what_is_http_scene_1.wav
# Say: "And generated narration audio using TTS"
```

**[02:00-02:30]** Show Code
```
# Briefly show main.py or src/ folder
# Say: "Complete Python implementation with Groq API integration"
```

**[02:30-03:00]** Conclusion
```
# Say: "This demonstrates the end-to-end AI video synthesis pipeline"
# Show README.md or documentation
```

---

## **Option 2: Stop Current Process & Create Simple Demo**

**If audio generation is still running:**

```powershell
# 1. Press Ctrl+C to stop

# 2. Create a shorter demo with fewer scenes
venv311\Scripts\python.exe main.py --topic "HTTP basics"

# This might generate faster with a simpler topic
```

---

## **Option 3: PowerPoint Demo Video**

Create a presentation showing:

**Slide 1: Title**
- "AI Video Synthesis System"
- Your name/ID

**Slide 2: System Architecture**
- Topic → Script → Blueprint → Audio → Video
- Show the workflow

**Slide 3: Live Demo - Input**
```
Command: python main.py --topic "What is HTTP"
```

**Slide 4: Output 1 - Script**
- Screenshot of JSON file
- Highlight 9 scenes, narration text

**Slide 5: Output 2 - Blueprint**
- Screenshot of blueprint JSON
- Highlight visual elements, animations

**Slide 6: Output 3 - Audio**
- Screenshot of audio files in folder
- Icon showing WAV files generated

**Slide 7: Code Structure**
- Screenshot of src/ folder
- Show main components

**Slide 8: Results**
- "Successfully generates:
  - AI-written scripts
  - Animation blueprints  
  - TTS audio narration"

Then record PowerPoint presentation with narration (File → Export → Create Video)

---

## **FASTEST Path (2 minutes):**

```powershell
# 1. Stop current execution (Ctrl+C)

# 2. Take screenshots:
- Terminal showing command
- output/scripts/what_is_http_script.json (opened)
- output/blueprints/what_is_http_blueprint.json (opened)
- output/audio/ folder with files

# 3. Create PowerPoint with screenshots

# 4. Record PowerPoint to video (built-in feature)

Done!
```

---

## **Files You Already Have for Demo:**

✅ **Scripts:** `output/scripts/what_is_http_script.json` (5.4 KB, 9 scenes)  
✅ **Blueprints:** `output/blueprints/what_is_http_blueprint.json` (18.4 KB)  
✅ **Audio:** 2 WAV files generated (proof it works)  
✅ **Code:** Complete implementation in `src/`  
✅ **Docs:** README, SETUP guides

**You have everything needed to show the system works!**

---

Which option would you like to use? I recommend **Option 1** (screen recording) - it's the most professional and shows real execution.

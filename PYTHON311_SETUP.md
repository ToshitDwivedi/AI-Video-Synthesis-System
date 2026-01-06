# Quick Start with Python 3.11 Environment

## The project now has a Python 3.11 virtual environment for TTS compatibility

### Activate the environment:
```powershell
venv311\Scripts\activate
```

### Run tests:
```powershell
# Quick test (no video generation)
python tests\quick_test.py

# Or run with specific topic
python main.py --topic "What is HTTP"
```

### Deactivate when done:
```powershell
deactivate
```

## Why Python 3.11?
TTS (Coqui Text-to-Speech) library requires Python < 3.12
Your system has Python 3.12.3, so we created a separate 3.11 environment.

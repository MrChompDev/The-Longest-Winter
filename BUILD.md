# Building The Longest Winter

## 🚀 Quick Start (3 Steps)

### Step 1: Install Requirements
Open PowerShell or Command Prompt in the project folder and run:
```bash
pip install pygame pyinstaller
```

Or install from requirements.txt:
```bash
pip install -r requirements.txt
```

### Step 2: Add Your Audio (Optional)
Place these files in `assets/audio/`:
- `Mainost.mp3` (background music)
- `Bell tolls.mp3` (bell sound effects)
- `Success.mp3`
- `Fail.mp3`  
- `Warning.mp3`
- `Footstep sounds.mp3`

The game works without audio but will be silent.

### Step 3: Build!
```bash
python build.py
```

That's it! Your .exe will be in the `dist/` folder.

---

## 📋 Detailed Instructions

### First Time Setup

1. **Make sure Python is installed**
   ```bash
   python --version
   ```
   Should show Python 3.7 or higher.

2. **Install required packages**
   ```bash
   pip install pygame pyinstaller
   ```

   If you get "pip not recognized", try:
   ```bash
   python -m pip install pygame pyinstaller
   ```

3. **Navigate to project folder**
   ```bash
   cd path\to\project
   ```

### Building the Game

**Option A: Automated Build (Recommended)**
```bash
python build.py
```
This script will:
- ✅ Check if requirements are installed
- ✅ Install missing packages automatically
- ✅ Check for audio files
- ✅ Build the .exe
- ✅ Show you where to find it

**Option B: Manual Build**
```bash
python -m PyInstaller the_longest_winter.spec
```

### After Building

Your game will be in: `dist/The_Longest_Winter.exe`

The `dist/` folder contains:
```
dist/
├── The_Longest_Winter.exe    ← Main executable
├── assets/
│   └── audio/                 ← Your audio files
└── [other files]              ← Required libraries
```

### Testing Your Build

1. Open `dist/` folder
2. Double-click `The_Longest_Winter.exe`
3. Game should launch!

---

## 🎵 About Audio Files

The .exe file will include whatever audio files are in `assets/audio/` when you build.

**If building without audio:**
- Game works fine, just silent
- You can add audio files later directly to `dist/assets/audio/`

**If building with audio:**
- Put your .mp3 files in `assets/audio/` BEFORE running build.py
- They'll be packaged into the .exe automatically

---

## 📤 Distributing Your Game

To share with others:

1. **Zip the dist folder:**
   - Right-click `dist/` folder
   - Send to → Compressed (zipped) folder

2. **Share the zip:**
   - Upload to Google Drive, Dropbox, itch.io, etc.

3. **Players just need to:**
   - Extract the zip
   - Run `The_Longest_Winter.exe`
   - No Python installation needed!

---

## ❓ Troubleshooting

### "pip is not recognized"
```bash
python -m pip install pygame pyinstaller
```

### "pyinstaller is not recognized"  
PyInstaller isn't in your PATH. Use:
```bash
python -m PyInstaller the_longest_winter.spec
```

Or just use the build script:
```bash
python build.py
```

### "No module named pygame"
```bash
pip install pygame
```

### "Permission denied" or "Access denied"
- Run Command Prompt/PowerShell as Administrator
- Or install packages for your user:
  ```bash
  pip install --user pygame pyinstaller
  ```

### Build works but .exe won't run
- Make sure you're running from the `dist/` folder
- All files in `dist/` must stay together
- Check Windows Defender isn't blocking it

### Audio not playing
- Check `dist/assets/audio/` has your .mp3 files
- Files must be named exactly:
  - Mainost.mp3
  - Success.mp3
  - Fail.mp3
  - Warning.mp3

---

## 📊 File Sizes

- **With audio**: ~60-80 MB
- **Without audio**: ~50-60 MB

The .exe includes:
- Python runtime
- Pygame library  
- All game code
- All assets

---

## 🔧 Advanced: Manual PyInstaller

If you want to customize the build:

```bash
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "The_Longest_Winter" ^
    --add-data "assets;assets" ^
    main.py
```

But the .spec file already has all the settings configured!

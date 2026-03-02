#!/usr/bin/env python3
"""
Build script for The Longest Winter
Creates a standalone executable
"""
import os
import sys
import shutil
import subprocess

def check_python():
    """Verify Python version"""
    if sys.version_info < (3, 7):
        print("✗ Python 3.7 or higher required")
        print(f"  Current version: {sys.version}")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} found")

def install_requirements():
    """Install required packages"""
    packages = ['pygame', 'pyinstaller']
    
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package} already installed")
        except ImportError:
            print(f"✗ {package} not found. Installing...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✓ {package} installed successfully")
            except subprocess.CalledProcessError:
                print(f"✗ Failed to install {package}")
                print("  Try running: pip install pygame pyinstaller")
                sys.exit(1)

def clean_build():
    """Clean previous builds"""
    print("\nCleaning previous builds...")
    for folder in ['build', 'dist', '__pycache__']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"  Removed {folder}/")
    
    # Clean .pyc files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))

def check_audio_files():
    """Check if audio files exist"""
    audio_dir = os.path.join('assets', 'audio')
    required_files = ['Mainost.mp3', 'Bell tolls.mp3', 'Success.mp3', 'Fail.mp3', 'Warning.mp3']
    
    print("\nChecking audio files...")
    all_exist = True
    for audio_file in required_files:
        path = os.path.join(audio_dir, audio_file)
        if os.path.exists(path) and os.path.getsize(path) > 0:
            print(f"  ✓ {audio_file}")
        else:
            print(f"  ✗ {audio_file} (missing or empty)")
            all_exist = False
    
    if not all_exist:
        print("\n⚠ WARNING: Some audio files are missing!")
        print("  The game will work but will be silent.")
        print("  Add your .mp3 files to assets/audio/ before building.")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)

def build_exe():
    """Build the executable"""
    print("\n" + "=" * 60)
    print("Building The Longest Winter...")
    print("=" * 60)
    
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",
        "the_longest_winter.spec"
    ]
    
    print(f"\nRunning: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    return result.returncode == 0

def main():
    print("=" * 60)
    print("THE LONGEST WINTER - Build Script")
    print("=" * 60)
    print()
    
    # Check Python version
    check_python()
    
    # Install requirements
    print("\nChecking requirements...")
    install_requirements()
    
    # Check audio files
    check_audio_files()
    
    # Clean previous builds
    clean_build()
    
    # Build
    if build_exe():
        print("\n" + "=" * 60)
        print("✓ BUILD SUCCESSFUL!")
        print("=" * 60)
        print("\n📦 Your game is ready!")
        print(f"\n📂 Location: {os.path.abspath('dist')}")
        print("\n🎮 Files created:")
        print("   - The_Longest_Winter.exe (main executable)")
        print("   - assets/ folder (with your audio files)")
        print("\n🚀 To distribute:")
        print("   1. Zip the entire 'dist' folder")
        print("   2. Share the zip file")
        print("   3. Players extract and run The_Longest_Winter.exe")
        print("\n💡 Tip: Test the .exe by running it from the dist folder!")
        
    else:
        print("\n" + "=" * 60)
        print("✗ BUILD FAILED")
        print("=" * 60)
        print("\n⚠ Troubleshooting:")
        print("   1. Make sure you're in the project folder")
        print("   2. Try: pip install --upgrade pyinstaller pygame")
        print("   3. Check for error messages above")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nBuild cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        print("\nPlease report this error with the message above.")
        sys.exit(1)

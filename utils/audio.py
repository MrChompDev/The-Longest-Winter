"""
Audio management system
"""
import pygame
import os
from settings import ENABLE_SOUND, AUDIO_PATH, SOUND_FILES


class AudioManager:
    """Manages all game audio"""
    
    def __init__(self):
        self.enabled = ENABLE_SOUND
        self.sounds = {}
        self.music_playing = False
        
        if self.enabled:
            try:
                pygame.mixer.init()
                self._load_sounds()
            except:
                print("Audio system failed to initialize")
                self.enabled = False
    
    def _load_sounds(self):
        """Load all sound files"""
        for sound_name, filename in SOUND_FILES.items():
            filepath = os.path.join(AUDIO_PATH, filename)
            try:
                if os.path.exists(filepath):
                    self.sounds[sound_name] = pygame.mixer.Sound(filepath)
                else:
                    print(f"Sound file not found: {filepath}")
            except Exception as e:
                print(f"Failed to load {sound_name}: {e}")
    
    def play_sound(self, sound_name, volume=1.0):
        """Play a sound effect"""
        if self.enabled and sound_name in self.sounds:
            try:
                self.sounds[sound_name].set_volume(volume)
                self.sounds[sound_name].play()
            except:
                pass
    
    def play_music(self, music_name, loops=-1, volume=0.3):
        """Play background music"""
        if self.enabled and music_name in SOUND_FILES:
            filepath = os.path.join(AUDIO_PATH, SOUND_FILES[music_name])
            try:
                if os.path.exists(filepath):
                    pygame.mixer.music.load(filepath)
                    pygame.mixer.music.set_volume(volume)
                    pygame.mixer.music.play(loops)
                    self.music_playing = True
            except:
                pass
    
    def stop_music(self):
        """Stop background music"""
        if self.enabled:
            try:
                pygame.mixer.music.stop()
                self.music_playing = False
            except:
                pass
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        if self.enabled:
            try:
                pygame.mixer.music.set_volume(volume)
            except:
                pass


# Global audio manager instance
audio_manager = AudioManager()

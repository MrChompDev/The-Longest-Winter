# THE LONGEST WINTER - Settings & Constants

# Display
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60
TILE_SIZE = 48

# Colors
COLOR_BG = (15, 20, 35)
COLOR_SNOW = (240, 245, 255)
COLOR_SNOW_DARK = (180, 190, 200)
COLOR_UI_BG = (25, 30, 45)
COLOR_UI_TEXT = (220, 225, 235)
COLOR_ALERT = (220, 80, 60)
COLOR_WARNING = (230, 180, 60)
COLOR_SAFE = (80, 200, 120)
COLOR_PATH = (100, 110, 130)

# Meter colors
COLOR_HEAT = (255, 100, 50)
COLOR_FOOD = (180, 140, 60)
COLOR_SANITY = (120, 100, 200)
COLOR_SAFETY = (100, 180, 160)

# Game timing
WIN_TIME = 600  # 10 minutes in seconds
TASK_SPAWN_MIN = 3.0
TASK_SPAWN_MAX = 8.0

# System drain rates (per second)
HEAT_DRAIN_RATE = 0.8
FOOD_DRAIN_RATE = 0.6
SANITY_DRAIN_RATE = 0.5
SAFETY_DRAIN_RATE = 0.7

# Escalation thresholds
ESCALATION_STAGE_2 = 0.4  # Below 40%
ESCALATION_STAGE_3 = 0.2  # Below 20%

# Mini-game settings
MINIGAME_SUCCESS_THRESHOLD = 0.8
FURNACE_DRIFT_SPEED = 0.2  # Slower base drift speed
SORTING_TIME_LIMIT = 15
BELL_SEQUENCE_LENGTH = 4
SIGNAL_MATCH_TIME = 12

# Audio settings
ENABLE_SOUND = True
AUDIO_PATH = 'assets/audio/'
SOUND_FILES = {
    'bell': 'Bell tolls.mp3',
    'fail': 'Fail.mp3',
    'footstep': 'Footstep sounds.mp3',
    'success': 'Success.mp3',
    'warning': 'Warning.mp3',
    'music': 'Mainost.mp3',
}

# Player
PLAYER_SPEED = 150
PLAYER_SIZE = 40
PLAYER_INTERACT_DISTANCE = 80  # Distance to interact with buildings

# Buildings (pixel positions for top-down view)
BUILDINGS = {
    'TOWN_HALL': {
        'pos': (640, 360),  # Center
        'name': 'Town Hall',
        'system': None,
        'size': (120, 100),
        'color': (100, 100, 120)
    },
    'WORKSHOP': {
        'pos': (300, 400),  # Left-bottom
        'name': 'Workshop',
        'system': 'HEAT',
        'size': (100, 80),
        'color': (140, 60, 40)
    },
    'FARM': {
        'pos': (980, 400),  # Right-bottom
        'name': 'Farm Storage',
        'system': 'FOOD',
        'size': (100, 80),
        'color': (120, 100, 50)
    },
    'CHURCH': {
        'pos': (780, 200),  # Right-top
        'name': 'Church',
        'system': 'SANITY',
        'size': (90, 110),
        'color': (80, 70, 100)
    },
    'WATCHTOWER': {
        'pos': (300, 180),  # Left-top
        'name': 'Watchtower',
        'system': 'SAFETY',
        'size': (70, 120),
        'color': (70, 90, 90)
    },
}


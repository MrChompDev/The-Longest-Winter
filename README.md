# THE LONGEST WINTER

A top-down thriller/management game where you play as the last mayor of a frozen mountain village, desperately trying to keep all systems running until dawn.

## 🎮 Game Concept

You are CONSTANTLY OVERWORKED - managing heat, food, sanity, and safety systems that all deteriorate simultaneously. Every action you take to fix one problem creates or escalates another. There are no upgrades, no help, and no breaks. Just survival.

## 📋 Requirements

- Python 3.7+
- Pygame

## 🔧 Installation

1. Install Python from https://www.python.org/

2. Install Pygame:
```bash
pip install pygame
```

3. **Add Audio Files (Optional)**:
   - Place the following .mp3 files in `project/assets/audio/`:
     - `Mainost.mp3` (background music - loops)
     - `Bell tolls.mp3` (bell sound effects)
     - `Fail.mp3`
     - `Footstep sounds.mp3`
     - `Success.mp3`
     - `Warning.mp3`
   - The game works without audio but is more atmospheric with it!

4. Run the game from the project directory:
```bash
cd project
python main.py
```

## 🕹️ How to Play

### Objective
Survive until dawn (10 minutes) without letting TWO systems collapse simultaneously.

### Controls
- **WASD or Arrow Keys** - Move your character around the village (top-down view)
- **E or SPACE** - Interact with buildings when nearby (work on systems)
- **Mini-game controls** - Vary by building (instructions shown in-game)

### Gameplay
Walk around the village using WASD controls, just like in Among Us! When you get near a building, you'll see a prompt to interact. Press E or SPACE to start the mini-game for that building's system.

### The Four Systems

1. **🔥 HEAT (Workshop)**
   - Mini-games: 
     - **Furnace Regulation**: Keep needle in green zone using A/D
     - **Pipe Repair**: Connect pipes from start to end
   - When low: Vision shrinks, movement slows

2. **🌾 FOOD (Farm Storage)**
   - Mini-games:
     - **Supply Sorting**: Drag crates to matching shelves
     - **Resource Count**: Count specific items quickly
   - When low: Stamina drain, slower actions

3. **🧠 SANITY (Church)**
   - Mini-games:
     - **Pattern Memory**: Simon Says style pattern matching
     - **Word Unscramble**: Unscramble winter-themed words
     - **Maze Escape**: Navigate through a maze with WASD
   - When low: UI distortion, false alerts

4. **👁 SAFETY (Watchtower)**
   - Mini-games:
     - **Signal Matching**: Match light patterns in time
     - **Reaction Test**: Click when the circle turns green
     - **Code Breaker**: Crack the symbol code (Mastermind style)
   - When low: Phantom tasks appear

### Buildings on Map (Top-Down View)
```
    [Watchtower]        [Church]
         
         
    [Workshop]    [Town Hall]    [Farm]
```

Walk between buildings using WASD. The village is shown from a top-down perspective similar to Among Us.

## 🎯 Strategy Tips

1. **Prioritize critical systems** - Red/yellow buildings need immediate attention
2. **Plan your routes** - Walking takes time you don't have
3. **Accept some failures** - You can't fix everything
4. **Watch for urgent tasks** - Red indicators mean imminent collapse
5. **Late game gets harder** - More tasks spawn, systems drain faster

## 📁 File Structure

```
project/
├── main.py              # Main game loop and scene management
├── settings.py          # Game constants and configuration
├── assets/              # Asset directories (for future expansion)
│   ├── tiles/
│   ├── ui/
│   └── audio/
├── systems/             # Game systems
│   ├── __init__.py
│   ├── meters.py        # Meter management
│   ├── tasks.py         # Task spawning and tracking
│   └── escalation.py    # Difficulty scaling
├── scenes/              # Game scenes
│   ├── __init__.py
│   ├── village.py       # Main gameplay scene
│   └── minigames.py     # Mini-game implementations
└── utils/               # Utility functions
    ├── __init__.py
    └── helpers.py       # Helper functions and classes
```

## 🎨 Features Implemented

- ✅ **Top-down view** like Among Us with WASD movement
- ✅ **Among Us-style player character** with capsule body and visor
- ✅ Modular architecture with proper package structure
- ✅ Complete village map with 5 distinct buildings
- ✅ **10 unique mini-games** with random variations:
  - 2 different mini-games for Heat system
  - 2 different mini-games for Food system
  - 3 different mini-games for Sanity system
  - 3 different mini-games for Safety system
- ✅ **Full audio system** with Mainost background music:
  - Success/fail sounds for all mini-games
  - Warning sounds for critical systems
  - Background music loops continuously
- ✅ Global meter system with synchronized decay
- ✅ Dynamic task spawning based on system health
- ✅ Escalation manager that adjusts difficulty
- ✅ Win/lose conditions
- ✅ Visual feedback (building colors change with system health)
- ✅ Atmospheric snow particle effects
- ✅ Proximity-based interaction system
- ✅ Pulsing task indicators
- ✅ Clean scene management

## 🎲 Game Jam Details

- **Theme**: Winter
- **Prerequisite**: CONSTANTLY OVERWORKED
- **Development Time**: 24-hour jam design
- **Engine**: Pygame
- **Genre**: Top-Down Thriller / Management / Folk Horror

## 🔄 Escalation Mechanics

As systems deteriorate:
- **Stage 1** (100-40%): Normal operation
- **Stage 2** (40-20%): Faster drain, harder mini-games
- **Stage 3** (<20%): Critical - environmental penalties kick in

The `EscalationManager` dynamically adjusts:
- Task spawn rates
- Maximum active tasks
- Mini-game difficulty
- Environmental effects

## 🏆 Winning

Survive until the timer reaches 0:00. The snow will slow and music will soften (in the full version with audio). You've made it through the longest winter.

## ☠️ Losing

If ANY two systems collapse (reach 0%) simultaneously, the game ends. The village systems are too interconnected - double failure is terminal.

## 🎵 Atmosphere

The game emphasizes atmosphere over horror:
- Heavy snow obscures the edges of your vision
- Constant wind ambiance (audio in full version)
- Isolated, desolate feeling
- No NPCs - just you and your responsibilities
- Unease through mechanics, not jump scares

## 🛠️ Customization

You can modify game difficulty in `settings.py`:
- `WIN_TIME` - Time to survive (default: 600 seconds)
- Drain rates for each system
- Mini-game difficulty parameters
- Task spawn rates
- Building positions

## 🔧 Extending the Game

The modular structure makes it easy to add:

**New Systems** (`systems/`):
- Add new meter types in `meters.py`
- Create new task types in `tasks.py`
- Adjust escalation logic in `escalation.py`

**New Mini-games** (`scenes/minigames.py`):
- Extend `MiniGame` base class
- Add to `create_minigame()` factory
- Configure in `settings.py`

**New Scenes** (`scenes/`):
- Create new scene classes
- Add scene management in `main.py`

**Assets** (`assets/`):
- Add sprites to `tiles/`
- Add UI elements to `ui/`
- Add sounds to `audio/`

## 📝 Design Philosophy

**"Choice, Not Mastery"** - The game is about deciding what fails, not what succeeds. You're always late, always choosing losses, always managing stress. CONSTANTLY OVERWORKED is not a modifier - it IS the game.

## 🐛 Known Limitations

This is a 24-hour jam MVP. Planned additions:
- Sound effects and ambient audio
- More visual effects (screen shake, distortion)
- Additional building interactions
- Save/load system
- Difficulty settings menu
- Achievements/statistics

## 📄 License

Created for game jam purposes. Feel free to modify and extend!

## 👤 Credits

Game Design Document provided by user
Implementation: Claude (Anthropic)

---

**Good luck, Mayor. Dawn is coming... if you can make it that long.**

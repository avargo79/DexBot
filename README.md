# DexBot - Modular Bot System

DexBot is a modular bot system for Ultima Online with RazorEnhanced, featuring a modern UI and robust state management.

## Directory Structure

```
DexBot/
├── __init__.py                     # Package initialization
├── DexBot.py                       # Main DexBot application
├── test_dexbot.py                  # Unit tests for DexBot
├── DexBot_PRD.md                   # Product Requirements Document
├── DexBot_Rebuild_Summary.md       # Development summary
└── DexBot_tasks.md                 # Task tracking
```

## Features

### Auto Heal System
- **Unified Healing**: Single system managing both bandages and potions
- **Real-time Monitoring**: Live status tracking with color-coded resource levels
- **Independent Toggles**: Enable/disable bandage or potion healing separately
- **Usage Counters**: Track healing statistics over time
- **Configurable Thresholds**: Customizable health and resource warning levels

### Modern UI/UX
- **Main GUMP**: Compact, dialog-style interface with real-time status
- **Settings GUMP**: Dedicated configuration interface with detailed controls
- **Responsive Design**: Minimize/maximize functionality
- **Intuitive Navigation**: Clear buttons for switching between interfaces
- **Rate Limited**: Prevents accidental rapid-fire button clicks

### Robust State Management
- **GUMP State Tracking**: Maintains correct interface state across interactions
- **Error Recovery**: Graceful handling of disconnections and errors
- **Resource Monitoring**: Real-time tracking of bandages and potions
- **Performance Optimized**: Singleton patterns and efficient update cycles

## Configuration

Edit the `BotConfig` class in `DexBot.py` to customize:
- Health thresholds
- Resource warning levels
- Timer settings
- UI positioning
- System toggles

## Usage

Run the script from RazorEnhanced:
```python
exec(open('DexBot/DexBot.py').read())
```

Or directly execute the DexBot.py file from the RazorEnhanced Scripts interface.

## Development

See the included documentation files for detailed information:
- `DexBot_PRD.md` - Product requirements and specifications
- `DexBot_Rebuild_Summary.md` - Development history and decisions
- `DexBot_tasks.md` - Task tracking and progress

## Version

Current Version: 2.0
Author: DexBot Development Team
License: MIT

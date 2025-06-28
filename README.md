# DexBot - Modular Bot System

DexBot is a modular bot system for Ultima Online with RazorEnhanced, currently featuring an advanced Auto Heal system with a modern GUMP interface and robust state management. Built with scalability in mind for future combat, looting, and farming modules.

## Directory Structure

```
DexBot/
├── __init__.py                     # Package initialization
├── DexBot.py                       # Main DexBot application (Auto Heal system)
├── test_dexbot.py                  # Unit tests for DexBot
├── README.md                       # This file - project overview
├── .gitignore                      # Git ignore patterns for Python projects
└── docs/                           # Documentation directory
    ├── DexBot_PRD.md               # Product Requirements Document
    ├── DexBot_Rebuild_Summary.md   # Development summary and decisions
    └── DexBot_tasks.md             # Task tracking and development progress
```

## Features

### ✅ Auto Heal System (Implemented)
- **Intelligent Healing Logic**: Prioritizes heal potions for critical health (<50%), bandages for normal healing
- **Dual Resource Management**: Independent toggle controls for bandages and heal potions
- **Real-time Health Monitoring**: Continuous tracking with 95% healing threshold activation
- **Advanced Retry Mechanism**: 3-attempt system for bandage application with 500ms delays
- **Resource Warnings**: Low bandage alerts when supply drops below 10
- **Journal Integration**: Monitors healing completion messages for accurate cooldown tracking
- **Death Handling**: Automatic pause during death, resume on resurrection

### ✅ Modern GUMP Interface (Implemented)
- **Main Status GUMP**: Real-time health, resources, and runtime display
- **Auto Heal Settings GUMP**: Dedicated configuration interface with detailed controls
- **Dynamic UI Updates**: Interface refreshes only when data changes (performance optimized)
- **Multiple View States**: Full, minimized, and settings modes
- **Interactive Controls**: Toggle buttons with tooltips and visual feedback
- **Color-coded Status**: Green/yellow/red indicators for health and resource levels
- **Rate Limiting**: 500ms minimum between button presses prevents accidental spam

### ✅ Robust Architecture (Implemented)
- **Singleton Pattern**: Efficient configuration and status management
- **Modular Design**: Clean separation of concerns for easy maintenance
- **Type Safety**: Comprehensive type hints throughout codebase
- **Error Recovery**: Graceful handling of missing resources and connection issues
- **Performance Optimized**: Minimal object creation, conditional updates
- **Comprehensive Logging**: Debug, info, warning, and error levels with toggle control

### 🔄 Planned Future Modules
- **Combat System**: Auto-attack with enemy detection and targeting (placeholder exists)
- **Looting System**: Automated corpse processing and resource collection (placeholder exists)
- **Fishing System**: AFK fishing automation (placeholder exists)
- **Buff Management**: Automatic strength/agility potion maintenance
- **Weapon Management**: Auto re-equip on disarm detection
- **Inventory Management**: Smart item dropping when backpack full

## Quick Start

### 1. Installation
- Download or clone the DexBot directory to your RazorEnhanced Scripts folder
- Ensure all files are in the correct directory structure shown above

### 2. Usage
Run the script from RazorEnhanced using one of these methods:

**Method 1: Direct execution**
```python
exec(open('DexBot/DexBot.py').read())
```

**Method 2: RazorEnhanced Scripts interface**
- Open RazorEnhanced Scripts tab
- Navigate to DexBot folder
- Double-click `DexBot.py` to execute

### 3. Interface Controls
- **Enable/Disable Auto Heal**: Click the toggle button (left side of main GUMP)
- **Settings**: Click the gear icon to open detailed healing configuration
- **Minimize/Maximize**: Use window controls in upper-right corner
- **Close**: Click the X button to close interface (bot continues running)
- **Stop Bot**: Press ESC or Ctrl+C to stop the entire script

### 4. First-Time Setup
1. Start the script and open the GUMP interface
2. Verify bandages and heal potions are in your backpack
3. Adjust settings via the Settings GUMP if needed
4. Toggle Auto Heal ON and monitor the real-time status display

## Configuration

### Runtime Configuration (Recommended)
Use the GUMP interface for real-time configuration changes:
- **Auto Heal Toggle**: Enable/disable entire healing system
- **Bandage Healing**: Independent toggle for bandage-based healing
- **Potion Healing**: Independent toggle for heal potion usage
- **Debug Mode**: Toggle detailed logging output

### Advanced Configuration (Code Editing)
Edit the `BotConfig` class in `DexBot.py` to customize advanced settings:

**Health Thresholds:**
- `HEALING_THRESHOLD_PERCENTAGE = 95` - When to start healing (95% health)
- `CRITICAL_HEALTH_THRESHOLD = 50` - When to prioritize potions (50% health)
- `BANDAGE_THRESHOLD = 1` - Minimum HP loss to trigger bandage (1 HP)

**Resource Management:**
- `LOW_BANDAGE_WARNING = 10` - Warn when bandages below this amount
- `BANDAGE_RETRY_ATTEMPTS = 3` - Number of bandage application attempts
- `SEARCH_RANGE = 2` - Item search range in backpack

**Timing Settings:**
- `HEALING_TIMER_DURATION = 11000` - Bandage cooldown (11 seconds)
- `POTION_COOLDOWN_MS = 10000` - Heal potion cooldown (10 seconds)
- `DEFAULT_SCRIPT_DELAY = 250` - Main loop interval (250ms)

**UI Settings:**
- `GUMP_WIDTH/HEIGHT = 320/240` - Main GUMP dimensions
- `GUMP_X/Y = 100/100` - Default GUMP position

## Item Requirements

Ensure these items are in your backpack for the Auto Heal system:
- **Bandages** (Item ID: 0x0E21) - For normal healing
- **Heal Potions** (Item ID: 0x0F0C) - For critical health situations

## Troubleshooting

### Common Issues
1. **"No bandages found"** - Ensure bandages are in your main backpack
2. **"No heal resources"** - Check that healing methods aren't disabled in settings
3. **GUMP not updating** - Try closing and reopening the interface
4. **Script stops unexpectedly** - Check console for error messages

### Debug Mode
Enable debug mode via the GUMP interface for detailed logging:
- Shows health monitoring details
- Displays resource checking information
- Logs GUMP state changes
- Provides healing decision explanations

## Development

See the included documentation files for detailed information:
- `docs/DexBot_PRD.md` - Product requirements and specifications
- `docs/DexBot_Rebuild_Summary.md` - Development history and decisions
- `docs/DexBot_tasks.md` - Task tracking and progress

## Contributing

This project uses Git for version control. To contribute:
1. Make your changes to the appropriate files
2. Test thoroughly with RazorEnhanced
3. Update documentation as needed
4. Commit changes with descriptive messages

## Version

Current Version: 2.0
Author: RugRat79 (DexBot Development Team)
License: MIT

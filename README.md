# DexBot - Modular Bot System

DexBot is a modular bot system for Ultima Online with RazorEnhanced, currently featuring an advanced Auto Heal system with a modern GUMP interface and robust state management. Built with scalability in mind for future combat, looting, and farming modules.

## Recent Updates (v2.0.1)

**🎯 Integrated Auto Heal Controls**: All healing settings are now integrated directly into the main GUMP interface for improved user experience:
- ✅ **Streamlined Interface**: No separate settings window - all controls accessible from main GUMP
- ✅ **Two-Line Auto Heal Section**: Status line + toggle buttons for bandages and potions
- ✅ **Faster Access**: Toggle healing methods without opening additional windows
- ✅ **Same Functionality**: All previous features maintained in more accessible design

## Directory Structure

```
DexBot/
├── __init__.py                     # Package initialization
├── DexBot.py                       # Main DexBot application (Auto Heal system)
├── test_dexbot.py                  # Unit tests for DexBot and configuration system
├── README.md                       # This file - project overview
├── .gitignore                      # Git ignore patterns for Python projects
├── config/                         # Configuration directory
│   ├── main_config.json            # Main bot settings and system toggles
│   └── auto_heal_config.json       # Auto Heal system specific settings
└── docs/                           # Documentation directory
    ├── DexBot_PRD.md               # Product Requirements Document
    ├── DexBot_Rebuild_Summary.md   # Development summary and decisions
    └── DexBot_tasks.md             # Task tracking and development progress
```

## Features

### ✅ Configuration Management System (Implemented)
- **JSON-based Configuration**: Separate config files for main bot settings and Auto Heal system
- **Persistent Settings**: All GUMP toggles automatically save to configuration files
- **Runtime Reloading**: Configuration changes apply immediately without restart
- **Default Value Handling**: Automatic creation of config files with sensible defaults
- **Nested Setting Access**: Dot notation for easy access to configuration values
- **Merge Protection**: New config keys automatically added when updating versions

### ✅ Auto Heal System (Implemented)
- **Intelligent Healing Logic**: Prioritizes heal potions for critical health (<50%), bandages for normal healing
- **Dual Resource Management**: Independent toggle controls for bandages and heal potions
- **Real-time Health Monitoring**: Continuous tracking with 95% healing threshold activation
- **Advanced Retry Mechanism**: 3-attempt system for bandage application with 500ms delays
- **Resource Warnings**: Low bandage alerts when supply drops below 10
- **Journal Integration**: Monitors healing completion messages for accurate cooldown tracking
- **Death Handling**: Automatic pause during death, resume on resurrection

### ✅ Modern GUMP Interface (Implemented)
- **Main Status GUMP**: Real-time health, resources, and runtime display with integrated healing controls
- **Integrated Settings**: All healing toggles accessible directly from the main interface
- **Dynamic UI Updates**: Interface refreshes only when data changes (performance optimized)
- **Multiple View States**: Full and minimized modes
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
- **Enable/Disable Auto Heal**: Click the main toggle button (left side of Auto Heal section)
- **Toggle Bandage Healing**: Use the bandage toggle button in the Auto Heal section
- **Toggle Potion Healing**: Use the potion toggle button in the Auto Heal section
- **Minimize/Maximize**: Use window controls in upper-right corner
- **Close**: Click the X button to close interface (bot continues running)
- **Debug Mode**: Toggle the debug button (bottom left corner)
- **Stop Bot**: Press ESC or Ctrl+C to stop the entire script

### 4. First-Time Setup
1. Start the script and open the GUMP interface
2. Verify bandages and heal potions are in your backpack
3. Use the integrated toggle controls to configure healing methods as needed
4. Toggle Auto Heal ON and monitor the real-time status display

## Configuration

### ✅ JSON Configuration Files (New!)
DexBot now uses a modern configuration system with separate JSON files:

**Main Configuration (`config/main_config.json`):**
- System toggles for all bot modules (healing, combat, looting, etc.)
- Global settings (debug mode, timing, safety features)
- GUMP interface settings (size, position, update intervals)
- Logging preferences

**Auto Heal Configuration (`config/auto_heal_config.json`):**
- Healing method toggles (bandages, potions)
- Health thresholds and timing settings
- Item IDs and resource management
- Color coding thresholds for UI
- Journal message monitoring

### Runtime Configuration (Recommended)
Use the GUMP interface for real-time configuration changes:
- **Auto Heal Toggle**: Enable/disable entire healing system
- **Bandage Healing**: Independent toggle for bandage-based healing
- **Potion Healing**: Independent toggle for heal potion usage
- **Debug Mode**: Toggle detailed logging output
- **All settings automatically save** to JSON config files

### Advanced Configuration (Manual Editing)
You can manually edit the JSON files in the `config/` directory:

**Key Settings in `main_config.json`:**
```json
{
  "system_toggles": {
    "healing_system_enabled": true,
    "debug_mode": false
  },
  "global_settings": {
    "main_loop_delay_ms": 250,
    "target_wait_timeout_ms": 1000
  },
  "gump_interface": {
    "main_gump": {
      "width": 320,
      "height": 240,
      "x_position": 100,
      "y_position": 100
    }
  }
}
```

**Key Settings in `auto_heal_config.json`:**
```json
{
  "health_thresholds": {
    "healing_threshold_percentage": 95,
    "critical_health_threshold": 50,
    "bandage_threshold_hp": 1
  },
  "timing_settings": {
    "healing_timer_duration_ms": 11000,
    "potion_cooldown_ms": 10000
  },
  "resource_management": {
    "bandage_retry_attempts": 3,
    "low_bandage_warning": 10
  }
}
```

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

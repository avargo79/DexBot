# DexBot - Product Requirements Document (PRD)

**Version**: 2.1.0
**Last Updated**: June 28, 2025

## 1. Overview

### 1.1 Purpose
DexBot is a modular bot system for Ultima Online using RazorEnhanced. It is designed to be a scalable and maintainable bot with an initial focus on providing an advanced Auto Heal system. The long-term vision is to create a comprehensive bot that can handle a variety of automated tasks.

### 1.2 Target User
The target users are Ultima Online players who use the RazorEnhanced client and want to automate repetitive tasks such as healing, looting, and resource gathering. The system is aimed at players who want a reliable and easy-to-use bot that can be customized to their needs.

### 1.3 Core Objectives (Current Implementation)
- Provide intelligent, automated healing management using bandages and heal potions.
- Offer a real-time GUMP (Graphical User Menu Popup) interface for bot control and status monitoring.
- Allow for persistent configuration of healing thresholds and resource management.
- Gracefully handle player death and resurrection.
- Establish a modular architecture that allows for the easy addition of new systems in the future.

### 1.4 Future Objectives (Planned)
- Automate enemy detection and combat engagement.
- Implement corpse skinning and scavenging.
- Maintain character buffs and stamina.
- Automatically re-equip a weapon when disarmed.
- Smart inventory management to drop items when the backpack is full.
- AFK fishing automation.

## 2. Functional Requirements

### 2.1 Auto Heal System (Implemented)
- **FR-001: Intelligent Healing Logic**: Prioritizes heal potions for critical health (<50%) and uses bandages for normal healing.
- **FR-002: Dual Resource Management**: Allows independent toggling of bandages and heal potions.
- **FR-003: Real-time Health Monitoring**: Continuously tracks player health and activates healing at a 95% threshold.
- **FR-004: Advanced Retry Mechanism**: Implements a 3-attempt system for bandage application with 500ms delays.
- **FR-005: Resource Warnings**: Alerts the user when bandage supply drops below 10.
- **FR-006: Journal Integration**: Monitors healing completion messages for accurate cooldown tracking.
- **FR-007: Death Handling**: Automatically pauses the system upon death and resumes upon resurrection.

### 2.2 Modern GUMP Interface (Implemented)
- **FR-008: Main Status GUMP**: Displays real-time health, resources, and runtime statistics with integrated healing controls.
- **FR-009: Integrated Settings**: All healing toggles are accessible directly from the main interface, eliminating the need for a separate settings window.
- **FR-010: Dynamic UI Updates**: The interface refreshes only when data changes to optimize performance.
- **FR-011: Multiple View States**: Supports both full and minimized modes.
- **FR-012: Interactive Controls**: Provides toggle buttons with tooltips and visual feedback.
- **FR-013: Color-coded Status**: Uses green, yellow, and red indicators for health and resource levels.
- **FR-014: Rate Limiting**: A 500ms minimum delay between button presses prevents accidental spam.

### 2.3 Configuration Management System (Implemented)
- **FR-015: JSON-based Configuration**: Uses separate JSON files for main bot settings and the Auto Heal system.
- **FR-016: Persistent Settings**: All GUMP toggles are automatically saved to the configuration files.
- **FR-017: Runtime Reloading**: Configuration changes are applied immediately without requiring a script restart.
- **FR-018: Default Value Handling**: Automatically creates configuration files with sensible defaults if they are missing.
- **FR-019: Merge Protection**: New configuration keys are automatically added when updating versions, preserving user settings.

### 2.4 Robust Architecture (Implemented)
- **FR-020: Singleton Pattern**: Manages configuration and status efficiently.
- **FR-021: Modular Design**: A clean separation of concerns allows for easy maintenance and future expansion.
- **FR-022: Type Safety**: The codebase includes comprehensive type hints.
- **FR-023: Error Recovery**: Gracefully handles missing resources and connection issues.
- **FR-024: Performance Optimized**: Minimizes object creation and uses conditional updates to reduce overhead.
- **FR-025: Comprehensive Logging**: Provides debug, info, warning, and error logging levels with a toggle control.

## 3. Non-Functional Requirements

### 3.1 Performance
- The bot should have a minimal impact on client performance.
- The main loop should be efficient, with a target delay of 250ms.
- GUMP updates should be optimized to only occur when necessary.

### 3.2 Usability
- The GUMP interface should be intuitive and easy to use.
- Configuration should be straightforward, with most options accessible through the GUMP.
- The bot should provide clear feedback to the user about its status and actions.

### 3.3 Reliability
- The bot should run stably for extended periods without crashing.
- The healing logic should be robust and handle edge cases gracefully.
- The bot should recover from common in-game events, such as player death or disconnection.

## 4. System Design

### 4.1 Directory Structure
The project is organized into a modular structure to facilitate development and maintenance:
```
DexBot/
├── dist/                           # Bundled output for distribution
├── docs/                           # Documentation files
├── src/                            # Source code
│   ├── config/                     # Configuration management
│   ├── core/                       # Core bot functionality
│   ├── systems/                    # Individual bot systems (e.g., auto_heal)
│   ├── ui/                         # GUMP interface code
│   └── utils/                      # Utility functions
├── tests/                          # Test files
├── main.py                         # Main script entry point
├── tasks.py                        # Development tasks for invoke
└── README.md                       # Project overview
```

### 4.2 Core Components
- **`main.py`**: The entry point of the script.
- **`src/core/main_loop.py`**: The heart of the bot, responsible for orchestrating the different systems.
- **`src/systems/auto_heal.py`**: The implementation of the Auto Heal system.
- **`src/ui/gump_interface.py`**: Manages the GUMP interface.
- **`src/config/config_manager.py`**: Handles loading and saving of configuration files.

## 5. Out of Scope
The following features are not planned for the current version of DexBot:
- PvP (Player vs. Player) automation.
- Complex questing or dungeon crawling logic.
- Support for clients other than RazorEnhanced.

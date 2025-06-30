# DexBot - Product Requirements Document (PRD)

**Version**: 3.1.1
**Last Updated**: June 29, 2025

## 1. Overview

### 1.1 Purpose
DexBot is a modular bot system for Ultima Online using RazorEnhanced. It is designed to be a scalable and maintainable bot that provides advanced automation for healing, combat, and looting tasks. The system has evolved from an initial Auto Heal focus to a comprehensive bot that handles multiple automated systems with exceptional performance optimizations.

### 1.2 Target User
The target users are Ultima Online players who use the RazorEnhanced client and want to automate repetitive tasks such as healing, combat engagement, and intelligent looting. The system is aimed at players who want a reliable, high-performance bot that can be customized to their needs and provides real-time feedback and control.

### 1.3 Core Objectives (Current Implementation - v3.1.1)
- Provide intelligent, automated healing management using bandages and heal potions with advanced retry mechanisms.
- Offer a real-time GUMP (Graphical User Menu Popup) interface for bot control and status monitoring.
- Implement advanced combat system with enemy detection, targeting, and automated engagement.
- Provide intelligent looting system with configurable item filters and performance optimizations.
- Allow for persistent configuration of healing thresholds, combat settings, and loot preferences.
- Gracefully handle player death and resurrection with system state management.
- Deliver exceptional performance through API-level optimizations (ignore lists, caching, streamlined execution).
- Establish a modular architecture that supports easy addition and modification of systems.

### 1.4 Future Objectives (Planned)
- Implement corpse skinning and resource harvesting.
- Maintain character buffs and stamina management.
- Automatically re-equip weapons when disarmed.
- Smart inventory management to drop items when the backpack is full.
- Advanced skill training systems.

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

### 2.4 Combat System (Implemented)
- **FR-020: Intelligent Enemy Detection**: Automatically scans for and prioritizes hostile enemies within configured range.
- **FR-021: Smart Targeting System**: Selects optimal targets based on proximity, threat level, and engagement rules.
- **FR-022: Automated Combat Engagement**: Handles weapon attacks, special abilities, and combat timing.
- **FR-023: Combat State Management**: Tracks combat status and coordinates with healing system during fights.
- **FR-024: Configurable Combat Settings**: Allows customization of engagement range, target priorities, and combat behaviors.
- **FR-025: Death Recovery**: Automatically handles player death during combat and resumes operation after resurrection.

### 2.5 Looting System (Implemented)
- **FR-026: Intelligent Corpse Detection**: Efficiently scans for and identifies lootable corpses using optimized filtering.
- **FR-027: Configurable Item Filtering**: Supports always_take, never_take, and take_if_space item categories with ItemID-based matching.
- **FR-028: Performance Optimization**: Uses ignore lists and caching to prevent repeated processing of empty corpses.
- **FR-029: Smart Inventory Management**: Prioritizes valuable items and manages limited backpack space intelligently.
- **FR-030: Gold Collection**: Reliable gold detection and collection using proper ItemID matching.
- **FR-031: API-Level Optimization**: Leverages RazorEnhanced ignore list features for 90% reduction in corpse scan overhead.

### 2.6 Robust Architecture (Implemented)
- **FR-032: Singleton Pattern**: Manages configuration and status efficiently.
- **FR-033: Modular Design**: A clean separation of concerns allows for easy maintenance and future expansion.
- **FR-034: Type Safety**: The codebase includes comprehensive type hints.
- **FR-035: Error Recovery**: Gracefully handles missing resources and connection issues.
- **FR-036: Performance Optimized**: Minimizes object creation and uses conditional updates to reduce overhead.
- **FR-037: Comprehensive Logging**: Provides debug, info, warning, and error logging levels with a toggle control.

## 3. Non-Functional Requirements

### 3.1 Performance
- The bot should have minimal impact on client performance through optimized execution.
- The main loop should maintain efficient operation with a target delay of 250ms.
- GUMP updates should be optimized to only occur when data changes (dynamic refresh).
- Looting system should achieve 85-95% performance improvement through ignore list optimization.
- Combat system should maintain responsive targeting and engagement timing.
- Memory usage should remain stable over extended runtime periods through cache management.

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
The project is organized into a clean, modular structure optimized for maintainability and performance:
```
DexBot/
├── dist/                           # Bundled distribution files (DexBot.py - 198KB)
├── docs/                           # Essential documentation only
├── src/                            # Source code modules
│   ├── config/                     # Configuration management
│   ├── core/                       # Core bot functionality
│   ├── systems/                    # Individual bot systems (auto_heal, combat, looting)
│   ├── ui/                         # GUMP interface code
│   └── utils/                      # Utility functions
├── scripts/                        # Build and development scripts
├── tmp/                            # Temporary files and development docs
├── config/                         # User configuration files
├── pyproject.toml                  # Project configuration
└── README.md                       # Project overview
```

### 4.2 Core Components
- **`dist/DexBot.py`**: The bundled distribution file containing all systems.
- **`src/core/main_loop.py`**: The heart of the bot, orchestrating all systems with performance optimization.
- **`src/systems/auto_heal.py`**: Advanced healing system with retry mechanisms and resource management.
- **`src/systems/combat.py`**: Intelligent combat system with enemy detection and targeting.
- **`src/systems/looting.py`**: High-performance looting system with ignore list optimization.
- **`src/ui/gump_interface.py`**: Dynamic GUMP interface with real-time updates.
- **`src/config/config_manager.py`**: Centralized configuration management with persistent storage.

## 5. Out of Scope
The following features are not planned for the current version of DexBot:
- PvP (Player vs. Player) automation.
- Complex questing or dungeon crawling logic.
- Support for clients other than RazorEnhanced.

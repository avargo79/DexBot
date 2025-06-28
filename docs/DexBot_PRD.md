# DexBot - Product Requirements Document (PRD)

## 1. Overview

### 1.1 Purpose
DexBot is a modular bot system for Ultima Online using RazorEnhanced. Currently implements an advanced Auto Heal system as the first component, based on the proven Dexxor.py healing system. The bot is designed for scalability with plans to add combat, looting, and other automation modules.

### 1.2 Target User
Players who want automated healing assistance during gameplay, with potential expansion to full PvE farming automation for dexterity-based melee characters.

### 1.3 Core Objectives (Current Implementation)
- Provide intelligent healing management using bandages and heal potions
- Real-time GUMP interface for bot control and status monitoring
- Configurable healing thresholds and resource management
- Death/resurrection handling and recovery
- Modular architecture for future system additions

### 1.4 Future Objectives (Planned)
- Automate enemy detection and combat engagement
- Handle corpse skinning and scavenging
- Maintain character buffs and stamina
- Ensure weapon management (rearm when disarmed)

## 2. Functional Requirements

### 2.1 Auto Heal System (IMPLEMENTED)
**FR-001: Intelligent Healing Management**
- **Description**: Automatically manage player healing using bandages and heal potions
- **Behavior**: 
  - Monitor health continuously (95% threshold for healing activation)
  - Prioritize heal potions for critical health (<50%)
  - Use bandages for normal healing (when missing 1+ HP)
  - Support independent enable/disable of bandage and potion healing
  - Track healing cooldowns and prevent spam
- **Dependencies**: Player.Hits, Player.HitsMax, Items.FindByID(), Items.UseItemByID(), Target.Self()

**FR-002: Bandage Healing**
- **Description**: Use bandages for healing with intelligent retry mechanism
- **Behavior**:
  - Apply bandage when health threshold is met
  - 3 retry attempts with 500ms delay between attempts
  - Track bandage supply and warn when low (<10 bandages)
  - 11-second cooldown timer for bandage applications
  - Journal monitoring for healing completion messages
- **Dependencies**: Items.UseItemByID(BANDAGE_ID), Target.Self(), Timer.Create(), Journal.SearchByType()

**FR-003: Heal Potion Usage**
- **Description**: Use heal potions for critical health situations
- **Behavior**:
  - Activate when health drops below 50% (configurable)
  - 10-second cooldown for potion usage
  - Support for different potion types (currently regular heal potions)
  - Prioritized over bandages for critical situations
- **Dependencies**: Items.UseItemByID(HEAL_POTION_ID), Timer.Create()

### 2.2 GUMP Interface System (IMPLEMENTED)
**FR-004: Main Status GUMP**
- **Description**: Real-time status display and bot control interface
- **Behavior**:
  - Display current health, bandage count, runtime statistics
  - Toggle Auto Heal system on/off
  - Minimize/maximize interface
  - Real-time updates when data changes
  - Compact and full view modes
- **Dependencies**: Gumps.CreateGump(), Gumps.SendGump(), Gumps.GetGumpData()

**FR-005: Auto Heal Settings GUMP**
- **Description**: Detailed configuration interface for healing system
- **Behavior**:
  - Independent toggle for bandage and potion healing
  - Display resource counts and usage statistics
  - Show current configuration thresholds
  - Access via settings button in main GUMP
- **Dependencies**: Gumps.CreateGump(), Gumps.SendGump()

**FR-006: GUMP Response Handling**
- **Description**: Process user interactions with the interface
- **Behavior**:
  - Rate limiting to prevent rapid button presses (500ms minimum)
  - Real-time configuration updates without restart
  - State management for different GUMP views
  - Button press feedback and tooltips
- **Dependencies**: Gumps.GetGumpData(), time tracking

### 2.3 System Management (IMPLEMENTED)
**FR-007: Death/Resurrection Handling**
- **Description**: Detect player death and handle resurrection
- **Behavior**:
  - Pause all systems when player is ghost
  - Display waiting message during death
  - Resume operations upon resurrection
  - Clear journal messages after resurrection
- **Dependencies**: Player.IsGhost, Player.Visible

**FR-008: Resource Monitoring**
- **Description**: Track and display healing resource availability
- **Behavior**:
  - Monitor bandage and heal potion counts
  - Color-coded resource display (green/yellow/red thresholds)
  - Low resource warnings
  - Usage statistics tracking
- **Dependencies**: Items.FindByID(), color threshold calculations

### 2.4 Future Systems (PLANNED - NOT IMPLEMENTED)
**FR-009: Combat System**
- **Description**: Automatically attack enemies when player is in war mode
- **Status**: Placeholder in code, not implemented

**FR-010: Corpse Processing**
- **Description**: Automatically skin and scavenge corpses within range
- **Status**: Not implemented

**FR-011: Buff Management**
- **Description**: Maintain strength and agility buffs during combat
- **Status**: Not implemented

**FR-012: Weapon Management**
- **Description**: Handle weapon disarm situations
- **Status**: Not implemented

## 3. Technical Requirements

### 3.1 Architecture (IMPLEMENTED)
- **TR-001**: Modular design with singleton pattern for configuration management
- **TR-002**: Separation of concerns: Config, Messages, Status, Interface, and Core systems
- **TR-003**: Type hints and comprehensive documentation for maintainability
- **TR-004**: Centralized logging system with debug, info, error, and warning levels

### 3.2 Performance (IMPLEMENTED)
- **TR-005**: Main loop execution frequency: 250ms intervals
- **TR-006**: GUMP updates only when data changes (optimized UI performance)
- **TR-007**: Singleton pattern for configuration to minimize object creation
- **TR-008**: Response time: <500ms for critical actions (healing)

### 3.3 Error Handling (IMPLEMENTED)
- **TR-009**: Graceful handling of missing items (bandages, heal potions)
- **TR-010**: Retry mechanisms for critical operations (3 attempts for bandage application)
- **TR-011**: Timeout handling for targeting operations (1000ms)
- **TR-012**: Exception handling in main loop with error recovery delays
- **TR-013**: Connection loss detection and graceful shutdown

### 3.4 Configuration (IMPLEMENTED)
- **TR-014**: Runtime configuration updates via GUMP interface
- **TR-015**: Centralized configuration constants in BotConfig class
- **TR-016**: Individual enable/disable toggles for healing methods
- **TR-017**: Configurable thresholds and timing parameters

### 3.5 User Interface (IMPLEMENTED)
- **TR-018**: Real-time GUMP interface with status display
- **TR-019**: Rate limiting for button presses (500ms minimum)
- **TR-020**: Multiple GUMP states: full, minimized, settings
- **TR-021**: Color-coded resource displays with thresholds
- **TR-022**: Tooltips and user feedback for all interactive elements

## 4. Item ID Constants (Current Implementation)

### 4.1 Healing Items (IMPLEMENTED)
- **Bandages**: 0x0E21
- **Heal Potion**: 0x0F0C (Regular heal potion - orange/red)

### 4.2 Future Item IDs (PLANNED)
- **Lesser Heal Potion**: TBD
- **Greater Heal Potion**: TBD
- **Dagger**: 0x0F52 (for corpse processing)
- **Greater Strength Potion**: 0x0F09
- **Greater Agility Potion**: 0x0F08
- **Total Refresh Potion**: 0x0F0B

### 4.3 Weapons (FUTURE)
- Default weapon types to be defined in future combat system

## 5. Configuration Parameters (Current Implementation)

### 5.1 Auto Heal Settings (IMPLEMENTED)
- `HEALING_ENABLED`: True (master toggle for entire healing system)
- `BANDAGE_HEALING_ENABLED`: True (toggle for bandage healing)
- `POTION_HEALING_ENABLED`: True (toggle for potion healing)
- `HEALING_THRESHOLD_PERCENTAGE`: 95% (health percentage to start healing)
- `CRITICAL_HEALTH_THRESHOLD`: 50% (health percentage for potion priority)
- `BANDAGE_THRESHOLD`: 1 HP (minimum HP loss to trigger bandage)

### 5.2 Timing Settings (IMPLEMENTED)
- `HEALING_TIMER_DURATION`: 11000ms (bandage application cooldown)
- `POTION_COOLDOWN_MS`: 10000ms (heal potion cooldown)
- `DEFAULT_SCRIPT_DELAY`: 250ms (main loop interval)
- `TARGET_WAIT_TIMEOUT`: 1000ms (targeting operation timeout)
- `BANDAGE_RETRY_DELAY`: 500ms (delay between bandage retry attempts)

### 5.3 Resource Management (IMPLEMENTED)
- `BANDAGE_RETRY_ATTEMPTS`: 3 (number of bandage application attempts)
- `LOW_BANDAGE_WARNING`: 10 (warn when bandages below this amount)
- `SEARCH_RANGE`: 2 (item search range in backpack)
- `BANDAGE_CHECK_INTERVAL_CYCLES`: 120 cycles (~30 seconds)

### 5.4 GUMP Interface Settings (IMPLEMENTED)
- `GUMP_WIDTH`: 320 pixels
- `GUMP_HEIGHT`: 240 pixels
- `GUMP_MIN_WIDTH`: 100 pixels (minimized state)
- `GUMP_MIN_HEIGHT`: 30 pixels (minimized state)
- `GUMP_UPDATE_INTERVAL_CYCLES`: 8 cycles (~2 seconds)
- `GUMP_X/Y`: 100, 100 (default position)

### 5.5 Color Thresholds (IMPLEMENTED)
- `BANDAGE_HIGH_THRESHOLD`: 20 (green color when above)
- `BANDAGE_MEDIUM_THRESHOLD`: 10 (yellow color when above)
- `HEALTH_HIGH_THRESHOLD`: 75% (green color when above)
- `HEALTH_MEDIUM_THRESHOLD`: 50% (yellow color when above)

### 5.6 Future Settings (PLANNED)
- Combat range and targeting preferences
- Corpse processing range and timing
- Buff management intervals
- Stamina thresholds

## 6. Safety Requirements (Current Implementation)

### 6.1 Fail-safes (IMPLEMENTED)
- **SR-001**: Stop all healing actions if player is ghost/dead
- **SR-002**: Connection loss detection with graceful shutdown
- **SR-003**: Timeout mechanisms for all targeting operations (1000ms)
- **SR-004**: Rate limiting for user interactions (500ms minimum between button presses)
- **SR-005**: Retry limits to prevent infinite loops (3 attempts for bandages)

### 6.2 User Control (IMPLEMENTED)
- **SR-006**: Manual override via GUMP interface for all healing functions
- **SR-007**: Real-time enable/disable toggles for bandage and potion healing
- **SR-008**: Debug mode toggle for detailed logging
- **SR-009**: GUMP close/minimize options for interface management
- **SR-010**: Keyboard interrupt handling (Ctrl+C/ESC) for emergency stop

### 6.3 Resource Management (IMPLEMENTED)
- **SR-011**: Low resource warnings (bandages <10)
- **SR-012**: Resource availability checks before healing attempts
- **SR-013**: Graceful handling of missing healing items

### 6.4 Future Safety Features (PLANNED)
- Combat mode restrictions
- Health threshold emergency stops
- Inventory management safeguards

## 7. Dependencies (Current Implementation)

### 7.1 RazorEnhanced API Modules (USED)
- **Player** (health monitoring, equipment status, death detection)
- **Items** (inventory management, item usage, resource counting)
- **Target** (self-targeting for healing actions)
- **Timer** (cooldown management for healing actions)
- **Misc** (utility functions, pause operations)
- **Journal** (healing completion message monitoring)
- **Gumps** (user interface creation and management)

### 7.2 Python Modules (USED)
- **typing** (type hints for code clarity)
- **time** (timestamp management for rate limiting)
- **AutoComplete** (RazorEnhanced import dependency)

### 7.3 Future Dependencies (PLANNED)
- **Mobiles** (enemy detection and targeting)
- **Player.WarMode** (combat state detection)
- **Player.BuffsExist()** (buff monitoring)

### 7.4 External Files (CURRENT)
- **AutoComplete.py** (required RazorEnhanced import)
- **No external configuration files** (all config is internal)

## 8. Current Implementation Status

### 8.1 Completed Features ✅
- **Auto Heal System**: Fully functional with bandages and heal potions
- **GUMP Interface**: Real-time status display and configuration
- **Resource Management**: Monitoring, warnings, and usage tracking
- **Death Handling**: Automatic pause/resume on death/resurrection
- **Error Handling**: Comprehensive exception handling and recovery
- **Configuration Management**: Runtime toggles and centralized settings
- **Logging System**: Debug, info, warning, and error levels
- **Rate Limiting**: Protection against rapid user interactions

### 8.2 Architecture Highlights ✅
- **Singleton Pattern**: Efficient configuration and status management
- **Modular Design**: Separation of concerns for maintainability
- **Type Safety**: Comprehensive type hints throughout codebase
- **Performance Optimization**: GUMP updates only when data changes
- **User Experience**: Intuitive interface with tooltips and feedback

### 8.3 Future Enhancements (Planned - In Code Comments)
- **Combat System**: Auto-attack functionality (placeholder exists)
- **Looting System**: Automated corpse processing (placeholder exists)
- **Fishing System**: AFK fishing automation (placeholder exists)
- **Buff Management**: Strength/agility potion automation
- **Weapon Management**: Auto re-equip on disarm
- **Inventory Management**: Auto-drop items when full

## 9. Success Criteria

### 9.1 Current Implementation Goals ✅
- **Auto Heal Reliability**: 100% healing activation when health drops below 95%
- **Resource Management**: Accurate tracking and low-resource warnings
- **Interface Responsiveness**: Real-time GUMP updates within 2 seconds
- **Error Recovery**: Graceful handling of all missing resource scenarios
- **User Control**: Runtime configuration changes without script restart

### 9.2 Performance Metrics (Achieved)
- **Response Time**: <500ms for critical healing actions
- **Memory Efficiency**: Singleton pattern minimizes object creation
- **UI Performance**: GUMP updates only when data changes (optimized)
- **Reliability**: 3-attempt retry mechanism for bandage application
- **Safety**: Rate limiting prevents user interaction spam

### 9.3 Future Success Criteria (Planned)
- **Combat Integration**: Zero false-positive attacks outside war mode
- **Resource Efficiency**: Minimal waste of potions and bandages
- **Corpse Processing**: 100% processing rate within specified range
- **Buff Maintenance**: Automatic buff renewal during combat

## 10. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-06-27 | Assistant | Initial PRD creation based on user requirements |
| 2.0 | 2025-06-28 | RugRat79 | Complete rewrite based on actual implementation analysis - focused on Auto Heal system and GUMP interface |

## 11. Technical Implementation Details

### 11.1 Class Structure
- **BotConfig**: Singleton configuration management with all constants
- **BotMessages**: Centralized message constants for consistent logging
- **Logger**: Static logging methods with debug mode support
- **SystemStatus**: Singleton status tracking with runtime statistics
- **GumpInterface**: Static methods for GUMP creation and management
- **GumpInterface.GumpSection**: Reusable UI components for consistent design

### 11.2 Key Design Patterns
- **Singleton Pattern**: Used for configuration and status management
- **Factory Pattern**: GUMP creation with standardized sections
- **State Machine**: GUMP state management (closed, full, minimized, settings)
- **Observer Pattern**: Data change detection for optimized UI updates

### 11.3 Error Handling Strategy
- **Graceful Degradation**: Continue operation when non-critical resources missing
- **Retry Mechanisms**: 3 attempts for critical operations with delays
- **Timeout Protection**: All targeting operations have 1000ms timeout
- **Exception Isolation**: Main loop continues despite individual system errors

### 11.4 Performance Optimizations
- **Conditional Updates**: GUMP refreshes only when data actually changes
- **Singleton Instances**: Minimize object creation overhead
- **Efficient Resource Checking**: Cached values to reduce API calls
- **Rate Limiting**: Prevent excessive user interaction processing

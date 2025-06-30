# DexBot Combat System - Product Requirements Document (PRD)

**Version**: 1.4  
**Created**: June 29, 2025  
**Status**: ✅ **IMPLEMENTED** - Production Ready  
**Last Updated**: June 29, 2025  

## 1. Overview

### 1.1 Purpose
The Combat System is a core automated module for DexBot that provides intelligent enemy detection, targeting, and combat engagement. It operates exclusively when the player is in War Mode, ensuring user control over when combat automation is active.

### 1.2 Business Value
- **PvE Automation**: Streamlines monster hunting and farming activities
- **Safety-First Design**: Only activates in War Mode, preventing accidental combat
- **Strategic Targeting**: Intelligent enemy prioritization and engagement logic
- **Performance Optimized**: Mobile data caching and efficient target scanning

### 1.3 Integration Context
- **Primary Integration**: Auto Heal System (health management during combat)
- **Secondary Integration**: Looting System (post-combat resource collection)
- **Supporting Systems**: Configuration Management, GUMP Interface
- **War Mode Dependency**: System only activates when `Player.WarMode` is `True`

## 2. Functional Requirements

### 2.1 Core Combat Logic (FR-C001 to FR-C010)

#### FR-C001: War Mode Activation Control
- **Requirement**: Combat system only operates when player is in War Mode
- **Rationale**: Prevents accidental combat and gives player explicit control
- **Implementation**: Check `Player.WarMode` before any combat operations
- **Safety**: System disengages immediately if player exits War Mode

#### FR-C002: Enemy Detection and Filtering
- **Requirement**: Automatically detect hostile targets within configurable range
- **Target Types**: Monsters, hostile players, aggressive NPCs
- **Filtering**: Exclude innocents (blue), friends (green), pets, invulnerable entities
- **Configurability**: `allow_target_blues` option for advanced users
- **Range**: Default 10 tiles, user configurable

#### FR-C003: Target Prioritization System
- **Requirement**: Intelligent target selection based on multiple criteria
- **Priority Modes**:
  - `closest`: Nearest target first (default)
  - `lowest_health`: Weakest target first
  - `highest_threat`: Combination of proximity and health
- **Smart Engagement**: Maintain current target unless significantly better option available
- **Switch Threshold**: Only change targets if new target is 3+ tiles closer

#### FR-C004: Automated Attack System
- **Requirement**: Execute attacks using equipped weapon when auto-attack enabled
- **Attack Timing**: Configurable delay between attacks (default 250ms)
- **Weapon Agnostic**: Works with any equipped weapon type
- **Manual Override**: Player can disable auto-attack while keeping auto-targeting

#### FR-C005: Target Health Monitoring
- **Requirement**: Track target health and status in real-time
- **Health Bar Integration**: Open health bars for accurate health data
- **Death Detection**: Automatically disengage when target dies
- **Status Display**: Show target name and health percentage overhead (optional)

### 2.2 Safety and Control Features (FR-C006 to FR-C010)

#### FR-C006: Health-Based Retreat System
- **Requirement**: Automatically retreat when player health drops below threshold
- **Default Threshold**: 30% health
- **Configurable**: User can adjust retreat threshold or disable feature
- **Integration**: Works with Auto Heal system for coordinated health management

#### FR-C007: Combat Timeout Protection
- **Requirement**: Disengage from combat after specified time limit
- **Default Timeout**: 30 seconds per target
- **Purpose**: Prevent getting stuck on invulnerable or bugged targets
- **Configurability**: User can adjust timeout duration

#### FR-C008: Range Management
- **Requirement**: Disengage if target moves too far away
- **Range Buffer**: 150% of max targeting range
- **Purpose**: Prevent chasing targets indefinitely
- **Melee/Ranged**: System adapts to weapon type and range

#### FR-C009: Player Safety Features
- **Requirement**: Built-in protections against accidental PvP
- **Blue Protection**: Default exclusion of innocent players/NPCs
- **Pet Protection**: Automatic exclusion of player pets
- **Guild Protection**: Avoid targeting guild members (future enhancement)

#### FR-C010: Emergency Disengagement
- **Requirement**: Immediate combat stop under emergency conditions
- **Triggers**: Player death, disconnection, critical errors
- **Clean Exit**: Proper cleanup of combat state and targeting
- **Error Recovery**: Graceful handling of API failures

## 3. Technical Specifications

### 3.1 Performance Requirements
- **Target Scan Interval**: 250ms (adaptive based on combat state)
- **Mobile Data Caching**: 500ms cache duration for distance calculations
- **Memory Management**: Automatic cache cleanup and size limits
- **API Optimization**: Minimal health bar opening for performance

### 3.2 Configuration Architecture
- **Config File**: `combat_config.json` in `/config/` directory
- **Dot Notation Access**: `config_manager.get_combat_setting('section.key')`
- **Runtime Updates**: Settings changes apply immediately
- **Default Fallbacks**: Comprehensive default configuration

### 3.3 Integration Points
- **ConfigManager**: Centralized configuration management
- **Logger**: Standardized logging with debug levels
- **Player API**: War mode detection, health monitoring
- **Mobiles API**: Target detection and mobile data
- **Target API**: Target selection and attack commands

## 4. Configuration Schema

### 4.1 System Toggles
```json
"system_toggles": {
    "combat_system_enabled": false,    // Master enable/disable
    "auto_target_enabled": true,       // Automatic target selection
    "auto_attack_enabled": true        // Automatic attack execution
}
```

### 4.2 Target Selection
```json
"target_selection": {
    "max_range": 10,                   // Maximum targeting range in tiles
    "priority_mode": "closest",        // Target priority algorithm
    "ignore_innocents": true,          // Skip blue NPCs/players
    "ignore_pets": true,               // Skip pet animals
    "allow_target_blues": false        // Advanced: allow blue targeting
}
```

### 4.3 Combat Behavior
```json
"combat_behavior": {
    "attack_delay_ms": 250,            // Delay between attacks
    "combat_timeout_ms": 30000,        // Max time per target
    "retreat_on_low_health": true,     // Auto-retreat feature
    "retreat_health_threshold": 30     // Health % to retreat
}
```

### 4.4 Timing Settings
```json
"timing_settings": {
    "target_scan_interval": 250,       // How often to scan for targets
    "combat_check_interval": 250       // Combat system update frequency
}
```

### 4.5 Display Settings
```json
"display_settings": {
    "show_target_name_overhead": true,     // Show target info
    "target_name_display_interval_ms": 3000,  // Update frequency
    "target_name_display_color": 53        // Display color
}
```

## 5. User Experience

### 5.1 Activation Workflow
1. **Player enters War Mode** (press Tab key in UO)
2. **Combat system activates** (if enabled in config)
3. **System scans for valid targets** within range
4. **Auto-targeting selects best target** based on priority mode
5. **Auto-attack engages target** (if enabled)
6. **System monitors combat** until target dies or conditions change

### 5.2 Safety Controls
- **War Mode Requirement**: Explicit user control over combat activation
- **Manual Override**: Player can target manually at any time
- **Emergency Exit**: ESC key or exiting War Mode stops combat immediately
- **Health Monitoring**: Automatic retreat when health drops too low

### 5.3 Status Feedback
- **Target Name Display**: Shows current target and health overhead
- **Console Logging**: Detailed combat actions and decisions
- **Debug Mode**: Extensive logging for troubleshooting
- **GUMP Integration**: Combat status in main bot interface (future)

## 6. Testing Criteria

### 6.1 Core Functionality Tests
- **War Mode Detection**: Verify system only activates in War Mode
- **Target Selection**: Confirm correct priority-based targeting
- **Attack Execution**: Validate weapon attacks are triggered
- **Health Monitoring**: Check target death detection

### 6.2 Safety Tests
- **Blue Target Protection**: Ensure innocent targets are skipped
- **Retreat Testing**: Verify low health disengagement
- **Timeout Testing**: Confirm combat timeout works
- **Emergency Stop**: Test immediate disengagement

### 6.3 Performance Tests
- **Target Scanning**: Measure scan interval consistency
- **Memory Usage**: Monitor cache size and cleanup
- **API Efficiency**: Validate minimal health bar operations
- **Integration**: Test with Auto Heal and Looting systems

### 6.4 Configuration Tests
- **Setting Changes**: Verify runtime configuration updates
- **Default Handling**: Test with missing config sections
- **Edge Cases**: Invalid values, extreme ranges
- **Save/Load**: Configuration persistence testing

## 7. Future Enhancements

### 7.1 Advanced Targeting
- **Spell Target Integration**: Support for magic combat
- **Weapon Type Optimization**: Range-based targeting for archers
- **Guild/Party Protection**: Advanced friend/foe detection
- **Custom Target Lists**: User-defined priority targets

### 7.2 Combat Tactics
- **Kiting Support**: Hit-and-run combat for ranged builds
- **Spell Casting**: Integration with magic systems
- **Buff Management**: Automatic combat buffs
- **Formation Combat**: Multi-character coordination

### 7.3 Integration Expansions
- **GUMP Controls**: In-game combat configuration
- **Statistics Tracking**: Combat performance metrics
- **Loot Integration**: Seamless post-combat looting
- **Death Recovery**: Automatic resurrection coordination

---

## Implementation Status: ✅ COMPLETED

**Current Version**: 1.4 - Full implementation with performance optimizations
**Build Integration**: Available in `dist/DexBot.py` v3.1.1
**Configuration**: Complete JSON configuration system
**Testing**: Core functionality validated in production environment

*Document Version: 1.0 - Initial comprehensive PRD*

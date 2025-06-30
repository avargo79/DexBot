# Auto Heal System - Product Requirements Document (PRD)

**Version**: 3.1.1  
**Last Updated**: June 2025  
**Parent System**: DexBot  

## 1. Overview

### 1.1 Purpose
The Auto Heal System is a core component of DexBot that provides intelligent, automated healing management for Ultima Online characters. It utilizes both bandages and heal potions with advanced retry mechanisms, resource management, and performance optimizations to ensure reliable and efficient healing during gameplay.

### 1.2 System Goals
- Provide automated healing that prioritizes player survival and resource efficiency
- Offer flexible healing options with independent control over bandages and heal potions
- Implement intelligent healing logic that adapts to different health scenarios
- Maintain high performance with minimal impact on game client performance
- Provide comprehensive logging and status reporting for monitoring and debugging

### 1.3 Integration Points
- **Core Bot**: Integrates with main loop for continuous health monitoring
- **GUMP Interface**: Provides real-time controls and status display
- **Configuration Manager**: Manages persistent settings and user preferences
- **Combat System**: Coordinates healing during combat engagements
- **Logger**: Provides comprehensive logging for debugging and monitoring

## 2. Functional Requirements

### 2.1 Core Healing Logic
- **FR-AH-001: Intelligent Healing Prioritization**: System prioritizes heal potions for critical health (<50%) and uses bandages for normal healing
- **FR-AH-002: Dual Resource Management**: Allows independent toggling of bandages and heal potions through configuration
- **FR-AH-003: Real-time Health Monitoring**: Continuously tracks player health and activates healing at configurable threshold (default 90%)
- **FR-AH-004: Advanced Retry Mechanism**: Implements configurable retry system for bandage application with delays
- **FR-AH-005: Poison Detection**: Automatically detects and responds to poison status with appropriate healing
- **FR-AH-006: Death State Handling**: Automatically pauses healing when player is dead or ghosted

### 2.2 Resource Management
- **FR-AH-007: Bandage Supply Monitoring**: Tracks bandage inventory and provides low supply warnings
- **FR-AH-008: Heal Potion Detection**: Automatically detects available heal potions in inventory
- **FR-AH-009: Resource Validation**: Validates healing resources before attempting healing actions
- **FR-AH-010: Inventory Optimization**: Efficiently searches for healing items with configurable search range
- **FR-AH-011: Supply Alerts**: Provides user notifications when healing supplies are critically low

### 2.3 Timing and Cooldown Management
- **FR-AH-012: Healing Cooldowns**: Implements separate cooldown timers for bandages and potions
- **FR-AH-013: Journal Integration**: Monitors healing completion messages for accurate cooldown tracking
- **FR-AH-014: Configurable Timers**: Supports user-customizable healing timer durations
- **FR-AH-015: Performance Optimization**: Uses efficient timer checking to minimize CPU usage

### 2.4 Configuration Management
- **FR-AH-016: Persistent Settings**: Saves all healing preferences to JSON configuration file
- **FR-AH-017: Runtime Configuration**: Allows configuration changes without script restart
- **FR-AH-018: Default Handling**: Automatically creates configuration with sensible defaults
- **FR-AH-019: Backwards Compatibility**: Maintains compatibility with previous configuration versions

### 2.5 User Interface Integration
- **FR-AH-020: GUMP Controls**: Provides toggle controls for bandage and potion healing
- **FR-AH-021: Status Display**: Shows real-time healing status, resource counts, and health percentage
- **FR-AH-022: Visual Indicators**: Uses color-coded status indicators for health and resource levels
- **FR-AH-023: Statistics Tracking**: Displays healing statistics including bandages applied and potions used

## 3. Technical Requirements

### 3.1 Performance Requirements
- **TR-AH-001: Response Time**: Healing activation must occur within 500ms of health threshold breach
- **TR-AH-002: Resource Efficiency**: Bandage supply checks limited to every 30 seconds to minimize API calls
- **TR-AH-003: Memory Usage**: System must maintain stable memory usage over extended runtime
- **TR-AH-004: CPU Optimization**: Healing logic must consume minimal CPU cycles during idle periods

### 3.2 Reliability Requirements
- **TR-AH-005: Error Recovery**: System must gracefully handle healing failures and retry automatically
- **TR-AH-006: State Consistency**: Healing state must remain consistent across all system interactions
- **TR-AH-007: Resource Validation**: All healing attempts must validate resource availability before execution
- **TR-AH-008: Concurrent Safety**: System must handle concurrent healing requests safely

### 3.3 Integration Requirements
- **TR-AH-009: API Compatibility**: Must work with all standard RazorEnhanced API functions
- **TR-AH-010: System Coordination**: Must coordinate with combat and other systems without conflicts
- **TR-AH-011: Configuration Sync**: Must synchronize configuration changes with GUMP interface immediately
- **TR-AH-012: Logging Integration**: Must use centralized logging system for all messages

## 4. Configuration Schema

### 4.1 Healing Toggles
```json
{
  "healing_toggles": {
    "bandage_healing_enabled": true,
    "potion_healing_enabled": true
  }
}
```

### 4.2 Health Thresholds
```json
{
  "health_thresholds": {
    "healing_threshold_percentage": 90,
    "critical_health_threshold": 50,
    "bandage_threshold_hp": 1
  }
}
```

**Threshold Behavior:**
- `healing_threshold_percentage`: Start healing when health drops below this percentage
- `critical_health_threshold`: Use healing potions immediately when health is **at or below** this percentage (inclusive ≤ comparison)
- `bandage_threshold_hp`: Minimum HP threshold for bandage healing

### 4.3 Item Identification
```json
{
  "item_ids": {
    "bandage_id": "0x0E21",
    "heal_potion_id": "0x0F0C",
    "lesser_heal_potion_id": null,
    "greater_heal_potion_id": null
  }
}
```

### 4.4 Timing Settings
```json
{
  "timing_settings": {
    "healing_timer_duration_ms": 11000,
    "potion_cooldown_ms": 10000,
    "bandage_retry_delay_ms": 500,
    "healing_check_interval": 1
  }
}
```

### 4.5 Resource Management
```json
{
  "resource_management": {
    "bandage_retry_attempts": 3,
    "low_bandage_warning": 10,
    "search_range": 2,
    "bandage_check_interval_cycles": 120
  }
}
```

### 4.6 Journal Monitoring
```json
{
  "journal_monitoring": {
    "healing_success_msg": "You finish applying the bandages.",
    "healing_partial_msg": "You apply the bandages, but they barely help.",
    "journal_message_type": "System"
  }
}
```

### 4.7 UI Color Thresholds
```json
{
  "color_thresholds": {
    "bandage_high_threshold": 20,
    "bandage_medium_threshold": 10,
    "potion_high_threshold": 10,
    "potion_medium_threshold": 5,
    "health_high_threshold": 75,
    "health_medium_threshold": 50
  }
}
```

## 5. System Architecture

### 5.1 Core Components
- **`auto_heal.py`**: Main healing system implementation
- **`auto_heal_config.json`**: Configuration file for healing settings
- **Helper Functions**: Utility functions for resource checking and validation
- **Integration Modules**: Interfaces with GUMP, logging, and configuration systems

### 5.2 Healing Flow
1. **Health Monitoring**: Continuous health percentage checking
2. **Resource Validation**: Verify availability of healing resources
3. **Method Selection**: Choose between bandages and potions based on health level
4. **Healing Execution**: Apply selected healing method with retry logic
5. **Cooldown Management**: Track healing timers and completion status
6. **Status Updates**: Update GUMP interface and logging systems

### 5.3 Error Handling
- **Resource Exhaustion**: Graceful handling when healing supplies run out
- **API Failures**: Retry mechanisms for failed healing attempts
- **State Corruption**: Recovery procedures for inconsistent healing states
- **Timeout Handling**: Proper cleanup for healing operations that exceed expected duration

## 6. Testing Requirements

### 6.1 Unit Testing
- **UT-AH-001**: Test healing threshold calculations
- **UT-AH-002**: Test resource availability checking
- **UT-AH-003**: Test healing method selection logic
- **UT-AH-004**: Test configuration loading and validation
- **UT-AH-005**: Test timer and cooldown management

### 6.2 Integration Testing
- **IT-AH-001**: Test integration with GUMP interface
- **IT-AH-002**: Test integration with combat system
- **IT-AH-003**: Test configuration synchronization
- **IT-AH-004**: Test logging integration
- **IT-AH-005**: Test resource depletion scenarios

### 6.3 Performance Testing
- **PT-AH-001**: Test healing response times under load
- **PT-AH-002**: Test memory usage during extended runtime
- **PT-AH-003**: Test CPU usage during idle and active periods
- **PT-AH-004**: Test resource checking efficiency

### 6.4 User Acceptance Testing
- **UAT-AH-001**: Test healing effectiveness in combat scenarios
- **UAT-AH-002**: Test GUMP interface responsiveness
- **UAT-AH-003**: Test configuration changes take effect immediately
- **UAT-AH-004**: Test healing statistics accuracy
- **UAT-AH-005**: Test resource warning notifications

## 7. Success Criteria

### 7.1 Performance Metrics
- Healing activation within 500ms of threshold breach
- 99.9% uptime during normal gameplay
- Memory usage remains stable over 8+ hour sessions
- CPU usage under 5% during idle periods

### 7.2 Functionality Metrics
- 95% success rate for healing attempts
- Accurate resource tracking with <1% error rate
- Configuration changes applied within 100ms
- Zero healing conflicts with combat system

### 7.3 User Experience Metrics
- Intuitive GUMP interface with clear status indicators
- Comprehensive logging for troubleshooting
- Flexible configuration options for different playstyles
- Reliable operation without manual intervention

## 8. Future Enhancements

### 8.1 Planned Features
- **Multi-Potion Support**: Support for lesser and greater heal potions
- **Cure Potion Integration**: Automatic cure potion usage for poison
- **Bandage Types**: Support for different bandage types and effectiveness
- **Healing Spells**: Integration with magical healing spells

### 8.2 Advanced Features
- **Predictive Healing**: Anticipate damage patterns and pre-heal
- **Group Healing**: Extend healing to party members
- **Reagent Management**: Automatic reagent restocking for spell healing
- **Custom Healing Profiles**: Preset configurations for different scenarios

## 9. Dependencies

### 9.1 External Dependencies
- **RazorEnhanced**: Core API for game interaction
- **Ultima Online Client**: Target game client
- **Python Runtime**: Execution environment

### 9.2 Internal Dependencies
- **Bot Configuration**: Shared configuration management
- **Logger System**: Centralized logging infrastructure
- **GUMP Interface**: User interface components
- **Helper Utilities**: Common utility functions

## 10. Risk Assessment

### 10.1 Technical Risks
- **API Changes**: RazorEnhanced API modifications could break functionality
- **Performance Degradation**: Inefficient healing logic could impact client performance
- **Resource Conflicts**: Inventory management conflicts with other systems

### 10.2 Mitigation Strategies
- **API Abstraction**: Use wrapper functions to isolate API dependencies
- **Performance Monitoring**: Implement performance metrics and alerts
- **Resource Coordination**: Centralized inventory management system
- **Comprehensive Testing**: Extensive testing across different scenarios

This PRD defines the complete Auto Heal System as a standalone, well-documented component that can be developed, tested, and maintained independently while integrating seamlessly with the broader DexBot ecosystem.

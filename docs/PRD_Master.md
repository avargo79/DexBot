# DexBot - Master Product Requirements Document (PRD)

**Version**: 3.1.1
**Last Updated**: June 30, 2025

## 1. Overview

### 1.1 Purpose
DexBot is a modular bot system for Ultima Online using RazorEnhanced. It is designed to be a scalable and maintainable bot that provides advanced automation for healing, combat, and looting tasks. The system has evolved from an initial Auto Heal focus to a comprehensive bot that handles multiple automated systems with exceptional performance optimizations.

### 1.2 Target User
The target users are Ultima Online players who use the RazorEnhanced client and want to automate repetitive tasks such as healing, combat engagement, and intelligent looting. The system is aimed at players who want a reliable, high-performance bot that can be customized to their needs and provides real-time feedback and control.

### 1.3 System Architecture Goals
- **Modular Design**: Establish a clean separation of concerns with independent, maintainable systems
- **High Performance**: Deliver exceptional performance through API-level optimizations and efficient execution
- **User Experience**: Provide an intuitive real-time GUMP interface for bot control and status monitoring
- **Configuration Management**: Allow persistent configuration of all system settings with runtime updates
- **Reliability**: Gracefully handle player death, resurrection, and system state management
- **Extensibility**: Support easy addition and modification of systems through well-defined interfaces

### 1.4 Current System Components (v3.1.1)
- **Auto Heal System**: Intelligent healing management using bandages and heal potions
- **Combat System**: Advanced combat with enemy detection, targeting, and automated engagement
- **Looting System**: Intelligent looting with configurable item filters and performance optimizations
- **GUMP Interface**: Real-time user interface for control and monitoring
- **Configuration Manager**: Centralized configuration with persistent storage
- **Logging System**: Comprehensive logging with multiple levels and system integration

### 1.5 Future System Roadmap
- **Skinning System**: Corpse skinning and resource harvesting automation
- **Buff Management**: Character buff maintenance and stamina management
- **Equipment Manager**: Automatic weapon re-equipping and gear management
- **Inventory System**: Smart inventory management with automatic item dropping
- **Skill Training**: Advanced skill training automation
- **Party Support**: Multi-character coordination and party-based automation

## 2. System Integration Requirements

### 2.1 Core Integration Framework
The DexBot architecture is built around a central integration framework that coordinates all subsystems:

- **FR-INT-001: Unified Main Loop**: All systems execute through a single, optimized main loop with 250ms cycle time
- **FR-INT-002: Shared Configuration**: Centralized configuration management with system-specific config files
- **FR-INT-003: Cross-System Communication**: Systems can communicate status and coordinate actions through shared interfaces
- **FR-INT-004: State Management**: Unified state management for player status, system status, and runtime statistics
- **FR-INT-005: Error Coordination**: Centralized error handling and recovery across all systems

### 2.2 User Interface Integration
- **FR-UI-001: Unified GUMP Interface**: Single GUMP interface that provides controls and status for all systems
- **FR-UI-002: Real-time Updates**: Dynamic UI updates that reflect system status changes immediately
- **FR-UI-003: System Toggle Controls**: Independent enable/disable controls for each major system
- **FR-UI-004: Consolidated Statistics**: Unified display of runtime statistics across all systems
- **FR-UI-005: Visual Status Indicators**: Color-coded status indicators that provide at-a-glance system health

### 2.3 Configuration Management Integration
- **FR-CFG-001: Modular Configuration**: Each system maintains its own configuration file while integrating with global settings
- **FR-CFG-002: Runtime Configuration**: All configuration changes apply immediately without requiring script restart
- **FR-CFG-003: Configuration Validation**: Centralized validation of configuration values across all systems
- **FR-CFG-004: Default Management**: Automatic creation and management of default configurations for all systems
- **FR-CFG-005: Version Migration**: Automatic migration of configuration files when system versions change

### 2.4 Performance Integration
- **FR-PERF-001: Shared Optimizations**: Common performance optimizations (ignore lists, caching) shared across systems
- **FR-PERF-002: Resource Coordination**: Coordinated resource management to prevent conflicts between systems
- **FR-PERF-003: Performance Monitoring**: Built-in performance monitoring and reporting across all systems
- **FR-PERF-004: Adaptive Timing**: Dynamic timing adjustments based on system load and performance metrics

### 2.5 System-Specific Integration Points

#### 2.5.1 Auto Heal System Integration
- Integration with combat system for coordinated healing during fights
- GUMP interface for healing controls and status display
- Configuration synchronization for healing thresholds and options
- Performance optimization through efficient resource checking

#### 2.5.2 Combat System Integration  
- Coordination with auto heal system for damage management
- Integration with looting system for post-combat corpse processing
- GUMP interface for combat controls and target information
- Configuration management for combat settings and targeting rules

#### 2.5.3 Looting System Integration
- Post-combat activation through combat system coordination
- GUMP interface for loot statistics and configuration
- Shared ignore lists and performance optimizations
- Configuration management for item filters and looting preferences

## 3. System Architecture Requirements

### 3.1 Performance Architecture
- **AR-PERF-001: Main Loop Efficiency**: The bot should maintain efficient operation with a target delay of 250ms per cycle
- **AR-PERF-002: Dynamic UI Updates**: GUMP updates should be optimized to only occur when data changes
- **AR-PERF-003: API Optimization**: Systems should achieve 85-95% performance improvement through ignore list optimization and caching
- **AR-PERF-004: Memory Management**: Memory usage should remain stable over extended runtime periods through efficient resource management
- **AR-PERF-005: Minimal Impact**: The bot should have minimal impact on client performance through optimized execution

### 3.2 Integration Architecture
- **AR-INT-001: Modular Design**: Systems must be designed as independent modules with well-defined interfaces
- **AR-INT-002: Shared Services**: Common services (logging, configuration, UI) must be shared across all systems
- **AR-INT-003: Event Coordination**: Systems must coordinate through event-based communication where appropriate
- **AR-INT-004: State Synchronization**: System states must be synchronized and accessible through shared interfaces
- **AR-INT-005: Error Isolation**: Errors in one system must not cascade to other systems

### 3.3 Configuration Architecture
- **AR-CFG-001: Hierarchical Configuration**: Support global, system-specific, and user-specific configuration layers
- **AR-CFG-002: Schema Validation**: All configuration must be validated against defined schemas
- **AR-CFG-003: Migration Support**: Configuration must support automatic migration between versions
- **AR-CFG-004: Runtime Reload**: Configuration changes must be applied without system restart
- **AR-CFG-005: Backup and Recovery**: Configuration must support backup and recovery mechanisms

### 3.4 User Interface Architecture
- **AR-UI-001: Single Interface**: All systems must integrate into a single, coherent GUMP interface
- **AR-UI-002: Responsive Design**: Interface must respond to user interactions within 100ms
- **AR-UI-003: Status Consistency**: Interface must accurately reflect the current state of all systems
- **AR-UI-004: Accessibility**: Interface must provide clear visual and textual feedback for all operations
- **AR-UI-005: Customization**: Interface must support user customization of layout and display options

## 4. Non-Functional Requirements

### 4.1 Performance Requirements
- **Main loop execution**: 250ms target cycle time with 95% consistency
- **Healing response time**: Sub-500ms response to health threshold breaches
- **Combat engagement**: Sub-1000ms target acquisition and engagement
- **Looting efficiency**: 85-95% performance improvement through optimization
- **Memory stability**: Stable memory usage over 8+ hour runtime sessions
- **CPU efficiency**: Under 5% CPU usage during idle periods

### 4.2 Reliability Requirements
- **System uptime**: 99.9% uptime during normal gameplay conditions
- **Error recovery**: Automatic recovery from 95% of common error conditions
- **State consistency**: Maintained across player death, resurrection, and reconnection
- **Configuration integrity**: Preserved across all system updates and changes
- **Resource handling**: Graceful degradation when resources are unavailable

### 4.3 Usability Requirements
- **Interface intuitiveness**: New users should understand basic controls within 5 minutes
- **Configuration simplicity**: Most users should only need to adjust 3-5 key settings
- **Status clarity**: System status should be clear at a glance without detailed analysis
- **Response feedback**: All user actions should provide immediate visual feedback
- **Documentation accessibility**: Core functionality should be self-documenting through the interface

### 4.4 Maintainability Requirements
- **Modular architecture**: Individual systems can be updated without affecting others
- **Code documentation**: All public interfaces must have comprehensive documentation
- **Testing coverage**: Critical functionality must have automated test coverage
- **Version compatibility**: New versions must maintain compatibility with existing configurations
- **Debug capability**: Comprehensive logging must support troubleshooting and optimization

## 5. System Design and Architecture

### 5.1 Overall System Architecture
```
DexBot System Architecture
├── Core Framework
│   ├── Main Loop Controller (250ms cycle)
│   ├── System Coordinator (cross-system communication)
│   ├── State Manager (unified state management)
│   └── Error Handler (system-wide error management)
├── User Interface Layer
│   ├── GUMP Controller (unified interface)
│   ├── Status Display (real-time updates)
│   ├── Control Handlers (user interactions)
│   └── Visual Feedback (status indicators)
├── System Layer
│   ├── Auto Heal System (healing automation)
│   ├── Combat System (enemy engagement)
│   ├── Looting System (corpse processing)
│   └── [Future Systems] (extensible architecture)
├── Configuration Layer
│   ├── Configuration Manager (centralized config)
│   ├── Schema Validator (config validation)
│   ├── Migration Handler (version updates)
│   └── Persistence Manager (config storage)
├── Utility Layer
│   ├── Logger (comprehensive logging)
│   ├── Performance Monitor (system metrics)
│   ├── Helper Functions (common utilities)
│   └── API Wrappers (RazorEnhanced interface)
└── Data Layer
    ├── Shared Cache (performance optimization)
    ├── Ignore Lists (API optimization)
    ├── Statistics Store (runtime metrics)
    └── Configuration Store (persistent settings)
```

### 5.2 Directory Structure
The project follows a clean, modular structure optimized for maintainability and performance:
```
DexBot/
├── dist/                           # Bundled distribution files
│   └── DexBot.py                   # Main distribution file (generated)
├── docs/                           # Project documentation
│   ├── PRD_Master.md              # Master architecture PRD (this file)
│   ├── PRD_Auto_Heal_System.md    # Auto Heal system PRD
│   ├── PRD_Combat_System.md       # Combat system PRD
│   ├── PRD_Looting_System.md      # Looting system PRD
│   ├── Development_Status.md      # Development status and roadmap
│   └── CHANGELOG.md               # Version history and changes
├── src/                           # Source code modules
│   ├── config/                    # Configuration management
│   │   ├── config_manager.py      # Centralized configuration
│   │   └── [system]_config.json   # System-specific configurations
│   ├── core/                      # Core bot functionality
│   │   ├── main_loop.py           # Main execution loop
│   │   ├── bot_config.py          # Core configuration
│   │   └── logger.py              # Logging system
│   ├── systems/                   # Individual bot systems
│   │   ├── auto_heal.py           # Auto healing system
│   │   ├── combat.py              # Combat system
│   │   └── looting.py             # Looting system
│   ├── ui/                        # User interface components
│   │   └── gump_interface.py      # GUMP interface controller
│   └── utils/                     # Utility functions and helpers
│       ├── helpers.py             # Common utility functions
│       └── imports.py             # RazorEnhanced API imports
├── config/                        # User configuration files
│   ├── main_config.json           # Main bot configuration
│   ├── auto_heal_config.json      # Auto heal settings
│   ├── combat_config.json         # Combat settings
│   └── looting_config.json        # Looting settings
├── ref/                           # Reference documentation
│   ├── Items_Reference.md         # Game item references
│   └── RazorEnhanced_API.md       # API documentation
├── archive/                       # Legacy files and development artifacts
├── scripts/                       # Build and development scripts
├── tests/                         # Test files
├── pyproject.toml                 # Project configuration
└── README.md                      # Project overview
```

### 5.3 Core Component Descriptions
- **`dist/DexBot.py`**: The bundled distribution file containing all systems integrated into a single script
- **`src/core/main_loop.py`**: The heart of the bot, orchestrating all systems with performance optimization
- **`src/systems/[system].py`**: Individual system implementations with well-defined interfaces
- **`src/ui/gump_interface.py`**: Dynamic GUMP interface with real-time updates and unified controls
- **`src/config/config_manager.py`**: Centralized configuration management with validation and persistence
- **Configuration Files**: JSON-based configuration files for each system with schema validation

### 5.4 Integration Patterns
- **Event-Driven Architecture**: Systems communicate through events and shared state
- **Singleton Configuration**: Centralized configuration management with system-specific extensions
- **Observer Pattern**: UI components observe system state changes for real-time updates
- **Command Pattern**: User interactions processed through command handlers
- **Strategy Pattern**: Different algorithms for healing, combat, and looting based on configuration

### 5.5 Performance Optimization Strategies
- **API Ignore Lists**: Extensive use of RazorEnhanced ignore lists to reduce API overhead
- **Intelligent Caching**: Cached results for expensive operations with appropriate invalidation
- **Conditional Updates**: UI and system updates only when actual changes occur
- **Resource Pooling**: Reuse of objects and resources to minimize garbage collection
- **Batch Processing**: Group related operations to minimize API calls

## 6. System Integration Specifications

### 6.1 Inter-System Communication
Systems communicate through well-defined interfaces and shared state management:

#### 6.1.1 Shared State Interface
```python
class SystemState:
    # Player state
    health_percentage: float
    is_dead: bool
    is_in_combat: bool
    
    # System status
    healing_active: bool
    combat_active: bool
    looting_active: bool
    
    # Resource tracking
    bandage_count: int
    potion_count: int
    current_target: Optional[int]
```

#### 6.1.2 Event System
```python
class SystemEvents:
    # Combat events
    COMBAT_STARTED = "combat_started"
    COMBAT_ENDED = "combat_ended"
    TARGET_KILLED = "target_killed"
    
    # Healing events
    HEALING_STARTED = "healing_started"
    HEALING_COMPLETED = "healing_completed"
    RESOURCES_LOW = "resources_low"
    
    # System events
    PLAYER_DIED = "player_died"
    PLAYER_RESURRECTED = "player_resurrected"
```

### 6.2 Configuration Integration
Each system maintains its own configuration while integrating with the global configuration framework:

#### 6.2.1 Configuration Hierarchy
```
Global Configuration (main_config.json)
├── System Enable/Disable Flags
├── Global Performance Settings
├── UI Preferences
└── Debug Settings

System Configurations
├── auto_heal_config.json
├── combat_config.json
└── looting_config.json
```

#### 6.2.2 Configuration Synchronization
- Changes to GUMP toggles immediately update both memory and configuration files
- Configuration validation occurs on load and before save operations
- Migration handlers ensure compatibility across version updates

### 6.3 User Interface Integration
The unified GUMP interface provides centralized control for all systems:

#### 6.3.1 Interface Sections
```
Main GUMP Interface
├── System Status Section
│   ├── Health Display (Auto Heal integration)
│   ├── Combat Status (Combat system integration)
│   └── Loot Statistics (Looting system integration)
├── Control Section
│   ├── System Toggle Buttons
│   ├── Emergency Stop Button
│   └── Configuration Access
└── Statistics Section
    ├── Runtime Information
    ├── Performance Metrics
    └── Resource Tracking
```

#### 6.3.2 Real-time Updates
- UI updates occur only when system state changes
- Color-coded status indicators provide immediate visual feedback
- Statistics update in real-time based on system activity

## 7. Quality Assurance and Testing

### 7.1 Testing Strategy
- **Unit Testing**: Each system component tested independently
- **Integration Testing**: Cross-system communication and coordination
- **Performance Testing**: Load testing and resource usage monitoring
- **User Acceptance Testing**: Real-world gameplay scenario validation

### 7.2 Quality Metrics
- **Code Coverage**: Minimum 80% code coverage for critical paths
- **Performance Benchmarks**: Established baselines for all performance metrics
- **Reliability Metrics**: Mean time between failures and recovery rates
- **User Experience Metrics**: Interface responsiveness and user satisfaction

### 7.3 Continuous Monitoring
- **Performance Monitoring**: Real-time performance metrics collection
- **Error Tracking**: Comprehensive error logging and analysis
- **Usage Analytics**: Understanding how systems are used in practice
- **Resource Monitoring**: Tracking resource usage patterns and optimization opportunities

## 8. Future Architecture Considerations

### 8.1 Scalability Planning
- **Multi-Character Support**: Architecture designed to support multiple character automation
- **Distributed Processing**: Potential for distributed system processing
- **Plugin Architecture**: Framework for third-party system development
- **Cloud Integration**: Potential for cloud-based configuration and statistics

### 8.2 Technology Evolution
- **API Updates**: Prepared for RazorEnhanced API changes and enhancements
- **Performance Improvements**: Ongoing optimization strategies and techniques
- **Language Features**: Leveraging new Python features and capabilities
- **Development Tools**: Integration with modern development and deployment tools

### 8.3 Community and Ecosystem
- **Open Source Considerations**: Potential for open source community contributions
- **Documentation Standards**: Comprehensive documentation for all system interfaces
- **Development Guidelines**: Clear guidelines for system development and integration
- **Support Infrastructure**: User support and community engagement frameworks

## 9. Risk Management and Mitigation

### 9.1 Technical Risks
- **API Dependency**: RazorEnhanced API changes could affect functionality
- **Performance Degradation**: Complex system interactions could impact performance
- **Configuration Complexity**: Growing configuration options could overwhelm users
- **System Conflicts**: Inter-system resource conflicts could cause instability

### 9.2 Mitigation Strategies
- **API Abstraction**: Wrapper functions isolate direct API dependencies
- **Performance Monitoring**: Continuous monitoring with automated alerts
- **Configuration UI**: Intuitive interface reduces configuration complexity
- **Resource Coordination**: Centralized resource management prevents conflicts

### 9.3 Contingency Planning
- **Fallback Modes**: Graceful degradation when systems fail
- **Recovery Procedures**: Automated recovery from common failure scenarios
- **Emergency Stops**: Safe shutdown procedures for critical failures
- **Backup Systems**: Alternative approaches for critical functionality

## 10. Success Criteria and Metrics

### 10.1 Technical Success Criteria
- **Performance**: Consistent 250ms main loop execution with <5% CPU usage
- **Reliability**: 99.9% uptime during normal gameplay conditions
- **Integration**: Seamless coordination between all systems
- **Maintainability**: New system integration in <1 day development time

### 10.2 User Experience Success Criteria
- **Ease of Use**: New users operational within 10 minutes
- **Reliability**: Users can rely on bot for extended gameplay sessions
- **Customization**: Users can configure bot to their specific needs
- **Feedback**: Clear understanding of bot status and actions at all times

### 10.3 Business/Project Success Criteria
- **Maintainability**: Individual system updates without affecting others
- **Extensibility**: New system development follows established patterns
- **Documentation**: Comprehensive documentation supports community growth
- **Sustainability**: Architecture supports long-term development and maintenance

This master PRD provides the architectural foundation for the DexBot system while allowing individual system PRDs to define specific requirements and implementation details. The modular architecture ensures that each system can be developed, tested, and maintained independently while integrating seamlessly with the overall bot ecosystem.

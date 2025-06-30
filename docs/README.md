# Documentation Index

This directory contains all project documentation for DexBot, organized by system and purpose.

## Product Requirements Documents (PRDs)

### Master Architecture
- **[PRD_Master.md](PRD_Master.md)** - Master PRD focusing on overall system architecture, integration patterns, and cross-system requirements

### System-Specific PRDs
- **[PRD_Auto_Heal_System.md](PRD_Auto_Heal_System.md)** - Complete requirements for the Auto Heal system including configuration schema, functional requirements, and testing criteria
- **[PRD_Combat_System.md](PRD_Combat_System.md)** - Combat system requirements covering enemy detection, targeting, engagement logic, and configuration options
- **[PRD_Looting_System.md](PRD_Looting_System.md)** - Looting system requirements including corpse processing, item filtering, and performance optimizations

## Project Management
- **[Development_Status.md](Development_Status.md)** - Development tasks, roadmap, and project tracking
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and release notes

## Documentation Organization

### PRD Structure
Each system PRD follows a consistent structure:
1. **Overview** - Purpose, goals, and integration points
2. **Functional Requirements** - Detailed feature requirements with FR codes
3. **Technical Requirements** - Performance, reliability, and integration specs with TR codes
4. **Configuration Schema** - Complete configuration documentation with examples
5. **System Architecture** - Component descriptions and interaction patterns
6. **Testing Requirements** - Unit, integration, performance, and user acceptance tests
7. **Success Criteria** - Measurable goals and acceptance criteria
8. **Future Enhancements** - Planned features and extensibility considerations
9. **Dependencies** - External and internal dependencies
10. **Risk Assessment** - Identified risks and mitigation strategies

### Requirement Numbering
- **FR-[SYSTEM]-###**: Functional Requirements (e.g., FR-AH-001 for Auto Heal)
- **TR-[SYSTEM]-###**: Technical Requirements (e.g., TR-CB-001 for Combat)
- **AR-[CATEGORY]-###**: Architecture Requirements (e.g., AR-PERF-001 for Performance)
- **UT/IT/PT/UAT-[SYSTEM]-###**: Testing Requirements by type

### System Abbreviations
- **AH**: Auto Heal System
- **CB**: Combat System  
- **LT**: Looting System
- **INT**: Integration/Framework
- **UI**: User Interface
- **CFG**: Configuration
- **PERF**: Performance

## Usage Guidelines

### For Developers
1. Start with the master PRD to understand the overall architecture
2. Review the specific system PRD for detailed implementation requirements
3. Use requirement codes for traceability in code comments and commit messages
4. Update PRDs when adding new features or changing existing functionality

### For Contributors
1. Ensure any new systems follow the established PRD structure
2. Update the master PRD when adding new integration points
3. Maintain requirement numbering consistency
4. Document all configuration options and schemas

### For Users
1. Refer to system PRDs for comprehensive configuration options
2. Check the CHANGELOG for recent updates and changes
3. Use requirement codes when reporting issues or requesting features

## Maintenance Notes

- PRDs should be updated whenever significant changes are made to system requirements
- The master PRD should reflect the current overall architecture and integration patterns
- Configuration schemas in PRDs must match the actual JSON configuration files
- Testing requirements should be updated when new test scenarios are identified
- Success criteria should be measurable and regularly evaluated

This documentation structure supports both current development needs and future scalability while maintaining clear separation of concerns between systems.

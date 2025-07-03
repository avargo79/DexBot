# DexBot Documentation

This directory contains all project documentation for DexBot, organized according to industry best practices for product management and development.

## Quick Navigation

### 📋 Product Information
- **[Product Overview](PRODUCT_OVERVIEW.md)** - Executive summary, vision, and market position
- **[Project Status Summary](PROJECT_STATUS_SUMMARY.md)** - Comprehensive current project status and achievements
- **[Features & Capabilities](FEATURES.md)** - Comprehensive feature documentation

### 🗂️ GitHub Issues Workflow
- **[GitHub Issues Workflow](GITHUB_ISSUES_WORKFLOW.md)** - Official process guide for project management
- **[GitHub Issues Automation](GITHUB_ISSUES_AUTOMATION.md)** - Complete automation system guide with usage, configuration, and troubleshooting

### 📋 Product Backlog
- **[Product Backlog](backlog/PRODUCT_BACKLOG.md)** - Master prioritized list of features, bugs, and tasks
- **[Backlog Management Guide](backlog/README.md)** - Process documentation and best practices

### 📄 Product Requirements Documents (PRDs)  
- **[PRD Index](prds/README.md)** - Detailed specifications for approved features
- **[Active PRDs](prds/)** - Features ready for or in development

### 📊 Project Status
- **[Development Status](Development_Status.md)** - Current project status and roadmap
- **[Change Log](CHANGELOG.md)** - Version history and release notes

## Documentation Structure

```
docs/
├── README.md                     # This file - main documentation index
├── Development_Status.md         # Project status and roadmap
├── CHANGELOG.md                  # Version history
│
├── backlog/                      # Product backlog organization
│   ├── PRODUCT_BACKLOG.md       # Master prioritized backlog
│   ├── README.md                 # Backlog process guide
│   ├── high-priority/            # P1 items (current development)
│   ├── medium-priority/          # P2 items (next 2-3 versions) 
│   └── future/                   # P3+ items (long-term ideas)
│
└── prds/                         # Product Requirements Documents
    ├── README.md                 # PRD index and templates
    ├── [Active PRDs]             # Features in development
    └── archived/                 # Completed PRDs
```

## System-Specific Documentation

### Completed Systems (Production Ready)
- **Auto Heal System** ✅ - Automated healing and buff management
- **Combat System** ✅ - Enemy detection, targeting, and engagement  
- **Looting System** ✅ - Corpse processing and item management with performance optimization
- **GitHub Issues Workflow Automation** ✅ - Complete automation suite with intelligent routing and predictive analytics

### Active Development PRDs
- **[Inventory Management System](prds/FR-095_Inventory_Management_System.md)** - Smart inventory organization
- **[Equipment Manager System](prds/FR-096_Equipment_Manager_System.md)** - Automated equipment management

## Documentation Standards

### Backlog vs PRDs
- **Backlog Items**: Brief, prioritized tasks focusing on WHAT needs to be done and WHEN
- **PRDs**: Detailed specifications focusing on HOW features should be built
- **Relationship**: Backlog items reference PRDs when detailed specifications exist

### Priority Levels
- **P1 (High)**: Current sprint and critical issues
- **P2 (Medium)**: Next 2-3 versions  
- **P3+ (Future)**: Long-term considerations and ideas

### Item Types
- **FR-XXX**: Features (new functionality)
- **BUG-XXX**: Bug fixes and defects
- **ENH-XXX**: Enhancements to existing features
- **TECH-XXX**: Technical debt and optimization
- **RES-XXX**: Research and investigation items

### PRD Structure Standards
Each PRD follows this structure:
1. **Feature Overview** - Name, description, user story, business value
2. **Functional Requirements** - Detailed specs with acceptance criteria
3. **Technical Requirements** - Architecture and implementation details
4. **Configuration Schema** - API and config specifications
5. **Implementation Plan** - Development phases and timeline
6. **Success Criteria** - Measurable outcomes
7. **Risk Assessment** - Technical risks and mitigation
8. **Future Enhancements** - Potential extensions

## Contributing to Documentation

### Adding New Backlog Items
1. Review existing backlog to avoid duplicates
2. Add item to appropriate priority category
3. Include clear description and effort estimate
4. Link to PRD if detailed specification exists

### Creating PRDs
1. Use the standard PRD template from `/prds/README.md`
2. Include all required sections with detailed information
3. Get technical and business review before finalizing
4. Update related backlog items and links

### Maintaining Documentation
- Keep backlog items current and prioritized
- Update PRDs during development as needed
- Archive completed PRDs appropriately
- Maintain cross-references and links

## Process and Workflows

### Backlog Refinement
- **Frequency**: Bi-weekly review sessions
- **Activities**: Priority adjustment, effort estimation, PRD creation needs
- **Participants**: Development team and stakeholders

### Feature Development Lifecycle
1. **Backlog Entry** - Item identified and prioritized
2. **PRD Creation** - Detailed specification developed
3. **Development Planning** - Resource allocation and scheduling
4. **Implementation** - Feature development and testing
5. **Completion** - PRD archival and documentation updates

## Getting Started

### For Developers
1. Start with the [Product Backlog](backlog/PRODUCT_BACKLOG.md) to understand priorities
2. Review relevant [PRDs](prds/README.md) for detailed specifications
3. Check [Development Status](Development_Status.md) for current project state

### For Stakeholders  
1. Review [Product Backlog](backlog/PRODUCT_BACKLOG.md) for feature priorities
2. Provide feedback through established channels
3. Participate in backlog refinement sessions

### For Contributors
1. Read the [Backlog Process Guide](backlog/README.md)
2. Follow documentation standards when creating or updating content
3. Ensure proper cross-referencing and linking

---

**Last Updated**: July 1, 2025  
**Documentation Version**: 2.0 (Restructured for industry best practices)

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

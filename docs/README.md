# DexBot Documentation

This directory contains all project documentation for DexBot, organized for easy navigation and development workflow.

## Quick Navigation

### 📋 Project Information
- **[Project Overview](OVERVIEW.md)** - What DexBot is and what it does
- **[Project Status](PROJECT_STATUS.md)** - Current development status and achievements
- **[Features & Capabilities](FEATURES.md)** - Comprehensive feature documentation

### 🔧 Development & Workflow
- **[Development Guide](DEVELOPMENT_GUIDE.md)** - Complete development workflow and best practices
- **[Usage Examples](USAGE_EXAMPLES.md)** - Practical code examples and integration patterns
- **[GitHub Workflow](GITHUB_WORKFLOW.md)** - GitHub Issues workflow and automation

### 🔬 Research & Future Vision
- **[Research & Future Concepts](RESEARCH_AND_FUTURE_CONCEPTS.md)** - Long-term research concepts and collaboration opportunities

### 📄 Product Requirements Documents (PRDs)  
- **[PRD Index](prds/README.md)** - Detailed specifications for approved features
- **[Active PRDs](prds/)** - Features ready for or in development

### 📊 Project History
- **[Change Log](CHANGELOG.md)** - Version history and release notes

## Documentation Structure

```
docs/
├── README.md                           # This file - main documentation index
├── OVERVIEW.md                         # Project overview and vision
├── PROJECT_STATUS.md                   # Current status and achievements
├── DEVELOPMENT_GUIDE.md                # Complete development workflow
├── USAGE_EXAMPLES.md                   # Practical code examples and patterns
├── GITHUB_WORKFLOW.md                  # GitHub Issues and automation
├── FEATURES.md                         # Feature documentation
├── RESEARCH_AND_FUTURE_CONCEPTS.md    # Long-term research concepts
├── CHANGELOG.md                        # Version history
└── prds/                               # Product Requirements Documents
    ├── README.md                       # PRD index and templates
    └── [Active PRDs]                   # Features and technical specifications
```

## System-Specific Documentation

### ✅ Production Systems (Stable & Battle-Tested)
- **Auto Heal System** - Automated healing and buff management
- **Combat System** - Enemy detection, targeting, and engagement  
- **Looting System** - Corpse processing and item management with 90% performance optimization
- **GitHub Issues Workflow Automation** - Complete automation suite with intelligent routing

### 📋 Ready for Implementation
- **[Inventory Management System](prds/FR-095_Inventory_Management_System.md)** - Smart inventory organization
- **[Equipment Manager System](prds/FR-096_Equipment_Manager_System.md)** - Automated equipment management
- **[Buff Management System](prds/FR-084_Buff_Management_System.md)** - Automated buff monitoring and renewal

## Documentation Standards

### GitHub Issues vs PRDs
- **GitHub Issues**: Brief, prioritized tasks focusing on WHAT needs to be done and WHEN
- **PRDs**: Detailed specifications focusing on HOW features should be built
- **Relationship**: GitHub Issues reference PRDs when detailed specifications exist

### Priority Levels
- **P1 (High)**: Current development priorities
- **P2 (Medium)**: Next 2-3 versions  
- **P3+ (Future)**: Long-term considerations and ideas

### Item Types
- **FR-XXX**: Features (new functionality)
- **BUG-XXX**: Bug fixes and defects
- **ENH-XXX**: Enhancements to existing features
- **TECH-XXX**: Technical debt and optimization
- **RES-XXX**: Research and investigation items

## Navigation Workflows

### For New Developers
1. Start with [GitHub Issues](https://github.com/avargo79/DexBot/issues) to understand current development priorities
2. Read the [Development Guide](DEVELOPMENT_GUIDE.md) for complete workflow
3. Review [Project Overview](OVERVIEW.md) for context and architecture
4. Check [PRDs](prds/) for detailed feature specifications

### For Contributors
1. Review [GitHub Issues](https://github.com/avargo79/DexBot/issues) for current feature priorities and development status
2. Read the [GitHub Workflow Guide](GITHUB_WORKFLOW.md) for project management processes
3. Participate in GitHub Discussions for feature concepts and community input
4. Follow the [Development Guide](DEVELOPMENT_GUIDE.md) for contribution standards

### Adding New GitHub Issues
1. Review existing issues to avoid duplicates
2. Use appropriate labels according to issue type and priority
3. Reference related PRDs when detailed specifications exist
4. Follow established templates for consistency

### Creating PRDs
1. Feature identified and approved through GitHub Issues
2. Create PRD using template in [prds/README.md](prds/README.md)
3. Update related issues and documentation
4. Include acceptance criteria and technical specifications

## Best Practices

- Keep GitHub Issues current and properly labeled
- Reference PRDs in GitHub Issues for detailed specifications
- Update documentation when implementing features
- Follow established development workflow and coding standards
- Use the automated feature preparation scripts for new development

### Development Lifecycle
1. **GitHub Issue** - Feature identified and prioritized
2. **PRD Creation** - Detailed specification developed (for complex features)
3. **Implementation** - Code development following PRD requirements
4. **Testing** - Comprehensive testing using established patterns
5. **Documentation** - Update guides and references
6. **Release** - Version increment and deployment

### Getting Help
1. **Start with Documentation**: Most questions are answered in this directory
2. **GitHub Issues**: For bugs, feature requests, and support questions
3. **GitHub Discussions**: For broader concept exploration and community input
4. **Development Guide**: For development process and workflow questions

---

*This documentation directory provides comprehensive guidance for understanding, using, and contributing to the DexBot project. All files are actively maintained and synchronized with current development status.*

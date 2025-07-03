# DexBot Development Tools

**Purpose**: Development automation, analysis, and project management tools  
**Last Updated**: July 3, 2025

---

## 📁 Directory Structure

```
dev-tools/
├── github-automation/     # GitHub Issues and repository automation tools
├── analysis/             # Performance analysis and data processing tools  
├── project-management/   # Project planning and management automation
└── README.md            # This file - development tools overview
```

---

## 🛠️ Tool Categories

### GitHub Automation (`github-automation/`)
**Purpose**: Automate GitHub Issues, labels, and repository management

**Tools**:
- `create_issues.ps1` - Batch create GitHub Issues from backlog/PRDs
- `manage_issues.ps1` - Update, assign, and manage existing issues
- `setup_labels.ps1` - Configure GitHub repository labels and organization
- `github_auth_helper.ps1` - GitHub authentication and API setup
- `test_mock_github.ps1` - Mock GitHub API testing utilities
- `mock_github_api.ps1` - GitHub API simulation for development

**Usage**: GitHub repository management, issue automation, community engagement

### Analysis Tools (`analysis/`)
**Purpose**: Performance analysis, data processing, and metrics collection

**Tools**:
- `analyze_cycle_times.ps1` - Development cycle time analysis
- `analyze_planning.ps1` - Planning accuracy and estimation analysis
- `profile_performance.ps1` - System performance profiling and optimization
- `analyze_uo_items_performance.py` - UO Items database performance analysis

**Usage**: Performance optimization, development metrics, system analysis

### Project Management (`project-management/`)
**Purpose**: Project planning, automation, and workflow management

**Tools**:
- `generate_prd.ps1` - Product Requirements Document generation
- `suggest_assignment.ps1` - Intelligent task assignment recommendations
- `intelligent_routing.ps1` - Smart workflow routing and automation
- `generate_dashboard.ps1` - Project status dashboard generation
- `predictive_dashboard.ps1` - Predictive analytics dashboard
- `batch_operations.ps1` - Bulk project management operations
- `full_automation_suite.ps1` - Complete automation workflow orchestration

**Usage**: Project planning, workflow automation, team coordination

---

## 🚀 Getting Started

### Prerequisites
- **PowerShell 5.1+** (for .ps1 scripts)
- **Python 3.8+** (for .py analysis tools)
- **GitHub CLI** (for GitHub automation tools)
- **Git** (for repository operations)

### Authentication Setup
1. **GitHub Authentication**: Run `github-automation/github_auth_helper.ps1`
2. **Configure Access**: Set up GitHub Personal Access Token or GitHub CLI
3. **Test Connection**: Use `github-automation/test_mock_github.ps1` for validation

### Common Workflows

#### GitHub Issues Management
```powershell
# Set up repository labels
.\dev-tools\github-automation\setup_labels.ps1

# Create issues from backlog
.\dev-tools\github-automation\create_issues.ps1

# Manage existing issues
.\dev-tools\github-automation\manage_issues.ps1
```

#### Performance Analysis
```powershell
# Profile system performance
.\dev-tools\analysis\profile_performance.ps1

# Analyze development cycles
.\dev-tools\analysis\analyze_cycle_times.ps1
```

#### Project Management
```powershell
# Generate project dashboard
.\dev-tools\project-management\generate_dashboard.ps1

# Run full automation suite
.\dev-tools\project-management\full_automation_suite.ps1
```

---

## 🎯 Tool Integration

### GitHub Issues Workflow
1. **Setup**: Configure labels and authentication
2. **Creation**: Generate issues from backlog ideas
3. **Management**: Assign, update, and track progress
4. **Analysis**: Review cycle times and completion metrics

### Development Workflow
1. **Planning**: Use PRD generation and assignment tools
2. **Analysis**: Monitor performance and development metrics
3. **Automation**: Leverage full automation suite for routine tasks
4. **Reporting**: Generate dashboards and status reports

### Quality Assurance
- **Testing**: Mock APIs and test utilities for validation
- **Monitoring**: Performance profiling and analysis tools
- **Metrics**: Cycle time and planning accuracy tracking
- **Optimization**: Data-driven improvement recommendations

---

## 📊 Tool Maintenance

### Update Schedule
- **Weekly**: Review automation effectiveness and adjust parameters
- **Monthly**: Update tool configurations based on workflow changes
- **Quarterly**: Evaluate new tool needs and retire obsolete utilities

### Best Practices
- **Version Control**: All tools are tracked in git for change management
- **Documentation**: Each tool includes usage documentation and examples
- **Testing**: Mock utilities ensure reliable operation before production use
- **Security**: Authentication helpers manage secure access to external services

---

## 🤝 Contributing to Development Tools

### Adding New Tools
1. **Identify Need**: Document specific automation or analysis requirement
2. **Choose Category**: Place in appropriate subdirectory (github-automation, analysis, project-management)
3. **Follow Standards**: Use established patterns for naming, documentation, and error handling
4. **Include Tests**: Add mock or test utilities where applicable
5. **Update Documentation**: Add tool description to this README

### Tool Standards
- **PowerShell**: Use approved verbs, proper error handling, parameter validation
- **Python**: Follow PEP 8, include type hints, comprehensive docstrings
- **Documentation**: Include purpose, usage examples, and configuration options
- **Security**: Implement secure authentication and API access patterns

---

**Note**: These tools are for development automation and project management. They are not part of the core DexBot runtime system and should not be included in production distributions.

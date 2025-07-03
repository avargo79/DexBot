# DexBot Development Guide

**Purpose**: Complete guide for developing features and contributing to the DexBot project.

---

## Quick Start

### Automated Feature Preparation

Instead of manual setup, use the automated scripts:

```powershell
# Windows PowerShell (Interactive)
.\scripts\prepare_feature.ps1 feature-name

# Windows PowerShell (Non-Interactive) 
.\scripts\prepare_feature.ps1 feature-name -NonInteractive

# Linux/macOS
./scripts/prepare_feature.sh feature-name [--non-interactive]
```

**Script Options**:
- `-SkipGitUpdate` / `--skip-git`: Skip Git repository update
- `-SkipCleanup` / `--skip-cleanup`: Skip cleaning temporary files
- `-SkipValidation` / `--skip-validation`: Skip validation tests
- `-Help` / `--help`: Display help information

---

## Development Workflow

### 1. Workspace Preparation

#### Git Repository Cleanup
```powershell
# Switch to main and update
git checkout main
git fetch origin && git pull origin main

# Clean up merged branches
git branch --merged main | grep -v "^\* main" | xargs git branch -d
git remote prune origin
```

#### Code Workspace Cleanup
```powershell
# Clean temporary files
Get-ChildItem -Path "reports/*" -Exclude ".gitkeep" | Remove-Item -Force -Recurse

# Clean build artifacts  
Get-ChildItem -Path "dist/*" -Exclude ".gitkeep" | Remove-Item -Force -Recurse

# Clean Python cache
Get-ChildItem -Path "." -Include "__pycache__", "*.pyc", "*.pyo" -Recurse | Remove-Item -Force -Recurse
```

#### Environment Validation
```powershell
python -m invoke validate  # Check system integrity
python -m invoke test      # Run test suite
python -m invoke build     # Verify build process
```

### 2. Feature Development Process

#### Branch Creation and Naming
```powershell
# Create feature branch
git checkout -b feature/FR-###-short-description

# Examples:
# feature/FR-127-uo-item-database-integration
# hotfix/TECH-001-memory-leak-fix
# bugfix/BUG-045-looting-range-calculation
```

#### Implementation Steps
1. **Review PRD**: Read the full PRD document (e.g., `docs/prds/FR-###_System_Name.md`)
2. **Create Configuration**: Add necessary config files in `config/`
3. **Implement Core System**: Create main system files in `src/systems/`
4. **Write Tests**: Follow 3-case testing pattern (pass/fail/edge)
5. **Add UI Components**: Create GUMP interfaces if needed in `src/ui/`
6. **Update Documentation**: Update relevant docs and README

#### Development Commands
```powershell
# Regular development cycle
python -m invoke validate    # Check for issues
python -m invoke test       # Run tests
python -m invoke build      # Create bundled output

# Fast development cycle
python -m invoke quick      # Build + test in one step

# Monitor changes during development
python -m invoke watch      # Watch for file changes
```

### 3. Version Management

#### Central Version System
- **Single source**: `version.txt` contains version, name, and date
- **Format**: `VERSION|VERSION_NAME|BUILD_DATE`
- **Example**: `3.2.0|UO Database Integration & Performance Optimization|2025-07-01`

#### Semantic Versioning (MAJOR.MINOR.PATCH)
- **MAJOR**: Breaking changes, major rewrites
- **MINOR**: New features, significant improvements  
- **PATCH**: Bug fixes, small improvements

#### Version Update Process
```powershell
# Update version.txt for new feature
# Example: 3.2.0 → 3.3.0 for new feature
echo "3.3.0|Inventory Management System|$(Get-Date -Format 'yyyy-MM-dd')" > version.txt
```

### 4. Pre-Commit Validation

**Always validate before committing**:
```powershell
python -m invoke validate    # Check system integrity  
python -m invoke test       # Ensure tests pass (96%+ expected)
python -m invoke build      # Verify bundled output
```

**Never commit broken builds** - always ensure:
- Code compiles without errors
- Core tests pass
- Bundled output builds successfully

### 5. Pull Request Process

#### Before Creating PR
- [ ] All validation checks pass
- [ ] Tests have high pass rate (96%+)
- [ ] Documentation updated
- [ ] Feature aligns with PRD requirements
- [ ] Version updated if needed

#### PR Template Compliance
- Follow the established PR template
- Include links to related GitHub Issues
- Reference relevant PRD documents
- Ensure all CI checks pass

---

## AI-Assisted Development

### AI Assistant Configuration System

DexBot includes a comprehensive YAML configuration system in the `.copilot/` directory that provides structured context for AI assistants like GitHub Copilot. This system enables more effective and consistent AI assistance throughout the development process.

#### Configuration Files Overview

- **`.copilot/ai-config.yaml`** - Master configuration with project summary and workflows
- **`.copilot/project-context.yaml`** - Detailed development environment and architecture context
- **`.copilot/development-tasks.yaml`** - Task-specific templates and guidance
- **`.copilot/razorenhanced-api.yaml`** - RazorEnhanced API reference and usage patterns

#### Benefits of the Configuration System

**For AI Assistants:**
- Automatic understanding of project constraints and patterns
- Pre-configured templates for common development tasks
- Built-in error handling and testing strategies
- RazorEnhanced-specific API usage guidance

**For Developers:**
- Consistent AI-generated code that follows project standards
- Faster development with pre-configured templates
- Reduced errors through established patterns
- Better integration with existing systems

#### How to Use

When requesting AI assistance, the configuration system automatically provides:
- Proper RazorEnhanced imports and constraints
- Comprehensive error handling patterns
- 3-case testing templates
- Performance optimization strategies
- Integration with existing configuration management

**Example**: When asking "Create a new healing optimization system", the AI will automatically apply DexBot patterns, use proper imports, include error handling, and follow the established architecture.

### GitHub Copilot Integration

DexBot includes comprehensive GitHub Copilot instructions for optimal AI assistance:

1. **Install GitHub Copilot** extension in VS Code
2. **Open DexBot project** - Copilot automatically loads project context
3. **Start coding** - AI understands architecture, constraints, and patterns

---

## Testing Standards

### 3-Case Testing Pattern
For all new functionality, implement:
1. **Pass Case**: Normal operation succeeds
2. **Fail Case**: Expected failure handled gracefully  
3. **Edge Case**: Boundary conditions and unexpected inputs

### Test Categories
- **Unit Tests**: Individual function/method testing
- **Integration Tests**: System interaction testing
- **Performance Tests**: Long-running operation validation
- **API Tests**: RazorEnhanced API interaction testing

### Test Execution
```powershell
# Run all tests
python -m invoke test

# Run with verbose output
python -m invoke test --verbose

# Run specific test patterns
python -m invoke test --pattern "auto_heal"
```

---

## Code Quality Standards

### Documentation Requirements
- **Comprehensive docstrings** with Args, Returns, Raises, and Example sections
- **Type hints** when beneficial for understanding
- **Inline comments** for complex RazorEnhanced API usage
- **README updates** for new features

### Error Handling Best Practices
```python
# Specific exception handling
try:
    result = risky_operation()
except SpecificError as e:
    Logger.error(f"Operation failed: {e}")
    return default_value
except Exception as e:
    Logger.error(f"Unexpected error: {e}")
    raise

# Input validation
def process_data(data: Optional[List[str]]) -> bool:
    if not data:
        raise ValueError("Data cannot be empty")
    
    if not isinstance(data, list):
        raise TypeError("Data must be a list")
    
    return True
```

### Performance Considerations
- **Memory Management**: Use appropriate data structures for long sessions
- **API Efficiency**: Cache results when possible to reduce API calls
- **Resource Cleanup**: Properly dispose of resources and clear caches
- **Background Processing**: Prefer non-blocking operations where possible

---

## Troubleshooting

### Common Development Issues

#### Build Failures
- Run `python -m invoke validate` to check for missing functions
- Verify all imports are available in RazorEnhanced environment
- Check for syntax errors with proper Python linting

#### Test Failures  
- Review test output for specific failure patterns
- Ensure test environment matches development environment
- Validate that all required test data and mocks are available

#### Performance Issues
- Profile memory usage during development
- Monitor API call frequency and optimize caching
- Test with long-running sessions to identify memory leaks

#### AI Integration Issues
- Verify GitHub Copilot extension is installed and activated
- Check that project-specific instructions are loading
- Try specific DexBot prompts to test AI understanding

---

## Best Practices Summary

### Development Workflow
- Always start with automated feature preparation scripts
- Follow the standardized branch naming convention
- Validate frequently during development with invoke tasks
- Never commit broken builds

### Code Quality
- Write comprehensive tests using the 3-case pattern
- Include detailed docstrings and type hints
- Handle RazorEnhanced API errors gracefully
- Optimize for long-running bot sessions

### Collaboration
- Reference GitHub Issues and PRDs in commits
- Follow the established PR template and process
- Keep documentation current with code changes
- Use AI assistance effectively with project-specific prompts

---

## Related Documentation

### Essential Reading
- **[Usage Examples](USAGE_EXAMPLES.md)** - Practical code examples and patterns
- **[GitHub Workflow](GITHUB_WORKFLOW.md)** - GitHub Issues workflow and automation  
- **[Project Status](PROJECT_STATUS.md)** - Current development status
- **[Features](FEATURES.md)** - System capabilities and documentation

### Specialized References
- **[Product Requirements](prds/README.md)** - Detailed feature specifications
- **[Research Concepts](RESEARCH_AND_FUTURE_CONCEPTS.md)** - Long-term research ideas
- **[Project Overview](OVERVIEW.md)** - High-level project information

---

*This guide provides the complete development workflow for contributing to DexBot. For specific feature requirements, refer to the relevant PRD documents in `docs/prds/`.*

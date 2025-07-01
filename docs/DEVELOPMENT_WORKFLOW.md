# DexBot Development Workflow - Version Management

## Overview
DexBot now uses a centralized version management system with `version.txt` as the single source of truth for version information. This eliminates the need to update version numbers in multiple files and provides a clear development workflow.

## Version Management System

### 1. Central Version File: `version.txt`
```
3.2.0|UO Database Integration & Performance Optimization|2025-07-01
```

**Format**: `VERSION|VERSION_NAME|BUILD_DATE`

### 2. Automated Version Reading
- **Build System** (`tasks.py`): Reads version.txt for bundle headers
- **Runtime Code** (`src/core/bot_config.py`): Reads version.txt for runtime version info
- **Git Branch**: Automatically included in build for development context

### 3. Version Information Display
The bundled DexBot.py now includes:
```python
"""
Version: 3.2.0 - UO Database Integration & Performance Optimization
Build Date: 2025-07-01
Branch: feature/uo-item-database-optimization
"""
```

## Recommended Development Workflow

### Branch Naming Convention
```
feature/FR-###-short-description    # Feature Requests
hotfix/TECH-###-short-description   # Technical issues
bugfix/BUG-###-short-description    # Bug fixes
```

**Examples**:
- `feature/FR-127-uo-item-database-integration`
- `hotfix/TECH-001-memory-leak-fix`
- `bugfix/BUG-045-looting-range-calculation`

### Version Numbering Strategy

#### Semantic Versioning: `MAJOR.MINOR.PATCH`

**MAJOR** (x.0.0): Breaking changes, major rewrites
- New bot architecture
- API changes that break existing configs
- Complete system redesigns

**MINOR** (x.Y.0): New features, significant improvements
- New bot systems (combat, looting, crafting)
- Database integrations
- Performance optimizations
- New configuration options

**PATCH** (x.y.Z): Bug fixes, small improvements
- Bug fixes
- Performance tweaks
- Documentation updates
- Configuration adjustments

### Development Process

#### 1. Start New Feature/Fix
```bash
# Create branch with FR/TECH/BUG number
git checkout -b feature/FR-128-inventory-management

# Update version.txt for the new feature
# Increment MINOR version: 3.2.0 → 3.3.0
```

#### 2. Update version.txt
```
3.3.0|Inventory Management System|2025-07-01

# Version History:
# 3.3.0 - Inventory Management System (2025-07-01)
# 3.2.0 - UO Database Integration & Performance Optimization (2025-07-01)
# 3.1.1 - Ignore List Optimization (2025-06-30)
```

#### 3. Development & Testing
- Make changes to source files
- Build using `python -m invoke build`
- Version automatically pulled from version.txt
- Branch name automatically included in build

#### 4. Merge to Main
```bash
# When ready for production
git checkout main
git merge feature/FR-128-inventory-management
git tag v3.3.0  # Tag the release
git push origin main --tags
```

### Backlog Integration

#### Product Requirements Documents (PRDs)
- **Location**: `docs/prds/FR-###_Feature_Name.md`
- **Version**: Should match the version.txt when implementing
- **Status**: Track implementation status in PRD

#### Example PRD Workflow
1. **Create PRD**: `docs/prds/FR-128_Inventory_Management.md`
2. **Create Branch**: `feature/FR-128-inventory-management`
3. **Update Version**: `3.3.0|Inventory Management System|2025-07-01`
4. **Develop**: Implement the feature
5. **Build & Test**: Automated version management
6. **Merge**: Tag with version number

## Benefits of This System

### ✅ Single Source of Truth
- No more updating version in multiple files
- Consistent version across build and runtime
- Eliminates version sync issues

### ✅ Automated Workflow
- Build system automatically reads version
- Runtime code automatically gets correct version
- Branch information included for development context

### ✅ Clear Development Flow
- Branch names linked to backlog items
- Version increments match feature scope
- Easy to track what's in each release

### ✅ Production Ready
- Clean version management for releases
- Easy to identify what's in production
- Clear rollback points with git tags

## Current State

**Active Branch**: `feature/uo-item-database-optimization`
**Current Version**: `3.2.0 - UO Database Integration & Performance Optimization`
**Build Date**: `2025-07-01`
**Status**: Ready for merge to main and version tag

## Next Steps

1. **Complete Current Feature**: Finish any remaining work on current branch
2. **Merge to Main**: Merge the current feature branch
3. **Tag Release**: `git tag v3.2.0`
4. **New Features**: Follow the FR-### branch naming convention
5. **Update Backlog**: Ensure PRDs match version numbers

This system provides clear traceability from backlog items through development to production releases.

# DexBot Feature Development Preparation Guide

**Purpose**: This guide outlines the standard process for preparing your workspace before starting work on a new feature in the DexBot project.

## Quick Start

Instead of manually performing all the steps in this guide, you can use the automated feature preparation scripts:

```powershell
# Windows PowerShell (Interactive)
.\scripts\prepare_feature.ps1 feature-name

# Windows PowerShell (Non-Interactive)
.\scripts\prepare_feature.ps1 feature-name -NonInteractive

# Linux/macOS (Interactive)
./scripts/prepare_feature.sh feature-name

# Linux/macOS (Non-Interactive)
./scripts/prepare_feature.sh feature-name --non-interactive
```

Additional script options:
- `-SkipGitUpdate` / `--skip-git`: Skip Git repository update and branch management
- `-SkipCleanup` / `--skip-cleanup`: Skip cleaning temporary files and build artifacts
- `-SkipValidation` / `--skip-validation`: Skip running validation and tests
- `-Help` / `--help`: Display help information

The interactive mode includes sensible defaults for all Y/N prompts:
- Default values are indicated with capital letters (e.g., `[Y/n]` or `[y/N]`)
- Pressing Enter accepts the default value
- Explicit "y" or "n" input works as before
- Non-interactive mode always uses the defaults

These scripts will automate the entire workspace preparation process, create a feature branch, and set up an initial planning document.

## 1. Workspace Preparation Checklist

### 1.1 Git Repository Cleanup

```powershell
# Step 1: Switch to main branch
git checkout main

# Step 2: Update main branch from remote
git fetch origin
git pull origin main

# Step 3: Check for and clean up local feature branches
git branch --merged main | grep -v "^\* main" | xargs git branch -d

# Step 4: Prune remote tracking branches that no longer exist on remote
git remote prune origin

# Step 5: List remaining branches (be aware of what branches still exist)
git branch -a
```

### 1.2 Code Workspace Cleanup

```powershell
# Step 1: Clean temporary files
Get-ChildItem -Path "reports/*" -Exclude ".gitkeep" | Remove-Item -Force -Recurse

# Step 2: Clean build artifacts
Get-ChildItem -Path "dist/*" -Exclude ".gitkeep" | Remove-Item -Force -Recurse

# Step 3: Clean Python cache files
Get-ChildItem -Path "." -Include "__pycache__", "*.pyc", "*.pyo" -Recurse | Remove-Item -Force -Recurse
```

### 1.3 Environment Validation

```powershell
# Step 1: Run validation tests to ensure clean environment
python -m invoke validate

# Step 2: Run tests to ensure all systems are functioning
python -m invoke test

# Step 3: Verify build process works
python -m invoke build
```

## 2. Starting a New Feature

### 2.1 Create Feature Branch

```powershell
# Create and switch to a new feature branch
# Use the naming convention: feature/[feature-name]
git checkout -b feature/buff-management-system
```

### 2.2 Set Up Configuration

1. **Review PRD Document**:
   - Read the full PRD for the feature (e.g., `docs/prds/FR-084_Buff_Management_System.md`)
   - Note key requirements and acceptance criteria

2. **Create Default Configuration**:
   - Create default configuration JSON file in `config/` directory
   - Update `ConfigManager` to handle the new configuration

### 2.3 Implementation Planning

1. **Create Feature Implementation Plan**:
   ```powershell
   # Create a temporary planning document
   New-Item -Path "reports/FEATURE_IMPLEMENTATION_PLAN.md" -Force
   ```

2. **Define Module Structure**:
   - Identify required new files
   - Plan integration points with existing systems
   - Document API design

## 3. Development Workflow

### 3.1 Incremental Development

1. **Implement Core Functionality First**:
   - Start with the system's core functionality
   - Ensure it can be tested independently

2. **Regular Testing**:
   ```powershell
   # Run tests frequently
   python -m invoke test
   ```

3. **Commit Frequently**:
   ```powershell
   # Make small, focused commits
   git add [files]
   git commit -m "feat: implement [specific feature component]"
   ```

### 3.2 Integration Testing

1. **Build Bundled Script**:
   ```powershell
   python -m invoke build
   ```

2. **Test with RazorEnhanced**:
   ```powershell
   # Run with log capture
   python -m invoke run:log
   ```

## 4. Pre-PR Checklist

Before creating a Pull Request:

1. **Full Test Suite**:
   ```powershell
   python -m invoke test:all
   ```

2. **Code Quality Checks**:
   ```powershell
   python -m invoke lint
   ```

3. **Documentation**:
   - Update relevant documentation
   - Add usage examples

4. **Clean Commit History**:
   ```powershell
   # Optional: Squash commits if there are many small ones
   git rebase -i origin/main
   ```

5. **Final Build Verification**:
   ```powershell
   python -m invoke build
   ```

## 5. Handling Multiple Features

If you need to work on multiple features simultaneously:

1. **Complete Current Feature**:
   - Whenever possible, complete one feature before starting another
   - Commit or stash changes before switching

2. **Switching Between Features**:
   ```powershell
   # Save current work
   git add .
   git commit -m "wip: save current progress on [feature]"
   
   # Switch to another feature branch
   git checkout feature/other-feature
   ```

3. **Creating Feature from Another Feature**:
   - Avoid branching from feature branches
   - Always branch new features from main

## 6. Emergency Procedures

### 6.1 Saving Work in Progress

```powershell
# Create a WIP commit that can be amended later
git add .
git commit -m "wip: save current state before emergency"

# Create a patch file as backup
git format-patch HEAD~1 -o reports/patches
```

### 6.2 Recovering from Failed State

```powershell
# Discard all changes and reset to last commit
git reset --hard

# Pull latest changes
git pull origin main

# Recreate your branch
git checkout -b feature/buff-management-system
```

## 7. Tips for Efficient Feature Development

1. **Read the PRD thoroughly** before starting implementation
2. **Test-driven development** - write tests first when possible
3. **Keep the scope focused** - avoid feature creep
4. **Maintain good documentation** as you develop
5. **Regular commits** with descriptive messages
6. **Clean up temporary files** before committing

---

**Remember**: Always follow the DexBot coding standards outlined in the project's documentation. All feature development should align with the project's architecture and patterns.

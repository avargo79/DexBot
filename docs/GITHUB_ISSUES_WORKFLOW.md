# GitHub Issues Project Management Workflow

**Last Updated**: July 1, 2025

## Overview

This document outlines the GitHub Issues-based project management workflow for DexBot. This system provides better collaboration, tracking, and visibility into project progress.

## Issue Types and Labels

### Issue Types
- **Enhancement**: New features and improvements
- **Bug**: Bug reports and fixes
- **Documentation**: Documentation updates and improvements
- **Testing**: Test-related tasks
- **Maintenance**: Code cleanup, refactoring, organization

### Priority Labels
- `priority:critical` - Blocking issues, system failures
- `priority:high` - Important features, significant bugs
- `priority:medium` - Standard development tasks
- `priority:low` - Nice-to-have improvements

### Component Labels
- `component:auto-heal` - Auto heal system
- `component:combat` - Combat system
- `component:looting` - Looting system
- `component:ui` - User interface (GUMPs)
- `component:config` - Configuration management
- `component:core` - Core systems and utilities
- `component:build` - Build system and CI/CD
- `component:docs` - Documentation

### Status Labels
- `status:proposed` - Items under consideration, not yet approved
- `status:planning` - Requirements gathering and planning
- `status:in-progress` - Currently being worked on
- `status:review` - Ready for code review
- `status:testing` - Being tested
- `status:blocked` - Cannot proceed due to dependencies

## Issue Creation Workflow

### 0. Proposed Items (New!)
```bash
# Create a proposed feature for discussion
gh issue create --title "[PROPOSED] Advanced Combat AI System" \
  --body "## Proposal
This is a proposal for an advanced combat AI system that would enhance target selection and combat tactics.

## Discussion Points
- Is this aligned with project goals?
- What would be the implementation complexity?
- Should this be prioritized over other features?

## Next Steps
If approved, this will be converted to a proper feature issue with full requirements." \
  --label "status:proposed,enhancement,priority:medium"
```

### 1. Feature Issues (from PRD)
```bash
# Create a feature issue from PRD
gh issue create --title "FR-084: Implement Buff Management System" \
  --body-file docs/prds/FR-084_Buff_Management_System.md \
  --label "enhancement,priority:high,component:core"
```

### 2. Bug Reports
```bash
# Create a bug report
gh issue create --title "Memory leak in long-running looting sessions" \
  --body "## Description
Memory usage increases over time during extended looting sessions (12+ hours).

## Steps to Reproduce
1. Start DexBot with looting enabled
2. Run for 8+ hours
3. Monitor memory usage

## Expected Behavior
Memory usage should remain stable

## Environment
- RazorEnhanced version: [version]
- DexBot version: 3.2.0" \
  --label "bug,priority:high,component:looting"
```

### 3. Maintenance Tasks
```bash
# Create a maintenance task
gh issue create --title "Refactor UO Items database loading for better performance" \
  --body "Optimize the UO Items database loading to reduce startup time and memory usage." \
  --label "maintenance,priority:medium,component:core"
```

## Development Workflow Integration

### 1. Branch Creation from Issue
```bash
# Create a branch for an issue
gh issue develop 123 --checkout
# This creates: feature/123-implement-buff-management-system
```

### 2. Linking Commits to Issues
```bash
# Commit with issue reference
git commit -m "feat: add buff detection logic

Implements core buff detection functionality for issue #123.
- Add Buffs API integration
- Create buff state management
- Add configuration options

Closes #123"
```

### 3. Pull Request Creation
```bash
# Create PR that references issue
gh pr create --title "Implement Buff Management System" \
  --body "Implements FR-084 Buff Management System.

## Changes
- Core buff detection and management
- Configuration integration
- Comprehensive testing
- Documentation updates

## Testing
- [x] Unit tests pass
- [x] Integration tests pass
- [x] Manual testing in RazorEnhanced

Closes #123"
```

## Issue Triage Workflow

### Manual Triage Process
DexBot uses a manual triage process to ensure quality control and strategic alignment:

1. **New Issue Submission**: Users create issues without status labels
2. **Review Queue**: Maintainers review unlabeled issues for merit
3. **Triage Decision**: 
   - **Has Merit**: Label as `status:proposed` for PRD development
   - **No Merit**: Close with explanation
4. **PRD Development**: Create detailed requirements in issue comments
5. **Final Approval**: Move to `status:planning` with FR-### number assignment

### Triage Commands
```bash
# View issues needing triage and proposed items ready for PRD work
.\scripts\manage_issues.ps1 -Action review-queue

# Mark an issue as having merit (moves to proposed status)
.\scripts\manage_issues.ps1 -Action status -IssueNumber 123 -Status proposed

# View issue details for evaluation
gh issue view 123

# Close invalid issues
gh issue close 123 --comment "Reason for closing"
```

### PRD Development Process
1. **Research**: Analyze requirements and technical feasibility
2. **Draft PRD**: Create detailed Product Requirements Document
3. **Post PRD**: Add PRD content as issue comment, tag original author
4. **Iterate**: Refine based on feedback and discussion
5. **Promote**: When approved, use promote action to create new FR issue

```bash
# Add PRD content to issue
gh issue comment 123 --body "## Product Requirements Document
### Feature Overview
[Detailed requirements here...]

@original-author Please review this PRD and let us know your thoughts."

# After approval, promote to formal Feature Request (creates new FR issue)
.\scripts\manage_issues.ps1 -Action promote -IssueNumber 123

# Or specify a custom FR number
.\scripts\manage_issues.ps1 -Action promote -IssueNumber 123 -FRNumber FR-086
```

**What the promote action does:**
- Auto-determines next available FR number (if not specified)
- Creates new FR issue with proper title and PRD content
- Cross-links original request and new FR issue
- Subscribes original requester to FR issue for updates
- Closes original request with friendly message
- Sets up FR issue for development planning

## Issue Management Commands

### List Issues
```bash
# View all open issues
gh issue list

# View issues by label
gh issue list --label "priority:high"
gh issue list --label "component:looting"

# View your assigned issues
gh issue list --assignee @me
```

### Issue Status Updates
```bash
# Promote proposed item to planning
gh issue edit 123 --remove-label "status:proposed"
gh issue edit 123 --add-label "status:planning"

# Assign issue to yourself
gh issue edit 123 --add-assignee @me

# Update labels
gh issue edit 123 --add-label "status:in-progress"
gh issue edit 123 --remove-label "status:planning"

# Comment on issue
gh issue comment 123 --body "Starting work on this feature. Will begin with core implementation."
```

### Closing Issues
```bash
# Close with comment
gh issue close 123 --comment "Completed in PR #45. Buff management system is now fully implemented and tested."
```

## Project Planning with Issues

### 1. Milestone Creation
```bash
# Create milestone for next release
gh api repos/:owner/:repo/milestones \
  --method POST \
  --field title="v3.3.0 - Buff Management" \
  --field description="Release focusing on buff management and performance improvements" \
  --field due_on="2025-08-01T00:00:00Z"
```

### 2. Issue Assignment to Milestones
```bash
# Assign issue to milestone
gh issue edit 123 --milestone "v3.3.0 - Buff Management"
```

### 3. Project Boards (if using GitHub Projects)
```bash
# List projects
gh project list

# Add issue to project
gh project item-add [project-number] --url [issue-url]
```

## Automated Issue Creation Scripts

### Script: Create Issues from Backlog
Create `scripts/create_issues_from_backlog.ps1`:

```powershell
# PowerShell script to create GitHub issues from backlog items
param(
    [string]$BacklogFile = "docs/backlog/CURRENT_DEVELOPMENT_PRIORITIES.md",
    [switch]$DryRun = $false
)

# Parse backlog and create issues
# Implementation would read backlog file and create issues
```

### Script: Update Issue Status from Git
Create `scripts/update_issues_from_commits.ps1`:

```powershell
# Automatically update issues based on commit messages
# Looks for patterns like "refs #123", "closes #123", etc.
```

## Integration with Development Workflow

### 1. Pre-Commit Hook Integration
Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
# Check if commit message references an issue
if ! grep -q "#[0-9]" "$1"; then
    echo "Warning: Commit message should reference an issue number (#123)"
fi
```

### 2. Feature Development Process
1. Create GitHub issue for feature
2. Use `gh issue develop` to create branch
3. Implement feature following standard workflow
4. Reference issue in all commits
5. Create PR that closes the issue
6. Use issue for discussion and tracking

### 3. Bug Tracking Process
1. Report bug as GitHub issue
2. Triage and label appropriately
3. Assign to milestone if critical
4. Create branch and implement fix
5. Test thoroughly and update issue
6. Close with PR merge

## Issue Templates

GitHub issue templates can be created in `.github/ISSUE_TEMPLATE/`:

### Feature Request Template
```yaml
name: Feature Request
about: Suggest a new feature for DexBot
title: '[FEATURE] '
labels: enhancement
assignees: ''

body:
  - type: markdown
    attributes:
      value: |
        Thanks for suggesting a feature for DexBot!
  - type: textarea
    id: description
    attributes:
      label: Feature Description
      description: What feature would you like to see added?
    validations:
      required: true
  - type: textarea
    id: use-case
    attributes:
      label: Use Case
      description: How would this feature be used in gameplay?
    validations:
      required: true
```

### Bug Report Template
```yaml
name: Bug Report
about: Report a bug in DexBot
title: '[BUG] '
labels: bug
assignees: ''

body:
  - type: textarea
    id: description
    attributes:
      label: Bug Description
      description: Clear description of the bug
    validations:
      required: true
  - type: textarea
    id: reproduction
    attributes:
      label: Steps to Reproduce
      description: How can this bug be reproduced?
    validations:
      required: true
```

## Best Practices

### Issue Creation
- Use clear, descriptive titles
- Include enough detail for implementation
- Reference related PRDs or documentation
- Add appropriate labels immediately
- Assign to milestones when applicable

### Issue Management
- Keep issues focused on single topics
- Use comments for progress updates
- Close issues promptly when complete
- Link related issues using keywords

### Integration with Development
- Always reference issues in commits
- Use conventional commit messages
- Create PRs that close issues
- Update issue status regularly

### Communication
- Use issue comments for technical discussion
- Tag team members when input needed
- Document decisions in issue comments
- Keep status current with labels

## Quick Reference

### Daily Workflow Commands
```bash
# Review issues needing attention
.\scripts\manage_issues.ps1 -Action review-queue

# Check your assigned work
.\scripts\manage_issues.ps1 -Action list -Mine

# Project overview
.\scripts\manage_issues.ps1 -Action summary

# Start work on approved feature
.\scripts\manage_issues.ps1 -Action develop -IssueNumber 123
```

### Triage Workflow
```bash
# 1. Review new submissions
.\scripts\manage_issues.ps1 -Action review-queue

# 2. Mark promising ones as proposed  
.\scripts\manage_issues.ps1 -Action status -IssueNumber 123 -Status proposed

# 3. Develop PRD in issue comments
gh issue comment 123 --body "## PRD Content..."

# 4. After approval, promote to formal Feature Request
.\scripts\manage_issues.ps1 -Action promote -IssueNumber 123

# 5. Assign component and priority to new FR issue
gh issue edit <new-fr-number> --add-label "component:looting" --add-label "priority:medium"
```

### Feature Request Management
```bash
# Promote user request to formal FR (auto-determines FR number)
.\scripts\manage_issues.ps1 -Action promote -IssueNumber 123

# Promote with specific FR number
.\scripts\manage_issues.ps1 -Action promote -IssueNumber 123 -FRNumber FR-086

# Update FR status during development
.\scripts\manage_issues.ps1 -Action status -IssueNumber 456 -Status in-progress

# Mark FR as complete
.\scripts\manage_issues.ps1 -Action status -IssueNumber 456 -Status testing
```

## Next Steps

1. **Setup Issue Labels**: Create the label system in GitHub
2. **Create Issue Templates**: Add templates to `.github/ISSUE_TEMPLATE/`
3. **Migrate Current Backlog**: Convert current backlog items to GitHub issues
4. **Setup Milestones**: Create milestones for upcoming releases
5. **Team Training**: Ensure all contributors understand the workflow

This GitHub Issues workflow will provide better project visibility, collaboration, and tracking for DexBot development.

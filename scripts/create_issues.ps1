#!/usr/bin/env powershell
<#
.SYNOPSIS
    Helper script for creating GitHub issues from DexBot backlog items

.DESCRIPTION
    This script reads the current development priorities and helps create
    GitHub issues with appropriate labels and formatting.

.PARAMETER BacklogFile
    Path to the backlog file to process

.PARAMETER DryRun
    If specified, shows what would be created without actually creating issues

.PARAMETER Interactive
    If specified, prompts for confirmation before creating each issue

.EXAMPLE
    .\create_issues.ps1 -Interactive
    .\create_issues.ps1 -DryRun
#>

param(
    [string]$BacklogFile = "docs\backlog\PRODUCT_BACKLOG.md",
    [switch]$DryRun = $false,
    [switch]$Interactive = $false
)

# Color output functions
function Write-Success { param($Message) Write-Host $Message -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host $Message -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host $Message -ForegroundColor Red }
function Write-Info { param($Message) Write-Host $Message -ForegroundColor Cyan }

Write-Info "DexBot GitHub Issues Creator"
Write-Info "============================"

# Check if gh CLI is available
try {
    $ghVersion = gh --version
    Write-Success "GitHub CLI detected: $($ghVersion[0])"
} catch {
    Write-Error "GitHub CLI not found. Please install GitHub CLI first."
    exit 1
}

# Check if we're in a git repository
try {
    $repoInfo = gh repo view --json name,owner | ConvertFrom-Json
    Write-Success "Repository: $($repoInfo.owner.login)/$($repoInfo.name)"
} catch {
    Write-Error "Not in a GitHub repository or not authenticated."
    exit 1
}

# Check if backlog file exists
if (-not (Test-Path $BacklogFile)) {
    Write-Error "Backlog file not found: $BacklogFile"
    exit 1
}

Write-Info "Reading backlog file: $BacklogFile"

# Feature definitions for quick issue creation
$FeatureIssues = @(
    @{
        Title = "FR-084: Implement Buff Management System"
        Body = @"
## Feature Overview
Implement a comprehensive buff management system to monitor and maintain character buffs during gameplay.

## Requirements
- Detect current active buffs
- Monitor buff expiration times
- Automatic buff renewal when needed
- Configuration for buff priorities
- Integration with existing systems

## Acceptance Criteria
- [ ] Buff detection functionality
- [ ] Buff expiration monitoring
- [ ] Automatic renewal system
- [ ] Configuration integration
- [ ] Comprehensive testing
- [ ] Documentation updates

## Related PRD
See docs/prds/FR-084_Buff_Management_System.md for detailed requirements.

## Priority
High - This is a critical gameplay enhancement that improves character survivability and effectiveness.
"@
        Labels = @("enhancement", "priority:high", "component:core")
    },
    @{
        Title = "FR-085: Implement Inventory Management System"
        Body = @"
## Feature Overview
Implement an intelligent inventory management system to optimize bag space and item organization.

## Requirements
- Real-time inventory monitoring
- Automatic item sorting and organization
- Configurable item priority system
- Integration with looting system
- Bag space optimization

## Acceptance Criteria
- [ ] Inventory monitoring functionality
- [ ] Item sorting algorithms
- [ ] Priority-based organization
- [ ] Looting system integration
- [ ] Configuration options
- [ ] Testing and validation

## Related PRD
See docs/prds/FR-085_Inventory_Management_System.md for detailed requirements.

## Priority
Medium - Important for long-term gameplay efficiency.
"@
        Labels = @("enhancement", "priority:medium", "component:core")
    }
)

# Bug issues for known problems
$BugIssues = @(
    @{
        Title = "Memory leak in long-running looting sessions"
        Body = @"
## Bug Description
Memory usage increases continuously during extended looting sessions, eventually causing performance degradation.

## Steps to Reproduce
1. Start DexBot with looting system enabled
2. Run for 8+ hours in active looting area
3. Monitor memory usage over time
4. Observe gradual increase in memory consumption

## Expected Behavior
Memory usage should remain stable throughout extended sessions.

## Actual Behavior
Memory usage increases continuously, eventually impacting system performance.

## Environment
- DexBot version: 3.2.0
- RazorEnhanced version: Latest
- Session duration: 12+ hours
- System: Windows 10/11

## Impact
High - Affects long-term stability and user experience.

## Potential Causes
- Unclosed object references in looting system
- Event handler accumulation
- UO Items database caching issues
"@
        Labels = @("bug", "priority:high", "component:looting")
    },
    @{
        Title = "Performance degradation during peak combat periods"
        Body = @"
## Bug Description
Combat system performance degrades significantly during high-intensity combat scenarios with multiple targets.

## Steps to Reproduce
1. Enter area with 5+ hostile targets
2. Engage combat system
3. Monitor response times and system performance
4. Observe degradation over time

## Expected Behavior
Combat system should maintain consistent performance regardless of target count.

## Actual Behavior
Response times increase, target selection becomes sluggish, overall system performance degrades.

## Environment
- DexBot version: 3.2.0
- Combat scenarios: High-density mob areas
- Target count: 5+ simultaneous

## Impact
Medium - Affects combat effectiveness in challenging scenarios.

## Potential Causes
- Inefficient target scanning algorithms
- Lack of caching in mobile queries
- Excessive API calls during combat loops
"@
        Labels = @("bug", "priority:medium", "component:combat")
    }
)

# Maintenance issues
$MaintenanceIssues = @(
    @{
        Title = "Optimize UO Items database loading performance"
        Body = @"
## Task Description
Optimize the UO Items database loading process to reduce startup time and memory usage.

## Current Issues
- Database loading takes 3-5 seconds on startup
- High memory usage during initial load
- No caching mechanism for repeated queries

## Proposed Improvements
- Implement lazy loading for item data
- Add caching mechanism for frequently accessed items
- Optimize JSON parsing and data structures
- Consider database format alternatives

## Acceptance Criteria
- [ ] Reduce startup time by 50%
- [ ] Implement caching system
- [ ] Maintain data integrity
- [ ] Backward compatibility
- [ ] Performance benchmarking

## Impact
Medium - Improves user experience and system performance.
"@
        Labels = @("maintenance", "priority:medium", "component:core")
    }
)

# Function to create an issue
function Create-Issue {
    param($Issue)
    
    $labelString = $Issue.Labels -join ","
    
    if ($DryRun) {
        Write-Info "Would create issue:"
        Write-Host "  Title: $($Issue.Title)" -ForegroundColor White
        Write-Host "  Labels: $labelString" -ForegroundColor Gray
        Write-Host "  Body: $($Issue.Body.Substring(0, [Math]::Min(100, $Issue.Body.Length)))" -ForegroundColor Gray
        Write-Host ""
        return
    }
    
    if ($Interactive) {
        Write-Host "Create issue: $($Issue.Title)?" -ForegroundColor Yellow
        Write-Host "Labels: $labelString" -ForegroundColor Gray
        $response = Read-Host "Create this issue? (y/N)"
        if ($response.ToLower() -ne 'y') {
            Write-Warning "Skipped: $($Issue.Title)"
            return
        }
    }
    
    try {
        $result = gh issue create --title $Issue.Title --body $Issue.Body --label $labelString
        Write-Success "Created: $($Issue.Title)"
        Write-Host "  URL: $result" -ForegroundColor Gray
    } catch {
        Write-Error "Failed to create issue: $($Issue.Title)"
        Write-Error "Error: $($_.Exception.Message)"
    }
}

# Main execution
Write-Info "Creating issues for DexBot project..."
Write-Host ""

if ($DryRun) {
    Write-Warning "DRY RUN MODE - No issues will be created"
    Write-Host ""
}

# Create feature issues
Write-Info "Feature Issues:"
Write-Info "==============="
foreach ($issue in $FeatureIssues) {
    Create-Issue $issue
}

Write-Host ""

# Create bug issues
Write-Info "Bug Issues:"
Write-Info "==========="
foreach ($issue in $BugIssues) {
    Create-Issue $issue
}

Write-Host ""

# Create maintenance issues
Write-Info "Maintenance Issues:"
Write-Info "=================="
foreach ($issue in $MaintenanceIssues) {
    Create-Issue $issue
}

Write-Host ""

if (-not $DryRun) {
    Write-Success "Issue creation complete!"
    Write-Info "View all issues: gh issue list"
    Write-Info "View project board: gh repo view --web"
} else {
    Write-Info "Dry run complete. Use without -DryRun to create issues."
}

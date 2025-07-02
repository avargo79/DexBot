#!/usr/bin/env powershell
<#
.SYNOPSIS
    Helper script for managing GitHub issues workflow in DexBot

.DESCRIPTION
    Provides common issue management operations like status updates,
    assignment, labeling, and project board management.

.PARAMETER Action
    The action to perform: list, assign, status, comment, close

.PARAMETER IssueNumber
    The issue number to operate on

.PARAMETER Status
    The status to set (proposed, planning, ready-for-pickup, in-progress, testing, on-hold, blocked, rejected, implemented)

.PARAMETER Comment
    Comment to add to the issue

.EXAMPLE
    .\manage_issues.ps1 -Action list
    .\manage_issues.ps1 -Action assign -IssueNumber 123
    .\manage_issues.ps1 -Action status -IssueNumber 123 -Status "in-progress"
    .\manage_issues.ps1 -Action comment -IssueNumber 123 -Comment "Starting implementation"
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("list", "assign", "status", "comment", "close", "develop", "summary", "review-queue", "triage", "promote")]
    [string]$Action,
    
    [int]$IssueNumber,
    
    [ValidateSet("proposed", "planning", "ready-for-pickup", "in-progress", "testing", "on-hold", "blocked", "rejected", "implemented")]
    [string]$Status,
    
    [string]$Comment,
    
    [switch]$Mine = $false,
    
    [string]$Label,
    
    [ValidateSet("critical", "high", "medium", "low")]
    [string]$Priority,
    
    [string]$FRNumber
    
    # TODO: Implement PRD validation functionality
    # [switch]$PRDReady = $false  # Planned for Phase 1 Week 1 implementation
)

# Color output functions
function Write-Success { param($Message) Write-Host $Message -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host $Message -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host $Message -ForegroundColor Red }
function Write-Info { param($Message) Write-Host $Message -ForegroundColor Cyan }

Write-Info "DexBot GitHub Issues Manager"
Write-Info "============================"

# Check if gh CLI is available
try {
    $ghVersion = gh --version
    Write-Success "GitHub CLI detected: $($ghVersion[0])"
} catch {
    Write-Error "GitHub CLI not found. Please install GitHub CLI first."
    exit 1
}

# Validate parameters based on action
switch ($Action) {
    "assign" { 
        if (-not $IssueNumber) {
            Write-Error "IssueNumber is required for assign action"
            exit 1
        }
    }
    "status" { 
        if (-not $IssueNumber -or -not $Status) {
            Write-Error "IssueNumber and Status are required for status action"
            exit 1
        }
    }
    "comment" { 
        if (-not $IssueNumber -or -not $Comment) {
            Write-Error "IssueNumber and Comment are required for comment action"
            exit 1
        }
    }
    "close" { 
        if (-not $IssueNumber) {
            Write-Error "IssueNumber is required for close action"
            exit 1
        }
    }
    "develop" { 
        if (-not $IssueNumber) {
            Write-Error "IssueNumber is required for develop action"
            exit 1
        }
    }
    "promote" { 
        if (-not $IssueNumber) {
            Write-Error "IssueNumber is required for promote action"
            Write-Error "Example: .\manage_issues.ps1 -Action promote -IssueNumber 14"
            Write-Error "Example: .\manage_issues.ps1 -Action promote -IssueNumber 14 -FRNumber 'FR-086'"
            exit 1
        }
    }
}

# Execute the requested action
switch ($Action) {
    "list" {
        Write-Info "Listing GitHub Issues"
        Write-Host ""
        
        if ($Mine) {
            Write-Info "Your assigned issues:"
            gh issue list --assignee @me --state open
        } elseif ($Label) {
            Write-Info "Issues with label '$Label':"
            gh issue list --label $Label --state open
        } elseif ($Priority) {
            Write-Info "Issues with priority '$Priority':"
            gh issue list --label "priority:$Priority" --state open
        } else {
            Write-Info "All open issues:"
            gh issue list --state open
        }
        
        Write-Host ""
        Write-Info "Quick filters:"
        Write-Host "  Your issues: .\manage_issues.ps1 -Action list -Mine" -ForegroundColor Gray
        Write-Host "  High priority: .\manage_issues.ps1 -Action list -Priority high" -ForegroundColor Gray
        Write-Host "  In progress: .\manage_issues.ps1 -Action list -Label 'status:in-progress'" -ForegroundColor Gray
    }
    
    "assign" {
        Write-Info "Assigning issue #$IssueNumber to yourself..."
        try {
            gh issue edit $IssueNumber --add-assignee @me
            gh issue edit $IssueNumber --add-label "status:in-progress"
            gh issue edit $IssueNumber --remove-label "status:planning"
            Write-Success "Issue #$IssueNumber assigned and marked as in-progress"
        } catch {
            Write-Error "Failed to assign issue: $($_.Exception.Message)"
        }
    }
    
    "status" {
        Write-Info "Updating status of issue #$IssueNumber to '$Status'..."
        try {
            # Remove existing status labels
            $statusLabels = @("status:proposed", "status:planning", "status:ready-for-pickup", "status:in-progress", "status:testing", "status:on-hold", "status:blocked", "status:rejected", "status:implemented")
            foreach ($statusLabel in $statusLabels) {
                try {
                    gh issue edit $IssueNumber --remove-label $statusLabel 2>$null
                } catch {
                    # Ignore errors for non-existent labels
                }
            }
            
            # Add new status label
            gh issue edit $IssueNumber --add-label "status:$Status"
            
            # Auto-assign if moving to in-progress
            if ($Status -eq "in-progress") {
                gh issue edit $IssueNumber --add-assignee @me
            }
            
            Write-Success "Issue #$IssueNumber status updated to '$Status'"
        } catch {
            Write-Error "Failed to update status: $($_.Exception.Message)"
        }
    }
    
    "comment" {
        Write-Info "Adding comment to issue #$IssueNumber..."
        try {
            gh issue comment $IssueNumber --body $Comment
            Write-Success "Comment added to issue #$IssueNumber"
        } catch {
            Write-Error "Failed to add comment: $($_.Exception.Message)"
        }
    }
    
    "close" {
        Write-Info "Closing issue #$IssueNumber..."
        if ($Comment) {
            try {
                gh issue close $IssueNumber --comment $Comment
                Write-Success "Issue #$IssueNumber closed with comment"
            } catch {
                Write-Error "Failed to close issue: $($_.Exception.Message)"
            }
        } else {
            try {
                gh issue close $IssueNumber
                Write-Success "Issue #$IssueNumber closed"
            } catch {
                Write-Error "Failed to close issue: $($_.Exception.Message)"
            }
        }
    }
    
    "develop" {
        Write-Info "Creating development branch for issue #$IssueNumber..."
        try {
            # Get issue details
            $issueData = gh issue view $IssueNumber --json title,number | ConvertFrom-Json
            $branchName = "feature/$($issueData.number)-$(($issueData.title -replace '[^\w\s-]', '' -replace '\s+', '-').ToLower())"
            
            Write-Info "Creating branch: $branchName"
            
            # Ensure we're on main and up to date
            git checkout main
            git pull origin main
            
            # Create and checkout feature branch
            git checkout -b $branchName
            
            # Update issue status
            gh issue edit $IssueNumber --add-assignee @me
            gh issue edit $IssueNumber --add-label "status:in-progress"
            gh issue edit $IssueNumber --remove-label "status:planning"
            
            # Add comment
            gh issue comment $IssueNumber --body "Started development in branch ``$branchName``"
            
            Write-Success "Development branch '$branchName' created and checked out"
            Write-Success "Issue #$IssueNumber assigned and marked as in-progress"
        } catch {
            Write-Error "Failed to create development branch: $($_.Exception.Message)"
        }
    }
    
    "summary" {
        Write-Info "DexBot Issues Summary"
        Write-Host ""
        
        # Get issue counts by status
        Write-Info "Issues by Status:"
        $allIssues = gh issue list --state open --json labels,title,number | ConvertFrom-Json
        
        $statusCounts = @{}
        $priorityCounts = @{}
        $componentCounts = @{}
        
        foreach ($issue in $allIssues) {
            # Count by status
            $statusLabel = $issue.labels | Where-Object { $_.name -like "status:*" } | Select-Object -First 1
            if ($statusLabel) {
                $status = $statusLabel.name -replace "status:", ""
                if ($statusCounts.ContainsKey($status)) {
                    $statusCounts[$status] = $statusCounts[$status] + 1
                } else {
                    $statusCounts[$status] = 1
                }
            } else {
                if ($statusCounts.ContainsKey("unassigned")) {
                    $statusCounts["unassigned"] = $statusCounts["unassigned"] + 1
                } else {
                    $statusCounts["unassigned"] = 1
                }
            }
            
            # Count by priority
            $priorityLabel = $issue.labels | Where-Object { $_.name -like "priority:*" } | Select-Object -First 1
            if ($priorityLabel) {
                $priority = $priorityLabel.name -replace "priority:", ""
                if ($priorityCounts.ContainsKey($priority)) {
                    $priorityCounts[$priority] = $priorityCounts[$priority] + 1
                } else {
                    $priorityCounts[$priority] = 1
                }
            }
            
            # Count by component
            $componentLabel = $issue.labels | Where-Object { $_.name -like "component:*" } | Select-Object -First 1
            if ($componentLabel) {
                $component = $componentLabel.name -replace "component:", ""
                if ($componentCounts.ContainsKey($component)) {
                    $componentCounts[$component] = $componentCounts[$component] + 1
                } else {
                    $componentCounts[$component] = 1
                }
            }
        }
        
        foreach ($status in $statusCounts.Keys | Sort-Object) {
            Write-Host "  $status`: $($statusCounts[$status])" -ForegroundColor White
        }
        
        Write-Host ""
        Write-Info "Issues by Priority:"
        foreach ($priority in $priorityCounts.Keys | Sort-Object) {
            $color = switch ($priority) {
                "critical" { "Red" }
                "high" { "Yellow" }
                "medium" { "White" }
                "low" { "Gray" }
                default { "White" }
            }
            Write-Host "  $priority`: $($priorityCounts[$priority])" -ForegroundColor $color
        }
        
        Write-Host ""
        Write-Info "Issues by Component:"
        foreach ($component in $componentCounts.Keys | Sort-Object) {
            Write-Host "  $component`: $($componentCounts[$component])" -ForegroundColor White
        }
        
        Write-Host ""
        Write-Info "Quick Actions:"
        Write-Host "  View your issues: .\manage_issues.ps1 -Action list -Mine" -ForegroundColor Gray
        Write-Host "  Start work on issue: .\manage_issues.ps1 -Action develop -IssueNumber 123" -ForegroundColor Gray
        Write-Host "  Update status: .\manage_issues.ps1 -Action status -IssueNumber 123 -Status testing" -ForegroundColor Gray
    }
    
    "review-queue" {
        Write-Info "Issues Needing Triage (Review Queue)"
        Write-Host ""
        
        # Get all open issues
        $allIssues = gh issue list --state open --json labels,title,number,createdAt,author | ConvertFrom-Json
        
        # Filter issues without status labels (need triage)
        $triageIssues = @()
        foreach ($issue in $allIssues) {
            $hasStatusLabel = $false
            foreach ($label in $issue.labels) {
                if ($label.name -like "status:*") {
                    $hasStatusLabel = $true
                    break
                }
            }
            if (-not $hasStatusLabel) {
                $triageIssues += $issue
            }
        }
        
        if ($triageIssues.Count -eq 0) {
            Write-Success "No issues pending triage - review queue is empty!"
        } else {
            Write-Warning "Found $($triageIssues.Count) issue(s) needing triage:"
            Write-Host ""
            
            foreach ($issue in $triageIssues) {
                $createdDate = [DateTime]::Parse($issue.createdAt).ToString("yyyy-MM-dd")
                $author = $issue.author.login
                
                Write-Host "  #$($issue.number)" -ForegroundColor Cyan -NoNewline
                Write-Host " - $($issue.title)" -ForegroundColor White
                Write-Host "    Created: $createdDate by @$author" -ForegroundColor Gray
                
                # Show existing labels (non-status)
                $otherLabels = $issue.labels | Where-Object { $_.name -notlike "status:*" } | ForEach-Object { $_.name }
                if ($otherLabels.Count -gt 0) {
                    Write-Host "    Labels: $($otherLabels -join ', ')" -ForegroundColor Gray
                }
                Write-Host ""
            }
            
            Write-Info "Quick Triage Commands:"
            Write-Host "  Mark as proposed: .\manage_issues.ps1 -Action status -IssueNumber ### -Status proposed" -ForegroundColor Gray
            Write-Host "  View issue details: gh issue view ###" -ForegroundColor Gray
            Write-Host "  Close invalid: gh issue close ### --comment 'Reason for closing'" -ForegroundColor Gray
        }
        
        # Also show proposed issues ready for PRD work
        Write-Host ""
        Write-Info "Proposed Issues (Ready for PRD Development):"
        $proposedIssues = gh issue list --label "status:proposed" --state open --json title,number,author | ConvertFrom-Json
        
        if ($proposedIssues.Count -eq 0) {
            Write-Success "No proposed issues awaiting PRD development"
        } else {
            foreach ($issue in $proposedIssues) {
                Write-Host "  #$($issue.number)" -ForegroundColor Yellow -NoNewline
                Write-Host " - $($issue.title)" -ForegroundColor White
                Write-Host "    Author: @$($issue.author.login)" -ForegroundColor Gray
            }
            Write-Host ""
            Write-Info "PRD Development Commands:"
            Write-Host "  Add PRD comment: gh issue comment ### --body-file prd-content.md" -ForegroundColor Gray
            Write-Host "  Promote to FR (auto FR#): .\manage_issues.ps1 -Action promote -IssueNumber ###" -ForegroundColor Gray
            Write-Host "  Promote with custom FR#: .\manage_issues.ps1 -Action promote -IssueNumber ### -FRNumber 'FR-###'" -ForegroundColor Gray
        }
    }
    
    "promote" {
        Write-Info "Promoting issue #$IssueNumber to formal Feature Request..."
        try {
            # Get current issue details
            $issueData = gh issue view $IssueNumber --json title,body,author,assignees,labels | ConvertFrom-Json
            $currentTitle = $issueData.title
            $originalAuthor = $issueData.author.login
            
            # Auto-determine FR number if not provided
            if (-not $FRNumber) {
                Write-Info "Auto-determining next FR number..."
                
                # Get all existing FR issues
                $allIssues = gh issue list --state all --limit 1000 --json title | ConvertFrom-Json
                $frNumbers = @()
                
                foreach ($issue in $allIssues) {
                    if ($issue.title -match "^FR-(\d+):") {
                        $frNumbers += [int]$matches[1]
                    }
                }
                
                $nextFRNumber = if ($frNumbers.Count -gt 0) {
                    ($frNumbers | Measure-Object -Maximum).Maximum + 1
                } else {
                    1
                }
                
                $FRNumber = "FR-$nextFRNumber"
                Write-Info "Next available FR number: $FRNumber"
            }
            
            # Validate FR number format
            if ($FRNumber -notmatch "^FR-\d+$") {
                Write-Error "FR number must be in format 'FR-###' (e.g., FR-001, FR-042)"
                return
            }
            
            # Check if FR number already exists
            $existingFR = gh issue list --state all --search "title:$FRNumber" --json number,title | ConvertFrom-Json
            if ($existingFR.Count -gt 0) {
                Write-Error "FR number $FRNumber already exists in issue #$($existingFR[0].number): $($existingFR[0].title)"
                return
            }
            
            # Create new FR issue title
            $frTitle = "$FRNumber`: $currentTitle"
            
            # Extract PRD content from comments
            Write-Info "Extracting PRD content from issue comments..."
            $comments = gh issue view $IssueNumber --comments --json comments | ConvertFrom-Json
            
            $prdContent = ""
            foreach ($comment in $comments.comments) {
                if ($comment.body -match "(?s).*PRD.*|.*Product Requirements.*|.*## Requirements.*|.*## Specification.*") {
                    $prdContent = $comment.body
                    break
                }
            }
            
            # Create FR issue body
            $frBody = @"
# Feature Request: $FRNumber

**Original Request:** #$IssueNumber by @$originalAuthor
**Status:** Planning
**Priority:** TBD (to be assigned during sprint planning)

## Overview
This feature request was promoted from the original user request in #$IssueNumber after triage and PRD development.

## Original Description
$($issueData.body)

## Product Requirements Document (PRD)
$prdContent

## Implementation Status
- [ ] Technical design
- [ ] Implementation planning  
- [ ] Development
- [ ] Testing
- [ ] Documentation
- [ ] Deployment

## Cross-References
- Original request: #$IssueNumber
- Related issues: (to be added during development)

---
*This is a formal Feature Request created from user feedback. Implementation timeline will be determined during sprint planning.*
"@

            Write-Info "Creating new FR issue: $frTitle"
            
            # Create the new FR issue
            $newIssueNumber = gh issue create --title $frTitle --body $frBody --label "status:planning" --label "enhancement" | ForEach-Object {
                if ($_ -match "#(\d+)") { $matches[1] }
            }
            
            if (-not $newIssueNumber) {
                Write-Error "Failed to create new FR issue"
                return
            }
            
            Write-Success "Created new FR issue #$newIssueNumber"
            
            # Subscribe original author to new FR issue
            Write-Info "Subscribing @$originalAuthor to FR issue #$newIssueNumber..."  
            try {
                gh api repos/:owner/:repo/issues/$newIssueNumber/subscribers --method PUT --field "subscribers[]=@$originalAuthor" 2>$null
            } catch {
                Write-Warning "Could not auto-subscribe @$originalAuthor (they may need to subscribe manually)"
            }
            
            # Close original issue with cross-reference
            $closureComment = @"
## ✅ Feature Request Approved & Promoted

Thank you for this feature request! After review and PRD development, this has been approved for implementation.

**🎯 Promoted to:** #$newIssueNumber ($FRNumber`)
**📋 Status:** Planning
**🔗 Track Progress:** Follow #$newIssueNumber for development updates

### What happens next:
1. **Technical Design** - Our team will create detailed technical specifications
2. **Sprint Planning** - The feature will be scheduled in an upcoming development sprint  
3. **Implementation** - Development work will begin based on the PRD
4. **Updates** - You'll receive notifications on progress via #$newIssueNumber

Thanks for contributing to DexBot! 🚀

---
*This request is now managed as formal Feature Request $FRNumber in issue #$newIssueNumber*
"@
            
            gh issue comment $IssueNumber --body $closureComment
            gh issue close $IssueNumber
            
            # Add cross-reference comment to new FR
            $crossRefComment = @"
## 📋 Feature Request Details

**Original User Request:** #$IssueNumber  
**Requested by:** @$originalAuthor  
**Promotion Date:** $(Get-Date -Format 'yyyy-MM-dd')  
**PRD Status:** Complete

This feature request was created from user feedback and has completed the triage and PRD development process.
"@
            
            gh issue comment $newIssueNumber --body $crossRefComment
            
            Write-Success "✅ Promotion Complete!"
            Write-Success "Original request #$IssueNumber closed with cross-reference"
            Write-Success "New FR issue #$newIssueNumber created and ready for planning"
            Write-Success "Original author @$originalAuthor subscribed to updates"
            
            Write-Host ""
            Write-Info "Next Steps:"
            Write-Host "  1. Assign component/priority labels: gh issue edit $newIssueNumber --add-label 'component:core' --add-label 'priority:medium'" -ForegroundColor Gray
            Write-Host "  2. Assign to milestone: gh issue edit $newIssueNumber --milestone 'v1.2.0'" -ForegroundColor Gray
            Write-Host "  3. Begin technical design and implementation planning" -ForegroundColor Gray
            
        } catch {
            Write-Error "Failed to promote issue: $($_.Exception.Message)"
            Write-Error "Stack trace: $($_.ScriptStackTrace)"
        }
    }
}

Write-Host ""
Write-Info "Issue management complete!"
Write-Info "Available actions: list, review-queue, assign, status, comment, close, develop, summary, promote"

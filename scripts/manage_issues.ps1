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
    The status to set (planning, in-progress, review, testing, blocked)

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
    [ValidateSet("list", "assign", "status", "comment", "close", "develop", "summary")]
    [string]$Action,
    
    [int]$IssueNumber,
    
    [ValidateSet("planning", "in-progress", "review", "testing", "blocked")]
    [string]$Status,
    
    [string]$Comment,
    
    [switch]$Mine = $false,
    
    [string]$Label,
    
    [ValidateSet("critical", "high", "medium", "low")]
    [string]$Priority
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
            $statusLabels = @("status:planning", "status:in-progress", "status:review", "status:testing", "status:blocked")
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
        Write-Host "  Update status: .\manage_issues.ps1 -Action status -IssueNumber 123 -Status review" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Info "Issue management complete!"

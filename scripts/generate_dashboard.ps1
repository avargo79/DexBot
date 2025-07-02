#!/usr/bin/env powershell
<#
.SYNOPSIS
    Generate GitHub Issues workflow dashboard for DexBot project management

.DESCRIPTION
    Creates status visualization dashboards for GitHub Issues workflow, including
    triage queue management, cycle time analysis, and project progress tracking.
    Integrates with existing issue management and fast-track systems.

.PARAMETER DashboardType
    Type of dashboard to generate: status, triage, cycle-time, or comprehensive

.PARAMETER OutputPath
    Path where the dashboard file will be created (default: current directory)

.PARAMETER OutputFormat
    Output format: markdown, html, or json

.PARAMETER TimeRange
    Time range for analysis: 7d, 30d, 90d, or all

.PARAMETER RefreshData
    Refresh data from GitHub API before generating dashboard

.PARAMETER Interactive
    Run in interactive mode with options selection

.PARAMETER Force
    Overwrite existing dashboard files

.EXAMPLE
    .\generate_dashboard.ps1 -DashboardType status
    .\generate_dashboard.ps1 -DashboardType triage -OutputFormat html
    .\generate_dashboard.ps1 -Interactive
    .\generate_dashboard.ps1 -DashboardType comprehensive -TimeRange 30d -RefreshData
#>

param(
    [ValidateSet("status", "triage", "cycle-time", "comprehensive")]
    [string]$DashboardType = "status",
    
    [string]$OutputPath = ".",
    
    [ValidateSet("markdown", "html", "json")]
    [string]$OutputFormat = "markdown",
    
    [ValidateSet("7d", "30d", "90d", "all")]
    [string]$TimeRange = "30d",
    
    [switch]$RefreshData = $false,
    
    [switch]$Interactive = $false,
    
    [switch]$Force = $false
)

# Color output functions
function Write-Success { param($Message) Write-Host $Message -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host $Message -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host $Message -ForegroundColor Red }
function Write-Info { param($Message) Write-Host $Message -ForegroundColor Cyan }

Write-Info "DexBot GitHub Issues Dashboard Generator"
Write-Info "======================================"

# Check if gh CLI is available
try {
    $ghVersion = gh --version
    Write-Success "GitHub CLI detected: $($ghVersion[0])"
} catch {
    Write-Error "GitHub CLI not found. Please install GitHub CLI first."
    exit 1
}

# Interactive mode
if ($Interactive) {
    Write-Info "Interactive Dashboard Generation"
    Write-Host ""
    
    # Get dashboard type
    Write-Info "Available dashboard types:"
    Write-Host "  1. Status - Current project status overview" -ForegroundColor Gray
    Write-Host "  2. Triage - Issues requiring attention" -ForegroundColor Gray
    Write-Host "  3. Cycle-Time - Performance metrics and timing analysis" -ForegroundColor Gray
    Write-Host "  4. Comprehensive - All dashboards combined" -ForegroundColor Gray
    
    $typeChoice = Read-Host "Select dashboard type (1-4, default: 1)"
    if ($typeChoice -eq "") { $typeChoice = "1" }
    
    $typeMap = @{
        "1" = "status"
        "2" = "triage"
        "3" = "cycle-time"
        "4" = "comprehensive"
    }
    $DashboardType = $typeMap[$typeChoice]
    
    # Get output format
    Write-Host ""
    Write-Info "Output formats:"
    Write-Host "  1. Markdown - GitHub-compatible markdown (default)" -ForegroundColor Gray
    Write-Host "  2. HTML - Web-viewable HTML dashboard" -ForegroundColor Gray
    Write-Host "  3. JSON - Machine-readable data format" -ForegroundColor Gray
    
    $formatChoice = Read-Host "Select output format (1-3, default: 1)"
    if ($formatChoice -eq "") { $formatChoice = "1" }
    
    $formatMap = @{
        "1" = "markdown"
        "2" = "html"
        "3" = "json"
    }
    $OutputFormat = $formatMap[$formatChoice]
    
    # Get time range
    Write-Host ""
    Write-Info "Time ranges:"
    Write-Host "  1. 7 days - Recent activity" -ForegroundColor Gray
    Write-Host "  2. 30 days - Monthly overview (default)" -ForegroundColor Gray
    Write-Host "  3. 90 days - Quarterly analysis" -ForegroundColor Gray
    Write-Host "  4. All - Complete project history" -ForegroundColor Gray
    
    $rangeChoice = Read-Host "Select time range (1-4, default: 2)"
    if ($rangeChoice -eq "") { $rangeChoice = "2" }
    
    $rangeMap = @{
        "1" = "7d"
        "2" = "30d"
        "3" = "90d"
        "4" = "all"
    }
    $TimeRange = $rangeMap[$rangeChoice]
    
    # Refresh data option
    Write-Host ""
    $refreshChoice = Read-Host "Refresh data from GitHub API? (y/N, default: N)"
    $RefreshData = ($refreshChoice -eq "y" -or $refreshChoice -eq "Y")
}

# Generate timestamp for file naming
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$dashboardFile = Join-Path $OutputPath "DexBot_Dashboard_$($DashboardType)_$($timestamp).$($OutputFormat)"

# Check if file exists
if ((Test-Path $dashboardFile) -and (-not $Force)) {
    Write-Error "Dashboard file already exists: $dashboardFile"
    Write-Info "Use -Force to overwrite or wait for next minute"
    exit 1
}

Write-Host ""
Write-Info "Generating dashboard..."
Write-Host "  Type: $DashboardType" -ForegroundColor Gray
Write-Host "  Format: $OutputFormat" -ForegroundColor Gray
Write-Host "  Time Range: $TimeRange" -ForegroundColor Gray
Write-Host "  Output: $dashboardFile" -ForegroundColor Gray

# Fetch data from GitHub
Write-Info "Fetching GitHub Issues data..."

try {
    # Get current repository info
    $repoInfo = gh repo view --json name,owner | ConvertFrom-Json
    $repoName = "$($repoInfo.owner.login)/$($repoInfo.name)"
    
    # Calculate date range
    $endDate = Get-Date
    switch ($TimeRange) {
        "7d" { $startDate = $endDate.AddDays(-7) }
        "30d" { $startDate = $endDate.AddDays(-30) }
        "90d" { $startDate = $endDate.AddDays(-90) }
        "all" { $startDate = $endDate.AddYears(-10) }  # Effectively all time
    }
    
    # Fetch issues data
    Write-Info "Fetching issues (this may take a moment)..."
    $allIssues = gh issue list --state all --limit 1000 --json number,title,state,labels,createdAt,updatedAt,closedAt,author,assignees,milestone | ConvertFrom-Json
    
    # Filter issues by date range if not "all"
    if ($TimeRange -ne "all") {
        $allIssues = $allIssues | Where-Object { 
            $createdDate = [DateTime]::Parse($_.createdAt)
            $createdDate -ge $startDate
        }
    }
    
    Write-Success "Fetched $($allIssues.Count) issues for analysis"
    
} catch {
    Write-Error "Failed to fetch GitHub data: $($_.Exception.Message)"
    exit 1
}

# Data analysis functions
function Get-IssuesByStatus {
    param($Issues)
    
    $statusCounts = @{}
    foreach ($issue in $Issues) {
        $statusLabel = ($issue.labels | Where-Object { $_.name -like "status:*" } | Select-Object -First 1)
        if ($statusLabel) { $statusLabel = $statusLabel.name } else { $statusLabel = "no-status" }
        
        if ($statusCounts.ContainsKey($statusLabel)) {
            $statusCounts[$statusLabel]++
        } else {
            $statusCounts[$statusLabel] = 1
        }
    }
    return $statusCounts
}

function Get-IssuesByPriority {
    param($Issues)
    
    $priorityCounts = @{}
    foreach ($issue in $Issues) {
        $priorityLabel = ($issue.labels | Where-Object { $_.name -like "priority:*" } | Select-Object -First 1)
        if ($priorityLabel) { $priorityLabel = $priorityLabel.name } else { $priorityLabel = "no-priority" }
        
        if ($priorityCounts.ContainsKey($priorityLabel)) {
            $priorityCounts[$priorityLabel]++
        } else {
            $priorityCounts[$priorityLabel] = 1
        }
    }
    return $priorityCounts
}

function Get-IssuesByComponent {
    param($Issues)
    
    $componentCounts = @{}
    foreach ($issue in $Issues) {
        $componentLabel = ($issue.labels | Where-Object { $_.name -like "component:*" } | Select-Object -First 1)
        if ($componentLabel) { $componentLabel = $componentLabel.name } else { $componentLabel = "no-component" }
        
        if ($componentCounts.ContainsKey($componentLabel)) {
            $componentCounts[$componentLabel]++
        } else {
            $componentCounts[$componentLabel] = 1
        }
    }
    return $componentCounts
}

function Get-TriageQueue {
    param($Issues)
    
    # Issues needing triage (no status or proposed status)
    $triageIssues = $Issues | Where-Object { 
        $_.state -eq "open" -and (
            -not ($_.labels | Where-Object { $_.name -like "status:*" }) -or
            ($_.labels | Where-Object { $_.name -eq "status:proposed" })
        )
    }
    
    return $triageIssues | Sort-Object { [DateTime]::Parse($_.createdAt) }
}

function Get-FastTrackIssues {
    param($Issues)
    
    return $Issues | Where-Object { 
        $_.state -eq "open" -and 
        ($_.labels | Where-Object { $_.name -eq "prd:fast-track" })
    }
}

function Get-CycleTimeMetrics {
    param($Issues)
    
    $closedIssues = $Issues | Where-Object { $_.state -eq "closed" -and $_.closedAt }
    $cycleTimes = @()
    
    foreach ($issue in $closedIssues) {
        $created = [DateTime]::Parse($issue.createdAt)
        $closed = [DateTime]::Parse($issue.closedAt)
        $cycleTime = ($closed - $created).TotalDays
        $cycleTimes += $cycleTime
    }
    
    if ($cycleTimes.Count -gt 0) {
        $avgCycleTime = ($cycleTimes | Measure-Object -Average).Average
        $medianCycleTime = ($cycleTimes | Sort-Object)[[math]::Floor($cycleTimes.Count / 2)]
        $minCycleTime = ($cycleTimes | Measure-Object -Minimum).Minimum
        $maxCycleTime = ($cycleTimes | Measure-Object -Maximum).Maximum
        
        return @{
            Average = [math]::Round($avgCycleTime, 1)
            Median = [math]::Round($medianCycleTime, 1)
            Minimum = [math]::Round($minCycleTime, 1)
            Maximum = [math]::Round($maxCycleTime, 1)
            Count = $cycleTimes.Count
        }
    } else {
        return @{
            Average = 0
            Median = 0
            Minimum = 0
            Maximum = 0
            Count = 0
        }
    }
}

# Perform data analysis
Write-Info "Analyzing issue data..."

$openIssues = $allIssues | Where-Object { $_.state -eq "open" }
$closedIssues = $allIssues | Where-Object { $_.state -eq "closed" }

$statusBreakdown = Get-IssuesByStatus $openIssues
$priorityBreakdown = Get-IssuesByPriority $openIssues
$componentBreakdown = Get-IssuesByComponent $openIssues
$triageQueue = Get-TriageQueue $allIssues
$fastTrackIssues = Get-FastTrackIssues $allIssues
$cycleTimeMetrics = Get-CycleTimeMetrics $allIssues

# Generate dashboard content based on type and format
$currentDate = Get-Date -Format "yyyy-MM-dd HH:mm"

Write-Info "Generating $DashboardType dashboard in $OutputFormat format..."

switch ($OutputFormat) {
    "markdown" {
        $dashboardContent = @"
# DexBot GitHub Issues Dashboard
## $($DashboardType.ToUpper()) OVERVIEW

**Generated**: $currentDate  
**Repository**: $repoName  
**Time Range**: $TimeRange  
**Total Issues Analyzed**: $($allIssues.Count)

---

"@

        # Add content based on dashboard type
        switch ($DashboardType) {
            "status" {
                $dashboardContent += @"
## STATUS OVERVIEW

### Issue Counts
- **Open Issues**: $($openIssues.Count)
- **Closed Issues**: $($closedIssues.Count)
- **Total Issues**: $($allIssues.Count)
- **Completion Rate**: $(if ($allIssues.Count -gt 0) { [math]::Round(($closedIssues.Count / $allIssues.Count) * 100, 1) } else { 0 })%

### Status Breakdown (Open Issues)
$(if ($openIssues.Count -gt 0) {
    foreach ($status in $statusBreakdown.Keys | Sort-Object) {
        $count = $statusBreakdown[$status]
        $percentage = [math]::Round(($count / $openIssues.Count) * 100, 1)
        "- **$status**: $count issues ($percentage%)"
    }
} else {
    "No open issues to display."
}) -join "`n"

### Priority Breakdown (Open Issues)
$(if ($openIssues.Count -gt 0) {
    foreach ($priority in $priorityBreakdown.Keys | Sort-Object) {
        $count = $priorityBreakdown[$priority]
        $percentage = [math]::Round(($count / $openIssues.Count) * 100, 1)
        "- **$priority**: $count issues ($percentage%)"
    }
} else {
    "No open issues to display."
}) -join "`n"

### Component Breakdown (Open Issues)
$(if ($openIssues.Count -gt 0) {
    foreach ($component in $componentBreakdown.Keys | Sort-Object) {
        $count = $componentBreakdown[$component]
        $percentage = [math]::Round(($count / $openIssues.Count) * 100, 1)
        "- **$component**: $count issues ($percentage%)"
    }
} else {
    "No open issues to display."
}) -join "`n"

"@
            }
            
            "triage" {
                $dashboardContent += @"
## TRIAGE QUEUE

### Triage Summary
- **Issues Needing Triage**: $($triageQueue.Count)
- **Fast-Track Issues**: $($fastTrackIssues.Count)
- **Triage Queue Status**: $(if ($triageQueue.Count -eq 0) { "[CLEAR]" } else { "[NEEDS ATTENTION]" })

### Issues Requiring Triage
$(if ($triageQueue.Count -eq 0) {
    "**No issues currently need triage!**"
} else {
    foreach ($issue in $triageQueue | Select-Object -First 10) {
        $age = [math]::Round(((Get-Date) - [DateTime]::Parse($issue.createdAt)).TotalDays, 1)
        $labels = ($issue.labels | Where-Object { $_.name -notlike "status:*" } | ForEach-Object { $_.name }) -join ", "
        "#### Issue #$($issue.number) - $($issue.title)
- **Age**: $age days
- **Author**: @$($issue.author.login)
- **Labels**: $labels
- **Created**: $($issue.createdAt.Substring(0,10))
"
    }
    if ($triageQueue.Count -gt 10) {
        "
*... and $($triageQueue.Count - 10) more issues requiring triage*"
    }
})

### Fast-Track Issues (Ready for Pickup)
$(if ($fastTrackIssues.Count -eq 0) {
    "No fast-track issues currently available."
} else {
    foreach ($issue in $fastTrackIssues) {
        $labels = ($issue.labels | ForEach-Object { $_.name }) -join ", "
        "#### Issue #$($issue.number) - $($issue.title)
- **Author**: @$($issue.author.login)
- **Labels**: $labels
- **Created**: $($issue.createdAt.Substring(0,10))
"
    }
})

### Triage Actions
- **Review Queue**: ``.\manage_issues.ps1 -Action triage``
- **Fast-Track Validation**: ``.\manage_issues.ps1 -Action fast-track -IssueNumber XXX``
- **Status Management**: ``.\manage_issues.ps1 -Action status -IssueNumber XXX -Status proposed``

"@
            }
            
            "cycle-time" {
                $dashboardContent += @"
## CYCLE TIME ANALYSIS

### Cycle Time Metrics
- **Average Cycle Time**: $($cycleTimeMetrics.Average) days
- **Median Cycle Time**: $($cycleTimeMetrics.Median) days
- **Minimum Cycle Time**: $($cycleTimeMetrics.Minimum) days
- **Maximum Cycle Time**: $($cycleTimeMetrics.Maximum) days
- **Issues Analyzed**: $($cycleTimeMetrics.Count)

### Performance Indicators
$(if ($cycleTimeMetrics.Average -le 7) {
    "[EXCELLENT] - Average cycle time under 1 week"
} elseif ($cycleTimeMetrics.Average -le 14) {
    "[GOOD] - Average cycle time under 2 weeks"
} elseif ($cycleTimeMetrics.Average -le 30) {
    "[FAIR] - Average cycle time under 1 month"
} else {
    "[NEEDS IMPROVEMENT] - Average cycle time over 1 month"
})

### Cycle Time Distribution
$(if ($cycleTimeMetrics.Count -gt 0) {
    $fastIssues = $allIssues | Where-Object { 
        $_.state -eq "closed" -and $_.closedAt -and 
        ([DateTime]::Parse($_.closedAt) - [DateTime]::Parse($_.createdAt)).TotalDays -le 7 
    }
    $mediumIssues = $allIssues | Where-Object { 
        $_.state -eq "closed" -and $_.closedAt -and 
        ([DateTime]::Parse($_.closedAt) - [DateTime]::Parse($_.createdAt)).TotalDays -gt 7 -and
        ([DateTime]::Parse($_.closedAt) - [DateTime]::Parse($_.createdAt)).TotalDays -le 30
    }
    $slowIssues = $allIssues | Where-Object { 
        $_.state -eq "closed" -and $_.closedAt -and 
        ([DateTime]::Parse($_.closedAt) - [DateTime]::Parse($_.createdAt)).TotalDays -gt 30
    }
    
    "- **Fast (≤7 days)**: $($fastIssues.Count) issues ($([math]::Round(($fastIssues.Count / $cycleTimeMetrics.Count) * 100, 1))%)
- **Medium (8-30 days)**: $($mediumIssues.Count) issues ($([math]::Round(($mediumIssues.Count / $cycleTimeMetrics.Count) * 100, 1))%)
- **Slow (>30 days)**: $($slowIssues.Count) issues ($([math]::Round(($slowIssues.Count / $cycleTimeMetrics.Count) * 100, 1))%)"
} else {
    "No closed issues available for cycle time analysis."
})

"@
            }
            
            "comprehensive" {
                # Combine all dashboard types
                $dashboardContent += @"
## STATUS OVERVIEW

### Issue Counts
- **Open Issues**: $($openIssues.Count)
- **Closed Issues**: $($closedIssues.Count)
- **Total Issues**: $($allIssues.Count)
- **Completion Rate**: $(if ($allIssues.Count -gt 0) { [math]::Round(($closedIssues.Count / $allIssues.Count) * 100, 1) } else { 0 })%

### Status Breakdown (Open Issues)
$(if ($openIssues.Count -gt 0) {
    foreach ($status in $statusBreakdown.Keys | Sort-Object) {
        $count = $statusBreakdown[$status]
        $percentage = [math]::Round(($count / $openIssues.Count) * 100, 1)
        "- **$status**: $count issues ($percentage%)"
    }
} else {
    "- No open issues to analyze"
}) -join "`n"

---

## TRIAGE QUEUE

### Triage Summary
- **Issues Needing Triage**: $($triageQueue.Count)
- **Fast-Track Issues**: $($fastTrackIssues.Count)
- **Triage Queue Status**: $(if ($triageQueue.Count -eq 0) { "[CLEAR]" } else { "[NEEDS ATTENTION]" })

### Priority Triage Items
$(if ($triageQueue.Count -eq 0) {
    "**Triage queue is clear!**"
} else {
    foreach ($issue in $triageQueue | Select-Object -First 5) {
        $age = [math]::Round(((Get-Date) - [DateTime]::Parse($issue.createdAt)).TotalDays, 1)
        "- **Issue #$($issue.number)**: $($issue.title) ($age days old)"
    }
    if ($triageQueue.Count -gt 5) {
        "- *... and $($triageQueue.Count - 5) more issues*"
    }
})

---

## CYCLE TIME METRICS

### Performance Summary
- **Average Cycle Time**: $($cycleTimeMetrics.Average) days
- **Median Cycle Time**: $($cycleTimeMetrics.Median) days
- **Performance Level**: $(if ($cycleTimeMetrics.Average -le 7) {
    "[EXCELLENT]"
} elseif ($cycleTimeMetrics.Average -le 14) {
    "[GOOD]"
} elseif ($cycleTimeMetrics.Average -le 30) {
    "[FAIR]"
} else {
    "[NEEDS IMPROVEMENT]"
})

---

## QUICK ACTIONS

### Management Commands
- **Review Triage Queue**: ``.\manage_issues.ps1 -Action triage``
- **Check Fast-Track Issues**: ``.\manage_issues.ps1 -Action list -Label prd:fast-track``
- **Generate PRD Template**: ``.\generate_prd.ps1 -Interactive``
- **Refresh Dashboard**: ``.\generate_dashboard.ps1 -DashboardType comprehensive -RefreshData``

"@
            }
        }
        
        # Add footer
        $dashboardContent += @"

---

## DASHBOARD INFORMATION

**Dashboard Type**: $DashboardType  
**Time Range**: $TimeRange  
**Generated**: $currentDate  
**Data Source**: GitHub Issues API  
**Generator**: DexBot Dashboard Generator v1.0  

### Refresh Dashboard
``````powershell
.\generate_dashboard.ps1 -DashboardType $DashboardType -OutputFormat $OutputFormat -TimeRange $TimeRange -RefreshData
``````

*Dashboard will be automatically refreshed on next generation*
"@
    }
    
    "html" {
        $dashboardContent = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DexBot Dashboard - $($DashboardType.ToUpper())</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background-color: #f6f8fa; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #24292e; border-bottom: 3px solid #0366d6; padding-bottom: 10px; }
        h2 { color: #0366d6; margin-top: 30px; }
        .metric { display: inline-block; margin: 10px 20px 10px 0; padding: 15px; background: #f1f8ff; border-radius: 6px; min-width: 120px; text-align: center; }
        .metric-value { font-size: 24px; font-weight: bold; color: #0366d6; }
        .metric-label { font-size: 14px; color: #586069; margin-top: 5px; }
        .status-good { color: #28a745; }
        .status-warning { color: #ffc107; }
        .status-danger { color: #dc3545; }
        .issue-item { border-left: 4px solid #0366d6; padding: 10px; margin: 10px 0; background: #f8f9fa; }
        .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #e1e4e8; font-size: 12px; color: #586069; }
        table { width: 100%; border-collapse: collapse; margin: 15px 0; }
        th, td { padding: 8px 12px; text-align: left; border-bottom: 1px solid #e1e4e8; }
        th { background-color: #f6f8fa; font-weight: 600; }
    </style>
</head>
<body>
    <div class="container">
        <h1>DexBot GitHub Issues Dashboard</h1>
        <h2>$($DashboardType.ToUpper()) OVERVIEW</h2>
        
        <div class="metric">
            <div class="metric-value">$($allIssues.Count)</div>
            <div class="metric-label">Total Issues</div>
        </div>
        
        <div class="metric">
            <div class="metric-value">$($openIssues.Count)</div>
            <div class="metric-label">Open Issues</div>
        </div>
        
        <div class="metric">
            <div class="metric-value">$($closedIssues.Count)</div>
            <div class="metric-label">Closed Issues</div>
        </div>
        
        <div class="metric">
            <div class="metric-value $(if ($triageQueue.Count -eq 0) { 'status-good' } else { 'status-warning' })">$($triageQueue.Count)</div>
            <div class="metric-label">Triage Queue</div>
        </div>
        
        <p><strong>Generated:</strong> $currentDate | <strong>Time Range:</strong> $TimeRange | <strong>Repository:</strong> $repoName</p>
        
        <div class="footer">
            <p>Dashboard generated by DexBot Dashboard Generator v1.0</p>
            <p>Refresh command: <code>.\generate_dashboard.ps1 -DashboardType $DashboardType -OutputFormat html -RefreshData</code></p>
        </div>
    </div>
</body>
</html>
"@
    }
    
    "json" {
        $dashboardData = @{
            metadata = @{
                generated = $currentDate
                dashboardType = $DashboardType
                timeRange = $TimeRange
                repository = $repoName
                totalIssues = $allIssues.Count
            }
            summary = @{
                openIssues = $openIssues.Count
                closedIssues = $closedIssues.Count
                completionRate = if ($allIssues.Count -gt 0) { [math]::Round(($closedIssues.Count / $allIssues.Count) * 100, 1) } else { 0 }
                triageQueue = $triageQueue.Count
                fastTrackIssues = $fastTrackIssues.Count
            }
            breakdown = @{
                status = $statusBreakdown
                priority = $priorityBreakdown
                component = $componentBreakdown
            }
            cycleTime = $cycleTimeMetrics
            triageQueue = @($triageQueue | Select-Object -First 20 | ForEach-Object {
                @{
                    number = $_.number
                    title = $_.title
                    author = $_.author.login
                    createdAt = $_.createdAt
                    labels = @($_.labels | ForEach-Object { $_.name })
                }
            })
            fastTrackIssues = @($fastTrackIssues | ForEach-Object {
                @{
                    number = $_.number
                    title = $_.title
                    author = $_.author.login
                    createdAt = $_.createdAt
                    labels = @($_.labels | ForEach-Object { $_.name })
                }
            })
        }
        
        $dashboardContent = $dashboardData | ConvertTo-Json -Depth 10
    }
}

# Write the dashboard file
try {
    $dashboardContent | Out-File -FilePath $dashboardFile -Encoding UTF8
    Write-Success "Dashboard generated successfully!"
    Write-Host "  File: $dashboardFile" -ForegroundColor Green
    Write-Host "  Size: $((Get-Item $dashboardFile).Length) bytes" -ForegroundColor Gray
    Write-Host "  Format: $OutputFormat" -ForegroundColor Gray
    
    # Open HTML files in browser if requested
    if ($OutputFormat -eq "html") {
        $openChoice = Read-Host "Open HTML dashboard in browser? (y/N)"
        if ($openChoice -eq "y" -or $openChoice -eq "Y") {
            Start-Process $dashboardFile
        }
    }
    
    Write-Host ""
    Write-Info "Dashboard Summary:"
    Write-Host "  Total Issues: $($allIssues.Count)" -ForegroundColor Gray
    Write-Host "  Open Issues: $($openIssues.Count)" -ForegroundColor Gray
    Write-Host "  Triage Queue: $($triageQueue.Count)" -ForegroundColor Gray
    Write-Host "  Fast-Track Issues: $($fastTrackIssues.Count)" -ForegroundColor Gray
    
    if ($triageQueue.Count -gt 0) {
        Write-Warning "$($triageQueue.Count) issues need triage attention"
        Write-Host "   Run: .\manage_issues.ps1 -Action triage" -ForegroundColor Yellow
    } else {
        Write-Success "Triage queue is clear!"
    }
    
    Write-Host ""
    Write-Info "Next steps:"
    Write-Host "  1. Review the generated dashboard" -ForegroundColor Gray
    Write-Host "  2. Address any issues in triage queue" -ForegroundColor Gray
    Write-Host "  3. Process fast-track issues for quick wins" -ForegroundColor Gray
    Write-Host "  4. Regenerate dashboard: .\generate_dashboard.ps1 -DashboardType $DashboardType -RefreshData" -ForegroundColor Gray
    
} catch {
    Write-Error "Failed to create dashboard file: $($_.Exception.Message)"
    exit 1
}

Write-Host ""
Write-Info "Dashboard Generation Complete!"
Write-Success "Dashboard '$DashboardType' created successfully in $OutputPath"

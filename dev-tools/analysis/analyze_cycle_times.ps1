#!/usr/bin/env powershell
<#
.SYNOPSIS
    Cycle Time Analyzer for GitHub Issues workflow performance metrics

.DESCRIPTION
    Analyzes GitHub Issues lifecycle performance, identifies bottlenecks, and provides
    actionable insights for workflow optimization. Integrates with dashboard system
    to provide comprehensive performance analytics.

.PARAMETER Action
    Analysis type to perform:
    - analyze: Full cycle time analysis with performance metrics
    - bottlenecks: Identify workflow bottlenecks and delays
    - trends: Performance trends analysis over time
    - report: Generate comprehensive performance report
    - compare: Compare performance between time periods

.PARAMETER OutputPath
    Path where analysis results will be saved (default: current directory)

.PARAMETER OutputFormat
    Output format: markdown, html, json, or csv

.PARAMETER TimeRange
    Time range for analysis: 7d, 30d, 90d, 180d, or all

.PARAMETER Threshold
    Performance threshold in days for identifying slow issues (default: 30)

.PARAMETER GroupBy
    Group analysis by: component, priority, status, or author

.PARAMETER Interactive
    Run in interactive mode with detailed explanations

.PARAMETER Baseline
    Baseline period for comparison analysis (30d, 90d, 180d)

.PARAMETER RefreshData
    Refresh data from GitHub API before analysis

.EXAMPLE
    .\analyze_cycle_times.ps1 -Action analyze -TimeRange 90d
    .\analyze_cycle_times.ps1 -Action bottlenecks -GroupBy component -Interactive
    .\analyze_cycle_times.ps1 -Action compare -TimeRange 30d -Baseline 90d
    .\analyze_cycle_times.ps1 -Action report -OutputFormat html -RefreshData
#>

param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("analyze", "bottlenecks", "trends", "report", "compare")]
    [string]$Action,
    
    [string]$OutputPath = ".",
    
    [ValidateSet("markdown", "html", "json", "csv")]
    [string]$OutputFormat = "markdown",
    
    [ValidateSet("7d", "30d", "90d", "180d", "all")]
    [string]$TimeRange = "90d",
    
    [int]$Threshold = 30,
    
    [ValidateSet("component", "priority", "status", "author")]
    [string]$GroupBy = "component",
    
    [switch]$Interactive,
    
    [ValidateSet("30d", "90d", "180d")]
    [string]$Baseline = "90d",
    
    [switch]$RefreshData
)

# ================================================================================
# CONFIGURATION AND SETUP
# ================================================================================

# ASCII-safe PowerShell output for cross-platform compatibility
$OutputEncoding = [System.Text.Encoding]::ASCII
[Console]::OutputEncoding = [System.Text.Encoding]::ASCII

# Create tmp directory if it doesn't exist
if (-not (Test-Path "tmp")) {
    New-Item -ItemType Directory -Path "tmp" -Force | Out-Null
}

# Initialize logging
$LogFile = "tmp/cycle_time_analysis_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

function Write-AnalysisLog {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"
    
    # Write to console
    switch ($Level) {
        "ERROR" { Write-Host $logEntry -ForegroundColor Red }
        "WARN" { Write-Host $logEntry -ForegroundColor Yellow }
        "SUCCESS" { Write-Host $logEntry -ForegroundColor Green }
        "INFO" { Write-Host $logEntry -ForegroundColor Cyan }
        default { Write-Host $logEntry }
    }
    
    # Write to log file
    try {
        Add-Content -Path $LogFile -Value $logEntry -Encoding UTF8
    } catch {
        Write-Warning "Failed to write to log file: $_"
    }
}

# Validation functions
function Test-GitHubCLI {
    try {
        $ghVersion = gh --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-AnalysisLog "GitHub CLI detected: $($ghVersion[0])"
            return $true
        }
    } catch {
        # Ignore errors
    }
    
    Write-AnalysisLog "GitHub CLI not found. Please install gh CLI." "ERROR"
    return $false
}

function Get-TimeRangeDays {
    param([string]$Range)
    
    switch ($Range) {
        "7d" { return 7 }
        "30d" { return 30 }
        "90d" { return 90 }
        "180d" { return 180 }
        "all" { return 365 * 5 } # 5 years max
        default { return 90 }
    }
}

function Get-GitHubIssueData {
    param(
        [int]$Days,
        [switch]$RefreshCache
    )
    
    $cacheFile = "tmp/github_issues_cache_$(Get-Date -Format 'yyyyMMdd').json"
    
    # Check if we should use cached data
    if (-not $RefreshCache -and (Test-Path $cacheFile)) {
        $cacheAge = (Get-Date) - (Get-Item $cacheFile).LastWriteTime
        if ($cacheAge.Hours -lt 1) {
            Write-AnalysisLog "Using cached GitHub data (age: $([math]::Round($cacheAge.TotalMinutes, 1)) minutes)"
            try {
                $cachedData = Get-Content $cacheFile -Raw | ConvertFrom-Json
                return $cachedData
            } catch {
                Write-AnalysisLog "Failed to load cached data, fetching fresh data" "WARN"
            }
        }
    }
    
    Write-AnalysisLog "Fetching GitHub Issues data (this may take a moment)..."
    
    try {
        # Fetch all issues with comprehensive data
        $issuesJson = gh issue list --json number,title,state,labels,createdAt,closedAt,updatedAt,author,assignees,milestone,comments --limit 1000 --state all 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to fetch issues from GitHub"
        }
        
        $allIssues = $issuesJson | ConvertFrom-Json
        
        # Fetch pull requests as well for complete analysis
        $prsJson = gh pr list --json number,title,state,labels,createdAt,closedAt,updatedAt,author,assignees,milestone,comments --limit 1000 --state all 2>$null
        if ($LASTEXITCODE -eq 0) {
            $allPRs = $prsJson | ConvertFrom-Json
            # Add PRs to the dataset with a type indicator
            $allPRs | ForEach-Object { $_ | Add-Member -NotePropertyName "type" -NotePropertyValue "pull_request" }
        } else {
            $allPRs = @()
        }
        
        # Add type indicator to issues
        $allIssues | ForEach-Object { $_ | Add-Member -NotePropertyName "type" -NotePropertyValue "issue" }
        
        # Combine issues and PRs
        $combinedData = @($allIssues) + @($allPRs)
        
        # Cache the data
        try {
            $combinedData | ConvertTo-Json -Depth 10 | Set-Content $cacheFile -Encoding UTF8
            Write-AnalysisLog "Cached GitHub data for future use"
        } catch {
            Write-AnalysisLog "Failed to cache GitHub data: $_" "WARN"
        }
        
        Write-AnalysisLog "Fetched $($combinedData.Count) items ($($allIssues.Count) issues, $($allPRs.Count) PRs)"
        return $combinedData
        
    } catch {
        Write-AnalysisLog "Error fetching GitHub data: $_" "ERROR"
        return @()
    }
}

function Get-CycleTimeMetrics {
    param(
        [array]$Issues,
        [int]$ThresholdDays
    )
    
    Write-AnalysisLog "Calculating cycle time metrics for $($Issues.Count) items"
    
    $metrics = @{
        TotalItems = $Issues.Count
        OpenItems = 0
        ClosedItems = 0
        CycleTimes = @()
        FastItems = @()      # <= 7 days
        MediumItems = @()    # 8-30 days
        SlowItems = @()      # > 30 days
        ThresholdViolations = @()
        AverageTime = 0
        MedianTime = 0
        MinTime = 0
        MaxTime = 0
        StdDeviation = 0
    }
    
    foreach ($item in $Issues) {
        if ($item.state -eq "closed" -and $item.closedAt) {
            $metrics.ClosedItems++
            
            try {
                $created = [DateTime]::Parse($item.createdAt)
                $closed = [DateTime]::Parse($item.closedAt)
                $cycleTime = ($closed - $created).TotalDays
                
                $metrics.CycleTimes += $cycleTime
                
                # Categorize by speed
                if ($cycleTime -le 7) {
                    $metrics.FastItems += $item
                } elseif ($cycleTime -le 30) {
                    $metrics.MediumItems += $item
                } else {
                    $metrics.SlowItems += $item
                }
                
                # Check threshold violations
                if ($cycleTime -gt $ThresholdDays) {
                    $metrics.ThresholdViolations += @{
                        Item = $item
                        CycleTime = $cycleTime
                        DaysOverThreshold = $cycleTime - $ThresholdDays
                    }
                }
                
            } catch {
                Write-AnalysisLog "Error parsing dates for item #$($item.number): $_" "WARN"
            }
        } else {
            $metrics.OpenItems++
        }
    }
    
    # Calculate statistics
    if ($metrics.CycleTimes.Count -gt 0) {
        $metrics.AverageTime = [math]::Round(($metrics.CycleTimes | Measure-Object -Average).Average, 2)
        $metrics.MedianTime = [math]::Round(($metrics.CycleTimes | Sort-Object)[[math]::Floor($metrics.CycleTimes.Count / 2)], 2)
        $metrics.MinTime = [math]::Round(($metrics.CycleTimes | Measure-Object -Minimum).Minimum, 2)
        $metrics.MaxTime = [math]::Round(($metrics.CycleTimes | Measure-Object -Maximum).Maximum, 2)
        
        # Calculate standard deviation
        $variance = ($metrics.CycleTimes | ForEach-Object { [math]::Pow($_ - $metrics.AverageTime, 2) } | Measure-Object -Average).Average
        $metrics.StdDeviation = [math]::Round([math]::Sqrt($variance), 2)
    }
    
    Write-AnalysisLog "Calculated metrics: $($metrics.ClosedItems) closed items, avg cycle time: $($metrics.AverageTime) days"
    
    return $metrics
}

function Get-BottleneckAnalysis {
    param(
        [array]$Issues,
        [string]$GroupBy
    )
    
    Write-AnalysisLog "Analyzing bottlenecks grouped by: $GroupBy"
    
    $bottlenecks = @{}
    $groupMetrics = @{}
    
    foreach ($item in $Issues) {
        if ($item.state -eq "closed" -and $item.closedAt) {
            # Determine grouping key
            $groupKey = switch ($GroupBy) {
                "component" {
                    $componentLabel = $item.labels | Where-Object { $_.name -like "component:*" } | Select-Object -First 1
                    if ($componentLabel) { $componentLabel.name } else { "unassigned" }
                }
                "priority" {
                    $priorityLabel = $item.labels | Where-Object { $_.name -like "priority:*" } | Select-Object -First 1
                    if ($priorityLabel) { $priorityLabel.name } else { "unassigned" }
                }
                "status" {
                    $statusLabel = $item.labels | Where-Object { $_.name -like "status:*" } | Select-Object -First 1
                    if ($statusLabel) { $statusLabel.name } else { "unassigned" }
                }
                "author" {
                    if ($item.author) { $item.author.login } else { "unknown" }
                }
                default { "all" }
            }
            
            # Initialize group if not exists
            if (-not $groupMetrics.ContainsKey($groupKey)) {
                $groupMetrics[$groupKey] = @{
                    Items = @()
                    CycleTimes = @()
                    Count = 0
                    AverageTime = 0
                    MedianTime = 0
                    MaxTime = 0
                    SlowItems = @()
                }
            }
            
            # Calculate cycle time
            try {
                $created = [DateTime]::Parse($item.createdAt)
                $closed = [DateTime]::Parse($item.closedAt)
                $cycleTime = ($closed - $created).TotalDays
                
                $groupMetrics[$groupKey].Items += $item
                $groupMetrics[$groupKey].CycleTimes += $cycleTime
                $groupMetrics[$groupKey].Count++
                
                if ($cycleTime -gt 30) {
                    $groupMetrics[$groupKey].SlowItems += @{
                        Item = $item
                        CycleTime = $cycleTime
                    }
                }
                
            } catch {
                Write-AnalysisLog "Error calculating cycle time for item #$($item.number): $_" "WARN"
            }
        }
    }
    
    # Calculate group statistics
    foreach ($group in $groupMetrics.Keys) {
        $metrics = $groupMetrics[$group]
        if ($metrics.CycleTimes.Count -gt 0) {
            $metrics.AverageTime = [math]::Round(($metrics.CycleTimes | Measure-Object -Average).Average, 2)
            $metrics.MedianTime = [math]::Round(($metrics.CycleTimes | Sort-Object)[[math]::Floor($metrics.CycleTimes.Count / 2)], 2)
            $metrics.MaxTime = [math]::Round(($metrics.CycleTimes | Measure-Object -Maximum).Maximum, 2)
        }
    }
    
    # Identify bottlenecks (groups with high average cycle times)
    $sortedGroups = $groupMetrics.Keys | Sort-Object { $groupMetrics[$_].AverageTime } -Descending
    
    Write-AnalysisLog "Identified $($sortedGroups.Count) groups for bottleneck analysis"
    
    return @{
        GroupMetrics = $groupMetrics
        RankedGroups = $sortedGroups
        BottleneckGroups = $sortedGroups | Select-Object -First 3
    }
}

function Get-TrendAnalysis {
    param(
        [array]$Issues,
        [int]$Days
    )
    
    Write-AnalysisLog "Analyzing performance trends over $Days days"
    
    $endDate = Get-Date
    $startDate = $endDate.AddDays(-$Days)
    $weeklyData = @{}
    
    # Group issues by week
    for ($i = 0; $i -lt $Days; $i += 7) {
        $weekStart = $startDate.AddDays($i)
        $weekEnd = $weekStart.AddDays(6)
        $weekKey = $weekStart.ToString("yyyy-MM-dd")
        
        $weeklyData[$weekKey] = @{
            WeekStart = $weekStart
            WeekEnd = $weekEnd
            Created = @()
            Closed = @()
            CycleTimes = @()
            AverageTime = 0
        }
    }
    
    # Populate weekly data
    foreach ($item in $Issues) {
        $createdDate = [DateTime]::Parse($item.createdAt)
        
        # Find the appropriate week for creation
        foreach ($weekKey in $weeklyData.Keys) {
            $week = $weeklyData[$weekKey]
            if ($createdDate -ge $week.WeekStart -and $createdDate -le $week.WeekEnd) {
                $week.Created += $item
                break
            }
        }
        
        # Process closed items
        if ($item.state -eq "closed" -and $item.closedAt) {
            $closedDate = [DateTime]::Parse($item.closedAt)
            $cycleTime = ($closedDate - $createdDate).TotalDays
            
            # Find the appropriate week for closure
            foreach ($weekKey in $weeklyData.Keys) {
                $week = $weeklyData[$weekKey]
                if ($closedDate -ge $week.WeekStart -and $closedDate -le $week.WeekEnd) {
                    $week.Closed += $item
                    $week.CycleTimes += $cycleTime
                    break
                }
            }
        }
    }
    
    # Calculate weekly averages
    foreach ($weekKey in $weeklyData.Keys) {
        $week = $weeklyData[$weekKey]
        if ($week.CycleTimes.Count -gt 0) {
            $week.AverageTime = [math]::Round(($week.CycleTimes | Measure-Object -Average).Average, 2)
        }
    }
    
    $sortedWeeks = $weeklyData.Keys | Sort-Object
    Write-AnalysisLog "Analyzed trends across $($sortedWeeks.Count) weeks"
    
    return @{
        WeeklyData = $weeklyData
        SortedWeeks = $sortedWeeks
        TrendDirection = if ($sortedWeeks.Count -ge 2) {
            $first = $weeklyData[$sortedWeeks[0]].AverageTime
            $last = $weeklyData[$sortedWeeks[-1]].AverageTime
            if ($last -gt $first) { "increasing" } elseif ($last -lt $first) { "decreasing" } else { "stable" }
        } else { "insufficient_data" }
    }
}

# ================================================================================
# ANALYSIS FUNCTIONS
# ================================================================================

function Invoke-CycleTimeAnalysis {
    param(
        [array]$Issues,
        [int]$ThresholdDays
    )
    
    Write-AnalysisLog "Starting comprehensive cycle time analysis"
    
    $metrics = Get-CycleTimeMetrics -Issues $Issues -ThresholdDays $ThresholdDays
    
    # Generate analysis report
    $analysis = @{
        Summary = @{
            TotalItems = $metrics.TotalItems
            OpenItems = $metrics.OpenItems
            ClosedItems = $metrics.ClosedItems
            CompletionRate = if ($metrics.TotalItems -gt 0) { [math]::Round(($metrics.ClosedItems / $metrics.TotalItems) * 100, 1) } else { 0 }
            ThresholdViolations = $metrics.ThresholdViolations.Count
            ViolationRate = if ($metrics.ClosedItems -gt 0) { [math]::Round(($metrics.ThresholdViolations.Count / $metrics.ClosedItems) * 100, 1) } else { 0 }
        }
        Performance = @{
            AverageTime = $metrics.AverageTime
            MedianTime = $metrics.MedianTime
            MinTime = $metrics.MinTime
            MaxTime = $metrics.MaxTime
            StandardDeviation = $metrics.StdDeviation
            FastItems = $metrics.FastItems.Count
            MediumItems = $metrics.MediumItems.Count
            SlowItems = $metrics.SlowItems.Count
        }
        Distribution = @{
            Fast = if ($metrics.ClosedItems -gt 0) { [math]::Round(($metrics.FastItems.Count / $metrics.ClosedItems) * 100, 1) } else { 0 }
            Medium = if ($metrics.ClosedItems -gt 0) { [math]::Round(($metrics.MediumItems.Count / $metrics.ClosedItems) * 100, 1) } else { 0 }
            Slow = if ($metrics.ClosedItems -gt 0) { [math]::Round(($metrics.SlowItems.Count / $metrics.ClosedItems) * 100, 1) } else { 0 }
        }
        Violations = $metrics.ThresholdViolations | Sort-Object CycleTime -Descending | Select-Object -First 10
    }
    
    Write-AnalysisLog "Analysis complete: $($analysis.Summary.CompletionRate)% completion rate, $($analysis.Performance.AverageTime) days average" "SUCCESS"
    
    return $analysis
}

function Invoke-BottleneckAnalysis {
    param(
        [array]$Issues,
        [string]$GroupBy
    )
    
    Write-AnalysisLog "Starting bottleneck analysis grouped by: $GroupBy"
    
    $bottleneckData = Get-BottleneckAnalysis -Issues $Issues -GroupBy $GroupBy
    
    $analysis = @{
        GroupBy = $GroupBy
        TotalGroups = $bottleneckData.GroupMetrics.Count
        Groups = @{}
        Bottlenecks = @()
        Recommendations = @()
    }
    
    # Process each group
    foreach ($groupName in $bottleneckData.GroupMetrics.Keys) {
        $group = $bottleneckData.GroupMetrics[$groupName]
        $analysis.Groups[$groupName] = @{
            Count = $group.Count
            AverageTime = $group.AverageTime
            MedianTime = $group.MedianTime
            MaxTime = $group.MaxTime
            SlowItemsCount = $group.SlowItems.Count
            SlowItemsRate = if ($group.Count -gt 0) { [math]::Round(($group.SlowItems.Count / $group.Count) * 100, 1) } else { 0 }
        }
    }
    
    # Identify top bottlenecks
    foreach ($groupName in $bottleneckData.BottleneckGroups) {
        $group = $analysis.Groups[$groupName]
        $analysis.Bottlenecks += @{
            Group = $groupName
            AverageTime = $group.AverageTime
            SlowItemsRate = $group.SlowItemsRate
            ItemCount = $group.Count
            Severity = if ($group.AverageTime -gt 60) { "High" } elseif ($group.AverageTime -gt 30) { "Medium" } else { "Low" }
        }
    }
    
    # Generate recommendations
    foreach ($bottleneck in $analysis.Bottlenecks) {
        if ($bottleneck.Severity -eq "High") {
            $analysis.Recommendations += "HIGH PRIORITY: $($bottleneck.Group) has $($bottleneck.AverageTime) days average cycle time - needs immediate attention"
        } elseif ($bottleneck.Severity -eq "Medium") {
            $analysis.Recommendations += "MEDIUM PRIORITY: $($bottleneck.Group) shows $($bottleneck.SlowItemsRate)% slow items - consider process improvements"
        }
    }
    
    Write-AnalysisLog "Bottleneck analysis complete: $($analysis.Bottlenecks.Count) bottlenecks identified" "SUCCESS"
    
    return $analysis
}

function Invoke-TrendAnalysis {
    param(
        [array]$Issues,
        [int]$Days
    )
    
    Write-AnalysisLog "Starting trend analysis for $Days days"
    
    $trendData = Get-TrendAnalysis -Issues $Issues -Days $Days
    
    $analysis = @{
        TimeRange = $Days
        WeekCount = $trendData.SortedWeeks.Count
        TrendDirection = $trendData.TrendDirection
        WeeklyMetrics = @()
        PerformanceChange = 0
        Insights = @()
    }
    
    # Process weekly data
    foreach ($weekKey in $trendData.SortedWeeks) {
        $week = $trendData.WeeklyData[$weekKey]
        $analysis.WeeklyMetrics += @{
            Week = $weekKey
            Created = $week.Created.Count
            Closed = $week.Closed.Count
            AverageTime = $week.AverageTime
            Throughput = $week.Closed.Count
        }
    }
    
    # Calculate performance change
    if ($analysis.WeeklyMetrics.Count -ge 2) {
        $firstWeek = $analysis.WeeklyMetrics[0].AverageTime
        $lastWeek = $analysis.WeeklyMetrics[-1].AverageTime
        
        if ($firstWeek -gt 0) {
            $analysis.PerformanceChange = [math]::Round((($lastWeek - $firstWeek) / $firstWeek) * 100, 1)
        }
    }
    
    # Generate insights
    switch ($analysis.TrendDirection) {
        "increasing" {
            $analysis.Insights += "WARNING: Cycle times are trending upward - performance is degrading"
            $analysis.Insights += "METRIC: Performance decreased by $([math]::Abs($analysis.PerformanceChange))% over the analysis period"
        }
        "decreasing" {
            $analysis.Insights += "SUCCESS: Cycle times are trending downward - performance is improving"
            $analysis.Insights += "METRIC: Performance improved by $([math]::Abs($analysis.PerformanceChange))% over the analysis period"
        }
        "stable" {
            $analysis.Insights += "INFO: Cycle times are stable - consistent performance"
        }
        "insufficient_data" {
            $analysis.Insights += "INFO: Insufficient data for trend analysis"
        }
    }
    
    Write-AnalysisLog "Trend analysis complete: $($analysis.TrendDirection) trend over $($analysis.WeekCount) weeks" "SUCCESS"
    
    return $analysis
}

function Invoke-ComparisonAnalysis {
    param(
        [array]$Issues,
        [int]$CurrentDays,
        [int]$BaselineDays
    )
    
    Write-AnalysisLog "Starting comparison analysis: $CurrentDays days vs $BaselineDays days baseline"
    
    $currentDate = Get-Date
    $currentStart = $currentDate.AddDays(-$CurrentDays)
    $baselineStart = $currentDate.AddDays(-$BaselineDays)
    $baselineEnd = $currentDate.AddDays(-$CurrentDays)
    
    # Split issues into current and baseline periods
    $currentIssues = @()
    $baselineIssues = @()
    
    foreach ($item in $Issues) {
        $createdDate = [DateTime]::Parse($item.createdAt)
        
        if ($createdDate -ge $currentStart) {
            $currentIssues += $item
        } elseif ($createdDate -ge $baselineStart -and $createdDate -lt $baselineEnd) {
            $baselineIssues += $item
        }
    }
    
    # Get metrics for both periods
    $currentMetrics = Get-CycleTimeMetrics -Issues $currentIssues -ThresholdDays 30
    $baselineMetrics = Get-CycleTimeMetrics -Issues $baselineIssues -ThresholdDays 30
    
    # Calculate changes
    $analysis = @{
        CurrentPeriod = @{
            Days = $CurrentDays
            Items = $currentMetrics.TotalItems
            Closed = $currentMetrics.ClosedItems
            AverageTime = $currentMetrics.AverageTime
            CompletionRate = if ($currentMetrics.TotalItems -gt 0) { [math]::Round(($currentMetrics.ClosedItems / $currentMetrics.TotalItems) * 100, 1) } else { 0 }
        }
        BaselinePeriod = @{
            Days = $BaselineDays - $CurrentDays
            Items = $baselineMetrics.TotalItems
            Closed = $baselineMetrics.ClosedItems
            AverageTime = $baselineMetrics.AverageTime
            CompletionRate = if ($baselineMetrics.TotalItems -gt 0) { [math]::Round(($baselineMetrics.ClosedItems / $baselineMetrics.TotalItems) * 100, 1) } else { 0 }
        }
        Changes = @{
            AverageTimeChange = 0
            CompletionRateChange = 0
            ThroughputChange = 0
            PerformanceDirection = "stable"
        }
        Insights = @()
    }
    
    # Calculate changes
    if ($analysis.BaselinePeriod.AverageTime -gt 0) {
        $analysis.Changes.AverageTimeChange = [math]::Round((($analysis.CurrentPeriod.AverageTime - $analysis.BaselinePeriod.AverageTime) / $analysis.BaselinePeriod.AverageTime) * 100, 1)
    }
    
    $analysis.Changes.CompletionRateChange = $analysis.CurrentPeriod.CompletionRate - $analysis.BaselinePeriod.CompletionRate
    $analysis.Changes.ThroughputChange = $analysis.CurrentPeriod.Closed - $analysis.BaselinePeriod.Closed
    
    # Determine performance direction
    if ($analysis.Changes.AverageTimeChange -gt 10) {
        $analysis.Changes.PerformanceDirection = "degrading"
    } elseif ($analysis.Changes.AverageTimeChange -lt -10) {
        $analysis.Changes.PerformanceDirection = "improving"
    }
    
    # Generate insights
    if ($analysis.Changes.PerformanceDirection -eq "improving") {
        $analysis.Insights += "SUCCESS: Performance is improving compared to baseline"
        $analysis.Insights += "METRIC: Average cycle time improved by $([math]::Abs($analysis.Changes.AverageTimeChange))%"
    } elseif ($analysis.Changes.PerformanceDirection -eq "degrading") {
        $analysis.Insights += "WARNING: Performance is degrading compared to baseline"
        $analysis.Insights += "METRIC: Average cycle time increased by $([math]::Abs($analysis.Changes.AverageTimeChange))%"
    } else {
        $analysis.Insights += "INFO: Performance is stable compared to baseline"
    }
    
    if ($analysis.Changes.ThroughputChange -gt 0) {
        $analysis.Insights += "INFO: Throughput increased by $($analysis.Changes.ThroughputChange) items"
    } elseif ($analysis.Changes.ThroughputChange -lt 0) {
        $analysis.Insights += "INFO: Throughput decreased by $([math]::Abs($analysis.Changes.ThroughputChange)) items"
    }
    
    Write-AnalysisLog "Comparison analysis complete: $($analysis.Changes.PerformanceDirection) performance trend" "SUCCESS"
    
    return $analysis
}

# ================================================================================
# OUTPUT GENERATION
# ================================================================================

function Export-AnalysisResult {
    param(
        [hashtable]$Analysis,
        [string]$Action,
        [string]$Format,
        [string]$OutputPath
    )
    
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $filename = "cycle_time_${Action}_${timestamp}"
    $fullPath = Join-Path $OutputPath "$filename.$Format"
    
    Write-AnalysisLog "Exporting $Action analysis to $fullPath"
    
    try {
        switch ($Format) {
            "json" {
                $Analysis | ConvertTo-Json -Depth 10 | Set-Content $fullPath -Encoding UTF8
            }
            "csv" {
                # Create CSV for specific analysis types
                if ($Action -eq "analyze") {
                    $csvData = @()
                    foreach ($violation in $Analysis.Violations) {
                        $csvData += [PSCustomObject]@{
                            ItemNumber = $violation.Item.number
                            Title = $violation.Item.title
                            Author = $violation.Item.author.login
                            CycleTime = $violation.CycleTime
                            DaysOverThreshold = $violation.DaysOverThreshold
                            CreatedAt = $violation.Item.createdAt
                            ClosedAt = $violation.Item.closedAt
                        }
                    }
                    $csvData | Export-Csv $fullPath -NoTypeInformation -Encoding UTF8
                } else {
                    throw "CSV export not supported for action: $Action"
                }
            }
            "html" {
                $htmlContent = Generate-HTMLReport -Analysis $Analysis -Action $Action
                $htmlContent | Set-Content $fullPath -Encoding UTF8
            }
            "markdown" {
                $markdownContent = Generate-MarkdownReport -Analysis $Analysis -Action $Action
                $markdownContent | Set-Content $fullPath -Encoding UTF8
            }
        }
        
        Write-AnalysisLog "Analysis exported successfully to: $fullPath" "SUCCESS"
        return $fullPath
        
    } catch {
        Write-AnalysisLog "Failed to export analysis: $_" "ERROR"
        return $null
    }
}

function Generate-MarkdownReport {
    param(
        [hashtable]$Analysis,
        [string]$Action
    )
    
    $currentDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    $markdown = @"
# GitHub Issues Cycle Time Analysis Report

**Generated**: $currentDate  
**Analysis Type**: $Action  
**Time Range**: $TimeRange  

"@
    
    switch ($Action) {
        "analyze" {
            $markdown += @"
## Executive Summary

- **Total Items**: $($Analysis.Summary.TotalItems)
- **Completion Rate**: $($Analysis.Summary.CompletionRate)%
- **Average Cycle Time**: $($Analysis.Performance.AverageTime) days
- **Threshold Violations**: $($Analysis.Summary.ThresholdViolations) ($($Analysis.Summary.ViolationRate)%)

## Performance Metrics

### Cycle Time Statistics
- **Average**: $($Analysis.Performance.AverageTime) days
- **Median**: $($Analysis.Performance.MedianTime) days
- **Min/Max**: $($Analysis.Performance.MinTime) - $($Analysis.Performance.MaxTime) days
- **Standard Deviation**: $($Analysis.Performance.StandardDeviation) days

### Speed Distribution
- **Fast (≤7 days)**: $($Analysis.Performance.FastItems) items ($($Analysis.Distribution.Fast)%)
- **Medium (8-30 days)**: $($Analysis.Performance.MediumItems) items ($($Analysis.Distribution.Medium)%)
- **Slow (>30 days)**: $($Analysis.Performance.SlowItems) items ($($Analysis.Distribution.Slow)%)

## Top Threshold Violations

$(if ($Analysis.Violations.Count -gt 0) {
    foreach ($violation in $Analysis.Violations) {
        "- **#$($violation.Item.number)**: $($violation.Item.title) - $($violation.CycleTime) days ($($violation.DaysOverThreshold) days over threshold)"
    }
} else {
    "No threshold violations found."
}) -join "`n"

"@
        }
        "bottlenecks" {
            $markdown += @"
## Bottleneck Analysis

**Grouped By**: $($Analysis.GroupBy)  
**Total Groups**: $($Analysis.TotalGroups)

## Identified Bottlenecks

$(foreach ($bottleneck in $Analysis.Bottlenecks) {
    "### $($bottleneck.Group) - $($bottleneck.Severity) Priority
- **Average Cycle Time**: $($bottleneck.AverageTime) days
- **Slow Items Rate**: $($bottleneck.SlowItemsRate)%
- **Total Items**: $($bottleneck.ItemCount)
"
}) -join "`n"

## Recommendations

$(foreach ($recommendation in $Analysis.Recommendations) {
    "- $recommendation"
}) -join "`n"

"@
        }
        "trends" {
            $markdown += @"
## Trend Analysis

**Time Range**: $($Analysis.TimeRange) days  
**Trend Direction**: $($Analysis.TrendDirection)  
**Performance Change**: $($Analysis.PerformanceChange)%

## Weekly Metrics

| Week | Created | Closed | Avg Time | Throughput |
|------|---------|--------|----------|------------|
$(foreach ($week in $Analysis.WeeklyMetrics) {
    "| $($week.Week) | $($week.Created) | $($week.Closed) | $($week.AverageTime) | $($week.Throughput) |"
}) -join "`n"

## Insights

$(foreach ($insight in $Analysis.Insights) {
    "- $insight"
}) -join "`n"

"@
        }
        "compare" {
            $markdown += @"
## Comparison Analysis

### Current Period ($($Analysis.CurrentPeriod.Days) days)
- **Items**: $($Analysis.CurrentPeriod.Items)
- **Completed**: $($Analysis.CurrentPeriod.Closed)
- **Average Time**: $($Analysis.CurrentPeriod.AverageTime) days
- **Completion Rate**: $($Analysis.CurrentPeriod.CompletionRate)%

### Baseline Period ($($Analysis.BaselinePeriod.Days) days)
- **Items**: $($Analysis.BaselinePeriod.Items)
- **Completed**: $($Analysis.BaselinePeriod.Closed)
- **Average Time**: $($Analysis.BaselinePeriod.AverageTime) days
- **Completion Rate**: $($Analysis.BaselinePeriod.CompletionRate)%

### Performance Changes
- **Average Time**: $($Analysis.Changes.AverageTimeChange)%
- **Completion Rate**: $($Analysis.Changes.CompletionRateChange)%
- **Throughput**: $($Analysis.Changes.ThroughputChange) items
- **Direction**: $($Analysis.Changes.PerformanceDirection)

## Insights

$(foreach ($insight in $Analysis.Insights) {
    "- $insight"
}) -join "`n"

"@
        }
    }
    
    $markdown += @"

---

**Generated by**: DexBot Cycle Time Analyzer  
**Log File**: $LogFile  
**Report Date**: $currentDate
"@
    
    return $markdown
}

function Generate-HTMLReport {
    param(
        [hashtable]$Analysis,
        [string]$Action
    )
    
    $currentDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    # Generate basic HTML structure
    $html = @"
<!DOCTYPE html>
<html>
<head>
    <title>GitHub Issues Cycle Time Analysis</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background-color: #f8f9fa; padding: 20px; border-left: 4px solid #007bff; }
        .metric { background-color: #e9ecef; padding: 10px; margin: 10px 0; border-radius: 5px; }
        .high { color: #dc3545; }
        .medium { color: #ffc107; }
        .low { color: #28a745; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #f8f9fa; }
    </style>
</head>
<body>
    <div class="header">
        <h1>GitHub Issues Cycle Time Analysis Report</h1>
        <p><strong>Generated:</strong> $currentDate</p>
        <p><strong>Analysis Type:</strong> $Action</p>
        <p><strong>Time Range:</strong> $TimeRange</p>
    </div>
"@
    
    # Add analysis-specific content
    switch ($Action) {
        "analyze" {
            $html += @"
    <h2>Executive Summary</h2>
    <div class="metric">
        <strong>Total Items:</strong> $($Analysis.Summary.TotalItems)<br>
        <strong>Completion Rate:</strong> $($Analysis.Summary.CompletionRate)%<br>
        <strong>Average Cycle Time:</strong> $($Analysis.Performance.AverageTime) days<br>
        <strong>Threshold Violations:</strong> $($Analysis.Summary.ThresholdViolations) ($($Analysis.Summary.ViolationRate)%)
    </div>
    
    <h2>Performance Distribution</h2>
    <div class="metric low">
        <strong>Fast (≤7 days):</strong> $($Analysis.Performance.FastItems) items ($($Analysis.Distribution.Fast)%)
    </div>
    <div class="metric medium">
        <strong>Medium (8-30 days):</strong> $($Analysis.Performance.MediumItems) items ($($Analysis.Distribution.Medium)%)
    </div>
    <div class="metric high">
        <strong>Slow (>30 days):</strong> $($Analysis.Performance.SlowItems) items ($($Analysis.Distribution.Slow)%)
    </div>
"@
        }
        "bottlenecks" {
            $html += @"
    <h2>Bottleneck Analysis</h2>
    <p><strong>Grouped By:</strong> $($Analysis.GroupBy)</p>
    <p><strong>Total Groups:</strong> $($Analysis.TotalGroups)</p>
    
    <h3>Top Bottlenecks</h3>
    $(foreach ($bottleneck in $Analysis.Bottlenecks) {
        $severityClass = $bottleneck.Severity.ToLower()
        "<div class='metric $severityClass'>
            <strong>$($bottleneck.Group)</strong> - $($bottleneck.Severity) Priority<br>
            Average Time: $($bottleneck.AverageTime) days<br>
            Slow Items: $($bottleneck.SlowItemsRate)%
        </div>"
    }) -join ""
"@
        }
    }
    
    $html += @"
    <footer>
        <hr>
        <p><em>Generated by DexBot Cycle Time Analyzer - $currentDate</em></p>
    </footer>
</body>
</html>
"@
    
    return $html
}

# ================================================================================
# MAIN EXECUTION
# ================================================================================

function Main {
    Write-Host "DexBot Cycle Time Analyzer" -ForegroundColor Cyan
    Write-Host "=========================" -ForegroundColor Cyan
    
    # Validate prerequisites
    if (-not (Test-GitHubCLI)) {
        exit 1
    }
    
    Write-AnalysisLog "Starting cycle time analysis: $Action"
    Write-AnalysisLog "Configuration: TimeRange=$TimeRange, Threshold=$Threshold days, GroupBy=$GroupBy"
    
    # Get GitHub data
    $days = Get-TimeRangeDays -Range $TimeRange
    $issues = Get-GitHubIssueData -Days $days -RefreshCache:$RefreshData
    
    if ($issues.Count -eq 0) {
        Write-AnalysisLog "No issues found for analysis" "ERROR"
        exit 1
    }
    
    # Filter issues by time range
    if ($TimeRange -ne "all") {
        $cutoffDate = (Get-Date).AddDays(-$days)
        $issues = $issues | Where-Object { [DateTime]::Parse($_.createdAt) -ge $cutoffDate }
    }
    
    Write-AnalysisLog "Analyzing $($issues.Count) items for time range: $TimeRange"
    
    # Execute requested analysis
    $analysisResult = $null
    
    switch ($Action) {
        "analyze" {
            $analysisResult = Invoke-CycleTimeAnalysis -Issues $issues -ThresholdDays $Threshold
        }
        "bottlenecks" {
            $analysisResult = Invoke-BottleneckAnalysis -Issues $issues -GroupBy $GroupBy
        }
        "trends" {
            $analysisResult = Invoke-TrendAnalysis -Issues $issues -Days $days
        }
        "compare" {
            $baselineDays = Get-TimeRangeDays -Range $Baseline
            $analysisResult = Invoke-ComparisonAnalysis -Issues $issues -CurrentDays $days -BaselineDays $baselineDays
        }
        "report" {
            # Generate comprehensive report
            $cycleAnalysis = Invoke-CycleTimeAnalysis -Issues $issues -ThresholdDays $Threshold
            $bottleneckAnalysis = Invoke-BottleneckAnalysis -Issues $issues -GroupBy $GroupBy
            $trendAnalysis = Invoke-TrendAnalysis -Issues $issues -Days $days
            
            $analysisResult = @{
                CycleTime = $cycleAnalysis
                Bottlenecks = $bottleneckAnalysis
                Trends = $trendAnalysis
                Summary = @{
                    TotalItems = $issues.Count
                    TimeRange = $TimeRange
                    ThresholdDays = $Threshold
                    GeneratedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
                }
            }
        }
    }
    
    # Export results
    if ($analysisResult) {
        $outputFile = Export-AnalysisResult -Analysis $analysisResult -Action $Action -Format $OutputFormat -OutputPath $OutputPath
        
        if ($outputFile) {
            Write-Host ""
            Write-Host "Analysis completed successfully!" -ForegroundColor Green
            Write-Host "Output file: $outputFile" -ForegroundColor Green
            Write-Host "Log file: $LogFile" -ForegroundColor Gray
            
            # Interactive mode summary
            if ($Interactive) {
                Write-Host ""
                Write-Host "=== ANALYSIS SUMMARY ===" -ForegroundColor Yellow
                
                switch ($Action) {
                    "analyze" {
                        Write-Host "Total Items: $($analysisResult.Summary.TotalItems)" -ForegroundColor White
                        Write-Host "Completion Rate: $($analysisResult.Summary.CompletionRate)%" -ForegroundColor White
                        Write-Host "Average Cycle Time: $($analysisResult.Performance.AverageTime) days" -ForegroundColor White
                        Write-Host "Threshold Violations: $($analysisResult.Summary.ThresholdViolations)" -ForegroundColor $(if ($analysisResult.Summary.ThresholdViolations -gt 0) { "Red" } else { "Green" })
                    }
                    "bottlenecks" {
                        Write-Host "Groups Analyzed: $($analysisResult.TotalGroups)" -ForegroundColor White
                        Write-Host "Bottlenecks Found: $($analysisResult.Bottlenecks.Count)" -ForegroundColor White
                        if ($analysisResult.Bottlenecks.Count -gt 0) {
                            Write-Host "Top Bottleneck: $($analysisResult.Bottlenecks[0].Group) ($($analysisResult.Bottlenecks[0].AverageTime) days)" -ForegroundColor Red
                        }
                    }
                    "trends" {
                        Write-Host "Trend Direction: $($analysisResult.TrendDirection)" -ForegroundColor $(if ($analysisResult.TrendDirection -eq "increasing") { "Red" } elseif ($analysisResult.TrendDirection -eq "decreasing") { "Green" } else { "Yellow" })
                        Write-Host "Performance Change: $($analysisResult.PerformanceChange)%" -ForegroundColor White
                    }
                }
                
                Write-Host ""
                Write-Host "Next steps:" -ForegroundColor Yellow
                Write-Host "1. Review the generated report file" -ForegroundColor White
                Write-Host "2. Address any identified bottlenecks or issues" -ForegroundColor White
                Write-Host "3. Re-run analysis periodically to track improvements" -ForegroundColor White
            }
            
            exit 0
        } else {
            Write-Host "Failed to export analysis results" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "Analysis failed to generate results" -ForegroundColor Red
        exit 1
    }
}

# Run main function
Main

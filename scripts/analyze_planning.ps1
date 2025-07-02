#!/usr/bin/env powershell
<#
.SYNOPSIS
    Automated Planning Analysis for GitHub Issues workflow optimization

.DESCRIPTION
    Analyzes project dependencies, resource allocation, and timeline predictions
    to provide automated planning insights. Integrates with GitHub Issues workflow
    to optimize project planning and delivery forecasting.

.PARAMETER Action
    Planning analysis type to perform:
    - dependencies: Analyze issue dependencies and blocking relationships
    - timeline: Generate timeline predictions and delivery forecasts
    - resources: Optimize resource allocation across components
    - risks: Identify project risks and bottlenecks
    - plan: Generate comprehensive project plan

.PARAMETER Component
    Filter analysis by specific component

.PARAMETER Priority
    Filter by priority level (low, medium, high, critical)

.PARAMETER TimeHorizon
    Planning time horizon: 30d, 90d, 180d, 365d

.PARAMETER OutputPath
    Path where analysis results will be saved (default: current directory)

.PARAMETER OutputFormat
    Output format: markdown, html, json, or csv

.PARAMETER Interactive
    Run in interactive mode with detailed explanations

.PARAMETER IncludeClosed
    Include closed issues in dependency analysis

.PARAMETER Confidence
    Confidence level for predictions: low, medium, high (default: medium)

.PARAMETER TeamSize
    Team size for resource allocation planning (default: auto-detect)

.EXAMPLE
    .\analyze_planning.ps1 -Action dependencies -Component combat
    .\analyze_planning.ps1 -Action timeline -TimeHorizon 90d -Interactive
    .\analyze_planning.ps1 -Action plan -OutputFormat html -Confidence high
    .\analyze_planning.ps1 -Action risks -Priority high
#>

param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("dependencies", "timeline", "resources", "risks", "plan")]
    [string]$Action,
    
    [string]$Component,
    
    [ValidateSet("low", "medium", "high", "critical")]
    [string]$Priority,
    
    [ValidateSet("30d", "90d", "180d", "365d")]
    [string]$TimeHorizon = "90d",
    
    [string]$OutputPath = ".",
    
    [ValidateSet("markdown", "html", "json", "csv")]
    [string]$OutputFormat = "markdown",
    
    [switch]$Interactive,
    
    [switch]$IncludeClosed,
    
    [ValidateSet("low", "medium", "high")]
    [string]$Confidence = "medium",
    
    [int]$TeamSize = 0
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
$LogFile = "tmp/planning_analysis_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

function Write-PlanningLog {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"
    
    Write-Host $logEntry
    Add-Content -Path $LogFile -Value $logEntry -Encoding ASCII
}

function Test-GitHubCLI {
    try {
        $ghVersion = gh --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            $version = ($ghVersion | Select-Object -First 1).Split(' ')[2]
            Write-PlanningLog "GitHub CLI detected: gh version $version"
            return $true
        }
    }
    catch {
        Write-PlanningLog "GitHub CLI not available: $($_.Exception.Message)" "ERROR"
    }
    
    Write-PlanningLog "GitHub CLI (gh) is required but not available" "ERROR"
    Write-Host "Please install GitHub CLI: https://cli.github.com/" -ForegroundColor Red
    return $false
}

function Get-GitHubData {
    $cacheFile = "tmp/github_data_cache.json"
    $cacheAge = if (Test-Path $cacheFile) { 
        (Get-Date) - (Get-Item $cacheFile).LastWriteTime 
    } else { 
        [TimeSpan]::MaxValue 
    }
    
    # Use cache if less than 15 minutes old
    if ($cacheAge.TotalMinutes -lt 15) {
        Write-PlanningLog "Using cached GitHub data (age: $([math]::Round($cacheAge.TotalMinutes, 1)) minutes)"
        return Get-Content $cacheFile -Raw | ConvertFrom-Json
    }
    
    Write-PlanningLog "Fetching GitHub data for planning analysis..."
    
    try {
        # Fetch comprehensive issue data including comments and events
        $stateFilter = if ($IncludeClosed) { "all" } else { "open" }
        $issues = gh issue list --repo . --state $stateFilter --limit 1000 --json number,title,state,createdAt,closedAt,assignees,labels,author,body,comments --jq '.'
        $prs = gh pr list --repo . --state $stateFilter --limit 1000 --json number,title,state,createdAt,closedAt,assignees,labels,author,body --jq '.'
        
        # Fetch milestone information
        $milestones = gh api repos/:owner/:repo/milestones --jq '.'
        
        $data = @{
            issues = if ($issues) { $issues | ConvertFrom-Json } else { @() }
            prs = if ($prs) { $prs | ConvertFrom-Json } else { @() }
            milestones = if ($milestones) { $milestones | ConvertFrom-Json } else { @() }
            fetchedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        }
        
        # Cache the data
        $data | ConvertTo-Json -Depth 10 | Set-Content $cacheFile -Encoding ASCII
        Write-PlanningLog "Cached GitHub data for future use"
        
        return $data
    }
    catch {
        Write-PlanningLog "Error fetching GitHub data: $($_.Exception.Message)" "ERROR"
        throw
    }
}

function Get-IssueDependencies {
    param(
        [object]$GitHubData
    )
    
    Write-PlanningLog "Analyzing issue dependencies and blocking relationships"
    
    $dependencies = @{}
    $blocks = @{}
    
    # Analyze issue bodies and comments for dependency keywords
    foreach ($issue in $GitHubData.issues) {
        if (-not $issue -or -not $issue.number) {
            Write-PlanningLog "Skipping invalid issue" "WARN"
            continue
        }
        
        $dependencies[$issue.number] = @{
            issue = $issue
            dependsOn = @()
            blocks = @()
            mentions = @()
            priority = "medium"
            component = "general"
            estimatedEffort = 5  # Default effort in days
        }
        
        # Extract priority from labels
        if ($issue.labels -and $issue.labels.Count -gt 0) {
            foreach ($label in $issue.labels) {
                if ($label.name -match "^priority:(.+)") {
                    $dependencies[$issue.number].priority = $matches[1]
                }
                if ($label.name -match "^(component|system):(.+)") {
                    $dependencies[$issue.number].component = $matches[2]
                }
            }
        }
        
        # Estimate effort based on issue complexity
        $bodyLength = if ($issue.body) { $issue.body.Length } else { 0 }
        $labelCount = if ($issue.labels) { $issue.labels.Count } else { 0 }
        $effortScore = [math]::Max(1, [math]::Min(21, ($bodyLength / 100) + ($labelCount * 2)))
        $dependencies[$issue.number].estimatedEffort = [math]::Round($effortScore, 0)
        
        # Parse dependency relationships from issue body
        if ($issue.body) {
            $dependencyPatterns = @(
                "depends on #(\d+)",
                "blocked by #(\d+)",
                "requires #(\d+)",
                "after #(\d+)",
                "needs #(\d+)"
            )
            
            foreach ($pattern in $dependencyPatterns) {
                $matches = [regex]::Matches($issue.body, $pattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
                foreach ($match in $matches) {
                    $dependentIssue = [int]$match.Groups[1].Value
                    if ($dependencies.ContainsKey($dependentIssue)) {
                        $dependencies[$issue.number].dependsOn += $dependentIssue
                        if (-not $blocks.ContainsKey($dependentIssue)) {
                            $blocks[$dependentIssue] = @()
                        }
                        $blocks[$dependentIssue] += $issue.number
                    }
                }
            }
            
            $blockingPatterns = @(
                "blocks #(\d+)",
                "blocking #(\d+)",
                "prevents #(\d+)",
                "required for #(\d+)"
            )
            
            foreach ($pattern in $blockingPatterns) {
                $matches = [regex]::Matches($issue.body, $pattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
                foreach ($match in $matches) {
                    $blockedIssue = [int]$match.Groups[1].Value
                    if ($dependencies.ContainsKey($blockedIssue)) {
                        $dependencies[$issue.number].blocks += $blockedIssue
                        if (-not $blocks.ContainsKey($issue.number)) {
                            $blocks[$issue.number] = @()
                        }
                        $blocks[$issue.number] += $blockedIssue
                    }
                }
            }
            
            # Find issue mentions for potential relationships
            $mentionMatches = [regex]::Matches($issue.body, "#(\d+)", [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
            foreach ($match in $mentionMatches) {
                $mentionedIssue = [int]$match.Groups[1].Value
                if ($dependencies.ContainsKey($mentionedIssue) -and $mentionedIssue -ne $issue.number) {
                    $dependencies[$issue.number].mentions += $mentionedIssue
                }
            }
        }
    }
    
    # Add blocking relationships
    foreach ($issueNum in $blocks.Keys) {
        if ($dependencies.ContainsKey($issueNum)) {
            $dependencies[$issueNum].blocks = $blocks[$issueNum]
        }
    }
    
    Write-PlanningLog "Analyzed dependencies for $($dependencies.Keys.Count) issues"
    return $dependencies
}

function Get-TimelinePredictions {
    param(
        [hashtable]$Dependencies,
        [object]$GitHubData,
        [string]$TimeHorizon,
        [int]$TeamSize
    )
    
    Write-PlanningLog "Generating timeline predictions for $TimeHorizon horizon"
    
    # Calculate team velocity based on historical data
    $closedIssues = $GitHubData.issues | Where-Object { $_.state -eq "closed" }
    $recentClosures = @()
    
    $horizonDays = switch ($TimeHorizon) {
        "30d" { 30 }
        "90d" { 90 }
        "180d" { 180 }
        "365d" { 365 }
        default { 90 }
    }
    
    $cutoffDate = (Get-Date).AddDays(-$horizonDays)
    
    foreach ($issue in $closedIssues) {
        try {
            if ($issue.closedAt) {
                $closedDate = [DateTime]::Parse($issue.closedAt)
                if ($closedDate -gt $cutoffDate) {
                    $createdDate = [DateTime]::Parse($issue.createdAt)
                    $cycleTime = ($closedDate - $createdDate).TotalDays
                    $recentClosures += $cycleTime
                }
            }
        }
        catch {
            # Skip issues with invalid dates
        }
    }
    
    $avgCycleTime = if ($recentClosures.Count -gt 0) {
        ($recentClosures | Measure-Object -Average).Average
    } else {
        14  # Default 2 weeks if no historical data
    }
    
    $teamVelocity = if ($TeamSize -gt 0) {
        [math]::Max(1, [math]::Round($TeamSize / $avgCycleTime * 7, 1))  # Issues per week
    } else {
        1  # Default velocity
    }
    
    Write-PlanningLog "Calculated team velocity: $teamVelocity issues/week (avg cycle: $([math]::Round($avgCycleTime, 1)) days)"
    
    # Build dependency graph and calculate critical path
    $timeline = @{}
    $openIssues = $Dependencies.Values | Where-Object { $_.issue.state -eq "open" }
    
    # Sort issues by priority and dependencies
    $priorityWeights = @{
        "critical" = 4
        "high" = 3
        "medium" = 2
        "low" = 1
    }
    
    $sortedIssues = $openIssues | Sort-Object { 
        $priorityWeights[$_.priority] * -1 + $_.dependsOn.Count 
    }
    
    $currentDate = Get-Date
    $scheduleOffset = 0
    
    foreach ($issueDep in $sortedIssues) {
        $issue = $issueDep.issue
        
        # Calculate start date based on dependencies
        $startDate = $currentDate.AddDays($scheduleOffset)
        
        # Check if any dependencies would delay start
        foreach ($depIssueNum in $issueDep.dependsOn) {
            if ($timeline.ContainsKey($depIssueNum)) {
                $depEndDate = $timeline[$depIssueNum].endDate
                if ($depEndDate -gt $startDate) {
                    $startDate = $depEndDate.AddDays(1)
                }
            }
        }
        
        # Estimate duration based on effort and team capacity
        $duration = [math]::Max(1, [math]::Round($issueDep.estimatedEffort / $teamVelocity * 7, 0))
        $endDate = $startDate.AddDays($duration)
        
        $timeline[$issue.number] = @{
            issue = $issue
            startDate = $startDate
            endDate = $endDate
            duration = $duration
            effort = $issueDep.estimatedEffort
            priority = $issueDep.priority
            component = $issueDep.component
            dependsOn = $issueDep.dependsOn
            blocks = $issueDep.blocks
            criticalPath = ($issueDep.dependsOn.Count -gt 0 -or $issueDep.blocks.Count -gt 0)
        }
        
        # Update schedule offset for non-parallel work
        if ($issueDep.priority -eq "critical" -or $issueDep.dependsOn.Count -gt 0) {
            $scheduleOffset = ($endDate - $currentDate).TotalDays
        }
    }
    
    Write-PlanningLog "Generated timeline predictions for $($timeline.Keys.Count) open issues"
    return @{
        timeline = $timeline
        velocity = $teamVelocity
        avgCycleTime = $avgCycleTime
        totalEffort = ($sortedIssues | Measure-Object -Property estimatedEffort -Sum).Sum
        projectedCompletion = $currentDate.AddDays($scheduleOffset)
    }
}

function Get-ResourceAllocation {
    param(
        [hashtable]$Dependencies,
        [object]$TimelinePredictions,
        [int]$TeamSize
    )
    
    Write-PlanningLog "Analyzing resource allocation and optimization opportunities"
    
    # Group issues by component
    $componentWorkload = @{}
    $componentEffort = @{}
    
    foreach ($issueNum in $Dependencies.Keys) {
        $dep = $Dependencies[$issueNum]
        $component = $dep.component
        
        if (-not $componentWorkload.ContainsKey($component)) {
            $componentWorkload[$component] = @()
            $componentEffort[$component] = 0
        }
        
        if ($dep.issue.state -eq "open") {
            $componentWorkload[$component] += $dep.issue
            $componentEffort[$component] = $componentEffort[$component] + $dep.estimatedEffort
        }
    }
    
    # Calculate resource distribution
    $totalEffort = ($componentEffort.Values | Measure-Object -Sum).Sum
    $resourceAllocation = @{}
    
    foreach ($component in $componentWorkload.Keys) {
        $effort = $componentEffort[$component]
        $percentage = if ($totalEffort -gt 0) { 
            [math]::Round(($effort / $totalEffort) * 100, 1) 
        } else { 
            0 
        }
        
        $estimatedDeveloperNeed = if ($TeamSize -gt 0 -and $totalEffort -gt 0) {
            [math]::Round(($effort / $totalEffort) * $TeamSize, 1)
        } else {
            1
        }
        
        $resourceAllocation[$component] = @{
            issues = $componentWorkload[$component]
            totalEffort = $effort
            percentageOfTotal = $percentage
            estimatedDeveloperNeed = $estimatedDeveloperNeed
            priority = "medium"  # Could be calculated based on issue priorities
        }
    }
    
    # Identify bottlenecks and optimization opportunities
    $bottlenecks = @()
    $optimizations = @()
    
    foreach ($component in $resourceAllocation.Keys) {
        $allocation = $resourceAllocation[$component]
        
        # Identify potential bottlenecks (>40% of total effort)
        if ($allocation.percentageOfTotal -gt 40) {
            $bottlenecks += @{
                component = $component
                effort = $allocation.totalEffort
                percentage = $allocation.percentageOfTotal
                risk = "high"
                recommendation = "Consider breaking down large issues or adding specialized resources"
            }
        }
        
        # Identify optimization opportunities
        if ($allocation.issues.Count -gt 5 -and $allocation.percentageOfTotal -lt 10) {
            $optimizations += @{
                component = $component
                opportunity = "Many small issues - consider batch processing"
                potentialSavings = "20-30%"
            }
        }
    }
    
    Write-PlanningLog "Resource allocation analysis complete: $($componentWorkload.Keys.Count) components analyzed"
    
    return @{
        allocation = $resourceAllocation
        bottlenecks = $bottlenecks
        optimizations = $optimizations
        totalEffort = $totalEffort
        teamSize = $TeamSize
    }
}

function Get-ProjectRisks {
    param(
        [hashtable]$Dependencies,
        [object]$TimelinePredictions,
        [object]$ResourceAllocation
    )
    
    Write-PlanningLog "Identifying project risks and potential issues"
    
    $risks = @()
    
    # Dependency risks
    foreach ($issueNum in $Dependencies.Keys) {
        $dep = $Dependencies[$issueNum]
        
        # High dependency count risk
        if ($dep.dependsOn.Count -gt 3) {
            $risks += @{
                type = "dependency"
                severity = "high"
                issue = $dep.issue.number
                title = $dep.issue.title
                description = "Issue has $($dep.dependsOn.Count) dependencies - high coordination risk"
                impact = "Delays likely if any dependency is delayed"
                mitigation = "Consider breaking down or parallelizing work"
            }
        }
        
        # Blocking risk
        if ($dep.blocks.Count -gt 2) {
            $risks += @{
                type = "blocking"
                severity = "medium"
                issue = $dep.issue.number
                title = $dep.issue.title
                description = "Issue blocks $($dep.blocks.Count) other issues"
                impact = "Bottleneck for downstream work"
                mitigation = "Prioritize completion or find alternative approaches"
            }
        }
        
        # High effort risk
        if ($dep.estimatedEffort -gt 15) {
            $risks += @{
                type = "effort"
                severity = "medium"
                issue = $dep.issue.number
                title = $dep.issue.title
                description = "High effort estimate ($($dep.estimatedEffort) days)"
                impact = "Resource intensive, scope creep risk"
                mitigation = "Break down into smaller tasks, frequent review"
            }
        }
    }
    
    # Timeline risks
    if ($TimelinePredictions.projectedCompletion) {
        $daysToCompletion = ($TimelinePredictions.projectedCompletion - (Get-Date)).TotalDays
        
        if ($daysToCompletion -gt 180) {
            $risks += @{
                type = "timeline"
                severity = "high"
                issue = "overall"
                title = "Extended timeline"
                description = "Projected completion in $([math]::Round($daysToCompletion, 0)) days"
                impact = "Long delivery cycles, stakeholder concerns"
                mitigation = "Reduce scope, increase team size, or improve velocity"
            }
        }
    }
    
    # Resource risks
    foreach ($bottleneck in $ResourceAllocation.bottlenecks) {
        $risks += @{
            type = "resource"
            severity = "high"
            issue = $bottleneck.component
            title = "Resource bottleneck"
            description = "$($bottleneck.component) requires $($bottleneck.percentage)% of total effort"
            impact = "Single point of failure, knowledge concentration"
            mitigation = $bottleneck.recommendation
        }
    }
    
    Write-PlanningLog "Identified $($risks.Count) project risks"
    return $risks
}

function Export-PlanningAnalysis {
    param(
        [string]$Action,
        [object]$Data,
        [string]$OutputPath,
        [string]$OutputFormat
    )
    
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $filename = "planning_${Action}_${timestamp}.${OutputFormat}"
    $filepath = Join-Path $OutputPath $filename
    
    Write-PlanningLog "Exporting $Action analysis to $filepath"
    
    switch ($OutputFormat) {
        "markdown" {
            Export-MarkdownReport -Action $Action -Data $Data -FilePath $filepath
        }
        "html" {
            Export-HtmlReport -Action $Action -Data $Data -FilePath $filepath
        }
        "json" {
            $Data | ConvertTo-Json -Depth 10 | Set-Content $filepath -Encoding ASCII
        }
        "csv" {
            Export-CsvReport -Action $Action -Data $Data -FilePath $filepath
        }
    }
    
    Write-PlanningLog "Analysis exported successfully to: $filepath" "SUCCESS"
    return $filepath
}

function Export-MarkdownReport {
    param(
        [string]$Action,
        [object]$Data,
        [string]$FilePath
    )
    
    $content = @"
# GitHub Issues Automated Planning Analysis Report

**Generated**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")  
**Analysis Type**: $Action  
**Time Horizon**: $TimeHorizon  
**Confidence Level**: $Confidence  

"@

    switch ($Action) {
        "dependencies" {
            $content += @"
## Dependency Analysis

### Summary
- **Total Issues Analyzed**: $($Data.Keys.Count)
- **Issues with Dependencies**: $(($Data.Values | Where-Object { $_.dependsOn.Count -gt 0 }).Count)
- **Blocking Issues**: $(($Data.Values | Where-Object { $_.blocks.Count -gt 0 }).Count)

### Dependency Details
"@
            foreach ($issueNum in ($Data.Keys | Sort-Object)) {
                $dep = $Data[$issueNum]
                if ($dep.dependsOn.Count -gt 0 -or $dep.blocks.Count -gt 0) {
                    $content += @"

#### Issue #$($issueNum): $($dep.issue.title)
- **Priority**: $($dep.priority)
- **Component**: $($dep.component)
- **Estimated Effort**: $($dep.estimatedEffort) days
"@
                    if ($dep.dependsOn.Count -gt 0) {
                        $content += "- **Depends On**: #$($dep.dependsOn -join ', #')`n"
                    }
                    if ($dep.blocks.Count -gt 0) {
                        $content += "- **Blocks**: #$($dep.blocks -join ', #')`n"
                    }
                }
            }
        }
        
        "timeline" {
            $content += @"
## Timeline Predictions

### Team Metrics
- **Team Velocity**: $($Data.velocity) issues/week
- **Average Cycle Time**: $([math]::Round($Data.avgCycleTime, 1)) days
- **Total Estimated Effort**: $($Data.totalEffort) days
- **Projected Completion**: $($Data.projectedCompletion.ToString("yyyy-MM-dd"))

### Issue Timeline
"@
            foreach ($issueNum in ($Data.timeline.Keys | Sort-Object { $Data.timeline[$_].startDate })) {
                $item = $Data.timeline[$issueNum]
                $content += @"

#### Issue #$($issueNum): $($item.issue.title)
- **Start Date**: $($item.startDate.ToString("yyyy-MM-dd"))
- **End Date**: $($item.endDate.ToString("yyyy-MM-dd"))
- **Duration**: $($item.duration) days
- **Priority**: $($item.priority)
- **Component**: $($item.component)
- **Critical Path**: $(if ($item.criticalPath) { "Yes" } else { "No" })
"@
            }
        }
        
        "risks" {
            $content += @"
## Project Risk Analysis

### Risk Summary
- **Total Risks Identified**: $($Data.Count)
- **High Severity**: $(($Data | Where-Object { $_.severity -eq "high" }).Count)
- **Medium Severity**: $(($Data | Where-Object { $_.severity -eq "medium" }).Count)

### Risk Details
"@
            foreach ($risk in ($Data | Sort-Object severity -Descending)) {
                $content += @"

#### $($risk.type.ToUpper()) Risk: $($risk.title)
- **Severity**: $($risk.severity.ToUpper())
- **Issue**: #$($risk.issue)
- **Description**: $($risk.description)
- **Impact**: $($risk.impact)
- **Mitigation**: $($risk.mitigation)
"@
            }
        }
        
        "resources" {
            $content += @"
## Resource Allocation Analysis

### Allocation Summary
- **Total Effort**: $($Data.totalEffort) days
- **Team Size**: $($Data.teamSize)
- **Components**: $($Data.allocation.Keys.Count)

### Component Breakdown
"@
            foreach ($component in ($Data.allocation.Keys | Sort-Object { $Data.allocation[$_].percentageOfTotal } -Descending)) {
                $allocation = $Data.allocation[$component]
                $content += @"

#### $component
- **Issues**: $($allocation.issues.Count)
- **Total Effort**: $($allocation.totalEffort) days
- **Percentage**: $($allocation.percentageOfTotal)%
- **Estimated Developer Need**: $($allocation.estimatedDeveloperNeed)
"@
            }
            
            if ($Data.bottlenecks.Count -gt 0) {
                $content += @"

### Identified Bottlenecks
"@
                foreach ($bottleneck in $Data.bottlenecks) {
                    $content += @"
- **$($bottleneck.component)**: $($bottleneck.percentage)% of total effort
  - Risk: $($bottleneck.risk)
  - Recommendation: $($bottleneck.recommendation)
"@
                }
            }
        }
        
        "plan" {
            $content += @"
## Comprehensive Project Plan

### Executive Summary
- **Total Issues**: $($Data.dependencies.Keys.Count)
- **Projected Timeline**: $($Data.timeline.projectedCompletion.ToString("yyyy-MM-dd"))
- **Total Effort**: $($Data.resources.totalEffort) days
- **Risk Count**: $($Data.risks.Count) ($(($Data.risks | Where-Object { $_.severity -eq "high" }).Count) high-severity)

### Key Milestones
"@
            # Extract critical path items as milestones
            $milestones = $Data.timeline.timeline.Values | Where-Object { $_.criticalPath -or $_.priority -eq "critical" } | Sort-Object startDate | Select-Object -First 10
            
            foreach ($milestone in $milestones) {
                $content += @"
- **$($milestone.endDate.ToString("yyyy-MM-dd"))**: Complete Issue #$($milestone.issue.number) ($($milestone.issue.title))
"@
            }
            
            $content += @"

### Resource Requirements
"@
            foreach ($component in ($Data.resources.allocation.Keys | Sort-Object { $Data.resources.allocation[$_].percentageOfTotal } -Descending)) {
                $allocation = $Data.resources.allocation[$component]
                $content += @"
- **$component**: $($allocation.estimatedDeveloperNeed) developers ($($allocation.percentageOfTotal)% of capacity)
"@
            }
            
            $content += @"

### Critical Risks
"@
            $criticalRisks = $Data.risks | Where-Object { $_.severity -eq "high" } | Select-Object -First 5
            foreach ($risk in $criticalRisks) {
                $content += @"
- **$($risk.title)**: $($risk.description)
"@
            }
        }
    }
    
    $content += @"

---

**Generated by**: DexBot Automated Planning Analysis  
**Log File**: $LogFile  
**Report Date**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@

    Set-Content -Path $FilePath -Value $content -Encoding ASCII
}

function Export-HtmlReport {
    param(
        [string]$Action,
        [object]$Data,
        [string]$FilePath
    )
    
    $html = @"
<!DOCTYPE html>
<html>
<head>
    <title>Planning Analysis - $Action</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1, h2, h3 { color: #333; }
        .summary { background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .risk-high { background: #ffebee; border-left: 4px solid #f44336; padding: 10px; margin: 5px 0; }
        .risk-medium { background: #fff3e0; border-left: 4px solid #ff9800; padding: 10px; margin: 5px 0; }
        .metric { display: inline-block; margin: 5px 15px 5px 0; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>Automated Planning Analysis - $Action</h1>
    <div class="summary">
        <strong>Generated:</strong> $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")<br>
        <strong>Time Horizon:</strong> $TimeHorizon<br>
        <strong>Confidence Level:</strong> $Confidence
    </div>
"@

    # Add action-specific HTML content here (similar to markdown but with HTML formatting)
    
    $html += @"
    <hr>
    <p><em>Generated by: DexBot Automated Planning Analysis</em></p>
    <p><em>Report Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")</em></p>
</body>
</html>
"@
    
    Set-Content -Path $FilePath -Value $html -Encoding ASCII
}

function Export-CsvReport {
    param(
        [string]$Action,
        [object]$Data,
        [string]$FilePath
    )
    
    switch ($Action) {
        "dependencies" {
            $csvData = foreach ($issueNum in $Data.Keys) {
                $dep = $Data[$issueNum]
                [PSCustomObject]@{
                    IssueNumber = $issueNum
                    Title = $dep.issue.title
                    Priority = $dep.priority
                    Component = $dep.component
                    EstimatedEffort = $dep.estimatedEffort
                    DependsOnCount = $dep.dependsOn.Count
                    BlocksCount = $dep.blocks.Count
                    DependsOn = ($dep.dependsOn -join "; ")
                    Blocks = ($dep.blocks -join "; ")
                }
            }
            $csvData | Export-Csv -Path $FilePath -NoTypeInformation -Encoding ASCII
        }
        
        "risks" {
            $csvData = foreach ($risk in $Data) {
                [PSCustomObject]@{
                    Type = $risk.type
                    Severity = $risk.severity
                    Issue = $risk.issue
                    Title = $risk.title
                    Description = $risk.description
                    Impact = $risk.impact
                    Mitigation = $risk.mitigation
                }
            }
            $csvData | Export-Csv -Path $FilePath -NoTypeInformation -Encoding ASCII
        }
    }
}

# ================================================================================
# MAIN EXECUTION
# ================================================================================

Write-Host ""
Write-Host "DexBot Automated Planning Analysis" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green

Write-PlanningLog "Starting automated planning analysis: $Action"
Write-PlanningLog "Configuration: TimeHorizon=$TimeHorizon, Confidence=$Confidence, Output=$OutputFormat"

# Check GitHub CLI availability
if (-not (Test-GitHubCLI)) {
    exit 1
}

try {
    # Get GitHub data
    $githubData = Get-GitHubData
    
    $totalItems = $githubData.issues.Count + $githubData.prs.Count
    Write-PlanningLog "Fetched $totalItems items ($($githubData.issues.Count) issues, $($githubData.prs.Count) PRs)"
    
    # Determine team size if not specified
    if ($TeamSize -eq 0) {
        # Simple heuristic based on recent activity
        $recentContributors = @()
        if ($githubData.issues -and $githubData.issues.Count -gt 0) {
            foreach ($issue in $githubData.issues) {
                if ($issue.author -and $issue.author.login) {
                    $recentContributors += $issue.author.login
                }
                if ($issue.assignees -and $issue.assignees.Count -gt 0) {
                    foreach ($assignee in $issue.assignees) {
                        if ($assignee.login) {
                            $recentContributors += $assignee.login
                        }
                    }
                }
            }
        }
        $TeamSize = [math]::Max(1, ($recentContributors | Select-Object -Unique).Count)
        Write-PlanningLog "Auto-detected team size: $TeamSize developers"
    }
    
    $result = $null
    
    switch ($Action) {
        "dependencies" {
            Write-PlanningLog "Starting dependency analysis"
            $result = Get-IssueDependencies -GitHubData $githubData
            Write-PlanningLog "Dependency analysis complete: $($result.Keys.Count) issues analyzed" "SUCCESS"
        }
        
        "timeline" {
            Write-PlanningLog "Starting timeline analysis"
            $dependencies = Get-IssueDependencies -GitHubData $githubData
            $result = Get-TimelinePredictions -Dependencies $dependencies -GitHubData $githubData -TimeHorizon $TimeHorizon -TeamSize $TeamSize
            Write-PlanningLog "Timeline analysis complete: projected completion $($result.projectedCompletion.ToString('yyyy-MM-dd'))" "SUCCESS"
        }
        
        "resources" {
            Write-PlanningLog "Starting resource allocation analysis"
            $dependencies = Get-IssueDependencies -GitHubData $githubData
            $timeline = Get-TimelinePredictions -Dependencies $dependencies -GitHubData $githubData -TimeHorizon $TimeHorizon -TeamSize $TeamSize
            $result = Get-ResourceAllocation -Dependencies $dependencies -TimelinePredictions $timeline -TeamSize $TeamSize
            Write-PlanningLog "Resource allocation analysis complete: $($result.allocation.Keys.Count) components analyzed" "SUCCESS"
        }
        
        "risks" {
            Write-PlanningLog "Starting risk analysis"
            $dependencies = Get-IssueDependencies -GitHubData $githubData
            $timeline = Get-TimelinePredictions -Dependencies $dependencies -GitHubData $githubData -TimeHorizon $TimeHorizon -TeamSize $TeamSize
            $resources = Get-ResourceAllocation -Dependencies $dependencies -TimelinePredictions $timeline -TeamSize $TeamSize
            $result = Get-ProjectRisks -Dependencies $dependencies -TimelinePredictions $timeline -ResourceAllocation $resources
            Write-PlanningLog "Risk analysis complete: $($result.Count) risks identified" "SUCCESS"
        }
        
        "plan" {
            Write-PlanningLog "Starting comprehensive planning analysis"
            $dependencies = Get-IssueDependencies -GitHubData $githubData
            $timeline = Get-TimelinePredictions -Dependencies $dependencies -GitHubData $githubData -TimeHorizon $TimeHorizon -TeamSize $TeamSize
            $resources = Get-ResourceAllocation -Dependencies $dependencies -TimelinePredictions $timeline -TeamSize $TeamSize
            $risks = Get-ProjectRisks -Dependencies $dependencies -TimelinePredictions $timeline -ResourceAllocation $resources
            
            $result = @{
                dependencies = $dependencies
                timeline = $timeline
                resources = $resources
                risks = $risks
                summary = @{
                    totalIssues = $dependencies.Keys.Count
                    projectedCompletion = $timeline.projectedCompletion
                    totalEffort = $resources.totalEffort
                    highRisks = ($risks | Where-Object { $_.severity -eq "high" }).Count
                }
            }
            Write-PlanningLog "Comprehensive planning analysis complete" "SUCCESS"
        }
    }
    
    # Export results
    $outputFile = Export-PlanningAnalysis -Action $Action -Data $result -OutputPath $OutputPath -OutputFormat $OutputFormat
    
    # Interactive mode explanations
    if ($Interactive) {
        Write-Host ""
        Write-Host "=== INTERACTIVE ANALYSIS EXPLANATION ===" -ForegroundColor Cyan
        
        switch ($Action) {
            "dependencies" {
                Write-Host "Dependency analysis identifies:" -ForegroundColor Yellow
                Write-Host "- Direct blocking relationships between issues" -ForegroundColor White
                Write-Host "- Complexity based on issue content and labels" -ForegroundColor White
                Write-Host "- Effort estimates using heuristic scoring" -ForegroundColor White
                Write-Host "- Component classifications for resource planning" -ForegroundColor White
            }
            
            "timeline" {
                Write-Host "Timeline predictions consider:" -ForegroundColor Yellow
                Write-Host "- Historical team velocity and cycle times" -ForegroundColor White
                Write-Host "- Issue dependencies and critical path analysis" -ForegroundColor White
                Write-Host "- Priority-based scheduling optimization" -ForegroundColor White
                Write-Host "- Team capacity and parallel work opportunities" -ForegroundColor White
            }
            
            "risks" {
                Write-Host "Risk analysis evaluates:" -ForegroundColor Yellow
                Write-Host "- Dependency complexity and coordination risks" -ForegroundColor White
                Write-Host "- Resource concentration and bottlenecks" -ForegroundColor White
                Write-Host "- Timeline feasibility and delivery risks" -ForegroundColor White
                Write-Host "- Scope and effort estimation accuracy" -ForegroundColor White
            }
            
            "plan" {
                Write-Host "Comprehensive planning provides:" -ForegroundColor Yellow
                Write-Host "- Integrated view of dependencies, timeline, and resources" -ForegroundColor White
                Write-Host "- Critical milestones and delivery checkpoints" -ForegroundColor White
                Write-Host "- Risk-adjusted recommendations and contingencies" -ForegroundColor White
                Write-Host "- Actionable insights for project optimization" -ForegroundColor White
            }
        }
        
        Write-Host ""
        Write-Host "Review the generated report for detailed analysis and recommendations." -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "Analysis completed successfully!" -ForegroundColor Green
    Write-Host "Output file: $outputFile" -ForegroundColor Cyan
    Write-Host "Log file: $LogFile" -ForegroundColor Cyan
}
catch {
    Write-PlanningLog "Error during analysis: $($_.Exception.Message)" "ERROR"
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

#!/usr/bin/env powershell
<#
.SYNOPSIS
    Smart Assignment System for GitHub Issues workflow optimization

.DESCRIPTION
    Analyzes developer availability, skill sets, and workload to suggest optimal
    issue assignments. Integrates with GitHub API and workflow systems to provide
    intelligent assignment recommendations with capacity planning.

.PARAMETER Action
    Assignment analysis type to perform:
    - suggest: Suggest assignments for open issues
    - capacity: Analyze team capacity and workload
    - skills: Analyze developer skills and expertise
    - workload: Current workload analysis by developer
    - optimize: Optimize current assignments for balance

.PARAMETER IssueNumber
    Specific issue number to analyze for assignment suggestions

.PARAMETER Developer
    Specific developer to analyze (GitHub username)

.PARAMETER Component
    Filter by component for specialized assignment analysis

.PARAMETER Priority
    Filter by priority level (low, medium, high, critical)

.PARAMETER OutputPath
    Path where analysis results will be saved (default: current directory)

.PARAMETER OutputFormat
    Output format: markdown, html, json, or csv

.PARAMETER Interactive
    Run in interactive mode with detailed explanations

.PARAMETER TeamSize
    Expected team size for capacity planning (default: auto-detect)

.PARAMETER WeeksAhead
    Weeks ahead for capacity forecasting (default: 4)

.PARAMETER IncludeExternal
    Include external contributors in analysis

.EXAMPLE
    .\suggest_assignment.ps1 -Action suggest -Component combat
    .\suggest_assignment.ps1 -Action capacity -WeeksAhead 8 -Interactive
    .\suggest_assignment.ps1 -Action optimize -OutputFormat html
    .\suggest_assignment.ps1 -Action skills -Developer johndoe
#>

param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("suggest", "capacity", "skills", "workload", "optimize")]
    [string]$Action,
    
    [int]$IssueNumber,
    
    [string]$Developer,
    
    [string]$Component,
    
    [ValidateSet("low", "medium", "high", "critical")]
    [string]$Priority,
    
    [string]$OutputPath = ".",
    
    [ValidateSet("markdown", "html", "json", "csv")]
    [string]$OutputFormat = "markdown",
    
    [switch]$Interactive,
    
    [int]$TeamSize = 0,
    
    [int]$WeeksAhead = 4,
    
    [switch]$IncludeExternal
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
$LogFile = "tmp/assignment_analysis_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

function Write-AssignmentLog {
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
            Write-AssignmentLog "GitHub CLI detected: gh version $version"
            return $true
        }
    }
    catch {
        Write-AssignmentLog "GitHub CLI not available: $($_.Exception.Message)" "ERROR"
    }
    
    Write-AssignmentLog "GitHub CLI (gh) is required but not available" "ERROR"
    Write-Host "Please install GitHub CLI: https://cli.github.com/" -ForegroundColor Red
    return $false
}

function Get-GitHubData {
    param(
        [switch]$RefreshCache
    )
    
    $cacheFile = "tmp/github_data_cache.json"
    $cacheAge = if (Test-Path $cacheFile) { 
        (Get-Date) - (Get-Item $cacheFile).LastWriteTime 
    } else { 
        [TimeSpan]::MaxValue 
    }
    
    # Use cache if less than 15 minutes old and refresh not requested
    if (-not $RefreshCache -and $cacheAge.TotalMinutes -lt 15) {
        Write-AssignmentLog "Using cached GitHub data (age: $([math]::Round($cacheAge.TotalMinutes, 1)) minutes)"
        return Get-Content $cacheFile -Raw | ConvertFrom-Json
    }
    
    Write-AssignmentLog "Fetching GitHub data (issues, PRs, and team info)..."
    
    try {
        # Get repository information first
        $repoInfo = gh repo view --json owner,name 2>$null
        if (-not $repoInfo) {
            Write-AssignmentLog "Not in a Git repository or no GitHub remote configured" "ERROR"
            throw "This script must be run from within a Git repository with GitHub remote"
        }
        
        $repo = $repoInfo | ConvertFrom-Json
        $repoFullName = "$($repo.owner.login)/$($repo.name)"
        Write-AssignmentLog "Analyzing repository: $repoFullName"
        
        # Fetch issues and PRs
        $issues = gh issue list --repo $repoFullName --state all --limit 1000 --json number,title,state,createdAt,closedAt,assignees,labels,author
        $prs = gh pr list --repo $repoFullName --state all --limit 1000 --json number,title,state,createdAt,closedAt,assignees,labels,author,reviews
        
        # Fetch repository contributors
        $contributors = @()
        try {
            $contributorsJson = gh api repos/$repoFullName/contributors
            $contributors = ($contributorsJson | ConvertFrom-Json).login
        }
        catch {
            Write-AssignmentLog "Could not fetch contributors: $($_.Exception.Message)" "WARN"
        }
        
        # Fetch team members if available (organization repos)
        $teamMembers = @()
        try {
            $teams = gh api orgs/$($repo.owner.login)/teams --jq '.[].slug' 2>$null
            if ($teams) {
                foreach ($team in $teams) {
                    $members = gh api orgs/$($repo.owner.login)/teams/$team/members --jq '.[].login' 2>$null
                    if ($members) {
                        $teamMembers += $members
                    }
                }
            }
        }
        catch {
            Write-AssignmentLog "Team information not available (private org or personal repo)" "INFO"
        }
        
        $data = @{
            issues = if ($issues) { $issues | ConvertFrom-Json } else { @() }
            prs = if ($prs) { $prs | ConvertFrom-Json } else { @() }
            contributors = $contributors
            teamMembers = $teamMembers
            repository = $repoFullName
            fetchedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        }
        
        # Cache the data
        $data | ConvertTo-Json -Depth 10 | Set-Content $cacheFile -Encoding ASCII
        Write-AssignmentLog "Cached GitHub data for future use"
        
        return $data
    }
    catch {
        Write-AssignmentLog "Error fetching GitHub data: $($_.Exception.Message)" "ERROR"
        throw
    }
}

function Get-DeveloperWorkload {
    param(
        [object]$GitHubData,
        [string]$TimeRange = "30d"
    )
    
    $cutoffDate = switch ($TimeRange) {
        "7d" { (Get-Date).AddDays(-7) }
        "30d" { (Get-Date).AddDays(-30) }
        "90d" { (Get-Date).AddDays(-90) }
        default { (Get-Date).AddDays(-30) }
    }
    
    Write-AssignmentLog "Analyzing developer workload for time range: $TimeRange"
    
    $workload = @{}
    $allDevelopers = @()
    
    # Collect all developers from issues and PRs
    foreach ($issue in $GitHubData.issues) {
        if ($issue.author.login) {
            $allDevelopers += $issue.author.login
        }
        foreach ($assignee in $issue.assignees) {
            $allDevelopers += $assignee.login
        }
    }
    
    foreach ($pr in $GitHubData.prs) {
        if ($pr.author.login) {
            $allDevelopers += $pr.author.login
        }
        foreach ($assignee in $pr.assignees) {
            $allDevelopers += $assignee.login
        }
    }
    
    # Add contributors and team members
    $allDevelopers += $GitHubData.contributors
    $allDevelopers += $GitHubData.teamMembers
    
    # Remove duplicates and initialize workload tracking
    $uniqueDevelopers = $allDevelopers | Select-Object -Unique | Where-Object { $_ }
    
    foreach ($dev in $uniqueDevelopers) {
        $workload[$dev] = @{
            assignedIssues = 0
            assignedPRs = 0
            createdIssues = 0
            createdPRs = 0
            totalWorkload = 0
            availabilityScore = 100
            skillAreas = @()
            recentActivity = 0
        }
    }
    
    # Calculate current assignments
    foreach ($issue in $GitHubData.issues) {
        if ($issue.state -eq "open") {
            foreach ($assignee in $issue.assignees) {
                if ($workload.ContainsKey($assignee.login)) {
                    $workload[$assignee.login].assignedIssues = $workload[$assignee.login].assignedIssues + 1
                    $workload[$assignee.login].totalWorkload = $workload[$assignee.login].totalWorkload + 2  # Weight issues as 2 points
                }
            }
        }
        
        # Track recent activity
        try {
            $createdDate = [DateTime]::Parse($issue.createdAt)
            if ($createdDate -gt $cutoffDate -and $issue.author.login -and $workload.ContainsKey($issue.author.login)) {
                $workload[$issue.author.login].createdIssues = $workload[$issue.author.login].createdIssues + 1
                $workload[$issue.author.login].recentActivity = $workload[$issue.author.login].recentActivity + 1
            }
        }
        catch {
            # Skip items with invalid dates
            Write-AssignmentLog "Skipping issue with invalid date: $($issue.createdAt)" "WARN"
        }
    }
    
    foreach ($pr in $GitHubData.prs) {
        if ($pr.state -eq "open") {
            foreach ($assignee in $pr.assignees) {
                if ($workload.ContainsKey($assignee.login)) {
                    $workload[$assignee.login].assignedPRs = $workload[$assignee.login].assignedPRs + 1
                    $workload[$assignee.login].totalWorkload = $workload[$assignee.login].totalWorkload + 3  # Weight PRs as 3 points
                }
            }
        }
        
        # Track recent activity
        try {
            $createdDate = [DateTime]::Parse($pr.createdAt)
            if ($createdDate -gt $cutoffDate -and $pr.author.login -and $workload.ContainsKey($pr.author.login)) {
                $workload[$pr.author.login].createdPRs = $workload[$pr.author.login].createdPRs + 1
                $workload[$pr.author.login].recentActivity = $workload[$pr.author.login].recentActivity + 1
            }
        }
        catch {
            # Skip items with invalid dates
            Write-AssignmentLog "Skipping PR with invalid date: $($pr.createdAt)" "WARN"
        }
    }
    
    # Calculate availability scores (higher is more available)
    foreach ($dev in $workload.Keys) {
        $totalWork = $workload[$dev].totalWorkload
        $recentActivity = $workload[$dev].recentActivity
        
        # Base availability score starts at 100
        $availabilityScore = 100
        
        # Reduce score based on current workload
        $availabilityScore -= ($totalWork * 10)  # 10 points per workload unit
        
        # Adjust for recent activity level
        if ($recentActivity -gt 5) {
            $availabilityScore -= 20  # High activity reduces availability
        }
        elseif ($recentActivity -eq 0) {
            $availabilityScore -= 30  # No recent activity might indicate unavailability
        }
        
        # Ensure score doesn't go below 0
        $workload[$dev].availabilityScore = [Math]::Max(0, $availabilityScore)
    }
    
    Write-AssignmentLog "Analyzed workload for $($uniqueDevelopers.Count) developers"
    return $workload
}

function Get-DeveloperSkills {
    param(
        [object]$GitHubData
    )
    
    Write-AssignmentLog "Analyzing developer skills and expertise areas"
    
    $skills = @{}
    
    # Analyze skills based on issue/PR labels and components
    foreach ($issue in $GitHubData.issues) {
        if ($issue.author.login) {
            if (-not $skills.ContainsKey($issue.author.login)) {
                $skills[$issue.author.login] = @{}
            }
            
            foreach ($label in $issue.labels) {
                $labelName = $label.name
                
                # Map labels to skill areas
                $skillArea = switch -Regex ($labelName) {
                    "^(component|system):" { $labelName }
                    "^priority:" { "priority-management" }
                    "^status:" { "workflow-management" }
                    "^type:" { $labelName }
                    "ui|interface|gump" { "ui-development" }
                    "core|system" { "core-development" }
                    "config|settings" { "configuration" }
                    "test|testing" { "testing" }
                    "docs|documentation" { "documentation" }
                    "performance|optimization" { "performance" }
                    "bug|fix" { "bug-fixing" }
                    "feature|enhancement" { "feature-development" }
                    default { "general" }
                }
                
                if (-not $skills[$issue.author.login].ContainsKey($skillArea)) {
                    $skills[$issue.author.login][$skillArea] = 0
                }
                $skills[$issue.author.login][$skillArea] = $skills[$issue.author.login][$skillArea] + 1
            }
        }
    }
    
    # Similar analysis for PRs
    foreach ($pr in $GitHubData.prs) {
        if ($pr.author.login) {
            if (-not $skills.ContainsKey($pr.author.login)) {
                $skills[$pr.author.login] = @{}
            }
            
            foreach ($label in $pr.labels) {
                $labelName = $label.name
                
                $skillArea = switch -Regex ($labelName) {
                    "^(component|system):" { $labelName }
                    "^priority:" { "priority-management" }
                    "^status:" { "workflow-management" }
                    "^type:" { $labelName }
                    "ui|interface|gump" { "ui-development" }
                    "core|system" { "core-development" }
                    "config|settings" { "configuration" }
                    "test|testing" { "testing" }
                    "docs|documentation" { "documentation" }
                    "performance|optimization" { "performance" }
                    "bug|fix" { "bug-fixing" }
                    "feature|enhancement" { "feature-development" }
                    default { "general" }
                }
                
                if (-not $skills[$pr.author.login].ContainsKey($skillArea)) {
                    $skills[$pr.author.login][$skillArea] = 0
                }
                $skills[$pr.author.login][$skillArea] = $skills[$pr.author.login][$skillArea] + 2  # PRs weighted higher for skill assessment
            }
        }
    }
    
    Write-AssignmentLog "Analyzed skills for $($skills.Keys.Count) developers"
    return $skills
}

function Get-AssignmentSuggestions {
    param(
        [object]$GitHubData,
        [hashtable]$Workload,
        [hashtable]$Skills,
        [int]$IssueNumber = 0,
        [string]$Component = "",
        [string]$Priority = ""
    )
    
    Write-AssignmentLog "Generating assignment suggestions"
    
    # Filter issues for assignment
    $openIssues = $GitHubData.issues | Where-Object { $_.state -eq "open" }
    
    if ($IssueNumber -gt 0) {
        $openIssues = $openIssues | Where-Object { $_.number -eq $IssueNumber }
    }
    
    if ($Component) {
        $openIssues = $openIssues | Where-Object { 
            $_.labels | Where-Object { $_.name -like "component:$Component*" -or $_.name -like "system:$Component*" }
        }
    }
    
    if ($Priority) {
        $openIssues = $openIssues | Where-Object { 
            $_.labels | Where-Object { $_.name -eq "priority:$Priority" }
        }
    }
    
    $suggestions = @()
    
    foreach ($issue in $openIssues) {
        # Skip if already assigned
        if ($issue.assignees.Count -gt 0) {
            continue
        }
        
        $issueSkillRequirements = @()
        foreach ($label in $issue.labels) {
            $labelName = $label.name
            
            $skillArea = switch -Regex ($labelName) {
                "^(component|system):" { $labelName }
                "ui|interface|gump" { "ui-development" }
                "core|system" { "core-development" }
                "config|settings" { "configuration" }
                "test|testing" { "testing" }
                "docs|documentation" { "documentation" }
                "performance|optimization" { "performance" }
                "bug|fix" { "bug-fixing" }
                "feature|enhancement" { "feature-development" }
                default { "general" }
            }
            
            if ($skillArea -ne "general") {
                $issueSkillRequirements += $skillArea
            }
        }
        
        # Score developers for this issue
        $developerScores = @()
        
        foreach ($dev in $Workload.Keys) {
            $score = $Workload[$dev].availabilityScore
            
            # Bonus for relevant skills
            if ($Skills.ContainsKey($dev)) {
                foreach ($skill in $issueSkillRequirements) {
                    if ($Skills[$dev].ContainsKey($skill)) {
                        $score += ($Skills[$dev][$skill] * 5)  # 5 points per skill level
                    }
                }
            }
            
            # Penalty for high current workload
            $score -= ($Workload[$dev].totalWorkload * 5)
            
            $developerScores += @{
                developer = $dev
                score = $score
                availability = $Workload[$dev].availabilityScore
                currentWork = $Workload[$dev].totalWorkload
                relevantSkills = ($issueSkillRequirements | Where-Object { 
                    $Skills.ContainsKey($dev) -and $Skills[$dev].ContainsKey($_) 
                })
            }
        }
        
        # Sort by score (highest first) and take top 3
        $topCandidates = $developerScores | Sort-Object score -Descending | Select-Object -First 3
        
        $suggestions += @{
            issue = $issue
            candidates = $topCandidates
            skillRequirements = $issueSkillRequirements
        }
    }
    
    Write-AssignmentLog "Generated suggestions for $($suggestions.Count) unassigned issues"
    return $suggestions
}

function Export-AssignmentAnalysis {
    param(
        [string]$Action,
        [object]$Data,
        [string]$OutputPath,
        [string]$OutputFormat
    )
    
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $filename = "assignment_${Action}_${timestamp}.${OutputFormat}"
    $filepath = Join-Path $OutputPath $filename
    
    Write-AssignmentLog "Exporting $Action analysis to $filepath"
    
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
    
    Write-AssignmentLog "Analysis exported successfully to: $filepath" "SUCCESS"
    return $filepath
}

function Export-MarkdownReport {
    param(
        [string]$Action,
        [object]$Data,
        [string]$FilePath
    )
    
    $content = @"
# GitHub Issues Smart Assignment Analysis Report

**Generated**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")  
**Analysis Type**: $Action  

"@

    switch ($Action) {
        "suggest" {
            $content += @"
## Assignment Suggestions

"@
            foreach ($suggestion in $Data) {
                $content += @"
### Issue #$($suggestion.issue.number): $($suggestion.issue.title)

**Skill Requirements**: $($suggestion.skillRequirements -join ", ")

**Recommended Candidates**:
"@
                foreach ($candidate in $suggestion.candidates) {
                    $skills = $candidate.relevantSkills -join ", "
                    if (-not $skills) { $skills = "General" }
                    
                    $content += @"
- **$($candidate.developer)** (Score: $($candidate.score), Availability: $($candidate.availability)%, Current Work: $($candidate.currentWork))
  - Relevant Skills: $skills

"@
                }
                $content += "`n---`n`n"
            }
        }
        
        "capacity" {
            $content += @"
## Team Capacity Analysis

### Overall Metrics
- **Team Size**: $($Data.teamSize)
- **Average Workload**: $([math]::Round($Data.averageWorkload, 2))
- **Total Capacity**: $($Data.totalCapacity)%

### Developer Capacity
"@
            foreach ($dev in $Data.developers.Keys) {
                $devData = $Data.developers[$dev]
                $content += @"
- **$dev**: $($devData.availabilityScore)% available, $($devData.totalWorkload) work units
"@
            }
        }
        
        "workload" {
            $content += @"
## Workload Analysis

"@
            foreach ($dev in $Data.Keys) {
                $devData = $Data[$dev]
                $content += @"
### $dev
- **Assigned Issues**: $($devData.assignedIssues)
- **Assigned PRs**: $($devData.assignedPRs)
- **Total Workload**: $($devData.totalWorkload) units
- **Availability Score**: $($devData.availabilityScore)%
- **Recent Activity**: $($devData.recentActivity) items

"@
            }
        }
        
        "skills" {
            $content += @"
## Developer Skills Analysis

"@
            foreach ($dev in $Data.Keys) {
                $devSkills = $Data[$dev]
                $content += @"
### $dev
"@
                foreach ($skill in $devSkills.Keys) {
                    $content += @"
- **$skill**: $($devSkills[$skill]) experience points
"@
                }
                $content += "`n"
            }
        }
    }
    
    $content += @"

---

**Generated by**: DexBot Smart Assignment System  
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
    <title>Smart Assignment Analysis - $Action</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1, h2, h3 { color: #333; }
        .summary { background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .developer { background: #e8f4fd; padding: 10px; margin: 5px 0; border-radius: 3px; }
        .metric { display: inline-block; margin: 5px 15px 5px 0; }
        .score { font-weight: bold; color: #2e8b57; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>GitHub Issues Smart Assignment Analysis</h1>
    <div class="summary">
        <strong>Generated:</strong> $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")<br>
        <strong>Analysis Type:</strong> $Action
    </div>
"@

    switch ($Action) {
        "suggest" {
            $html += "<h2>Assignment Suggestions</h2>"
            foreach ($suggestion in $Data) {
                $html += @"
                <h3>Issue #$($suggestion.issue.number): $($suggestion.issue.title)</h3>
                <p><strong>Skill Requirements:</strong> $($suggestion.skillRequirements -join ", ")</p>
                <div class="candidates">
"@
                foreach ($candidate in $suggestion.candidates) {
                    $skills = $candidate.relevantSkills -join ", "
                    if (-not $skills) { $skills = "General" }
                    
                    $html += @"
                    <div class="developer">
                        <strong>$($candidate.developer)</strong> 
                        <span class="score">(Score: $($candidate.score))</span><br>
                        <span class="metric">Availability: $($candidate.availability)%</span>
                        <span class="metric">Current Work: $($candidate.currentWork)</span><br>
                        <em>Skills: $skills</em>
                    </div>
"@
                }
                $html += "</div><hr>"
            }
        }
        
        "capacity" {
            $html += @"
            <h2>Team Capacity Analysis</h2>
            <div class="summary">
                <span class="metric">Team Size: $($Data.teamSize)</span>
                <span class="metric">Average Workload: $([math]::Round($Data.averageWorkload, 2))</span>
                <span class="metric">Total Capacity: $($Data.totalCapacity)%</span>
            </div>
            <h3>Developer Capacity</h3>
"@
            foreach ($dev in $Data.developers.Keys) {
                $devData = $Data.developers[$dev]
                $html += @"
                <div class="developer">
                    <strong>$dev</strong>: $($devData.availabilityScore)% available, $($devData.totalWorkload) work units
                </div>
"@
            }
        }
    }
    
    $html += @"
    <hr>
    <p><em>Generated by: DexBot Smart Assignment System</em></p>
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
        "workload" {
            $csvData = foreach ($dev in $Data.Keys) {
                $devData = $Data[$dev]
                [PSCustomObject]@{
                    Developer = $dev
                    AssignedIssues = $devData.assignedIssues
                    AssignedPRs = $devData.assignedPRs
                    TotalWorkload = $devData.totalWorkload
                    AvailabilityScore = $devData.availabilityScore
                    RecentActivity = $devData.recentActivity
                }
            }
            $csvData | Export-Csv -Path $FilePath -NoTypeInformation -Encoding ASCII
        }
        
        "suggest" {
            $csvData = foreach ($suggestion in $Data) {
                foreach ($candidate in $suggestion.candidates) {
                    [PSCustomObject]@{
                        IssueNumber = $suggestion.issue.number
                        IssueTitle = $suggestion.issue.title
                        Developer = $candidate.developer
                        Score = $candidate.score
                        Availability = $candidate.availability
                        CurrentWork = $candidate.currentWork
                        RelevantSkills = ($candidate.relevantSkills -join "; ")
                    }
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
Write-Host "DexBot Smart Assignment System" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Green

Write-AssignmentLog "Starting smart assignment analysis: $Action"
Write-AssignmentLog "Configuration: Output=$OutputFormat, WeeksAhead=$WeeksAhead"

# Check GitHub CLI availability
if (-not (Test-GitHubCLI)) {
    exit 1
}

try {
    # Get GitHub data
    $githubData = Get-GitHubData
    
    $totalItems = $githubData.issues.Count + $githubData.prs.Count
    Write-AssignmentLog "Fetched $totalItems items ($($githubData.issues.Count) issues, $($githubData.prs.Count) PRs)"
    
    # Get workload and skills analysis
    $workload = Get-DeveloperWorkload -GitHubData $githubData
    $skills = Get-DeveloperSkills -GitHubData $githubData
    
    $result = $null
    
    switch ($Action) {
        "suggest" {
            Write-AssignmentLog "Starting assignment suggestion analysis"
            $result = Get-AssignmentSuggestions -GitHubData $githubData -Workload $workload -Skills $skills -IssueNumber $IssueNumber -Component $Component -Priority $Priority
            Write-AssignmentLog "Generated suggestions for $($result.Count) issues" "SUCCESS"
        }
        
        "capacity" {
            Write-AssignmentLog "Starting team capacity analysis"
            $teamSize = if ($TeamSize -gt 0) { $TeamSize } else { $workload.Keys.Count }
            
            # Calculate averages safely
            $totalCapacity = 0
            $avgWorkload = 0
            $devCount = 0
            
            foreach ($dev in $workload.Keys) {
                $totalCapacity += $workload[$dev].availabilityScore
                $avgWorkload += $workload[$dev].totalWorkload
                $devCount++
            }
            
            if ($devCount -gt 0) {
                $totalCapacity = [math]::Round($totalCapacity / $devCount, 1)
                $avgWorkload = [math]::Round($avgWorkload / $devCount, 2)
            }
            
            $result = @{
                teamSize = $teamSize
                totalCapacity = $totalCapacity
                averageWorkload = $avgWorkload
                developers = $workload
                weeksForecast = $WeeksAhead
            }
            Write-AssignmentLog "Team capacity analysis complete: $teamSize developers, $totalCapacity% average capacity" "SUCCESS"
        }
        
        "skills" {
            Write-AssignmentLog "Starting skills analysis"
            $result = $skills
            Write-AssignmentLog "Skills analysis complete for $($skills.Keys.Count) developers" "SUCCESS"
        }
        
        "workload" {
            Write-AssignmentLog "Starting workload analysis"
            $result = $workload
            Write-AssignmentLog "Workload analysis complete for $($workload.Keys.Count) developers" "SUCCESS"
        }
        
        "optimize" {
            Write-AssignmentLog "Starting assignment optimization analysis"
            # This would implement optimization logic for rebalancing assignments
            $suggestions = Get-AssignmentSuggestions -GitHubData $githubData -Workload $workload -Skills $skills
            
            # Find overloaded developers and suggest reassignments
            $overloaded = $workload.GetEnumerator() | Where-Object { $_.Value.totalWorkload -gt 8 }
            $underloaded = $workload.GetEnumerator() | Where-Object { $_.Value.totalWorkload -lt 3 -and $_.Value.availabilityScore -gt 50 }
            
            $result = @{
                suggestions = $suggestions
                overloaded = $overloaded
                underloaded = $underloaded
                rebalanceOpportunities = ($overloaded.Count + $underloaded.Count)
            }
            Write-AssignmentLog "Optimization analysis complete: $($overloaded.Count) overloaded, $($underloaded.Count) underloaded developers" "SUCCESS"
        }
    }
    
    # Export results
    $outputFile = Export-AssignmentAnalysis -Action $Action -Data $result -OutputPath $OutputPath -OutputFormat $OutputFormat
    
    # Interactive mode explanations
    if ($Interactive) {
        Write-Host ""
        Write-Host "=== INTERACTIVE ANALYSIS EXPLANATION ===" -ForegroundColor Cyan
        
        switch ($Action) {
            "suggest" {
                Write-Host "Assignment suggestions are based on:" -ForegroundColor Yellow
                Write-Host "- Developer availability (current workload)" -ForegroundColor White
                Write-Host "- Skill match with issue requirements" -ForegroundColor White
                Write-Host "- Recent activity levels" -ForegroundColor White
                Write-Host "- Component expertise history" -ForegroundColor White
            }
            
            "capacity" {
                Write-Host "Capacity analysis considers:" -ForegroundColor Yellow
                Write-Host "- Current assignment load per developer" -ForegroundColor White
                Write-Host "- Historical activity patterns" -ForegroundColor White
                Write-Host "- Projected capacity for $WeeksAhead weeks ahead" -ForegroundColor White
            }
            
            "workload" {
                Write-Host "Workload scoring system:" -ForegroundColor Yellow
                Write-Host "- Issues: 2 points each" -ForegroundColor White
                Write-Host "- PRs: 3 points each" -ForegroundColor White
                Write-Host "- Availability: 100 - (workload * 10) - activity_penalty" -ForegroundColor White
            }
        }
        
        Write-Host ""
        Write-Host "Review the generated report for detailed recommendations." -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "Analysis completed successfully!" -ForegroundColor Green
    Write-Host "Output file: $outputFile" -ForegroundColor Cyan
    Write-Host "Log file: $LogFile" -ForegroundColor Cyan
}
catch {
    Write-AssignmentLog "Error during analysis: $($_.Exception.Message)" "ERROR"
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Performance Profiling for Full Automation Suite
# Analyzes performance metrics and identifies optimization opportunities

param(
    [string]$Repository,
    [string]$OutputPath = "reports\performance_profile_$(Get-Date -Format 'yyyyMMdd_HHmmss').md",
    [int]$Iterations = 3,
    [string]$Token = $env:GITHUB_TOKEN
)

# Verify GitHub token
if (-not $Token) {
    Write-Host "GitHub token not found. Please set GITHUB_TOKEN environment variable or provide via -Token parameter." -ForegroundColor Red
    exit 1
}

# Ensure PowerShellForGitHub module is installed
if (-not (Get-Module -ListAvailable -Name PowerShellForGitHub)) {
    Write-Host "Installing PowerShellForGitHub module..." -ForegroundColor Yellow
    Install-Module -Name PowerShellForGitHub -Scope CurrentUser -Force
}

# Import module
Import-Module PowerShellForGitHub

# Setup authentication
try {
    Set-GitHubAuthentication -Token $Token
    Write-Host "GitHub authentication configured successfully" -ForegroundColor Green
} catch {
    Write-Host "Failed to configure GitHub authentication: $_" -ForegroundColor Red
    exit 1
}

# Set default repository if not provided
if (-not $Repository) {
    # Get current user
    $currentUser = Get-GitHubUser
    $ownerName = $currentUser.login
    
    # Try to use test repositories if available
    $testRepos = @("dexbot-test-small", "dexbot-test-medium", "dexbot-test-large")
    
    foreach ($repo in $testRepos) {
        try {
            Get-GitHubRepository -OwnerName $ownerName -RepositoryName $repo -ErrorAction SilentlyContinue | Out-Null
            $Repository = "$ownerName/$repo"
            Write-Host "Using test repository: $Repository" -ForegroundColor Yellow
            break
        } catch {
            # Repository not found, try next one
        }
    }
    
    if (-not $Repository) {
        Write-Host "No test repositories found. Please specify a repository using the -Repository parameter." -ForegroundColor Red
        exit 1
    }
}

# Path to full automation suite script
$scriptPath = Join-Path $PSScriptRoot "full_automation_suite.ps1"

# Initialize results storage
$results = @{}

# Function to profile a command
function Measure-Command2 {
    param (
        [ScriptBlock]$ScriptBlock,
        [int]$Iterations = 3
    )
    
    $measurements = @()
    $exceptions = @()
    $outputs = @()
    
    for ($i = 1; $i -le $Iterations; $i++) {
        Write-Host "  Running iteration $i of $Iterations..." -ForegroundColor Gray -NoNewline
        $startMemory = [System.GC]::GetTotalMemory($true)
        $startTime = Get-Date
        
        try {
            $output = & $ScriptBlock
            $outputs += $output
            Write-Host " Success" -ForegroundColor Green
        } catch {
            $exceptions += $_
            Write-Host " Failed: $_" -ForegroundColor Red
        }
        
        $endTime = Get-Date
        $endMemory = [System.GC]::GetTotalMemory($false)
        
        $duration = $endTime - $startTime
        $memoryUsed = $endMemory - $startMemory
        
        $measurements += [PSCustomObject]@{
            Iteration = $i
            Duration = $duration
            TotalSeconds = $duration.TotalSeconds
            MemoryUsed = $memoryUsed
            MemoryUsedMB = [math]::Round($memoryUsed / 1MB, 2)
            StartTime = $startTime
            EndTime = $endTime
            Success = ($exceptions.Count -lt $i)
        }
        
        # Force garbage collection
        [System.GC]::Collect()
        Start-Sleep -Seconds 1
    }
    
    # Calculate statistics
    $successfulRuns = $measurements | Where-Object Success -eq $true
    
    if ($successfulRuns.Count -gt 0) {
        $avgDuration = $successfulRuns | Measure-Object -Property TotalSeconds -Average | Select-Object -ExpandProperty Average
        $minDuration = $successfulRuns | Measure-Object -Property TotalSeconds -Minimum | Select-Object -ExpandProperty Minimum
        $maxDuration = $successfulRuns | Measure-Object -Property TotalSeconds -Maximum | Select-Object -ExpandProperty Maximum
        $stdDevDuration = [math]::Sqrt(($successfulRuns | ForEach-Object { [math]::Pow($_.TotalSeconds - $avgDuration, 2) } | Measure-Object -Average).Average)
        
        $avgMemory = $successfulRuns | Measure-Object -Property MemoryUsedMB -Average | Select-Object -ExpandProperty Average
        $minMemory = $successfulRuns | Measure-Object -Property MemoryUsedMB -Minimum | Select-Object -ExpandProperty Minimum
        $maxMemory = $successfulRuns | Measure-Object -Property MemoryUsedMB -Maximum | Select-Object -ExpandProperty Maximum
    } else {
        $avgDuration = $minDuration = $maxDuration = $stdDevDuration = 0
        $avgMemory = $minMemory = $maxMemory = 0
    }
    
    return [PSCustomObject]@{
        Measurements = $measurements
        Exceptions = $exceptions
        Outputs = $outputs
        SuccessfulRuns = $successfulRuns.Count
        TotalRuns = $Iterations
        AverageDuration = $avgDuration
        MinimumDuration = $minDuration
        MaximumDuration = $maxDuration
        StandardDeviation = $stdDevDuration
        AverageMemoryMB = $avgMemory
        MinimumMemoryMB = $minMemory
        MaximumMemoryMB = $maxMemory
    }
}

# Operations to profile
$operations = @(
    @{
        Name = "Help Command"
        Description = "Basic help information display"
        ScriptBlock = { & $scriptPath -Action help }
        Category = "Basic"
        Priority = "Low"
    },
    @{
        Name = "Config Validation"
        Description = "Configuration file validation"
        ScriptBlock = { & $scriptPath -Action validate-config }
        Category = "Basic"
        Priority = "Low"
    },
    @{
        Name = "Single Issue Analysis"
        Description = "Analysis of a single issue text"
        ScriptBlock = { 
            & $scriptPath -Action analyze-text -Text "Combat system crashes when engaging multiple targets" -Format json 
        }
        Category = "Intelligent Routing"
        Priority = "Medium"
    },
    @{
        Name = "Complex Issue Analysis"
        Description = "Analysis of complex issue text with multiple components"
        ScriptBlock = { 
            & $scriptPath -Action analyze-text -Text "This is a complex issue involving multiple components. The combat system crashes when engaging multiple targets, but only after the looting system has attempted to process corpses. Additionally, the UI becomes unresponsive and the configuration file appears to be corrupted. The core system also shows signs of memory leaks during extended operation." -Format json 
        }
        Category = "Intelligent Routing"
        Priority = "High"
    },
    @{
        Name = "Single Issue Routing"
        Description = "Routing of a single issue"
        ScriptBlock = {
            $issues = Get-GitHubIssue -Uri "https://api.github.com/repos/$Repository/issues" -State open
            $issue = $issues | Select-Object -First 1
            if ($issue) {
                & $scriptPath -Action route-issue -Repository $Repository -IssueNumber $issue.number -Format json
            } else {
                Write-Host "No open issues found for testing" -ForegroundColor Yellow
                return "No open issues found"
            }
        }
        Category = "Intelligent Routing"
        Priority = "High"
    },
    @{
        Name = "Batch Issue Routing (5 issues)"
        Description = "Batch routing of 5 issues"
        ScriptBlock = { 
            & $scriptPath -Action batch-route -Repository $Repository -State open -Limit 5 -Format json 
        }
        Category = "Batch Processing"
        Priority = "Critical"
    },
    @{
        Name = "Batch Issue Routing (20 issues)"
        Description = "Batch routing of 20 issues"
        ScriptBlock = { 
            & $scriptPath -Action batch-route -Repository $Repository -State open -Limit 20 -Format json 
        }
        Category = "Batch Processing"
        Priority = "Critical"
    },
    @{
        Name = "Predictive Analytics"
        Description = "Generation of predictive analytics"
        ScriptBlock = { 
            & $scriptPath -Action predict -Repository $Repository -Format json 
        }
        Category = "Analytics"
        Priority = "High"
    },
    @{
        Name = "Learning from History"
        Description = "Learning from historical issue data"
        ScriptBlock = { 
            & $scriptPath -Action learn -Repository $Repository -HistoryDays 7 -Format json 
        }
        Category = "Self-Optimization"
        Priority = "Medium"
    },
    @{
        Name = "Full Orchestration"
        Description = "Complete orchestration process"
        ScriptBlock = { 
            & $scriptPath -Action orchestrate -Repository $Repository -DryRun true -Format json 
        }
        Category = "Integration"
        Priority = "Critical"
    }
)

# Perform profiling
Write-Host "Starting Performance Profiling for Full Automation Suite..." -ForegroundColor Cyan
Write-Host "Repository: $Repository" -ForegroundColor Cyan
Write-Host "Output Path: $OutputPath" -ForegroundColor Cyan
Write-Host "Iterations per operation: $Iterations" -ForegroundColor Cyan
Write-Host "`n" + "="*80 -ForegroundColor Cyan

foreach ($op in $operations) {
    Write-Host "Profiling Operation: $($op.Name)" -ForegroundColor Yellow
    Write-Host "Description: $($op.Description)" -ForegroundColor Gray
    Write-Host "Category: $($op.Category) - Priority: $($op.Priority)" -ForegroundColor Gray
    
    $result = Measure-Command2 -ScriptBlock $op.ScriptBlock -Iterations $Iterations
    $results[$op.Name] = @{
        Operation = $op
        Result = $result
    }
    
    Write-Host "  Results:" -ForegroundColor White
    Write-Host "    Successful Runs: $($result.SuccessfulRuns)/$($result.TotalRuns)" -ForegroundColor $(if ($result.SuccessfulRuns -eq $result.TotalRuns) { "Green" } else { "Yellow" })
    Write-Host "    Average Duration: $([math]::Round($result.AverageDuration, 2)) seconds" -ForegroundColor White
    Write-Host "    Duration Range: $([math]::Round($result.MinimumDuration, 2)) - $([math]::Round($result.MaximumDuration, 2)) seconds" -ForegroundColor White
    Write-Host "    Standard Deviation: $([math]::Round($result.StandardDeviation, 3)) seconds" -ForegroundColor White
    Write-Host "    Average Memory Usage: $([math]::Round($result.AverageMemoryMB, 2)) MB" -ForegroundColor White
    Write-Host "`n" + "-"*80 -ForegroundColor Gray
}

# Generate markdown report
$reportContent = @"
# Full Automation Suite Performance Profile

**Date**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")  
**Repository**: $Repository  
**Iterations per operation**: $Iterations

## Executive Summary

This report presents the performance profile of the Full Automation Suite across various operations. It identifies performance bottlenecks and provides recommendations for optimization.

## Performance Metrics by Category

"@

# Group results by category
$categorizedResults = $results.Values | Group-Object { $_.Operation.Category }

foreach ($category in $categorizedResults) {
    $reportContent += "`n### $($category.Name)`n`n"
    $reportContent += "| Operation | Priority | Avg Duration (s) | Std Dev | Memory (MB) | Success Rate |`n"
    $reportContent += "|-----------|----------|------------------|---------|-------------|--------------|`n"
    
    foreach ($item in $category.Group) {
        $successRate = "$($item.Result.SuccessfulRuns)/$($item.Result.TotalRuns)"
        $reportContent += "| $($item.Operation.Name) | $($item.Operation.Priority) | $([math]::Round($item.Result.AverageDuration, 2)) | $([math]::Round($item.Result.StandardDeviation, 3)) | $([math]::Round($item.Result.AverageMemoryMB, 2)) | $successRate |`n"
    }
}

# Identify bottlenecks
$bottlenecks = $results.Values | 
    Where-Object { $_.Result.AverageDuration -gt 5 -or $_.Result.AverageMemoryMB -gt 100 } | 
    Sort-Object { $_.Result.AverageDuration } -Descending

$reportContent += "`n## Performance Bottlenecks`n`n"

if ($bottlenecks.Count -gt 0) {
    $reportContent += "The following operations have been identified as potential bottlenecks:\n\n"
    
    foreach ($bottleneck in $bottlenecks) {
        $reportContent += "### $($bottleneck.Operation.Name) - $($bottleneck.Operation.Category)`n`n"
        $reportContent += "- **Average Duration**: $([math]::Round($bottleneck.Result.AverageDuration, 2)) seconds`n"
        $reportContent += "- **Memory Usage**: $([math]::Round($bottleneck.Result.AverageMemoryMB, 2)) MB`n"
        $reportContent += "- **Priority**: $($bottleneck.Operation.Priority)`n"
        $reportContent += "- **Description**: $($bottleneck.Operation.Description)`n`n"
    }
} else {
    $reportContent += "No significant bottlenecks detected. All operations complete within acceptable time and memory constraints.`n"
}

# Generate optimization recommendations
$reportContent += "`n## Optimization Recommendations`n`n"

# Get critical operations
$criticalOps = $results.Values | Where-Object { $_.Operation.Priority -eq "Critical" }
$highPriorityOps = $results.Values | Where-Object { $_.Operation.Priority -eq "High" }

if ($criticalOps.Count -gt 0) {
    $reportContent += "### Critical Priority Optimizations`n`n"
    
    foreach ($op in $criticalOps | Sort-Object { $_.Result.AverageDuration } -Descending) {
        $reportContent += "#### $($op.Operation.Name)`n`n"
        
        # Generate specific recommendations based on operation category and performance
        $recommendations = @()
        
        if ($op.Operation.Category -eq "Batch Processing") {
            $recommendations += "- Implement parallel processing for batch operations"
            $recommendations += "- Add caching for GitHub API responses to reduce redundant calls"
            $recommendations += "- Optimize issue filtering to reduce the dataset size before processing"
            $recommendations += "- Consider implementing pagination handling for better memory management"
        }
        
        if ($op.Operation.Category -eq "Intelligent Routing") {
            $recommendations += "- Optimize text analysis algorithms to reduce processing time"
            $recommendations += "- Implement early-exit conditions for clear component matches"
            $recommendations += "- Cache analysis results for similar issue texts"
        }
        
        if ($op.Operation.Category -eq "Integration") {
            $recommendations += "- Break down orchestration into smaller, parallelizable tasks"
            $recommendations += "- Implement incremental processing rather than full repository scans"
            $recommendations += "- Add progress reporting to allow cancellation of long-running operations"
        }
        
        if ($op.Result.AverageDuration -gt 10) {
            $recommendations += "- Profile internal execution to identify specific code bottlenecks"
            $recommendations += "- Consider rewriting critical sections in more efficient code"
        }
        
        if ($op.Result.AverageMemoryMB -gt 200) {
            $recommendations += "- Implement streaming processing for large datasets"
            $recommendations += "- Reduce object creation and transformation overhead"
            $recommendations += "- Add explicit garbage collection for long-running operations"
        }
        
        if ($recommendations.Count -gt 0) {
            foreach ($rec in $recommendations) {
                $reportContent += "$rec`n"
            }
        } else {
            $reportContent += "No specific recommendations at this time.`n"
        }
        
        $reportContent += "`n"
    }
}

# General recommendations
$reportContent += "### General Optimization Strategies`n`n"
$reportContent += "1. **API Optimization**:`n"
$reportContent += "   - Implement comprehensive caching system for GitHub API responses`n"
$reportContent += "   - Use conditional requests with ETags to reduce bandwidth and rate limit usage`n"
$reportContent += "   - Consolidate multiple API calls into batched requests where possible`n`n"

$reportContent += "2. **Computational Optimization**:`n"
$reportContent += "   - Profile and optimize text analysis algorithms for intelligent routing`n"
$reportContent += "   - Use more efficient data structures for high-volume operations`n"
$reportContent += "   - Implement early-exit strategies for clear matches`n`n"

$reportContent += "3. **Memory Management**:`n"
$reportContent += "   - Implement streaming for large datasets to reduce memory footprint`n"
$reportContent += "   - Dispose of large objects explicitly when no longer needed`n"
$reportContent += "   - Use memory-efficient data structures for large collections`n`n"

$reportContent += "4. **Parallelization**:`n"
$reportContent += "   - Implement parallel processing for independent operations`n"
$reportContent += "   - Use job queuing for long-running batch tasks`n"
$reportContent += "   - Add progress reporting and cancellation support`n`n"

$reportContent += "5. **Configuration Tuning**:`n"
$reportContent += "   - Adjust confidence thresholds based on performance testing`n"
$reportContent += "   - Optimize batch sizes for different repository sizes`n"
$reportContent += "   - Create performance profiles for different environments`n`n"

# Next steps
$reportContent += "## Next Steps`n`n"
$reportContent += "1. Implement high-priority optimizations identified above`n"
$reportContent += "2. Re-run performance tests to measure improvements`n"
$reportContent += "3. Conduct load testing with larger repositories`n"
$reportContent += "4. Document performance recommendations in the user guide`n"

# Save report
$reportContent | Out-File -FilePath $OutputPath -Encoding UTF8
Write-Host "`nPerformance profiling complete. Report saved to: $OutputPath" -ForegroundColor Green

# Return results for further processing
return $results

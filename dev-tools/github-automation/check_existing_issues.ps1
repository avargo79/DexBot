#!/usr/bin/env pwsh

<#
.SYNOPSIS
    Check which PRDs and features already exist as GitHub Issues

.DESCRIPTION
    This script checks the current GitHub Issues against our PRD files
    to identify what's already been created and what might be missing.

.NOTES
    Requires GitHub CLI (gh) to be installed and authenticated
#>

# Ensure we're in the correct directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Simple GitHub CLI check
function Test-GitHubCLI {
    try {
        $null = gh auth status 2>$null
        return $true
    } catch {
        return $false
    }
}

function Check-ExistingIssues {
    Write-Host "=== Checking Existing GitHub Issues ===" -ForegroundColor Cyan
    
    try {
        # Get all open issues
        Write-Host "Fetching current GitHub Issues..." -ForegroundColor Yellow
        $issues = gh issue list --state=all --limit 200 --json number,title,state | ConvertFrom-Json
        
        Write-Host "Found $($issues.Count) total issues" -ForegroundColor Green
        
        # Check for PRD-related issues
        Write-Host "`n=== PRD Status ===" -ForegroundColor Cyan
        $prdFiles = Get-ChildItem -Path "..\..\docs\prds\FR-*.md" | Sort-Object Name
        
        foreach ($prdFile in $prdFiles) {
            $prdNumber = ($prdFile.BaseName -split '_')[0]
            $matchingIssue = $issues | Where-Object { $_.title -like "*$prdNumber*" }
            
            if ($matchingIssue) {
                Write-Host "✅ $prdNumber - Issue #$($matchingIssue.number): $($matchingIssue.title) [$($matchingIssue.state)]" -ForegroundColor Green
            } else {
                Write-Host "❌ $prdNumber - No matching issue found" -ForegroundColor Red
            }
        }
        
        # Check for TECH issues
        Write-Host "`n=== Technical Issues ===" -ForegroundColor Cyan
        $techFiles = Get-ChildItem -Path "..\..\docs\prds\TECH-*.md" | Sort-Object Name
        
        foreach ($techFile in $techFiles) {
            $techNumber = ($techFile.BaseName -split '_')[0]
            $matchingIssue = $issues | Where-Object { $_.title -like "*$techNumber*" }
            
            if ($matchingIssue) {
                Write-Host "✅ $techNumber - Issue #$($matchingIssue.number): $($matchingIssue.title) [$($matchingIssue.state)]" -ForegroundColor Green
            } else {
                Write-Host "❌ $techNumber - No matching issue found" -ForegroundColor Red
            }
        }
        
        # Show recent issues
        Write-Host "`n=== Recent Issues (Last 10) ===" -ForegroundColor Cyan
        $recentIssues = $issues | Sort-Object number -Descending | Select-Object -First 10
        foreach ($issue in $recentIssues) {
            Write-Host "#$($issue.number): $($issue.title) [$($issue.state)]" -ForegroundColor White
        }
        
    } catch {
        Write-Error "Failed to check GitHub Issues: $($_.Exception.Message)"
        return $false
    }
    
    return $true
}

function Check-DuplicateIssues {
    Write-Host "\n=== Checking for Duplicate Issues ===" -ForegroundColor Cyan

    try {
        # Get all open issues
        Write-Host "Fetching current GitHub Issues..." -ForegroundColor Yellow
        $issues = gh issue list --state=all --limit 200 --json number,title,body | ConvertFrom-Json

        Write-Host "Found $($issues.Count) total issues" -ForegroundColor Green

        # Check for duplicates based on title similarity
        $duplicates = @()
        foreach ($issue in $issues) {
            $similarIssues = $issues | Where-Object { $_.number -ne $issue.number -and $_.title -like "*$($issue.title)*" }
            if ($similarIssues) {
                $duplicates += [PSCustomObject]@{
                    IssueNumber = $issue.number
                    Title = $issue.title
                    SimilarIssues = $similarIssues | Select-Object -Property number, title
                }
            }
        }

        if ($duplicates.Count -gt 0) {
            Write-Host "\nDuplicate Issues Found:" -ForegroundColor Yellow
            foreach ($dup in $duplicates) {
                Write-Host "Issue #$($dup.IssueNumber): $($dup.Title)" -ForegroundColor Red
                foreach ($similar in $dup.SimilarIssues) {
                    Write-Host "  Similar Issue #$($similar.number): $($similar.title)" -ForegroundColor Yellow
                }
            }
        } else {
            Write-Host "\nNo duplicate issues found." -ForegroundColor Green
        }

    } catch {
        Write-Error "Failed to check for duplicate issues: $($_.Exception.Message)"
        return $false
    }

    return $true
}

function Close-OldestDuplicateIssues {
    Write-Host "\n=== Closing Oldest Duplicate Issues ===" -ForegroundColor Cyan

    try {
        # Get all open issues
        Write-Host "Fetching current GitHub Issues..." -ForegroundColor Yellow
        $issues = gh issue list --state=all --limit 200 --json number,title,createdAt | ConvertFrom-Json

        Write-Host "Found $($issues.Count) total issues" -ForegroundColor Green

        # Check for duplicates based on title similarity
        $duplicates = @()
        foreach ($issue in $issues) {
            $similarIssues = $issues | Where-Object { $_.number -ne $issue.number -and $_.title -like "*$($issue.title)*" }
            if ($similarIssues) {
                $duplicates += [PSCustomObject]@{
                    IssueNumber = $issue.number
                    Title = $issue.title
                    SimilarIssues = $similarIssues | Sort-Object createdAt | Select-Object -Property number, title, createdAt
                }
            }
        }

        foreach ($dup in $duplicates) {
            $oldestIssue = $dup.SimilarIssues | Select-Object -First 1
            if ($oldestIssue) {
                Write-Host "Closing Issue #$($oldestIssue.number): $($oldestIssue.title)" -ForegroundColor Red
                gh issue close $oldestIssue.number --comment "Closing as duplicate of newer issue."
            }
        }

        Write-Host "\nOldest duplicate issues closed successfully." -ForegroundColor Green

    } catch {
        Write-Error "Failed to close duplicate issues: $($_.Exception.Message)"
        return $false
    }

    return $true
}

# Main execution
if (-not (Test-GitHubCLI)) {
    Write-Error "GitHub CLI not authenticated. Run 'gh auth login' first."
    exit 1
}

Check-ExistingIssues
Check-DuplicateIssues
Close-OldestDuplicateIssues

Write-Host "`n=== Issue Check Complete ===" -ForegroundColor Cyan
Write-Host "Review the output above to see which PRDs need GitHub Issues created." -ForegroundColor Yellow

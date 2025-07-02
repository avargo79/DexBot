# Test Environment Setup for Full Automation Suite
# Sets up test repositories and populates them with sample issues for testing

param(
    [string]$OutputPath = "tmp\test_setup_$(Get-Date -Format 'yyyyMMdd_HHmmss').log",
    [switch]$ForceCreate = $false,
    [string]$Token = $env:GITHUB_TOKEN
)

# Verify GitHub token
if (-not $Token) {
    Write-Host "GitHub token not found. Please set GITHUB_TOKEN environment variable or provide via -Token parameter." -ForegroundColor Red
    exit 1
}

# Initialize logging
$LogFile = $OutputPath
Start-Transcript -Path $LogFile -Append
Write-Host "Starting Test Environment Setup for Full Automation Suite..." -ForegroundColor Cyan
Write-Host "Log file: $LogFile" -ForegroundColor Gray

# Ensure PowerShellForGitHub module is installed
if (-not (Get-Module -ListAvailable -Name PowerShellForGitHub)) {
    Write-Host "Installing PowerShellForGitHub module..." -ForegroundColor Yellow
    Install-Module -Name PowerShellForGitHub -Scope CurrentUser -Force
}

# Import the module
Import-Module PowerShellForGitHub

# Setup authentication
try {
    Set-GitHubAuthentication -Token $Token
    Write-Host "GitHub authentication configured successfully" -ForegroundColor Green
} catch {
    Write-Host "Failed to configure GitHub authentication: $_" -ForegroundColor Red
    exit 1
}

# Test repository configurations
$TestRepos = @(
    @{
        Name = "dexbot-test-small"
        Description = "Small test repository for DexBot Automation Suite"
        IssueCount = 25
        Private = $true
    },
    @{
        Name = "dexbot-test-medium"
        Description = "Medium test repository for DexBot Automation Suite"
        IssueCount = 100
        Private = $true
    },
    @{
        Name = "dexbot-test-large"
        Description = "Large test repository for DexBot Automation Suite"
        IssueCount = 250
        Private = $true
    }
)

# Component categories for testing
$Components = @("core", "combat", "looting", "auto-heal", "ui", "config", "utils")
$Priorities = @("critical", "high", "medium", "low")
$Tags = @("bug", "enhancement", "documentation", "question", "testing")

# Sample issue descriptions by component
$IssueTemplates = @{
    "core" = @(
        "Core system crashes unexpectedly after running for {0} hours",
        "Memory leak in core bot state machine causing performance degradation over time",
        "Core initialization fails when config file has special characters",
        "Bot state machine enters infinite loop during {0} process",
        "Race condition in core event handlers causes system instability"
    )
    "combat" = @(
        "Combat system fails to target nearest enemy in crowded areas",
        "Combat targeting system selects incorrect targets when multiple enemies present",
        "Weapon switching fails during intense combat scenarios",
        "Combat system crashes when engaging {0} targets simultaneously",
        "Attack sequence interrupted by invalid state transition"
    )
    "looting" = @(
        "Looting system misses valuable items on corpses",
        "Looting system not picking up {0} and {1} from corpses",
        "Corpse identification fails in crowded areas",
        "Looting system causes inventory overflow without warning",
        "Custom loot filters not working correctly for specific item types"
    )
    "auto-heal" = @(
        "Auto heal not working with {0} when health below {1}%",
        "Healing priority system ignores critical status effects",
        "Bandage application fails when moving",
        "Potion consumption doesn't register correctly",
        "Auto heal doesn't recognize certain damage types"
    )
    "ui" = @(
        "GUMP interface becomes unresponsive after long sessions",
        "UI elements misaligned on high DPI displays",
        "Button click handlers stop responding after multiple interactions",
        "Status display shows incorrect health/mana values",
        "Configuration interface doesn't save changes properly"
    )
    "config" = @(
        "Configuration file corruption causes system startup failure",
        "Settings reset to default unexpectedly",
        "Unable to save custom configuration profiles",
        "Config validation fails to catch invalid parameter combinations",
        "Import/export functionality breaks with complex settings"
    )
    "utils" = @(
        "Utility functions for distance calculation producing incorrect results",
        "Path finding algorithm fails in complex environments",
        "Timer functions drift significantly over long sessions",
        "Coordinate conversion functions fail at map boundaries",
        "String parsing utilities break with unicode characters"
    )
}

# Create randomized issue body content
function Get-RandomIssueBody {
    param (
        [string]$Component,
        [string]$Title
    )
    
    $templates = @(
        "## Description`n`n$Title`n`n## Steps to Reproduce`n1. Start the bot`n2. Enable $Component system`n3. Wait for approximately {0} minutes`n`n## Expected Behavior`nThe $Component system should continue functioning normally`n`n## Actual Behavior`nThe system {1}`n`n## Environment`n- Version: 1.{2}.{3}`n- OS: Windows {4}`n- UO Server: {5}`n- System Uptime: {6} hours",
        
        "## Bug Report`n`n**What happened**:`n$Title`n`n**What I expected**:`nThe $Component system should work correctly`n`n**How to reproduce**:`n1. Configure the $Component settings to {0}`n2. Run the bot for {1} minutes`n3. Observe the failure`n`n**Screenshots**:`n[Screenshot would be attached here]`n`n**System Information**:`n- Version: 1.{2}.{3}`n- Platform: Windows {4}`n- Settings: Default configuration",
        
        "# Issue with $Component System`n`nI've encountered a problem: $Title`n`nThis happens every time I try to {0} with the following configuration:`n```json`n{`n  \"$Component\": {`n    \"enabled\": true,`n    \"parameter1\": {1},`n    \"parameter2\": \"{2}\"`n  }`n}`n````n`nThe error occurs after approximately {3} minutes of operation. Any suggestions on how to fix this?`n`nAdditional details:`n- Bot Version: 1.{4}.{5}`n- Operating System: Windows {6}`n- UO Shard: {7}"
    )
    
    $template = Get-Random -InputObject $templates
    
    # Generate random values for template parameters
    $minutes = Get-Random -Minimum 5 -Maximum 120
    $failureModes = @("crashes unexpectedly", "freezes completely", "starts consuming excessive CPU", "stops responding to commands", "produces incorrect results")
    $failureMode = Get-Random -InputObject $failureModes
    $majorVersion = Get-Random -Minimum 0 -Maximum 5
    $minorVersion = Get-Random -Minimum 1 -Maximum 20
    $windowsVersion = Get-Random -InputObject @("10", "11")
    $servers = @("UO Forever", "Outlands", "UO Evolution", "UO Renaissance", "Official Servers")
    $server = Get-Random -InputObject $servers
    $uptime = Get-Random -Minimum 1 -Maximum 48
    $setting = Get-Random -Minimum 1 -Maximum 100
    $options = @("aggressive", "balanced", "conservative", "optimal", "experimental")
    $option = Get-Random -InputObject $options
    
    return $template -f $minutes, $failureMode, $majorVersion, $minorVersion, $windowsVersion, $server, $uptime, $setting, $option
}

# Function to create a test repository
function New-TestRepository {
    param (
        [string]$Name,
        [string]$Description,
        [bool]$Private
    )
    
    $RepoParams = @{
        Organization = $null  # Null for personal account
        OwnerName = $null    # Will use authenticated user
        RepositoryName = $Name
        Description = $Description
        Private = $Private
        AutoInit = $true     # Initialize with README
    }
    
    try {
        # Check if repo already exists
        $existingRepo = $null
        try {
            $existingRepo = Get-GitHubRepository -OwnerName (Get-GitHubUser).login -RepositoryName $Name -ErrorAction SilentlyContinue
        } catch {
            # Repository doesn't exist, which is what we want
        }
        
        if ($existingRepo -and -not $ForceCreate) {
            Write-Host "Repository '$Name' already exists. Use -ForceCreate to recreate." -ForegroundColor Yellow
            return $existingRepo
        } elseif ($existingRepo -and $ForceCreate) {
            Write-Host "Removing existing repository '$Name'..." -ForegroundColor Yellow
            Remove-GitHubRepository -OwnerName (Get-GitHubUser).login -RepositoryName $Name -Force
            Start-Sleep -Seconds 2  # Give GitHub a moment
        }
        
        Write-Host "Creating repository '$Name'..." -ForegroundColor Cyan
        $repo = New-GitHubRepository @RepoParams
        
        # Create labels for components and priorities
        foreach ($component in $Components) {
            $labelParams = @{
                OwnerName = $repo.owner.login
                RepositoryName = $repo.name
                Name = "component:$component"
                Color = (Get-Random -Minimum 0 -Maximum 16777215).ToString("X6")  # Random color
                Description = "Issues related to the $component component"
            }
            New-GitHubLabel @labelParams | Out-Null
        }
        
        foreach ($priority in $Priorities) {
            $colorMap = @{
                "critical" = "FF0000"  # Red
                "high" = "FF9900"      # Orange
                "medium" = "FFFF00"    # Yellow
                "low" = "00FF00"       # Green
            }
            
            $labelParams = @{
                OwnerName = $repo.owner.login
                RepositoryName = $repo.name
                Name = "priority:$priority"
                Color = $colorMap[$priority]
                Description = "$priority priority issues"
            }
            New-GitHubLabel @labelParams | Out-Null
        }
        
        foreach ($tag in $Tags) {
            $labelParams = @{
                OwnerName = $repo.owner.login
                RepositoryName = $repo.name
                Name = "type:$tag"
                Color = (Get-Random -Minimum 0 -Maximum 16777215).ToString("X6")  # Random color
                Description = "Issues of type $tag"
            }
            New-GitHubLabel @labelParams | Out-Null
        }
        
        Write-Host "Repository '$Name' created successfully with component and priority labels" -ForegroundColor Green
        return $repo
    } catch {
        Write-Host "Failed to create repository '$Name': $_" -ForegroundColor Red
        return $null
    }
}

# Function to create sample issues in a repository
function New-SampleIssues {
    param (
        [object]$Repository,
        [int]$Count
    )
    
    Write-Host "Creating $Count sample issues in repository '$($Repository.name)'..." -ForegroundColor Cyan
    $createdCount = 0
    $startTime = Get-Date
    
    for ($i = 1; $i -le $Count; $i++) {
        # Select a random component and issue template
        $component = Get-Random -InputObject $Components
        $templateList = $IssueTemplates[$component]
        $titleTemplate = Get-Random -InputObject $templateList
        
        # Generate random values for the title
        $randomValues = @(
            (Get-Random -Minimum 2 -Maximum 20),                               # Number
            (Get-Random -InputObject @("gold", "reagents", "resources", "weapons", "armor")),  # Item type 1
            (Get-Random -InputObject @("gems", "scrolls", "potions", "tools", "runes"))        # Item type 2
        )
        
        $title = $titleTemplate -f $randomValues
        
        # Generate a detailed body
        $body = Get-RandomIssueBody -Component $component -Title $title
        
        # Select a random priority and tag
        $priority = Get-Random -InputObject $Priorities
        $tag = Get-Random -InputObject $Tags
        
        $labels = @("component:$component", "priority:$priority", "type:$tag")
        
        # Create the issue
        try {
            $issueParams = @{
                OwnerName = $Repository.owner.login
                RepositoryName = $Repository.name
                Title = $title
                Body = $body
                Label = $labels
            }
            
            $issue = New-GitHubIssue @issueParams
            $createdCount++
            
            # Randomly close some issues (about 30%)
            if ((Get-Random -Minimum 1 -Maximum 10) -le 3) {
                $updateParams = @{
                    OwnerName = $Repository.owner.login
                    RepositoryName = $Repository.name
                    Issue = $issue.number
                    State = "closed"
                }
                Update-GitHubIssue @updateParams | Out-Null
            }
            
            # Add comments to some issues (about 50%)
            if ((Get-Random -Minimum 1 -Maximum 10) -le 5) {
                $commentCount = Get-Random -Minimum 1 -Maximum 5
                for ($j = 1; $j -le $commentCount; $j++) {
                    $commentParams = @{
                        OwnerName = $Repository.owner.login
                        RepositoryName = $Repository.name
                        Issue = $issue.number
                        Body = "Comment $j: Additional information about this issue. Testing comment functionality for the Full Automation Suite."
                    }
                    New-GitHubIssueComment @commentParams | Out-Null
                }
            }
            
            # Progress reporting
            $percentComplete = [math]::Round(($i / $Count) * 100, 1)
            $elapsedTime = (Get-Date) - $startTime
            $estimatedTotalTime = $elapsedTime.TotalSeconds / ($i / $Count)
            $estimatedRemaining = $estimatedTotalTime - $elapsedTime.TotalSeconds
            
            Write-Progress -Activity "Creating Issues" -Status "$i of $Count issues created ($percentComplete%)" -PercentComplete $percentComplete
            
            if ($i % 10 -eq 0 -or $i -eq $Count) {
                Write-Host "  Progress: $i/$Count issues created ($percentComplete%) - Est. remaining: $([math]::Round($estimatedRemaining / 60, 1)) minutes" -ForegroundColor Yellow
            }
            
            # Add a small delay to avoid rate limiting
            Start-Sleep -Milliseconds 500
            
        } catch {
            Write-Host "Failed to create issue #$i in repository '$($Repository.name)': $_" -ForegroundColor Red
        }
    }
    
    Write-Progress -Activity "Creating Issues" -Completed
    Write-Host "Created $createdCount/$Count issues in repository '$($Repository.name)'" -ForegroundColor Green
}

# Main execution
try {
    $CreatedRepos = @()
    
    foreach ($repoConfig in $TestRepos) {
        $repo = New-TestRepository -Name $repoConfig.Name -Description $repoConfig.Description -Private $repoConfig.Private
        
        if ($repo) {
            $CreatedRepos += $repo
            New-SampleIssues -Repository $repo -Count $repoConfig.IssueCount
        }
    }
    
    # Output summary
    Write-Host "`n========== TEST ENVIRONMENT SETUP SUMMARY ==========" -ForegroundColor Cyan
    foreach ($repo in $CreatedRepos) {
        Write-Host "Repository: $($repo.html_url)" -ForegroundColor Green
        $issueCount = (Get-GitHubIssue -OwnerName $repo.owner.login -RepositoryName $repo.name -State all).Count
        Write-Host "  Total Issues: $issueCount" -ForegroundColor Green
    }
    
    Write-Host "`nTest environment setup complete. Use these repositories for end-to-end testing of the Full Automation Suite." -ForegroundColor Cyan
    Write-Host "Log file saved to: $LogFile" -ForegroundColor Gray
    
} catch {
    Write-Host "An error occurred during test environment setup: $_" -ForegroundColor Red
} finally {
    Stop-Transcript
}

#!/usr/bin/env powershell
<#
.SYNOPSIS
    Setup GitHub repository labels for DexBot project management

.DESCRIPTION
    Creates all necessary labels for the GitHub Issues project management system.
    This includes priority labels, component labels, and status labels.

.PARAMETER Force
    Delete existing labels and recreate them

.EXAMPLE
    .\setup_labels.ps1
    .\setup_labels.ps1 -Force
#>

param(
    [switch]$Force = $false
)

# Color output functions
function Write-Success { param($Message) Write-Host $Message -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host $Message -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host $Message -ForegroundColor Red }
function Write-Info { param($Message) Write-Host $Message -ForegroundColor Cyan }

Write-Info "DexBot GitHub Labels Setup"
Write-Info "=========================="

# Check if gh CLI is available
try {
    $ghVersion = gh --version
    Write-Success "GitHub CLI detected: $($ghVersion[0])"
} catch {
    Write-Error "GitHub CLI not found. Please install GitHub CLI first."
    exit 1
}

# Define all labels for DexBot project management
$Labels = @(
    # Priority Labels
    @{ Name = "priority:critical"; Description = "Critical priority - blocking issues"; Color = "B60205" },
    @{ Name = "priority:high"; Description = "High priority - important features/fixes"; Color = "D93F0B" },
    @{ Name = "priority:medium"; Description = "Medium priority - standard development"; Color = "FBCA04" },
    @{ Name = "priority:low"; Description = "Low priority - nice to have improvements"; Color = "0E8A16" },
    
    # Component Labels
    @{ Name = "component:auto-heal"; Description = "Auto heal system"; Color = "C5DEF5" },
    @{ Name = "component:combat"; Description = "Combat system"; Color = "F9D0C4" },
    @{ Name = "component:looting"; Description = "Looting system"; Color = "D4C5F9" },
    @{ Name = "component:ui"; Description = "User interface (GUMPs)"; Color = "C5F5DE" },
    @{ Name = "component:config"; Description = "Configuration management"; Color = "F5E6C5" },
    @{ Name = "component:core"; Description = "Core systems and utilities"; Color = "E6C5F5" },
    @{ Name = "component:build"; Description = "Build system and CI/CD"; Color = "C5F5F5" },
    @{ Name = "component:docs"; Description = "Documentation"; Color = "F5C5C5" },
    
    # Status Labels
    @{ Name = "status:proposed"; Description = "Proposed item under consideration"; Color = "D4C5F9" },
    @{ Name = "status:planning"; Description = "Requirements gathering and planning"; Color = "EDEDED" },
    @{ Name = "status:ready-for-pickup"; Description = "Ready for developer assignment"; Color = "7CFC00" },
    @{ Name = "status:in-progress"; Description = "Currently being worked on"; Color = "0052CC" },
    @{ Name = "status:testing"; Description = "Being tested"; Color = "FF8C00" },
    @{ Name = "status:on-hold"; Description = "Temporarily paused"; Color = "FFC107" },
    @{ Name = "status:blocked"; Description = "Cannot proceed due to dependencies"; Color = "000000" },
    @{ Name = "status:rejected"; Description = "Will not be implemented"; Color = "DC3545" },
    @{ Name = "status:implemented"; Description = "Feature implemented and deployed"; Color = "28A745" },
    
    # PRD Labels
    @{ Name = "prd:fast-track"; Description = "PRD approved for fast-track processing"; Color = "FF6B6B" },
    
    # Type Labels (enhance existing ones)
    @{ Name = "idea"; Description = "Initial idea or suggestion needing evaluation"; Color = "E6F3FF" },
    @{ Name = "maintenance"; Description = "Code cleanup, refactoring, optimization"; Color = "FEF2C0" },
    @{ Name = "performance"; Description = "Performance improvements"; Color = "FF6B6B" },
    @{ Name = "security"; Description = "Security-related issues"; Color = "EE0701" },
    @{ Name = "testing"; Description = "Testing improvements and additions"; Color = "BFD4F2" }
)

Write-Info "Setting up $($Labels.Count) labels..."
Write-Host ""

# Function to create a label
function Create-Label {
    param($Label)
    
    try {
        # Check if label exists
        $existingLabel = gh label list --json name | ConvertFrom-Json | Where-Object { $_.name -eq $Label.Name }
        
        if ($existingLabel) {
            if ($Force) {
                Write-Warning "Deleting existing label: $($Label.Name)"
                gh label delete $Label.Name --confirm
            } else {
                Write-Warning "Label already exists: $($Label.Name) (use -Force to recreate)"
                return
            }
        }
        
        # Create the label
        gh label create $Label.Name --description $Label.Description --color $Label.Color
        Write-Success "Created label: $($Label.Name)"
        
    } catch {
        Write-Error "Failed to create label: $($Label.Name)"
        Write-Error "Error: $($_.Exception.Message)"
    }
}

# Create all labels
foreach ($label in $Labels) {
    Create-Label $label
}

Write-Host ""
Write-Success "Label setup complete!"
Write-Info "You can now use these labels in your issues:"
Write-Host ""

Write-Info "Priority Labels:"
Write-Host "  priority:critical, priority:high, priority:medium, priority:low" -ForegroundColor Gray

Write-Info "Component Labels:"
Write-Host "  component:auto-heal, component:combat, component:looting, component:ui" -ForegroundColor Gray
Write-Host "  component:config, component:core, component:build, component:docs" -ForegroundColor Gray

Write-Info "Status Labels:"
Write-Host "  status:proposed, status:planning, status:ready-for-pickup, status:in-progress" -ForegroundColor Gray
Write-Host "  status:testing, status:on-hold, status:blocked, status:rejected, status:implemented" -ForegroundColor Gray

Write-Info "PRD Labels:"
Write-Host "  prd:fast-track" -ForegroundColor Gray

Write-Info "Type Labels:"
Write-Host "  idea, enhancement, bug, documentation, maintenance, performance, security, testing" -ForegroundColor Gray

Write-Host ""
Write-Info "Next steps:"
Write-Host "  1. Test issue creation: .\scripts\create_issues.ps1 -DryRun" -ForegroundColor Gray
Write-Host "  2. Create actual issues: .\scripts\create_issues.ps1 -Interactive" -ForegroundColor Gray
Write-Host "  3. Manage issues: .\scripts\manage_issues.ps1 -Action list" -ForegroundColor Gray

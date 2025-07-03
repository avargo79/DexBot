#!/usr/bin/env powershell
<#
.SYNOPSIS
    Batch operations for GitHub Issues workflow management in DexBot

.DESCRIPTION
    Provides bulk management capabilities for GitHub Issues, including status updates,
    priority changes, component assignments, and other workflow operations.
    Integrates with existing issue management and fast-track systems.

.PARAMETER Action
    Batch operation to perform:
    - bulk-status: Update status for multiple issues
    - bulk-priority: Update priority for multiple issues  
    - bulk-component: Assign component to multiple issues
    - bulk-label: Add/remove labels from multiple issues
    - bulk-assign: Assign issues to users
    - bulk-close: Close multiple issues
    - bulk-archive: Archive completed issues
    - triage-batch: Process triage queue
    - fast-track-batch: Process fast-track issues

.PARAMETER IssueNumbers
    Comma-separated list of issue numbers to process

.PARAMETER IssueFile
    File containing issue numbers (one per line)

.PARAMETER Filter
    Filter criteria for automatic issue selection:
    - status:needs-triage
    - priority:low
    - component:auto-heal
    - label:bug
    - age:>30d
    - author:username

.PARAMETER NewValue
    New value to apply (status, priority, component, etc.)

.PARAMETER Labels
    Labels to add or remove (comma-separated)

.PARAMETER Assignee
    User to assign issues to

.PARAMETER DryRun
    Preview changes without applying them

.PARAMETER Interactive
    Run in interactive mode with confirmations

.PARAMETER Force
    Skip confirmations and apply changes immediately

.PARAMETER LogFile
    Path to log file for batch operations

.EXAMPLE
    .\batch_operations.ps1 -Action bulk-status -IssueNumbers "1,2,3" -NewValue "in-progress"
    .\batch_operations.ps1 -Action bulk-priority -Filter "status:needs-triage" -NewValue "medium" -DryRun
    .\batch_operations.ps1 -Action triage-batch -Interactive
    .\batch_operations.ps1 -Action bulk-component -IssueFile issues.txt -NewValue "combat-system"
#>

param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("bulk-status", "bulk-priority", "bulk-component", "bulk-label", 
                 "bulk-assign", "bulk-close", "bulk-archive", "triage-batch", "fast-track-batch")]
    [string]$Action,
    
    [string]$IssueNumbers,
    
    [string]$IssueFile,
    
    [string]$Filter,
    
    [string]$NewValue,
    
    [string]$Labels,
    
    [string]$Assignee,
    
    [switch]$DryRun,
    
    [switch]$Interactive,
    
    [switch]$Force,
    
    [string]$LogFile = "tmp/batch_operations_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
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
function Write-BatchLog {
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
            Write-BatchLog "GitHub CLI detected: $($ghVersion[0])"
            return $true
        }
    } catch {
        # Ignore errors
    }
    
    Write-BatchLog "GitHub CLI not found. Please install gh CLI." "ERROR"
    return $false
}

function Get-IssueList {
    param(
        [string]$Numbers,
        [string]$File,
        [string]$FilterCriteria
    )
    
    $issues = @()
    
    # From direct numbers
    if ($Numbers) {
        $issues += $Numbers -split "," | ForEach-Object { $_.Trim() } | Where-Object { $_ -match '^\d+$' }
    }
    
    # From file
    if ($File -and (Test-Path $File)) {
        $fileIssues = Get-Content $File | ForEach-Object { $_.Trim() } | Where-Object { $_ -match '^\d+$' }
        $issues += $fileIssues
    }
    
    # From filter criteria
    if ($FilterCriteria) {
        Write-BatchLog "Applying filter: $FilterCriteria"
        $filteredIssues = Get-FilteredIssues -Filter $FilterCriteria
        $issues += $filteredIssues
    }
    
    # Remove duplicates and return
    $uniqueIssues = $issues | Sort-Object -Unique
    Write-BatchLog "Selected $($uniqueIssues.Count) issues for processing"
    
    return $uniqueIssues
}

function Get-FilteredIssues {
    param([string]$Filter)
    
    Write-BatchLog "Fetching issues with filter: $Filter"
    
    try {
        # Parse filter criteria
        $filterParts = $Filter -split ":"
        if ($filterParts.Count -ne 2) {
            throw "Invalid filter format. Use 'field:value' format."
        }
        
        $field = $filterParts[0].ToLower()
        $value = $filterParts[1]
        
        # Build GitHub CLI query
        $query = ""
        switch ($field) {
            "status" { $query = "label:`"status:$value`"" }
            "priority" { $query = "label:`"priority:$value`"" }
            "component" { $query = "label:`"component:$value`"" }
            "label" { $query = "label:`"$value`"" }
            "author" { $query = "author:$value" }
            "assignee" { $query = "assignee:$value" }
            "age" {
                # Parse age criteria (e.g., >30d, <7d)
                if ($value -match '^([<>]=?)(\d+)([dwhm])$') {
                    $operator = $matches[1]
                    $number = $matches[2]
                    $unit = $matches[3]
                    
                    $date = switch ($unit) {
                        'd' { (Get-Date).AddDays(-$number) }
                        'w' { (Get-Date).AddDays(-($number * 7)) }
                        'h' { (Get-Date).AddHours(-$number) }
                        'm' { (Get-Date).AddMonths(-$number) }
                    }
                    
                    $dateStr = $date.ToString("yyyy-MM-dd")
                    $query = if ($operator -eq ">") { "created:<$dateStr" } else { "created:>$dateStr" }
                } else {
                    throw "Invalid age format. Use format like '>30d', '<7d'"
                }
            }
            default { throw "Unsupported filter field: $field" }
        }
        
        # Fetch issues using GitHub CLI
        $issuesJson = gh issue list --json number,title,state,labels --limit 1000 --search $query 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to fetch issues from GitHub"
        }
        
        $issueData = $issuesJson | ConvertFrom-Json
        $issueNumbers = $issueData | ForEach-Object { $_.number.ToString() }
        
        Write-BatchLog "Filter returned $($issueNumbers.Count) issues"
        return $issueNumbers
        
    } catch {
        Write-BatchLog "Error applying filter: $_" "ERROR"
        return @()
    }
}

function Confirm-BatchOperation {
    param(
        [string]$Operation,
        [array]$Issues,
        [string]$NewValue
    )
    
    if ($Force) {
        return $true
    }
    
    Write-Host ""
    Write-Host "=== BATCH OPERATION CONFIRMATION ===" -ForegroundColor Cyan
    Write-Host "Operation: $Operation" -ForegroundColor Yellow
    Write-Host "Issues to process: $($Issues.Count)" -ForegroundColor Yellow
    Write-Host "New value: $NewValue" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Issues:" -ForegroundColor White
    $Issues | ForEach-Object { Write-Host "  - #$_" }
    Write-Host ""
    
    if ($DryRun) {
        Write-Host "DRY RUN MODE - No changes will be applied" -ForegroundColor Magenta
        return $true
    }
    
    do {
        $confirmation = Read-Host "Proceed with batch operation? [Y/n]"
        if ($confirmation -eq "" -or $confirmation -eq "Y" -or $confirmation -eq "y") {
            return $true
        } elseif ($confirmation -eq "N" -or $confirmation -eq "n") {
            return $false
        }
        Write-Host "Please enter Y or N"
    } while ($true)
}

# ================================================================================
# BATCH OPERATION FUNCTIONS
# ================================================================================

function Invoke-BulkStatus {
    param(
        [array]$Issues,
        [string]$Status
    )
    
    $validStatuses = @("needs-triage", "ready-for-pickup", "in-progress", "blocked", 
                      "needs-review", "on-hold", "rejected", "implemented")
    
    if ($Status -notin $validStatuses) {
        Write-BatchLog "Invalid status: $Status. Valid options: $($validStatuses -join ', ')" "ERROR"
        return $false
    }
    
    Write-BatchLog "Starting bulk status update to '$Status' for $($Issues.Count) issues"
    
    $successCount = 0
    $errorCount = 0
    
    foreach ($issueNumber in $Issues) {
        try {
            if (-not $DryRun) {
                # Remove existing status labels
                $existingLabels = gh issue view $issueNumber --json labels --template '{{range .labels}}{{.name}},{{end}}' 2>$null
                if ($LASTEXITCODE -eq 0 -and $existingLabels) {
                    $statusLabels = $existingLabels -split "," | Where-Object { $_ -like "status:*" }
                    foreach ($label in $statusLabels) {
                        if ($label.Trim()) {
                            gh issue edit $issueNumber --remove-label $label.Trim() 2>$null | Out-Null
                        }
                    }
                }
                
                # Add new status label
                gh issue edit $issueNumber --add-label "status:$Status" 2>$null
                if ($LASTEXITCODE -eq 0) {
                    Write-BatchLog "✓ Issue #$issueNumber status updated to '$Status'" "SUCCESS"
                    $successCount++
                } else {
                    Write-BatchLog "✗ Failed to update issue #$issueNumber" "ERROR"
                    $errorCount++
                }
            } else {
                Write-BatchLog "[DRY RUN] Would update issue #$issueNumber status to '$Status'"
                $successCount++
            }
        } catch {
            Write-BatchLog "✗ Error updating issue #$issueNumber`: $_" "ERROR"
            $errorCount++
        }
    }
    
    Write-BatchLog "Bulk status update completed: $successCount success, $errorCount errors"
    return $errorCount -eq 0
}

function Invoke-BulkPriority {
    param(
        [array]$Issues,
        [string]$Priority
    )
    
    $validPriorities = @("critical", "high", "medium", "low")
    
    if ($Priority -notin $validPriorities) {
        Write-BatchLog "Invalid priority: $Priority. Valid options: $($validPriorities -join ', ')" "ERROR"
        return $false
    }
    
    Write-BatchLog "Starting bulk priority update to '$Priority' for $($Issues.Count) issues"
    
    $successCount = 0
    $errorCount = 0
    
    foreach ($issueNumber in $Issues) {
        try {
            if (-not $DryRun) {
                # Remove existing priority labels
                $existingLabels = gh issue view $issueNumber --json labels --template '{{range .labels}}{{.name}},{{end}}' 2>$null
                if ($LASTEXITCODE -eq 0 -and $existingLabels) {
                    $priorityLabels = $existingLabels -split "," | Where-Object { $_ -like "priority:*" }
                    foreach ($label in $priorityLabels) {
                        if ($label.Trim()) {
                            gh issue edit $issueNumber --remove-label $label.Trim() 2>$null | Out-Null
                        }
                    }
                }
                
                # Add new priority label
                gh issue edit $issueNumber --add-label "priority:$Priority" 2>$null
                if ($LASTEXITCODE -eq 0) {
                    Write-BatchLog "✓ Issue #$issueNumber priority updated to '$Priority'" "SUCCESS"
                    $successCount++
                } else {
                    Write-BatchLog "✗ Failed to update issue #$issueNumber" "ERROR"
                    $errorCount++
                }
            } else {
                Write-BatchLog "[DRY RUN] Would update issue #$issueNumber priority to '$Priority'"
                $successCount++
            }
        } catch {
            Write-BatchLog "✗ Error updating issue #$issueNumber`: $_" "ERROR"
            $errorCount++
        }
    }
    
    Write-BatchLog "Bulk priority update completed: $successCount success, $errorCount errors"
    return $errorCount -eq 0
}

function Invoke-BulkComponent {
    param(
        [array]$Issues,
        [string]$Component
    )
    
    $validComponents = @("auto-heal", "combat", "looting", "ui", "config", "core", "build", "docs")
    
    if ($Component -notin $validComponents) {
        Write-BatchLog "Invalid component: $Component. Valid options: $($validComponents -join ', ')" "ERROR"
        return $false
    }
    
    Write-BatchLog "Starting bulk component assignment to '$Component' for $($Issues.Count) issues"
    
    $successCount = 0
    $errorCount = 0
    
    foreach ($issueNumber in $Issues) {
        try {
            if (-not $DryRun) {
                # Remove existing component labels
                $existingLabels = gh issue view $issueNumber --json labels --template '{{range .labels}}{{.name}},{{end}}' 2>$null
                if ($LASTEXITCODE -eq 0 -and $existingLabels) {
                    $componentLabels = $existingLabels -split "," | Where-Object { $_ -like "component:*" }
                    foreach ($label in $componentLabels) {
                        if ($label.Trim()) {
                            gh issue edit $issueNumber --remove-label $label.Trim() 2>$null | Out-Null
                        }
                    }
                }
                
                # Add new component label
                gh issue edit $issueNumber --add-label "component:$Component" 2>$null
                if ($LASTEXITCODE -eq 0) {
                    Write-BatchLog "✓ Issue #$issueNumber component updated to '$Component'" "SUCCESS"
                    $successCount++
                } else {
                    Write-BatchLog "✗ Failed to update issue #$issueNumber" "ERROR"
                    $errorCount++
                }
            } else {
                Write-BatchLog "[DRY RUN] Would update issue #$issueNumber component to '$Component'"
                $successCount++
            }
        } catch {
            Write-BatchLog "✗ Error updating issue #$issueNumber`: $_" "ERROR"
            $errorCount++
        }
    }
    
    Write-BatchLog "Bulk component assignment completed: $successCount success, $errorCount errors"
    return $errorCount -eq 0
}

function Invoke-BulkLabel {
    param(
        [array]$Issues,
        [string]$LabelOperation
    )
    
    if (-not $Labels) {
        Write-BatchLog "No labels specified for bulk label operation" "ERROR"
        return $false
    }
    
    $labelList = $Labels -split "," | ForEach-Object { $_.Trim() }
    $operation = if ($LabelOperation -eq "add") { "--add-label" } else { "--remove-label" }
    
    Write-BatchLog "Starting bulk label operation ($LabelOperation) for $($Issues.Count) issues"
    Write-BatchLog "Labels: $($labelList -join ', ')"
    
    $successCount = 0
    $errorCount = 0
    
    foreach ($issueNumber in $Issues) {
        try {
            if (-not $DryRun) {
                foreach ($label in $labelList) {
                    gh issue edit $issueNumber $operation $label 2>$null
                    if ($LASTEXITCODE -ne 0) {
                        Write-BatchLog "✗ Failed to $LabelOperation label '$label' on issue #$issueNumber" "ERROR"
                        $errorCount++
                        continue
                    }
                }
                Write-BatchLog "✓ Issue #$issueNumber labels updated ($LabelOperation)" "SUCCESS"
                $successCount++
            } else {
                Write-BatchLog "[DRY RUN] Would $LabelOperation labels ($($labelList -join ', ')) on issue #$issueNumber"
                $successCount++
            }
        } catch {
            Write-BatchLog "✗ Error updating issue #$issueNumber`: $_" "ERROR"
            $errorCount++
        }
    }
    
    Write-BatchLog "Bulk label operation completed: $successCount success, $errorCount errors"
    return $errorCount -eq 0
}

function Invoke-BulkAssign {
    param(
        [array]$Issues,
        [string]$Username
    )
    
    if (-not $Username) {
        Write-BatchLog "No assignee specified for bulk assignment" "ERROR"
        return $false
    }
    
    Write-BatchLog "Starting bulk assignment to '$Username' for $($Issues.Count) issues"
    
    $successCount = 0
    $errorCount = 0
    
    foreach ($issueNumber in $Issues) {
        try {
            if (-not $DryRun) {
                gh issue edit $issueNumber --add-assignee $Username 2>$null
                if ($LASTEXITCODE -eq 0) {
                    Write-BatchLog "✓ Issue #$issueNumber assigned to '$Username'" "SUCCESS"
                    $successCount++
                } else {
                    Write-BatchLog "✗ Failed to assign issue #$issueNumber" "ERROR"
                    $errorCount++
                }
            } else {
                Write-BatchLog "[DRY RUN] Would assign issue #$issueNumber to '$Username'"
                $successCount++
            }
        } catch {
            Write-BatchLog "✗ Error assigning issue #$issueNumber`: $_" "ERROR"
            $errorCount++
        }
    }
    
    Write-BatchLog "Bulk assignment completed: $successCount success, $errorCount errors"
    return $errorCount -eq 0
}

function Invoke-BulkClose {
    param(
        [array]$Issues,
        [string]$Reason = "completed"
    )
    
    Write-BatchLog "Starting bulk close operation for $($Issues.Count) issues"
    
    $successCount = 0
    $errorCount = 0
    
    foreach ($issueNumber in $Issues) {
        try {
            if (-not $DryRun) {
                # Update status to implemented before closing
                gh issue edit $issueNumber --add-label "status:implemented" 2>$null | Out-Null
                
                # Close the issue
                gh issue close $issueNumber --reason $Reason 2>$null
                if ($LASTEXITCODE -eq 0) {
                    Write-BatchLog "✓ Issue #$issueNumber closed with reason '$Reason'" "SUCCESS"
                    $successCount++
                } else {
                    Write-BatchLog "✗ Failed to close issue #$issueNumber" "ERROR"
                    $errorCount++
                }
            } else {
                Write-BatchLog "[DRY RUN] Would close issue #$issueNumber with reason '$Reason'"
                $successCount++
            }
        } catch {
            Write-BatchLog "✗ Error closing issue #$issueNumber`: $_" "ERROR"
            $errorCount++
        }
    }
    
    Write-BatchLog "Bulk close operation completed: $successCount success, $errorCount errors"
    return $errorCount -eq 0
}

function Invoke-TriageBatch {
    Write-BatchLog "Starting triage batch processing"
    
    # Get issues that need triage
    $triageIssues = Get-FilteredIssues -Filter "status:needs-triage"
    
    if ($triageIssues.Count -eq 0) {
        Write-BatchLog "No issues found in triage queue" "SUCCESS"
        return $true
    }
    
    Write-BatchLog "Found $($triageIssues.Count) issues needing triage"
    
    if ($Interactive) {
        Write-Host ""
        Write-Host "=== TRIAGE BATCH PROCESSING ===" -ForegroundColor Cyan
        Write-Host "Found $($triageIssues.Count) issues needing triage" -ForegroundColor Yellow
        Write-Host ""
        
        foreach ($issueNumber in $triageIssues) {
            try {
                # Get issue details
                $issueJson = gh issue view $issueNumber --json title,body,labels,assignees 2>$null
                if ($LASTEXITCODE -ne 0) {
                    Write-BatchLog "✗ Failed to get details for issue #$issueNumber" "ERROR"
                    continue
                }
                
                $issue = $issueJson | ConvertFrom-Json
                
                Write-Host ""
                Write-Host "--- Issue #$issueNumber ---" -ForegroundColor White
                Write-Host "Title: $($issue.title)" -ForegroundColor Yellow
                Write-Host "Labels: $($issue.labels.name -join ', ')" -ForegroundColor Gray
                Write-Host ""
                
                # Triage options
                Write-Host "Triage Options:"
                Write-Host "  1. Set Priority (critical/high/medium/low)"
                Write-Host "  2. Assign Component (auto-heal/combat/looting/ui/config/core/build/docs)"
                Write-Host "  3. Change Status (ready-for-pickup/blocked/rejected)"
                Write-Host "  4. Skip this issue"
                Write-Host "  5. Exit triage batch"
                
                do {
                    $choice = Read-Host "Select option [1-5]"
                    switch ($choice) {
                        "1" {
                            $priority = Read-Host "Enter priority (critical/high/medium/low)"
                            if ($priority -in @("critical", "high", "medium", "low")) {
                                Invoke-BulkPriority -Issues @($issueNumber) -Priority $priority
                            } else {
                                Write-Host "Invalid priority" -ForegroundColor Red
                            }
                        }
                        "2" {
                            $component = Read-Host "Enter component (auto-heal/combat/looting/ui/config/core/build/docs)"
                            if ($component -in @("auto-heal", "combat", "looting", "ui", "config", "core", "build", "docs")) {
                                Invoke-BulkComponent -Issues @($issueNumber) -Component $component
                            } else {
                                Write-Host "Invalid component" -ForegroundColor Red
                            }
                        }
                        "3" {
                            $status = Read-Host "Enter status (ready-for-pickup/blocked/rejected)"
                            if ($status -in @("ready-for-pickup", "blocked", "rejected")) {
                                Invoke-BulkStatus -Issues @($issueNumber) -Status $status
                            } else {
                                Write-Host "Invalid status" -ForegroundColor Red
                            }
                        }
                        "4" {
                            Write-Host "Skipping issue #$issueNumber" -ForegroundColor Yellow
                            break
                        }
                        "5" {
                            Write-Host "Exiting triage batch processing" -ForegroundColor Yellow
                            return $true
                        }
                        default {
                            Write-Host "Invalid choice. Please select 1-5." -ForegroundColor Red
                            continue
                        }
                    }
                    break
                } while ($true)
                
            } catch {
                Write-BatchLog "✗ Error processing issue #$issueNumber for triage: $_" "ERROR"
            }
        }
    } else {
        Write-BatchLog "Non-interactive triage batch processing not implemented. Use -Interactive flag." "WARN"
        return $false
    }
    
    Write-BatchLog "Triage batch processing completed"
    return $true
}

function Invoke-FastTrackBatch {
    Write-BatchLog "Starting fast-track batch processing"
    
    # Get fast-track issues
    $fastTrackIssues = Get-FilteredIssues -Filter "label:prd:fast-track"
    
    if ($fastTrackIssues.Count -eq 0) {
        Write-BatchLog "No fast-track issues found" "SUCCESS"
        return $true
    }
    
    Write-BatchLog "Found $($fastTrackIssues.Count) fast-track issues for processing"
    
    $successCount = 0
    $errorCount = 0
    
    foreach ($issueNumber in $fastTrackIssues) {
        try {
            Write-BatchLog "Processing fast-track issue #$issueNumber"
            
            if (-not $DryRun) {
                # Validate PRD using the existing fast-track validator
                $validationResult = & "$PSScriptRoot\manage_issues.ps1" -Action fast-track -IssueNumber $issueNumber -ValidatePRD 2>$null
                
                if ($LASTEXITCODE -eq 0) {
                    # Update status to ready-for-pickup
                    Invoke-BulkStatus -Issues @($issueNumber) -Status "ready-for-pickup"
                    Write-BatchLog "✓ Fast-track issue #$issueNumber processed successfully" "SUCCESS"
                    $successCount++
                } else {
                    Write-BatchLog "✗ Fast-track validation failed for issue #$issueNumber" "ERROR"
                    $errorCount++
                }
            } else {
                Write-BatchLog "[DRY RUN] Would process fast-track issue #$issueNumber"
                $successCount++
            }
        } catch {
            Write-BatchLog "✗ Error processing fast-track issue #$issueNumber`: $_" "ERROR"
            $errorCount++
        }
    }
    
    Write-BatchLog "Fast-track batch processing completed: $successCount success, $errorCount errors"
    return $errorCount -eq 0
}

# ================================================================================
# MAIN EXECUTION
# ================================================================================

function Main {
    Write-Host "DexBot Batch Operations for GitHub Issues" -ForegroundColor Cyan
    Write-Host "======================================" -ForegroundColor Cyan
    
    # Validate prerequisites
    if (-not (Test-GitHubCLI)) {
        exit 1
    }
    
    Write-BatchLog "Starting batch operation: $Action"
    
    # Get issue list based on parameters
    $issueList = Get-IssueList -Numbers $IssueNumbers -File $IssueFile -FilterCriteria $Filter
    
    if ($issueList.Count -eq 0 -and $Action -notin @("triage-batch", "fast-track-batch")) {
        Write-BatchLog "No issues specified for processing" "ERROR"
        Write-Host ""
        Write-Host "Usage examples:" -ForegroundColor Yellow
        Write-Host "  .\batch_operations.ps1 -Action bulk-status -IssueNumbers '1,2,3' -NewValue 'in-progress'"
        Write-Host "  .\batch_operations.ps1 -Action bulk-priority -Filter 'status:needs-triage' -NewValue 'medium'"
        Write-Host "  .\batch_operations.ps1 -Action triage-batch -Interactive"
        exit 1
    }
    
    # Execute batch operation
    $success = $false
    
    switch ($Action) {
        "bulk-status" {
            if (-not $NewValue) {
                Write-BatchLog "NewValue parameter required for bulk-status operation" "ERROR"
                exit 1
            }
            if (Confirm-BatchOperation -Operation "Status Update" -Issues $issueList -NewValue $NewValue) {
                $success = Invoke-BulkStatus -Issues $issueList -Status $NewValue
            }
        }
        "bulk-priority" {
            if (-not $NewValue) {
                Write-BatchLog "NewValue parameter required for bulk-priority operation" "ERROR"
                exit 1
            }
            if (Confirm-BatchOperation -Operation "Priority Update" -Issues $issueList -NewValue $NewValue) {
                $success = Invoke-BulkPriority -Issues $issueList -Priority $NewValue
            }
        }
        "bulk-component" {
            if (-not $NewValue) {
                Write-BatchLog "NewValue parameter required for bulk-component operation" "ERROR"
                exit 1
            }
            if (Confirm-BatchOperation -Operation "Component Assignment" -Issues $issueList -NewValue $NewValue) {
                $success = Invoke-BulkComponent -Issues $issueList -Component $NewValue
            }
        }
        "bulk-label" {
            if (-not $Labels) {
                Write-BatchLog "Labels parameter required for bulk-label operation" "ERROR"
                exit 1
            }
            $operation = if ($NewValue -eq "remove") { "remove" } else { "add" }
            if (Confirm-BatchOperation -Operation "Label $operation" -Issues $issueList -NewValue $Labels) {
                $success = Invoke-BulkLabel -Issues $issueList -LabelOperation $operation
            }
        }
        "bulk-assign" {
            if (-not $Assignee) {
                Write-BatchLog "Assignee parameter required for bulk-assign operation" "ERROR"
                exit 1
            }
            if (Confirm-BatchOperation -Operation "Assignment" -Issues $issueList -NewValue $Assignee) {
                $success = Invoke-BulkAssign -Issues $issueList -Username $Assignee
            }
        }
        "bulk-close" {
            $reason = if ($NewValue) { $NewValue } else { "completed" }
            if (Confirm-BatchOperation -Operation "Close Issues" -Issues $issueList -NewValue $reason) {
                $success = Invoke-BulkClose -Issues $issueList -Reason $reason
            }
        }
        "bulk-archive" {
            # Archive is essentially closing with "not planned" reason
            if (Confirm-BatchOperation -Operation "Archive Issues" -Issues $issueList -NewValue "archive") {
                $success = Invoke-BulkClose -Issues $issueList -Reason "not_planned"
            }
        }
        "triage-batch" {
            $success = Invoke-TriageBatch
        }
        "fast-track-batch" {
            $success = Invoke-FastTrackBatch
        }
        default {
            Write-BatchLog "Unknown action: $Action" "ERROR"
            exit 1
        }
    }
    
    # Summary
    Write-Host ""
    if ($success) {
        Write-Host "Batch operation completed successfully!" -ForegroundColor Green
        Write-BatchLog "Batch operation '$Action' completed successfully" "SUCCESS"
    } else {
        Write-Host "Batch operation completed with errors." -ForegroundColor Red
        Write-BatchLog "Batch operation '$Action' completed with errors" "ERROR"
    }
    
    Write-Host "Log file: $LogFile" -ForegroundColor Gray
    
    if ($success) {
        exit 0
    } else {
        exit 1
    }
}

# Run main function
Main

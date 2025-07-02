# Full Automation Suite Example Scenarios

This document provides detailed examples of how to use the Full Automation Suite for common GitHub issue management workflows.

## Example 1: Setting Up a New Repository

When setting up automation for a new repository, follow these steps:

```powershell
# 1. Initial setup with repository configuration
.\scripts\full_automation_suite.ps1 -Action setup -Repository "DexBot/NewRepo" -WebhookSecret "your-secret-here"

# 2. Configure component categories specific to your repository
$configPath = ".\config\automation_config.json"
$config = Get-Content $configPath -Raw | ConvertFrom-Json
$config.intelligent_routing.component_categories = @(
    "core", 
    "api", 
    "ui", 
    "documentation", 
    "build", 
    "testing"
)
$config | ConvertTo-Json -Depth 10 | Set-Content $configPath

# 3. Generate initial GitHub Actions workflow file
.\scripts\full_automation_suite.ps1 -Action generate-workflow -OutputFile ".github/workflows/issue-automation.yml"

# 4. Perform initial analysis of existing issues
.\scripts\full_automation_suite.ps1 -Action batch-route -State all -GenerateReport
```

## Example 2: Processing High-Priority Issues

For immediate handling of high-priority issues:

```powershell
# 1. Identify critical issues
$criticalIssues = .\scripts\full_automation_suite.ps1 -Action find-issues -Priority critical -Format json | ConvertFrom-Json

# 2. Process each critical issue with special handling
foreach ($issue in $criticalIssues) {
    # Route to appropriate component
    .\scripts\full_automation_suite.ps1 -Action route-issue -IssueNumber $issue.number
    
    # Add priority label and notify team
    .\scripts\full_automation_suite.ps1 -Action label-issue -IssueNumber $issue.number -Label "priority:critical"
    .\scripts\full_automation_suite.ps1 -Action notify-team -IssueNumber $issue.number -Channel "slack"
}

# 3. Generate impact report
.\scripts\full_automation_suite.ps1 -Action generate-report -ReportType "impact" -Issues $criticalIssues.number -OutputFile "reports/critical_impact_report.html"
```

## Example 3: Setting Up Automated Weekly Reports

For regular reporting on issue status and trends:

```powershell
# Create a scheduled task for weekly reporting (Windows)
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File `"C:\Path\To\DexBot\scripts\full_automation_suite.ps1`" -Action generate-report -ReportType weekly -OutputFile `"reports/weekly_report_$(Get-Date -Format 'yyyy-MM-dd').html`""
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 9am
$settings = New-ScheduledTaskSettingsSet -RunOnlyIfNetworkAvailable -WakeToRun
Register-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -TaskName "DexBot Weekly Report" -Description "Generate weekly issue analytics report"
```

## Example 4: Intelligent Routing with Custom Rules

For repositories with specialized categorization needs:

```powershell
# 1. Create custom routing rules
$customRules = @"
{
    "rules": [
        {
            "pattern": "database|sql|query|table",
            "component": "database",
            "priority": "high"
        },
        {
            "pattern": "security|authentication|auth|login|password",
            "component": "security",
            "priority": "critical"
        },
        {
            "pattern": "performance|slow|timeout|latency",
            "component": "performance",
            "priority": "medium"
        }
    ]
}
"@ | Out-File -FilePath "config/custom_routing_rules.json"

# 2. Update configuration to use custom rules
$configPath = ".\config\automation_config.json"
$config = Get-Content $configPath -Raw | ConvertFrom-Json
$config.intelligent_routing.custom_rules_file = "config/custom_routing_rules.json"
$config | ConvertTo-Json -Depth 10 | Set-Content $configPath

# 3. Test the custom rules
.\scripts\full_automation_suite.ps1 -Action test-routing -InputText "Database query performance is slow when joining large tables" -Verbose
```

## Example 5: Integration with External Systems

For connecting the automation suite with external project management tools:

```powershell
# 1. Configure external system integration
$configPath = ".\config\automation_config.json"
$config = Get-Content $configPath -Raw | ConvertFrom-Json

# Add JIRA integration settings
$config.integrations = @{
    "jira" = @{
        "enabled" = $true
        "url" = "https://your-company.atlassian.net"
        "project_key" = "PROJ"
        "username" = "jira_username"
        "api_token" = "jira_api_token"
        "sync_status" = $true
        "sync_comments" = $true
    }
}

$config | ConvertTo-Json -Depth 10 | Set-Content $configPath

# 2. Sync issues with JIRA
.\scripts\full_automation_suite.ps1 -Action sync-external -System jira -Direction both
```

## Example 6: Self-Optimization Configuration

For enabling the self-learning capabilities of the automation system:

```powershell
# 1. Enable self-optimization
$configPath = ".\config\automation_config.json"
$config = Get-Content $configPath -Raw | ConvertFrom-Json

$config.self_optimization = @{
    "enabled" = $true
    "learning_rate" = 0.05
    "history_days" = 30
    "min_samples" = 50
    "confidence_threshold_adjustment" = $true
    "auto_update_rules" = $true
    "accuracy_report_frequency_days" = 7
}

$config | ConvertTo-Json -Depth 10 | Set-Content $configPath

# 2. Initiate learning from historical data
.\scripts\full_automation_suite.ps1 -Action learn -HistoryDays 90 -Verbose

# 3. Generate accuracy report
.\scripts\full_automation_suite.ps1 -Action optimization-report -OutputFile "reports/self_optimization_results.html"
```

## Example 7: Disaster Recovery and Backup

For ensuring your automation configuration is backed up and recoverable:

```powershell
# 1. Create backup of configuration
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = ".\backups\$timestamp"
New-Item -Path $backupDir -ItemType Directory -Force

# Backup all configuration files
Copy-Item ".\config\*.json" -Destination $backupDir
Copy-Item ".\.github\workflows\*.yml" -Destination $backupDir

# 2. Export current system state
.\scripts\full_automation_suite.ps1 -Action export-state -OutputFile "$backupDir\system_state.json"

# 3. Create restoration script
@"
# Restoration script generated $(Get-Date)
# To restore this configuration:
Copy-Item "$backupDir\*.json" -Destination ".\config\"
Copy-Item "$backupDir\*.yml" -Destination ".\.github\workflows\"
.\scripts\full_automation_suite.ps1 -Action import-state -InputFile "$backupDir\system_state.json"
"@ | Out-File -FilePath "$backupDir\restore.ps1"

# 4. Test restoration in a temporary location
$testDir = ".\test_restore"
New-Item -Path $testDir -ItemType Directory -Force
Copy-Item "$backupDir\*" -Destination $testDir -Recurse
Push-Location $testDir
.\restore.ps1
Pop-Location
```

These examples demonstrate the flexibility and power of the Full Automation Suite for various GitHub issue management scenarios.

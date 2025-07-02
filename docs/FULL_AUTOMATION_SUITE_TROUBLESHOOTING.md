# Full Automation Suite Troubleshooting Guide

This document provides solutions to common issues encountered when using the Full Automation Suite.

## Authentication Issues

### Problem: GitHub API Authentication Failures

**Symptoms:**
- Error messages containing "401 Unauthorized"
- "Bad credentials" errors
- Authentication-related exceptions

**Solutions:**

1. **Verify Token Validity**
   ```powershell
   # Test if your token is valid
   $token = "<your-token>"
   $headers = @{
       Authorization = "token $token"
       Accept = "application/vnd.github.v3+json"
   }
   Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers
   ```

2. **Check Token Permissions**
   - Ensure your token has the `repo` scope
   - For organization repositories, verify you have the correct organization permissions

3. **Token Expiration**
   - GitHub tokens might have expiration dates
   - Generate a new token if yours has expired

4. **Rate Limiting**
   - Check if you've hit GitHub's API rate limits
   ```powershell
   Invoke-RestMethod -Uri "https://api.github.com/rate_limit" -Headers $headers
   ```

5. **Update Authentication in Script**
   ```powershell
   # Set your token directly in the script
   Set-GitHubAuthentication -Token "<your-new-token>"
   ```

## Webhook Configuration Issues

### Problem: Webhooks Not Triggering Automation

**Symptoms:**
- No activity when creating or updating issues
- No logs generated for webhook events
- GitHub shows successful delivery but no action taken

**Solutions:**

1. **Verify Webhook Configuration**
   - Check the webhook in GitHub repository settings
   - Ensure the webhook secret matches your configuration
   - Verify the correct events are selected (Issues, Issue comments)

2. **Check Webhook Delivery Logs**
   - In GitHub repository settings, check Recent Deliveries
   - Look for successful 200 responses
   - Examine the payload and response for errors

3. **Test Webhook Endpoint**
   ```powershell
   # Create a test webhook payload
   $payload = @{
       action = "opened"
       issue = @{
           number = 1
           title = "Test Issue"
           body = "This is a test issue for webhook validation"
       }
       repository = @{
           full_name = "owner/repo"
       }
   } | ConvertTo-Json

   # Send test payload to your endpoint
   Invoke-RestMethod -Uri "your-webhook-endpoint" -Method Post -Body $payload -ContentType "application/json"
   ```

4. **Verify Firewall Settings**
   - Ensure your server allows incoming connections on the webhook endpoint port
   - Check that GitHub IPs are not blocked

5. **Reinstall Webhook**
   ```powershell
   # Remove and recreate the webhook
   .\scripts\full_automation_suite.ps1 -Action setup-webhook -Repository "owner/repo" -Force
   ```

## Intelligent Routing Issues

### Problem: Incorrect Issue Routing

**Symptoms:**
- Issues assigned to wrong components
- Low confidence scores in routing decisions
- Inconsistent priority assignments

**Solutions:**

1. **Adjust Confidence Threshold**
   ```powershell
   # Update configuration file
   $configPath = ".\config\automation_config.json"
   $config = Get-Content $configPath -Raw | ConvertFrom-Json
   $config.intelligent_routing.confidence_threshold = 0.65  # Lower for more matches
   $config | ConvertTo-Json -Depth 10 | Set-Content $configPath
   ```

2. **Add Custom Routing Rules**
   ```powershell
   # Create or update custom rules
   $rulesPath = ".\config\custom_routing_rules.json"
   $rules = @{
       rules = @(
           @{
               pattern = "database|sql|query"
               component = "database"
               priority = "medium"
               weight = 1.0
           }
       )
       keywords = @{
           ui = @(
               @{ word = "interface"; weight = 1.0 },
               @{ word = "button"; weight = 0.9 }
           )
       }
   } | ConvertTo-Json -Depth 5
   $rules | Out-File -FilePath $rulesPath -Encoding UTF8
   
   # Update main config to use custom rules
   $config = Get-Content $configPath -Raw | ConvertFrom-Json
   $config.intelligent_routing.custom_rules_file = $rulesPath
   $config | ConvertTo-Json -Depth 10 | Set-Content $configPath
   ```

3. **Test Routing with Sample Issues**
   ```powershell
   # Test with various issue texts
   .\scripts\intelligent_routing.ps1 -Action analyze -IssueText "Database query performance is slow" -Format json
   ```

4. **Retrain the Model**
   ```powershell
   # Retrain with more samples
   .\scripts\full_automation_suite.ps1 -Action retrain -HistoryDays 90
   ```

5. **Check Component Categories**
   - Verify your component categories are comprehensive
   - Add missing categories to cover all issue types

## Performance Issues

### Problem: Slow Script Execution

**Symptoms:**
- Long execution times for automation tasks
- High CPU usage
- Memory consumption issues

**Solutions:**

1. **Enable Parallel Processing**
   ```powershell
   # Update configuration
   $configPath = ".\config\automation_config.json"
   $config = Get-Content $configPath -Raw | ConvertFrom-Json
   
   if (-not $config.advanced_settings) {
       $config | Add-Member -NotePropertyName "advanced_settings" -NotePropertyValue @{}
   }
   
   $config.advanced_settings.parallel_processing = $true
   $config.advanced_settings.max_parallel_threads = 4
   $config | ConvertTo-Json -Depth 10 | Set-Content $configPath
   ```

2. **Optimize API Usage**
   ```powershell
   # Update API batch size
   $config.advanced_settings.api_batch_size = 50
   $config.advanced_settings.cache_timeout_minutes = 60
   $config | ConvertTo-Json -Depth 10 | Set-Content $configPath
   ```

3. **Run Performance Diagnostics**
   ```powershell
   # Run with timing measurements
   Measure-Command { 
       .\scripts\full_automation_suite.ps1 -Action orchestrate -Repository "owner/repo" -Verbose 
   }
   ```

4. **Profile Script Execution**
   ```powershell
   # Install and use profiler
   Install-Module -Name PSProfiler -Scope CurrentUser
   Import-Module PSProfiler
   
   $profiler = New-PSProfiler
   $profiler.Start()
   .\scripts\full_automation_suite.ps1 -Action orchestrate -Repository "owner/repo"
   $profiler.Stop()
   $profiler.GetResults() | Sort-Object -Property ElapsedMS -Descending | Select-Object -First 10
   ```

5. **Run in Background Mode**
   ```powershell
   # For long-running tasks, use background jobs
   Start-Job -ScriptBlock {
       cd "C:\Path\To\DexBot"
       .\scripts\full_automation_suite.ps1 -Action batch-route -State all
   }
   ```

## Integration Issues

### Problem: External System Integration Failures

**Symptoms:**
- Failed connections to external systems (JIRA, Slack, etc.)
- Error messages about missing credentials
- Synchronization failures

**Solutions:**

1. **Verify Credentials**
   ```powershell
   # Test JIRA connection
   $configPath = ".\config\automation_config.json"
   $config = Get-Content $configPath -Raw | ConvertFrom-Json
   
   $jira = $config.integrations.jira
   $headers = @{
       Authorization = "Basic " + [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("$($jira.username):$($jira.api_token)"))
   }
   
   try {
       Invoke-RestMethod -Uri "$($jira.url)/rest/api/2/project/$($jira.project_key)" -Headers $headers
       Write-Host "JIRA connection successful" -ForegroundColor Green
   } catch {
       Write-Host "JIRA connection failed: $_" -ForegroundColor Red
   }
   ```

2. **Update Integration Settings**
   ```powershell
   # Update JIRA settings
   $config.integrations.jira.username = "new_username"
   $config.integrations.jira.api_token = "new_token"
   $config | ConvertTo-Json -Depth 10 | Set-Content $configPath
   ```

3. **Test Slack Integration**
   ```powershell
   # Test Slack webhook
   $slackPayload = @{
       text = "Test message from DexBot Automation Suite"
   } | ConvertTo-Json
   
   Invoke-RestMethod -Uri $config.integrations.slack.webhook_url -Method Post -Body $slackPayload -ContentType "application/json"
   ```

4. **Check Network Connectivity**
   - Verify your server can reach external services
   - Check for proxy requirements
   - Ensure SSL/TLS versions are compatible

5. **Enable Debug Logging**
   ```powershell
   # Run with detailed logging
   .\scripts\full_automation_suite.ps1 -Action sync-external -System jira -Debug
   ```

## Configuration Issues

### Problem: Configuration File Problems

**Symptoms:**
- "Configuration file not found" errors
- Invalid JSON errors
- Missing configuration sections

**Solutions:**

1. **Validate JSON Syntax**
   ```powershell
   # Check if JSON is valid
   $configPath = ".\config\automation_config.json"
   try {
       $config = Get-Content $configPath -Raw | ConvertFrom-Json
       Write-Host "Configuration file is valid JSON" -ForegroundColor Green
   } catch {
       Write-Host "Invalid JSON in configuration file: $_" -ForegroundColor Red
   }
   ```

2. **Restore Default Configuration**
   ```powershell
   # Generate default configuration
   .\scripts\full_automation_suite.ps1 -Action generate-config -OutputFile ".\config\automation_config.new.json"
   
   # Compare with current config
   if (Test-Path ".\config\automation_config.json") {
       Copy-Item ".\config\automation_config.json" ".\config\automation_config.backup.json"
   }
   Move-Item ".\config\automation_config.new.json" ".\config\automation_config.json" -Force
   ```

3. **Verify Required Sections**
   ```powershell
   # Check for required configuration sections
   $config = Get-Content $configPath -Raw | ConvertFrom-Json
   $requiredSections = @("intelligent_routing", "webhook_configuration")
   
   foreach ($section in $requiredSections) {
       if (-not (Get-Member -InputObject $config -Name $section -MemberType NoteProperty)) {
           Write-Host "Missing required section: $section" -ForegroundColor Red
       }
   }
   ```

4. **Use Environment Variables**
   ```powershell
   # Set environment variables to override config
   $env:GITHUB_TOKEN = "your-github-token"
   $env:AUTOMATION_REPO = "owner/repo"
   $env:WEBHOOK_SECRET = "your-webhook-secret"
   
   # Test with environment variables
   .\scripts\full_automation_suite.ps1 -Action orchestrate
   ```

5. **Fix Path Issues**
   ```powershell
   # Use absolute paths in configuration
   $config = Get-Content $configPath -Raw | ConvertFrom-Json
   $config.intelligent_routing.custom_rules_file = Join-Path $PSScriptRoot "config\custom_routing_rules.json"
   $config | ConvertTo-Json -Depth 10 | Set-Content $configPath
   ```

## Logging and Debugging

### Problem: Insufficient Diagnostic Information

**Symptoms:**
- Unclear error messages
- Difficulty determining source of issues
- No log files generated

**Solutions:**

1. **Enable Debug Mode**
   ```powershell
   # Run with verbose and debug output
   .\scripts\full_automation_suite.ps1 -Action orchestrate -Repository "owner/repo" -Verbose -Debug
   ```

2. **Configure Logging**
   ```powershell
   # Update logging configuration
   $configPath = ".\config\automation_config.json"
   $config = Get-Content $configPath -Raw | ConvertFrom-Json
   
   if (-not $config.advanced_settings) {
       $config | Add-Member -NotePropertyName "advanced_settings" -NotePropertyValue @{}
   }
   
   $config.advanced_settings.log_level = "Debug"
   $config.advanced_settings.log_file = "logs/automation_$(Get-Date -Format 'yyyyMMdd').log"
   $config | ConvertTo-Json -Depth 10 | Set-Content $configPath
   ```

3. **Create Log Directory**
   ```powershell
   # Ensure log directory exists
   if (-not (Test-Path "logs")) {
       New-Item -Path "logs" -ItemType Directory
   }
   ```

4. **Add Transcript Logging**
   ```powershell
   # Start transcript for detailed logging
   $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
   Start-Transcript -Path "logs/transcript_$timestamp.log"
   
   # Run your commands
   .\scripts\full_automation_suite.ps1 -Action orchestrate -Repository "owner/repo"
   
   # Stop transcript
   Stop-Transcript
   ```

5. **Enable PowerShell Script Debugging**
   ```powershell
   # Set PowerShell debugging preferences
   $DebugPreference = "Continue"
   $VerbosePreference = "Continue"
   
   # Run with built-in debugging
   .\scripts\full_automation_suite.ps1 -Action orchestrate -Repository "owner/repo"
   ```

## Workflow Automation Issues

### Problem: GitHub Actions Workflow Failures

**Symptoms:**
- Failed GitHub Actions runs
- Error messages in workflow logs
- Automation not triggered by events

**Solutions:**

1. **Check Workflow File Syntax**
   ```powershell
   # Generate a validated workflow file
   .\scripts\full_automation_suite.ps1 -Action generate-workflow -OutputFile ".github/workflows/issue-automation.yml" -Validate
   ```

2. **Verify GitHub Secrets**
   - Check that `GITHUB_TOKEN` is available in the workflow
   - Verify any custom secrets are properly configured

3. **Test Workflow Locally**
   ```powershell
   # Install act to test GitHub Actions locally
   # https://github.com/nektos/act
   
   # Run workflow locally
   act issue -e test/fixtures/issue_opened.json
   ```

4. **Review Action Logs**
   - Go to your repository on GitHub
   - Navigate to Actions tab
   - Find the failed workflow run
   - Review logs for specific errors

5. **Update GitHub Actions Configuration**
   ```powershell
   # Generate updated workflow file
   .\scripts\full_automation_suite.ps1 -Action generate-workflow -OutputFile ".github/workflows/issue-automation.yml" -Force
   
   # Commit and push changes
   git add .github/workflows/issue-automation.yml
   git commit -m "Update issue automation workflow"
   git push
   ```

## Self-Optimization Issues

### Problem: Self-Learning Not Improving Results

**Symptoms:**
- No improvement in routing accuracy over time
- Learning doesn't seem to be active
- No optimization reports generated

**Solutions:**

1. **Verify Self-Optimization Settings**
   ```powershell
   # Check current settings
   $configPath = ".\config\automation_config.json"
   $config = Get-Content $configPath -Raw | ConvertFrom-Json
   
   # Ensure self-optimization is properly configured
   if (-not $config.self_optimization) {
       $config | Add-Member -NotePropertyName "self_optimization" -NotePropertyValue @{
           enabled = $true
           learning_rate = 0.05
           history_days = 30
           min_samples = 20  # Lower threshold to start learning sooner
           confidence_threshold_adjustment = $true
           auto_update_rules = $true
           accuracy_report_frequency_days = 7
       }
       $config | ConvertTo-Json -Depth 10 | Set-Content $configPath
   } else {
       $config.self_optimization.enabled = $true
       $config.self_optimization.min_samples = 20  # Lower threshold
       $config | ConvertTo-Json -Depth 10 | Set-Content $configPath
   }
   ```

2. **Force Learning From Historical Data**
   ```powershell
   # Force learning from more historical data
   .\scripts\full_automation_suite.ps1 -Action learn -HistoryDays 90 -Force
   ```

3. **Generate Optimization Report**
   ```powershell
   # Generate report to check learning status
   .\scripts\full_automation_suite.ps1 -Action optimization-report -OutputFile "reports/self_optimization_status.html"
   ```

4. **Reset Learning Data**
   ```powershell
   # Reset learning data and start fresh
   .\scripts\full_automation_suite.ps1 -Action reset-learning -Confirm:$false
   ```

5. **Manually Provide Training Examples**
   ```powershell
   # Create training data file
   $trainingData = @(
       @{
           text = "Database query performance is slow"
           component = "database"
           priority = "high"
       },
       @{
           text = "Button click not working in Firefox"
           component = "ui"
           priority = "medium"
       }
   ) | ConvertTo-Json -Depth 3
   
   $trainingData | Out-File -FilePath "training_examples.json"
   
   # Import training data
   .\scripts\full_automation_suite.ps1 -Action import-training -InputFile "training_examples.json"
   ```

## Recovery Procedures

### Emergency Recovery for Critical Failures

If you encounter critical failures that require immediate resolution:

1. **Revert to Last Known Good Configuration**
   ```powershell
   # Look for backup configurations
   $backups = Get-ChildItem -Path ".\config\*backup*.json"
   
   if ($backups.Count -gt 0) {
       # Get most recent backup
       $latestBackup = $backups | Sort-Object LastWriteTime -Descending | Select-Object -First 1
       
       # Restore backup
       Copy-Item -Path $latestBackup.FullName -Destination ".\config\automation_config.json" -Force
       Write-Host "Restored configuration from: $($latestBackup.Name)" -ForegroundColor Green
   } else {
       # Generate new default configuration
       .\scripts\full_automation_suite.ps1 -Action generate-config -OutputFile ".\config\automation_config.json" -Force
       Write-Host "Generated new default configuration" -ForegroundColor Yellow
   }
   ```

2. **Disable Automation Temporarily**
   ```powershell
   # Update config to disable automation
   $configPath = ".\config\automation_config.json"
   $config = Get-Content $configPath -Raw | ConvertFrom-Json
   
   $config.intelligent_routing.enabled = $false
   $config.predictive_dashboard.enabled = $false
   if ($config.self_optimization) { $config.self_optimization.enabled = $false }
   
   $config | ConvertTo-Json -Depth 10 | Set-Content $configPath
   
   Write-Host "Automation temporarily disabled" -ForegroundColor Yellow
   ```

3. **Emergency Webhook Deactivation**
   - Go to your repository settings on GitHub
   - Navigate to Webhooks
   - Locate your automation webhook
   - Click "Edit" and uncheck "Active"
   - Click "Update webhook"

4. **Collect Diagnostic Information**
   ```powershell
   # Create diagnostic package
   $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
   $diagnosticDir = "diagnostics_$timestamp"
   New-Item -Path $diagnosticDir -ItemType Directory
   
   # Copy configuration files
   Copy-Item -Path ".\config\*.json" -Destination $diagnosticDir
   
   # Get system information
   $systemInfo = @{
       PowerShellVersion = $PSVersionTable.PSVersion.ToString()
       OS = [System.Environment]::OSVersion.ToString()
       ModuleVersions = Get-Module -ListAvailable PowerShellForGitHub | Select-Object Name, Version
   } | ConvertTo-Json
   
   $systemInfo | Out-File -FilePath "$diagnosticDir\system_info.json"
   
   # Run diagnostics
   .\scripts\full_automation_suite.ps1 -Action diagnostics -OutputFile "$diagnosticDir\diagnostics_report.json"
   
   # Create archive
   Compress-Archive -Path $diagnosticDir -DestinationPath "automation_diagnostics_$timestamp.zip"
   
   Write-Host "Diagnostic information collected in: automation_diagnostics_$timestamp.zip" -ForegroundColor Green
   ```

5. **Restore Default Webhook**
   ```powershell
   # Create new webhook with default settings
   .\scripts\full_automation_suite.ps1 -Action setup-webhook -Repository "owner/repo" -Force
   ```

## Getting Additional Help

If you're still experiencing issues after trying these solutions:

1. Check the detailed documentation in the `docs/` directory
2. Review GitHub Issues in the DexBot repository for similar problems
3. Create a new issue with detailed diagnostic information
4. Contact the project maintainers directly

## Appendix: Common Error Messages and Solutions

| Error Message | Likely Cause | Solution |
|---------------|--------------|----------|
| "Could not find configuration file" | Missing or moved config file | Run `-Action generate-config` to create default |
| "Invalid repository format" | Incorrect owner/repo format | Use "owner/repo" format exactly |
| "Webhook secret missing" | Webhook secret not configured | Run `-Action setup-webhook` to generate |
| "401 Unauthorized" | Invalid GitHub token | Update token or authentication |
| "403 Forbidden" | Insufficient permissions | Check token scopes and permissions |
| "404 Not Found" | Repository doesn't exist or no access | Verify repository name and access |
| "No matching component found" | Component categorization issue | Add more components or custom rules |
| "Self-optimization disabled" | Feature not enabled | Enable in configuration |
| "Failed to parse JSON" | Invalid JSON in config | Validate JSON syntax |
| "PowerShellForGitHub module not found" | Missing dependency | Install required module |

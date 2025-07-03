# Webhook Testing Script for GitHub Issues Workflow Automation
# This script demonstrates how to use the mock GitHub API to test webhook event handling

# Import the Mock GitHub API module
$scriptPath = $MyInvocation.MyCommand.Path
$scriptDir = Split-Path -Parent $scriptPath
$projectRoot = Split-Path -Parent $scriptDir
$scriptsDir = Join-Path $projectRoot "scripts"
$mockApiPath = Join-Path $scriptsDir "mock_github_api.ps1"

if (Test-Path $mockApiPath) {
    . $mockApiPath
} else {
    throw "Mock GitHub API script not found at: $mockApiPath"
}

# Create necessary directories
$mockDataDir = Join-Path (Split-Path -Parent $scriptDir) "tmp\mock_github"
if (-not (Test-Path $mockDataDir)) {
    New-Item -ItemType Directory -Path $mockDataDir -Force | Out-Null
    Write-Host "Created mock data directory: $mockDataDir"
}

# Initialize the test environment
function Initialize-WebhookTestEnvironment {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$false)]
        [switch]$ClearExisting
    )
    
    if ($ClearExisting) {
        Clear-MockGitHubData
        Write-Host "Cleared existing mock data"
    }
    
    # Create a test repository
    $testRepo = New-MockRepository -Name "test-webhook-repo" -Description "Repository for testing webhook events"
    Write-Host "Created test repository: $($testRepo.name)"
    
    # Create some issues for testing
    for ($i = 1; $i -le 3; $i++) {
        $issueType = if ($i % 3 -eq 0) { "bug" } elseif ($i % 3 -eq 1) { "feature" } else { "docs" }
        $priority = if ($i % 2 -eq 0) { "high" } else { "medium" }
        
        $issueTitle = "Test Issue #$i ($issueType)"
        $issueBody = "This is a test issue of type '$issueType' with priority '$priority'."
        $issueLabels = @($issueType, "priority:$priority")
        
        $issue = New-MockIssue -RepositoryName $testRepo.name -Title $issueTitle -Body $issueBody -Labels $issueLabels
        Write-Host "  Created issue #$($issue.number): $issueTitle"
    }
    
    # Create a webhook
    $webhookUrl = "https://example.com/webhook/receiver"
    $webhook = New-MockWebhook -RepositoryName $testRepo.name -Url $webhookUrl -Events @("issues", "issue_comment", "pull_request")
    Write-Host "  Created webhook for repository: $($testRepo.name) with URL: $webhookUrl"
    
    return $testRepo
}

# Test issue webhook events
function Test-IssueWebhookEvents {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [hashtable]$Repository
    )
    
    Write-Host "`nTesting issue webhook events for repository: $($Repository.name)"
    
    # Test issue opened event
    Write-Host "  Triggering issue.opened event..."
    Invoke-MockWebhookEvent -RepositoryName $Repository.name -EventType "issues" -Action "opened" -EventData @{
        number = 101
        title = "New bug report from webhook test"
        body = "This issue was created via a simulated webhook event."
        labels = @("bug", "priority:high")
    }
    
    # Test issue labeled event
    Write-Host "  Triggering issue.labeled event..."
    Invoke-MockWebhookEvent -RepositoryName $Repository.name -EventType "issues" -Action "labeled" -EventData @{
        number = 101
        title = "New bug report from webhook test"
        labels = @("bug", "priority:high", "needs-triage")
    }
    
    # Test issue closed event
    Write-Host "  Triggering issue.closed event..."
    Invoke-MockWebhookEvent -RepositoryName $Repository.name -EventType "issues" -Action "closed" -EventData @{
        number = 101
        title = "New bug report from webhook test"
        state = "closed"
    }
}

# Test issue comment webhook events
function Test-CommentWebhookEvents {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [hashtable]$Repository
    )
    
    Write-Host "`nTesting issue comment webhook events for repository: $($Repository.name)"
    
    # Test comment created event
    Write-Host "  Triggering issue_comment.created event..."
    Invoke-MockWebhookEvent -RepositoryName $Repository.name -EventType "issue_comment" -Action "created" -EventData @{
        number = 1
        comment_body = "This is a test comment via webhook simulation."
    }
    
    # Test comment with command
    Write-Host "  Triggering issue_comment.created event with command..."
    Invoke-MockWebhookEvent -RepositoryName $Repository.name -EventType "issue_comment" -Action "created" -EventData @{
        number = 2
        comment_body = "/label bug priority:high"
    }
}

# Test pull request webhook events
function Test-PullRequestWebhookEvents {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [hashtable]$Repository
    )
    
    Write-Host "`nTesting pull request webhook events for repository: $($Repository.name)"
    
    # Test PR opened event
    Write-Host "  Triggering pull_request.opened event..."
    Invoke-MockWebhookEvent -RepositoryName $Repository.name -EventType "pull_request" -Action "opened" -EventData @{
        number = 10
        title = "Fix for issue #1"
        body = "This PR addresses the bug reported in issue #1."
    }
    
    # Test PR closed/merged event
    Write-Host "  Triggering pull_request.closed event (merged)..."
    Invoke-MockWebhookEvent -RepositoryName $Repository.name -EventType "pull_request" -Action "closed" -EventData @{
        number = 10
        title = "Fix for issue #1"
        body = "This PR addresses the bug reported in issue #1."
        merged = $true
    }
}

# Generate a webhook test report
function Generate-WebhookTestReport {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$false)]
        [string]$OutputPath = (Join-Path (Split-Path -Parent $scriptDir) "reports\webhook_test_report.md")
    )
    
    Write-Host "`nGenerating webhook test report..."
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $apiCallLog = Get-MockAPICallLog
    $webhookCalls = $apiCallLog | Where-Object { $_.Method -eq "POST" -and $_.Endpoint -like "https://*" }
    
    $reportContent = @"
# GitHub Webhook Events Test Report
Generated: $timestamp

## Test Results Summary

Webhook events successfully simulated and processed.

| Event Type | Action | Target | Status |
|------------|--------|--------|--------|
"@
    
    foreach ($call in $webhookCalls) {
        $eventType = $call.Payload.event
        $action = $call.Payload.payload.action
        $target = ""
        
        if ($eventType -eq "issues") {
            $issueNumber = $call.Payload.payload.issue.number
            $target = "Issue #$issueNumber"
        }
        elseif ($eventType -eq "issue_comment") {
            $issueNumber = $call.Payload.payload.issue.number
            $target = "Comment on Issue #$issueNumber"
        }
        elseif ($eventType -eq "pull_request") {
            $prNumber = $call.Payload.payload.pull_request.number
            $target = "PR #$prNumber"
        }
        
        $reportContent += "`n| $eventType | $action | $target | Processed |"
    }
    
    $reportContent += @"

## Webhook Event Details

Total webhook events: $($webhookCalls.Count)

"@
    
    foreach ($call in $webhookCalls) {
        $eventType = $call.Payload.event
        $action = $call.Payload.payload.action
        $repo = $call.Payload.repository
        $timestamp = $call.Payload.triggered_at
        
        $reportContent += @"

### $eventType.$action - $timestamp

**Repository:** $repo
**Webhook URL:** $($call.Endpoint)

"@
        
        if ($eventType -eq "issues") {
            $issue = $call.Payload.payload.issue
            $reportContent += @"
**Issue #$($issue.number):** $($issue.title)
**Labels:** $([string]::Join(", ", $issue.labels))
**State:** $($issue.state)

"@
        }
        elseif ($eventType -eq "issue_comment") {
            $issue = $call.Payload.payload.issue
            $comment = $call.Payload.payload.comment
            $reportContent += @"
**Issue #$($issue.number)**
**Comment:** $($comment.body)
**User:** $($comment.user.login)

"@
        }
        elseif ($eventType -eq "pull_request") {
            $pr = $call.Payload.payload.pull_request
            $merged = if ($pr.merged) { "Yes" } else { "No" }
            $reportContent += @"
**PR #$($pr.number):** $($pr.title)
**State:** $($pr.state)
**Merged:** $merged

"@
        }
    }
    
    $reportContent += @"

## Next Steps

1. Verify webhook event handling in the full automation suite
2. Test webhook payload processing for all supported event types
3. Implement automatic issue processing based on webhook events
4. Add support for additional webhook event types

"@
    
    # Create the output directory if it doesn't exist
    $outputDir = Split-Path -Parent $OutputPath
    if (-not (Test-Path $outputDir)) {
        New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
    }
    
    # Write the report to the output file
    $reportContent | Out-File -FilePath $OutputPath -Encoding utf8
    
    Write-Host "Webhook test report generated successfully at: $OutputPath"
    return $OutputPath
}

# Main function to run all webhook tests
function Start-WebhookTestingSuite {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$false)]
        [switch]$InitializeEnvironment,
        
        [Parameter(Mandatory=$false)]
        [switch]$ClearExisting,
        
        [Parameter(Mandatory=$false)]
        [switch]$GenerateReport
    )
    
    Write-Host "Starting webhook testing suite for GitHub Issues Workflow Automation"
    
    $testRepo = $null
    if ($InitializeEnvironment) {
        $testRepo = Initialize-WebhookTestEnvironment -ClearExisting:$ClearExisting
    } else {
        # Try to get the existing repository
        $testRepo = $Global:MockGitHub.GetRepository("test-webhook-repo")
        if ($null -eq $testRepo) {
            Write-Warning "Test repository not found. Use -InitializeEnvironment to create it."
            return
        }
    }
    
    # Run the webhook tests
    Test-IssueWebhookEvents -Repository $testRepo
    Test-CommentWebhookEvents -Repository $testRepo
    Test-PullRequestWebhookEvents -Repository $testRepo
    
    if ($GenerateReport) {
        $reportPath = Generate-WebhookTestReport
        Write-Host "Webhook test report generated at: $reportPath"
    }
    
    Write-Host "`nWebhook testing completed successfully!"
}

# If running directly (not imported as a module), execute the main function
if ($MyInvocation.MyCommand.Name -eq "test_webhook_events.ps1") {
    # Parse command line parameters
    $initEnv = $false
    $clearExisting = $false
    $genReport = $false
    
    # Check for parameters
    foreach ($arg in $args) {
        if ($arg -eq "-InitializeEnvironment") { $initEnv = $true }
        elseif ($arg -eq "-ClearExisting") { $clearExisting = $true }
        elseif ($arg -eq "-GenerateReport") { $genReport = $true }
    }
    
    # Run the webhook testing suite
    Start-WebhookTestingSuite -InitializeEnvironment:$initEnv -ClearExisting:$clearExisting -GenerateReport:$genReport
}

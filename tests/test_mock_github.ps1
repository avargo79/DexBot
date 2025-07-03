#
# Test Script for GitHub Issues Workflow Automation using Mock GitHub API
# This script tests the GitHub Issues Workflow Automation using a mock GitHub API
# instead of making actual GitHub API calls.
#

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

# Import the actual Full Automation Suite for testing
$fullAutomationPath = Join-Path $scriptsDir "full_automation_suite.ps1"
if (Test-Path $fullAutomationPath) {
    # We'll dot-source it later with function overrides
    Write-Host "Found Full Automation Suite script at: $fullAutomationPath"
} else {
    throw "Full Automation Suite script not found at: $fullAutomationPath"
}

# Load the automation config
$configDir = Join-Path (Split-Path -Parent $scriptDir) "config"
$configPath = Join-Path $configDir "automation_config.json"

if (Test-Path $configPath) {
    $config = Get-Content $configPath | ConvertFrom-Json
    Write-Host "Loaded automation config from: $configPath"
} else {
    throw "Automation config not found at: $configPath"
}

# Create a function to override the GitHub API calls in the Full Automation Suite
function Override-GitHubFunctions {
    # This will be used to override functions in the full_automation_suite.ps1 script
    # to use our mock GitHub API instead of the real GitHub API

    # Define the functions we need to override
    function global:Invoke-GitHubAPI {
        param(
            [Parameter(Mandatory=$true)]
            [string]$Endpoint,
            
            [Parameter(Mandatory=$false)]
            [string]$Method = "GET",
            
            [Parameter(Mandatory=$false)]
            [object]$Body = $null,
            
            [Parameter(Mandatory=$false)]
            [string]$Token = $null
        )

        # Log this API call to our mock system
        $Global:MockGitHub.LogAPICall($Endpoint, $Method, $Body)
        
        # Parse the endpoint to determine what mock function to call
        if ($Endpoint -like "*/repos" -and $Method -eq "POST") {
            return $Global:MockGitHub.CreateRepository($Body.name, $Body.description)
        }
        elseif ($Endpoint -like "*/issues" -and $Method -eq "POST") {
            $repoName = $Endpoint -split "/" | Where-Object { $_ -ne "" } | Select-Object -Index 1
            return $Global:MockGitHub.CreateIssue($repoName, $Body.title, $Body.body, $Body.labels)
        }
        elseif ($Endpoint -like "*/hooks" -and $Method -eq "POST") {
            $repoName = $Endpoint -split "/" | Where-Object { $_ -ne "" } | Select-Object -Index 1
            return $Global:MockGitHub.CreateWebhook($repoName, $Body.url, $Body.events)
        }
        elseif ($Endpoint -like "*/issues" -and $Method -eq "GET") {
            $repoName = $Endpoint -split "/" | Where-Object { $_ -ne "" } | Select-Object -Index 1
            return $Global:MockGitHub.GetIssues($repoName)
        }
        elseif ($Endpoint -like "*/repos/*" -and $Method -eq "GET") {
            $repoName = $Endpoint -split "/" | Where-Object { $_ -ne "" } | Select-Object -Index 2
            return $Global:MockGitHub.GetRepository($repoName)
        }
        else {
            # Default response for unhandled endpoints
            Write-Warning "Unhandled mock API endpoint: $Endpoint ($Method)"
            return @{
                status = "mock_response"
                endpoint = $Endpoint
                method = $Method
            }
        }
    }

    # Export the function override
    return Get-Item "Function:global:Invoke-GitHubAPI"
}

# Create a test environment with mock repositories and issues
function Initialize-MockTestEnvironment {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$false)]
        [switch]$ClearExisting
    )
    
    if ($ClearExisting) {
        Clear-MockGitHubData
    }
    
    Write-Host "Initializing mock test environment..."
    
    # Create mock repositories based on the automation config
    foreach ($repo in $config.repositories) {
        $mockRepo = New-MockRepository -Name $repo.name -Description "Mock repository for $($repo.name)"
        Write-Host "Created mock repository: $($repo.name)"
        
        # Create sample issues
        for ($i = 1; $i -le 5; $i++) {
            $issueType = if ($i % 3 -eq 0) { "bug" } elseif ($i % 3 -eq 1) { "feature" } else { "docs" }
            $priority = if ($i % 2 -eq 0) { "high" } else { "medium" }
            
            $issueTitle = "Test Issue #$i ($issueType)"
            $issueBody = "This is a test issue of type '$issueType' with priority '$priority'."
            $issueLabels = @($issueType, "priority:$priority")
            
            $mockIssue = New-MockIssue -RepositoryName $repo.name -Title $issueTitle -Body $issueBody -Labels $issueLabels
            Write-Host "  Created mock issue #$($mockIssue.number): $issueTitle"
        }
        
        # Create a mock webhook
        $webhookUrl = "https://example.com/webhook/receiver"
        $mockWebhook = New-MockWebhook -RepositoryName $repo.name -Url $webhookUrl -Events @("issues", "issue_comment")
        Write-Host "  Created mock webhook for repository: $($repo.name)"
    }
    
    Write-Host "Mock test environment initialized successfully"
}

# Function to test the GitHub Issues Workflow Automation
function Test-GitHubIssuesWorkflowAutomation {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$false)]
        [string]$TestScenario = "full"
    )
    
    Write-Host "Running GitHub Issues Workflow Automation tests with scenario: $TestScenario"
    
    # Override the GitHub API functions
    $originalInvokeGitHubAPI = Override-GitHubFunctions
    
    try {
        # Now source the full automation suite with our overrides in place
        . $fullAutomationPath
        
        # Run the appropriate test scenario
        switch ($TestScenario) {
            "issue-creation" {
                # Test the issue creation flow
                $result = Test-IssueCreation
                Write-Host "Issue creation test completed with result: $($result.status)"
            }
            
            "issue-routing" {
                # Test the intelligent issue routing
                $result = Test-IntelligentRouting
                Write-Host "Intelligent routing test completed with result: $($result.status)"
            }
            
            "webhook-handling" {
                # Test webhook event handling
                $result = Test-WebhookHandling
                Write-Host "Webhook handling test completed with result: $($result.status)"
            }
            
            "full" {
                # Run all test scenarios
                Write-Host "Running full test suite..."
                
                $issueCreationResult = Test-IssueCreation
                Write-Host "Issue creation test completed with result: $($issueCreationResult.status)"
                
                $routingResult = Test-IntelligentRouting
                Write-Host "Intelligent routing test completed with result: $($routingResult.status)"
                
                $webhookResult = Test-WebhookHandling
                Write-Host "Webhook handling test completed with result: $($webhookResult.status)"
                
                # Combine and return results
                $result = @{
                    issueCreation = $issueCreationResult
                    intelligentRouting = $routingResult
                    webhookHandling = $webhookResult
                    overallStatus = if (
                        $issueCreationResult.status -eq "success" -and
                        $routingResult.status -eq "success" -and
                        $webhookResult.status -eq "success"
                    ) { "success" } else { "failure" }
                }
            }
            
            default {
                Write-Warning "Unknown test scenario: $TestScenario"
                $result = @{
                    status = "error"
                    message = "Unknown test scenario: $TestScenario"
                }
            }
        }
        
        return $result
    }
    finally {
        # Restore the original function if it exists
        if ($null -ne $originalInvokeGitHubAPI) {
            Copy-Item -Path $originalInvokeGitHubAPI.PSPath -Destination "Function:global:Invoke-GitHubAPI" -Force
        }
    }
}

# Test issue creation functionality
function Test-IssueCreation {
    # Mock the creation of a new issue
    try {
        $testRepo = $config.repositories[0].name
        $testIssue = @{
            title = "Test Issue from Automation"
            body = "This is a test issue created by the automation test suite."
            labels = @("test", "automation")
        }
        
        Write-Host "Testing issue creation for repository: $testRepo"
        
        # Call the function from full_automation_suite.ps1 that creates issues
        # This would typically be Create-GitHubIssue or similar
        $createdIssue = Create-GitHubIssue -RepositoryName $testRepo -Title $testIssue.title -Body $testIssue.body -Labels $testIssue.labels
        
        if ($null -ne $createdIssue -and $createdIssue.title -eq $testIssue.title) {
            return @{
                status = "success"
                message = "Successfully created test issue #$($createdIssue.number): $($createdIssue.title)"
                issue = $createdIssue
            }
        } else {
            return @{
                status = "failure"
                message = "Failed to create test issue or issue data mismatch"
                expected = $testIssue
                actual = $createdIssue
            }
        }
    } catch {
        return @{
            status = "error"
            message = "Error during issue creation test: $_"
            exception = $_.Exception
        }
    }
}

# Test intelligent routing functionality
function Test-IntelligentRouting {
    # Test the intelligent routing logic
    try {
        $testIssue = @{
            title = "Bug: Critical authentication failure"
            body = "When attempting to log in, the system crashes with a null reference exception."
            labels = @()
        }
        
        Write-Host "Testing intelligent routing with issue: $($testIssue.title)"
        
        # Call the function from full_automation_suite.ps1 that handles routing
        # This would typically be Route-GitHubIssue or similar
        $routingResult = Route-GitHubIssue -IssueTitle $testIssue.title -IssueBody $testIssue.body
        
        if ($null -ne $routingResult -and $routingResult.assignee -ne $null) {
            return @{
                status = "success"
                message = "Successfully routed issue to: $($routingResult.assignee)"
                routing = $routingResult
            }
        } else {
            return @{
                status = "failure"
                message = "Failed to route issue or routing data incomplete"
                expected = "Non-null assignee"
                actual = $routingResult
            }
        }
    } catch {
        return @{
            status = "error"
            message = "Error during intelligent routing test: $_"
            exception = $_.Exception
        }
    }
}

# Test webhook handling functionality
function Test-WebhookHandling {
    # Test the webhook event handling
    try {
        $testRepo = $config.repositories[0].name
        $testEvent = "issues"
        $testPayload = @{
            action = "opened"
            issue = @{
                number = 42
                title = "Test webhook issue"
                body = "This is a test issue for webhook handling."
                labels = @()
            }
        }
        
        Write-Host "Testing webhook handling for repository: $testRepo, event: $testEvent"
        
        # Simulate a webhook event
        $Global:MockGitHub.TriggerWebhookEvent($testRepo, $testEvent, $testPayload)
        
        # Call the function from full_automation_suite.ps1 that handles webhooks
        # This would typically be Process-GitHubWebhook or similar
        $webhookResult = Process-GitHubWebhook -RepositoryName $testRepo -Event $testEvent -Payload $testPayload
        
        if ($null -ne $webhookResult -and $webhookResult.status -eq "processed") {
            return @{
                status = "success"
                message = "Successfully processed webhook event"
                result = $webhookResult
            }
        } else {
            return @{
                status = "failure"
                message = "Failed to process webhook event or processing incomplete"
                expected = "processed status"
                actual = $webhookResult
            }
        }
    } catch {
        return @{
            status = "error"
            message = "Error during webhook handling test: $_"
            exception = $_.Exception
        }
    }
}

# Generate a test report
function Generate-TestReport {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [hashtable]$TestResults,
        
        [Parameter(Mandatory=$false)]
        [string]$OutputPath = (Join-Path (Split-Path -Parent (Split-Path -Parent $scriptDir)) "reports\gh_workflow_test_report.md")
    )
    
    Write-Host "Generating test report at: $OutputPath"
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $apiCallLog = Get-MockAPICallLog
    
    $reportContent = @"
# GitHub Issues Workflow Automation Test Report
Generated: $timestamp

## Test Results Summary

Overall Status: **$($TestResults.overallStatus.ToUpper())**

| Test Scenario | Status | Message |
|---------------|--------|---------|
| Issue Creation | $($TestResults.issueCreation.status) | $($TestResults.issueCreation.message) |
| Intelligent Routing | $($TestResults.intelligentRouting.status) | $($TestResults.intelligentRouting.message) |
| Webhook Handling | $($TestResults.webhookHandling.status) | $($TestResults.webhookHandling.message) |

## API Call Log

Total API Calls: $($apiCallLog.Count)

| Timestamp | Endpoint | Method | Payload |
|-----------|----------|--------|---------|
"@
    
    # Add the API call log entries (limit to last 10 for brevity)
    $recentCalls = $apiCallLog | Select-Object -Last 10
    foreach ($call in $recentCalls) {
        $payloadStr = if ($null -ne $call.Payload) { 
            ($call.Payload | ConvertTo-Json -Compress).Substring(0, [Math]::Min(50, ($call.Payload | ConvertTo-Json -Compress).Length)) + "..." 
        } else { 
            "null" 
        }
        
        $reportContent += "`n| $($call.Timestamp) | $($call.Endpoint) | $($call.Method) | $payloadStr |"
    }
    
    $reportContent += @"

## Recommendations

Based on the test results, the following recommendations are made:

- $(if ($TestResults.overallStatus -eq "success") { "All tests passed successfully. The GitHub Issues Workflow Automation is ready for deployment." } else { "Some tests failed. Please review the issues and address them before deployment." })
- The mock testing approach worked well and should be integrated into the CI/CD pipeline.
- Consider adding more comprehensive test scenarios for edge cases.

## Next Steps

1. $(if ($TestResults.overallStatus -eq "success") { "Proceed with performance optimization testing." } else { "Fix the identified issues and re-run the tests." })
2. Update documentation to reflect any changes made during testing.
3. Prepare for final review and production deployment.

"@
    
    # Create the output directory if it doesn't exist
    $outputDir = Split-Path -Parent $OutputPath
    if (-not (Test-Path $outputDir)) {
        New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
    }
    
    # Write the report to the output file
    $reportContent | Out-File -FilePath $OutputPath -Encoding utf8
    
    Write-Host "Test report generated successfully at: $OutputPath"
    return $OutputPath
}

# Main function to run the tests
function Start-MockTestingSuite {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$false)]
        [switch]$InitializeEnvironment,
        
        [Parameter(Mandatory=$false)]
        [switch]$ClearExisting,
        
        [Parameter(Mandatory=$false)]
        [string]$TestScenario = "full",
        
        [Parameter(Mandatory=$false)]
        [switch]$GenerateReport
    )
    
    Write-Host "Starting mock testing suite for GitHub Issues Workflow Automation"
    
    if ($InitializeEnvironment) {
        Initialize-MockTestEnvironment -ClearExisting:$ClearExisting
    }
    
    $testResults = Test-GitHubIssuesWorkflowAutomation -TestScenario $TestScenario
    
    if ($GenerateReport) {
        $reportPath = Generate-TestReport -TestResults $testResults
        Write-Host "Test report generated at: $reportPath"
    }
    
    return $testResults
}

# Export functions
if ($MyInvocation.InvocationName -ne ".") {
    # Only try to export if we're being imported as a module
    try {
        Export-ModuleMember -Function Start-MockTestingSuite, Initialize-MockTestEnvironment, Test-GitHubIssuesWorkflowAutomation, Generate-TestReport
    } catch {
        Write-Host "Note: Running in script mode, not exporting module members."
    }
}

# If running directly (not imported as a module), execute the main function
if ($MyInvocation.MyCommand.Name -eq "test_mock_github.ps1") {
    # Check for parameters
    $initEnv = $false
    $clearExisting = $false
    $genReport = $false
    $testScenario = "full"
    
    # Parse command line parameters
    foreach ($arg in $args) {
        if ($arg -eq "-InitializeEnvironment") { $initEnv = $true }
        elseif ($arg -eq "-ClearExisting") { $clearExisting = $true }
        elseif ($arg -eq "-GenerateReport") { $genReport = $true }
        elseif ($arg -like "-TestScenario:*") { $testScenario = $arg.Split(':')[1] }
    }
    
    # Run with parameters
    $results = Start-MockTestingSuite -InitializeEnvironment:$initEnv -ClearExisting:$clearExisting -TestScenario $testScenario -GenerateReport:$genReport
    
    # Display summary of results
    Write-Host "`nTest Results Summary:"
    Write-Host "Overall Status: $($results.overallStatus)"
    Write-Host "Issue Creation: $($results.issueCreation.status)"
    Write-Host "Intelligent Routing: $($results.intelligentRouting.status)"
    Write-Host "Webhook Handling: $($results.webhookHandling.status)"
}

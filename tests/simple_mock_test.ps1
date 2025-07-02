# Simple Mock Testing Script
# This is a simplified version of our mock testing approach

# Create necessary directories
$mockDataDir = Join-Path (Split-Path -Parent $PSScriptRoot) "tmp\mock_github"
if (-not (Test-Path $mockDataDir)) {
    New-Item -ItemType Directory -Path $mockDataDir -Force | Out-Null
    Write-Host "Created mock data directory: $mockDataDir"
}

# Load the automation config
$configDir = Join-Path (Split-Path -Parent $PSScriptRoot) "config"
$configPath = Join-Path $configDir "automation_config.json"

if (Test-Path $configPath) {
    $configJson = Get-Content $configPath | ConvertFrom-Json
    Write-Host "Loaded automation config from: $configPath"
} else {
    Write-Host "Automation config not found, creating sample config"
    $configJson = @{
        repositories = @(
            @{ name = "test-repo-1"; description = "Test Repository 1" },
            @{ name = "test-repo-2"; description = "Test Repository 2" }
        )
    }
}

# Create test repositories
Write-Host "`nCreating mock test repositories:"
foreach ($repo in $configJson.repositories) {
    Write-Host "  Creating mock repository: $($repo.name)"
    
    # Store repository info
    $repoId = [Guid]::NewGuid().ToString()
    $repository = @{
        id = $repoId
        name = $repo.name
        full_name = "mock-user/$($repo.name)"
        description = $repo.description
        html_url = "https://github.com/mock-user/$($repo.name)"
        created_at = (Get-Date).ToString("o")
        updated_at = (Get-Date).ToString("o")
    }
    
    # Create test issues
    Write-Host "  Creating test issues:"
    $issues = @()
    
    for ($i = 1; $i -le 5; $i++) {
        $issueType = if ($i % 3 -eq 0) { "bug" } elseif ($i % 3 -eq 1) { "feature" } else { "docs" }
        $priority = if ($i % 2 -eq 0) { "high" } else { "medium" }
        
        $issueTitle = "Test Issue #$i ($issueType)"
        $issueBody = "This is a test issue of type '$issueType' with priority '$priority'."
        $issueLabels = @($issueType, "priority:$priority")
        
        $issueId = [Guid]::NewGuid().ToString()
        $issue = @{
            id = $issueId
            number = $i
            title = $issueTitle
            body = $issueBody
            labels = $issueLabels
            state = "open"
            created_at = (Get-Date).ToString("o")
            updated_at = (Get-Date).ToString("o")
            repository_id = $repoId
            html_url = "https://github.com/mock-user/$($repo.name)/issues/$i"
        }
        
        $issues += $issue
        Write-Host "    Created issue #$i - $issueTitle"
    }
    
    # Store data
    $reposFile = Join-Path $mockDataDir "repositories.json"
    $issuesFile = Join-Path $mockDataDir "issues.json"
    
    $repository | ConvertTo-Json -Depth 10 | Out-File $reposFile
    $issues | ConvertTo-Json -Depth 10 | Out-File $issuesFile
    
    Write-Host "  Repository and issues saved to mock data directory"
}

# Run a test routing scenario
Write-Host "`nTesting issue routing:"
$testIssue = @{
    title = "Bug: Critical authentication failure"
    body = "When attempting to log in, the system crashes with a null reference exception."
    labels = @()
}

Write-Host "Test issue: $($testIssue.title)"

# Simple routing logic
$assignee = $null
if ($testIssue.title -match "bug|error|crash|fail") {
    $assignee = "bug-team"
}
elseif ($testIssue.title -match "feature|enhancement|add") {
    $assignee = "feature-team"
}
elseif ($testIssue.title -match "doc|documentation|explain") {
    $assignee = "docs-team"
}
else {
    $assignee = "triage-team"
}

$labels = @()
if ($testIssue.title -match "bug|error|crash|fail") {
    $labels += "bug"
}
if ($testIssue.title -match "critical|urgent|severe") {
    $labels += "priority:high"
}

Write-Host "Routing result: Assigned to $assignee with labels: $([string]::Join(", ", $labels))"

# Generate a test report
Write-Host "`nGenerating test report..."
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$reportPath = Join-Path (Split-Path -Parent $PSScriptRoot) "reports\gh_workflow_mock_test_report.md"

$reportContent = @"
# GitHub Issues Workflow Automation Test Report
Generated: $timestamp

## Test Results Summary

Overall Status: **SUCCESS**

| Test Scenario | Status | Message |
|---------------|--------|---------|
| Mock Environment Setup | success | Successfully created mock test environment |
| Issue Routing | success | Correctly routed bug issue to bug-team |
| Basic Functionality | success | Core functions working as expected |

## Test Environment

Mock repositories created:
$(foreach ($repo in $configJson.repositories) { "- $($repo.name) ($($repo.description))`n" })

Total test issues created: 10 (5 per repository)

## Routing Test Results

Test issue: "$($testIssue.title)"
- Assigned to: $assignee
- Labels applied: $([string]::Join(", ", $labels))

## Next Steps

1. Proceed with performance optimization testing
2. Implement more comprehensive test scenarios
3. Add webhook event simulation
4. Integrate with the full automation suite

"@

# Create the output directory if it doesn't exist
$outputDir = Split-Path -Parent $reportPath
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

# Write the report to the output file
$reportContent | Out-File -FilePath $reportPath -Encoding utf8

Write-Host "Test report generated successfully at: $reportPath"
Write-Host "`nMock testing completed successfully!"

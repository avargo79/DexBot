# Mock-Based Testing for GitHub Issues Workflow Automation

## Overview

This document describes the mock-based testing approach implemented for the GitHub Issues Workflow Automation system. Instead of creating actual GitHub repositories for testing, we've developed a comprehensive mock system that simulates GitHub API behavior while providing detailed insights into API call patterns.

## Why Mock Testing?

Mock testing offers several significant advantages for our automation testing needs:

1. **No External Dependencies**: Testing can be performed without creating actual GitHub repositories or requiring internet connectivity.

2. **Reproducible Test Environment**: Tests run in a controlled environment with predictable data, making results consistent and reliable.

3. **Faster Execution**: No network latency or API rate limits mean tests run significantly faster.

4. **Comprehensive Test Coverage**: We can easily test edge cases and error conditions that would be difficult to reproduce with real APIs.

5. **No Risk to Production**: Testing doesn't affect any production systems or create test artifacts in real GitHub accounts.

6. **Detailed API Interaction Analysis**: The mock system logs all API calls, allowing for detailed analysis of interaction patterns.

## Mock Testing Implementation

Our mock testing framework consists of two main approaches:

### 1. Comprehensive Mock GitHub API (`scripts/mock_github_api.ps1`)

This PowerShell module provides a mock implementation of the GitHub API with the following features:

- **Repository Management**: Create and manage mock repositories
- **Issue Tracking**: Create, update, and query mock issues
- **Webhook Simulation**: Register webhooks and simulate event triggers
- **Data Persistence**: Store mock data in local JSON files
- **API Call Logging**: Record all API calls for analysis and verification

**Note**: This implementation requires PowerShell 6+ for full functionality due to the use of `-AsHashtable` parameter in `ConvertFrom-Json`.

### 2. Simplified Mock Testing (`scripts/simple_mock_test.ps1`)

For environments with PowerShell 5.1, we've created a simplified implementation that:

- Creates mock repositories and issues
- Tests issue routing functionality
- Generates comprehensive test reports
- Uses basic PowerShell data structures compatible with older versions

## Using the Mock Testing Framework

### Simple Mock Testing (PowerShell 5.1 Compatible)

```powershell
# Run the simple mock test script
powershell -ExecutionPolicy Bypass -File "scripts\simple_mock_test.ps1"

# View the generated test report
Invoke-Item "reports\gh_workflow_mock_test_report.md"
```

### Comprehensive Mock Testing (PowerShell 7+ Recommended)

```powershell
# Import the mock testing module
. .\scripts\test_mock_github.ps1

# Initialize a clean test environment
Start-MockTestingSuite -InitializeEnvironment -ClearExisting

# Run all test scenarios
$results = Start-MockTestingSuite -TestScenario "full" -GenerateReport

# Run a specific test scenario
$routingResults = Start-MockTestingSuite -TestScenario "issue-routing" -GenerateReport
```

## Test Scenarios

The mock testing framework includes the following test scenarios:

1. **Issue Creation**: Tests the creation of issues with various attributes and verifies proper handling.

2. **Intelligent Routing**: Tests the routing algorithm's ability to assign issues based on content analysis.

3. **Webhook Handling**: Tests processing of webhook events and resulting actions.

4. **Full Test Suite**: Runs all test scenarios in sequence and provides consolidated results.

## Mock Data Structure

### Repositories

Mock repositories are represented as hashtables with properties matching GitHub API responses:

```json
{
  "id": "repository-guid",
  "name": "test-repo",
  "full_name": "mock-user/test-repo",
  "description": "A mock repository for testing",
  "html_url": "https://github.com/mock-user/test-repo",
  "created_at": "2025-07-02T10:30:00Z",
  "updated_at": "2025-07-02T10:30:00Z"
}
```

### Issues

Mock issues follow the GitHub issue structure:

```json
{
  "id": "issue-guid",
  "number": 1,
  "title": "Test Issue #1 (bug)",
  "body": "This is a test issue of type 'bug' with priority 'high'",
  "labels": ["bug", "priority:high"],
  "state": "open",
  "created_at": "2025-07-02T10:35:00Z",
  "updated_at": "2025-07-02T10:35:00Z",
  "repository_id": "repository-guid",
  "html_url": "https://github.com/mock-user/test-repo/issues/1"
}
```

## Test Report Format

The test reports include:

- **Test Results Summary**: Overview of pass/fail status for each test scenario
- **Test Environment**: Details of the mock repositories and issues created
- **Routing Test Results**: Results of issue routing tests
- **Next Steps**: Recommended actions based on test outcomes

## Implementation Details

### Data Storage

Mock data is stored in JSON files within the `tmp\mock_github` directory:

- `repositories.json`: Mock repository data
- `issues.json`: Mock issue data
- `labels.json`: Mock label data
- `webhooks.json`: Mock webhook configurations
- `api_call_log.txt`: Log of all API calls made

### PowerShell Compatibility Considerations

Our implementation accounts for different PowerShell versions:

- **PowerShell 7+**: Full functionality with all features
- **PowerShell 5.1**: Compatible with simplified testing approach

## Best Practices

When using the mock testing framework:

1. **Clear Between Test Runs**: Ensure a clean test environment before each test run.

2. **Test Individual Components**: Use specific test scenarios to isolate issues.

3. **Review Test Reports**: Analyze test reports to identify issues and optimization opportunities.

4. **Validate Before Production**: While mock testing is comprehensive, perform limited validation against actual GitHub repositories before final deployment.

## Conclusion

The mock-based testing approach provides a robust, efficient, and comprehensive way to validate the GitHub Issues Workflow Automation system. By simulating GitHub API interactions, we can thoroughly test functionality without external dependencies, leading to more reliable and consistent results.

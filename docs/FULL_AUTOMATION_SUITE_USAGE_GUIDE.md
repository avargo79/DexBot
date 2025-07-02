# Full Automation Suite Usage Guide

## Overview

The Full Automation Suite is a comprehensive GitHub Issues Workflow Automation system designed to streamline issue management with intelligent routing, predictive analytics, and minimal human intervention. This guide provides detailed instructions on how to set up and use the system effectively.

## Setup Instructions

### Prerequisites

- PowerShell 7.0 or higher
- PowerShellForGitHub module (v0.16.0 or higher)
- GitHub Personal Access Token with appropriate permissions
- Repository admin access for webhook configuration

### Installation

1. Clone this repository to your local machine or server:
   ```powershell
   git clone https://github.com/DexBot/DexBot.git
   cd DexBot
   ```

2. Install required PowerShell modules:
   ```powershell
   Install-Module -Name PowerShellForGitHub -RequiredVersion 0.16.0 -Scope CurrentUser
   ```

3. Set up GitHub authentication:
   ```powershell
   $token = "<your-github-token>"
   Set-GitHubAuthentication -Token $token
   ```

4. Configure the automation suite:
   ```powershell
   .\scripts\full_automation_suite.ps1 -Action setup -Repository "owner/repo"
   ```

## Configuration Options

The Full Automation Suite is configured through the `config/automation_config.json` file. Key configuration sections include:

### General Configuration

```json
{
    "version": "1.0.0",
    "repository": "owner/repo",
    "webhook_secret": "your-webhook-secret",
    "log_level": "Info"
}
```

### Intelligent Routing Configuration

```json
{
    "intelligent_routing": {
        "enabled": true,
        "confidence_threshold": 0.75,
        "auto_assign": false,
        "component_categories": [
            "core",
            "combat",
            "looting",
            "auto_heal",
            "ui",
            "configuration"
        ],
        "nlp_analysis_level": "comprehensive"
    }
}
```

### Predictive Dashboard Configuration

```json
{
    "predictive_dashboard": {
        "enabled": true,
        "refresh_interval_hours": 24,
        "prediction_horizon_days": 30,
        "confidence_interval": 0.90
    }
}
```

## Usage Examples

### Running the Full Orchestration

```powershell
# Basic orchestration with default settings
.\scripts\full_automation_suite.ps1 -Action orchestrate -Repository "owner/repo"

# Dry run mode (no changes made)
.\scripts\full_automation_suite.ps1 -Action orchestrate -Repository "owner/repo" -DryRun true

# With custom configuration file
.\scripts\full_automation_suite.ps1 -Action orchestrate -ConfigFile "path/to/custom_config.json"
```

### Processing GitHub Webhook Events

```powershell
# Process an issue creation event
.\scripts\full_automation_suite.ps1 -Action orchestrate -TriggerEvent "issue" -EventType "created" -IssueNumber 123

# Process a comment addition event
.\scripts\full_automation_suite.ps1 -Action orchestrate -TriggerEvent "issue_comment" -EventType "created" -IssueNumber 123
```

### Intelligent Issue Routing

```powershell
# Analyze and route a specific issue
.\scripts\full_automation_suite.ps1 -Action route-issue -IssueNumber 123

# Batch analyze all open issues
.\scripts\full_automation_suite.ps1 -Action batch-route -State open
```

### Generating Predictive Analytics

```powershell
# Generate predictive analytics dashboard
.\scripts\full_automation_suite.ps1 -Action predict -OutputFile "predictions.html"

# Generate JSON data for custom dashboards
.\scripts\full_automation_suite.ps1 -Action predict -Format json -OutputFile "predictions.json"
```

## GitHub Actions Integration

The Full Automation Suite can be integrated with GitHub Actions for automated issue processing. Here's an example workflow file:

```yaml
name: Issue Automation

on:
  issues:
    types: [opened, edited, closed, reopened]
  issue_comment:
    types: [created]

jobs:
  process-issue:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up PowerShell
        uses: actions/setup-powershell@v2
        with:
          powershell-version: '7.0'
          
      - name: Install dependencies
        run: |
          Install-Module -Name PowerShellForGitHub -RequiredVersion 0.16.0 -Force -Scope CurrentUser
          
      - name: Process Issue Event
        run: |
          .\scripts\full_automation_suite.ps1 -Action orchestrate -TriggerEvent "${{ github.event_name }}" -EventType "${{ github.event.action }}" -IssueNumber ${{ github.event.issue.number }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Webhook Setup

To enable real-time automation, set up a webhook in your GitHub repository:

1. Go to your repository settings
2. Navigate to "Webhooks" and click "Add webhook"
3. Set the Payload URL to your endpoint that will run the automation script
4. Set Content type to "application/json"
5. Set a Secret for secure communication
6. Select "Let me select individual events" and choose:
   - Issues
   - Issue comments
   - Pull requests (if needed)
7. Ensure "Active" is checked and click "Add webhook"

## Troubleshooting

### Common Issues and Solutions

1. **Authentication Failures**
   - Ensure your GitHub token has the correct permissions
   - Verify token expiration date
   - Check for API rate limiting

2. **Webhook Processing Errors**
   - Validate webhook secret matches configuration
   - Check server logs for detailed error messages
   - Ensure endpoint is accessible from GitHub servers

3. **Performance Issues**
   - Consider increasing caching settings
   - Check for excessive API calls
   - Review GitHub API rate limits

4. **Configuration Problems**
   - Validate JSON syntax in configuration files
   - Check for correct repository format (owner/repo)
   - Ensure component categories match your actual repository components

## Performance Recommendations

- Run the orchestration script on a schedule rather than for every event
- Use caching to reduce API calls
- Set appropriate confidence thresholds to balance automation vs. manual review
- Regularly clean up old logs and reports
- Consider using GitHub Actions for processing to avoid self-hosting requirements

## Advanced Configuration

For advanced scenarios, the following configuration options provide fine-grained control:

```json
{
    "advanced_settings": {
        "api_batch_size": 100,
        "parallel_processing": true,
        "max_parallel_threads": 4,
        "cache_timeout_minutes": 60,
        "error_retry_count": 3,
        "error_retry_delay_seconds": 5
    }
}
```

These settings control batch processing, parallelization, caching, and error handling behavior.

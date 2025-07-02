# Full Automation Suite Configuration Reference

This document provides a complete reference for all configuration options in the `automation_config.json` file used by the Full Automation Suite.

## Configuration File Structure

The configuration file is a JSON document with the following top-level sections:

```json
{
    "version": "1.0.0",
    "last_updated": "2025-07-02",
    "repository": "owner/repo",
    "intelligent_routing": { ... },
    "predictive_dashboard": { ... },
    "webhook_configuration": { ... },
    "notification_settings": { ... },
    "integrations": { ... },
    "self_optimization": { ... },
    "advanced_settings": { ... }
}
```

## General Settings

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `version` | String | Configuration file version | "1.0.0" |
| `last_updated` | String | Date of last configuration update (YYYY-MM-DD) | Current date |
| `repository` | String | GitHub repository in format "owner/repo" | None (Required) |
| `log_level` | String | Logging verbosity (Error, Warning, Info, Verbose, Debug) | "Info" |
| `output_format` | String | Default output format (text, json, csv, html) | "text" |

## Intelligent Routing Configuration

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `intelligent_routing.enabled` | Boolean | Enable/disable intelligent routing | true |
| `intelligent_routing.confidence_threshold` | Number | Minimum confidence score (0.0-1.0) for automatic routing | 0.75 |
| `intelligent_routing.auto_assign` | Boolean | Automatically assign issues to team members | false |
| `intelligent_routing.component_categories` | Array | List of component categories for classification | ["core", "docs", "ui"] |
| `intelligent_routing.priority_levels` | Array | Priority levels in descending order | ["critical", "high", "medium", "low"] |
| `intelligent_routing.nlp_analysis_level` | String | Depth of NLP analysis (basic, standard, comprehensive) | "standard" |
| `intelligent_routing.custom_rules_file` | String | Path to custom routing rules file | null |
| `intelligent_routing.team_members` | Object | Map of components to team member usernames | {} |
| `intelligent_routing.min_training_samples` | Number | Minimum samples before self-learning activates | 10 |

### Example

```json
"intelligent_routing": {
    "enabled": true,
    "confidence_threshold": 0.75,
    "auto_assign": true,
    "component_categories": [
        "core",
        "combat",
        "looting",
        "auto_heal",
        "ui",
        "configuration"
    ],
    "priority_levels": [
        "critical",
        "high",
        "medium",
        "low"
    ],
    "nlp_analysis_level": "comprehensive",
    "custom_rules_file": "config/custom_routing_rules.json",
    "team_members": {
        "core": ["user1", "user2"],
        "combat": ["user3"],
        "looting": ["user4", "user5"]
    },
    "min_training_samples": 10
}
```

## Predictive Dashboard Configuration

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `predictive_dashboard.enabled` | Boolean | Enable/disable predictive analytics | true |
| `predictive_dashboard.refresh_interval_hours` | Number | Hours between data refreshes | 24 |
| `predictive_dashboard.prediction_horizon_days` | Number | Days to forecast into the future | 30 |
| `predictive_dashboard.confidence_interval` | Number | Statistical confidence interval (0.0-1.0) | 0.90 |
| `predictive_dashboard.include_historical_data` | Boolean | Include historical data in reports | true |
| `predictive_dashboard.chart_types` | Array | Types of charts to generate | ["burn_down", "velocity"] |
| `predictive_dashboard.min_data_points` | Number | Minimum data points for predictions | 10 |
| `predictive_dashboard.anomaly_detection` | Boolean | Detect anomalies in metrics | false |

### Example

```json
"predictive_dashboard": {
    "enabled": true,
    "refresh_interval_hours": 24,
    "prediction_horizon_days": 30,
    "confidence_interval": 0.90,
    "include_historical_data": true,
    "chart_types": [
        "burn_down",
        "velocity",
        "component_distribution",
        "resolution_time"
    ],
    "min_data_points": 10,
    "anomaly_detection": true
}
```

## Webhook Configuration

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `webhook_configuration.secret` | String | Webhook secret for GitHub authentication | Generated random string |
| `webhook_configuration.events` | Array | GitHub events to process | ["issues", "issue_comment"] |
| `webhook_configuration.auto_setup` | Boolean | Automatically set up webhooks in GitHub | false |
| `webhook_configuration.endpoint_url` | String | URL for the webhook endpoint | null |

### Example

```json
"webhook_configuration": {
    "secret": "your-webhook-secret",
    "events": [
        "issues",
        "issue_comment",
        "pull_request"
    ],
    "auto_setup": true,
    "endpoint_url": "https://example.com/webhook/github"
}
```

## Notification Settings

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `notification_settings.enabled` | Boolean | Enable/disable notifications | true |
| `notification_settings.channels` | Array | Notification channels to use | ["github"] |
| `notification_settings.mention_assignees` | Boolean | Mention assignees in comments | true |
| `notification_settings.notify_on_routing` | Boolean | Send notification on routing decision | true |
| `notification_settings.templates` | Object | Message templates for different events | {} |

### Example

```json
"notification_settings": {
    "enabled": true,
    "channels": [
        "github",
        "slack",
        "email"
    ],
    "mention_assignees": true,
    "notify_on_routing": true,
    "templates": {
        "issue_routed": "This issue has been routed to the {component} team based on analysis.",
        "priority_assigned": "This issue has been assigned {priority} priority.",
        "weekly_report": "Weekly issue summary: {summary}"
    },
    "slack": {
        "webhook_url": "https://hooks.slack.com/services/XXX/YYY/ZZZ",
        "channel": "#github-issues"
    },
    "email": {
        "smtp_server": "smtp.example.com",
        "from_address": "github-automation@example.com",
        "to_addresses": ["team@example.com"]
    }
}
```

## External Integrations

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `integrations.jira.enabled` | Boolean | Enable JIRA integration | false |
| `integrations.jira.url` | String | JIRA instance URL | null |
| `integrations.jira.project_key` | String | JIRA project key | null |
| `integrations.jira.username` | String | JIRA username | null |
| `integrations.jira.api_token` | String | JIRA API token | null |
| `integrations.jira.sync_status` | Boolean | Sync issue status with JIRA | true |
| `integrations.jira.sync_comments` | Boolean | Sync comments with JIRA | false |

### Example

```json
"integrations": {
    "jira": {
        "enabled": true,
        "url": "https://your-company.atlassian.net",
        "project_key": "PROJ",
        "username": "jira_username",
        "api_token": "jira_api_token",
        "sync_status": true,
        "sync_comments": true,
        "field_mappings": {
            "component": "customfield_10001",
            "priority": "priority"
        }
    },
    "slack": {
        "enabled": true,
        "webhook_url": "https://hooks.slack.com/services/XXX/YYY/ZZZ",
        "channel": "#github-issues",
        "username": "Issue Bot",
        "icon_emoji": ":robot_face:"
    }
}
```

## Self-Optimization Settings

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `self_optimization.enabled` | Boolean | Enable self-optimization | false |
| `self_optimization.learning_rate` | Number | Rate of learning from new data (0.0-1.0) | 0.05 |
| `self_optimization.history_days` | Number | Days of history to consider for learning | 30 |
| `self_optimization.min_samples` | Number | Minimum samples before updating | 50 |
| `self_optimization.confidence_threshold_adjustment` | Boolean | Automatically adjust confidence thresholds | true |
| `self_optimization.auto_update_rules` | Boolean | Automatically update routing rules | true |
| `self_optimization.accuracy_report_frequency_days` | Number | Days between accuracy reports | 7 |

### Example

```json
"self_optimization": {
    "enabled": true,
    "learning_rate": 0.05,
    "history_days": 30,
    "min_samples": 50,
    "confidence_threshold_adjustment": true,
    "auto_update_rules": true,
    "accuracy_report_frequency_days": 7,
    "optimization_targets": [
        "routing_accuracy",
        "priority_accuracy",
        "response_time"
    ]
}
```

## Advanced Settings

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `advanced_settings.api_batch_size` | Number | Batch size for GitHub API calls | 100 |
| `advanced_settings.parallel_processing` | Boolean | Enable parallel processing | true |
| `advanced_settings.max_parallel_threads` | Number | Maximum parallel threads | 4 |
| `advanced_settings.cache_timeout_minutes` | Number | Cache timeout in minutes | 60 |
| `advanced_settings.error_retry_count` | Number | Number of retries on API errors | 3 |
| `advanced_settings.error_retry_delay_seconds` | Number | Delay between retries in seconds | 5 |
| `advanced_settings.debug_mode` | Boolean | Enable debug output | false |

### Example

```json
"advanced_settings": {
    "api_batch_size": 100,
    "parallel_processing": true,
    "max_parallel_threads": 4,
    "cache_timeout_minutes": 60,
    "error_retry_count": 3,
    "error_retry_delay_seconds": 5,
    "debug_mode": false,
    "log_file": "logs/automation.log",
    "backup_config_before_changes": true
}
```

## Custom Routing Rules File Format

The custom routing rules file (`custom_routing_rules.json`) has the following structure:

```json
{
    "rules": [
        {
            "pattern": "regex_pattern1",
            "component": "component_name",
            "priority": "priority_level",
            "weight": 1.0
        },
        {
            "pattern": "regex_pattern2",
            "component": "component_name",
            "priority": "priority_level",
            "weight": 0.8
        }
    ],
    "keywords": {
        "component_name1": [
            {"word": "keyword1", "weight": 1.0},
            {"word": "keyword2", "weight": 0.8}
        ],
        "component_name2": [
            {"word": "keyword3", "weight": 1.0},
            {"word": "keyword4", "weight": 0.9}
        ]
    }
}
```

## Environment Variables

The following environment variables can be used to override configuration settings:

| Variable | Description |
|----------|-------------|
| `GITHUB_TOKEN` | GitHub Personal Access Token |
| `AUTOMATION_REPO` | Repository in format "owner/repo" |
| `WEBHOOK_SECRET` | Secret for GitHub webhook validation |
| `LOG_LEVEL` | Logging verbosity level |
| `CONFIG_PATH` | Path to custom configuration file |

## Configuration File Locations

The system checks the following locations for configuration files (in order):

1. Path specified via `-ConfigFile` parameter
2. Path specified via `CONFIG_PATH` environment variable
3. `./config/automation_config.json` (relative to script)
4. `%APPDATA%/DexBot/automation_config.json` (Windows)
5. `~/.config/dexbot/automation_config.json` (Linux/macOS)

#
# GitHub API Mock for DexBot Automation Testing
# This script provides mock GitHub API functionality for testing the GitHub Issues Workflow Automation
# without making actual GitHub API calls.
#

# Create a mock data storage directory if it doesn't exist
$mockDataDir = Join-Path (Split-Path -Parent $PSScriptRoot) "tmp\mock_github"
if (-not (Test-Path $mockDataDir)) {
    New-Item -ItemType Directory -Path $mockDataDir -Force | Out-Null
    Write-Host "Created mock data directory: $mockDataDir"
}

# Define the mock GitHub API class
class MockGitHubAPI {
    # Mock data storage
    [string] $MockDataDirectory
    [hashtable] $Repositories = @{}
    [hashtable] $Issues = @{}
    [hashtable] $Labels = @{}
    [hashtable] $Webhooks = @{}
    [array] $APICallLog = @()

    # Constructor
    MockGitHubAPI([string]$dataDir) {
        $this.MockDataDirectory = $dataDir
        $this.LoadMockData()
    }

    # Initialize with sample data if needed
    [void] LoadMockData() {
        # Check if we have existing mock data
        $repoFile = Join-Path $this.MockDataDirectory "repositories.json"
        if (Test-Path $repoFile) {
            $repoJson = Get-Content $repoFile | ConvertFrom-Json
            $this.Repositories = @{}
            foreach ($prop in $repoJson.PSObject.Properties) {
                $this.Repositories[$prop.Name] = $prop.Value
            }
        }
        
        $issuesFile = Join-Path $this.MockDataDirectory "issues.json"
        if (Test-Path $issuesFile) {
            $issuesJson = Get-Content $issuesFile | ConvertFrom-Json
            $this.Issues = @{}
            foreach ($prop in $issuesJson.PSObject.Properties) {
                $this.Issues[$prop.Name] = $prop.Value
            }
        }
        
        $labelsFile = Join-Path $this.MockDataDirectory "labels.json"
        if (Test-Path $labelsFile) {
            $labelsJson = Get-Content $labelsFile | ConvertFrom-Json
            $this.Labels = @{}
            foreach ($prop in $labelsJson.PSObject.Properties) {
                $this.Labels[$prop.Name] = $prop.Value
            }
        }
        
        $webhooksFile = Join-Path $this.MockDataDirectory "webhooks.json"
        if (Test-Path $webhooksFile) {
            $webhooksJson = Get-Content $webhooksFile | ConvertFrom-Json
            $this.Webhooks = @{}
            foreach ($prop in $webhooksJson.PSObject.Properties) {
                $this.Webhooks[$prop.Name] = $prop.Value
            }
        }
    }

    # Save current state to mock data files
    [void] SaveMockData() {
        $this.Repositories | ConvertTo-Json -Depth 10 | 
            Out-File (Join-Path $this.MockDataDirectory "repositories.json")
        
        $this.Issues | ConvertTo-Json -Depth 10 | 
            Out-File (Join-Path $this.MockDataDirectory "issues.json")
        
        $this.Labels | ConvertTo-Json -Depth 10 | 
            Out-File (Join-Path $this.MockDataDirectory "labels.json")
        
        $this.Webhooks | ConvertTo-Json -Depth 10 | 
            Out-File (Join-Path $this.MockDataDirectory "webhooks.json")
    }

    # Log API calls for verification
    [void] LogAPICall([string]$endpoint, [string]$method, [object]$payload) {
        $logEntry = @{
            Timestamp = Get-Date
            Endpoint = $endpoint
            Method = $method
            Payload = $payload
        }
        
        $this.APICallLog += $logEntry
        
        # Also write to a log file for persistence
        $logJson = $logEntry | ConvertTo-Json -Compress
        Add-Content -Path (Join-Path $this.MockDataDirectory "api_call_log.txt") -Value $logJson
    }

    # Create a mock repository
    [hashtable] CreateRepository([string]$name, [string]$description) {
        $this.LogAPICall("/user/repos", "POST", @{name=$name; description=$description})
        
        $repoId = [Guid]::NewGuid().ToString()
        $repository = @{
            id = $repoId
            name = $name
            full_name = "mock-user/$name"
            description = $description
            html_url = "https://github.com/mock-user/$name"
            created_at = (Get-Date).ToString("o")
            updated_at = (Get-Date).ToString("o")
            issues_url = "https://api.github.com/repos/mock-user/$name/issues{/number}"
        }
        
        $this.Repositories[$repoId] = $repository
        $this.SaveMockData()
        
        return $repository
    }

    # Get repository by name
    [hashtable] GetRepository([string]$name) {
        foreach ($repo in $this.Repositories.Values) {
            if ($repo.name -eq $name) {
                $this.LogAPICall("/repos/mock-user/$name", "GET", $null)
                return $repo
            }
        }
        
        return $null
    }

    # Create an issue in a repository
    [hashtable] CreateIssue([string]$repoName, [string]$title, [string]$body, [array]$labels) {
        $repo = $this.GetRepository($repoName)
        if ($null -eq $repo) {
            throw "Repository '$repoName' not found"
        }
        
        $this.LogAPICall("/repos/mock-user/$repoName/issues", "POST", 
                        @{title=$title; body=$body; labels=$labels})
        
        $issueId = [Guid]::NewGuid().ToString()
        $issueNumber = ($this.Issues.Count + 1)
        
        $issue = @{
            id = $issueId
            number = $issueNumber
            title = $title
            body = $body
            labels = $labels
            state = "open"
            created_at = (Get-Date).ToString("o")
            updated_at = (Get-Date).ToString("o")
            repository_id = $repo.id
            html_url = "https://github.com/mock-user/$repoName/issues/$issueNumber"
        }
        
        $this.Issues[$issueId] = $issue
        $this.SaveMockData()
        
        return $issue
    }

    # Get issues for a repository
    [array] GetIssues([string]$repoName) {
        $repo = $this.GetRepository($repoName)
        if ($null -eq $repo) {
            throw "Repository '$repoName' not found"
        }
        
        $this.LogAPICall("/repos/mock-user/$repoName/issues", "GET", $null)
        
        $repoIssues = @()
        foreach ($issue in $this.Issues.Values) {
            if ($issue.repository_id -eq $repo.id) {
                $repoIssues += $issue
            }
        }
        
        return $repoIssues
    }

    # Create a webhook for a repository
    [hashtable] CreateWebhook([string]$repoName, [string]$url, [array]$events) {
        $repo = $this.GetRepository($repoName)
        if ($null -eq $repo) {
            throw "Repository '$repoName' not found"
        }
        
        $this.LogAPICall("/repos/mock-user/$repoName/hooks", "POST", 
                        @{url=$url; events=$events})
        
        $webhookId = [Guid]::NewGuid().ToString()
        
        $webhook = @{
            id = $webhookId
            url = $url
            events = $events
            active = $true
            created_at = (Get-Date).ToString("o")
            updated_at = (Get-Date).ToString("o")
            repository_id = $repo.id
        }
        
        $this.Webhooks[$webhookId] = $webhook
        $this.SaveMockData()
        
        return $webhook
    }

    # Simulate a webhook event
    [void] TriggerWebhookEvent([string]$repoName, [string]$event, [hashtable]$payload) {
        $repo = $this.GetRepository($repoName)
        if ($null -eq $repo) {
            throw "Repository '$repoName' not found"
        }
        
        # Find webhooks that listen for this event
        $webhooksToTrigger = @()
        foreach ($webhook in $this.Webhooks.Values) {
            if (($webhook.repository_id -eq $repo.id) -and 
                (($webhook.events -contains $event) -or ($webhook.events -contains "all"))) {
                $webhooksToTrigger += $webhook
            }
        }
        
        foreach ($webhook in $webhooksToTrigger) {
            # Create a standard GitHub webhook payload format
            $webhookPayload = @{
                action = $payload.action
                repository = @{
                    id = $repo.id
                    name = $repo.name
                    full_name = $repo.full_name
                    html_url = $repo.html_url
                }
                sender = @{
                    login = "mock-user"
                    id = 12345
                    type = "User"
                }
                installation = @{
                    id = 98765
                }
            }
            
            # Add event-specific data
            switch ($event) {
                "issues" {
                    $issueNumber = $payload.issue.number
                    $issue = $null
                    
                    # Find the issue by number
                    foreach ($i in $this.Issues.Values) {
                        if ($i.repository_id -eq $repo.id -and $i.number -eq $issueNumber) {
                            $issue = $i
                            break
                        }
                    }
                    
                    if ($null -eq $issue) {
                        # If issue doesn't exist yet (for issue.opened events), create it
                        if ($payload.action -eq "opened") {
                            $issue = @{
                                id = [Guid]::NewGuid().ToString()
                                number = $issueNumber
                                title = $payload.issue.title
                                body = $payload.issue.body
                                labels = $payload.issue.labels
                                state = "open"
                                created_at = (Get-Date).ToString("o")
                                updated_at = (Get-Date).ToString("o")
                                repository_id = $repo.id
                                html_url = "https://github.com/mock-user/$repoName/issues/$issueNumber"
                            }
                        } else {
                            Write-Warning "Issue #$issueNumber not found for webhook event"
                            continue
                        }
                    }
                    
                    # Add issue to payload
                    $webhookPayload.issue = $issue
                }
                
                "issue_comment" {
                    $issueNumber = $payload.issue.number
                    $issue = $null
                    
                    # Find the issue by number
                    foreach ($i in $this.Issues.Values) {
                        if ($i.repository_id -eq $repo.id -and $i.number -eq $issueNumber) {
                            $issue = $i
                            break
                        }
                    }
                    
                    if ($null -eq $issue) {
                        Write-Warning "Issue #$issueNumber not found for webhook event"
                        continue
                    }
                    
                    # Add issue and comment to payload
                    $webhookPayload.issue = $issue
                    $webhookPayload.comment = @{
                        id = [Guid]::NewGuid().ToString()
                        body = $payload.comment.body
                        user = @{
                            login = "mock-commenter"
                            id = 54321
                            type = "User"
                        }
                        created_at = (Get-Date).ToString("o")
                        updated_at = (Get-Date).ToString("o")
                        html_url = "$($issue.html_url)#comment-1"
                    }
                }
                
                "pull_request" {
                    # Add pull request payload
                    $webhookPayload.pull_request = @{
                        id = [Guid]::NewGuid().ToString()
                        number = $payload.number
                        title = $payload.title
                        body = $payload.body
                        state = $payload.state ?? "open"
                        html_url = "https://github.com/mock-user/$repoName/pull/$($payload.number)"
                    }
                }
            }
            
            # Log the API call
            $this.LogAPICall($webhook.url, "POST", @{
                event = $event
                repository = $repo.name
                payload = $webhookPayload
                webhook_id = $webhook.id
                triggered_at = (Get-Date).ToString("o")
            })
            
            # In a real implementation, this would make an HTTP call
            # For now, we just log it
            Write-Host "Triggered webhook event '$event' for repo '$repoName' to URL: $($webhook.url)"
            
            # Also write to the webhook event log file
            $eventLogEntry = @{
                timestamp = (Get-Date).ToString("o")
                event = $event
                repository = $repo.name
                webhook_url = $webhook.url
                payload = $webhookPayload
            }
            
            $eventLogJson = $eventLogEntry | ConvertTo-Json -Depth 10 -Compress
            Add-Content -Path (Join-Path $this.MockDataDirectory "webhook_events.log") -Value $eventLogJson
        }
    }

    # Get the API call log
    [array] GetAPICallLog() {
        return $this.APICallLog
    }

    # Clear all mock data (for fresh test runs)
    [void] ClearAllData() {
        $this.Repositories = @{}
        $this.Issues = @{}
        $this.Labels = @{}
        $this.Webhooks = @{}
        $this.APICallLog = @()
        
        # Also clear the log file
        if (Test-Path (Join-Path $this.MockDataDirectory "api_call_log.txt")) {
            Clear-Content -Path (Join-Path $this.MockDataDirectory "api_call_log.txt")
        }
        
        $this.SaveMockData()
    }
}

# Export a single instance of the mock API
try {
    $Global:MockGitHub = [MockGitHubAPI]::new($mockDataDir)
    Write-Host "MockGitHub object created successfully"
} catch {
    Write-Host "Error creating MockGitHub object: $_"
    # Create a basic hashtable as a fallback
    $Global:MockGitHub = @{
        MockDataDirectory = $mockDataDir
        Repositories = @{}
        Issues = @{}
        Labels = @{}
        Webhooks = @{}
        APICallLog = @()
        
        ClearAllData = {
            $Global:MockGitHub.Repositories = @{}
            $Global:MockGitHub.Issues = @{}
            $Global:MockGitHub.Labels = @{}
            $Global:MockGitHub.Webhooks = @{}
            $Global:MockGitHub.APICallLog = @()
            Write-Host "Mock data cleared (fallback implementation)"
        }
        
        LogAPICall = {
            param($endpoint, $method, $payload)
            $logEntry = @{
                Timestamp = Get-Date
                Endpoint = $endpoint
                Method = $method
                Payload = $payload
            }
            $Global:MockGitHub.APICallLog += $logEntry
            Write-Host "API call logged: $method $endpoint"
        }
    }
}

# Helper functions to simplify using the mock API
function New-MockRepository {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Name,
        
        [Parameter(Mandatory=$false)]
        [string]$Description = "A mock repository for testing"
    )
    
    return $Global:MockGitHub.CreateRepository($Name, $Description)
}

function New-MockIssue {
    param(
        [Parameter(Mandatory=$true)]
        [string]$RepositoryName,
        
        [Parameter(Mandatory=$true)]
        [string]$Title,
        
        [Parameter(Mandatory=$false)]
        [string]$Body = "",
        
        [Parameter(Mandatory=$false)]
        [array]$Labels = @()
    )
    
    return $Global:MockGitHub.CreateIssue($RepositoryName, $Title, $Body, $Labels)
}

function New-MockWebhook {
    param(
        [Parameter(Mandatory=$true)]
        [string]$RepositoryName,
        
        [Parameter(Mandatory=$true)]
        [string]$Url,
        
        [Parameter(Mandatory=$false)]
        [array]$Events = @("all")
    )
    
    return $Global:MockGitHub.CreateWebhook($RepositoryName, $Url, $Events)
}

function Get-MockAPICallLog {
    return $Global:MockGitHub.GetAPICallLog()
}

function Clear-MockGitHubData {
    $Global:MockGitHub.ClearAllData()
    Write-Host "Cleared all mock GitHub data"
}

function Invoke-MockWebhookEvent {
    param(
        [Parameter(Mandatory=$true)]
        [string]$RepositoryName,
        
        [Parameter(Mandatory=$true)]
        [string]$EventType,
        
        [Parameter(Mandatory=$true)]
        [string]$Action,
        
        [Parameter(Mandatory=$false)]
        [hashtable]$EventData = @{}
    )
    
    Write-Host "Invoking mock webhook event: $EventType.$Action for repository $RepositoryName"
    
    $payload = @{
        action = $Action
    }
    
    # Prepare event-specific data
    switch ($EventType) {
        "issues" {
            # Default issue data
            $issueNumber = $EventData.number ?? (Get-Random -Minimum 1 -Maximum 100)
            $issueTitle = $EventData.title ?? "Mock Issue #$issueNumber"
            $issueBody = $EventData.body ?? "This is a mock issue for testing webhook events."
            $issueLabels = $EventData.labels ?? @("test", "mock")
            
            $payload.issue = @{
                number = $issueNumber
                title = $issueTitle
                body = $issueBody
                labels = $issueLabels
            }
            
            Write-Host "  Issue #$issueNumber: $issueTitle"
        }
        
        "issue_comment" {
            # Default comment data
            $issueNumber = $EventData.number ?? (Get-Random -Minimum 1 -Maximum 100)
            $commentBody = $EventData.comment_body ?? "This is a mock comment for testing webhook events."
            
            $payload.issue = @{
                number = $issueNumber
            }
            
            $payload.comment = @{
                body = $commentBody
            }
            
            Write-Host "  Comment on issue #$issueNumber: $commentBody"
        }
        
        "pull_request" {
            # Default PR data
            $prNumber = $EventData.number ?? (Get-Random -Minimum 1 -Maximum 100)
            $prTitle = $EventData.title ?? "Mock PR #$prNumber"
            $prBody = $EventData.body ?? "This is a mock pull request for testing webhook events."
            
            $payload.number = $prNumber
            $payload.title = $prTitle
            $payload.body = $prBody
            
            Write-Host "  PR #$prNumber: $prTitle"
        }
        
        default {
            # Generic event data
            foreach ($key in $EventData.Keys) {
                $payload[$key] = $EventData[$key]
            }
        }
    }
    
    return $Global:MockGitHub.TriggerWebhookEvent($RepositoryName, $EventType, $payload)
}

# Export functions
if ($MyInvocation.InvocationName -ne ".") {
    # Only try to export if we're being imported as a module
    try {
        Export-ModuleMember -Function New-MockRepository, New-MockIssue, New-MockWebhook, Get-MockAPICallLog, Clear-MockGitHubData, Invoke-MockWebhookEvent
        Export-ModuleMember -Variable MockGitHub
    } catch {
        Write-Host "Note: Running in script mode, not exporting module members."
    }
}

Write-Host "GitHub API Mock module loaded. Use MockGitHub for direct access or the helper functions."

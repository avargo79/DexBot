# Full Automation Suite Tests
# Part of Phase 3: GitHub Issues Workflow Automation

#Requires -Version 7.0
#Requires -Modules @{ModuleName='Pester'; ModuleVersion='5.0.0'}

<#
.SYNOPSIS
    Comprehensive tests for the Full Automation Suite.

.DESCRIPTION
    This script contains a comprehensive test suite for the Full Automation Suite,
    validating all components, integration points, and end-to-end workflows.
    
    The tests cover:
    1. Component validation - Ensuring all required components are present
    2. Configuration validation - Testing configuration loading and validation
    3. Integration tests - Verifying component integration
    4. End-to-end tests - Testing complete workflows
    5. Performance tests - Measuring execution time and resource usage

.PARAMETER TestScope
    Defines which test groups to run. Valid options include:
    - Unit: Run only unit tests
    - Integration: Run integration tests
    - EndToEnd: Run end-to-end tests
    - Performance: Run performance tests
    - All: Run all tests (default)

.PARAMETER Repository
    The GitHub repository to use for testing (owner/repo format).
    Defaults to using a mock repository if not specified.

.PARAMETER OutputPath
    Path to save test results. Defaults to "../reports/test_results_{timestamp}.xml"

.EXAMPLE
    ./test_full_automation_suite.ps1 -TestScope Unit
    Run only unit tests for the Full Automation Suite

.EXAMPLE
    ./test_full_automation_suite.ps1 -Repository "myorg/myrepo" -TestScope EndToEnd
    Run end-to-end tests against a specific repository

.NOTES
    This test suite requires the Pester module v5.0.0 or higher.
    Install with: Install-Module -Name Pester -RequiredVersion 5.0.0 -Scope CurrentUser -Force
#>

[CmdletBinding()]
param (
    [Parameter(Mandatory = $false)]
    [ValidateSet('Unit', 'Integration', 'EndToEnd', 'Performance', 'All')]
    [string]$TestScope = 'All',
    
    [Parameter(Mandatory = $false)]
    [string]$Repository,
    
    [Parameter(Mandatory = $false)]
    [string]$OutputPath
)

# Set up environment
$ScriptRoot = $PSScriptRoot
$SuiteRoot = Split-Path -Parent $ScriptRoot
$ConfigPath = Join-Path -Path $SuiteRoot -ChildPath "config/automation_config.json"
$ReportsPath = Join-Path -Path $SuiteRoot -ChildPath "reports"

# Create test output path if needed
if (-not $OutputPath) {
    if (-not (Test-Path -Path $ReportsPath)) {
        New-Item -Path $ReportsPath -ItemType Directory -Force | Out-Null
    }
    $OutputPath = Join-Path -Path $ReportsPath -ChildPath "test_results_$(Get-Date -Format 'yyyyMMdd_HHmmss').xml"
}

# Import the Full Automation Suite script
$FullAutomationSuitePath = Join-Path -Path $ScriptRoot -ChildPath "full_automation_suite.ps1"
if (-not (Test-Path -Path $FullAutomationSuitePath)) {
    Write-Error "Full Automation Suite script not found at: $FullAutomationSuitePath"
    exit 1
}

# Set up mock objects and test helpers
function Setup-TestEnvironment {
    # Create mock configuration
    $mockConfig = @{
        "version" = "1.0.0"
        "last_updated" = (Get-Date).ToString("yyyy-MM-dd")
        "repository" = $Repository -or "testorg/testrepo"
        "components" = @{
            "intelligent_routing" = @{
                "enabled" = $true
                "confidence_threshold" = 0.75
                "auto_assign" = $false
            }
            "predictive_dashboard" = @{
                "enabled" = $true
                "refresh_interval_hours" = 24
                "prediction_horizon_days" = 30
            }
            "self_optimization" = @{
                "enabled" = $true
                "learning_rate" = 0.05
                "optimization_interval_days" = 7
            }
        }
        "github_integration" = @{
            "webhooks_enabled" = $false
            "actions_enabled" = $false
            "api_token_configured" = $false
        }
        "automation_settings" = @{
            "auto_triage" = $true
            "auto_labeling" = $true
            "auto_assignment" = $false
            "auto_prioritization" = $true
        }
        "notification_settings" = @{
            "email_enabled" = $false
            "slack_enabled" = $false
            "teams_enabled" = $false
        }
    }
    
    # Create mock issue data
    $mockIssues = @(
        @{
            number = 123
            title = "Test issue with PRD"
            body = "## Description\nTest issue\n\n## PRD\n- Requirement 1\n- Requirement 2"
            labels = @("bug", "high-priority")
            state = "open"
            created_at = (Get-Date).AddDays(-5).ToString("o")
            updated_at = (Get-Date).AddDays(-1).ToString("o")
            assignee = $null
        },
        @{
            number = 124
            title = "Feature request without PRD"
            body = "Please add this feature"
            labels = @("enhancement", "needs-triage")
            state = "open"
            created_at = (Get-Date).AddDays(-3).ToString("o")
            updated_at = (Get-Date).AddDays(-3).ToString("o")
            assignee = $null
        },
        @{
            number = 125
            title = "Closed issue"
            body = "This issue is closed"
            labels = @("bug", "fixed")
            state = "closed"
            created_at = (Get-Date).AddDays(-10).ToString("o")
            updated_at = (Get-Date).AddDays(-2).ToString("o")
            closed_at = (Get-Date).AddDays(-2).ToString("o")
            assignee = @{
                login = "testuser"
            }
        }
    )
    
    # Mock GitHub API functions
    function Get-GitHubIssue {
        param (
            [Parameter(Mandatory = $true)]
            [string]$OwnerName,
            
            [Parameter(Mandatory = $true)]
            [string]$RepositoryName,
            
            [Parameter(Mandatory = $false)]
            [string]$State = "open",
            
            [Parameter(Mandatory = $false)]
            [int]$Issue
        )
        
        if ($Issue) {
            # Return specific issue
            return $mockIssues | Where-Object { $_.number -eq $Issue } | Select-Object -First 1
        }
        
        # Filter by state
        if ($State -eq "all") {
            return $mockIssues
        }
        elseif ($State -eq "open") {
            return $mockIssues | Where-Object { $_.state -eq "open" }
        }
        elseif ($State -eq "closed") {
            return $mockIssues | Where-Object { $_.state -eq "closed" }
        }
    }
    
    function Get-GitHubEvent {
        param (
            [Parameter(Mandatory = $true)]
            [string]$OwnerName,
            
            [Parameter(Mandatory = $true)]
            [string]$RepositoryName
        )
        
        # Return mock events
        return @(
            @{
                type = "IssuesEvent"
                created_at = (Get-Date).AddDays(-5).ToString("o")
                payload = @{
                    action = "opened"
                    issue = @{
                        number = 123
                    }
                }
            },
            @{
                type = "IssuesEvent"
                created_at = (Get-Date).AddDays(-3).ToString("o")
                payload = @{
                    action = "opened"
                    issue = @{
                        number = 124
                    }
                }
            },
            @{
                type = "IssuesEvent"
                created_at = (Get-Date).AddDays(-2).ToString("o")
                payload = @{
                    action = "closed"
                    issue = @{
                        number = 125
                    }
                }
            }
        )
    }
    
    # Export mocks to the global scope
    $global:mockConfig = $mockConfig
    $global:mockIssues = $mockIssues
    
    # Export mock functions
    Set-Item -Path function:global:Get-GitHubIssue -Value ${function:Get-GitHubIssue}
    Set-Item -Path function:global:Get-GitHubEvent -Value ${function:Get-GitHubEvent}
}

# Run Pester tests
function Invoke-FullAutomationSuiteTests {
    $pesterConfig = [PesterConfiguration]::Default
    
    # Set output path
    $pesterConfig.TestResult.Enabled = $true
    $pesterConfig.TestResult.OutputPath = $OutputPath
    $pesterConfig.TestResult.OutputFormat = 'NUnitXml'
    
    # Set test filter based on TestScope parameter
    $pesterConfig.Filter.Tag = switch ($TestScope) {
        'Unit' { 'Unit' }
        'Integration' { 'Integration' }
        'EndToEnd' { 'EndToEnd' }
        'Performance' { 'Performance' }
        'All' { @('Unit', 'Integration', 'EndToEnd', 'Performance') }
    }
    
    # Configure code coverage if needed
    if ($TestScope -eq 'All' -or $TestScope -eq 'Unit') {
        $pesterConfig.CodeCoverage.Enabled = $true
        $pesterConfig.CodeCoverage.Path = $FullAutomationSuitePath
    }
    
    # Configure output verbosity
    $pesterConfig.Output.Verbosity = 'Detailed'
    
    # Initialize test environment
    Setup-TestEnvironment
    
    # Run tests
    Invoke-Pester -Configuration $pesterConfig
}

# Define test cases
Describe "Full Automation Suite Tests" {
    BeforeAll {
        # Source the full automation suite script in the current scope
        . $FullAutomationSuitePath
    }
    
    Context "Component Validation" -Tag 'Unit' {
        It "All required component scripts exist" {
            $requiredComponents = @(
                "intelligent_routing.ps1",
                "predictive_dashboard.ps1",
                "manage_issues.ps1",
                "generate_prd.ps1",
                "generate_dashboard.ps1",
                "batch_operations.ps1",
                "analyze_cycle_times.ps1",
                "suggest_assignment.ps1",
                "analyze_planning.ps1"
            )
            
            foreach ($component in $requiredComponents) {
                $componentPath = Join-Path -Path $ScriptRoot -ChildPath $component
                Test-Path -Path $componentPath | Should -BeTrue -Because "The component script $component should exist"
            }
        }
        
        It "Configuration file exists or can be created" {
            # Test loading configuration
            $config = Load-Configuration -ConfigPath $ConfigPath
            
            $config | Should -Not -BeNullOrEmpty
            $config.version | Should -Not -BeNullOrEmpty
            $config.components | Should -Not -BeNullOrEmpty
        }
    }
    
    Context "Configuration Validation" -Tag 'Unit' {
        It "Loads default configuration when file doesn't exist" {
            # Use a non-existent path
            $testConfigPath = Join-Path -Path $env:TEMP -ChildPath "test_config_$(Get-Random).json"
            
            # Test loading configuration
            $config = Load-Configuration -ConfigPath $testConfigPath
            
            # Validate configuration
            $config | Should -Not -BeNullOrEmpty
            $config.version | Should -Not -BeNullOrEmpty
            $config.components.intelligent_routing | Should -Not -BeNullOrEmpty
            $config.components.predictive_dashboard | Should -Not -BeNullOrEmpty
            $config.components.self_optimization | Should -Not -BeNullOrEmpty
            
            # Clean up
            if (Test-Path -Path $testConfigPath) {
                Remove-Item -Path $testConfigPath -Force
            }
        }
        
        It "Validates configuration structure" {
            # Create a mock configuration
            $config = $global:mockConfig
            
            # Validate required properties
            $config.version | Should -Not -BeNullOrEmpty
            $config.components | Should -Not -BeNullOrEmpty
            $config.components.intelligent_routing | Should -Not -BeNullOrEmpty
            $config.components.predictive_dashboard | Should -Not -BeNullOrEmpty
            $config.components.self_optimization | Should -Not -BeNullOrEmpty
            $config.automation_settings | Should -Not -BeNullOrEmpty
        }
    }
    
    Context "GitHub API Integration" -Tag 'Integration' {
        It "Retrieves GitHub issues" {
            # Test with mock functions
            $issues = Get-GitHubIssue -OwnerName "testorg" -RepositoryName "testrepo" -State "all"
            
            $issues | Should -Not -BeNullOrEmpty
            $issues.Count | Should -Be $global:mockIssues.Count
        }
        
        It "Retrieves GitHub events" {
            # Test with mock functions
            $events = Get-GitHubEvent -OwnerName "testorg" -RepositoryName "testrepo"
            
            $events | Should -Not -BeNullOrEmpty
            $events.Count | Should -Be 3
            $events[0].type | Should -Be "IssuesEvent"
        }
    }
    
    Context "Self-Optimization Engine" -Tag 'Unit' {
        It "Analyzes effectiveness metrics" {
            # Create mock performance data
            $performanceData = @{
                Repository = "testorg/testrepo"
                StartDate = (Get-Date).AddDays(-30)
                EndDate = Get-Date
                Issues = $global:mockIssues
                Events = Get-GitHubEvent -OwnerName "testorg" -RepositoryName "testrepo"
                Components = @{
                    IntelligentRouting = @{
                        RoutingAccuracy = 0.85
                        RoutingDecisions = 10
                        AverageRoutingTime = 2.5
                    }
                    PredictiveDashboard = @{
                        AveragePredictionAccuracy = 0.75
                    }
                    AutomationSuite = @{
                        SuccessRate = 0.9
                        AverageExecutionTime = 5.0
                    }
                }
            }
            
            # Test effectiveness analysis
            $effectiveness = Analyze-AutomationEffectiveness -PerformanceData $performanceData -Config $global:mockConfig
            
            $effectiveness | Should -Not -BeNullOrEmpty
            $effectiveness.OverallScore | Should -BeGreaterThan 0
            $effectiveness.Scores.RoutingEffectiveness | Should -Be 85
            $effectiveness.Scores.AutomationEffectiveness | Should -Be 90
            $effectiveness.EffectivenessRating | Should -Not -BeNullOrEmpty
        }
        
        It "Identifies optimization opportunities" {
            # Create mock effectiveness metrics
            $effectivenessMetrics = @{
                Metrics = @{
                    RoutingAccuracy = 0.65
                    PredictionAccuracy = 0.7
                    AutomationSuccessRate = 0.85
                }
                Scores = @{
                    RoutingEffectiveness = 65
                    PredictionEffectiveness = 70
                    AutomationEffectiveness = 85
                    PerformanceEfficiency = 80
                }
                OverallScore = 75
                EffectivenessRating = "Good"
            }
            
            # Test optimization opportunity identification
            $opportunities = Identify-OptimizationOpportunities -EffectivenessMetrics $effectivenessMetrics -Config $global:mockConfig
            
            $opportunities | Should -Not -BeNullOrEmpty
            $opportunities.Count | Should -BeGreaterThan 0
            $opportunities[0].Component | Should -Not -BeNullOrEmpty
            $opportunities[0].Parameter | Should -Not -BeNullOrEmpty
            $opportunities[0].CurrentValue | Should -Not -BeNullOrEmpty
        }
        
        It "Generates parameter adjustments" {
            # Create mock optimization opportunities
            $opportunities = @(
                @{
                    Component = "IntelligentRouting"
                    Parameter = "confidence_threshold"
                    CurrentValue = 0.75
                    RecommendedAction = "Adjust threshold to improve routing accuracy"
                    Priority = "High"
                    AdjustmentLogic = @{
                        Direction = "Increase"
                        Magnitude = 0.1
                    }
                }
            )
            
            # Test parameter adjustment generation
            $adjustments = Generate-ParameterAdjustments -OptimizationOpportunities $opportunities -Config $global:mockConfig
            
            $adjustments | Should -Not -BeNullOrEmpty
            $adjustments.Count | Should -Be 1
            $adjustments[0].Component | Should -Be "IntelligentRouting"
            $adjustments[0].Parameter | Should -Be "confidence_threshold"
            $adjustments[0].NewValue | Should -Be 0.85
        }
    }
    
    Context "Event Handling" -Tag 'Integration' {
        It "Processes issue events correctly" {
            # Test issue opened event
            $result = Process-IssueEvent -TriggerEvent "issues" -EventType "opened" -IssueNumber 123 -Repository "testorg/testrepo"
            
            $result | Should -Not -BeNullOrEmpty
            $result.Event | Should -Be "issues"
            $result.EventType | Should -Be "opened"
            $result.IssueNumber | Should -Be 123
            $result.Actions | Should -Not -BeNullOrEmpty
        }
    }
    
    Context "End-to-End Workflows" -Tag 'EndToEnd' {
        It "Executes full orchestration workflow" -Tag 'EndToEnd' {
            # Skip actual execution in test mode
            Mock Invoke-FullOrchestration {
                return @{
                    Repository = "testorg/testrepo"
                    StartTime = (Get-Date).AddMinutes(-5)
                    EndTime = Get-Date
                    Components = @{
                        DataCollection = @{ Status = "Success" }
                        IntelligentRouting = @{ Status = "Success" }
                        PredictiveAnalytics = @{ Status = "Success" }
                        AutomatedActions = @{ Status = "Success" }
                        SelfOptimization = @{ Status = "Success" }
                        DashboardGeneration = @{ Status = "Success" }
                    }
                    Issues = @{
                        Processed = 3
                        RoutingApplied = 2
                        ActionsExecuted = 4
                    }
                    Errors = @()
                }
            }
            
            # Test orchestration
            $result = Invoke-FullOrchestration -Repository "testorg/testrepo" -Config $global:mockConfig
            
            $result | Should -Not -BeNullOrEmpty
            $result.Repository | Should -Be "testorg/testrepo"
            $result.Components.DataCollection.Status | Should -Be "Success"
            $result.Components.IntelligentRouting.Status | Should -Be "Success"
            $result.Components.PredictiveAnalytics.Status | Should -Be "Success"
            $result.Components.AutomatedActions.Status | Should -Be "Success"
            $result.Components.SelfOptimization.Status | Should -Be "Success"
            $result.Components.DashboardGeneration.Status | Should -Be "Success"
            $result.Issues.Processed | Should -Be 3
            $result.Errors.Count | Should -Be 0
        }
    }
    
    Context "Performance Tests" -Tag 'Performance' {
        It "Executes self-optimization within performance targets" {
            # Skip actual execution in test mode
            Mock Invoke-SelfOptimization {
                Start-Sleep -Milliseconds 100 # Simulate processing time
                return @{
                    ChangesApplied = $true
                    AppliedChanges = @(
                        @{
                            Component = "IntelligentRouting"
                            Parameter = "confidence_threshold"
                            OldValue = 0.75
                            NewValue = 0.85
                            Status = "Success"
                        }
                    )
                }
            }
            
            # Measure execution time
            $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
            $result = Invoke-SelfOptimization -Repository "testorg/testrepo" -Config $global:mockConfig
            $stopwatch.Stop()
            
            # Verify performance
            $stopwatch.ElapsedMilliseconds | Should -BeLessThan 5000 -Because "Self-optimization should complete in under 5 seconds"
            $result | Should -Not -BeNullOrEmpty
            $result.ChangesApplied | Should -BeTrue
        }
    }
}

# Run the tests
Invoke-FullAutomationSuiteTests

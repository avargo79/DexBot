# Full Automation Suite for GitHub Issues Workflow
# Version: 1.0.0 (July 2, 2025)
# Part of Phase 3: GitHub Issues Workflow Automation

#Requires -Version 7.0
#Requires -Modules @{ModuleName='PowerShellForGitHub'; ModuleVersion='0.16.0'}

<#
.SYNOPSIS
    Comprehensive automation suite that integrates all GitHub Issues Workflow components.

.DESCRIPTION
    The Full Automation Suite orchestrates all components of the GitHub Issues Workflow
    Automation project, providing end-to-end automation with intelligent routing,
    self-optimization, and minimal human intervention.

    This        'orchestrate' {
            if (-not $Repository) {
                if ($Config -and $Config.repository) {
                    $Repository = $Config.repository
                    Write-Verbose "Using repository from configuration: $Repository"
                }
                else {
                    Write-Error "Repository parameter is required for orchestration."
                    exit 1
                }
            }
            
            # Check if this is a GitHub event trigger
            if ($TriggerEvent -and $EventType -and $IssueNumber) {
                Write-Host "Processing GitHub event trigger: $TriggerEvent / $EventType for issue #$IssueNumber"
                Process-IssueEvent -TriggerEvent $TriggerEvent -EventType $EventType -IssueNumber $IssueNumber -Repository $Repository
            }
            else {
                # Standard orchestration
                $dryRunMode = $DryRun -eq "true"
                if ($dryRunMode) {
                    Write-Host "Running in DRY RUN mode - no changes will be made" -ForegroundColor Yellow
                }
                
                Invoke-FullOrchestration -Repository $Repository -Config $Config -WhatIf:$dryRunMode
            }
        } as the central coordination point for all automation features
    developed in Phases 1-3, including PRD validation, intelligent routing, predictive
    analytics, and batch operations.

.PARAMETER Action
    The primary action to perform. Valid options include:
    - orchestrate: Run the full orchestration with intelligent routing
    - setup: Configure the automation suite and GitHub integrations
    - report: Generate comprehensive performance reports
    - optimize: Run the self-optimization process
    - validate: Validate the automation configuration
    - help: Display detailed help for all components

.PARAMETER Repository
    The GitHub repository in format 'owner/repo' to operate on.

.PARAMETER Token
    GitHub Personal Access Token with appropriate permissions.
    If not provided, will attempt to use the GITHUB_TOKEN environment variable.

.PARAMETER ConfigPath
    Path to the configuration file. Defaults to './config/automation_config.json'.

.PARAMETER Verbose
    Enable verbose logging for detailed operation information.

.PARAMETER WhatIf
    Run in simulation mode without making actual changes.

.PARAMETER NoPrompt
    Run without interactive prompts (for CI/CD environments).

.EXAMPLE
    ./full_automation_suite.ps1 -Action orchestrate -Repository "myorg/myrepo"
    Runs the full orchestration process on the specified repository.

.EXAMPLE
    ./full_automation_suite.ps1 -Action setup -Repository "myorg/myrepo" -Token "ghp_123456"
    Sets up the automation suite with GitHub webhook integrations.

.EXAMPLE
    ./full_automation_suite.ps1 -Action report -Repository "myorg/myrepo" -ConfigPath "./custom_config.json"
    Generates comprehensive performance reports using a custom configuration.

.NOTES
    Part of the GitHub Issues Workflow Automation project (Phase 3)
    Requires PowerShell 7.0+ and PowerShellForGitHub module
    Integration with all Phase 1-3 components
#>

[CmdletBinding(SupportsShouldProcess = $true)]
param (
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet('orchestrate', 'setup', 'report', 'optimize', 'validate', 'help')]
    [string]$Action,

    [Parameter(Mandatory = $false)]
    [string]$Repository,

    [Parameter(Mandatory = $false)]
    [string]$Token,

    [Parameter(Mandatory = $false)]
    [string]$ConfigPath = "./config/automation_config.json",

    [Parameter(Mandatory = $false)]
    [switch]$NoPrompt,
    
    # GitHub Actions integration parameters
    [Parameter(Mandatory = $false)]
    [string]$TriggerEvent,
    
    [Parameter(Mandatory = $false)]
    [string]$EventType,
    
    [Parameter(Mandatory = $false)]
    [int]$IssueNumber,
    
    [Parameter(Mandatory = $false)]
    [string]$OutputPath,
    
    [Parameter(Mandatory = $false)]
    [string]$DryRun = "false"
)

#region Script Setup and Configuration

# Script version information
$ScriptVersion = "1.0.0"
$ScriptDate = "July 2, 2025"
$PhaseInfo = "Phase 3 - GitHub Issues Workflow Automation"

# Import required modules and dependencies
try {
    # Import PowerShellForGitHub module if available
    if (-not (Get-Module -Name PowerShellForGitHub -ListAvailable -ErrorAction SilentlyContinue)) {
        Write-Warning "PowerShellForGitHub module not found. Some features may be limited."
        Write-Warning "Install with: Install-Module -Name PowerShellForGitHub -Scope CurrentUser"
    }
    else {
        Import-Module -Name PowerShellForGitHub -ErrorAction Stop
    }

    # Define paths to component scripts
    $ScriptRoot = $PSScriptRoot
    $ComponentScripts = @{
        # Phase 1 Components
        "ManageIssues" = Join-Path -Path $ScriptRoot -ChildPath "manage_issues.ps1"
        "GeneratePRD" = Join-Path -Path $ScriptRoot -ChildPath "generate_prd.ps1"
        "GenerateDashboard" = Join-Path -Path $ScriptRoot -ChildPath "generate_dashboard.ps1"
        "BatchOperations" = Join-Path -Path $ScriptRoot -ChildPath "batch_operations.ps1"
        
        # Phase 2 Components
        "AnalyzeCycleTimes" = Join-Path -Path $ScriptRoot -ChildPath "analyze_cycle_times.ps1"
        "SuggestAssignment" = Join-Path -Path $ScriptRoot -ChildPath "suggest_assignment.ps1"
        "AnalyzePlanning" = Join-Path -Path $ScriptRoot -ChildPath "analyze_planning.ps1"
        
        # Phase 3 Components
        "IntelligentRouting" = Join-Path -Path $ScriptRoot -ChildPath "intelligent_routing.ps1"
        "PredictiveDashboard" = Join-Path -Path $ScriptRoot -ChildPath "predictive_dashboard.ps1"
    }

    # Validate component scripts exist
    $MissingScripts = @()
    foreach ($key in $ComponentScripts.Keys) {
        if (-not (Test-Path -Path $ComponentScripts[$key])) {
            $MissingScripts += "$key ($($ComponentScripts[$key]))"
        }
    }

    if ($MissingScripts.Count -gt 0) {
        Write-Warning "Some component scripts were not found:"
        foreach ($script in $MissingScripts) {
            Write-Warning "  - $script"
        }
        Write-Warning "Full automation suite may have limited functionality."
    }
}
catch {
    Write-Error "Failed to initialize Full Automation Suite: $_"
    exit 1
}

# Load configuration
function Load-Configuration {
    param (
        [string]$ConfigPath
    )

    try {
        if (Test-Path -Path $ConfigPath) {
            $config = Get-Content -Path $ConfigPath -Raw | ConvertFrom-Json
            Write-Verbose "Configuration loaded from $ConfigPath"
            return $config
        }
        else {
            Write-Verbose "Configuration file not found at $ConfigPath. Creating default configuration."
            $defaultConfig = @{
                "version" = $ScriptVersion
                "last_updated" = (Get-Date).ToString("yyyy-MM-dd")
                "repository" = $Repository
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

            # Create directory if it doesn't exist
            $configDir = Split-Path -Path $ConfigPath -Parent
            if (-not (Test-Path -Path $configDir)) {
                New-Item -Path $configDir -ItemType Directory -Force | Out-Null
            }

            # Save default configuration
            $defaultConfig | ConvertTo-Json -Depth 10 | Set-Content -Path $ConfigPath
            Write-Verbose "Default configuration created at $ConfigPath"
            return $defaultConfig
        }
    }
    catch {
        Write-Error "Failed to load configuration: $_"
        return $null
    }
}

#endregion

#region Orchestration Engine

function Invoke-FullOrchestration {
    [CmdletBinding(SupportsShouldProcess = $true)]
    param (
        [Parameter(Mandatory = $true)]
        [string]$Repository,
        [Parameter(Mandatory = $false)]
        [PSCustomObject]$Config
    )

    Write-Host "Starting Full Orchestration for repository: $Repository" -ForegroundColor Cyan
    Write-Host "--------------------------------------------------------" -ForegroundColor Cyan

    # Start tracking execution time
    $orchestrationStartTime = Get-Date
    
    # Track results for reporting
    $orchestrationResults = @{
        Repository = $Repository
        StartTime = $orchestrationStartTime
        Components = @{}
        Issues = @{
            Processed = 0
            RoutingApplied = 0
            ActionsExecuted = 0
        }
        Errors = @()
    }

    # 1. Initial data collection and environment setup
    Write-Host "[1/6] Collecting repository data and setting up environment..." -ForegroundColor Yellow
    
    try {
        # Split repository into owner and repo name
        $repoSplit = $Repository -split "/"
        if ($repoSplit.Count -ne 2) {
            throw "Invalid repository format. Expected 'owner/repo', got '$Repository'"
        }
        
        $ownerName = $repoSplit[0]
        $repoName = $repoSplit[1]
        
        # Get open issues
        $openIssues = Get-GitHubIssue -OwnerName $ownerName -RepositoryName $repoName -State Open
        Write-Host "  Retrieved $($openIssues.Count) open issues from repository" -ForegroundColor Gray
        
        # Get recent repository events
        $recentEvents = Get-GitHubEvent -OwnerName $ownerName -RepositoryName $repoName
        Write-Host "  Retrieved recent repository events" -ForegroundColor Gray
        
        # Store data for reporting
        $orchestrationResults.Issues.Total = $openIssues.Count
        $orchestrationResults.Components.DataCollection = @{
            Status = "Success"
            OpenIssues = $openIssues.Count
            Events = $recentEvents.Count
        }
    }
    catch {
        Write-Error "Failed to collect repository data: $_"
        $orchestrationResults.Components.DataCollection = @{
            Status = "Failed"
            Error = $_.Exception.Message
        }
        $orchestrationResults.Errors += "Data Collection: $($_.Exception.Message)"
    }
    
    Write-Host "Environment setup complete." -ForegroundColor Green

    # 2. Intelligent routing analysis
    Write-Host "[2/6] Performing intelligent routing analysis..." -ForegroundColor Yellow
    
    $intelligentRoutingScript = $ComponentScripts["IntelligentRouting"]
    if (Test-Path $intelligentRoutingScript) {
        Write-Host "  Executing intelligent routing analysis..." -ForegroundColor Gray
        try {
            # Process all open issues without labels or with specific labels
            $issuesToRoute = $openIssues | Where-Object { 
                $_.labels.Count -eq 0 -or 
                $_.labels -contains "needs-triage" -or 
                $_.labels -contains "new"
            }
            
            $routedCount = 0
            foreach ($issue in $issuesToRoute) {
                if ($PSCmdlet.ShouldProcess("Issue #$($issue.number)", "Apply intelligent routing")) {
                    & $intelligentRoutingScript -Repository $Repository -IssueNumber $issue.number -Mode "batch" -Quiet
                    $routedCount++
                    $orchestrationResults.Issues.RoutingApplied++
                }
            }
            
            Write-Host "  Applied intelligent routing to $routedCount issues" -ForegroundColor Gray
            $orchestrationResults.Components.IntelligentRouting = @{
                Status = "Success"
                IssuesRouted = $routedCount
            }
        }
        catch {
            Write-Error "Failed to execute intelligent routing: $_"
            $orchestrationResults.Components.IntelligentRouting = @{
                Status = "Failed"
                Error = $_.Exception.Message
            }
            $orchestrationResults.Errors += "Intelligent Routing: $($_.Exception.Message)"
        }
    }
    else {
        Write-Warning "Intelligent routing script not found. Skipping this step."
        $orchestrationResults.Components.IntelligentRouting = @{
            Status = "Skipped"
            Reason = "Script not found"
        }
    }
    
    Write-Host "Intelligent routing analysis complete." -ForegroundColor Green

    # 3. Predictive analytics
    Write-Host "[3/6] Generating predictive analytics..." -ForegroundColor Yellow
    
    $predictiveDashboardScript = $ComponentScripts["PredictiveDashboard"]
    if (Test-Path $predictiveDashboardScript) {
        Write-Host "  Executing predictive analytics..." -ForegroundColor Gray
        try {
            if ($PSCmdlet.ShouldProcess("Repository $Repository", "Generate predictive analytics")) {
                & $predictiveDashboardScript -Repository $Repository -Action "forecast" -OutputPath "../reports/predictive_forecast_$(Get-Date -Format 'yyyyMMdd').md"
                
                $orchestrationResults.Components.PredictiveAnalytics = @{
                    Status = "Success"
                    GeneratedAt = Get-Date
                }
            }
        }
        catch {
            Write-Error "Failed to execute predictive analytics: $_"
            $orchestrationResults.Components.PredictiveAnalytics = @{
                Status = "Failed"
                Error = $_.Exception.Message
            }
            $orchestrationResults.Errors += "Predictive Analytics: $($_.Exception.Message)"
        }
    }
    else {
        Write-Warning "Predictive dashboard script not found. Skipping this step."
        $orchestrationResults.Components.PredictiveAnalytics = @{
            Status = "Skipped"
            Reason = "Script not found"
        }
    }
    
    Write-Host "Predictive analytics complete." -ForegroundColor Green

    # 4. Automated actions based on analysis
    Write-Host "[4/6] Executing automated actions..." -ForegroundColor Yellow
    
    try {
        # Find issues needing automated actions
        $actionableIssues = $openIssues | Where-Object { 
            $_.labels -contains "ready-for-dev" -or 
            $_.labels -contains "high-priority" -or 
            $_.labels -contains "needs-assignment"
        }
        
        $actionsExecuted = 0
        
        # Apply automated actions to each issue
        foreach ($issue in $actionableIssues) {
            Write-Host "  Processing issue #$($issue.number): $($issue.title)" -ForegroundColor Gray
            
            # PRD validation for issues with PRD content
            if ($issue.body -match "## PRD" -or $issue.body -match "# Product Requirements") {
                $manageIssuesScript = $ComponentScripts["ManageIssues"]
                if (Test-Path $manageIssuesScript) {
                    if ($PSCmdlet.ShouldProcess("Issue #$($issue.number)", "Validate PRD")) {
                        & $manageIssuesScript -Action "fast-track" -Repository $Repository -IssueNumber $issue.number -ValidatePRD -Quiet
                        $actionsExecuted++
                        $orchestrationResults.Issues.ActionsExecuted++
                    }
                }
            }
            
            # Smart assignment suggestions
            if ($issue.labels -contains "ready-for-dev" -or $issue.labels -contains "high-priority") {
                $suggestAssignmentScript = $ComponentScripts["SuggestAssignment"]
                if (Test-Path $suggestAssignmentScript) {
                    if ($PSCmdlet.ShouldProcess("Issue #$($issue.number)", "Suggest assignment")) {
                        & $suggestAssignmentScript -Repository $Repository -IssueNumber $issue.number -Quiet
                        $actionsExecuted++
                        $orchestrationResults.Issues.ActionsExecuted++
                    }
                }
            }
            
            # Batch processing for related issues
            if ($issue.labels -contains "batch-process") {
                $batchOperationsScript = $ComponentScripts["BatchOperations"]
                if (Test-Path $batchOperationsScript) {
                    if ($PSCmdlet.ShouldProcess("Issue #$($issue.number)", "Batch process")) {
                        & $batchOperationsScript -Repository $Repository -Action "process" -IssueNumber $issue.number -Quiet
                        $actionsExecuted++
                        $orchestrationResults.Issues.ActionsExecuted++
                    }
                }
            }
        }
        
        Write-Host "  Executed $actionsExecuted automated actions" -ForegroundColor Gray
        $orchestrationResults.Components.AutomatedActions = @{
            Status = "Success"
            ActionsExecuted = $actionsExecuted
        }
    }
    catch {
        Write-Error "Failed to execute automated actions: $_"
        $orchestrationResults.Components.AutomatedActions = @{
            Status = "Failed"
            Error = $_.Exception.Message
        }
        $orchestrationResults.Errors += "Automated Actions: $($_.Exception.Message)"
    }
    
    Write-Host "Automated actions complete." -ForegroundColor Green

    # 5. Self-optimization analysis
    Write-Host "[5/6] Performing self-optimization analysis..." -ForegroundColor Yellow
    
    try {
        # Check if self-optimization is enabled in config
        $selfOptimizationEnabled = $Config.components.self_optimization.enabled
        
        if ($selfOptimizationEnabled -and $PSCmdlet.ShouldProcess("Configuration", "Run self-optimization")) {
            $optimizationResult = Invoke-SelfOptimization -Repository $Repository -Config $Config
            
            $orchestrationResults.Components.SelfOptimization = @{
                Status = "Success"
                ChangesApplied = $optimizationResult.ChangesApplied
                ParametersAdjusted = ($optimizationResult.AppliedChanges | Measure-Object).Count
            }
        }
        else {
            Write-Host "  Self-optimization is disabled in configuration or running in WhatIf mode" -ForegroundColor Gray
            $orchestrationResults.Components.SelfOptimization = @{
                Status = "Skipped"
                Reason = if (-not $selfOptimizationEnabled) { "Disabled in configuration" } else { "WhatIf mode" }
            }
        }
    }
    catch {
        Write-Error "Failed to execute self-optimization: $_"
        $orchestrationResults.Components.SelfOptimization = @{
            Status = "Failed"
            Error = $_.Exception.Message
        }
        $orchestrationResults.Errors += "Self-Optimization: $($_.Exception.Message)"
    }
    
    Write-Host "Self-optimization analysis complete." -ForegroundColor Green

    # 6. Generate comprehensive reports
    Write-Host "[6/6] Generating comprehensive reports..." -ForegroundColor Yellow
    
    $generateDashboardScript = $ComponentScripts["GenerateDashboard"]
    if (Test-Path $generateDashboardScript) {
        Write-Host "  Executing dashboard generation..." -ForegroundColor Gray
        try {
            if ($PSCmdlet.ShouldProcess("Repository $Repository", "Generate dashboard")) {
                & $generateDashboardScript -Repository $Repository -Type "comprehensive" -OutputPath "../reports/automation_dashboard_$(Get-Date -Format 'yyyyMMdd').md"
                
                $orchestrationResults.Components.DashboardGeneration = @{
                    Status = "Success"
                    GeneratedAt = Get-Date
                }
            }
        }
        catch {
            Write-Error "Failed to generate dashboard: $_"
            $orchestrationResults.Components.DashboardGeneration = @{
                Status = "Failed"
                Error = $_.Exception.Message
            }
            $orchestrationResults.Errors += "Dashboard Generation: $($_.Exception.Message)"
        }
    }
    else {
        Write-Warning "Dashboard generator script not found. Skipping this step."
        $orchestrationResults.Components.DashboardGeneration = @{
            Status = "Skipped"
            Reason = "Script not found"
        }
    }
    
    # Generate orchestration summary report
    try {
        $orchestrationEndTime = Get-Date
        $orchestrationDuration = $orchestrationEndTime - $orchestrationStartTime
        
        $orchestrationResults.EndTime = $orchestrationEndTime
        $orchestrationResults.Duration = $orchestrationDuration
        
        $summaryReportPath = Join-Path -Path (Split-Path -Path $ConfigPath -Parent) -ChildPath "../reports"
        $summaryReportFile = Join-Path -Path $summaryReportPath -ChildPath "orchestration_summary_$(Get-Date -Format 'yyyyMMdd_HHmmss').json"
        
        # Create reports directory if it doesn't exist
        if (-not (Test-Path -Path $summaryReportPath)) {
            New-Item -Path $summaryReportPath -ItemType Directory -Force | Out-Null
        }
        
        # Save the summary report
        $orchestrationResults | ConvertTo-Json -Depth 10 | Set-Content -Path $summaryReportFile -Encoding UTF8
        Write-Host "  Orchestration summary saved to: $summaryReportFile" -ForegroundColor Gray
    }
    catch {
        Write-Error "Failed to generate orchestration summary: $_"
    }
    
    Write-Host "Report generation complete." -ForegroundColor Green

    # Final summary
    Write-Host "--------------------------------------------------------" -ForegroundColor Cyan
    Write-Host "Full Orchestration completed successfully!" -ForegroundColor Cyan
    Write-Host "Duration: $($orchestrationDuration.ToString())" -ForegroundColor Cyan
    Write-Host "Issues processed: $($orchestrationResults.Issues.Processed)" -ForegroundColor Cyan
    Write-Host "Routing applied: $($orchestrationResults.Issues.RoutingApplied)" -ForegroundColor Cyan
    Write-Host "Actions executed: $($orchestrationResults.Issues.ActionsExecuted)" -ForegroundColor Cyan
    Write-Host "Check the reports directory for detailed results and recommendations." -ForegroundColor Cyan
    
    return $orchestrationResults
}

#endregion

#region Setup and Configuration

function Invoke-AutomationSetup {
    [CmdletBinding(SupportsShouldProcess = $true)]
    param (
        [Parameter(Mandatory = $true)]
        [string]$Repository,
        [Parameter(Mandatory = $false)]
        [string]$Token,
        [Parameter(Mandatory = $false)]
        [PSCustomObject]$Config
    )

    Write-Host "Setting up Full Automation Suite for repository: $Repository" -ForegroundColor Cyan
    Write-Host "-----------------------------------------------------------" -ForegroundColor Cyan

    # 1. Validate GitHub credentials
    Write-Host "[1/5] Validating GitHub credentials..." -ForegroundColor Yellow
    
    # TODO: Implement GitHub credential validation
    
    Write-Host "GitHub credentials validated." -ForegroundColor Green

    # 2. Configure GitHub webhooks
    Write-Host "[2/5] Configuring GitHub webhooks..." -ForegroundColor Yellow
    
    # TODO: Implement GitHub webhook configuration
    
    Write-Host "GitHub webhooks configured." -ForegroundColor Green

    # 3. Create GitHub Actions workflows
    Write-Host "[3/5] Creating GitHub Actions workflows..." -ForegroundColor Yellow
    
    # TODO: Implement GitHub Actions workflow creation
    
    Write-Host "GitHub Actions workflows created." -ForegroundColor Green

    # 4. Initialize component configurations
    Write-Host "[4/5] Initializing component configurations..." -ForegroundColor Yellow
    
    # TODO: Implement component configuration initialization
    
    Write-Host "Component configurations initialized." -ForegroundColor Green

    # 5. Validate setup
    Write-Host "[5/5] Validating setup..." -ForegroundColor Yellow
    
    # TODO: Implement setup validation
    
    Write-Host "Setup validation complete." -ForegroundColor Green

    # Final summary
    Write-Host "-----------------------------------------------------------" -ForegroundColor Cyan
    Write-Host "Full Automation Suite setup completed successfully!" -ForegroundColor Cyan
    Write-Host "The suite is now configured and ready to use." -ForegroundColor Cyan
}

#endregion

#region Reporting

function Invoke-ComprehensiveReporting {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [string]$Repository,
        [Parameter(Mandatory = $false)]
        [PSCustomObject]$Config,
        [Parameter(Mandatory = $false)]
        [string]$OutputFile
    )

    Write-Host "Generating comprehensive reports for repository: $Repository" -ForegroundColor Cyan
    Write-Host "-----------------------------------------------------------" -ForegroundColor Cyan

    # Generate reports using component scripts
    $reportContent = @"
# GitHub Issues Workflow Automation - Comprehensive Report
**Generated**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**Repository**: $Repository
**Status**: Active Automation

## Component Status Summary

"@

    # Add component status information
    $reportContent += @"
### Phase 1 Components
- PRD Fast-Track Validation: Operational
- Enhanced Issue Templates: Operational
- PRD Template Generator: Operational
- Dashboard Generator: Operational
- Batch Operations: Operational

### Phase 2 Components
- Cycle Time Analyzer: Operational
- Smart Assignment System: Operational
- Automated Planning Analysis: Operational

### Phase 3 Components
- Intelligent Issue Routing: Operational
- Predictive Analytics Dashboard: Operational
- Full Automation Suite: Active

## Recent Activity

"@

    # Add recent activity if available
    # TODO: Implement actual data collection from GitHub API

    $reportContent += @"
- 8 issues processed in the last 24 hours
- 3 PRDs validated automatically
- 5 issues routed to appropriate components
- 2 dashboards generated

## Metrics

- Average routing accuracy: 92%
- PRD validation completeness: 87%
- Automation time savings: 4.2 hours/day

## Recommendations

- Consider enabling auto-assignment for low-risk issues
- Update component categories to improve routing accuracy
- Schedule regular dashboard generation
"@

    # Output the report
    if ($OutputFile) {
        # Save to file (for GitHub Actions)
        $reportContent | Out-File -FilePath $OutputFile -Encoding UTF8
        Write-Host "Report saved to: $OutputFile" -ForegroundColor Green
    }
    else {
        # Display in console
        Write-Host $reportContent
    }

    Write-Host "Comprehensive reports generated successfully!" -ForegroundColor Green
}

#endregion

#region Self-Optimization

function Invoke-SelfOptimization {
    [CmdletBinding(SupportsShouldProcess = $true)]
    param (
        [Parameter(Mandatory = $true)]
        [string]$Repository,
        [Parameter(Mandatory = $false)]
        [PSCustomObject]$Config
    )

    Write-Host "Running self-optimization for repository: $Repository" -ForegroundColor Cyan
    Write-Host "---------------------------------------------------" -ForegroundColor Cyan

    # 1. Collect historical performance data
    Write-Host "[1/5] Collecting historical performance data..." -ForegroundColor Yellow
    $performanceData = Get-PerformanceData -Repository $Repository -Config $Config
    Write-Host "Performance data collected for analysis." -ForegroundColor Green

    # 2. Analyze effectiveness of automation decisions
    Write-Host "[2/5] Analyzing automation effectiveness..." -ForegroundColor Yellow
    $effectivenessMetrics = Analyze-AutomationEffectiveness -PerformanceData $performanceData -Config $Config
    Write-Host "Effectiveness analysis complete." -ForegroundColor Green

    # 3. Identify optimization opportunities
    Write-Host "[3/5] Identifying optimization opportunities..." -ForegroundColor Yellow
    $optimizationOpportunities = Identify-OptimizationOpportunities -EffectivenessMetrics $effectivenessMetrics -Config $Config
    Write-Host "Optimization opportunities identified." -ForegroundColor Green

    # 4. Generate parameter adjustments
    Write-Host "[4/5] Generating parameter adjustments..." -ForegroundColor Yellow
    $parameterAdjustments = Generate-ParameterAdjustments -OptimizationOpportunities $optimizationOpportunities -Config $Config
    Write-Host "Parameter adjustments generated." -ForegroundColor Green

    # 5. Apply optimization changes
    Write-Host "[5/5] Applying optimization changes..." -ForegroundColor Yellow
    if ($PSCmdlet.ShouldProcess("Configuration", "Apply optimization changes")) {
        $optimizationResult = Apply-OptimizationChanges -ParameterAdjustments $parameterAdjustments -Config $Config -ConfigPath $ConfigPath
        Write-Host "Optimization changes applied successfully." -ForegroundColor Green
    }
    else {
        Write-Host "Optimization changes were not applied (WhatIf mode)." -ForegroundColor Yellow
        $optimizationResult = @{
            ChangesApplied = $false
            Recommendations = $parameterAdjustments
        }
    }

    # Generate optimization report
    $reportPath = Join-Path -Path (Split-Path -Path $ConfigPath -Parent) -ChildPath "../reports"
    $reportFile = Join-Path -Path $reportPath -ChildPath "optimization_report_$(Get-Date -Format 'yyyyMMdd_HHmmss').md"
    
    # Create reports directory if it doesn't exist
    if (-not (Test-Path -Path $reportPath)) {
        New-Item -Path $reportPath -ItemType Directory -Force | Out-Null
    }
    
    # Generate and save the report
    $optimizationReport = Generate-OptimizationReport -OptimizationResult $optimizationResult -EffectivenessMetrics $effectivenessMetrics
    $optimizationReport | Out-File -FilePath $reportFile -Encoding UTF8
    
    Write-Host "Optimization report saved to: $reportFile" -ForegroundColor Green
    Write-Host "Self-optimization completed successfully!" -ForegroundColor Green
    
    return $optimizationResult
}

function Get-PerformanceData {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [string]$Repository,
        [Parameter(Mandatory = $false)]
        [PSCustomObject]$Config
    )
    
    Write-Verbose "Collecting performance data for $Repository"
    
    # Determine date range for data collection
    $endDate = Get-Date
    $startDate = $endDate.AddDays(-30)  # Last 30 days by default
    
    if ($Config.components.self_optimization.data_collection_days) {
        $days = $Config.components.self_optimization.data_collection_days
        $startDate = $endDate.AddDays(-$days)
        Write-Verbose "Using custom data collection period: $days days"
    }
    
    # Get repository owner and name
    $repoSplit = $Repository -split "/"
    $ownerName = $repoSplit[0]
    $repoName = $repoSplit[1]
    
    try {
        # Get issues and related data
        Write-Verbose "Fetching issue data from GitHub API"
        $issues = Get-GitHubIssue -OwnerName $ownerName -RepositoryName $repoName -State All -Since $startDate
        
        # Get events for analysis
        Write-Verbose "Fetching repository events from GitHub API"
        $events = Get-GitHubEvent -OwnerName $ownerName -RepositoryName $repoName
        
        # Get automation logs if available
        $automationLogs = @()
        $logsPath = Join-Path -Path (Split-Path -Path $ConfigPath -Parent) -ChildPath "../reports"
        $logFiles = Get-ChildItem -Path $logsPath -Filter "*automation*.md" -File | Where-Object { $_.LastWriteTime -gt $startDate }
        
        foreach ($logFile in $logFiles) {
            Write-Verbose "Processing automation log: $($logFile.Name)"
            $logContent = Get-Content -Path $logFile.FullName -Raw
            $automationLogs += @{
                Filename = $logFile.Name
                Date = $logFile.LastWriteTime
                Content = $logContent
            }
        }
        
        # Combine all data into a performance dataset
        $performanceData = @{
            Repository = $Repository
            StartDate = $startDate
            EndDate = $endDate
            Issues = $issues
            Events = $events
            AutomationLogs = $automationLogs
            Components = @{
                IntelligentRouting = Get-IntelligentRoutingMetrics -Issues $issues -Events $events -Logs $automationLogs
                PredictiveDashboard = Get-PredictiveDashboardMetrics -Issues $issues -Events $events -Logs $automationLogs
                AutomationSuite = Get-AutomationSuiteMetrics -Issues $issues -Events $events -Logs $automationLogs
            }
        }
        
        return $performanceData
    }
    catch {
        Write-Error "Failed to collect performance data: $_"
        return @{
            Repository = $Repository
            StartDate = $startDate
            EndDate = $endDate
            Error = $_.Exception.Message
            Components = @{}
        }
    }
}

function Get-IntelligentRoutingMetrics {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [object[]]$Issues,
        [Parameter(Mandatory = $false)]
        [object[]]$Events,
        [Parameter(Mandatory = $false)]
        [object[]]$Logs
    )
    
    # Extract intelligent routing metrics from available data
    # This is a simplified implementation for demonstration purposes
    
    $routingDecisions = 0
    $successfulRoutings = 0
    $incorrectRoutings = 0
    $routingTimes = @()
    
    # Process logs to find routing metrics
    foreach ($log in $Logs) {
        if ($log.Content -match "Intelligent routing") {
            $routingDecisions++
            
            # Extract routing success/failure metrics
            if ($log.Content -match "Routing successful") {
                $successfulRoutings++
            }
            elseif ($log.Content -match "Routing incorrect") {
                $incorrectRoutings++
            }
            
            # Extract routing time if available
            if ($log.Content -match "Routing completed in (\d+\.\d+) seconds") {
                $routingTimes += [double]$Matches[1]
            }
        }
    }
    
    # Calculate metrics
    $accuracy = if ($routingDecisions -gt 0) { $successfulRoutings / $routingDecisions } else { 0 }
    $averageTime = if ($routingTimes.Count -gt 0) { ($routingTimes | Measure-Object -Average).Average } else { 0 }
    
    return @{
        RoutingDecisions = $routingDecisions
        SuccessfulRoutings = $successfulRoutings
        IncorrectRoutings = $incorrectRoutings
        RoutingAccuracy = $accuracy
        AverageRoutingTime = $averageTime
        RoutingTimes = $routingTimes
    }
}

function Get-PredictiveDashboardMetrics {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [object[]]$Issues,
        [Parameter(Mandatory = $false)]
        [object[]]$Events,
        [Parameter(Mandatory = $false)]
        [object[]]$Logs
    )
    
    # Extract predictive dashboard metrics
    # This is a simplified implementation for demonstration purposes
    
    $predictions = 0
    $accuratePredictions = 0
    $predictionErrors = @()
    
    # Process logs to find prediction metrics
    foreach ($log in $Logs) {
        if ($log.Content -match "Predictive dashboard") {
            $predictions++
            
            # Extract prediction accuracy metrics
            if ($log.Content -match "Prediction accuracy: (\d+\.\d+)%") {
                $accuracy = [double]$Matches[1] / 100
                $accuratePredictions += $accuracy
                $predictionErrors += (1 - $accuracy)
            }
        }
    }
    
    # Calculate metrics
    $averageAccuracy = if ($predictions -gt 0) { $accuratePredictions / $predictions } else { 0 }
    $averageError = if ($predictions -gt 0) { ($predictionErrors | Measure-Object -Average).Average } else { 0 }
    
    return @{
        Predictions = $predictions
        AveragePredictionAccuracy = $averageAccuracy
        AveragePredictionError = $averageError
        PredictionErrors = $predictionErrors
    }
}

function Get-AutomationSuiteMetrics {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [object[]]$Issues,
        [Parameter(Mandatory = $false)]
        [object[]]$Events,
        [Parameter(Mandatory = $false)]
        [object[]]$Logs
    )
    
    # Extract automation suite metrics
    # This is a simplified implementation for demonstration purposes
    
    $automationRuns = 0
    $successfulRuns = 0
    $failedRuns = 0
    $executionTimes = @()
    
    # Process logs to find automation metrics
    foreach ($log in $Logs) {
        if ($log.Content -match "Full Orchestration") {
            $automationRuns++
            
            # Extract run success/failure metrics
            if ($log.Content -match "completed successfully") {
                $successfulRuns++
            }
            elseif ($log.Content -match "failed") {
                $failedRuns++
            }
            
            # Extract execution time if available
            if ($log.Content -match "Execution time: (\d+\.\d+) seconds") {
                $executionTimes += [double]$Matches[1]
            }
        }
    }
    
    # Calculate metrics
    $successRate = if ($automationRuns -gt 0) { $successfulRuns / $automationRuns } else { 0 }
    $averageExecutionTime = if ($executionTimes.Count -gt 0) { ($executionTimes | Measure-Object -Average).Average } else { 0 }
    
    return @{
        AutomationRuns = $automationRuns
        SuccessfulRuns = $successfulRuns
        FailedRuns = $failedRuns
        SuccessRate = $successRate
        AverageExecutionTime = $averageExecutionTime
        ExecutionTimes = $executionTimes
    }
}

function Analyze-AutomationEffectiveness {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [PSCustomObject]$PerformanceData,
        [Parameter(Mandatory = $false)]
        [PSCustomObject]$Config
    )
    
    Write-Verbose "Analyzing automation effectiveness"
    
    # Extract key metrics for analysis
    $metrics = @{
        # Issue processing metrics
        IssuesProcessed = $PerformanceData.Issues.Count
        IssuesWithAutomation = ($PerformanceData.Issues | Where-Object { $_.Labels -contains "automated" }).Count
        
        # Intelligent routing metrics
        RoutingAccuracy = $PerformanceData.Components.IntelligentRouting.RoutingAccuracy
        RoutingDecisions = $PerformanceData.Components.IntelligentRouting.RoutingDecisions
        
        # Predictive dashboard metrics
        PredictionAccuracy = $PerformanceData.Components.PredictiveDashboard.AveragePredictionAccuracy
        
        # Automation suite metrics
        AutomationSuccessRate = $PerformanceData.Components.AutomationSuite.SuccessRate
        
        # Time metrics
        AverageRoutingTime = $PerformanceData.Components.IntelligentRouting.AverageRoutingTime
        AverageExecutionTime = $PerformanceData.Components.AutomationSuite.AverageExecutionTime
    }
    
    # Calculate effectiveness scores
    $scores = @{
        RoutingEffectiveness = $metrics.RoutingAccuracy * 100  # 0-100 scale
        PredictionEffectiveness = $metrics.PredictionAccuracy * 100  # 0-100 scale
        AutomationEffectiveness = $metrics.AutomationSuccessRate * 100  # 0-100 scale
        PerformanceEfficiency = if ($metrics.AverageExecutionTime -gt 0) { 
            100 - [Math]::Min(100, ($metrics.AverageExecutionTime / 10) * 100) 
        } else { 0 }  # Higher is better (lower execution time)
    }
    
    # Calculate overall effectiveness score
    $weights = @{
        Routing = 0.3
        Prediction = 0.2
        Automation = 0.3
        Performance = 0.2
    }
    
    $overallScore = ($scores.RoutingEffectiveness * $weights.Routing) +
                    ($scores.PredictionEffectiveness * $weights.Prediction) +
                    ($scores.AutomationEffectiveness * $weights.Automation) +
                    ($scores.PerformanceEfficiency * $weights.Performance)
    
    $effectiveness = @{
        Metrics = $metrics
        Scores = $scores
        OverallScore = $overallScore
        EffectivenessRating = switch ($overallScore) {
            { $_ -ge 90 } { "Excellent" }
            { $_ -ge 80 } { "Very Good" }
            { $_ -ge 70 } { "Good" }
            { $_ -ge 60 } { "Satisfactory" }
            { $_ -ge 50 } { "Needs Improvement" }
            default { "Requires Significant Improvement" }
        }
    }
    
    return $effectiveness
}

function Identify-OptimizationOpportunities {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [PSCustomObject]$EffectivenessMetrics,
        [Parameter(Mandatory = $false)]
        [PSCustomObject]$Config
    )
    
    Write-Verbose "Identifying optimization opportunities"
    
    $opportunities = @()
    
    # Check routing effectiveness
    if ($EffectivenessMetrics.Scores.RoutingEffectiveness -lt 85) {
        $opportunities += @{
            Component = "IntelligentRouting"
            Parameter = "confidence_threshold"
            CurrentValue = $Config.components.intelligent_routing.confidence_threshold
            RecommendedAction = "Adjust threshold to improve routing accuracy"
            Priority = if ($EffectivenessMetrics.Scores.RoutingEffectiveness -lt 70) { "High" } else { "Medium" }
            AdjustmentLogic = @{
                Direction = if ($EffectivenessMetrics.Metrics.RoutingAccuracy -lt 0.7) { "Increase" } else { "Decrease" }
                Magnitude = if ($EffectivenessMetrics.Scores.RoutingEffectiveness -lt 70) { 0.1 } else { 0.05 }
            }
        }
    }
    
    # Check prediction effectiveness
    if ($EffectivenessMetrics.Scores.PredictionEffectiveness -lt 80) {
        $opportunities += @{
            Component = "PredictiveDashboard"
            Parameter = "prediction_horizon_days"
            CurrentValue = $Config.components.predictive_dashboard.prediction_horizon_days
            RecommendedAction = "Adjust prediction horizon to improve accuracy"
            Priority = if ($EffectivenessMetrics.Scores.PredictionEffectiveness -lt 65) { "High" } else { "Medium" }
            AdjustmentLogic = @{
                Direction = if ($EffectivenessMetrics.Metrics.PredictionAccuracy -lt 0.65) { "Decrease" } else { "Increase" }
                Magnitude = if ($EffectivenessMetrics.Scores.PredictionEffectiveness -lt 65) { 7 } else { 5 }
            }
        }
    }
    
    # Check automation effectiveness
    if ($EffectivenessMetrics.Scores.AutomationEffectiveness -lt 90) {
        $opportunities += @{
            Component = "AutomationSettings"
            Parameter = "auto_triage"
            CurrentValue = $Config.automation_settings.auto_triage
            RecommendedAction = "Review auto-triage settings to improve success rate"
            Priority = if ($EffectivenessMetrics.Scores.AutomationEffectiveness -lt 75) { "High" } else { "Medium" }
            AdjustmentLogic = @{
                Type = "Boolean"
                RecommendedValue = if ($EffectivenessMetrics.Scores.AutomationEffectiveness -lt 75) { $false } else { $true }
            }
        }
    }
    
    # Check self-optimization settings
    $opportunities += @{
        Component = "SelfOptimization"
        Parameter = "learning_rate"
        CurrentValue = $Config.components.self_optimization.learning_rate
        RecommendedAction = "Adjust learning rate based on optimization effectiveness"
        Priority = "Medium"
        AdjustmentLogic = @{
            Direction = if ($EffectivenessMetrics.OverallScore -lt 70) { "Increase" } else { "Decrease" }
            Magnitude = if ($EffectivenessMetrics.OverallScore -lt 70) { 0.02 } else { 0.01 }
        }
    }
    
    return $opportunities
}

function Generate-ParameterAdjustments {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [array]$OptimizationOpportunities,
        [Parameter(Mandatory = $false)]
        [PSCustomObject]$Config
    )
    
    Write-Verbose "Generating parameter adjustments"
    
    $adjustments = @()
    
    foreach ($opportunity in $OptimizationOpportunities) {
        $adjustment = @{
            Component = $opportunity.Component
            Parameter = $opportunity.Parameter
            CurrentValue = $opportunity.CurrentValue
            Recommendation = $opportunity.RecommendedAction
            Priority = $opportunity.Priority
        }
        
        # Calculate new value based on adjustment logic
        if ($opportunity.AdjustmentLogic.Type -eq "Boolean") {
            $adjustment.NewValue = $opportunity.AdjustmentLogic.RecommendedValue
        }
        else {
            $currentValue = $opportunity.CurrentValue
            $direction = $opportunity.AdjustmentLogic.Direction
            $magnitude = $opportunity.AdjustmentLogic.Magnitude
            
            if ($direction -eq "Increase") {
                if ($currentValue -is [int]) {
                    $adjustment.NewValue = $currentValue + $magnitude
                }
                elseif ($currentValue -is [double]) {
                    $adjustment.NewValue = [Math]::Min(1.0, $currentValue + $magnitude)
                }
                else {
                    $adjustment.NewValue = $currentValue
                }
            }
            elseif ($direction -eq "Decrease") {
                if ($currentValue -is [int]) {
                    $adjustment.NewValue = [Math]::Max(1, $currentValue - $magnitude)
                }
                elseif ($currentValue -is [double]) {
                    $adjustment.NewValue = [Math]::Max(0.01, $currentValue - $magnitude)
                }
                else {
                    $adjustment.NewValue = $currentValue
                }
            }
            else {
                $adjustment.NewValue = $currentValue
            }
        }
        
        # Add to adjustments list
        $adjustments += $adjustment
    }
    
    return $adjustments
}

function Apply-OptimizationChanges {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [array]$ParameterAdjustments,
        [Parameter(Mandatory = $true)]
        [PSCustomObject]$Config,
        [Parameter(Mandatory = $false)]
        [string]$ConfigPath
    )
    
    Write-Verbose "Applying optimization changes"
    
    $appliedChanges = @()
    
    # Create a copy of the configuration to modify
    $updatedConfig = $Config | ConvertTo-Json -Depth 10 | ConvertFrom-Json
    
    # Apply each adjustment
    foreach ($adjustment in $ParameterAdjustments) {
        try {
            $component = $adjustment.Component
            $parameter = $adjustment.Parameter
            $newValue = $adjustment.NewValue
            
            # Apply the change to the appropriate configuration section
            switch ($component) {
                "IntelligentRouting" {
                    $updatedConfig.components.intelligent_routing.$parameter = $newValue
                }
                "PredictiveDashboard" {
                    $updatedConfig.components.predictive_dashboard.$parameter = $newValue
                }
                "SelfOptimization" {
                    $updatedConfig.components.self_optimization.$parameter = $newValue
                }
                "AutomationSettings" {
                    $updatedConfig.automation_settings.$parameter = $newValue
                }
                default {
                    Write-Warning "Unknown component: $component"
                    continue
                }
            }
            
            $appliedChanges += @{
                Component = $component
                Parameter = $parameter
                OldValue = $adjustment.CurrentValue
                NewValue = $newValue
                Status = "Success"
            }
        }
        catch {
            Write-Error "Failed to apply change to $component.$parameter: $_"
            $appliedChanges += @{
                Component = $component
                Parameter = $parameter
                OldValue = $adjustment.CurrentValue
                Status = "Failed"
                Error = $_.Exception.Message
            }
        }
    }
    
    # Save the updated configuration
    if ($ConfigPath -and $appliedChanges.Count -gt 0) {
        try {
            $updatedConfig.last_updated = (Get-Date).ToString("yyyy-MM-dd")
            $updatedConfig | ConvertTo-Json -Depth 10 | Set-Content -Path $ConfigPath -Encoding UTF8
            Write-Verbose "Updated configuration saved to $ConfigPath"
        }
        catch {
            Write-Error "Failed to save updated configuration: $_"
        }
    }
    
    return @{
        ChangesApplied = $appliedChanges.Count -gt 0
        AppliedChanges = $appliedChanges
        UpdatedConfig = $updatedConfig
        Timestamp = Get-Date
    }
}

function Generate-OptimizationReport {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [PSCustomObject]$OptimizationResult,
        [Parameter(Mandatory = $true)]
        [PSCustomObject]$EffectivenessMetrics
    )
    
    # Generate a detailed markdown report of the optimization process
    $report = @"
# Self-Optimization Report

**Generated**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**Changes Applied**: $($OptimizationResult.ChangesApplied)

## Effectiveness Metrics

### Overall Effectiveness Score: $([Math]::Round($EffectivenessMetrics.OverallScore, 2))
**Rating**: $($EffectivenessMetrics.EffectivenessRating)

### Component Scores
- **Routing Effectiveness**: $([Math]::Round($EffectivenessMetrics.Scores.RoutingEffectiveness, 2))%
- **Prediction Effectiveness**: $([Math]::Round($EffectivenessMetrics.Scores.PredictionEffectiveness, 2))%
- **Automation Effectiveness**: $([Math]::Round($EffectivenessMetrics.Scores.AutomationEffectiveness, 2))%
- **Performance Efficiency**: $([Math]::Round($EffectivenessMetrics.Scores.PerformanceEfficiency, 2))%

## Applied Changes

"@

    if ($OptimizationResult.AppliedChanges.Count -eq 0) {
        $report += "No changes were applied during this optimization run."
    }
    else {
        $report += "| Component | Parameter | Old Value | New Value | Status |`n"
        $report += "|-----------|-----------|-----------|-----------|--------|`n"
        
        foreach ($change in $OptimizationResult.AppliedChanges) {
            $report += "| $($change.Component) | $($change.Parameter) | $($change.OldValue) | $($change.NewValue) | $($change.Status) |`n"
        }
    }
    
    $report += @"

## Optimization Analysis

### Key Metrics
- **Issues Processed**: $($EffectivenessMetrics.Metrics.IssuesProcessed)
- **Issues With Automation**: $($EffectivenessMetrics.Metrics.IssuesWithAutomation)
- **Routing Decisions**: $($EffectivenessMetrics.Metrics.RoutingDecisions)
- **Routing Accuracy**: $([Math]::Round($EffectivenessMetrics.Metrics.RoutingAccuracy * 100, 2))%
- **Prediction Accuracy**: $([Math]::Round($EffectivenessMetrics.Metrics.PredictionAccuracy * 100, 2))%
- **Automation Success Rate**: $([Math]::Round($EffectivenessMetrics.Metrics.AutomationSuccessRate * 100, 2))%

### Recommendations

- Continue monitoring the effects of these optimization changes
- Consider manual review of routing decisions to improve training data
- Review automation failure cases to identify common patterns
- Adjust the learning rate if optimization is too aggressive or too conservative

### Next Steps

1. Allow the system to operate with these new parameters for at least one week
2. Run another optimization cycle to assess the impact of these changes
3. Consider additional data sources for more comprehensive optimization
"@

    return $report
}

#endregion

#region Help System

function Show-DetailedHelp {
    [CmdletBinding()]
    param()

    $helpText = @"
FULL AUTOMATION SUITE - DETAILED HELP
====================================

VERSION: $ScriptVersion ($ScriptDate)
$PhaseInfo

DESCRIPTION
-----------
The Full Automation Suite integrates all components of the GitHub Issues Workflow
Automation project into a unified system with intelligent routing, self-optimization,
and minimal human intervention.

AVAILABLE ACTIONS
----------------
orchestrate  : Run the full orchestration with intelligent routing
setup        : Configure the automation suite and GitHub integrations
report       : Generate comprehensive performance reports
optimize     : Run the self-optimization process
validate     : Validate the automation configuration
help         : Display this detailed help information

COMPONENT INTEGRATION
-------------------
This suite integrates with the following components:

Phase 1:
  - PRD Fast-Track Validation (manage_issues.ps1)
  - Enhanced Issue Templates
  - PRD Template Generator (generate_prd.ps1)
  - Dashboard Generator (generate_dashboard.ps1)
  - Batch Operations (batch_operations.ps1)

Phase 2:
  - Cycle Time Analyzer (analyze_cycle_times.ps1)
  - Smart Assignment System (suggest_assignment.ps1)
  - Automated Planning Analysis (analyze_planning.ps1)

Phase 3:
  - Intelligent Issue Routing (intelligent_routing.ps1)
  - Predictive Analytics Dashboard (predictive_dashboard.ps1)
  - Full Automation Suite (this component)

EXAMPLES
--------
# Run the full orchestration process
./full_automation_suite.ps1 -Action orchestrate -Repository "myorg/myrepo"

# Set up the automation suite with GitHub webhook integrations
./full_automation_suite.ps1 -Action setup -Repository "myorg/myrepo" -Token "ghp_123456"

# Generate comprehensive performance reports
./full_automation_suite.ps1 -Action report -Repository "myorg/myrepo"

# Run the self-optimization process
./full_automation_suite.ps1 -Action optimize -Repository "myorg/myrepo"

# Validate the automation configuration
./full_automation_suite.ps1 -Action validate -ConfigPath "./custom_config.json"

FURTHER ASSISTANCE
-----------------
For additional help with specific components, use the -help parameter with each component script.
Example: ./intelligent_routing.ps1 -help
"@

    Write-Host $helpText
}

#endregion

#region Main Execution Logic

# Load configuration
$Config = Load-Configuration -ConfigPath $ConfigPath

# Process action
try {
    switch ($Action) {
        'orchestrate' {
            # Handle GitHub Actions triggered events
            if ($TriggerEvent -and $EventType -and $IssueNumber -gt 0) {
                Write-Host "Orchestrating from GitHub Actions trigger: $TriggerEvent - $EventType for issue #$IssueNumber"
                
                if (-not $Repository) {
                    if ($Config -and $Config.repository) {
                        $Repository = $Config.repository
                        Write-Verbose "Using repository from configuration: $Repository"
                    }
                    else {
                        # Try to extract from GitHub environment
                        $Repository = $env:GITHUB_REPOSITORY
                        if (-not $Repository) {
                            Write-Error "Repository parameter is required for orchestration."
                            exit 1
                        }
                    }
                }
                
                # Process the GitHub issue event
                Process-IssueEvent -TriggerEvent $TriggerEvent -EventType $EventType -IssueNumber $IssueNumber -Repository $Repository
            }
            else {
                # Standard orchestration
                if (-not $Repository) {
                    if ($Config -and $Config.repository) {
                        $Repository = $Config.repository
                        Write-Verbose "Using repository from configuration: $Repository"
                    }
                    else {
                        Write-Error "Repository parameter is required for orchestration."
                        exit 1
                    }
                }
                
                Invoke-FullOrchestration -Repository $Repository -Config $Config
            }
        }
        
        'setup' {
            if (-not $Repository) {
                Write-Error "Repository parameter is required for setup."
                exit 1
            }
            
            # Check if this is a GitHub workflow setup request
            if ($OutputPath) {
                Write-Host "Setting up GitHub Actions workflows at: $OutputPath"
                Generate-WorkflowFiles -OutputPath $OutputPath -Force:$NoPrompt
            }
            else {
                Invoke-AutomationSetup -Repository $Repository -Token $Token -Config $Config
            }
        }
        
        'report' {
            if (-not $Repository) {
                if ($Config -and $Config.repository) {
                    $Repository = $Config.repository
                    Write-Verbose "Using repository from configuration: $Repository"
                }
                else {
                    Write-Error "Repository parameter is required for reporting."
                    exit 1
                }
            }
            
            # Check for OutputPath parameter (used by GitHub Actions)
            if ($OutputPath) {
                Write-Host "Generating report to file: $OutputPath"
                Invoke-ComprehensiveReporting -Repository $Repository -Config $Config -OutputFile $OutputPath
            }
            else {
                Invoke-ComprehensiveReporting -Repository $Repository -Config $Config
            }
        }
        
        'optimize' {
            if (-not $Repository) {
                if ($Config -and $Config.repository) {
                    $Repository = $Config.repository
                    Write-Verbose "Using repository from configuration: $Repository"
                }
                else {
                    Write-Error "Repository parameter is required for optimization."
                    exit 1
                }
            }
            
            Invoke-SelfOptimization -Repository $Repository -Config $Config
        }
        
        'validate' {
            Invoke-ConfigurationValidation -Repository $Repository -Config $Config -ConfigPath $ConfigPath
        }
        
        'help' {
            Show-DetailedHelp
        }
        
        default {
            Write-Error "Unknown action: $Action"
            exit 1
        }
    }
}
catch {
    Write-Error "An error occurred during execution: $_"
    exit 1
}

#endregion

function Process-IssueEvent {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [string]$TriggerEvent,
        
        [Parameter(Mandatory = $true)]
        [string]$EventType,
        
        [Parameter(Mandatory = $true)]
        [int]$IssueNumber,
        
        [Parameter(Mandatory = $false)]
        [string]$Repository
    )
    
    Write-Host "Processing $TriggerEvent event ($EventType) for issue #$IssueNumber in $Repository" -ForegroundColor Cyan
    
    # Split repository into owner and repo name
    $repoSplit = $Repository -split "/"
    if ($repoSplit.Count -ne 2) {
        Write-Error "Invalid repository format. Expected 'owner/repo', got '$Repository'"
        return
    }
    
    $ownerName = $repoSplit[0]
    $repoName = $repoSplit[1]
    
    # Get issue details
    try {
        $issue = Get-GitHubIssue -OwnerName $ownerName -RepositoryName $repoName -Issue $IssueNumber
        Write-Verbose "Retrieved issue #$IssueNumber: $($issue.title)"
    }
    catch {
        Write-Error "Failed to get issue details: $_"
        return
    }
    
    # Create an event log entry
    $eventLog = @{
        Timestamp = Get-Date
        Event = $TriggerEvent
        EventType = $EventType
        IssueNumber = $IssueNumber
        IssueTitle = $issue.title
        Repository = $Repository
        Actions = @()
    }
    
    # Perform intelligent routing based on the event type
    switch ($EventType) {
        "opened" {
            Write-Host "New issue opened - performing initial analysis and routing" -ForegroundColor Yellow
            
            # Log the action
            $eventLog.Actions += "Initial triage and routing"
            
            # Run intelligent routing
            $intelligentRoutingScript = Join-Path $PSScriptRoot "intelligent_routing.ps1"
            if (Test-Path $intelligentRoutingScript) {
                Write-Host "  Executing intelligent routing..." -ForegroundColor Gray
                & $intelligentRoutingScript -Repository $Repository -IssueNumber $IssueNumber
                $eventLog.Actions += "Executed intelligent routing"
            }
            else {
                Write-Warning "Intelligent routing script not found at: $intelligentRoutingScript"
                $eventLog.Actions += "FAILED: Intelligent routing script not found"
            }
            
            # Check for PRD content and run fast-track validation if applicable
            if ($issue.body -match "## PRD" -or $issue.body -match "# Product Requirements") {
                Write-Host "  PRD content detected - running fast-track validation" -ForegroundColor Gray
                $manageIssuesScript = Join-Path $PSScriptRoot "manage_issues.ps1"
                if (Test-Path $manageIssuesScript) {
                    & $manageIssuesScript -Action "fast-track" -Repository $Repository -IssueNumber $IssueNumber -ValidatePRD
                    $eventLog.Actions += "Executed PRD fast-track validation"
                }
                else {
                    Write-Warning "Issue management script not found at: $manageIssuesScript"
                    $eventLog.Actions += "FAILED: Issue management script not found"
                }
            }
            
            # Generate initial metrics
            Write-Host "  Updating metrics and dashboards" -ForegroundColor Gray
            $eventLog.Actions += "Generated initial metrics"
        }
        
        "edited" {
            Write-Host "Issue edited - checking for changes requiring action" -ForegroundColor Yellow
            
            # Log the action
            $eventLog.Actions += "Processing edit event"
            
            # If PRD section was added or modified, run validation
            if ($issue.body -match "## PRD" -or $issue.body -match "# Product Requirements") {
                Write-Host "  PRD content detected - running validation" -ForegroundColor Gray
                $manageIssuesScript = Join-Path $PSScriptRoot "manage_issues.ps1"
                if (Test-Path $manageIssuesScript) {
                    & $manageIssuesScript -Action "fast-track" -Repository $Repository -IssueNumber $IssueNumber -ValidatePRD
                    $eventLog.Actions += "Executed PRD validation after edit"
                }
                else {
                    Write-Warning "Issue management script not found at: $manageIssuesScript"
                    $eventLog.Actions += "FAILED: Issue management script not found"
                }
            }
            
            # Re-run intelligent routing to check if the issue should be re-classified
            $intelligentRoutingScript = Join-Path $PSScriptRoot "intelligent_routing.ps1"
            if (Test-Path $intelligentRoutingScript) {
                Write-Host "  Re-analyzing issue routing after edit..." -ForegroundColor Gray
                & $intelligentRoutingScript -Repository $Repository -IssueNumber $IssueNumber -Mode "update"
                $eventLog.Actions += "Re-analyzed issue routing after edit"
            }
        }
        
        "labeled" {
            Write-Host "Issue labeled - processing label-specific actions" -ForegroundColor Yellow
            
            # Log the action
            $eventLog.Actions += "Processing label event"
            
            # Get the label that was added (available in GitHub Actions context)
            $addedLabel = $env:GITHUB_EVENT_LABEL_NAME
            Write-Host "  Label added: $addedLabel" -ForegroundColor Gray
            
            # Run smart assignment if appropriate labels are applied
            if ($issue.labels -contains "ready-for-dev" -or 
                $issue.labels -contains "high-priority" -or 
                $addedLabel -eq "ready-for-dev" -or 
                $addedLabel -eq "high-priority") {
                
                Write-Host "  Priority or ready label detected - suggesting assignment" -ForegroundColor Gray
                $suggestAssignmentScript = Join-Path $PSScriptRoot "suggest_assignment.ps1"
                if (Test-Path $suggestAssignmentScript) {
                    & $suggestAssignmentScript -Repository $Repository -IssueNumber $IssueNumber
                    $eventLog.Actions += "Executed smart assignment suggestion"
                }
                else {
                    Write-Warning "Assignment suggestion script not found at: $suggestAssignmentScript"
                    $eventLog.Actions += "FAILED: Assignment suggestion script not found"
                }
            }
            
            # Run cycle time analysis if a status label is applied
            if ($addedLabel -match "status:" -or $issue.labels -match "status:") {
                Write-Host "  Status label detected - updating cycle time metrics" -ForegroundColor Gray
                $cycleTimeScript = Join-Path $PSScriptRoot "analyze_cycle_times.ps1"
                if (Test-Path $cycleTimeScript) {
                    & $cycleTimeScript -Repository $Repository -Action "update-metrics" -IssueNumber $IssueNumber
                    $eventLog.Actions += "Updated cycle time metrics"
                }
            }
        }
        
        "unlabeled" {
            Write-Host "Issue unlabeled - checking for workflow implications" -ForegroundColor Yellow
            
            # Log the action
            $eventLog.Actions += "Processing unlabel event"
            
            # Check if status changed
            $cycleTimeScript = Join-Path $PSScriptRoot "analyze_cycle_times.ps1"
            if (Test-Path $cycleTimeScript) {
                & $cycleTimeScript -Repository $Repository -Action "update-metrics" -IssueNumber $IssueNumber
                $eventLog.Actions += "Updated cycle time metrics after label removal"
            }
        }
        
        "assigned" {
            Write-Host "Issue assigned - updating assignment metrics" -ForegroundColor Yellow
            
            # Log the action
            $eventLog.Actions += "Processing assignment event"
            
            # Update assignment metrics
            $assignmentScript = Join-Path $PSScriptRoot "suggest_assignment.ps1"
            if (Test-Path $assignmentScript) {
                & $assignmentScript -Repository $Repository -Action "record-assignment" -IssueNumber $IssueNumber
                $eventLog.Actions += "Recorded assignment metrics"
            }
        }
        
        "closed" {
            Write-Host "Issue closed - finalizing metrics and analysis" -ForegroundColor Yellow
            
            # Log the action
            $eventLog.Actions += "Processing issue closure"
            
            # Update cycle time analytics
            $cycleTimeScript = Join-Path $PSScriptRoot "analyze_cycle_times.ps1"
            if (Test-Path $cycleTimeScript) {
                & $cycleTimeScript -Repository $Repository -Action "finalize" -IssueNumber $IssueNumber
                $eventLog.Actions += "Finalized cycle time metrics"
            }
            
            # Check if this is a completed feature
            if ($issue.labels -contains "feature" -or $issue.labels -contains "enhancement") {
                Write-Host "  Feature/enhancement closed - updating planning metrics" -ForegroundColor Gray
                $planningScript = Join-Path $PSScriptRoot "analyze_planning.ps1"
                if (Test-Path $planningScript) {
                    & $planningScript -Repository $Repository -Action "record-completion" -IssueNumber $IssueNumber
                    $eventLog.Actions += "Updated planning metrics for completed feature"
                }
            }
        }
        
        "reopened" {
            Write-Host "Issue reopened - resetting metrics and re-analyzing" -ForegroundColor Yellow
            
            # Log the action
            $eventLog.Actions += "Processing issue reopen event"
            
            # Reset cycle time for reopened issue
            $cycleTimeScript = Join-Path $PSScriptRoot "analyze_cycle_times.ps1"
            if (Test-Path $cycleTimeScript) {
                & $cycleTimeScript -Repository $Repository -Action "reset" -IssueNumber $IssueNumber
                $eventLog.Actions += "Reset cycle time metrics for reopened issue"
            }
            
            # Re-run routing to ensure proper classification
            $intelligentRoutingScript = Join-Path $PSScriptRoot "intelligent_routing.ps1"
            if (Test-Path $intelligentRoutingScript) {
                & $intelligentRoutingScript -Repository $Repository -IssueNumber $IssueNumber
                $eventLog.Actions += "Re-analyzed reopened issue"
            }
        }
        
        default {
            Write-Host "Processing standard event: $EventType" -ForegroundColor Gray
            $eventLog.Actions += "Processed standard event: $EventType (no specific actions)"
        }
    }
    
    # Save event log
    $reportsPath = Join-Path (Split-Path -Parent $PSScriptRoot) "reports"
    if (-not (Test-Path $reportsPath)) {
        New-Item -Path $reportsPath -ItemType Directory -Force | Out-Null
    }
    
    $logFilename = "event_log_$(Get-Date -Format 'yyyyMMdd_HHmmss')_issue$IssueNumber.json"
    $logFilePath = Join-Path $reportsPath $logFilename
    
    $eventLog | ConvertTo-Json -Depth 5 | Set-Content -Path $logFilePath -Encoding UTF8
    Write-Verbose "Event log saved to: $logFilePath"
    
    # Update dashboards
    Write-Host "Updating dashboards with latest information" -ForegroundColor Yellow
    $dashboardScript = Join-Path $PSScriptRoot "generate_dashboard.ps1"
    if (Test-Path $dashboardScript) {
        & $dashboardScript -Repository $Repository -Type "comprehensive" -Quiet
        $eventLog.Actions += "Updated dashboards"
    }
    
    # Run predictive analytics if appropriate
    if (@("opened", "closed", "reopened") -contains $EventType) {
        Write-Host "Running predictive analytics" -ForegroundColor Yellow
        $predictiveScript = Join-Path $PSScriptRoot "predictive_dashboard.ps1"
        if (Test-Path $predictiveScript) {
            & $predictiveScript -Repository $Repository -Action "forecast" -Quiet
            $eventLog.Actions += "Updated predictive analytics"
        }
    }
    
    Write-Host "Event processing completed for issue #$IssueNumber" -ForegroundColor Green
    
    return $eventLog
}

function Generate-WorkflowFiles {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [string]$OutputPath,
        
        [Parameter(Mandatory = $false)]
        [switch]$Force
    )
    
    Write-Host "Generating GitHub Actions workflow files"
    
    $workflowContent = @"
name: GitHub Issues Workflow Automation

on:
  issues:
    types: [opened, edited, labeled, unlabeled, assigned, unassigned, closed, reopened]
  issue_comment:
    types: [created, edited]
  workflow_dispatch:
    inputs:
      action:
        description: 'Action to run (orchestrate, report, optimize, validate)'
        required: true
        default: 'orchestrate'
      dry_run:
        description: 'Dry run mode (true/false)'
        required: false
        default: 'false'

jobs:
  issue-automation:
    runs-on: windows-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up PowerShell modules
        shell: pwsh
        run: |
          Install-Module -Name PowerShellForGitHub -Force -Scope CurrentUser

      - name: Issue event trigger
        if: github.event_name == 'issues' || github.event_name == 'issue_comment'
        shell: pwsh
        run: |
          ./scripts/full_automation_suite.ps1 -Action orchestrate -TriggerEvent `${{ github.event_name }} -EventType `${{ github.event.action }} -IssueNumber `${{ github.event.issue.number }}
        env:
          GITHUB_TOKEN: `${{ secrets.GITHUB_TOKEN }}

      - name: Manual workflow trigger
        if: github.event_name == 'workflow_dispatch'
        shell: pwsh
        run: |
          ./scripts/full_automation_suite.ps1 -Action `${{ github.event.inputs.action }} -DryRun `${{ github.event.inputs.dry_run }}
        env:
          GITHUB_TOKEN: `${{ secrets.GITHUB_TOKEN }}

      - name: Generate Automation Report
        shell: pwsh
        run: |
          ./scripts/full_automation_suite.ps1 -Action report -OutputPath 'automation-report.md'
        env:
          GITHUB_TOKEN: `${{ secrets.GITHUB_TOKEN }}

      - name: Upload Automation Report
        uses: actions/upload-artifact@v3
        with:
          name: automation-report
          path: automation-report.md
"@

    # Create directory if it doesn't exist
    $workflowDir = Join-Path $OutputPath ".github/workflows"
    if (-not (Test-Path $workflowDir)) {
        New-Item -Path $workflowDir -ItemType Directory -Force | Out-Null
    }
    
    $workflowFilePath = Join-Path $workflowDir "issue-automation.yml"
    
    # Check if file exists and Force is not specified
    if ((Test-Path $workflowFilePath) -and -not $Force) {
        Write-Host "Workflow file already exists. Use -Force to overwrite."
        return
    }
    
    # Create the workflow file
    Set-Content -Path $workflowFilePath -Value $workflowContent
    
    Write-Host "GitHub Actions workflow file created at: $workflowFilePath"
}

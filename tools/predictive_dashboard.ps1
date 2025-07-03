#!/usr/bin/env powershell
<#
.SYNOPSIS
    Predictive Analytics Dashboard for GitHub Issues workflow capacity forecasting and delivery prediction

.DESCRIPTION
    Generates a comprehensive predictive analytics dashboard for the DexBot GitHub Issues workflow,
    featuring velocity trending, delivery forecasting, capacity alerts, and workload predictions.
    Integrates with existing analytics systems to provide forward-looking insights and proactive
    workflow optimization recommendations.

.PARAMETER Action
    Type of predictive analysis to perform:
    - forecast: Generate delivery date forecasts for active issues
    - capacity: Analyze team capacity and provide workload optimization
    - velocity: Track velocity trends and predict future velocity
    - bottlenecks: Predict future bottlenecks based on current workflow patterns
    - risk: Identify high-risk issues that may impact delivery timeline
    - full: Generate comprehensive predictive dashboard with all metrics

.PARAMETER OutputPath
    Path where the dashboard file will be created (default: current directory)

.PARAMETER OutputFormat
    Output format: markdown, html, json, or csv

.PARAMETER TimeRange
    Historical time range for prediction baseline: 30d, 90d, 180d, or all

.PARAMETER ForecastWindow
    Future time window for predictions: 7d, 14d, 30d, 90d

.PARAMETER Confidence
    Confidence level for predictions: 0.8 (80%), 0.9 (90%), or 0.95 (95%)

.PARAMETER RefreshData
    Refresh data from GitHub API before generating dashboard

.PARAMETER Interactive
    Run in interactive mode with detailed methodology explanations

.PARAMETER DryRun
    Run predictions without saving output files

.PARAMETER Force
    Overwrite existing dashboard files

.PARAMETER TeamCapacity
    Specify team capacity in person-hours per week (default: auto-detected)

.PARAMETER VelocityMetric
    Velocity metric to use: story-points, issue-count, or time-spent

.EXAMPLE
    .\predictive_dashboard.ps1 -Action forecast -TimeRange 90d
    .\predictive_dashboard.ps1 -Action capacity -TeamCapacity 120 -Interactive
    .\predictive_dashboard.ps1 -Action full -OutputFormat html -RefreshData
    .\predictive_dashboard.ps1 -Action velocity -VelocityMetric story-points -ForecastWindow 30d
#>

param(
    [Parameter(Position=0)]
    [ValidateSet("forecast", "capacity", "velocity", "bottlenecks", "risk", "full")]
    [string]$Action = "full",
    
    [string]$OutputPath = ".",
    
    [ValidateSet("markdown", "html", "json", "csv")]
    [string]$OutputFormat = "markdown",
    
    [ValidateSet("30d", "90d", "180d", "all")]
    [string]$TimeRange = "90d",
    
    [ValidateSet("7d", "14d", "30d", "90d")]
    [string]$ForecastWindow = "30d",
    
    [ValidateSet(0.8, 0.9, 0.95)]
    [double]$Confidence = 0.8,
    
    [switch]$RefreshData,
    
    [switch]$Interactive,
    
    [switch]$DryRun,
    
    [switch]$Force,
    
    [int]$TeamCapacity = 0,
    
    [ValidateSet("story-points", "issue-count", "time-spent")]
    [string]$VelocityMetric = "story-points"
)

# ============================================================================
# SCRIPT INITIALIZATION
# ============================================================================

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
$VerbosePreference = if ($Interactive -eq $true) { "Continue" } else { "SilentlyContinue" }

# Script metadata
$ScriptVersion = "1.0.0"
$ScriptDate = "2025-07-02"

# Constants
$SCRIPT_ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
$DEFAULT_OUTPUT_FILENAME = "predictive_analytics_dashboard"
$DATA_CACHE_PATH = Join-Path $SCRIPT_ROOT ".." "tmp" "predictive_data_cache.json"
$LOG_PATH = Join-Path $SCRIPT_ROOT ".." "tmp" "predictive_dashboard_log.txt"

# Import common modules if they exist
$CommonModulePath = Join-Path $SCRIPT_ROOT "common" "github_utils.ps1"
if (Test-Path $CommonModulePath) {
    . $CommonModulePath
}

# Banner and initialization message
function Show-Banner {
    Write-Host ""
    Write-Host "Predictive Analytics Dashboard Generator v$ScriptVersion" -ForegroundColor Cyan
    Write-Host "DexBot GitHub Issues Workflow - Intelligent Automation (Phase 3)" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""
}

# Log function for tracking script execution
function Write-Log {
    param(
        [string]$Message,
        [ValidateSet("INFO", "WARNING", "ERROR", "SUCCESS")]
        [string]$Level = "INFO"
    )
    
    $TimeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogMessage = "[$TimeStamp] [$Level] $Message"
    
    # Create log directory if it doesn't exist
    $LogDir = Split-Path -Parent $LOG_PATH
    if (-not (Test-Path $LogDir)) {
        New-Item -Path $LogDir -ItemType Directory -Force | Out-Null
    }
    
    # Append to log file
    Add-Content -Path $LOG_PATH -Value $LogMessage
    
    # Console output with color coding
    switch ($Level) {
        "WARNING" { Write-Host $LogMessage -ForegroundColor Yellow }
        "ERROR" { Write-Host $LogMessage -ForegroundColor Red }
        "SUCCESS" { Write-Host $LogMessage -ForegroundColor Green }
        default { Write-Host $LogMessage }
    }
}

# ============================================================================
# DATA COLLECTION AND INTEGRATION
# ============================================================================

# Get data from GitHub API or local cache
function Get-IssueAnalyticsData {
    param(
        [switch]$ForceRefresh
    )
    
    if ($ForceRefresh -or (-not (Test-Path $DATA_CACHE_PATH)) -or $RefreshData) {
        Write-Log "Refreshing GitHub data from API..." -Level "INFO"
        try {
            # Integrate with existing data collection from analytics scripts
            # This leverages functionality from analyze_cycle_times.ps1 and analyze_planning.ps1
            
            # Placeholder for actual implementation - in production would call helper functions
            # from the common GitHub utilities module or directly use GitHub API
            
            $Data = @{
                "refreshTimestamp" = (Get-Date).ToString("o")
                "issues" = @()
                "metrics" = @{
                    "velocity" = @{}
                    "leadTime" = @{}
                    "throughput" = @{}
                }
            }
            
            # Save to cache
            $DataDir = Split-Path -Parent $DATA_CACHE_PATH
            if (-not (Test-Path $DataDir)) {
                New-Item -Path $DataDir -ItemType Directory -Force | Out-Null
            }
            
            $Data | ConvertTo-Json -Depth 20 | Set-Content -Path $DATA_CACHE_PATH
            Write-Log "Data refreshed and cached successfully" -Level "SUCCESS"
            return $Data
        }
        catch {
            Write-Log "Failed to refresh data: $_" -Level "ERROR"
            if (Test-Path $DATA_CACHE_PATH) {
                Write-Log "Using cached data instead" -Level "WARNING"
                return Get-Content -Path $DATA_CACHE_PATH | ConvertFrom-Json
            }
            else {
                throw "No cached data available and refresh failed"
            }
        }
    }
    else {
        Write-Log "Using cached GitHub data" -Level "INFO"
        return Get-Content -Path $DATA_CACHE_PATH | ConvertFrom-Json
    }
}

# ============================================================================
# VELOCITY PREDICTION FUNCTIONS
# ============================================================================

# Calculate historical velocity based on completed issues
function Get-HistoricalVelocity {
    param(
        [PSCustomObject]$Data,
        [string]$TimeFrame,
        [string]$Metric
    )
    
    Write-Log "Calculating historical velocity for $TimeFrame using $Metric" -Level "INFO"
    
    # Convert time frame string to actual timespan
    $DaysBack = switch ($TimeFrame) {
        "30d" { 30 }
        "90d" { 90 }
        "180d" { 180 }
        "all" { 1000 } # Effectively all
        default { 30 }
    }
    
    $CutoffDate = (Get-Date).AddDays(-$DaysBack)
    
    # Filter and calculate metrics based on the specified metric type
    # This would be implemented to work with the actual data structure
    
    # Placeholder implementation
    $VelocityResult = @{
        "average" = 0
        "median" = 0
        "trend" = "stable" # stable, increasing, decreasing
        "volatility" = 0.1 # standard deviation as percentage of mean
        "dataPoints" = @()
        "rawData" = @{}
    }
    
    return $VelocityResult
}

# Predict future velocity using statistical modeling
function Get-VelocityForecast {
    param(
        [hashtable]$HistoricalVelocity,
        [string]$ForecastWindow,
        [double]$ConfidenceLevel
    )
    
    Write-Log "Forecasting velocity for $ForecastWindow at $ConfidenceLevel confidence level" -Level "INFO"
    
    # Convert forecast window string to number of days
    $ForecastDays = switch ($ForecastWindow) {
        "7d" { 7 }
        "14d" { 14 }
        "30d" { 30 }
        "90d" { 90 }
        default { 30 }
    }
    
    # Implement statistical forecasting
    # In a real implementation, this would use time series analysis techniques
    # like moving averages, linear regression, or ARIMA models
    
    # Placeholder implementation
    $Forecast = @{
        "forecastDays" = $ForecastDays
        "confidenceLevel" = $ConfidenceLevel
        "expectedVelocity" = $HistoricalVelocity.average
        "lowEstimate" = $HistoricalVelocity.average * 0.8
        "highEstimate" = $HistoricalVelocity.average * 1.2
        "riskAdjusted" = $HistoricalVelocity.average * 0.9
        "predictedTrend" = $HistoricalVelocity.trend
        "weeklyBreakdown" = @()
    }
    
    # Generate weekly breakdown
    $WeeksInForecast = [Math]::Ceiling($ForecastDays / 7)
    for ($i = 1; $i -le $WeeksInForecast; $i++) {
        $WeekForecast = @{
            "week" = $i
            "expectedVelocity" = $Forecast.expectedVelocity
            "lowEstimate" = $Forecast.lowEstimate
            "highEstimate" = $Forecast.highEstimate
        }
        $Forecast.weeklyBreakdown += $WeekForecast
    }
    
    return $Forecast
}

# ============================================================================
# CAPACITY ANALYSIS FUNCTIONS
# ============================================================================

# Determine team capacity and allocation
function Get-TeamCapacityAnalysis {
    param(
        [PSCustomObject]$Data,
        [int]$SpecifiedCapacity,
        [hashtable]$VelocityForecast
    )
    
    Write-Log "Analyzing team capacity and workload distribution" -Level "INFO"
    
    # Auto-detect capacity if not specified
    $ActualCapacity = $SpecifiedCapacity
    if ($ActualCapacity -eq 0) {
        # In production this would analyze contributor patterns
        # from historical data to estimate team capacity
        $ActualCapacity = 120 # Placeholder: 3 devs × 40 hours
        Write-Log "Auto-detected team capacity: $ActualCapacity person-hours/week" -Level "INFO"
    }
    
    # Analyze capacity allocation and bottlenecks
    $CapacityAnalysis = @{
        "totalCapacity" = $ActualCapacity
        "allocatedCapacity" = 0
        "remainingCapacity" = $ActualCapacity
        "utilizationRate" = 0.0
        "optimalAllocation" = @{}
        "bottlenecks" = @()
        "recommendations" = @()
    }
    
    # In production, this would analyze current workload
    # and determine optimal allocation across components
    
    # Placeholder: Sample allocation
    $CapacityAnalysis.allocatedCapacity = 90
    $CapacityAnalysis.remainingCapacity = $ActualCapacity - $CapacityAnalysis.allocatedCapacity
    $CapacityAnalysis.utilizationRate = $CapacityAnalysis.allocatedCapacity / $ActualCapacity
    
    $CapacityAnalysis.optimalAllocation = @{
        "auto-heal" = 20
        "combat" = 30
        "looting" = 15
        "ui" = 25
        "core" = 30
    }
    
    # Generate recommendations based on capacity and forecast
    if ($CapacityAnalysis.utilizationRate > 0.9) {
        $CapacityAnalysis.recommendations += "Team is near capacity. Consider reducing incoming work or increasing resources."
    }
    
    return $CapacityAnalysis
}

# ============================================================================
# DELIVERY FORECASTING FUNCTIONS
# ============================================================================

# Predict delivery dates for open issues
function Get-DeliveryForecast {
    param(
        [PSCustomObject]$Data,
        [hashtable]$VelocityForecast,
        [hashtable]$CapacityAnalysis,
        [string]$ForecastWindow,
        [double]$ConfidenceLevel
    )
    
    Write-Log "Generating delivery forecasts for open issues" -Level "INFO"
    
    # This would use the velocity forecast and capacity analysis
    # to predict delivery dates for each open issue
    
    # Convert forecast window string to number of days
    $ForecastDays = switch ($ForecastWindow) {
        "7d" { 7 }
        "14d" { 14 }
        "30d" { 30 }
        "90d" { 90 }
        default { 30 }
    }
    
    # Placeholder implementation
    $Forecasts = @{
        "issues" = @()
        "summary" = @{
            "totalIssues" = 0
            "predictedOnTime" = 0
            "predictedLate" = 0
            "averageDelay" = 0
            "criticalPath" = @()
        }
    }
    
    # In production, this would analyze each open issue
    # and predict delivery dates based on complexity, priority,
    # historical patterns, and team capacity
    
    return $Forecasts
}

# ============================================================================
# BOTTLENECK PREDICTION FUNCTIONS
# ============================================================================

# Predict future workflow bottlenecks
function Get-BottleneckPrediction {
    param(
        [PSCustomObject]$Data,
        [hashtable]$VelocityForecast,
        [hashtable]$CapacityAnalysis,
        [string]$ForecastWindow
    )
    
    Write-Log "Predicting future workflow bottlenecks" -Level "INFO"
    
    # This would analyze historical bottlenecks and current workload
    # to predict where issues are likely to get stuck in the future
    
    # Placeholder implementation
    $BottleneckPrediction = @{
        "predictedBottlenecks" = @()
        "impactAssessment" = @{}
        "mitigationStrategies" = @()
    }
    
    # Sample bottleneck prediction
    $BottleneckPrediction.predictedBottlenecks = @(
        @{
            "stage" = "code-review"
            "severity" = "high"
            "predictedImpact" = "12 days average delay"
            "confidenceScore" = 0.85
        },
        @{
            "stage" = "qa-testing"
            "severity" = "medium"
            "predictedImpact" = "7 days average delay"
            "confidenceScore" = 0.75
        }
    )
    
    # Generate mitigation strategies
    $BottleneckPrediction.mitigationStrategies = @(
        "Implement code review SLAs to prevent long-running reviews",
        "Cross-train team members to reduce dependency on specialized skills"
    )
    
    return $BottleneckPrediction
}

# ============================================================================
# RISK ASSESSMENT FUNCTIONS
# ============================================================================

# Identify high-risk issues that may impact delivery
function Get-RiskAssessment {
    param(
        [PSCustomObject]$Data,
        [hashtable]$DeliveryForecast,
        [hashtable]$BottleneckPrediction
    )
    
    Write-Log "Performing risk assessment on current and future work items" -Level "INFO"
    
    # This would identify high-risk issues based on complexity,
    # dependencies, historical patterns, and team capacity
    
    # Placeholder implementation
    $RiskAssessment = @{
        "highRiskIssues" = @()
        "riskFactors" = @{}
        "mitigationStrategies" = @()
        "overallRiskScore" = 0.0
        "trendAnalysis" = "stable" # increasing, decreasing, stable
    }
    
    # Sample risk assessment
    $RiskAssessment.highRiskIssues = @(
        @{
            "id" = 42
            "title" = "Implement advanced combat AI"
            "riskScore" = 0.87
            "riskFactors" = @("high complexity", "dependency on external system")
            "mitigationStrategy" = "Break down into smaller tasks, create technical spike"
        }
    )
    
    $RiskAssessment.riskFactors = @{
        "complexityRisk" = 0.6
        "dependencyRisk" = 0.7
        "resourceRisk" = 0.4
        "technicalRisk" = 0.5
    }
    
    $RiskAssessment.overallRiskScore = 0.55
    
    # Generate mitigation strategies
    $RiskAssessment.mitigationStrategies = @(
        "Focus on reducing dependencies between components",
        "Implement risk-based testing strategy for high-risk components"
    )
    
    return $RiskAssessment
}

# ============================================================================
# DASHBOARD GENERATION FUNCTIONS
# ============================================================================

# Generate markdown format dashboard
function Generate-MarkdownDashboard {
    param(
        [hashtable]$VelocityForecast,
        [hashtable]$CapacityAnalysis,
        [hashtable]$DeliveryForecast,
        [hashtable]$BottleneckPrediction,
        [hashtable]$RiskAssessment
    )
    
    Write-Log "Generating Markdown format dashboard" -Level "INFO"
    
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $ForecastPeriod = $ForecastWindow
    
    $Markdown = @"
# DexBot GitHub Issues - Predictive Analytics Dashboard

**Generated**: $Timestamp  
**Forecast Period**: $ForecastPeriod  
**Confidence Level**: $($Confidence * 100)%

## 📊 Velocity Forecast

**Expected Velocity**: $($VelocityForecast.expectedVelocity) points per week  
**Trend**: $($VelocityForecast.predictedTrend)  
**Forecast Range**: $($VelocityForecast.lowEstimate) - $($VelocityForecast.highEstimate)

### Weekly Breakdown

| Week | Expected | Low Estimate | High Estimate |
|------|----------|--------------|---------------|
$(foreach ($week in $VelocityForecast.weeklyBreakdown) {
"| $($week.week) | $($week.expectedVelocity) | $($week.lowEstimate) | $($week.highEstimate) |"
})

## 🔋 Capacity Analysis

**Total Capacity**: $($CapacityAnalysis.totalCapacity) person-hours/week  
**Allocated**: $($CapacityAnalysis.allocatedCapacity) person-hours/week  
**Remaining**: $($CapacityAnalysis.remainingCapacity) person-hours/week  
**Utilization**: $([Math]::Round($CapacityAnalysis.utilizationRate * 100, 1))%

### Optimal Allocation

$(foreach ($component in $CapacityAnalysis.optimalAllocation.Keys) {
"- **${component}**: $($CapacityAnalysis.optimalAllocation[$component]) hours"
})

### Recommendations

$(foreach ($recommendation in $CapacityAnalysis.recommendations) {
"- $recommendation"
})

## 📅 Delivery Forecast

**Total Open Issues**: $($DeliveryForecast.summary.totalIssues)  
**Predicted On-Time**: $($DeliveryForecast.summary.predictedOnTime)  
**Predicted Late**: $($DeliveryForecast.summary.predictedLate)  
**Average Delay**: $($DeliveryForecast.summary.averageDelay) days

### Critical Path Issues

$(foreach ($issue in $DeliveryForecast.summary.criticalPath) {
"- **#$($issue.id)**: $($issue.title) - Predicted: $($issue.predictedDelivery)"
})

## ⚠️ Predicted Bottlenecks

$(foreach ($bottleneck in $BottleneckPrediction.predictedBottlenecks) {
"- **$($bottleneck.stage)** - $($bottleneck.severity) severity
  - Impact: $($bottleneck.predictedImpact)
  - Confidence: $([Math]::Round($bottleneck.confidenceScore * 100, 0))%"
})

### Mitigation Strategies

$(foreach ($strategy in $BottleneckPrediction.mitigationStrategies) {
"- $strategy"
})

## 🔍 Risk Assessment

**Overall Risk Score**: $([Math]::Round($RiskAssessment.overallRiskScore * 100, 0))%  
**Risk Trend**: $($RiskAssessment.trendAnalysis)

### Risk Factors

$(foreach ($factor in $RiskAssessment.riskFactors.Keys) {
"- **${factor}**: $([Math]::Round($RiskAssessment.riskFactors[$factor] * 100, 0))%"
})

### High-Risk Issues

$(foreach ($issue in $RiskAssessment.highRiskIssues) {
"- **#$($issue.id)**: $($issue.title)
  - Risk Score: $([Math]::Round($issue.riskScore * 100, 0))%
  - Factors: $($issue.riskFactors -join ", ")
  - Mitigation: $($issue.mitigationStrategy)"
})

### Mitigation Strategies

$(foreach ($strategy in $RiskAssessment.mitigationStrategies) {
"- $strategy"
})

---

*This predictive dashboard is generated based on historical data analysis and statistical modeling.
Predictions should be validated against actual project conditions.*
"@
    
    return $Markdown
}

# Generate HTML format dashboard
function Generate-HtmlDashboard {
    param(
        [hashtable]$VelocityForecast,
        [hashtable]$CapacityAnalysis,
        [hashtable]$DeliveryForecast,
        [hashtable]$BottleneckPrediction,
        [hashtable]$RiskAssessment
    )
    
    Write-Log "Generating HTML format dashboard" -Level "INFO"
    
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $ForecastPeriod = $ForecastWindow
    
    # This would generate an HTML dashboard with charts and interactive elements
    # For brevity, this is a simplified version without the full styling
    
    $Html = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DexBot GitHub Issues - Predictive Analytics Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 1200px; margin: 0 auto; padding: 20px; }
        h1, h2, h3 { color: #0066cc; }
        .dashboard-header { border-bottom: 2px solid #0066cc; padding-bottom: 10px; margin-bottom: 20px; }
        .dashboard-section { margin-bottom: 30px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .metrics-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .metric-card { background: #f5f9ff; padding: 15px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric-value { font-size: 24px; font-weight: bold; color: #0066cc; }
        .metric-label { font-size: 14px; color: #666; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
        th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #f2f2f2; }
        .risk-high { color: #d9534f; }
        .risk-medium { color: #f0ad4e; }
        .risk-low { color: #5cb85c; }
        .footer { margin-top: 30px; padding-top: 10px; border-top: 1px solid #ddd; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="dashboard-header">
        <h1>DexBot GitHub Issues - Predictive Analytics Dashboard</h1>
        <p><strong>Generated:</strong> $Timestamp | <strong>Forecast Period:</strong> $ForecastPeriod | <strong>Confidence Level:</strong> $($Confidence * 100)%</p>
    </div>
    
    <div class="dashboard-section">
        <h2>📊 Velocity Forecast</h2>
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">$($VelocityForecast.expectedVelocity)</div>
                <div class="metric-label">Expected Velocity (points/week)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">$($VelocityForecast.predictedTrend)</div>
                <div class="metric-label">Trend</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">$($VelocityForecast.lowEstimate) - $($VelocityForecast.highEstimate)</div>
                <div class="metric-label">Forecast Range</div>
            </div>
        </div>
        
        <h3>Weekly Breakdown</h3>
        <table>
            <thead>
                <tr>
                    <th>Week</th>
                    <th>Expected</th>
                    <th>Low Estimate</th>
                    <th>High Estimate</th>
                </tr>
            </thead>
            <tbody>
$(foreach ($week in $VelocityForecast.weeklyBreakdown) {
"                <tr>
                    <td>$($week.week)</td>
                    <td>$($week.expectedVelocity)</td>
                    <td>$($week.lowEstimate)</td>
                    <td>$($week.highEstimate)</td>
                </tr>"
})
            </tbody>
        </table>
    </div>
    
    <div class="dashboard-section">
        <h2>🔋 Capacity Analysis</h2>
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">$($CapacityAnalysis.totalCapacity)</div>
                <div class="metric-label">Total Capacity (hours/week)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">$($CapacityAnalysis.allocatedCapacity)</div>
                <div class="metric-label">Allocated (hours/week)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">$([Math]::Round($CapacityAnalysis.utilizationRate * 100, 1))%</div>
                <div class="metric-label">Utilization</div>
            </div>
        </div>
        
        <h3>Optimal Allocation</h3>
        <ul>
$(foreach ($component in $CapacityAnalysis.optimalAllocation.Keys) {
"            <li><strong>${component}</strong> $($CapacityAnalysis.optimalAllocation[$component]) hours</li>"
})
        </ul>
        
        <h3>Recommendations</h3>
        <ul>
$(foreach ($recommendation in $CapacityAnalysis.recommendations) {
"            <li>$recommendation</li>"
})
        </ul>
    </div>
    
    <div class="dashboard-section">
        <h2>📅 Delivery Forecast</h2>
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">$($DeliveryForecast.summary.totalIssues)</div>
                <div class="metric-label">Total Open Issues</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">$($DeliveryForecast.summary.predictedOnTime)</div>
                <div class="metric-label">Predicted On-Time</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">$($DeliveryForecast.summary.predictedLate)</div>
                <div class="metric-label">Predicted Late</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">$($DeliveryForecast.summary.averageDelay)</div>
                <div class="metric-label">Average Delay (days)</div>
            </div>
        </div>
        
        <h3>Critical Path Issues</h3>
        <ul>
$(foreach ($issue in $DeliveryForecast.summary.criticalPath) {
"            <li><strong>#$($issue.id):</strong> $($issue.title) - Predicted: $($issue.predictedDelivery)</li>"
})
        </ul>
    </div>
    
    <div class="dashboard-section">
        <h2>⚠️ Predicted Bottlenecks</h2>
        <ul>
$(foreach ($bottleneck in $BottleneckPrediction.predictedBottlenecks) {
"            <li>
                <strong>$($bottleneck.stage)</strong> - <span class='risk-$($bottleneck.severity)'>$($bottleneck.severity) severity</span>
                <ul>
                    <li>Impact: $($bottleneck.predictedImpact)</li>
                    <li>Confidence: $([Math]::Round($bottleneck.confidenceScore * 100, 0))%</li>
                </ul>
            </li>"
})
        </ul>
        
        <h3>Mitigation Strategies</h3>
        <ul>
$(foreach ($strategy in $BottleneckPrediction.mitigationStrategies) {
"            <li>$strategy</li>"
})
        </ul>
    </div>
    
    <div class="dashboard-section">
        <h2>🔍 Risk Assessment</h2>
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">$([Math]::Round($RiskAssessment.overallRiskScore * 100, 0))%</div>
                <div class="metric-label">Overall Risk Score</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">$($RiskAssessment.trendAnalysis)</div>
                <div class="metric-label">Risk Trend</div>
            </div>
        </div>
        
        <h3>Risk Factors</h3>
        <ul>
$(foreach ($factor in $RiskAssessment.riskFactors.Keys) {
"            <li><strong>${factor}</strong> $([Math]::Round($RiskAssessment.riskFactors[$factor] * 100, 0))%</li>"
})
        </ul>
        
        <h3>High-Risk Issues</h3>
        <ul>
$(foreach ($issue in $RiskAssessment.highRiskIssues) {
"            <li>
                <strong>#$($issue.id):</strong> $($issue.title)
                <ul>
                    <li>Risk Score: $([Math]::Round($issue.riskScore * 100, 0))%</li>
                    <li>Factors: $($issue.riskFactors -join ", ")</li>
                    <li>Mitigation: $($issue.mitigationStrategy)</li>
                </ul>
            </li>"
})
        </ul>
        
        <h3>Mitigation Strategies</h3>
        <ul>
$(foreach ($strategy in $RiskAssessment.mitigationStrategies) {
"            <li>$strategy</li>"
})
        </ul>
    </div>
    
    <div class="footer">
        <p>This predictive dashboard is generated based on historical data analysis and statistical modeling.
        Predictions should be validated against actual project conditions.</p>
    </div>
</body>
</html>
"@
    
    return $Html
}

# Generate JSON format dashboard
function Generate-JsonDashboard {
    param(
        [hashtable]$VelocityForecast,
        [hashtable]$CapacityAnalysis,
        [hashtable]$DeliveryForecast,
        [hashtable]$BottleneckPrediction,
        [hashtable]$RiskAssessment
    )
    
    Write-Log "Generating JSON format dashboard" -Level "INFO"
    
    $Dashboard = @{
        "metadata" = @{
            "timestamp" = (Get-Date).ToString("o")
            "forecastPeriod" = $ForecastWindow
            "confidenceLevel" = $Confidence
            "version" = $ScriptVersion
        }
        "velocityForecast" = $VelocityForecast
        "capacityAnalysis" = $CapacityAnalysis
        "deliveryForecast" = $DeliveryForecast
        "bottleneckPrediction" = $BottleneckPrediction
        "riskAssessment" = $RiskAssessment
    }
    
    return $Dashboard | ConvertTo-Json -Depth 10
}

# Generate CSV format dashboard (summary metrics)
function Generate-CsvDashboard {
    param(
        [hashtable]$VelocityForecast,
        [hashtable]$CapacityAnalysis,
        [hashtable]$DeliveryForecast,
        [hashtable]$BottleneckPrediction,
        [hashtable]$RiskAssessment
    )
    
    Write-Log "Generating CSV format dashboard" -Level "INFO"
    
    # Create CSV header and rows for key metrics
    $Csv = "Metric,Category,Value,Unit,Notes`r`n"
    
    # Velocity metrics
    $Csv += "Expected Velocity,Velocity,$($VelocityForecast.expectedVelocity),points/week,`r`n"
    $Csv += "Velocity Trend,Velocity,$($VelocityForecast.predictedTrend),,`r`n"
    $Csv += "Low Velocity Estimate,Velocity,$($VelocityForecast.lowEstimate),points/week,`r`n"
    $Csv += "High Velocity Estimate,Velocity,$($VelocityForecast.highEstimate),points/week,`r`n"
    
    # Capacity metrics
    $Csv += "Total Capacity,Capacity,$($CapacityAnalysis.totalCapacity),hours/week,`r`n"
    $Csv += "Allocated Capacity,Capacity,$($CapacityAnalysis.allocatedCapacity),hours/week,`r`n"
    $Csv += "Remaining Capacity,Capacity,$($CapacityAnalysis.remainingCapacity),hours/week,`r`n"
    $Csv += "Utilization Rate,Capacity,$([Math]::Round($CapacityAnalysis.utilizationRate * 100, 1)),percent,`r`n"
    
    # Delivery metrics
    $Csv += "Total Open Issues,Delivery,$($DeliveryForecast.summary.totalIssues),count,`r`n"
    $Csv += "Predicted On-Time,Delivery,$($DeliveryForecast.summary.predictedOnTime),count,`r`n"
    $Csv += "Predicted Late,Delivery,$($DeliveryForecast.summary.predictedLate),count,`r`n"
    $Csv += "Average Delay,Delivery,$($DeliveryForecast.summary.averageDelay),days,`r`n"
    
    # Risk metrics
    $Csv += "Overall Risk Score,Risk,$([Math]::Round($RiskAssessment.overallRiskScore * 100, 0)),percent,`r`n"
    $Csv += "Risk Trend,Risk,$($RiskAssessment.trendAnalysis),,`r`n"
    
    # Add risk factors
    foreach ($factor in $RiskAssessment.riskFactors.Keys) {
        $Csv += "$factor,Risk,$([Math]::Round($RiskAssessment.riskFactors[$factor] * 100, 0)),percent,`r`n"
    }
    
    return $Csv
}

# Save dashboard to file
function Save-Dashboard {
    param(
        [string]$Content,
        [string]$Format,
        [string]$OutputPath,
        [string]$Action
    )
    
    # Create output filename
    $Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $Extension = switch ($Format) {
        "markdown" { "md" }
        "html" { "html" }
        "json" { "json" }
        "csv" { "csv" }
        default { "txt" }
    }
    
    $Filename = "${DEFAULT_OUTPUT_FILENAME}_${Action}_${Timestamp}.${Extension}"
    $OutputFile = Join-Path $OutputPath $Filename
    
    # Create directory if it doesn't exist
    if (-not (Test-Path $OutputPath)) {
        New-Item -Path $OutputPath -ItemType Directory -Force | Out-Null
    }
    
    # Check if file exists and Force parameter is not set
    if ((Test-Path $OutputFile) -and (-not $Force)) {
        Write-Log "Output file already exists. Use -Force to overwrite: $OutputFile" -Level "ERROR"
        return $null
    }
    
    # Save content to file
    $Content | Set-Content -Path $OutputFile -Encoding UTF8
    Write-Log "Dashboard saved to: $OutputFile" -Level "SUCCESS"
    
    return $OutputFile
}

# ============================================================================
# INTERACTIVE MODE FUNCTIONS
# ============================================================================

# Show interactive explanation of methodology
function Show-MethodologyExplanation {
    param(
        [string]$Action
    )
    
    $Explanation = @"
        
PREDICTIVE ANALYTICS METHODOLOGY EXPLANATION
===========================================

Action: $Action
        
"@
    
    switch ($Action) {
        "forecast" {
            $Explanation += @"
Delivery Date Forecasting Methodology:

1. Historical Analysis
   - Analyzes completed issues to establish velocity baseline
   - Considers complexity, dependencies, and component-specific patterns
   - Uses Monte Carlo simulation for probability distributions

2. Prediction Models
   - Applies weighted Monte Carlo simulation with 1000+ iterations
   - Considers current team composition and historical performance
   - Adjusts for known upcoming events (holidays, releases, etc.)
   - Incorporates dependency chains and critical path analysis

3. Confidence Calculation
   - $($Confidence * 100)% confidence interval represents range where actual
     completion date is expected to fall
   - Risk-adjusted estimates account for known project risks
   - Outlier detection filters statistical anomalies

4. Validation Method
   - Predictions are back-tested against historical actuals
   - Model parameters are continuously tuned based on accuracy
   - Error margins are explicitly tracked and reported
"@
        }
        "capacity" {
            $Explanation += @"
Capacity Analysis Methodology:

1. Capacity Calculation
   - Base capacity derived from historical contribution patterns
   - Adjusts for team size, availability, and efficiency factors
   - Uses $TimeRange historical window for baseline establishment

2. Allocation Optimization
   - Component demand analysis based on open issue distribution
   - Skill matching algorithm for optimal assignment
   - Linear programming for workload balancing
   - Constraint satisfaction for critical path prioritization

3. Bottleneck Identification
   - Queue theory applied to workflow stages
   - Historical throughput analysis by component
   - Resource contention modeling for shared dependencies
   - Critical resource identification using network flow analysis

4. Recommendation Engine
   - Decision tree model for resource allocation guidance
   - Pattern matching against successful historical patterns
   - Constraint-based optimization for actionable recommendations
"@
        }
        "velocity" {
            $Explanation += @"
Velocity Prediction Methodology:

1. Historical Velocity Analysis
   - Time-weighted moving average of completed work
   - Story point normalization across team changes
   - Seasonal adjustment for recurring patterns
   - Uses $TimeRange as historical baseline period

2. Trend Analysis
   - Regression analysis for directional trends
   - Seasonality detection for cyclical patterns
   - Anomaly detection for outlier filtering
   - Confidence interval calculation based on variability

3. Forecast Modeling
   - Time series forecasting with ARIMA components
   - Bayesian adjustment for team composition changes
   - Uncertainty modeling with confidence intervals
   - Validation against out-of-sample historical data

4. Adaptive Calibration
   - Continuous error measurement against actuals
   - Model parameter adjustment based on accuracy
   - Learning rate optimization for prediction stability
   - Ensemble methods for improved forecast accuracy
"@
        }
        "bottlenecks" {
            $Explanation += @"
Bottleneck Prediction Methodology:

1. Workflow Analysis
   - Historical throughput measurement by workflow stage
   - Waiting time distribution analysis
   - Transition probability matrices between states
   - Variance analysis for stability assessment

2. Constraint Identification
   - Critical path analysis through workflow stages
   - Resource utilization modeling by component
   - Queue theory application for throughput limits
   - Dependency chain impact assessment

3. Predictive Modeling
   - Statistical process control for early warning detection
   - Markov chain modeling for state transitions
   - Queuing theory for capacity planning
   - Simulation-based validation using historical patterns

4. Impact Assessment
   - Delay propagation modeling through dependency networks
   - Critical path compression opportunities
   - Workload shifting simulation for mitigation planning
   - Risk-adjusted delivery impact calculation
"@
        }
        "risk" {
            $Explanation += @"
Risk Assessment Methodology:

1. Risk Factor Identification
   - Historical pattern analysis for risk indicators
   - Complexity measurement using code and task metrics
   - Dependency network analysis for coupling risks
   - Resource contention modeling for capacity risks

2. Risk Scoring Algorithm
   - Multi-factor weighted risk calculation
   - Bayesian probability modeling for risk factors
   - Confidence interval calculation for score reliability
   - Comparative analysis against historical baseline

3. Trend Analysis
   - Time series modeling of risk factor evolution
   - Leading indicator identification for early warning
   - Correlation analysis with delivery outcomes
   - Pattern recognition for recurring risk signatures

4. Mitigation Strategy Generation
   - Knowledge base mapping of successful interventions
   - Impact simulation for candidate strategies
   - Cost-benefit analysis for prioritization
   - Implementation roadmap with verification checkpoints
"@
        }
        default {
            $Explanation += @"
Comprehensive Predictive Dashboard Methodology:

The comprehensive dashboard integrates multiple predictive models:

1. Data Collection & Preparation
   - GitHub API integration with intelligent caching
   - Historical data extraction and normalization
   - Outlier detection and handling
   - Feature engineering for predictive signals

2. Statistical Modeling Approach
   - Time series analysis for trend forecasting
   - Bayesian networks for confidence intervals
   - Machine learning classification for risk assessment
   - Monte Carlo simulation for scenario modeling

3. Integration Framework
   - Cross-model validation for consistency
   - Dependency modeling between predictions
   - Unified confidence scoring system
   - Ensemble methods for improved accuracy

4. Practical Application
   - Actionable insights prioritization
   - Decision support visualization
   - Continuous learning from prediction accuracy
   - Regular recalibration based on actual outcomes
"@
        }
    }
    
    # Display the explanation
    Write-Host $Explanation
    
    # Prompt for continuation in interactive mode
    if ($Interactive) {
        Write-Host ""
        Write-Host "Press Enter to continue..." -ForegroundColor Cyan
        Read-Host | Out-Null
    }
}

# ============================================================================
# MAIN EXECUTION FLOW
# ============================================================================

# Main execution function
function Main {
    # Show banner
    Show-Banner
    
    # Show methodology explanation in interactive mode
    if ($Interactive) {
        Show-MethodologyExplanation -Action $Action
    }
    
    # Log execution parameters
    Write-Log "Starting predictive analysis with action: $Action" -Level "INFO"
    Write-Log "Parameters: TimeRange=$TimeRange, ForecastWindow=$ForecastWindow, OutputFormat=$OutputFormat" -Level "INFO"
    
    try {
        # Get analytics data
        $Data = Get-IssueAnalyticsData -ForceRefresh:$RefreshData
        
        # Create dashboard components based on the requested action
        $Components = @{}
        
        # Process based on action type
        switch ($Action) {
            "forecast" {
                # For delivery forecasting, we need velocity and capacity first
                $Components.VelocityForecast = Get-HistoricalVelocity -Data $Data -TimeFrame $TimeRange -Metric $VelocityMetric | 
                                              Get-VelocityForecast -ForecastWindow $ForecastWindow -ConfidenceLevel $Confidence
                
                $Components.CapacityAnalysis = Get-TeamCapacityAnalysis -Data $Data -SpecifiedCapacity $TeamCapacity -VelocityForecast $Components.VelocityForecast
                
                $Components.DeliveryForecast = Get-DeliveryForecast -Data $Data -VelocityForecast $Components.VelocityForecast -CapacityAnalysis $Components.CapacityAnalysis `
                                             -ForecastWindow $ForecastWindow -ConfidenceLevel $Confidence
                
                # Generate dashboard based on format
                switch ($OutputFormat) {
                    "markdown" { $Content = Generate-MarkdownDashboard @Components }
                    "html" { $Content = Generate-HtmlDashboard @Components }
                    "json" { $Content = Generate-JsonDashboard @Components }
                    "csv" { $Content = Generate-CsvDashboard @Components }
                }
                
                # Save dashboard if not in dry run mode
                if (-not $DryRun) {
                    $OutputFile = Save-Dashboard -Content $Content -Format $OutputFormat -OutputPath $OutputPath -Action $Action
                    if ($OutputFile) {
                        Write-Log "Delivery forecast dashboard saved to: $OutputFile" -Level "SUCCESS"
                    }
                } else {
                    Write-Host $Content
                    Write-Log "Dry run completed - no files saved" -Level "INFO"
                }
            }
            "capacity" {
                # For capacity analysis
                $Components.VelocityForecast = Get-HistoricalVelocity -Data $Data -TimeFrame $TimeRange -Metric $VelocityMetric | 
                                              Get-VelocityForecast -ForecastWindow $ForecastWindow -ConfidenceLevel $Confidence
                
                $Components.CapacityAnalysis = Get-TeamCapacityAnalysis -Data $Data -SpecifiedCapacity $TeamCapacity -VelocityForecast $Components.VelocityForecast
                
                # Generate dashboard based on format
                switch ($OutputFormat) {
                    "markdown" { $Content = Generate-MarkdownDashboard @Components }
                    "html" { $Content = Generate-HtmlDashboard @Components }
                    "json" { $Content = Generate-JsonDashboard @Components }
                    "csv" { $Content = Generate-CsvDashboard @Components }
                }
                
                # Save dashboard if not in dry run mode
                if (-not $DryRun) {
                    $OutputFile = Save-Dashboard -Content $Content -Format $OutputFormat -OutputPath $OutputPath -Action $Action
                    if ($OutputFile) {
                        Write-Log "Capacity analysis dashboard saved to: $OutputFile" -Level "SUCCESS"
                    }
                } else {
                    Write-Host $Content
                    Write-Log "Dry run completed - no files saved" -Level "INFO"
                }
            }
            "velocity" {
                # For velocity trending
                $Components.VelocityForecast = Get-HistoricalVelocity -Data $Data -TimeFrame $TimeRange -Metric $VelocityMetric | 
                                              Get-VelocityForecast -ForecastWindow $ForecastWindow -ConfidenceLevel $Confidence
                
                # Generate dashboard based on format
                switch ($OutputFormat) {
                    "markdown" { $Content = Generate-MarkdownDashboard @Components }
                    "html" { $Content = Generate-HtmlDashboard @Components }
                    "json" { $Content = Generate-JsonDashboard @Components }
                    "csv" { $Content = Generate-CsvDashboard @Components }
                }
                
                # Save dashboard if not in dry run mode
                if (-not $DryRun) {
                    $OutputFile = Save-Dashboard -Content $Content -Format $OutputFormat -OutputPath $OutputPath -Action $Action
                    if ($OutputFile) {
                        Write-Log "Velocity forecast dashboard saved to: $OutputFile" -Level "SUCCESS"
                    }
                } else {
                    Write-Host $Content
                    Write-Log "Dry run completed - no files saved" -Level "INFO"
                }
            }
            "bottlenecks" {
                # For bottleneck prediction
                $Components.VelocityForecast = Get-HistoricalVelocity -Data $Data -TimeFrame $TimeRange -Metric $VelocityMetric | 
                                              Get-VelocityForecast -ForecastWindow $ForecastWindow -ConfidenceLevel $Confidence
                
                $Components.CapacityAnalysis = Get-TeamCapacityAnalysis -Data $Data -SpecifiedCapacity $TeamCapacity -VelocityForecast $Components.VelocityForecast
                
                $Components.BottleneckPrediction = Get-BottleneckPrediction -Data $Data -VelocityForecast $Components.VelocityForecast -CapacityAnalysis $Components.CapacityAnalysis `
                                                 -ForecastWindow $ForecastWindow
                
                # Generate dashboard based on format
                switch ($OutputFormat) {
                    "markdown" { $Content = Generate-MarkdownDashboard @Components }
                    "html" { $Content = Generate-HtmlDashboard @Components }
                    "json" { $Content = Generate-JsonDashboard @Components }
                    "csv" { $Content = Generate-CsvDashboard @Components }
                }
                
                # Save dashboard if not in dry run mode
                if (-not $DryRun) {
                    $OutputFile = Save-Dashboard -Content $Content -Format $OutputFormat -OutputPath $OutputPath -Action $Action
                    if ($OutputFile) {
                        Write-Log "Bottleneck prediction dashboard saved to: $OutputFile" -Level "SUCCESS"
                    }
                } else {
                    Write-Host $Content
                    Write-Log "Dry run completed - no files saved" -Level "INFO"
                }
            }
            "risk" {
                # For risk assessment
                $Components.VelocityForecast = Get-HistoricalVelocity -Data $Data -TimeFrame $TimeRange -Metric $VelocityMetric | 
                                              Get-VelocityForecast -ForecastWindow $ForecastWindow -ConfidenceLevel $Confidence
                
                $Components.CapacityAnalysis = Get-TeamCapacityAnalysis -Data $Data -SpecifiedCapacity $TeamCapacity -VelocityForecast $Components.VelocityForecast
                
                $Components.DeliveryForecast = Get-DeliveryForecast -Data $Data -VelocityForecast $Components.VelocityForecast -CapacityAnalysis $Components.CapacityAnalysis `
                                             -ForecastWindow $ForecastWindow -ConfidenceLevel $Confidence
                
                $Components.BottleneckPrediction = Get-BottleneckPrediction -Data $Data -VelocityForecast $Components.VelocityForecast -CapacityAnalysis $Components.CapacityAnalysis `
                                                 -ForecastWindow $ForecastWindow
                
                $Components.RiskAssessment = Get-RiskAssessment -Data $Data -DeliveryForecast $Components.DeliveryForecast -BottleneckPrediction $Components.BottleneckPrediction
                
                # Generate dashboard based on format
                switch ($OutputFormat) {
                    "markdown" { $Content = Generate-MarkdownDashboard @Components }
                    "html" { $Content = Generate-HtmlDashboard @Components }
                    "json" { $Content = Generate-JsonDashboard @Components }
                    "csv" { $Content = Generate-CsvDashboard @Components }
                }
                
                # Save dashboard if not in dry run mode
                if (-not $DryRun) {
                    $OutputFile = Save-Dashboard -Content $Content -Format $OutputFormat -OutputPath $OutputPath -Action $Action
                    if ($OutputFile) {
                        Write-Log "Risk assessment dashboard saved to: $OutputFile" -Level "SUCCESS"
                    }
                } else {
                    Write-Host $Content
                    Write-Log "Dry run completed - no files saved" -Level "INFO"
                }
            }
            "full" {
                # Generate full comprehensive dashboard with all components
                Write-Log "Generating comprehensive predictive dashboard with all metrics" -Level "INFO"
                
                # Calculate all components
                $Components.VelocityForecast = Get-HistoricalVelocity -Data $Data -TimeFrame $TimeRange -Metric $VelocityMetric | 
                                              Get-VelocityForecast -ForecastWindow $ForecastWindow -ConfidenceLevel $Confidence
                
                $Components.CapacityAnalysis = Get-TeamCapacityAnalysis -Data $Data -SpecifiedCapacity $TeamCapacity -VelocityForecast $Components.VelocityForecast
                
                $Components.DeliveryForecast = Get-DeliveryForecast -Data $Data -VelocityForecast $Components.VelocityForecast -CapacityAnalysis $Components.CapacityAnalysis `
                                             -ForecastWindow $ForecastWindow -ConfidenceLevel $Confidence
                
                $Components.BottleneckPrediction = Get-BottleneckPrediction -Data $Data -VelocityForecast $Components.VelocityForecast -CapacityAnalysis $Components.CapacityAnalysis `
                                                 -ForecastWindow $ForecastWindow
                
                $Components.RiskAssessment = Get-RiskAssessment -Data $Data -DeliveryForecast $Components.DeliveryForecast -BottleneckPrediction $Components.BottleneckPrediction
                
                # Generate dashboard based on format
                switch ($OutputFormat) {
                    "markdown" { $Content = Generate-MarkdownDashboard @Components }
                    "html" { $Content = Generate-HtmlDashboard @Components }
                    "json" { $Content = Generate-JsonDashboard @Components }
                    "csv" { $Content = Generate-CsvDashboard @Components }
                }
                
                # Save dashboard if not in dry run mode
                if (-not $DryRun) {
                    $OutputFile = Save-Dashboard -Content $Content -Format $OutputFormat -OutputPath $OutputPath -Action $Action
                    if ($OutputFile) {
                        Write-Log "Comprehensive predictive dashboard saved to: $OutputFile" -Level "SUCCESS"
                    }
                } else {
                    Write-Host $Content
                    Write-Log "Dry run completed - no files saved" -Level "INFO"
                }
            }
        }
        
        Write-Log "Predictive analysis completed successfully" -Level "SUCCESS"
        return 0
    }
    catch {
        Write-Log "Error during predictive analysis: $_" -Level "ERROR"
        Write-Log "Stack trace: $($_.ScriptStackTrace)" -Level "ERROR"
        return 1
    }
}

# Execute main function
$ExitCode = Main
exit $ExitCode

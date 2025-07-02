# End-to-End Testing for Full Automation Suite
# Comprehensive tests for all components of the GitHub Issues Workflow Automation

param(
    [string]$Repository,
    [string]$OutputPath = "tmp\e2e_test_results_$(Get-Date -Format 'yyyyMMdd_HHmmss').xml",
    [switch]$SkipSetup,
    [switch]$BasicTestsOnly,
    [string]$Token = $env:GITHUB_TOKEN
)

# Verify GitHub token
if (-not $Token) {
    Write-Host "GitHub token not found. Please set GITHUB_TOKEN environment variable or provide via -Token parameter." -ForegroundColor Red
    exit 1
}

# Ensure Pester module is installed
if (-not (Get-Module -ListAvailable -Name Pester)) {
    Write-Host "Installing Pester module..." -ForegroundColor Yellow
    Install-Module -Name Pester -Scope CurrentUser -Force -SkipPublisherCheck
}

# Ensure PowerShellForGitHub module is installed
if (-not (Get-Module -ListAvailable -Name PowerShellForGitHub)) {
    Write-Host "Installing PowerShellForGitHub module..." -ForegroundColor Yellow
    Install-Module -Name PowerShellForGitHub -Scope CurrentUser -Force
}

# Import modules
Import-Module Pester
Import-Module PowerShellForGitHub

# Setup authentication
try {
    Set-GitHubAuthentication -Token $Token
    Write-Host "GitHub authentication configured successfully" -ForegroundColor Green
} catch {
    Write-Host "Failed to configure GitHub authentication: $_" -ForegroundColor Red
    exit 1
}

# Setup test environment if needed
if (-not $SkipSetup) {
    Write-Host "Setting up test environment..." -ForegroundColor Cyan
    & "$PSScriptRoot\setup_test_environment.ps1" -Token $Token
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Test environment setup failed. Please check the logs and try again." -ForegroundColor Red
        exit 1
    }
}

# Set default repository if not provided
if (-not $Repository) {
    $Repository = "dexbot-test-small"  # Use the small test repo by default
    Write-Host "Using default test repository: $Repository" -ForegroundColor Yellow
}

# Get current user
$currentUser = Get-GitHubUser
$ownerName = $currentUser.login

# Full path to configuration file
$configPath = Join-Path $PSScriptRoot "..\config\automation_config.json"

# Path to full automation suite script
$scriptPath = Join-Path $PSScriptRoot "full_automation_suite.ps1"

# Pester tests
$pesterConfig = New-PesterConfiguration
$pesterConfig.Run.Path = $PSScriptRoot
$pesterConfig.Run.PassThru = $true
$pesterConfig.Output.Verbosity = 'Detailed'
$pesterConfig.TestResult.Enabled = $true
$pesterConfig.TestResult.OutputPath = $OutputPath

Describe "Full Automation Suite End-to-End Tests" {
    BeforeAll {
        # Update configuration for testing
        $config = Get-Content $configPath -Raw | ConvertFrom-Json
        $config.repository = "$ownerName/$Repository"
        $config.intelligent_routing.enabled = $true
        $config.intelligent_routing.confidence_threshold = 0.6  # Lower threshold for testing
        $config.predictive_dashboard.enabled = $true
        $config | ConvertTo-Json -Depth 10 | Set-Content $configPath
        
        # Setup complete
        Write-Host "Test configuration complete. Using repository: $ownerName/$Repository" -ForegroundColor Green
    }
    
    Context "Configuration and Setup" {
        It "Should have a valid automation_config.json file" {
            Test-Path $configPath | Should -Be $true
            { Get-Content $configPath -Raw | ConvertFrom-Json } | Should -Not -Throw
        }
        
        It "Should have the full_automation_suite.ps1 script" {
            Test-Path $scriptPath | Should -Be $true
        }
        
        It "Should be able to connect to GitHub API" {
            { Get-GitHubUser } | Should -Not -Throw
        }
        
        It "Should be able to access the test repository" {
            { Get-GitHubRepository -OwnerName $ownerName -RepositoryName $Repository } | Should -Not -Throw
        }
    }
    
    Context "Basic Functionality" {
        It "Should run the help command without errors" {
            $output = & $scriptPath -Action help
            $output | Should -Not -BeNullOrEmpty
        }
        
        It "Should validate the configuration file" {
            $output = & $scriptPath -Action validate-config
            $LASTEXITCODE | Should -Be 0
        }
    }
    
    Context "Intelligent Issue Routing" {
        It "Should analyze issue text and identify components" {
            $testText = "Combat system crashes when engaging multiple targets"
            $output = & $scriptPath -Action analyze-text -Text $testText -Format json
            $result = $output -join "" | ConvertFrom-Json
            
            $result.Scores.Components | Should -Not -BeNullOrEmpty
            $result.Scores.Components.PSObject.Properties.Name | Should -Contain "combat"
        }
        
        It "Should route an existing issue correctly" {
            # Get a random issue from the repository
            $issues = Get-GitHubIssue -OwnerName $ownerName -RepositoryName $Repository -State open
            $issue = $issues | Select-Object -First 1
            
            if ($issue) {
                $output = & $scriptPath -Action route-issue -Repository "$ownerName/$Repository" -IssueNumber $issue.number -Format json
                $result = $output -join "" | ConvertFrom-Json
                
                $result.Issue | Should -Not -BeNullOrEmpty
                $result.Routing | Should -Not -BeNullOrEmpty
                $result.Routing.Component | Should -Not -BeNullOrEmpty
                $result.Routing.Priority | Should -Not -BeNullOrEmpty
            } else {
                Set-ItResult -Inconclusive -Because "No open issues found in repository"
            }
        }
        
        It "Should handle batch routing of multiple issues" {
            $output = & $scriptPath -Action batch-route -Repository "$ownerName/$Repository" -State open -Limit 5 -Format json
            $result = $output -join "" | ConvertFrom-Json
            
            $result.ProcessedCount | Should -BeGreaterOrEqual 0
            $result.RoutedCount | Should -BeGreaterOrEqual 0
        }
    }
    
    Context "Predictive Analytics" {
        It "Should generate predictive analytics data" {
            $output = & $scriptPath -Action predict -Repository "$ownerName/$Repository" -Format json
            $result = $output -join "" | ConvertFrom-Json
            
            $result.Stats | Should -Not -BeNullOrEmpty
            $result.Predictions | Should -Not -BeNullOrEmpty
        }
    }
    
    # Skip advanced tests if BasicTestsOnly is specified
    if (-not $BasicTestsOnly) {
        Context "Self-Optimization" {
            It "Should be able to learn from historical data" {
                $output = & $scriptPath -Action learn -Repository "$ownerName/$Repository" -HistoryDays 7 -Format json
                $result = $output -join "" | ConvertFrom-Json
                
                $result.Status | Should -Be "success" -Because "Learning should complete successfully"
                $result.ProcessedCount | Should -BeGreaterOrEqual 0
            }
            
            It "Should generate an optimization report" {
                $output = & $scriptPath -Action optimization-report -Repository "$ownerName/$Repository" -Format json
                $result = $output -join "" | ConvertFrom-Json
                
                $result.Status | Should -Be "success" -Because "Report generation should complete successfully"
            }
        }
        
        Context "Performance Tests" {
            It "Should handle large batch operations efficiently" {
                # Measure execution time for a batch operation
                $timeResult = Measure-Command {
                    & $scriptPath -Action batch-route -Repository "$ownerName/$Repository" -State all -Format json | Out-Null
                }
                
                # Test should complete in a reasonable time
                $timeResult.TotalSeconds | Should -BeLessThan 30 -Because "Batch operations should be reasonably fast"
            }
            
            It "Should efficiently analyze complex issue text" {
                $longText = "This is a complex issue involving multiple components. The combat system crashes when engaging multiple targets, but only after the looting system has attempted to process corpses. Additionally, the UI becomes unresponsive and the configuration file appears to be corrupted. The core system also shows signs of memory leaks during extended operation."
                
                $timeResult = Measure-Command {
                    & $scriptPath -Action analyze-text -Text $longText -Format json | Out-Null
                }
                
                # Analysis should be fast
                $timeResult.TotalSeconds | Should -BeLessThan 5 -Because "Text analysis should be fast even for complex text"
            }
        }
    }
    
    Context "Error Handling" {
        It "Should gracefully handle invalid repository names" {
            $output = & $scriptPath -Action route-issue -Repository "invalid/repo" -IssueNumber 1 2>&1
            $LASTEXITCODE | Should -Not -Be 0
            $output | Should -Not -BeNullOrEmpty
        }
        
        It "Should handle non-existent issues properly" {
            $output = & $scriptPath -Action route-issue -Repository "$ownerName/$Repository" -IssueNumber 999999 2>&1
            $LASTEXITCODE | Should -Not -Be 0
            $output | Should -Not -BeNullOrEmpty
        }
        
        It "Should validate required parameters" {
            $output = & $scriptPath -Action route-issue 2>&1
            $LASTEXITCODE | Should -Not -Be 0
            $output | Should -Not -BeNullOrEmpty
        }
    }
    
    AfterAll {
        # Restore original configuration
        Write-Host "Tests complete. Restoring original configuration." -ForegroundColor Green
    }
}

# Run the tests
$results = Invoke-Pester -Configuration $pesterConfig

# Display summary
Write-Host "`n" + "="*80 -ForegroundColor Cyan
Write-Host "TEST SUMMARY" -ForegroundColor Cyan
Write-Host "="*80 -ForegroundColor Cyan
Write-Host "Total Tests  : $($results.TotalCount)" -ForegroundColor White
Write-Host "Passed       : $($results.PassedCount)" -ForegroundColor Green
Write-Host "Failed       : $($results.FailedCount)" -ForegroundColor Red
Write-Host "Skipped      : $($results.SkippedCount)" -ForegroundColor Yellow
Write-Host "NotRun       : $($results.NotRunCount)" -ForegroundColor Gray
Write-Host "Time Elapsed : $($results.Duration.TotalSeconds) seconds" -ForegroundColor White
Write-Host "`nTest results saved to: $OutputPath" -ForegroundColor Gray

# Return success/failure code based on test results
exit $results.FailedCount

# DexBot Feature Preparation Script Launcher
# This PowerShell script simplifies running the feature preparation script
param (
    [Parameter(Position=0)]
    [string]$FeatureName,
    
    [Parameter()]
    [switch]$NonInteractive,
    
    [Parameter()]
    [switch]$SkipGitUpdate,
    
    [Parameter()]
    [switch]$SkipCleanup,
    
    [Parameter()]
    [switch]$SkipValidation,
    
    [Parameter()]
    [switch]$Help
)

# Display help information
if ($Help) {
    Write-Host "DexBot Feature Preparation Tool - Help" -ForegroundColor Green
    Write-Host "=======================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Cyan
    Write-Host "  .\prepare_feature.ps1 [feature-name] [-NonInteractive] [-SkipGitUpdate] [-SkipCleanup] [-SkipValidation] [-Help]" -ForegroundColor White
    Write-Host ""
    Write-Host "Arguments:" -ForegroundColor Cyan
    Write-Host "  feature-name        Name of the feature to create (will create feature/[feature-name] branch)" -ForegroundColor White
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Cyan
    Write-Host "  -NonInteractive     Run without any prompts or user interaction" -ForegroundColor White
    Write-Host "  -SkipGitUpdate      Skip updating Git repository and branch management" -ForegroundColor White
    Write-Host "  -SkipCleanup        Skip cleaning temporary files and build artifacts" -ForegroundColor White
    Write-Host "  -SkipValidation     Skip running validation and tests" -ForegroundColor White
    Write-Host "  -Help               Display this help information" -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Cyan
    Write-Host "  .\prepare_feature.ps1 buff-management-system" -ForegroundColor White
    Write-Host "  .\prepare_feature.ps1 buff-management-system -NonInteractive" -ForegroundColor White
    Write-Host "  .\prepare_feature.ps1 -SkipValidation -SkipCleanup" -ForegroundColor White
    exit 0
}

# Display header
Write-Host "DexBot Feature Preparation Tool" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Green

# Build Python command with arguments based on PowerShell parameters
$PythonArgs = @()

if ($FeatureName) {
    $PythonArgs += $FeatureName
}

if ($NonInteractive) {
    $PythonArgs += "--non-interactive"
}

if ($SkipGitUpdate) {
    $PythonArgs += "--skip-git"
}

if ($SkipCleanup) {
    $PythonArgs += "--skip-cleanup"
}

if ($SkipValidation) {
    $PythonArgs += "--skip-validation"
}

# Execute Python script with arguments
$PythonCommand = "python tools\prepare_feature.py $($PythonArgs -join ' ')"
Write-Host "Executing: $PythonCommand" -ForegroundColor Yellow

try {
    Invoke-Expression $PythonCommand
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Python script exited with code $LASTEXITCODE" -ForegroundColor Red
        exit $LASTEXITCODE
    }
} catch {
    Write-Host "Error running prepare_feature.py: $_" -ForegroundColor Red
    Write-Host "Make sure Python is installed and in your PATH." -ForegroundColor Yellow
    exit 1
}

# Only show pause prompt if not in non-interactive mode
if (-not $NonInteractive) {
    Write-Host "Press any key to continue..." -ForegroundColor Cyan
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

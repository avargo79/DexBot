#!/usr/bin/env powershell

# DexBot Developer Tools - PowerShell Script
# Provides automated commands for linting, testing, building, and bundling DexBot

param(
    [Parameter(Position=0)]
    [string]$Command = ""
)

function Write-Info($message) {
    Write-Host "[INFO] $message" -ForegroundColor Blue
}

function Write-Success($message) {
    Write-Host "[SUCCESS] $message" -ForegroundColor Green
}

function Write-Warning($message) {
    Write-Host "[WARNING] $message" -ForegroundColor Yellow
}

function Write-Error($message) {
    Write-Host "[ERROR] $message" -ForegroundColor Red
}

function Test-Python {
    try {
        $pythonVersion = python --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Python found: $pythonVersion"
            return $true
        }
    }
    catch {}
    
    Write-Error "Python is not installed or not in PATH"
    return $false
}

function Test-Invoke {
    Write-Info "Checking invoke..."
    
    try {
        python -c "import invoke" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Success "invoke is available"
            return $true  
        }
    }
    catch {}
    
    Write-Warning "invoke not found. Installing..."
    try {
        python -m pip install invoke
        if ($LASTEXITCODE -eq 0) {
            Write-Success "invoke installed successfully"
            return $true
        }
    }
    catch {}
    
    return $false
}

function Invoke-Lint {
    Write-Info "Running code linting..."
    
    try {
        python -m invoke lint
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Linting completed successfully"
            return $true
        }
        else {
            Write-Error "Linting failed"
            return $false
        }
    }
    catch {
        Write-Error "Error running lint command"
        return $false
    }
}

function Invoke-Test {
    Write-Info "Running tests..."
    
    try {
        python -m invoke test
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Tests completed successfully"
            return $true
        }
        else {
            Write-Warning "Tests completed with issues"
            return $true
        }
    }
    catch {
        Write-Error "Error running test command"
        return $false
    }
}

function Invoke-Build {
    Write-Info "Building project..."
    
    try {
        python -m invoke build
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Build completed successfully"
            return $true
        }
        else {
            Write-Error "Build failed"
            return $false  
        }
    }
    catch {
        Write-Error "Error running build command"
        return $false
    }
}

function Invoke-Bundle {
    Write-Info "Creating bundle..."
    
    try {
        python -m invoke bundle
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Bundle created successfully"
            if (Test-Path "dist/DexBot.py") {
                $bundleSize = (Get-Item "dist/DexBot.py").Length
                Write-Info "Bundle size: $([math]::Round($bundleSize/1024, 2)) KB"
            }
            return $true
        }
        else {
            Write-Error "Bundle creation failed"
            return $false
        }
    }
    catch {
        Write-Error "Error running bundle command"
        return $false
    }
}

function Invoke-All {
    Write-Info "Running full development pipeline..."
    Write-Host ""
    
    $success = $true
    
    if (-not (Invoke-Lint)) { $success = $false }
    Write-Host ""
    
    if (-not (Invoke-Test)) { $success = $false }
    Write-Host ""
    
    if (-not (Invoke-Build)) { $success = $false }
    Write-Host ""
    
    if (-not (Invoke-Bundle)) { $success = $false }
    Write-Host ""
    
    if ($success) {
        Write-Success "All tasks completed successfully!"
    }
    else {
        Write-Error "Some tasks failed"
        exit 1
    }
}

function Show-Help {
    Write-Host "DexBot Developer Tools - PowerShell Version"
    Write-Host "Usage: .\dev-tools.ps1 <command>"
    Write-Host ""
    Write-Host "Available commands:"
    Write-Host "  lint    - Run code linting"
    Write-Host "  test    - Run test suite"
    Write-Host "  build   - Build/validate project"
    Write-Host "  bundle  - Create deployment bundle"
    Write-Host "  all     - Run all commands"
    Write-Host "  help    - Show this help"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\dev-tools.ps1 lint"
    Write-Host "  .\dev-tools.ps1 all"
}

function Main {
    if ([string]::IsNullOrEmpty($Command)) {
        Show-Help
        exit 1
    }
    
    if (-not (Test-Python)) {
        exit 1
    }
    
    if (-not (Test-Invoke)) {
        exit 1
    }
    
    switch ($Command.ToLower()) {
        "lint" { if (-not (Invoke-Lint)) { exit 1 } }
        "test" { if (-not (Invoke-Test)) { exit 1 } }
        "build" { if (-not (Invoke-Build)) { exit 1 } }  
        "bundle" { if (-not (Invoke-Bundle)) { exit 1 } }
        "all" { Invoke-All }
        { $_ -in @("help", "-h", "--help") } { Show-Help }
        default {
            Write-Error "Unknown command: $Command"
            Show-Help
            exit 1
        }
    }
    
    Write-Host ""
    Write-Success "Done!"
}

$ErrorActionPreference = "Stop"
Main

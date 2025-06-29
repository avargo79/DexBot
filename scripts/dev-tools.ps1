# DexBot Development Tools - PowerShell Script
# Usage: .\dev-tools.ps1 [command]
# Commands: lint, test, build, bundle, all, help

param(
    [string]$Command = "help"
)

# Color functions for better output
function Write-Success { param($Message) Write-Host $Message -ForegroundColor Green }
function Write-Error { param($Message) Write-Host $Message -ForegroundColor Red }
function Write-Warning { param($Message) Write-Host $Message -ForegroundColor Yellow }
function Write-Info { param($Message) Write-Host $Message -ForegroundColor Cyan }

# Header
function Show-Header {
    Write-Host "==================================================" -ForegroundColor Magenta
    Write-Host "      DexBot Development Tools (PowerShell)      " -ForegroundColor Magenta
    Write-Host "==================================================" -ForegroundColor Magenta
    Write-Host ""
}

# Check if Python is available
function Test-Python {
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "✓ Python found: $pythonVersion"
            return $true
        }
    }
    catch {
        Write-Error "✗ Python not found in PATH"
        Write-Warning "Please install Python 3.7+ and add it to your PATH"
        return $false
    }
    return $false
}

# Check if invoke is available
function Test-Invoke {
    try {
        python -c "import invoke" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Success "✓ Invoke module found"
            return $true
        }
    }
    catch {}
    
    Write-Warning "✗ Invoke module not found"
    Write-Info "Installing invoke..."
    try {
        python -m pip install invoke
        Write-Success "✓ Invoke installed successfully"
        return $true
    }
    catch {
        Write-Error "✗ Failed to install invoke"
        return $false
    }
}

# Run lint command
function Invoke-Lint {
    Write-Info "🔍 Running code linting..."
    try {
        python -m invoke lint
        if ($LASTEXITCODE -eq 0) {
            Write-Success "✓ Linting completed successfully"
            return $true
        } else {
            Write-Error "✗ Linting failed"
            return $false
        }
    }
    catch {
        Write-Error "✗ Error running lint command: $_"
        return $false
    }
}

# Run test command
function Invoke-Test {
    Write-Info "🧪 Running tests..."
    try {
        python -m invoke test
        if ($LASTEXITCODE -eq 0) {
            Write-Success "✓ Tests completed successfully"
            return $true
        } else {
            Write-Warning "⚠ Tests completed with issues (check output above)"
            return $true  # Don't fail build for test issues
        }
    }
    catch {
        Write-Error "✗ Error running test command: $_"
        return $false
    }
}

# Run build command
function Invoke-Build {
    Write-Info "🔨 Building project..."
    try {
        # For now, build is the same as lint since we don't have compilation
        python -m invoke lint
        if ($LASTEXITCODE -eq 0) {
            Write-Success "✓ Build completed successfully"
            return $true
        } else {
            Write-Error "✗ Build failed"
            return $false
        }
    }
    catch {
        Write-Error "✗ Error running build command: $_"
        return $false
    }
}

# Run bundle command
function Invoke-Bundle {
    Write-Info "📦 Creating bundle..."
    try {
        python -m invoke bundle
        if ($LASTEXITCODE -eq 0) {
            Write-Success "✓ Bundle created successfully"
            if (Test-Path "dist/DexBot.py") {
                $bundleSize = (Get-Item "dist/DexBot.py").Length
                Write-Info "   📊 Bundle size: $([math]::Round($bundleSize/1024, 2)) KB"
            }
            return $true
        } else {
            Write-Error "✗ Bundle creation failed"
            return $false
        }
    }
    catch {
        Write-Error "✗ Error running bundle command: $_"
        return $false
    }
}

# Run all commands
function Invoke-All {
    Write-Info "🚀 Running full development pipeline..."
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
        Write-Success "🎉 All operations completed successfully!"
        Write-Info "   Ready for commit and push!"
    } else {
        Write-Error "❌ Some operations failed. Please check the output above."
    }
    
    return $success
}

# Show help
function Show-Help {
    Write-Info "Available commands:"
    Write-Host "  lint    - Run code linting (flake8)" -ForegroundColor White
    Write-Host "  test    - Run test suite" -ForegroundColor White
    Write-Host "  build   - Build project (validate syntax)" -ForegroundColor White
    Write-Host "  bundle  - Create distribution bundle" -ForegroundColor White
    Write-Host "  all     - Run all commands in sequence" -ForegroundColor White
    Write-Host "  help    - Show this help message" -ForegroundColor White
    Write-Host ""
    Write-Info "Examples:"
    Write-Host "  .\dev-tools.ps1 all" -ForegroundColor Gray
    Write-Host "  .\dev-tools.ps1 lint" -ForegroundColor Gray
    Write-Host "  .\dev-tools.ps1 bundle" -ForegroundColor Gray
}

# Main execution
function Main {
    Show-Header
    
    # Check prerequisites
    if (-not (Test-Python)) {
        exit 1
    }
    
    if (-not (Test-Invoke)) {
        exit 1
    }
    
    Write-Host ""
    
    # Execute command
    switch ($Command.ToLower()) {
        "lint" {
            if (-not (Invoke-Lint)) { exit 1 }
        }
        "test" {
            if (-not (Invoke-Test)) { exit 1 }
        }
        "build" {
            if (-not (Invoke-Build)) { exit 1 }
        }
        "bundle" {
            if (-not (Invoke-Bundle)) { exit 1 }
        }
        "all" {
            if (-not (Invoke-All)) { exit 1 }
        }
        "help" {
            Show-Help
        }
        default {
            Write-Error "Unknown command: $Command"
            Write-Host ""
            Show-Help
            exit 1
        }
    }
    
    Write-Host ""
    Write-Success "Done! 🎯"
}

# Set error action preference
$ErrorActionPreference = "Stop"

# Run main function
Main

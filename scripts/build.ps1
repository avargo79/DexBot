# DexBot Build Script - PowerShell
# Runs the complete build pipeline: clean, lint, test, and bundle

Write-Host "DexBot Build Script" -ForegroundColor Cyan
Write-Host "===================" -ForegroundColor Cyan

function Write-Info($message) {
    Write-Host "[INFO] $message" -ForegroundColor Blue
}

function Write-Success($message) {
    Write-Host "[SUCCESS] $message" -ForegroundColor Green
}

function Write-Error($message) {
    Write-Host "[ERROR] $message" -ForegroundColor Red
}

# Check prerequisites
Write-Info "Checking prerequisites..."

# Check Python
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Python found: $pythonVersion"
    } else {
        Write-Error "Python is not installed or not in PATH"
        Write-Host "Please install Python 3.7+" -ForegroundColor Yellow
        exit 1
    }
}
catch {
    Write-Error "Python is not installed or not in PATH"
    Write-Host "Please install Python 3.7+" -ForegroundColor Yellow
    exit 1
}

# Check/Install invoke
try {
    python -c "import invoke" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Success "invoke is available"
    } else {
        Write-Info "Installing invoke..."
        python -m pip install invoke
        if ($LASTEXITCODE -eq 0) {
            Write-Success "invoke installed successfully"
        } else {
            Write-Error "Failed to install invoke"
            exit 1
        }
    }
}
catch {
    Write-Error "Error checking invoke"
    exit 1
}

# Run build
Write-Info "Running full build pipeline..."
Write-Host ""

try {
    python -m invoke build
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Success "Build completed successfully!"
        Write-Success "Bundled script available at: dist/DexBot.py"
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "  1. Copy dist/DexBot.py to your RazorEnhanced Scripts folder" -ForegroundColor White
        Write-Host "  2. Run the script in RazorEnhanced" -ForegroundColor White
        Write-Host ""
        Write-Host "Optional:" -ForegroundColor Cyan
        Write-Host "  - Update API docs: python scripts/update_api_docs.py" -ForegroundColor White
        exit 0
    } else {
        Write-Host ""
        Write-Error "Build failed"
        Write-Host "Try running individual tasks: python -m invoke lint, python -m invoke test" -ForegroundColor Yellow
        exit 1
    }
}
catch {
    Write-Host ""
    Write-Error "Error running build command"
    exit 1
}

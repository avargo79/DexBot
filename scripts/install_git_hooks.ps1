# Install Git Hooks for AI Validation Enforcement
# This script sets up git hooks that enforce AI validation requirements

Write-Host "Installing AI Validation Git Hooks..." -ForegroundColor Green

# Create .git/hooks directory if it doesn't exist
$hooksDir = ".git\hooks"
if (-not (Test-Path $hooksDir)) {
    New-Item -ItemType Directory -Path $hooksDir -Force
}

# Pre-push hook to prevent direct main pushes
$prePushHook = @"
#!/bin/sh
# Pre-push hook to enforce AI validation rules

protected_branch='main'
current_branch=`$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')`

if [ "`$current_branch" = "`$protected_branch" ]; then
    echo "ERROR: Direct push to main branch is forbidden!"
    echo "Please create a feature branch and submit a PR:"
    echo "  git checkout -b feature/your-feature-name"
    echo "  git push origin feature/your-feature-name"
    echo "  # Then create PR on GitHub"
    exit 1
fi

# Check if validation is available and required
if [ -f "tasks.py" ] && command -v python >/dev/null 2>&1; then
    echo "Running AI validation checks..."
    python -m invoke ai-validate
    if [ `$? -ne 0 ]; then
        echo "ERROR: AI validation failed. Please fix issues before pushing."
        exit 1
    fi
fi

exit 0
"@

# Pre-commit hook to validate workflow compliance
$preCommitHook = @"
#!/bin/sh
# Pre-commit hook to enforce workflow compliance

# Check if committing directly to main
current_branch=`$(git symbolic-ref --short HEAD)`
if [ "`$current_branch" = "main" ]; then
    echo "ERROR: Direct commits to main branch are forbidden!"
    echo "Please create a feature branch:"
    echo "  git checkout -b feature/your-feature-name"
    exit 1
fi

# Run validation if available
if [ -f "tasks.py" ] && command -v python >/dev/null 2>&1; then
    echo "Validating commit compliance..."
    python -m invoke validate
    if [ `$? -ne 0 ]; then
        echo "ERROR: Validation failed. Please fix issues before committing."
        exit 1
    fi
fi

exit 0
"@

# Install hooks
$prePushHook | Out-File -FilePath "$hooksDir\pre-push" -Encoding ASCII
$preCommitHook | Out-File -FilePath "$hooksDir\pre-commit" -Encoding ASCII

Write-Host "Git hooks installed successfully!" -ForegroundColor Green
Write-Host "Enforcement active for:" -ForegroundColor Yellow
Write-Host "  - Preventing direct main branch pushes" -ForegroundColor White
Write-Host "  - Preventing direct main branch commits" -ForegroundColor White
Write-Host "  - Running validation before commits/pushes" -ForegroundColor White

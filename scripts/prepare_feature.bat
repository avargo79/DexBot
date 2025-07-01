@echo off
REM DexBot Feature Preparation Script Launcher (Legacy)
REM This batch file now calls the PowerShell script for compatibility

echo DexBot Feature Preparation Tool (Legacy)
echo ======================================

echo NOTE: This batch file is deprecated and will be removed in a future update.
echo Please use prepare_feature.ps1 (PowerShell) or prepare_feature.sh (Bash) instead.
echo.

REM Check if any parameters were passed
if "%*"=="" (
    echo No parameters provided, calling PowerShell script...
    powershell -ExecutionPolicy Bypass -File "prepare_feature.ps1"
) else (
    echo Forwarding parameters to PowerShell script...
    powershell -ExecutionPolicy Bypass -File "prepare_feature.ps1" %*
)

pause

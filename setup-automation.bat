@echo off
REM Batch file to run PowerShell automation setup as Administrator
REM This handles the path with apostrophe correctly

echo.
echo ============================================================
echo  Git Automation Setup
echo ============================================================
echo.
echo This will create two scheduled tasks:
echo   1. Startup task - catches missed commits
echo   2. Daily 9PM task - commits daily changes
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

echo.
echo Running PowerShell setup script...
echo.

PowerShell -ExecutionPolicy Bypass -Command "& '%~dp0setup_daily_automation.ps1'"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo  Setup Complete!
    echo ============================================================
    echo.
) else (
    echo.
    echo ============================================================
    echo  Setup Failed
    echo ============================================================
    echo.
    echo Please check the error messages above.
    echo Or try the manual setup in SETUP_AUTOMATION.md
    echo.
)

pause

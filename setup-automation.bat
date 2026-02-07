@echo off
REM Batch file to run PowerShell automation setup as Administrator
REM Auto-elevates if not running as admin

:: Check for admin rights
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :run_setup
) else (
    echo.
    echo ============================================================
    echo  Requesting Administrator Privileges...
    echo ============================================================
    echo.
    echo This script needs admin rights to create scheduled tasks.
    echo You'll see a UAC prompt - click Yes to continue.
    echo.

    :: Re-launch as admin
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:run_setup
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
    echo Tasks created successfully!
    echo Open Task Scheduler to view them.
    echo.
) else (
    echo.
    echo ============================================================
    echo  Setup Failed
    echo ============================================================
    echo.
    echo Error code: %ERRORLEVEL%
    echo Please check the error messages above.
    echo Or try the manual setup in SETUP_AUTOMATION.md
    echo.
)

pause

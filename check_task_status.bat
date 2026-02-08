@echo off
REM Batch wrapper to run the PowerShell verification script

echo.
echo ============================================================
echo  Checking Task Scheduler Status
echo ============================================================
echo.

PowerShell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0check_task_status.ps1"

echo.
pause

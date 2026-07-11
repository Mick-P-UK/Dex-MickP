@echo off
REM Windows batch wrapper for session-start hook
REM Uses CLAUDE_PROJECT_DIR from environment (set by Claude Code) or falls back to script location

if "%CLAUDE_PROJECT_DIR%"=="" (
    REM If not set, calculate from script location
    set "CLAUDE_PROJECT_DIR=%~dp0..\.."
)
cd /d "%CLAUDE_PROJECT_DIR%"
REM Use -NoExit to prevent PowerShell from waiting, but actually we want it to exit
REM Redirect output to avoid blocking
powershell.exe -ExecutionPolicy Bypass -NoProfile -NonInteractive -File "%~dp0session-start.ps1" 2>&1
exit /b %ERRORLEVEL%

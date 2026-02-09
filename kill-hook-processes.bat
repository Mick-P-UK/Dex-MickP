@echo off
REM Kill any hanging hook processes
echo Killing any hanging Node.js, PowerShell, or cmd processes related to hooks...

REM Kill node processes running the wrapper
taskkill /F /IM node.exe /FI "WINDOWTITLE eq *session-start*" 2>nul
taskkill /F /IM node.exe /FI "COMMANDLINE eq *session-start-wrapper*" 2>nul

REM Kill PowerShell processes running session-start scripts
taskkill /F /IM powershell.exe /FI "COMMANDLINE eq *session-start*" 2>nul

REM Kill cmd processes running batch files
taskkill /F /IM cmd.exe /FI "COMMANDLINE eq *session-start.bat*" 2>nul

echo Done. Try starting Claude Code again.

@echo off
cd /d "%~dp0"
git add .claude/hooks/session-start.sh CLAUDE.md System/session_log.md
git commit -m "Fix session startup protocol and update session log

- Improved session-start.sh hook error handling for Windows compatibility
- Added explicit fallback instructions in CLAUDE.md to always read session_log.md
- Updated session log to include Obsidian integration work from today
- Session log now properly captures all work completed in session"
echo.
echo Commit completed! You can delete this batch file now.
pause

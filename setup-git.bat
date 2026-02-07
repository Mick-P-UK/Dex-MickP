@echo off
REM Git Repository Setup Script for Dex Customizations

echo Initializing git repository...

cd /d "c:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP"

if not exist ".git" (
    git init
    echo Git repository initialized
) else (
    echo Git repository already exists
)

echo.
echo Staging files...
git add .

echo.
echo Creating initial commit...
git commit -m "Initial commit: Dex setup with custom file naming convention

- Initial Dex system setup completed
- Custom file naming: YYYY.MM.DD-Filename.md format
- Code updated to dynamically find latest dated files
- Custom changes log created (CUSTOM_CHANGES.md)

Files renamed:
- DEX_Setup.md -^> 2026.02.07-DEX_Setup.md
- Tasks.md -^> 2026.02.07-Tasks.md
- Week_Priorities.md -^> 2026.02.07-Week_Priorities.md

Code changes:
- Python: work_server.py, career_server.py (added find_latest_dated_file helper)
- TypeScript: data-layer.ts, index.ts, context/task.ts (added findLatestDatedFile helper)
- All code now automatically finds most recent dated file or falls back to original name"

echo.
echo Git repository setup complete!
echo.
echo To view commit history: git log
echo To see changes: git status
echo To see what changed: git diff
pause

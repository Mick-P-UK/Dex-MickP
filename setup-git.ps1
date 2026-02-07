# Git Repository Setup Script for Dex Customizations
# Run this script to initialize git and commit custom changes

Write-Host "Initializing git repository..." -ForegroundColor Cyan

# Navigate to Dex directory
Set-Location "c:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP"

# Initialize git if not already initialized
if (-not (Test-Path ".git")) {
    git init
    Write-Host "✓ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "✓ Git repository already exists" -ForegroundColor Yellow
}

# Configure git user if not set (optional - uncomment and set your details)
# git config user.name "Mick Pavey"
# git config user.email "your-email@example.com"

Write-Host "`nStaging files..." -ForegroundColor Cyan

# Stage all files (respects .gitignore)
git add .

Write-Host "✓ Files staged" -ForegroundColor Green

Write-Host "`nCreating initial commit..." -ForegroundColor Cyan

# Create initial commit with descriptive message
git commit -m "Initial commit: Dex setup with custom file naming convention

- Initial Dex system setup completed
- Custom file naming: YYYY.MM.DD-Filename.md format
- Code updated to dynamically find latest dated files
- Custom changes log created (CUSTOM_CHANGES.md)

Files renamed:
- DEX_Setup.md → 2026.02.07-DEX_Setup.md
- Tasks.md → 2026.02.07-Tasks.md  
- Week_Priorities.md → 2026.02.07-Week_Priorities.md

Code changes:
- Python: work_server.py, career_server.py (added find_latest_dated_file helper)
- TypeScript: data-layer.ts, index.ts, context/task.ts (added findLatestDatedFile helper)
- All code now automatically finds most recent dated file or falls back to original name"

Write-Host "✓ Initial commit created" -ForegroundColor Green

Write-Host "`nGit repository setup complete!" -ForegroundColor Green
Write-Host "`nTo view commit history: git log" -ForegroundColor Cyan
Write-Host "To see changes: git status" -ForegroundColor Cyan
Write-Host "To see what changed: git diff" -ForegroundColor Cyan

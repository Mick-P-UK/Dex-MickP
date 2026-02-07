# Manual Git Setup Instructions

Due to PowerShell execution issues, please run these commands manually in your terminal.

## Option 1: Run the Batch File (Easiest)

Double-click `setup-git.bat` or run it from Command Prompt:

```cmd
cd "c:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP"
setup-git.bat
```

## Option 2: Run Commands Manually

Open Command Prompt or PowerShell and run:

```cmd
cd "c:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP"

REM Initialize git repository
git init

REM Stage all files
git add .

REM Create initial commit
git commit -m "Initial commit: Dex setup with custom file naming convention

- Initial Dex system setup completed
- Custom file naming: YYYY.MM.DD-Filename.md format  
- Code updated to dynamically find latest dated files
- Custom changes log created (CUSTOM_CHANGES.md)

Files renamed:
- DEX_Setup.md -> 2026.02.07-DEX_Setup.md
- Tasks.md -> 2026.02.07-Tasks.md
- Week_Priorities.md -> 2026.02.07-Week_Priorities.md

Code changes:
- Python: work_server.py, career_server.py (added find_latest_dated_file helper)
- TypeScript: data-layer.ts, index.ts, context/task.ts (added findLatestDatedFile helper)
- All code now automatically finds most recent dated file or falls back to original name"
```

## Option 3: Use Git GUI

If you have a Git GUI tool (like GitHub Desktop, SourceTree, or GitKraken):

1. Open your Git GUI tool
2. Add the repository: `c:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP`
3. Initialize repository if prompted
4. Stage all files
5. Commit with the message above

## Verify Setup

After running the setup, verify it worked:

```cmd
git status
git log
```

You should see:
- `git status` shows "nothing to commit, working tree clean"
- `git log` shows your initial commit

## Next Steps

Once git is initialized, you can:

1. **Make changes** to Dex system files
2. **Update CUSTOM_CHANGES.md** with details
3. **Commit changes:**
   ```cmd
   git add .
   git commit -m "Description of your changes"
   ```

See `GIT_SETUP.md` for more detailed git usage instructions.

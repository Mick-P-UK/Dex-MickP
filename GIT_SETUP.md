# Git Repository Setup for Dex Customizations

This document explains how to set up git tracking for your Dex system customizations.

## Quick Setup

Run the PowerShell script to initialize git and create the initial commit:

```powershell
.\setup-git.ps1
```

Or manually:

```powershell
cd "c:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP"
git init
git add .
git commit -m "Initial commit: Dex setup with custom file naming convention"
```

## What Gets Tracked

**Tracked (in git):**
- ✅ Dex system code (`core/`, `pi-extensions/`, `.claude/`)
- ✅ Custom changes log (`CUSTOM_CHANGES.md`)
- ✅ Configuration templates and documentation
- ✅ System setup scripts

**Not Tracked (excluded by .gitignore):**
- ❌ User data folders (`00-Inbox/`, `03-Tasks/`, `04-Projects/`, etc.)
- ❌ Personal configuration (`System/user-profile.yaml`, `System/pillars.yaml`)
- ❌ Environment files (`.env`)
- ❌ Node modules and build artifacts

**Why:** Your personal data (tasks, projects, meeting notes) stays private. Only system code and customizations are tracked.

## Making Future Changes

When you modify Dex system files:

1. **Make your changes** to the code/files
2. **Update `CUSTOM_CHANGES.md`** with details of what changed
3. **Commit with descriptive message:**
   ```powershell
   git add .
   git commit -m "Brief description of change

   Detailed explanation:
   - What was changed
   - Why it was changed
   - Files affected"
   ```

## Useful Git Commands

```powershell
# Check status
git status

# View commit history
git log --oneline

# See what changed in a file
git diff core/mcp/work_server.py

# View changes in last commit
git show

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Create a branch for experimental changes
git checkout -b experiment-branch-name
```

## Best Practices

1. **Commit frequently** - Small, focused commits are easier to understand and rollback
2. **Write clear messages** - Describe what changed and why
3. **Update CUSTOM_CHANGES.md** - Keep it in sync with your commits
4. **Test before committing** - Make sure changes work before committing
5. **Use branches** - For major changes, create a branch first

## Example Commit Workflow

```powershell
# 1. Make changes to code
# (edit files)

# 2. Update change log
# (edit CUSTOM_CHANGES.md)

# 3. Stage changes
git add core/mcp/work_server.py CUSTOM_CHANGES.md

# 4. Commit with descriptive message
git commit -m "Add helper function to find latest dated files

- Added find_latest_dated_file() to work_server.py
- Updated get_tasks_file() to use helper
- Documented in CUSTOM_CHANGES.md"
```

## Troubleshooting

**Q: Git says "nothing to commit" but I made changes**
- Check if files are in `.gitignore` (user data folders are excluded)
- Use `git status` to see what's tracked

**Q: I want to track my user data folders too**
- Remove the relevant lines from `.gitignore`
- Be aware this will track personal information (tasks, notes, etc.)

**Q: How do I see what changed between commits?**
- `git diff HEAD~1` - Compare with previous commit
- `git log -p` - Show commits with full diffs

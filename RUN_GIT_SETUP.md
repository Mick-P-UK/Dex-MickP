# Run Git Setup - Step by Step Guide

## Quick Start (Choose One Method)

### Method 1: Python Script (Recommended)
1. Open **Command Prompt** (Press `Win + R`, type `cmd`, press Enter)
2. Copy and paste these two lines:
```cmd
cd "c:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP"
python setup_git.py
```
3. Press Enter and follow the prompts

### Method 2: Batch File (Easier)
1. Open **File Explorer**
2. Navigate to: `c:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP`
3. Double-click `setup-git.bat`
4. Wait for it to complete

### Method 3: Manual Commands
If both above methods don't work, open Command Prompt and run:
```cmd
cd "c:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP"
git init
git add .
git commit -m "Initial commit: Dex setup with custom file naming convention"
```

---

## What Will Happen

The script will:
1. ✅ Check if Git is installed
2. ✅ Initialize git repository (if needed)
3. ✅ Stage all Dex system files
4. ✅ Create initial commit with description
5. ✅ Show you the results

**Time:** Takes about 10-30 seconds

---

## Expected Output

You should see something like:
```
============================================================
Git Repository Setup for Dex Customizations
============================================================

Working directory: c:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP

Checking git installation... ✓
  git version 2.43.0

  Initializing git repository... ✓
    Initialized empty Git repository in ...

  Staging files... ✓

  Creating initial commit... ✓
    [main (root-commit) abc1234] Initial commit: Dex setup...

============================================================
✓ Git repository setup complete!
============================================================
```

---

## Troubleshooting

**"Python is not recognized"**
- Try: `py setup_git.py` instead of `python setup_git.py`
- Or use: `setup-git.bat` instead

**"Git is not installed"**
- Download from: https://git-scm.com/download/win
- Install it, then try again

**"Nothing to commit"**
- This is normal! It means all files are already committed or ignored
- Check with: `git status`

---

## After Setup

Once git is initialized, you can:

**View your commits:**
```cmd
git log
```

**Check status:**
```cmd
git status
```

**See what changed:**
```cmd
git diff
```

---

## Daily Automation

After initial setup, the `daily_git_commit.py` script can automatically commit changes daily.

See `System/git_automation_log.md` for details on setting up daily automation.

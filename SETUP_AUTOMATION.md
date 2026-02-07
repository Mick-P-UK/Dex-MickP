# Set Up Daily Git Commit Automation

## Quick Setup (Recommended)

### Option 1: PowerShell Script (Easiest)

1. **Open PowerShell as Administrator:**
   - Press `Win + X`
   - Select "Windows PowerShell (Admin)" or "Terminal (Admin)"

2. **Navigate to Dex folder:**
   ```powershell
   cd "c:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP"
   ```

3. **Run the setup script:**
   ```powershell
   .\setup_daily_automation.ps1
   ```

4. **Done!** The script will create both tasks automatically.

---

### Option 2: Manual Task Scheduler Setup

If the PowerShell script doesn't work, set up manually:

#### Task 1: Startup Task

1. Open **Task Scheduler** (search for it in Start menu)
2. Click **Create Basic Task** (right side)
3. **Name:** `Dex Git Commit - Startup`
4. **Description:** `Dex: Git commit at system startup (catches up on missed commits)`
5. **Trigger:** When the computer starts
6. **Action:** Start a program
7. **Program/script:** `python` (or full path to python.exe)
8. **Add arguments:** `"c:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\daily_git_commit.py"`
9. **Start in:** `c:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP`
10. Check **"Open the Properties dialog..."** and click Finish
11. In Properties:
    - Check **"Run whether user is logged on or not"**
    - Check **"Run with highest privileges"**
    - Under **Conditions:** Check **"Start the task only if the computer is on AC power"** (uncheck this if you want it on battery too)
    - Click **OK**

#### Task 2: Daily 9PM Task

1. Click **Create Basic Task** again
2. **Name:** `Dex Git Commit - Daily 9PM`
3. **Description:** `Dex: Git commit daily at 9:00 PM`
4. **Trigger:** Daily
5. **Time:** 9:00 PM
6. **Action:** Start a program
7. **Program/script:** `python` (or full path to python.exe)
8. **Add arguments:** `"c:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\daily_git_commit.py"`
9. **Start in:** `c:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP`
10. Check **"Open the Properties dialog..."** and click Finish
11. In Properties:
    - Check **"Run whether user is logged on or not"**
    - Check **"Run with highest privileges"**
    - Under **Conditions:** Check **"Start the task only if the computer is on AC power"** (uncheck this if you want it on battery too)
    - Click **OK**

---

## Test the Setup

Before relying on automation, test that it works:

```cmd
cd "c:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP"
python test_daily_commit.py
```

Or test the daily commit script directly:

```cmd
python daily_git_commit.py
```

**Expected output:**
- If there are changes: Creates a commit
- If no changes: Shows "No changes to commit" (this is normal)

---

## What Gets Committed

**Automatically committed:**
- ✅ Changes to Dex system code (Python, TypeScript files)
- ✅ Updates to `CUSTOM_CHANGES.md`
- ✅ Changes to documentation files
- ✅ Configuration changes (if not in .gitignore)

**NOT committed (by design):**
- ❌ Your personal data (tasks, projects, meeting notes)
- ❌ Personal configuration files (`System/user-profile.yaml`, `System/pillars.yaml`)

---

## Verify Tasks Are Running

### Check Task Status

1. Open **Task Scheduler**
2. Look for tasks starting with "Dex Git Commit"
3. Check the **Last Run Result** column:
   - `0x0` = Success
   - Other codes = Check the task history

### View Task History

1. In Task Scheduler, select a task
2. Click **History** tab at bottom
3. Look for recent runs and any errors

### Test Manually

Right-click a task → **Run** to test it immediately.

---

## Troubleshooting

### "Python is not recognized"

**Solution:** Use full path to Python in Task Scheduler:
1. Find Python location: `where python` in Command Prompt
2. Use full path in Task Scheduler instead of just `python`

### Task runs but nothing commits

**This is normal if:**
- No changes were made to tracked files
- All changes are in user data folders (excluded by .gitignore)

**Check:** Run `git status` manually to see what's tracked

### Task fails to run

**Check:**
1. Task Scheduler History tab for error messages
2. Python is installed and in PATH
3. Script path is correct
4. Working directory is set correctly

### Want to change the time

1. Open Task Scheduler
2. Find "Dex Git Commit - Daily 9PM"
3. Right-click → Properties
4. Go to Triggers tab
5. Edit the trigger and change time
6. Click OK

---

## Disable Automation

To temporarily disable:
1. Open Task Scheduler
2. Find the tasks
3. Right-click → Disable

To permanently remove:
1. Open Task Scheduler
2. Find the tasks
3. Right-click → Delete

---

## What Happens

**At Startup:**
- Script runs when computer boots
- Checks for any uncommitted changes
- Commits them if found
- This ensures you never lose changes even if computer was off at 9PM

**At 9PM Daily:**
- Script runs automatically
- Commits any changes made during the day
- Creates descriptive commit message with file list

**If Computer is Off:**
- Startup task will catch up when you next boot
- No changes are lost

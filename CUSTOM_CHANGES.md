# Custom Changes Log

This file tracks all custom modifications made to the Dex system in this vault. This helps identify issues, rollback changes, and maintain system integrity.

**Note:** This is separate from `CHANGELOG.md`, which tracks official Dex updates. This log tracks YOUR customizations.

---

## 2026-02-07 - File Naming Convention Change

### Summary
Changed all Dex system files to use date-prefixed naming format: `YYYY.MM.DD-Filename.md` (no spaces around dash)

### Files Renamed
1. **Projects:**
   - `04-Projects/DEX_Setup.md` → `04-Projects/2026.02.07-DEX_Setup.md`

2. **Tasks:**
   - `03-Tasks/Tasks.md` → `03-Tasks/2026.02.07-Tasks.md`

3. **Week Priorities:**
   - `02-Week_Priorities/Week_Priorities.md` → `02-Week_Priorities/2026.02.07-Week_Priorities.md`

### Code Changes Made

#### Python Files (`core/mcp/`)

**1. `work_server.py`:**
- Added `find_latest_dated_file()` helper function (lines ~95-130)
  - Searches for files matching pattern `YYYY.MM.DD-Filename.md`
  - Sorts by date (most recent first)
  - Falls back to original filename if no dated version exists
- Updated `get_tasks_file()` to use helper function
- Updated `get_week_priorities_file()` to use helper function
- Fixed `WEEK_PRIORITIES_FILE` path (was pointing to wrong location)

**2. `career_server.py`:**
- Added `find_latest_dated_file()` helper function (duplicate of work_server version)
- Updated Tasks.md reference to use helper function (line ~755)

#### TypeScript Files (`pi-extensions/dex/`)

**1. `data-layer.ts`:**
- Added `findLatestDatedFile()` helper function
- Changed `TASKS_PATH` from constant to dynamic lookup using helper
- Updated `loadWeekPriorities()` to find latest dated file (line ~272)

**2. `index.ts`:**
- Added `findLatestDatedFile()` helper function
- Changed `TASKS_PATH` from constant to dynamic lookup using helper

**3. `context/task.ts`:**
- Added `findLatestDatedFile()` helper function
- Updated `parseTasks()` to find latest dated Tasks.md file (line ~14)

### Rationale
- Date-prefixed files allow tracking file versions over time
- Format without spaces (`YYYY.MM.DD-Filename.md`) is more programmatically friendly
- System automatically finds the most recent dated file
- Backward compatible: falls back to original filename if no dated version exists

### Testing Notes
- Code should automatically detect and use dated files
- If issues occur, check that helper functions are finding files correctly
- Verify that both dated and non-dated files work (backward compatibility)

### Rollback Instructions
If needed, rename files back to original names:
- `2026.02.07-DEX_Setup.md` → `DEX_Setup.md`
- `2026.02.07-Tasks.md` → `Tasks.md`
- `2026.02.07-Week_Priorities.md` → `Week_Priorities.md`

Code changes can be reverted by removing the helper functions and restoring original file path constants.

---

## 2026-02-22 - UTF-8 Pre-Commit Hook

### Summary
Installed a git pre-commit hook that scans all staged `.md` files for Windows-1252
typographic characters (em dashes, smart quotes, ellipsis, etc.) before every commit.
Blocks the commit and shows exact file/line/replacement if any are found.

This was triggered by an em dash (0x97) in `03-Tasks/2026.02.07-Tasks.md` at position
301 (phrase: "4th Mar -- find a free hour") that broke all work-mcp tools.

### Files Added/Modified
- **Added:** `.git/hooks/pre-commit` - Python script, scans staged .md files
- **Added:** `docs/utf8-corruption-troubleshooting.md` - Full troubleshooting guide
- **Fixed:** `03-Tasks/2026.02.07-Tasks.md` - Em dash replaced with hyphen
- **Fixed:** `03-Tasks/Tasks.md` - Smart quotes replaced with straight quotes

### How the Hook Works
- Runs automatically on every `git commit`
- Gets list of staged .md files via `git diff --cached --name-only`
- Scans each file byte-by-byte for bytes 0x80-0xA0 (Windows-1252 range)
- If found: blocks commit, prints file/line/position/suggested replacement
- If clean: prints quiet confirmation, allows commit

### Rationale
work-mcp tools use strict `encoding='utf-8'` when reading vault files. Windows-1252
typographic characters are invisible corruption - they look fine in editors but crash
Python's UTF-8 decoder, blocking all work-mcp functionality until manually fixed.

### If the Hook Stops Running
```powershell
git config core.hooksPath .git/hooks
```
See `docs/utf8-corruption-troubleshooting.md` for full recovery steps.

### Rollback Instructions
Delete `.git/hooks/pre-commit` to remove the hook. No other files are affected.

---

## Change Log Template

When making future changes, add entries using this format:

```markdown
## YYYY-MM-DD - [Brief Description]

### Summary
[What was changed and why]

### Files Modified
- [List of files changed]

### Code Changes Made
[Detailed description of code changes]

### Rationale
[Why this change was made]

### Testing Notes
[What to test, known issues]

### Rollback Instructions
[How to undo if needed]
```

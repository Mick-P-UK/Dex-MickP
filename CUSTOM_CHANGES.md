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

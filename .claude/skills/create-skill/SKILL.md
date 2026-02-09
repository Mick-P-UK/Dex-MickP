---
name: create-skill
description: Create a custom skill that's protected from Dex updates. Automatically appends -custom to ensure your skill is never overwritten.
---

# Create Custom Skill

Create your own skill that's protected from Dex updates.

## How It Works

When you create a skill with this command, Dex automatically:
1. Appends `-custom` to the folder name (so it's never overwritten by updates)
2. Creates the proper SKILL.md structure
3. Sets up optional folders for scripts, references, and assets

## Process

### Step 1: Get Skill Details

Ask the user:

```
What should this skill do?

Give me:
1. A short name (e.g., "meeting-notes", "weekly-report")
2. What it should help you with (1-2 sentences)
```

### Step 2: Check for Date-Based Operations

**Before creating the skill, ask:**

```
Does this skill involve creating files with dates in the filename or any date-based operations?

Examples:
- Creating daily/weekly/monthly reports
- Generating files named with dates (YYYY-MM-DD)
- Calculating "today", "this week", "this quarter"
- Creating date-based archives or reviews
- Any reference to dates, days of week, or time periods
```

**If YES:** The skill MUST include Step 0: Date Verification. See "Date Verification Template" below.

**If NO:** Proceed to Step 3.

---

### Step 3: Create the Skill

**Skill folder:** `.claude/skills/{name}-custom/`

The `-custom` suffix is automatic - don't let the user add it themselves.

**Create SKILL.md:**

```markdown
---
name: {name}-custom
description: {user's description}
---

# {Title Case Name}

{User's description expanded into a helpful intro}

## Process

{IF DATE-BASED: Include Step 0: Date Verification from template below}

### Step 1: [First Step]

[Instructions for what to do]

### Step 2: [Second Step]

[Instructions for what to do]

## Notes

- This is a custom skill, protected from Dex updates
- Edit `.claude/skills/{name}-custom/SKILL.md` to modify
```

---

### Date Verification Template (Use if skill involves dates)

**If the skill involves dates, ALWAYS include this as Step 0:**

```markdown
## Step 0: Date Verification (CRITICAL - MUST DO FIRST)

**Before anything else, verify the current date:**

1. **Get actual current date programmatically:**
   ```python
   from datetime import date
   today = date.today()
   date_str = today.strftime('%Y-%m-%d')  # e.g., "2026-02-08"
   day_name = today.strftime('%A')  # e.g., "Sunday"
   ```

2. **Check if file already exists:**
   ```python
   from pathlib import Path
   target_file = Path(f"path/to/{date_str}-filename.md")
   if target_file.exists():
       # File already exists - ask user if they want to update or create new
   ```

3. **Verify day of week matches date:**
   - Never assume day of week from date or vice versa
   - Always calculate both independently and verify they match

4. **Never assume date progression:**
   - Don't assume today is "yesterday + 1 day"
   - Don't assume date from session log timestamps
   - Always get actual current date from system

**Use `date_str` and `day_name` throughout the rest of the skill** - never hardcode dates or assume.

**Why:** Date-based files must use correct dates. Wrong dates cause confusion, duplicates, and break workflows. See CLAUDE.md → File Conventions → Date Verification for details.
```

**For weekly operations, also calculate Monday:**
```python
from datetime import timedelta
days_since_monday = today.weekday()  # 0=Monday, 6=Sunday
monday = today - timedelta(days=days_since_monday)
monday_str = monday.strftime('%Y-%m-%d')
```

**For quarterly operations, calculate quarter from user profile:**
```python
# Read q1_start_month from System/user-profile.yaml
# Calculate quarter based on current month and q1_start_month
# See quarter-plan skill for reference implementation
```

### Step 4: Confirm

```
✅ Created skill: /{{name}}-custom

Your skill is ready to use. Run /{name}-custom to try it.

**Protected from updates:** The -custom suffix means Dex updates
will never overwrite this skill. It's yours to customize.

**To edit:** Modify .claude/skills/{name}-custom/SKILL.md
```

## Examples

**User:** "I want a skill for preparing board updates"

**Result:**
- Folder: `.claude/skills/board-update-custom/`
- Invoke with: `/board-update-custom`
- Protected from all Dex updates

**User:** "Create a skill called weekly-standup-custom"

**Response:** "I'll create that as `weekly-standup-custom` - you don't need to add '-custom' yourself, I do that automatically. Want me to proceed with just 'weekly-standup'?"

## Tips

- Keep skill names short and descriptive
- Use hyphens, not spaces or underscores
- The skill can reference other files in its folder (scripts/, references/, assets/)

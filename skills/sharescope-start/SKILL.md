# ShareScope Start Skill

## Trigger Phrases
Use this skill when Mick says any of the following:
- "sharescope start" / "start ShareScope session"
- "pick up ShareScope" / "continue ShareScope work"
- "ShareScope automation" (at session start)
- "let's work on ShareScope"
- "/sharescope-start"

---

## Purpose
One-command session opener for ShareScope automation work. Connects all required
folders, reads the current pickup point, and delivers a clean briefing so work
can resume immediately without back-and-forth setup.

---

## Step 1 -- Connect Required Folders

Request BOTH folders simultaneously (one tool call with two requests is not possible,
so fire them back-to-back as fast as possible):

  Folder 1 (Vault -- for memory file):
    C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP

  Folder 2 (ShareScope project):
    C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation

Say to Mick: "Connecting your vault and ShareScope project folder -- approve both prompts."
Wait for both to confirm before proceeding.

---

## Step 2 -- Verify London Time

Run this code before greeting:

```python
from datetime import datetime, timezone, timedelta
utc_now = datetime.now(timezone.utc)
bst_active = 4 <= utc_now.month <= 10
offset = timedelta(hours=1) if bst_active else timedelta(hours=0)
london_now = utc_now.astimezone(timezone(offset))
hour = london_now.hour
tz = 'BST' if bst_active else 'GMT'
print(f'{london_now.strftime("%H:%M")} {tz} -- {london_now.strftime("%A %d %B %Y")}')
```

Greeting: before 12 = Good morning / 12-17 = Good afternoon / 18+ = Good evening

---

## Step 3 -- Read Key Files (both simultaneously)

Read these two files at the same time:

  File A: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\CEDRIC_MEMORY.md
          (read the RESUME HERE section and the most recent Session Log entry)

  File B: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\PICKUP_POINT.md
          (read in full -- this is the primary handoff document)

PICKUP_POINT.md takes priority if it conflicts with CEDRIC_MEMORY.md
(it is more recently updated and more granular on ShareScope specifics).

---

## Step 4 -- Deliver Session Briefing

Present a clean briefing to Mick in this format:

---
**ShareScope Session -- [Date] [Time]**

**Where we are:**
[2-3 sentence summary of current phase and what was last completed]

**Immediate next steps:**
1. [Step from PICKUP_POINT.md]
2. [Step from PICKUP_POINT.md]
3. [etc.]

**Key technical facts (quick reference):**
- Automation method: Python Playwright (bash/headed)
- Login URL: https://webservice.sharescope.co.uk/login.do
- Credentials: C:\Vaults\Mick's Vault\.env
- Project folder: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\
- PRD v2.0: [location from PICKUP_POINT.md]

**Ready to go. What would you like to tackle first?**
---

Keep the briefing concise -- Mick can read PICKUP_POINT.md himself if he wants the full detail.
The goal is to be work-ready within 60 seconds of saying "sharescope start".

---

## Step 5 -- Wait for Mick's Direction

Do NOT start making changes or writing code until Mick confirms the direction.
The briefing ends with a question. Wait for the answer.

---

## Notes

- PICKUP_POINT.md is updated at the end of each ShareScope session as a handoff doc.
  Always read it -- it may contain session-specific facts not yet in CEDRIC_MEMORY.md.
- If PICKUP_POINT.md does not exist, fall back to the RESUME HERE block in CEDRIC_MEMORY.md.
- If neither file gives enough context, read PHASE_1_SUMMARY.md from the project folder.
- Mick is a relative coding newbie -- always give step-by-step instructions with exact paths.

---

## Skill Metadata

Version:  1.0
Created:  2026.04.26
Author:   Cedric (PAIDA)
Vault:    C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\sharescope-start\SKILL.md
Mirror:   /mnt/skills/user/sharescope-start/SKILL.md

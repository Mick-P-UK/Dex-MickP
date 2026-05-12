# PICKUP NOTE - Poppy Build

**Last session**: 2026.05.04 (Monday evening)
**Next session**: TBC - Tuesday or Wednesday

---

## Where you left off

You finished reading Section 5 (Knowledge Files) of the `Poppy-Settings-and-Connectors.md` document, then asked Cedric where to physically create the three supporting files. Cedric recommended a new vault folder, edited from Cursor.

You wrapped at 20:44 BST.

## What is already produced and approved

Two files were delivered in the outputs folder:

1. **CLAUDE.md** - Poppy's project instructions (16 sections)
2. **Poppy-Settings-and-Connectors.md** - companion setup guide

Both are ASCII-clean, UK English, ready to use. They reflect every decision you made across the seven question rounds.

## What to do next (in order)

### Step 1 - Create the Poppy folder in your vault

```
C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\Poppy\
```

Open this folder in Cursor as a workspace.

### Step 2 - Save the two files Cedric produced into that folder

Move these from outputs into the new Poppy folder:

- `CLAUDE.md` (this is the project instructions text - will get pasted into Claude.ai later, but keep the master copy here)
- `Poppy-Settings-and-Connectors.md`

### Step 3 - Create the three supporting files in Cursor

Create these as new empty files first:

- `Rulebook.md` - use the starter structure in Section 14 of CLAUDE.md
- `Poppy-Reference.md` - use as overflow if CLAUDE.md hits a character limit in claude.ai (most of Sections 5-16 if needed)
- `PAIDA-Architecture.md` - one-pager explaining how Poppy / Cedric / Annie relate, so Poppy stays in her lane

Cedric can help you draft Poppy-Reference.md and PAIDA-Architecture.md when you resume - just ask.

### Step 4 - Build the Notion architecture

Before Poppy goes live, set up:

```
PAIDA (new top-level page)
+-- Cedric
|   +-- CEDRIC Memory Vault (move existing here)
|   +-- CEDRIC Knowledge Base (move existing here)
+-- Poppy
    +-- Poppy Memory (new database)
    +-- Poppy's Daily Digests (new database)

YT References (new top-level database, not under PAIDA)
```

Schemas for the three new databases are in CLAUDE.md Sections 4.3, 8.2, and 10.1.

### Step 5 - Sync Rulebook.md to Google Drive

Create folder `/PAIDA/Poppy/` in Google Drive. Copy the Rulebook.md there. This is what Poppy will actually read at session start.

### Step 6 - Create the claude.ai Project

- Project name: **Poppy - Personal Assistant**
- Paste CLAUDE.md content into project instructions field
- Upload Rulebook.md, Poppy-Reference.md, PAIDA-Architecture.md as knowledge files
- Enable connectors: Gmail, Notion, Google Drive, Slack, Google Calendar (read-only), web search

### Step 7 - First-run bootstrap

Open Poppy for the first time. She should walk through CLAUDE.md Section 13 first-run bootstrap:

- Confirm Notion architecture
- Create Gmail labels with `Poppy/` prefix
- Confirm Trusted Senders starter list (Jade, Azets minimum)
- Confirm Never Touch starter list (Debs, Leo - **need their email addresses from you**)
- Backfill last 7 days

### Step 8 - Set calendar reminders for digest times

Three repeating Google Calendar events:
- 07:00 daily - "Open Poppy - Morning Digest"
- 13:00 daily - "Open Poppy - Midday Check"
- 17:00 daily - "Open Poppy - Wrap-up"

Phone notifications will be your trigger. v2 (later) = n8n flow that automates this.

---

## Open items / decisions to provide

When you resume, have these ready:

1. **Debs and Leo's email addresses** (for Never Touch list)
2. **Justin's email address** if he should also go on Never Touch
3. **Channel list for Slack monitoring** - which channels (if any) should Poppy watch for mentions, beyond DMs? Default: DMs only, no channels.
4. **Confirm Drive folder structure** - happy with `/PAIDA/Poppy/Rulebook.md` or prefer something else?
5. **Project name** - sticking with "Poppy - Personal Assistant" or shorter?

---

## Meet Cedric episode notes

This build is being captured for a Meet Cedric two-parter:

- **Part 1**: "Building Poppy" - the discovery questions, the iteration on categories, the architecture decisions, producing CLAUDE.md
- **Part 2**: "Poppy in Action" - first-run bootstrap, real digest output, learning loop in action

Cedric has memory entry #30 (added 2026.05.04) confirming this. Recording everything.

---

## Files to reference

| File | Purpose |
|---|---|
| `outputs/CLAUDE.md` | Poppy project instructions (master copy will live in vault Poppy folder) |
| `outputs/Poppy-Settings-and-Connectors.md` | Setup guide |
| `System/session_log.md` | Full decision history from 2026.05.04 session |
| `CEDRIC_MEMORY.md` | Cedric's session memory (entry #30 covers Meet Cedric episode) |

---

## Quick start prompt for next session

When you reopen Cedric, paste this:

> Cedric, resuming Poppy build. Read PICKUP_NOTE_2026.05.04-Poppy.md and the latest session_log entry. I'm ready to continue from Step [N].

That gets us straight back into it.

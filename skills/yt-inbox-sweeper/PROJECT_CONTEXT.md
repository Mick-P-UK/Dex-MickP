# Project Context: YT Inbox Sweeper

A self-contained brief for the Cowork project. Drop this into the project's Instructions field so any future Cedric run has full context without needing to re-read the original setup conversation.

## Project owner
Mick Pavey (mickp.dbox@gmail.com)

## Purpose
Automate the triage of YouTube links that Mick forwards to his own Gmail address, so the inbox stays clean and every link ends up in a searchable Google Sheet with metadata, his hint phrase, and Cedric's commentary.

## Background
Mick has a habit of sending himself YouTube links by email, usually with a short hint phrase indicating his thinking - e.g.:
- "Cowork for diy?"
- "For webinar?"
- "SMALL BUSINESS"
- "Explore using linear for project management"
- "Goog clesr explanation of cowork! Fork this for diy-investors!"

These accumulate in the inbox and get lost. The sweeper turns them into structured rows in a Google Sheet.

## Solution architecture

A single skill (`yt-inbox-sweeper`) that:
1. Searches Gmail for self-sent emails containing YouTube links
2. Extracts URL, hint phrase, date, message ID
3. Enriches with YouTube video title, channel, duration (via web fetch)
4. Generates a 1-2 sentence "Cedric's Take" tying the hint to known projects
5. Appends one row per video to a Google Sheet
6. Labels each thread `YT-Processed` and archives it
7. Reports a summary

Runs daily at 06:45 London time, just before the 07:00 morning briefing.

## Output destination

### Google Sheet: "YouTube Queue - Email Sweep"
- Sheet ID: `1bXirFpcyp8XDoYMB5LcNxQm0ztJoRb6lheHln1md-Fo`
- URL: https://docs.google.com/spreadsheets/d/1bXirFpcyp8XDoYMB5LcNxQm0ztJoRb6lheHln1md-Fo

### Containing folder: "email-sweep-results"
- Folder ID: `1UVxW-I22TgpEydgw-mLT68N648ib5Xog`
- URL: https://drive.google.com/drive/folders/1UVxW-I22TgpEydgw-mLT68N648ib5Xog

### Parent folder: "0 - AI - Cowork"
- Folder ID: `1mfb82toinDXfo1ZjKTaEBPUh83dTmRE3`

The folder name `email-sweep-results` was chosen deliberately to allow future expansion - e.g. article sweeps, RNS sweeps, Substack sweeps - each as a separate sheet in the same folder.

## Sheet schema (columns A to K)
1. Date Sent (YYYY-MM-DD HH:MM, London time)
2. URL (cleaned, no tracking parameters)
3. Video Title (from YouTube metadata)
4. Channel (from YouTube metadata)
5. Duration (HH:MM:SS)
6. Your Tag (Mick's hint phrase, normalised)
7. Cedric's Take (1-2 sentences, UK English, ASCII only)
8. Status (one of: New, Reviewed, Actioned, Archived - default New)
9. Watched? (Yes / No / Partial - left blank by skill)
10. Your Notes (free text - left blank by skill)
11. Source Email ID (Gmail message ID for traceability)

## Schedule
- Cron expression: `45 6 * * *`
- Local time: 06:45 daily, London
- Scheduled task ID: `yt-inbox-sweeper-daily`

## Gmail labels
- `YT-Processed` - applied automatically by the skill after a thread is swept
- `YT-Skip` - veto label; Mick applies this manually to any thread he wants the sweeper to ignore

The sweeper excludes both labels from its search, so neither processed nor skipped threads ever come round again.

## Manual invocation triggers
Any of these phrases will run the skill on demand:
- "run the YT sweep"
- "process my YouTube self-emails"
- "clear the YouTube backlog"
- "sweep my inbox for YouTube"
- "do the YouTube tidy"

## Project files
- `SKILL.md` - the skill definition (workflow, schema, safety nets). Lives in Mick's vault skills folder at `C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\yt-inbox-sweeper\SKILL.md`
- `SCHEDULED_TASK_PROMPT.md` - the prompt for the daily scheduled task, ready to register
- `PROJECT_CONTEXT.md` - this file

## Outstanding work
1. **Register the scheduled task.** The scheduler refused registration during the initial setup conversation because that conversation was itself running as a scheduled task (the morning briefing). In a normal interactive session, say: "Cedric, register the yt-inbox-sweeper as a daily scheduled task at 06:45 London" - Cedric will use the prompt in `SCHEDULED_TASK_PROMPT.md`.
2. **Copy SKILL.md into the vault** at `C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\yt-inbox-sweeper\` so it loads as a discoverable skill.
3. **First live run.** Once scheduled, the first morning run will process whatever has accumulated in the last 2 days. Worth a manual check of the sheet to confirm the parsing of hint phrases works as expected.

## Conventions
- UK English throughout (organise, colour, behaviour)
- ASCII only when writing to the sheet or vault files (no em dashes, smart quotes, ellipsis)
- Times always in London (Europe/London)
- All file operations log to `/home/claude/paida_changelog/` per Mick's PAIDA conventions

## Future extensions (not yet built - park here for later discussion)
- **Expand beyond YouTube.** Same workflow for articles, Substack posts, RNS reminders Mick forwards himself. Each gets its own sheet in `email-sweep-results`.
- **Controlled tag vocabulary.** Currently Mick's hint phrases are free text. A controlled set (Project / Watch Later / Reference / Pass-along / Webinar Material) would make filtering easier.
- **Weekly unwatched digest.** Saturday morning summary of items still marked `Status: New` and `Watched?: blank` from the past week.
- **Cross-reference against AI-4-Inv webinar planning.** Auto-suggest links that look webinar-relevant based on title/channel and the current month's webinar theme.
- **Notion mirror.** Optional second destination - mirror new rows into a Notion database for richer note-taking.

## Key projects this sweeper supports
Context for "Cedric's Take" column - relevance flags worth using:
- **AI-4-Inv webinar** - monthly webinar for the AI for Investors series
- **DIY Investors** - Mick's website (diy-investors.ai) and YouTube channel
- **Cowork demos** - Mick produces content explaining Cowork to non-technical users
- **Claude Code workflows** - for the more technical side of Mick's content
- **Portfolio research** - UK and US stock portfolios (UK Active 10, US Active 10, etc.)
- **MCP / connector building** - Mick builds MCPs and plugins
- **Plugin development** - Cowork plugin work

## Setup date
2026-05-18, during the morning briefing scheduled task run.

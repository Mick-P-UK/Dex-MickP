# micks-view-query Skill v1.0
# Micks-View Query Command
# Created: 2026-03-10 | PRD v2.2 Phase 1

## Purpose

Query the Micks-View stock note library and return results in chronological
order. This is the PRIMARY read mechanism for Micks-View. It does NOT write -
use micks-stocknote for that.

## Trigger

User says any of:
- "query [TICKER]" or "search [TICKER]"
- "what do I think about [TICKER]"
- "micks view on [TICKER]"
- "show me notes on [TICKER]"
- "radar [TICKER]" (legacy trigger)
- "/radar [TICKER]"

## Vault Location

Scan these locations in order:
1. C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\Micks-View\00-Inbox\
2. C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\Micks-View\02-Areas\Stocks\
3. C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\Micks-View\02-Areas\Sectors\
4. C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\Micks-View\04-Archives\

## Query Modes

### Mode 1: Current View
"What is Mick's current view on [TICKER]?"

- Find the MOST RECENT note for TICKER (by date field in YAML)
- Check if date is within 90 days of today
- Return: date, sp_start, mcap, view_current, micks_summary, full content
- If note is older than 90 days, flag: "Note is [N] days old - view may be stale"

### Mode 2: Micks-View Log
"Show me Mick's full history on [TICKER]"

- Return ALL notes for TICKER where source = Brain Dump OR micks_edit = true
- Exclude pure AI-generated notes (source = AI AND micks_edit = false)
- Return chronologically (oldest first)
- Format: date | view_current | micks_summary

### Mode 3: Stock Query
"Everything about [TICKER]" or "full history [TICKER]"

- Return ALL notes for TICKER from all sources, all time
- Return chronologically (oldest first)
- Include source field in output

### Mode 4: Webinar Session
"What stocks came up in the [date] webinar?"

- Filter by source = IC Webinar AND date matching requested date
- Return: list of EPICs with view_current and micks_summary

### Mode 5: Sector Query
"What do I think about [sector]?"

- Filter by sector = [sector]
- Return most recent note per EPIC in that sector
- Return chronologically by date

## Output Format

### Single Note Result

```
[TICKER] - Company Name
Date: YYYY-MM-DD | Source: [source] | SP: [sp_start]p | MCap: [mcap]
View: [view_current]
Summary: [micks_summary]

---
[Full note content]
---
```

### Multiple Notes (Log / History)

```
[TICKER] History - [N] notes found

1. YYYY-MM-DD | [view_current] | [micks_summary]
2. YYYY-MM-DD | [view_current] | [micks_summary]
...

[Show full content of each note below, oldest first]
```

## File Parsing Rules

1. Use Filesystem:search_files to find .md files containing the EPIC
2. Read YAML frontmatter to get structured fields
3. Read body content below frontmatter
4. Sort results by `date` field in YAML (ascending = chronological)
5. If date field is missing, use file creation date as fallback

## Search Strategy

1. Primary: Filesystem:search_files with pattern `[TICKER]` in Micks-View folder
2. Secondary: Match filename containing TICKER (e.g. *-SLP-*.md)
3. Tertiary: Match `epic: TICKER` in YAML frontmatter

## IMPORTANT Rules

- Results ALWAYS returned chronologically (oldest first) - PRD v2.2 confirmed
- Mode 1 (Current View) is the DEFAULT if no mode specified
- NEVER modify files during a query operation
- If no notes found: "No Micks-View notes found for [TICKER]. Use micks-stocknote to add one."
- Case-insensitive matching for TICKER (SLP = slp = Slp)

## After Query

- Offer to add a new note (micks-stocknote)
- Offer to run a different query mode
- If view_current = Stop_Loss, highlight with warning

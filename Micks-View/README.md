# Micks-View
## Stock Intelligence System - Phase 1

Built: 2026-03-10 | PRD v2.2

---

## What Is This?

Micks-View is Mick's personal stock note system. It stores his views on
stocks and sectors as structured Obsidian markdown files with YAML frontmatter.

The system has two skills:
- micks-stocknote: Write a new stock note (brain dump or webinar extract)
- micks-view-query: Query existing notes by ticker, sector, date, or mode

---

## Folder Structure

  Micks-View/
    _templates/       Obsidian templates (sorted first in file browser)
    00-Inbox/         New notes land here. Review and file to 02-Areas.
    01-Projects/      Active investment research projects.
    02-Areas/
      Stocks/         One-per-ticker stock note files (after inbox review)
      Sectors/        Sector-level view notes
    03-Resources/     Reference docs, skill docs
    04-Archives/      Old or inactive notes

---

## File Naming Convention

All files: YYYY-MM-DD-[TICKER]-[slug].md

Example: 2026-03-10-SLP-quarterly-results.md

---

## YAML Fields (frozen per PRD v2.2)

epic           - Plain ticker. e.g. SLP
ticker         - Wikilink. e.g. "[[SLP]]"
company        - Full company name
date           - ISO date YYYY-MM-DD
source         - IC Webinar | Plaza | AI | Brain Dump | Research | News
sp_start       - Share price at time of note
mcap           - Market cap (thousands GBP)
exchanges      - List of exchange codes
sector         - Sector classification
view_current   - Watch | Positive | Negative | Shortlist | Stop_Loss
tags           - Multi-value list
micks_summary  - 200 char MAX plain text summary
micks_edit     - false = AI. true = Mick has reviewed/edited
visibility     - private | members | public

---

## Query Modes (via micks-view-query)

1. Current View  - Most recent note + 90-day staleness check (default)
2. Micks-View Log - Full history, Mick-authored only
3. Stock Query   - Everything about a ticker, all time
4. Webinar Session - All stocks from a given webinar date
5. Sector Query  - Most recent view per ticker in a sector

Results always returned chronologically (oldest first).

---

## GitHub

This folder is under version control via the Dex vault GitHub backup.
Scope: full Dex-MickP root (confirmed PRD v2.2).

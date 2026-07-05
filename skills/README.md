# Mick's PAIDA Skills Library

This folder contains custom skills for Cedric (Mick's Personal AI Digital Assistant).

Skills are modular instruction sets that tell Claude how to perform specific repeatable
tasks. Each skill lives in its own subfolder with a SKILL.md file.

## Available Skills

| Skill | Command | Description |
|-------|---------|-------------|
| session-start | (automatic) | Mandatory session start protocol. Probe MCP availability via tool_search and announce environment (Claude Desktop vs claude.ai) before any other action. |
| ax-mapper | "map [app] with ax-mapper" or `/ax-mapper` | Generic READ-ONLY accessibility-tree UI mapper for ANY Playwright-drivable web app. Engine + per-app adapters (ShareScope is one adapter). Generalised fork of the ShareScope mapper. Offline-tested (15 checks pass); live harvest is a Desktop task. Created 2026.07.04. |
| sharescope-start | "sharescope start" or `/sharescope-start` | ShareScope session opener. Connects vault + project folder, reads PICKUP_POINT.md and CEDRIC_MEMORY.md, delivers a clean briefing so work resumes immediately. Created 2026.04.26. Mirror: TODO (Claude Desktop session needed). |
| sharescope-financials | "download [TICKER] financials" or `/sharescope-financials [TICKER]` | Financial data export for any ShareScope stock. Gives PowerShell command, verifies 6 CSV files land in downloads\{TICKER}\, reports back with filenames. Created 2026.04.26. Mirror: TODO (Claude Desktop session needed). |
| pns | `/pns` | Post Notion Summary: reads a Notion page, generates a 200-word structured summary, posts it to the Summary (item) property field. Adapts headings to content type (financial results, trading updates, articles). |
| notion-summary | (on request) | Notion announcement summary via BROWSER CONTROL. Uses get_page_text, clicks the Summary (item) field, types with Ctrl+B for bold headings and Shift+Enter for line breaks. Max 200 words. Use in Claude Code or Claude in Chrome. See note below on two-skill distinction. |
| week-plan-print | `/week-plan-print` | Generates a formatted, print-ready one-page A4 Word document (.docx) showing the full week's calendar for printing and pinning on the wall. Pulls live Google Calendar data. |
| process-webinar | `/process-webinar` | Processes a single Inner Circle Webinar PDF: extracts company slides, infers verdicts from commentary, writes entries to Radar Log and AI Company Research in Notion. |
| batch-process-webinars | `/batch-process-webinars` | Batch version of /process-webinar. Processes an entire archive folder of IC Webinar PDFs in sequence, skipping duplicates and logging results. |
| my-view-writer | `/my-view-writer` | Writes or updates the "My View" narrative field on Radar Log entries in Notion, based on OCR-extracted commentary from webinar PDF slides. |
| thumbnail-play-button | (on request) | Add a YouTube-style play button overlay to any image thumbnail. Use for newsletter images, WordPress posts, or any document where a thumbnail should indicate a clickable video link. |
| yt-weekly-stats | (on request) | Update DIY Investors YouTube channel stats in the tracking Google Sheet. NOTE: enter data cell-by-cell via Name Box - tab-separated entry does not work in browser Sheets (updated 2026.03.14). Mirrored to /mnt/skills/user/yt-weekly-stats/ as of 2026.03.14. |
| sharescope-nlm-research | `/research [TICKER]` or "research [company]" or "Cedric, research [company]" | Full ShareScope + NotebookLM financial research pipeline (v1.0). Resolves ticker, checks NLM auth, runs orchestrator (~28s, headless, 6 CSVs), runs NLM researcher (parallel upload + news search, Nina analysis), monitors Research Log for report file, returns Obsidian deep-link. Also handles voice-activated runs. Replaces old stock-research skill. Created 2026.04.28. Dual-deployed: vault + .claude/skills mirror. Slash command: .claude/commands/research.md |
| logo-masking | "mask the logo", "remove the NotebookLM logo", "remove the branding", "clean up this slide" | Remove watermarks and branding logos from PNG/JPG images using auto-sampled colour matching. Designed for NotebookLM infographics (bottom-right logo) but works on any corner. Supports single file and batch processing. Tested 2026.04.29 on 2x NotebookLM infographics at 2752x1536. |
| portfolio-post-creator | (monthly portfolio batch) | Orchestrator for the four DIY Investors monthly portfolio posts. Reads ShareScope screenshots, runs calculations, builds HTML post bodies, hands off to the publisher. Calls benchmark-fetcher and wordpress-image-uploader. Migrated from Poster Pete project 2026.05.30. |
| benchmark-fetcher | (called by portfolio-post-creator) | Fetch month-end FTSE All-Share + S&P 500 closes from Yahoo Finance and update the Indices Monthly Performance spreadsheet. Migrated from Poster Pete project 2026.05.30. |
| wordpress-image-uploader | (called by portfolio-post-creator) | Find portfolio screenshots on the PC and upload to the WordPress media library; returns real media IDs and pixel dimensions. Migrated from Poster Pete project 2026.05.30. |
| wordpress-post-publisher | (called by portfolio-post-creator, or ad-hoc) | Push post objects to WordPress as drafts via the REST API. Content-agnostic and reusable. Migrated from Poster Pete project 2026.05.30. |

## IMPORTANT: Two Notion Summary Skills

There are two distinct skills for summarising announcements and posting to Notion.
They serve different environments and use different methods. Do not confuse them.

### notion-summary (browser-control version)
- **Vault location:** `skills/notion-summary/SKILL.md` (added 2026.04.18)
- **MCP mirror:** `/mnt/skills/user/notion-summary/SKILL.md`
- **Method:** Browser automation. Uses `get_page_text` to read the page, then clicks
  the Summary (item) field and types the summary using keyboard shortcuts:
  Ctrl+B to toggle bold for headings, Shift+Enter for line breaks within the field.
- **Use when:** Running in Claude Code or Claude in Chrome where browser control is available.
- **Bold formatting:** Works correctly - Ctrl+B produces actual bold text in Notion.
- **Bullet points:** Typed directly as bullet (bullet) characters.

### notion-summary-generator (Notion MCP version)
- **Vault location:** NOT YET IN VAULT - MCP mirror only (to be added)
- **MCP mirror:** `/mnt/skills/user/notion-summary-generator/SKILL.md`
- **Method:** Uses Notion MCP tools directly. `notion-fetch` to read the page,
  `notion-update-page` to write the summary to the Summary (item) property field.
- **Use when:** Running in Claude Desktop with Notion MCP connected. No browser needed.
- **Bold formatting:** Does NOT render visually - Summary (item) is a plain text property.
  Bold markers (**text**) are included for readability in raw text only.
- **Bullet points:** Preserved and display correctly in Notion.

Both skills produce a structured summary of max 200 words with adapted section headings
(Financial Highlights, Financial Position, Operations, Key Developments, or equivalent).

## How Skills Work

When Cedric (Claude) is asked to perform a task, it checks for a relevant skill file
and follows the documented workflow. This ensures consistent, verified execution
every time.

## Adding New Skills

Each skill requires:
- A subfolder named after the skill (e.g. `skills/my-skill-name/`)
- A `SKILL.md` file inside it with the standard frontmatter and workflow
- An entry in this README table
- A copy placed in `/mnt/skills/user/` to mirror for claude.ai sessions

## Skill Locations

Skills are stored in two places for universal availability:

1. **This vault** (`skills/`): Version-controlled, available to Claude Desktop,
   Claude Code, Cowork, and any tool with filesystem access to this vault.

2. **Mounted skills directory** (`/mnt/skills/user/`): Available to Claude in the
   browser (claude.ai) and Claude in Chrome sessions.

Both locations must be kept in sync when creating or updating skills.

# Product Requirements Document
# ax-trees-automation -- DIY Investors Browser Automation Library

**Version:** 1.0
**Owner:** Mick Pavey (Ditty Box Ltd / DIY-Investors)
**Built with:** Cedric (PAIDA) + Archie (Accessibility Trees specialist)
**Created:** 2026-05-01
**Last Updated:** 2026-05-01

---

## 1. Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-05-01 | Initial PRD written. Structure agreed, Task 1 complete. |

---

## 2. Project Purpose and Vision

### What This Project Is

ax-trees-automation is a growing library of browser automation tools that gives
Cedric (Mick's Personal AI Digital Assistant) the ability to operate web-based
investing applications autonomously.

The tools are built using Playwright and accessibility trees (AX trees) -- the
structured data representation of what a browser page contains. AX trees are
preferred over CSS selectors or XPath because they are more stable, more
readable, and closer to how a human actually navigates a page.

### Why It Exists

Mick currently performs a number of time-consuming manual routines in web apps:

- Pulling financial metrics from ShareScope for stock research reports
- Taking portfolio screenshots for webinar preparation
- Running stock screens and watchlist reviews
- Checking dividend data, sector filters, and forecast tables

These routines follow fixed patterns. They are ideal candidates for automation.
Once automated, each routine becomes a callable skill -- available to Cedric,
to research agents, and eventually to DIY-Investors members.

### The Vision

Every manual investing routine that follows a fixed pattern becomes a skill.
Skills are globally callable -- verbally ("Cedric, get me the ShareScope metrics
for ENQ") or by an automated agent running a research pipeline.

The library starts with ShareScope and expands to Stockopedia and other platforms
as each is proven. Completed skills may eventually be packaged as a distributable
plugin for DIY-Investors members.

---

## 3. Primary Use Cases

### 3.1 ShareScope Automation

ShareScope is Mick's primary stock research and portfolio management platform.
It is the first target for this project.

**Planned mini-projects (in priority order):**

| ID | Project | Output Skill | Purpose |
|----|---------|-------------|---------|
| SS-01 | Login automation | sharescope-login.js | Foundation for all other ShareScope skills |
| SS-02 | Key metrics extraction | sharescope-get-metrics.js | CSV-to-markdown pipeline for stock research |
| SS-03 | Portfolio screenshot | sharescope-portfolio-screenshot.js | Weekly and month-end portfolio images |
| SS-04 | Stock filter by sector | sharescope-stock-filter.js | Screen by sector, yield, or other criteria |
| SS-05 | Chart screenshot | sharescope-get-chart.js | Pull stock chart into output markdown |

See mini-projects/MINI-PROJECTS-MASTER.md for full status tracking.

### 3.2 Stockopedia Automation (Future)

Stockopedia is the secondary target. Work begins once ShareScope skills are
stable and proven. Planned as SP-01 (login) followed by data extraction skills.

### 3.3 Shared Utilities

Cross-app skills that every automation routine depends on:

| ID | Skill | Purpose | Status |
|----|-------|---------|--------|
| SH-01 | delay-helper.js | Human-paced random delays (anti-bot) | Complete |

---

## 4. Technical Approach

### 4.1 Playwright + Accessibility Trees

All automation is built with Playwright (Node.js / JavaScript). Two modes:

- **Playwright MCP** -- for interactive, Claude-supervised sessions. Used during
  development and exploration. Cedric reads the AX tree and navigates live.

- **Playwright CLI** -- for production-ready skills. Scripts run independently
  at the command line or on a schedule. Claude is not involved at runtime.

Accessibility trees (snapshot mode) are the primary navigation method. They are
captured via Playwright's `page.accessibility.snapshot()` and used to identify
form fields, buttons, links, and data elements without brittle CSS selectors.

Per-app guidelines files document the confirmed selectors, login flows, known
quirks, and AX tree patterns for each platform. See sharescope/sharescope-guidelines.md.

### 4.2 JavaScript (Node.js)

All scripts are written in JavaScript. The existing Python scripts in the
predecessor project (04-Projects/2026.04.04-ShareScope-Automation/) are
candidates for rewriting in JS as part of the migration to this library.

Reasons for JS over Python:
- Playwright's native language is JavaScript
- Node.js integrates tightly with the Playwright CLI
- Consistent language across all skills simplifies maintenance

### 4.3 The Sandwich Model

Every automation follows the same three-part structure:

  [LOGIN] --> [TASK SKILL] --> [LOGOUT]

Login and logout are the bread -- fixed, independently testable, unchanged
regardless of the task. The filling is the skill. This means new skills can
be added without touching the login or logout code.

The orchestrator (a thin runner script) calls all three in sequence.

### 4.4 Headless vs Headed Mode

All scripts support both modes, controlled by a single .env flag:

  SHARESCOPE_HEADLESS=false   -- browser is visible (development / debugging)
  SHARESCOPE_HEADLESS=true    -- browser runs silently (production / scheduled)

---

## 5. Skills Architecture

### 5.1 Global Skills

All finished, proven automation skills live in the root skills/ folder.
No skill is buried inside an app folder (sharescope/, stockopedia/, etc.).
App folders contain only AX trees and guidelines.

This means any agent or verbal instruction can invoke any skill without
needing to know which app it relates to.

### 5.2 Skills Index

skills/SKILLS-INDEX.md is the master catalogue. It documents every skill:
- Name and file path
- What it does
- Required inputs (env vars, parameters)
- What it outputs
- How to call it (CLI command or verbal trigger)

When an agent needs to decide which skill to invoke, it reads this index first.

### 5.3 Promotion Pipeline

A script begins life inside a mini-project subfolder (mini-projects/[name]/).
Once proven and tested, it is promoted to skills/ and the SKILLS-INDEX is updated.
The mini-project PROGRESS.md is updated to mark the skill as complete.

---

## 6. Output Format

### 6.1 Obsidian Markdown

All data outputs are saved as .md files in outputs/ with YAML frontmatter.
Templates are in templates/ -- use them for every new output type.

### 6.2 YAML Frontmatter Standard

Every output file must include:

  ---
  title: [descriptive title]
  date: YYYY-MM-DD
  ticker: [TICKER]
  source: [app name]
  author: AI
  tags: [relevant tags]
  ---

The author: AI field is mandatory. It distinguishes AI-generated files from
files Mick has written himself. This matters for search, filtering, and trust.

### 6.3 Outputs Folder

outputs/ is committed to GitHub (unlike auth/ and screenshots/debug/).
This means outputs build up as a searchable archive over time.

---

## 7. Anti-Bot Principles

Operating at machine speed is not acceptable. All scripts must apply human-paced
random delays between browser actions.

The shared delay-helper.js provides this utility. Import it into every script:

  import { randomDelay } from '../skills/delay-helper.js';
  await randomDelay(800, 2500);

Minimum delay between actions: 500ms.
Typical range: 800-2500ms.
Page load waits: 2000-5000ms.
Never hardcode a fixed delay -- always use a random range.

---

## 8. Credentials and Security

### 8.1 The .env File

All credentials and configuration live in a single .env file. This file:
- Lives in C:\Vaults\Mick's Vault\ (outside the GitHub-committed vault)
- Is never committed to git (enforced by .gitignore)
- Is never shared or logged

.env.example at the project root documents the required variable names
without values. Anyone setting up the project references this file.

### 8.2 Reference in Scripts

Scripts reference credentials via process.env.VARIABLE_NAME only.
Credentials are never hardcoded, never logged, never printed to console.

---

## 9. Project Management

### 9.1 Mini-Projects Tracker

mini-projects/MINI-PROJECTS-MASTER.md is the master to-do list.
Every automation project has a row. Status is updated by Claude as work progresses.
New ideas are added to the Ideas Backlog at the bottom.

### 9.2 Per-Project Progress Files

Each mini-project has its own subfolder with a PROGRESS.md file.
Cedric ticks off tasks in PROGRESS.md as they are completed.
This is the resume point after a break between sessions.

### 9.3 Session Logs

session-logs/ contains a full log of every working session.
The log documents: what was done, what decisions were made, what is deferred.
The "How to Pick Up" section at the bottom of each log tells the next session
exactly what to read and where to start.

### 9.4 GitHub Backup

The entire ax-trees-automation folder is committed to GitHub automatically
each evening at 9pm. This means:
- No work is ever lost between sessions
- The full history of scripts and structure is preserved
- Skills are version-controlled

---

## 10. Folder Structure

  ax-trees-automation/
  |
  +-- CLAUDE.md                      Global rules (anti-bot, credentials, JS only)
  +-- README.md                      Project overview
  +-- PRD.md                         This document
  +-- memory.md                      Running project memory and decisions log
  +-- .env.example                   Documents required variable names
  +-- .gitignore                     Excludes: .env, node_modules/, auth/,
  |                                  screenshots/debug/
  +-- package.json                   Node project config
  +-- playwright.config.js           Central Playwright config
  |
  +-- skills/                        ALL finished skills live here
  |   +-- SKILLS-INDEX.md            Master catalogue (agents read this first)
  |   +-- delay-helper.js            Anti-bot random delay utility [COMPLETE]
  |   +-- sharescope-login.js        (to be created - SS-01)
  |   +-- sharescope-get-metrics.js  (to be created - SS-02)
  |   +-- ...
  |
  +-- mini-projects/                 Workshop -- one folder per automation project
  |   +-- MINI-PROJECTS-MASTER.md    Master to-do list
  |   +-- sharescope-login/
  |   |   +-- PROGRESS.md            Claude ticks off tasks here
  |   |   +-- notes.md
  |   +-- sharescope-metrics-extraction/
  |   +-- portfolio-screenshots/
  |   +-- sharescope-stock-filter/
  |
  +-- templates/                     YAML output templates
  |   +-- chart-output-template.md
  |   +-- portfolio-output-template.md
  |   +-- metrics-output-template.md
  |
  +-- outputs/                       Committed to GitHub
  |   +-- charts/
  |   +-- portfolios/
  |   +-- metrics/
  |
  +-- screenshots/
  |   +-- debug/                     Gitignored - Playwright debug only
  |
  +-- auth/                          Gitignored - saved browser sessions
  |
  +-- session-logs/                  Full session logs
  |   +-- 2026-05-01-session.md
  |   +-- summaries/
  |
  +-- plugin/                        Future distributable plugin placeholder
  |   +-- README.md
  |
  +-- sharescope/                    AX trees + guidelines (no skills here)
  |   +-- sharescope-guidelines.md
  |   +-- sharescope-ax-tree-master.md
  |   +-- versions/
  |       +-- [dated AX tree snapshots]
  |
  +-- stockopedia/                   When needed
      +-- stockopedia-guidelines.md
      +-- versions/

---

## 11. Migration from Predecessor Project

A predecessor project exists at:
  C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\

It contains proven Python scripts and AX tree reference files from Phase 1
testing (login confirmed, session key mechanism confirmed, selectors confirmed).

The migration plan (Task 3) will:
1. Read every file in the predecessor project
2. Map each file to its destination in this structure
3. Decide: migrate as-is, rewrite in JS, or archive
4. Create PROGRESS.md files in the relevant mini-project subfolders
5. Update sharescope/sharescope-ax-tree-master.md with confirmed selectors

Migration is tracked in mini-projects/MINI-PROJECTS-MASTER.md.

---

## 12. Distribution and Plugin (Future)

The plugin/ folder is a placeholder for future packaging of this library
as a distributable plugin for DIY-Investors members.

This is not in scope for current development. It becomes relevant once
several skills are stable and Mick is ready to share the automation toolkit
with Inner Circle members who want to run their own ShareScope pipelines.

---

## 13. Related Resources

| Resource | Location |
|----------|---------|
| Predecessor project | 04-Projects/2026.04.04-ShareScope-Automation/ |
| ShareScope PRD v2.0 | C:\Vaults\Cowork\2026.04.26 - PRD - ShareScope Browser Automation System v2.0.docx |
| Meet Cedric series (Notion) | https://app.notion.com/p/353db32a9b0a81018396c00fb2378db4 |
| Archie knowledge base | Claude project -- Accessibility Trees Scraping Information |
| ShareScope pipeline doc | C:\Vaults\Cowork\2026.04.28 - ShareScope NLM Pipeline - How It Works.md |

---

## 14. Open Questions

| Question | Status |
|----------|--------|
| Scheduling approach for production runs | Open -- Windows Task Scheduler vs Python schedule vs n8n |
| GitHub repo: private or separate from main vault repo? | Open -- to be confirmed |
| Plugin format for member distribution | Open -- deferred until skills library is mature |

---

*PRD v1.0 | ax-trees-automation | Mick Pavey + Cedric PAIDA | 2026-05-01*

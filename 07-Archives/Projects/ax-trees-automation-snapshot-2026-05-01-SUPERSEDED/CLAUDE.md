# CLAUDE.md - ax-trees-automation

**Project:** DIY Investors Accessibility Tree Automation
**Owner:** Mick (Ditty Box Ltd / DIY-Investors)
**Started:** 2026-05-01
**Status:** Active development

---

## What This Project Is

A structured library of browser automation tools built using Playwright (MCP and CLI)
and accessibility trees (AX trees). The goal is to automate DIY Investing routines
that Mick currently does manually -- things like extracting metrics, taking portfolio
screenshots, and running stock filters.

Each automation routine is a mini-project that results in a callable skill.
Skills are globally available and can be called verbally via Claude or by a research agent.

---

## Global Rules (Apply to All Apps and Scripts)

### 1. Anti-Bot Delays (MANDATORY)
Never operate at machine speed. Always apply human-paced random delays between
browser actions. Use the shared delay-helper.js in skills/:

  import { randomDelay } from '../skills/delay-helper.js';
  await randomDelay(800, 2500); // ms range

Minimum delay: 500ms. Typical range: 800-2500ms. Longer for page loads (2000-5000ms).

### 2. Credentials (MANDATORY)
All credentials live in the .env file outside the GitHub-committed vault.
The .env.example at this root documents variable names. Never hardcode credentials.
Never commit real credentials. Reference via process.env.VARIABLE_NAME only.

### 3. Skills Are Global
All finished, proven automation skills live in skills/ at this root.
No skill lives inside an app folder (sharescope/, stockopedia/, etc.).
App folders contain AX trees and guidelines only.

### 4. JavaScript / Playwright
Scripts use JavaScript (Node.js) with Playwright. Both Playwright MCP and
Playwright CLI are available -- check the app guidelines file for which is
preferred per app.

### 5. Outputs Are Obsidian Markdown
All data outputs are .md files with YAML frontmatter. Use templates in templates/.
Include author: AI in all YAML to distinguish from manually-created files.

### 6. Plan Mode First
Before writing any new script or skill, discuss and agree the approach.
Reference Archie (Accessibility Trees knowledge base) for best practice.

---

## App-Specific Guidelines

For rules, quirks, login flows, and known issues specific to each application,
read the relevant guidelines file before starting work:

- ShareScope: sharescope/sharescope-guidelines.md
- Stockopedia: stockopedia/stockopedia-guidelines.md (when created)

---

## Key Files

| File | Purpose |
|------|---------|
| skills/SKILLS-INDEX.md | Master catalogue of all available skills |
| mini-projects/MINI-PROJECTS-MASTER.md | Master to-do list for all automation projects |
| PRD.md | Product Requirements Document |
| memory.md | Running project memory and decisions log |
| session-logs/ | Full session discussion logs |
| .env.example | Documents required environment variable names |

---

## Folder Structure Reference

See README.md for the full annotated folder structure.

---

## Related Projects

- Existing ShareScope automation: 04-Projects/2026.04.04-ShareScope-Automation/
  (migration to this folder is in progress -- see mini-projects/MINI-PROJECTS-MASTER.md)
- Meet Cedric YouTube series: ShareScope sub-series documented in Notion Content Studio
- Plugin (future): plugin/ folder -- for member distribution via DIY-Investors

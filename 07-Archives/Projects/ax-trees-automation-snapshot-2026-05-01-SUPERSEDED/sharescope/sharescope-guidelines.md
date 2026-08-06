# ShareScope - App Guidelines

Read this file before starting any ShareScope automation work.
Referenced by root CLAUDE.md.

**Last Updated:** 2026-05-01

---

## About ShareScope

ShareScope is a UK desktop/web-based stock analysis platform.
Mick holds a paid subscription - automation is for legitimate personal use only.
URL: (see .env - SHARESCOPE_URL)

---

## Authentication

- Credentials stored in .env as SHARESCOPE_USERNAME and SHARESCOPE_PASSWORD
- Existing login automation lives in 04-Projects/2026.04.04-ShareScope-Automation/
- Auth session can be saved to auth/ to avoid repeated logins (see Playwright docs)
- If session expires, re-run login skill before any other skill

---

## Playwright Approach

- **Preferred:** Playwright MCP for interactive/exploratory sessions
- **Preferred:** Playwright CLI (JS scripts) for scheduled/repeatable automations
- ShareScope uses JavaScript-heavy pages - always wait for network idle after navigation
- Use page.waitForLoadState('networkidle') after page.goto()

---

## Known Quirks and Gotchas

- ShareScope loads data asynchronously - do not assume data is present after page load
- Use accessibility tree snapshots (browser_snapshot) to inspect element state
- Ticker disambiguation: ShareScope covers both LSE and NASDAQ.
  e.g. COST = Costain Group (LSE) AND Costco (NASDAQ) - always verify exchange
- Stock search: use regex pattern :{TICKER}\b to match exchange-prefixed results
  e.g. LSE:SQZ, AIM:SQZ -- avoids matching Historical entries

---

## AX Tree Reference Files

| File | Contents |
|------|---------|
| sharescope-ax-tree-master.md | Current master accessibility tree snapshot |
| versions/ | Dated historical versions |

When the AX tree changes (ShareScope updates), create a new dated version in versions/
and update the master file.

---

## Existing Work (Pre-Migration)

The following scripts exist in 04-Projects/2026.04.04-ShareScope-Automation/
and are candidates for migration to skills/:

- sharescope_login.py - login (Python, needs JS rewrite)
- sharescope_export.py - CSV data export
- sharescope_search.py - stock search with AX tree approach
- sharescope_screenshot.py - screenshot capture
- sharescope_orchestrator.py - pipeline orchestrator

Migration plan: see mini-projects/MINI-PROJECTS-MASTER.md

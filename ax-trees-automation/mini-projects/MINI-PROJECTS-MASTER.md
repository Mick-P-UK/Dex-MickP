# Mini-Projects Master Tracker

This is the master to-do list for all automation mini-projects.
Each mini-project results in one or more skills in skills/.
Add new ideas here as they come up -- they will be prioritised and tackled in order.

**Last Updated:** 2026-05-01 (Task 3 - migration survey complete)

---

## Status Key

- [ ] Not started
- [~] In progress
- [x] Complete - skill live in skills/

---

## ShareScope Mini-Projects

| # | Project | Skill(s) Produced | Status | Notes |
|---|---------|-------------------|--------|-------|
| SS-01 | Login automation | sharescope-login.js | [ ] | Predecessor: sharescope_login.py (310 lines, working). JS rewrite needed. |
| SS-02 | Key metrics extraction | sharescope-get-metrics.js | [ ] | Predecessor: sharescope_search.py + sharescope_export.py (working, 12 companies run). Depends on SS-01. |
| SS-03 | Portfolio screenshot (weekly/monthly) | sharescope-portfolio-screenshot.js | [ ] | Scheduled automation. Portfolio nav selector confirmed (JS click on anchor). |
| SS-04 | Stock filter by sector | sharescope-stock-filter.js | [ ] | e.g. all LSE oil stocks paying dividends |
| SS-05 | Chart screenshot extraction | sharescope-get-chart.js | [ ] | Pull chart image into output markdown |

---

## Stockopedia Mini-Projects

| # | Project | Skill(s) Produced | Status | Notes |
|---|---------|-------------------|--------|-------|
| SP-01 | Login automation | stockopedia-login.js | [ ] | To be started when ShareScope stable |

---

## Shared / Cross-App Mini-Projects

| # | Project | Skill(s) Produced | Status | Notes |
|---|---------|-------------------|--------|-------|
| SH-01 | Delay helper utility | delay-helper.js | [x] | Complete - live in skills/ |

---

## Ideas Backlog (Not Yet Scheduled)

Add new automation ideas here as they come up:

- Monthly portfolio snapshot archive (automated end-of-month run)
- Sector watchlist filter (multiple sectors + metric combinations)
- Dividend yield screener across LSE universe
- Logout skill as standalone (sharescope-logout.js -- predecessor exists: sharescope_logout.py)

---

## Migration Status (from 04-Projects/2026.04.04-ShareScope-Automation/)

Survey completed 2026-05-01. Key findings:

The predecessor project is substantially more advanced than expected.
The full pipeline (login -> search -> 6 CSVs -> NLM upload -> Nina analysis -> report
saved to Research Log -> Notion entry created) is working in Python as of 2026-05-01.
12 companies have been processed (SQZ, GGP, ACMR, HAL, ENQ, HBR, COST, XPP, EDV,
TEP, COIN, SRB).

### Files in Predecessor Project

| File | Lines | Destination | Action |
|------|-------|-------------|--------|
| sharescope_login.py | 310 | SS-01 reference | Read, rewrite in JS |
| sharescope_search.py | ? | SS-02 reference | Read, rewrite in JS |
| sharescope_export.py | ? | SS-02 reference | Read, rewrite in JS |
| sharescope_logout.py | 160 | Logout skill reference | Read, rewrite in JS |
| sharescope_screenshot.py | 180 | SS-03 reference | Read, adapt in JS |
| sharescope_orchestrator.py | 280 | Orchestrator reference | Adapt to JS orchestrator |
| sharescope_nlm_researcher.py | large | Stay in Python | Complex NLM pipeline -- do NOT rewrite yet |
| sharescope_research_log.py | ? | Stay in Python | Research Log management -- leave in Python |
| sharescope_utils.py | ? | Review | Check for reusable utilities |
| sharescope_watcher.py | ? | Stay in Python | File watcher service -- leave in Python |
| voice_listener.py | ? | Future | Voice command listener -- future scope |
| sharescope_browser_run.js | ? | Review | Already JS -- check if reusable |

### AX Tree References -- Migrated

| Original file | Migrated to |
|---------------|-------------|
| ShareScope-Login-Accessibility-Reference.md | sharescope/sharescope-ax-tree-master.md (Section 1) |
| ShareScope-Export-Accessibility-Reference.md | sharescope/sharescope-ax-tree-master.md (Sections 3-6) |

Dated copies in: sharescope/versions/ (to be copied)

### Strategy Decision (2026-05-01)

Do NOT attempt a full rewrite of the Python pipeline.
The NLM integration, Research Log, and Notion publishing are complex, working,
and not broken. Leave them in Python.

FOCUS for this project:
- Rewrite the BROWSER INTERACTION layer in JS (login, search, export, screenshot)
- These become the callable skills in skills/
- The Python pipeline can call the JS skills via subprocess if needed
- Or the JS skills can operate independently for standalone use cases

---

## Notes

- Mini-projects have their own subfolder in mini-projects/ with PROGRESS.md
- When a skill is marked [x] complete, update SKILLS-INDEX.md
- PRD.md contains the full product requirements for this project
- Predecessor project stays intact at 04-Projects/ -- do not delete

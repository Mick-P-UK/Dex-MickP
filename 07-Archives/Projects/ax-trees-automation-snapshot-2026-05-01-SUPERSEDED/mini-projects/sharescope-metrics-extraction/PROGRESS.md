# SS-02: ShareScope Metrics Extraction (JS)
# Mini-Project Progress Tracker

**Output skill:** skills/sharescope-get-metrics.js
**Status:** [ ] Not started
**Depends on:** SS-01 (sharescope-login.js must be complete first)
**Last updated:** 2026-05-01

---

## Context

Working Python scripts exist in the predecessor project:
  04-Projects/2026.04.04-ShareScope-Automation/sharescope_search.py
  04-Projects/2026.04.04-ShareScope-Automation/sharescope_export.py
  04-Projects/2026.04.04-ShareScope-Automation/sharescope_orchestrator.py

These are the core of the pipeline -- they search for a stock by ticker,
navigate to its financials panel, and export 6 CSVs. This mini-project
rewrites them as a single callable JS skill.

The pipeline has been running in production (Python) since late April 2026
and has processed 12 companies. The selector logic is confirmed working.

---

## What the Skill Must Do

1. Accept ticker symbol as input (e.g. "SQZ", "HAL", "COIN")
2. Click button "Search" to open the "Find a share" dialog
3. Set combobox to "All instruments" (CRITICAL -- see quirks)
4. Clear search field, then pressSequentially(ticker, delay: 100)
5. Wait for results to appear dynamically
6. Click the result matching the target ticker (LSE:TICKER or exchange:TICKER)
7. Click button "OK" -- wait for financials panel to update
8. For each of 6 tabs (Income, Balance, Cash, Ratios, Dividends, Forecasts):
   a. Click tab button
   b. Wait for tab to load
   c. Click button "Sharing"
   d. Set up download listener BEFORE clicking Export
   e. Click "Export data..." -- file downloads immediately
   f. Save to outputs/metrics/{TICKER}/YYYYMMDD-{TICKER}-{tabname}.csv
9. Return: list of downloaded CSV file paths

---

## Selector Reference

All confirmed selectors are in:
  sharescope/sharescope-ax-tree-master.md (Sections 3, 4, 5)

Critical gotchas:
  - Combobox: locator('#find-share-dlg-list').selectOption('All instruments')
  - Search: getByRole('searchbox').pressSequentially(ticker, {delay: 100})
  - Forecasts: use .first() if multiple matches
  - Download: Promise.all([page.waitForEvent('download'), click]) pattern
  - Browser context: must have acceptDownloads: true

---

## Script Requirements (from CLAUDE.md)

- Import randomDelay from skills/delay-helper.js
- Apply delays between tab clicks (simulate reading/thinking time)
- SHARESCOPE_HEADLESS flag documented in header
- Full header comment block
- Credentials via process.env only
- Error screenshot on failure

---

## Output File Naming

Save CSVs to:
  ax-trees-automation/outputs/metrics/{TICKER}/

Filename format:
  YYYYMMDD-{TICKER}-income.csv
  YYYYMMDD-{TICKER}-balance.csv
  YYYYMMDD-{TICKER}-cash.csv
  YYYYMMDD-{TICKER}-ratios.csv
  YYYYMMDD-{TICKER}-dividends.csv
  YYYYMMDD-{TICKER}-forecasts.csv

These will then be picked up by the NLM pipeline (downstream).

---

## Tasks

- [ ] Read sharescope_search.py (understand search logic)
- [ ] Read sharescope_export.py (understand download handling)
- [ ] Write sharescope-get-metrics.js to skills/ folder
- [ ] Test: search SQZ, confirm 6 CSVs downloaded and named correctly
- [ ] Test: search HAL (US stock), confirm same flow works
- [ ] Test: invalid ticker -- confirm graceful error handling
- [ ] Update SKILLS-INDEX.md with sharescope-get-metrics entry
- [ ] Mark SS-02 as [x] complete in MINI-PROJECTS-MASTER.md

---

## Reference Files

- Predecessor scripts:
    04-Projects/2026.04.04-ShareScope-Automation/sharescope_search.py
    04-Projects/2026.04.04-ShareScope-Automation/sharescope_export.py
    04-Projects/2026.04.04-ShareScope-Automation/sharescope_orchestrator.py
- AX tree selectors: sharescope/sharescope-ax-tree-master.md (Sections 3, 4, 5)
- Download filenames: sharescope-ax-tree-master.md (Section 4, CSV table)

---

## Notes / Decisions

*(Add notes here as work progresses)*

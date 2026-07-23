---
name: sharescope-nlm-research
description: >
  Full ShareScope + NotebookLM financial research pipeline for any stock.
  Downloads six financial CSV files from ShareScope (income, balance, cash flow,
  ratios, dividends, forecasts), uploads them to a private NotebookLM notebook,
  runs a parallel news search, then asks Nina (the AI analyst) to write a full
  structured financial analysis report. Report is saved automatically to the
  Research Log in Obsidian. Use this skill whenever Mick says "/research [TICKER]",
  "research [company name]", "run a Nina report on [TICKER]", "do a report on
  [company]", "analyse [company] using ShareScope", "Cedric, research [company]",
  or any request to produce a ShareScope-backed financial analysis. Always use
  this skill for stock research -- do not attempt the pipeline manually without
  reading it first.
---

# Skill: sharescope-nlm-research

Full ShareScope + NotebookLM financial research pipeline.
Slash command: `/research [TICKER or company name]`
Output: Nina AI financial analysis report saved to Research Log (Obsidian vault).

---

## KEY PATHS

```
Project folder:  C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation
Research Log:    C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\06-Resources\Research-Log
Companies:       C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\06-Resources\Research-Log\Companies
Research:        C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\06-Resources\Research-Log\Research
```

All scripts run from the project folder. Never run them from elsewhere.

---

## STEP 0 -- RESOLVE TICKER AND COMPANY NAME

Extract the ticker or company name from the request.

If a ticker was given (e.g. HAL, SQZ, ACMR):
  - Normalise to uppercase.
  - Look for a matching Company Profile:
      C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\06-Resources\Research-Log\Companies\[TICKER] - *.md
  - If found, read the frontmatter to get `company_name` and `nlm_notebook_id`.
  - If not found, ask Mick: "I don't have a Company Profile for [TICKER] yet.
    What is the full company name? (e.g. Halliburton, ACM Research)"

If a company name was given (e.g. "Halliburton", "Serica"):
  - Scan the Companies folder for a filename containing that name (case-insensitive).
  - If found, extract the ticker from the filename prefix (e.g. HAL from "HAL - Halliburton.md").
  - If not found, ask: "I don't have [name] in the Research Log yet. What is the ticker code?"

Confirm before proceeding:
  "Running research on [TICKER] -- [Company Name]. Is that right?"

---

## STEP 1 -- PRE-FLIGHT CHECKS

Before giving any commands, run through these checks silently and report only issues.

### 1a. NLM Auth Status
Read: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\notebooklm_auth_status.json

If the file shows `"status": "expired"` or the file is missing, first attempt the
hands-off self-heal: run `notebooklm login` yourself. When the CLI's Chromium
profile session is still live it completes with no manual input ("Already logged
in.") and re-saves fresh auth; re-check and proceed silently. The pipeline's
`preflight_auth_check()` also does this automatically before halting. Only if the
self-heal does NOT recover it (login shows a Google sign-in page) tell Mick:
  "NotebookLM auth needs a manual login - open a terminal in the project
   folder and run: notebooklm login - then press ENTER after the browser confirms.
   Let me know when done."
  Wait for confirmation before proceeding.

If auth looks OK (or file shows valid/running), proceed silently.

### 1b. Watcher Status (optional check)
Read: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\watcher_heartbeat.json

This is informational only -- the pipeline does NOT depend on the watcher running.
If the watcher is running, mention it as a note. If not, no action needed.

### 1c. Existing Notebook Check
If a Company Profile exists and has a non-empty `nlm_notebook_id`:
  Tell Mick: "Found existing notebook for [TICKER] (ID: [nlm_notebook_id]).
  The pipeline will add new sources to that notebook."

If no Company Profile exists (new company):
  Tell Mick: "This is a new company -- a fresh NotebookLM notebook will be created."

---

## STEP 2 -- RUN THE ORCHESTRATOR (ShareScope CSV Download)

Tell Mick clearly:

"**Step 1 of 2 -- Downloading financials from ShareScope.**
Open a terminal, navigate to the project folder, and run:"

```
cd "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation"
python sharescope_orchestrator.py [TICKER]
```

"This will run silently (headless) for approximately 28 seconds and download
6 CSV files: income statement, balance sheet, cash flow, key ratios, dividends,
and forecasts. Let me know when it finishes."

### After Mick confirms it ran:

Check the downloads folder for today's CSV files:
  C:\Vaults\...\04-Projects\2026.04.04-ShareScope-Automation\downloads\[TICKER]\

Look for 6 files timestamped today. Confirm to Mick:
  "6 CSV files confirmed -- [TICKER] financials downloaded. Ready for Step 2."

If fewer than 6 files appear, or Mick reports an error, troubleshoot:
  - Login failure: check .env credentials (SHARESCOPE_USERNAME, SHARESCOPE_PASSWORD)
  - Timeout: ShareScope may be slow -- try running the orchestrator again
  - Wrong ticker: confirm the ticker is valid in ShareScope (try SQZ, not SERICA)

---

## STEP 3 -- RUN THE NLM RESEARCHER (Upload, News, Nina Analysis)

Tell Mick:

"**Step 2 of 2 -- Uploading to NotebookLM and generating the report.**
In the same terminal, run:"

```
python sharescope_nlm_researcher.py [TICKER] "[Company Name]"
```

Example (fill in actual values):
```
python sharescope_nlm_researcher.py HAL "Halliburton"
```

"Two things will happen in parallel:
  - The 6 CSV files will be uploaded to the NotebookLM notebook
  - A news search will fire for recent announcements and trading updates
Then Nina reads everything and writes the full analysis. This takes approximately
5-8 minutes. I will watch the Research Log for the report to appear."

### While it runs -- monitor for completion:

Poll for a new report file in:
  C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\06-Resources\Research-Log\Research\[TICKER]\

Watch for a file matching: YYYY.MM.DD - [TICKER] - [Company Name] - AI - Financial Analysis.md

Check every 30 seconds. When the file appears, tell Mick immediately:
  "Report saved. Click to open: [Obsidian deep-link]"

Build the Obsidian deep-link as:
  obsidian://open?path=C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\06-Resources\Research-Log\Research\[TICKER]\[filename]
  (URL-encode the path -- spaces become %20, backslashes become %5C)

If Mick confirms the terminal has finished but the file is not appearing after 2 minutes,
ask Mick to paste the last 10 lines of terminal output so we can diagnose.

---

## STEP 4 -- WRAP-UP

Once the report is confirmed:

1. Tell Mick the report is live and show the Research Log path:
   "Research-Log/Research/[TICKER]/[filename]"

2. If this was the company's first research run (no prior Company Profile),
   note: "Company Profile created in the Research Log -- [TICKER] is now indexed."

3. Ask (once, briefly):
   "Want me to log a Notion research entry for this one?"
   If yes: create a Notion page in the Research Database with title:
     YYYY.MM.DD - [Company Name] ([TICKER]): Cedric's Analysis
   If no: close the skill gracefully.

---

## TROUBLESHOOTING REFERENCE

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Orchestrator fails at login | Credentials or headless setting | Check .env: SHARESCOPE_USERNAME, SHARESCOPE_PASSWORD, SHARESCOPE_HEADLESS=true |
| Only 5 CSVs downloaded | One tab skipped (e.g. no forecasts) | Normal for some stocks -- proceed; Nina will note missing data |
| NLM researcher hangs at upload | Auth expired | Pipeline self-heals (preflight auto-runs `notebooklm login`); only if it cannot recover, run `notebooklm login` manually then retry |
| News search times out | Slow network or API limit | Pipeline continues without news -- still produces a report |
| Report file never appears | NLM phase failed | Ask Mick for last 10 lines of terminal output to diagnose |
| Obsidian link does not open | Vault not open in Obsidian | Open Obsidian first, then click the link |
| Report contains only "Error: Chat request timed out" | NLM ask timed out and error written to stdout | Re-run Step 2 only (CSVs still valid); pipeline now detects this and fails cleanly |
| Re-run overwrites a good same-day report | Duplicate filename from second run on same day | Fixed (2026.04.30): re-runs now save as _v2, _v3 etc. -- original is always preserved |
| News sources not appearing in NotebookLM notebook | research wait had no -n flag and targeted wrong context | Fixed (2026.04.30): pipeline now calls notebooklm use before research wait |

---

## BUG FIXES APPLIED (2026.04.30)

Three bugs were identified and fixed this session. All fixes are in sharescope_nlm_researcher.py
and sharescope_research_log.py. No changes needed to how you call the pipeline.

### Bug 1 -- News sources not loading into NotebookLM
File: sharescope_nlm_researcher.py -- add_news_via_fast_search()
Root cause: `notebooklm research wait` has no -n flag. It only monitors the current
notebook context (set via `notebooklm use`). The pipeline was passing -n to
`source add-research` (which worked) but then `research wait` had no context set
and silently monitored nothing. News sources were never imported. Non-fatal warning
was swallowed and the pipeline continued without news.
Fix: Added `notebooklm use notebook_id` call before the research sequence, so
`research wait --import-all` correctly targets the right notebook.

### Bug 2 -- Error message saved as report body
File: sharescope_nlm_researcher.py -- run_financial_analysis()
Root cause: `notebooklm ask` sometimes writes error messages to stdout (not stderr)
with a non-zero exit code. The old check was `if not ok and not stdout`, which passed
through when stdout contained "Error: Chat request timed out" -- treating it as success.
Fix: Added explicit error phrase detection in the response text. Added --new flag
to always start a fresh conversation (see Bug 3). Now returns failure cleanly.

### Bug 3 -- Stale conversation causes timeout on re-run
File: sharescope_nlm_researcher.py -- run_financial_analysis()
Root cause: `notebooklm ask` by default continues the last conversation. On a same-day
re-run, the stale conversation from the first run was resumed, causing NLM to time out.
Fix: Added --new flag to the ask command so every pipeline run starts a clean
conversation. No risk of stale context timeouts.

### Bug 4 -- Good report overwritten by failed re-run
File: sharescope_research_log.py -- save_research_item()
Root cause: No duplicate filename check. A same-day re-run generated the identical
filename and silently wrote the error output over the original successful report.
Fix: save_research_item() now checks for an existing file before writing. If one
exists, it saves as _v2, _v3 etc. The original is always preserved.

---

## VOICE-ACTIVATED ALTERNATIVE

If Mick says "Cedric, research [company]" from the voice listener, the pipeline
fires automatically via the file watcher. In this case:
- Skip Steps 2 and 3 above (the watcher handles those)
- Monitor Step 3's Research Log polling from the point Mick confirms the voice trigger fired
- The Obsidian link will still appear when the report lands

---

## COMPANIES IN THE RESEARCH LOG (as of 2026.04.30)

| Ticker | Company | NLM Notebook ID |
|--------|---------|-----------------|
| SQZ | Serica Energy | 0befe39a-d458-4392-9785-e2d808bafca9 |
| GGP | Greatland Gold | 7473143f-... |
| ACMR | ACM Research | ff97d932-6179-4a67-a7d8-f7f790f44a21 |
| HAL | Halliburton | 986322f7-8ddf-4ea0-ad03-86dc92fd3bfd |
| ENQ | Enquest | ade5f9e6-... |
| HBR | Harbour Energy | 1c91ef63-... |
| COST | Costain Group | 1deb3e2f-... |
| XPP | XP Power | (added 2026.04.29) |
| EDV | Endeavour Mining | 57014b58-830f-43bd-9c80-273bb64c1f71 (added 2026.04.30) |

For the current full list, read:
  C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\06-Resources\Research-Log\_index.md

---

## PHASE 2 NOTE (Member Distribution)

This skill is currently configured for Mick's machine (hardcoded paths).
A generalised, member-distributable version is planned for after the webinar.
That version will include a setup wizard and configurable paths.
Do not modify the paths above without Mick's instruction.

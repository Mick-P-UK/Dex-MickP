---
name: sharescope-nlm-upload
description: >
  Exports a stock's financial data from ShareScope (income statement, balance
  sheet, cash flow, ratios, dividends, forecasts) and uploads the CSVs as
  sources to an EXISTING NotebookLM notebook - upload only, no news search,
  no Nina report, never creates a notebook. Use this skill whenever Mick asks
  to "export [TICKER] financials into the notebook", "load [TICKER] data into
  the LM notebook", "upload the ShareScope CSVs to NotebookLM", "put the
  [TICKER] financials in my notebook", "add ShareScope data to the [TICKER]
  notebook", or "/sharescope-nlm-upload [TICKER]". For the FULL pipeline with
  news search and a Nina analysis report, use sharescope-nlm-research instead.
---

# Skill: sharescope-nlm-upload

Export ShareScope financials for a ticker and upload them into an existing
NotebookLM notebook. Data-in only - the notebook is otherwise untouched.

Slash command: /sharescope-nlm-upload [TICKER]

---

## WHEN TO USE THIS SKILL vs sharescope-nlm-research

| Request | Skill |
|---------|-------|
| "Export ZPHR financials into my notebook" | THIS skill (upload only) |
| "Research ZPHR" / "run a Nina report" | sharescope-nlm-research (full pipeline) |

This skill NEVER creates a notebook, NEVER adds news sources, and NEVER
generates a report. It is safe to point at a notebook Mick has curated by
hand - the only change is the added CSV sources.

---

## ARCHITECTURE NOTE (why Mick runs the commands)

Both scripts use headed Windows Playwright and the notebooklm CLI with
Mick's local auth, so they run in PowerShell on Mick's machine. Cedric
cannot execute them from the sandbox. Cedric's role: pre-flight checks,
give the exact commands, verify results from the mounted vault, and
confirm the sources landed in the notebook.

Key paths:

```
Project folder: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation
Downloads:      [project folder]\downloads\{TICKER}\
Companies:      C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\06-Resources\Research-Log\Companies
Upload script:  [project folder]\upload_csvs_to_nlm.py
```

---

## STEP 0 -- RESOLVE TICKER, COMPANY NAME AND NOTEBOOK

1. Extract the ticker from the request; normalise to uppercase.
2. Look for a Company Profile: Companies\[TICKER] - *.md
   - If found: read frontmatter for company_name and nlm_notebook_id.
   - If found WITH nlm_notebook_id: notebook resolves automatically - no
     URL needed from Mick.
   - If NOT found, or nlm_notebook_id empty: ask Mick for the company name
     (if unknown) and the NotebookLM notebook URL or ID. This skill must
     not create a notebook, so an existing one is required.
3. If Mick supplies a notebook URL/ID and no profile exists, CREATE the
   Company Profile so future runs resolve automatically (Cedric can do
   this directly from the sandbox - the vault is mounted):

```python
# run from the project folder with sys.path including it
from sharescope_research_log import create_company_profile
create_company_profile("ZPHR", "Zephyr Energy",
                       exchange="LSE:AIM",
                       nlm_notebook_id="<uuid>")
```

   Verify with get_company_profile(ticker) readback before proceeding.

4. Confirm: "Exporting [TICKER] - [Company Name] financials into notebook
   [id-prefix]... OK?"

---

## STEP 1 -- PRE-FLIGHT CHECKS (silent, report only issues)

1. NLM auth: read [project folder]\notebooklm_auth_status.json
   - status "ok": proceed silently.
   - status "expired" or file missing: ask Mick to run notebooklm login
     in a terminal first, and wait for confirmation.
2. Upload script exists: [project folder]\upload_csvs_to_nlm.py
   - If missing, stop and tell Mick (do not improvise a replacement).

---

## STEP 2 -- DOWNLOAD THE CSVs (Mick runs it)

Give Mick this exact block, substituting the ticker:

```
cd "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation"
python sharescope_orchestrator.py {TICKER}
```

Tell Mick: ShareScope opens in a browser window, exports the six
financial tabs, then closes - roughly 20-60 seconds. Wait for Mick to
confirm before moving on.

Then verify from the sandbox: check downloads\{TICKER}\ for CSVs
timestamped today. Six files is a full set; empty dividends/forecasts
files (under 10 bytes) are GENUINE for small caps, not an error - the
uploader skips them automatically. Report what landed.

---

## STEP 3 -- UPLOAD TO THE NOTEBOOK (Mick runs it)

If the Company Profile carries the notebook ID:

```
python upload_csvs_to_nlm.py {TICKER} "{Company Name}"
```

If Mick supplied a URL/ID this session (belt and braces - the third
argument accepts either the bare ID or the full URL):

```
python upload_csvs_to_nlm.py {TICKER} "{Company Name}" {NOTEBOOK_URL_OR_ID}
```

Expected output: found N CSV file(s), capacity check (X/50 sources),
"Done: N/N sources uploaded", then the notebook ID and clickable URL.

Source titles follow the pipeline convention:
  [PIPE] YYYY.MM.DD - {TICKER} {Tab Name} (ShareScope)

---

## STEP 4 -- VERIFY AND REPORT

1. Best: open the notebook URL via Claude in Chrome and confirm the new
   [PIPE] sources are listed in the Sources panel.
2. Fallback: rely on the script's "Done: N/N sources uploaded" plus the
   pre/post capacity arithmetic.
3. Report to Mick: sources uploaded (list tabs), any skipped-empty tabs,
   total sources now in the notebook, and the notebook URL.

---

## TROUBLESHOOTING

| Symptom | Cause | Fix |
|---------|-------|-----|
| "no existing notebook found" | No profile / no ID match | Ask Mick for the notebook URL; pass it as third argument; create the Company Profile for next time |
| Fewer than 6 CSVs | Empty tabs for small caps | Genuine - proceed; uploader skips empties |
| "notebooklm command not found" | CLI not on PATH | Run setup_notebooklm_windows.bat |
| Upload errors mention auth | Session expired | notebooklm login (30-second browser fix), retry Step 3 |
| Capacity error | Notebook at/near 50-source cap | Remove sources in NotebookLM, retry |
| Mick asks for "company summary" | Summary/Company tabs have no CSV export in ShareScope | Explain; offer text-source alternative or skip |

---

## HARD RULES

1. NEVER create a notebook from this skill. Existing notebooks only.
2. NEVER run the full researcher (news + Nina) from this skill - that is
   sharescope-nlm-research territory.
3. ASCII only in anything written to the vault.
4. Do not parse ShareScope manually or bypass the scripts - the AX Trees
   automation is the single source of truth for the export mechanics.

---

## Skill Metadata

Version:  1.0
Created:  2026.07.07
Author:   Cedric (PAIDA), built with Mick during the ZPHR notebook session
Depends:  sharescope_orchestrator.py, upload_csvs_to_nlm.py,
          sharescope_nlm_researcher.py (imported functions),
          sharescope_research_log.py, notebooklm CLI (Windows)
Vault:    C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\sharescope-nlm-upload\SKILL.md
Mirror:   /mnt/skills/user/sharescope-nlm-upload/SKILL.md (mirrored 2026.07.07
          from a claude.ai chat session with /mnt/skills/user mounted).
Cowork:   Installed as a Cowork skill 2026.07.07 via .skill package - live
          and auto-triggering in Cowork sessions.

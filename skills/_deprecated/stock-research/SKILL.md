---
name: stock-research
description: >
  Full ShareScope + NotebookLM financial research pipeline for a single stock.
  Checks for an existing NLM notebook, creates one if needed (prompting for
  permanent or temporary), triggers ShareScope CSV export, uploads data to NLM,
  runs Nina's financial analysis prompt, and saves a .md report to the vault.
  Use when Mick says "/stock-research", "run a research report on [TICKER]",
  "analyse [COMPANY] using ShareScope", "do a Nina report on [TICKER]",
  or any request to produce a ShareScope-backed financial analysis.
---

# Skill: /stock-research

Full ShareScope + NotebookLM financial research pipeline.
Produces a Nina financial analysis report saved as .md to the vault.

Uses:
- ShareScope watcher (nlm_action_queue.json + run_queue.json)
- notebooklm-py CLI (run by watcher)
- Vault path: 06-Resources/ShareScope-Reports/

---

## PRE-FLIGHT CHECKS

Before starting, verify:
1. The watcher is running: read watcher_heartbeat.json
   Path: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\watcher_heartbeat.json
   - status should be "running"
   - nlm_auth_status should be "ok" (not "expired")
   - If not running: tell Mick "The ShareScope watcher is not running - please run start_watcher.bat first"
   - If auth expired: tell Mick "NotebookLM auth has expired - please run: notebooklm login"

2. Confirm the ticker if not already provided. Ask: "Which ticker would you like to research?"

---

## PHASE 1 - NOTEBOOK CHECK

Write nlm_action_queue.json to the project folder:
  Path: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\nlm_action_queue.json
  Content: {"action": "check", "ticker": "[TICKER]"}

Tell Mick: "Checking NotebookLM for an existing [TICKER] notebook..."

Poll nlm_action_result.json every 3 seconds, up to 30 seconds:
  Path: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\nlm_action_result.json

If timeout with no result: tell Mick "Notebook check timed out - is the watcher running?"

On result:

### If found = true:
- Extract notebook_id and company_name from the result
- Tell Mick: "Found existing notebook: [notebook_name]. Using that for this run."
- Proceed to Phase 3

### If found = false:
- Proceed to Phase 2 (create notebook)

---

## PHASE 2 - CREATE NOTEBOOK (only if not found)

Ask Mick TWO questions (can be in one message):
1. "What is the full company name for [TICKER]?" (e.g. "Serica Energy")
2. "Should this be a permanent or temporary notebook?
   - Permanent: saved with the ticker name, reused for future research on this stock
   - Temporary: prefixed TEMP -, useful for demos or one-off analysis"

Wait for Mick's response, then write nlm_action_queue.json:
  Content: {
    "action": "create",
    "ticker": "[TICKER]",
    "company_name": "[Company Name from Mick]",
    "notebook_type": "permanent" or "temporary"
  }

Tell Mick: "Creating [permanent/temporary] notebook for [TICKER] - [Company Name]..."

Poll nlm_action_result.json every 3 seconds, up to 60 seconds.

On result:
- If success = true: extract notebook_id and company_name. Tell Mick "Notebook created."
- If success = false: report the error and stop.

---

## PHASE 3 - TRIGGER SHARESCOPE RUN

Delete any stale run_complete.json first (to avoid reading old results):
  Path: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\run_complete.json

Write run_queue.json:
  Path: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\run_queue.json
  Content: {
    "ticker":         "[TICKER]",
    "company_name":   "[Company Name]",
    "notebook_id":    "[notebook_id from Phase 1 or 2]",
    "notebook_type":  "permanent" or "temporary",
    "requested_at":   "[ISO timestamp - get via python3]"
  }

Tell Mick:
  "ShareScope pipeline started for [TICKER] ([Company Name]).
   Step 1 of 3: Exporting financial data from ShareScope...
   This usually takes 20-40 seconds."

---

## PHASE 4 - MONITOR PROGRESS

Poll run_complete.json every 5 seconds, up to 8 minutes (480 seconds total):
  Path: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\run_complete.json

While waiting, give progress updates at intervals:
- After 30s: "Step 1 still running - ShareScope can take up to a minute..."
- After 90s: "Step 2 of 3: Uploading data to NotebookLM and running Nina analysis..."
- After 180s: "Still working - NLM analysis can take 2-3 minutes..."

On run_complete.json appearing:

### If success = true:
- Check result.nlm_research.success
- If nlm_research succeeded:
  - Report path is in result.nlm_research.report_path
  - Tell Mick:
    "All done! Nina's financial analysis report for [TICKER] is ready.

    Report saved to vault:
    [report_path]

    The report includes:
    - Full Year Forecast Table
    - P&L, Balance Sheet, and Cash Flow analysis
    - Technical analysis
    - BUY / HOLD / SELL recommendation

    To view: open the ShareScope-Reports folder in Obsidian."
- If nlm_research failed:
  - Tell Mick:
    "ShareScope data exported successfully, but the NLM analysis step failed:
    [error message]
    The CSVs are saved at downloads/[TICKER]/. You can retry the NLM step manually."

### If success = false:
- Tell Mick the error from result.error
- Suggest checking the ShareScope watcher logs

### Timeout (no run_complete.json after 8 minutes):
- Tell Mick: "The pipeline seems to be taking longer than expected.
  Check the watcher logs at:
  C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\logs\"

---

## POLLING HELPER (Python)

Use this pattern to poll for a result file:

```python
import json, time
from pathlib import Path

result_file = Path(r"C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\nlm_action_result.json")
timeout = 30
start = time.time()

while time.time() - start < timeout:
    if result_file.exists():
        data = json.loads(result_file.read_text(encoding="utf-8"))
        print(json.dumps(data, indent=2))
        break
    time.sleep(3)
else:
    print("TIMEOUT")
```

Adapt the path and timeout as needed for each phase.

---

## TIMESTAMP HELPER

Always get the current ISO timestamp via python3 before writing run_queue.json:

```python
from datetime import datetime, timezone, timedelta
utc_now = datetime.now(timezone.utc)
bst_active = 4 <= utc_now.month <= 10
offset = timedelta(hours=1) if bst_active else timedelta(hours=0)
london_now = utc_now.astimezone(timezone(offset))
print(london_now.isoformat())
```

---

## NOTES

- Only one run can be in flight at a time (watcher processes one queue at a time)
- CSVs are saved to: downloads/[TICKER]/ inside the project folder
- Reports are saved to: 06-Resources/ShareScope-Reports/ in the Dex vault
- Report YAML frontmatter matches the Notion Research Database schema for sync
- Notebook naming: [TICKER] - [Company]_Updated:YYYY.MM.DD (permanent)
                   TEMP - [TICKER] - [Company]_Updated:YYYY.MM.DD (temporary)
- Sign-off on reports: "DYOR: Nina, Mick's AI Research Assistant"
- Auth status can be checked anytime via watcher_heartbeat.json

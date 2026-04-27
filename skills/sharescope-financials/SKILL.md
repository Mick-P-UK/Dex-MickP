# ShareScope Financials Skill

## Trigger Phrases
Use this skill when Mick says any of the following:
- "download [TICKER] financials"
- "get the financials for [TICKER]"
- "run ShareScope for [TICKER]"
- "export [TICKER] financials from ShareScope"
- "Cedric, download [TICKER] from ShareScope"
- "/sharescope-financials [TICKER]"

---

## Purpose
One-command financial data export for any stock in ShareScope.
Mick names a ticker; Cedric gives the exact PowerShell command to run,
then verifies the 6 CSV files landed correctly and reports back.

Output: 6 CSV files in the project downloads\{TICKER}\ folder:
  income_statement, balance_sheet, cash_flow, ratios, dividends, forecasts

---

## IMPORTANT: Architecture Note

The ShareScope automation uses a headed Windows Playwright browser
(SHARESCOPE_HEADLESS=false). This must be run from PowerShell on
Mick's Windows machine -- Cedric cannot execute it directly from
the Linux sandbox. Cedric's role is to give the exact command and
verify the results afterward.

This will be upgraded to full automation (Cedric runs it end-to-end)
once the Playwright CLI integration is confirmed working headlessly.

---

## Step 1 -- Extract and Confirm the Ticker

Read Mick's message and extract the ticker symbol.
Normalise to uppercase (e.g. "sqz" -> "SQZ", "bp." -> "BP.").

If the ticker is ambiguous or missing, ask:
  "Which ticker would you like me to pull? (e.g. SQZ, BP., AAPL)"

Once you have it, confirm briefly:
  "On it -- downloading SQZ financials. Run this in PowerShell:"

---

## Step 2 -- Give the PowerShell Command

Provide this exact block, substituting {TICKER} with the confirmed symbol:

```
cd "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation"
python sharescope_orchestrator.py {TICKER}
```

Tell Mick:
- ShareScope will open in a browser window (this is normal)
- The script will search for the stock, export all 6 financial tabs, then close
- It takes roughly 30-60 seconds per run
- Let me know when it finishes (or paste any error if it fails)

---

## Step 3 -- Wait for Mick to Confirm

Do NOT move on until Mick says it finished (or reports an error).

If Mick reports an error, see the Troubleshooting section below.

---

## Step 4 -- Verify the Output Files

Once Mick confirms the run completed, check the output folder.
The vault folder must already be connected (if not, request it first):
  C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP

Use Glob to check for CSV files:
  Pattern: downloads/{TICKER}/*.csv
  Path:    C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation

Expect exactly 6 files with today's date and the correct ticker in the name:
  YYYY.MM.DD-HH_MM_{TICKER}_income_statement.csv
  YYYY.MM.DD-HH_MM_{TICKER}_balance_sheet.csv
  YYYY.MM.DD-HH_MM_{TICKER}_cash_flow.csv
  YYYY.MM.DD-HH_MM_{TICKER}_ratios.csv
  YYYY.MM.DD-HH_MM_{TICKER}_dividends.csv
  YYYY.MM.DD-HH_MM_{TICKER}_forecasts.csv

---

## Step 5 -- Report Back to Mick

If all 6 files are present:
  "All done! 6 files downloaded for {TICKER}:
   [list filenames]
   Saved to: downloads\{TICKER}\"

If fewer than 6 files or no files:
  "Something looks off -- I can only see [N] file(s). Check the PowerShell
   output for errors and paste it here if you need me to debug."

---

## Troubleshooting

### "Stock not found in ShareScope"
The ticker may use a different format in ShareScope.
Try variations: "SQZ" vs "Serica Energy" (name search also works).

### "ImportError: cannot import name X"
A module import is broken. Check that all 7 Python files are in the
same project folder:
  sharescope_utils.py, sharescope_login.py, sharescope_search.py,
  sharescope_export.py, sharescope_screenshot.py, sharescope_logout.py,
  sharescope_orchestrator.py

### "Locator error" or Playwright timeout
ShareScope may have changed its UI. Check the selector reference files:
  ShareScope-Login-Accessibility-Reference.md
  ShareScope-Export-Accessibility-Reference.md
Report to Cedric and the selectors will be updated.

### Browser closes immediately / credentials error
Verify the .env file exists and contains the right values:
  C:\Vaults\Mick's Vault\.env
  SHARESCOPE_USERNAME=mick@diy-investors.com
  SHARESCOPE_PASSWORD="SPad#m1045"
  SHARESCOPE_HEADLESS=false

---

## Pending Work (Do Not Forget)

### Step 6 -- Add Novice-Friendly Comments to Original Scripts
The following 4 scripts need plain-English inline comments added so
anyone (including Mick) can read and understand what each block does.
The 3 new Phase 1B scripts (utils, search, export) already have
detailed comments -- only the originals need this work.

Files to update:
  sharescope_login.py
  sharescope_screenshot.py
  sharescope_logout.py
  sharescope_orchestrator.py

When to do this: next quiet session after Step 7 is confirmed working.
Assign roughly 20-30 mins. No code logic changes -- comments only.

---

## Skill Metadata

Version:  1.0
Created:  2026.04.26
Author:   Cedric (PAIDA)
Vault:    C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\sharescope-financials\SKILL.md
Mirror:   /mnt/skills/user/sharescope-financials/SKILL.md

# ShareScope Get Chart Skill

## Trigger Phrases
Use this skill when Mick says any of the following:
- "get the chart for [TICKER]"
- "sharescope chart [TICKER]"
- "grab the [TICKER] chart"
- "chart for [TICKER] from ShareScope"
- "add a chart for [TICKER]" (when building a report)
- "/sharescope-get-chart [TICKER]"

Also call this skill automatically as a COMPONENT when any report-building
skill or prompt needs a price chart for a stock (see "Use as a Report Component").

---

## Purpose
One-command 12-month price chart export for any stock in ShareScope, saved as a
clean PNG using ShareScope's own native "Save chart as PNG (Scaled)..." export
(not a screen grab). The PNG drops straight into a branded report.

Output: 1 PNG file in the project downloads\{TICKER}\ folder:
  YYYY.MM.DD-HH_MM_{TICKER}_chart_12m.png

---

## IMPORTANT: Architecture Note
The ShareScope automation is a headless-capable Windows Playwright script.
It reads credentials from the .env and must run on Mick's Windows machine.
Cedric (Linux sandbox) CANNOT execute it directly - Cedric's role is to give
the exact command, then verify the PNG landed and (for reports) embed it.

Credentials come from the .env ONLY - never write them into this file:
  C:\Vaults\Mick's Vault\.env
  (SHARESCOPE_HEADLESS=true for hands-off runs; set false the first time to
   watch the run and confirm the two unconfirmed selectors - see Troubleshooting.)

Future upgrade: trigger via the project watcher (sharescope_watcher.py) so
Cedric can run it end-to-end unattended. Not wired up yet.

---

## Step 1 -- Extract and Confirm the Ticker
Read Mick's message and extract the ticker. Normalise to uppercase
(e.g. "sqz" -> "SQZ", "bp." -> "BP.").
If missing or ambiguous, ask:
  "Which ticker would you like the chart for? (e.g. SQZ, BP., ULVR)"
Then confirm briefly:
  "On it - grabbing the 12-month chart for SQZ. Run this in PowerShell:"

---

## Step 2 -- Give the PowerShell Command
Provide this exact block, substituting {TICKER}:

```
cd "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation"
python sharescope_chart_orchestrator.py {TICKER}
```

Tell Mick:
- ShareScope opens, selects the stock, switches to Chart, saves the PNG, closes
- Takes roughly 20-40 seconds
- Let me know when it finishes (or paste any error)

---

## Step 3 -- Wait for Mick to Confirm
Do NOT move on until Mick says it finished (or reports an error).

---

## Step 4 -- Verify the Output File
Ensure the vault folder is connected, then check for the PNG:
  Folder: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\downloads\{TICKER}\
  Expect: one file matching YYYY.MM.DD-HH_MM_{TICKER}_chart_12m.png with today's date.
Sanity-check the file size is not tiny (a few KB suggests a blank/error image).

---

## Step 5 -- Report Back (or Embed)
If the PNG is present:
  "Chart ready for {TICKER}: [filename]. Saved to downloads\{TICKER}\."
If used inside a report: embed the PNG into the report at the agreed position
(see below) rather than just reporting the path.

---

## Use as a Report Component
When a report skill/prompt needs a chart:
1. Call this skill with the report's ticker.
2. Once the PNG exists, insert it into the report document (docx) using the
   python-docx add_picture flow, sized to fit the content width.
3. Caption it with the ticker and the capture date.
Keep the chart-fetch and the report generation as separate steps: fetch first,
confirm the PNG, then build/complete the report with the image embedded.

---

## Troubleshooting

### Chart period not 12 months
The 12-month period control selector is not yet confirmed. The script tries a
list of likely labels (see PERIOD_12M_CANDIDATES in sharescope_chart.py) and is
non-fatal - it will still export whatever period is shown. On the first HEADED
run, watch which control sets 1 year, then add its exact label to that list.

### "Save chart as PNG (Scaled)..." not found
The menu text is taken from the December Scribe workflow. If ShareScope has
reworded it, update SAVE_PNG_LABEL at the top of sharescope_chart.py.

### Stock not found
Try the full exchange-prefixed ticker (e.g. "LSE:SQZ") or search by name.

### Browser closes immediately / credentials error
Check the .env exists and is correct at C:\Vaults\Mick's Vault\.env
(SHARESCOPE_USERNAME, SHARESCOPE_PASSWORD, SHARESCOPE_HEADLESS). Do NOT paste
the values here.

### Locator / timeout error
ShareScope may have changed its UI. Update the selectors and log the change in
ShareScope-Export-Accessibility-Reference.md.

---

## Files
- sharescope_chart.py               (chart capture module - NEW)
- sharescope_chart_orchestrator.py  (entry point - NEW)
- sharescope_login.py / _search.py / _logout.py / _utils.py  (reused, unchanged)
All in: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\

---

## Skill Metadata

Version:  1.0 (confirmed live 2026.07.01 - end to end run on SQZ)
Created:  2026.07.01
Author:   Cedric (PAIDA)

Confirmed selectors (2026.07.01):
- Chart view button: button[data-cmd="ViewChart"] (NOT get_by_role name=Chart - two match)
- 12-month period control: labelled "1 year"
- Save-as-PNG menu item: "Save chart as PNG (bitmap)..." (a scaling dialog appears - click OK)

Known minor issue (non-blocking): the shared sharescope_logout.py logs two
harmless warnings on exit (logout button not found + playwright.stop on None).
The browser still closes and the PNG still saves. Pre-existing across the project.
Fix after the webinar - do NOT touch the shared logout module mid-deadline.

Vault:    C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\sharescope-get-chart\SKILL.md
Mirror:   /mnt/skills/user/sharescope-get-chart/SKILL.md  (PENDING dual-write)
Build:    C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.07.01-ShareScope-Chart-Export\

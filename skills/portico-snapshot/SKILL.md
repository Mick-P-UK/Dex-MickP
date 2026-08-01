---
name: portico-snapshot
description: Captures the Portico PP1 and PP2 portfolios from ShareScope and produces Mick's house-style branded snapshot images plus a week-on-week figures update. Standalone - runnable any time, not only at weekends. Use this skill whenever Mick says "capture the Portico snapshots", "snapshot PP1 and PP2", "grab the Portico weekend snapshot", "run the Portico snapshot", "do the PP1 and PP2 snapshots", "portico snapshot", or any request to capture and format the two Portico portfolios. Produces finished images only - it does NOT post to Slack (that is the separate PPfolios-to-Slack skill). For the full weekend post routine, follow the Portico-WE-portfolios SOP which chains this skill then PPfolios-to-Slack.
version: 1.0
created: 2026-08-01
owner: Mick (built with Cedric)
---

# portico-snapshot

Capture PP1 and PP2 from ShareScope and turn each into Mick's weekend house-style
image, with the week-on-week figures folded into the history store. The output is a
pair of finished, branded PNGs ready for Mick to review (and, at weekends, to hand to
the PPfolios-to-Slack skill).

This skill is deliberately SEPARATE from posting, so Mick can grab a snapshot any day
of the week without publishing anything.

## What "done" looks like

Two finished, stamped, house-style images in:
`04-Projects\2026.04.04-ShareScope-Automation\portico\outputs\`
named `YYYY.MM.DD - PP1 - Portico Weekend Snapshot.png` and `... - PP2 - ...`,
plus `portico\portico_history.json` updated with this capture's figures and the
week-on-week deltas. The skill STOPS here. It never posts to Slack.

## Key facts (do not get these wrong)

- Base capital (the rolling %-return basis), from portico_history.json:
  - PP1 base = 29,331.39 (carrying value; residual after 20,668.61 was transferred out to seed PP2)
  - PP2 base = 50,000.00 (nominal)
  - PP1 + PP2 carrying = 50,000.00 original Portico capital (started 27 Jan 2020).
- Gain = Total - base. Percentage return is TRUNCATED to 2dp, NEVER rounded
  (annotate_portico.py and the store both do this; keep it consistent).
- Currency is GBP.
- The label date is the ACTUAL capture day (the Saturday for a weekend run), not
  necessarily today - confirm the date with Mick if capturing for a specific weekend.

## Prerequisites

- Runs against LIVE ShareScope via headed Playwright on Mick's Windows PC (mick-pc25).
  The capture step CANNOT run from a fresh cloud session - it needs the real browser.
- ShareScope credentials live in `C:\Users\pavey\.env`
  (SHARESCOPE_USERNAME / SHARESCOPE_PASSWORD). Never hardcode them.
- The formatter (annotate_portico.py) needs Python with Pillow and pytesseract
  (Tesseract OCR) available. It uses OCR to find the Cash/Total rows and the table
  bottom. Run the format step where that toolchain exists (the Cowork/Desktop Linux
  sandbox has it; a bare Windows Python may not have Tesseract installed).

## The pipeline

### Step 1 - CAPTURE (Mick runs this on his PC)

Mick runs the capture script in PowerShell from the project folder:

```
cd "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation"
python sharescope_portico.py
```

One login -> for each of PP1, PP2: select portfolio -> ensure the live "Current
holdings" view -> capture the right-hand panel PNG -> export Holdings CSV (full
history, then filtered to a current-only copy) -> Cash tab -> export Transactions CSV
-> one logout.

Outputs land in `portico\downloads\`:
- `YYYY.MM.DD - PPx - Snapshot(raw).png`
- `YYYY.MM.DD - PPx - Holdings.csv` (current holdings only)
- `YYYY.MM.DD - PPx - Holdings (full history).csv`
- `YYYY.MM.DD - PPx - Transactions.csv`

Expect the run summary to read `holdings=OK transactions=OK snapshot=OK` for both,
plus a `filtered to N current holdings` line (roughly 18 for PP1, 22 for PP2).

CAVEAT (known, from the 2026-07-25 hardening): on a SLOW page load the capture can
occasionally grab the full holdings list instead of the current-holdings view. The
script fails loud - it flags `current-holdings view NOT confirmed` in the summary and
saves a debug shot. If you see that flag, re-run the capture, or verify the raw PNG by
eye before formatting. PP2 has been reliable; PP1's longer list is the one at risk.

### Step 2 - RECONCILE FIGURES (Cedric)

For each portfolio, read the Total from `YYYY.MM.DD - PPx - Holdings.csv` (the Total
row) and the holdings/cash split. Cross-check against the raw snapshot by eye. These
figures drive both the image annotation and the history store, so they must be right.

### Step 3 - FORMAT (Cedric runs annotate_portico.py, once per portfolio)

```
python3 portico/annotate_portico.py "portico/downloads/YYYY.MM.DD - PP1 - Snapshot(raw).png" \
  --top-label "PP1: Saturday 25th July 2026" \
  --bottom-label "PP1 (week-end position): Saturday 25th July 2026" \
  --total 72752.54 --base 29331.39 --currency GBP \
  --stamp "09:30 25/07/2026" \
  --out "portico/outputs/YYYY.MM.DD - PP1 - Portico Weekend Snapshot.png"
```

- `--total` = the reconciled Total for that portfolio.
- `--base` = 29331.39 for PP1, 50000 for PP2.
- `--stamp` = "HH:MM DD/MM/YYYY" - REQUIRED, because a Playwright page screenshot has
  no Windows taskbar clock for the formatter to crop.
- The formatter draws the house style: grey frame; blue underline under Cash, red
  under Total; a red-bordered top-right box (line 1 red = portfolio + date, line 2
  blue = the gain line); a red-bordered blue bottom label, inset so it never covers
  the stamp. It computes gain and the truncated 2dp percentage itself from --total
  and --base, so those two numbers are the only figures you pass.

Repeat for PP2 with its own labels, total and base.

### Step 4 - UPDATE THE WEEK-ON-WEEK STORE (Cedric)

Append this capture to `portico\portico_history.json` -> `history` (most recent last),
with, per portfolio: holdings_value, cash, total, base_capital, gain, pct_return, and
a `week_on_week` block versus the previous entry (value_change, pct_on_week,
return_points_change). Percentages truncated to 2dp. All money GBP. ASCII only.

## Output naming

Finished working images: `YYYY.MM.DD - PPn - Portico Weekend Snapshot.png` in
`portico\outputs\`.

Note: the JPG that actually gets POSTED to Slack uses a different, figure-encoded name
(`YYYY.MM.DD - PPn_{total}GBP_Up by {gain}GBP_Up by {pc}pc.jpg`). That JPG conversion
and naming is done by the PPfolios-to-Slack skill at post time, not here - this skill
keeps its output Slack-agnostic.

## Where this skill hands off

portico-snapshot ends with the two finished PNGs and the updated store. It does NOT:
- post anything to Slack (-> PPfolios-to-Slack skill),
- touch #micks-diary or the video commentary (Mick does that separately).

The weekend routine that chains capture -> post is the `Portico-WE-portfolios` SOP.

## Gotchas / notes

- Standing rule: all ShareScope UI automation targets stable `data-cmd` attributes
  (+ `:visible`), never button text/role/position. Map:
  `ShareScope-data-cmd-Reference.md`.
- `ExportHoldings` dumps FULL history regardless of the Current-holdings view toggle,
  which is why the script keeps a full-history file and derives a current-only copy.
- Logout logs a harmless `'NoneType' has no attribute 'stop'` warning - ignore it.
- OPEN (not yet built): a fully unattended weekend schedule. The capture must run on
  Mick's Windows machine (headed browser); the likely design is a Windows Task
  Scheduler job for capture, then Cedric formats + updates the store from the vault.
  Confirm the scheduling approach with Mick before automating end to end.

## Key files

- `04-Projects\2026.04.04-ShareScope-Automation\sharescope_portico.py` - capture (RUN THIS)
- `...\portico\annotate_portico.py` - house-style formatter (Cedric runs)
- `...\portico\portico_history.json` - week-on-week store
- `...\ShareScope-data-cmd-Reference.md` - data-cmd map + standing rule
- `...\portico\downloads\` - CSVs, raw snapshots, `_debug\`
- `...\portico\outputs\` - finished images

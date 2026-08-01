---
name: eom-portfolio-capture
description: Captures the end-of-month ShareScope images for Mick's four Active 10 portfolios plus the two index charts, and files them into the live folders that feed the End-of-Month Portfolio Posting routine. For each portfolio it grabs the current-holdings screenshot and a month-scoped transactions image (auto-cropped from the full Cash statement); for the ASX (FTSE All-Share) and SP500 (S&P 500) indices it captures a verified 12-month chart at two 16:9 sizes (1200px and 1920px), as JPEG. Use this skill whenever Mick says "do the end-of-month capture", "grab the month-end portfolio images", "capture the Active 10 portfolios and indices", "run the EOM capture", "take the month-end ShareScope images", or at the start of the end-of-month routine (the first day after month-end). This is the UPSTREAM capture that feeds the portfolio-post-creator posting pipeline.
version: 1.0
created: 2026-08-01
owner: Mick (built with Cedric)
---

# eom-portfolio-capture

Mick's month-end ShareScope image grab. In ONE ShareScope login it produces, for the
month that just ended:

- 4 x portfolio current-holdings screenshots (UK Active 10, UK Active 10 Yr2,
  US Active 10, US Active 10 Yr2) - unlabelled, ready for Mick's formatter.
- up to 4 x month-scoped transactions images (one per portfolio; a portfolio with no
  trades that month yields no transactions image - that is correct, not an error).
- 2 x index charts (ASX = FTSE All-Share; SP500 = S&P 500), each at 1200x675 and
  1920x1080 (both 16:9), 12-month period VERIFIED, native ShareScope PNG export saved
  as JPEG.

This is the front end that produces the screenshots the `End-of-Month Portfolio Posting`
SOP (and its `portfolio-post-creator` skill) assume already exist. It does NOT post
anything.

## What "done" looks like

Up to 12 JPEGs (11 in a typical month) filed into the six live folders:

| Image | Live folder |
|-------|-------------|
| `YYYY.MM.DD - <Portfolio> Portfolio.jpg` | the portfolio's `2026_...` folder |
| `YYYY.MM.DD - <Portfolio> Transactions <Month> YYYY.jpg` | same folder |
| `YYYY.MM.DD - ASX 12 month chart_1200px.jpg` / `_1920px.jpg` | `...01 - Indices\ASX` |
| `YYYY.MM.DD - SP500 12 month chart_1200px.jpg` / `_1920px.jpg` | `...01 - Indices\SP500` |

`YYYY.MM.DD` is the MONTH-END date (last day of the month), not the capture day.

## Prerequisites

- Run in **Claude Code on Mick's PC** (local). It logs into live ShareScope via headed
  Playwright - it cannot run from a cloud session.
- ShareScope credentials in `C:\Users\pavey\.env` (SHARESCOPE_USERNAME / SHARESCOPE_PASSWORD).
  Never hardcode them.
- Python with Playwright, Pillow, and **pytesseract** (Tesseract at
  `C:\Program Files\Tesseract-OCR\tesseract.exe`) - the transactions crop uses OCR.

## Scripts (in `04-Projects\2026.04.04-ShareScope-Automation\`)

- `eom_capture_full.py` - the orchestrator (login once, all captures, month-crop, stage).
- `crop_transactions.py` - turns a full Cash statement into the month-scoped image.
- Reused building blocks: `sharescope_login.py`, `sharescope_logout.py`,
  `sharescope_search.py`, `sharescope_chart.py` (period + PNG export), and helpers in
  `eom_capture_example.py` (portfolio dropdown selection, panel/chart capture, jpg).

## How to run

Step 0 - VERIFY the target month-end date with code (never from memory). The script
computes it automatically (last month if run on the 1st, else the current month-end),
but confirm it, and pass it explicitly if capturing for a specific month:

```
cd "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation"
python eom_capture_full.py            # auto month-end
python eom_capture_full.py 2026.07.31 # or an explicit month-end (YYYY.MM.DD)
```

This STAGES the images into `eom\full\` and writes `eom\full\manifest.json`. Nothing
touches the live folders yet. Cedric shows the images to Mick for review.

On Mick's OK, commit them into the live folders:

```
python eom_capture_full.py --commit
```

(`--commit` copies each staged file to its destination using manifest.json.)

## Key facts / gotchas (all confirmed live 2026-08-01)

- **Portfolios are NOT pinned quick-buttons.** The four Active 10 portfolios live in the
  top-toolbar **"Portfolios"** dropdown. Menu labels: `0 - 0 - 2026 - Active 10 - UK`,
  `... - UK (Yr2)`, `... - US`, `... - US (Yr2)`. Select the portfolio FIRST (that
  enables the Transactions view), then confirm via the panel header.
- **Index charts via Search, not the top buttons.** "FTSE All"/"US 500" top buttons open
  constituent LISTS, not charts. Use Search: `ASX` -> FTSE All-Share, `GSPC` -> S&P 500.
- **12-month period is VERIFIED**, not assumed - ShareScope remembers the last period, so
  the script sets "1 year" and checks the tab is active before exporting. Charts keep
  Mick's on-chart watermark (instrument code + daily change) - he wants it.
- **Chart sizes**: 1200x675 and 1920x1080 (both 16:9), suffixed `_1200px` / `_1920px`.
  Native "Save chart as PNG (bitmap)" export (not a screen grab), converted to JPEG.
- **Transactions = an edited screenshot.** There is NO native date filter on the Cash
  view (checked inline, Design, Advanced). The full statement is captured (scrolling the
  `.trans-view-scroll-div` to the bottom so the current month's rows - which sit at the
  end - are in view), then `crop_transactions.py` uses OCR to keep the green header, the
  "Cash account statement" title, the column headers and only that month's rows, drops
  the "Portfolio current value" summary block, and adds a blue-bordered red caption
  `"<Portfolio> - Transactions (<Month> YYYY)"`. OCR runs on a 3x-upscaled copy for
  reliable date reading, mapped back to native resolution.
- **No trades that month** -> no transactions image for that portfolio (valid).
- **Extension is `.jpg`** (matches the entire existing archive).
- **Dating**: files carry the MONTH-END date prefix (e.g. `2026.07.31`), even when
  captured on the 1st.

## Where this hands off

The images land in the same folders the `End-of-Month Portfolio Posting` SOP reads from,
so the next step is that routine (`portfolio-post-creator` -> `wordpress-*`), which builds
the four WordPress draft posts on diy-investors.com. This skill stops at filing the images.

## Related

- SOP: `06-Resources\SOPs\SOP - End-of-Month ShareScope Capture.md` (this routine).
- Downstream SOP: `06-Resources\SOPs\SOP - End-of-Month Portfolio Posting.md` + skill
  `portfolio-post-creator`.
- UI map: `04-Projects\2026.04.04-ShareScope-Automation\ShareScope-data-cmd-Reference.md`.

## Not yet built / open

- No-transactions months: DECIDED (Mick, 2026-08-01) - NO image. Instead the posting
  routine (`portfolio-post-creator`) puts a short line of text in the post, e.g. "There
  were no transactions during <Month>." This capture skill correctly produces no
  transactions image for such a portfolio; nothing to build here.
- Right-edge scrollbar on a scrolled (Yr2) transactions crop: cosmetic, left as-is by
  Mick's decision (2026-08-01).
- Unattended monthly schedule: run with `--headless` so it never steals the screen
  (added 2026-08-01). Still needs Mick's PC on and the images stored locally. A Windows
  Task Scheduler job in the early hours of the 1st is the intended design - not yet set up.
- The `_1920px` charts share the same watermark/size logic as `_1200px`; if Mick wants a
  different treatment per size, add it.

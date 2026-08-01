---
title: End-of-Month ShareScope Capture
tags:
  - SOP
type: SOP
status: active
version: 1.0
created: 2026-08-01
owner: Mick (built with Cedric)
related-skills: eom-portfolio-capture
feeds: End-of-Month Portfolio Posting
---

# SOP - End-of-Month ShareScope Capture

## 1. Purpose

The FIRST thing that happens at month-end: capture the six-plus ShareScope images that
every downstream end-of-month task needs. This is the upstream capture that the
`End-of-Month Portfolio Posting` SOP assumes has already been done.

For the month that just ended it produces:

- 4 portfolio current-holdings screenshots (UK Active 10, UK Active 10 Yr2, US Active 10,
  US Active 10 Yr2), unlabelled.
- up to 4 month-scoped transactions images (one per portfolio; skipped for any portfolio
  with no trades that month).
- 2 index charts (ASX = FTSE All-Share, SP500 = S&P 500), each at 1200x675 and 1920x1080
  (both 16:9), 12-month period verified. JPEG.

## 2. When to run it

Late on the last day of the month (after the UK and US markets have closed) OR early on
the first day of the new month. The images are dated with the MONTH-END date regardless.

## 3. Environment and prerequisites

- Run in **Claude Code on Mick's PC** (local). It drives live ShareScope through a headed
  browser and cannot run from a cloud session.
- ShareScope credentials in `C:\Users\pavey\.env`.
- Python with Playwright, Pillow, pytesseract (Tesseract installed at
  `C:\Program Files\Tesseract-OCR\tesseract.exe`).

## 4. The routine (skill: eom-portfolio-capture)

Cedric follows the `eom-portfolio-capture` skill. In one login it:

1. Logs into ShareScope, widens to 1920x1080.
2. For each of the four Active 10 portfolios: selects it from the top-toolbar
   **"Portfolios"** dropdown (they are NOT pinned quick-buttons), captures the
   current-holdings panel, then opens the Cash view, scrolls the statement to the bottom,
   captures the full statement, and month-crops it (drops the summary block and all other
   months, keeps the header + column headers + this month's rows, adds a blue-bordered
   caption). No trades that month -> no transactions image.
3. For ASX (`ASX`) and SP500 (`GSPC`), selected via Search: switches to the chart, sets
   and VERIFIES the 12-month period, and exports 1200x675 and 1920x1080 PNGs (native
   "Save chart as PNG (bitmap)"), converted to JPEG. The on-chart watermark is kept.
4. Stages everything to `eom\full\` with a manifest; Cedric shows Mick.
5. On Mick's OK, commits the files into the six live folders.

Run:

```
cd "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation"
python eom_capture_full.py            # (or: python eom_capture_full.py YYYY.MM.DD)
# review, then:
python eom_capture_full.py --commit
```

## 5. Destinations

Portfolio images -> `C:\Users\pavey\Documents\0.2 - Areas (n)\02 - DIY - Investors\DIY - Portfolios\`:

| Portfolio | Folder |
|-----------|--------|
| UK Active 10 | `2026_UK_Active 10` |
| UK Active 10 Yr2 | `2026_UK Active 10_Yr2` |
| US Active 10 | `2026_US_Active 10` |
| US Active 10 Yr2 | `2026_US Active 10_Yr2` |

Index charts -> `...\001 - DIY - Images\01 - Indices\ASX` and `...\SP500`.

## 6. Conventions

- Filenames: `YYYY.MM.DD - <Portfolio> Portfolio.jpg`,
  `YYYY.MM.DD - <Portfolio> Transactions <Month> YYYY.jpg`,
  `YYYY.MM.DD - ASX 12 month chart_1200px.jpg` (and `_1920px`, and SP500). Extension
  `.jpg` to match the archive. `YYYY.MM.DD` = month-end date.
- Charts keep ShareScope's on-chart watermark (instrument + daily change).
- Transactions caption: red text in a blue-bordered box,
  `"<Portfolio> - Transactions (<Month> YYYY)"`.

## 7. Key facts / gotchas

- Portfolio dropdown labels: `0 - 0 - 2026 - Active 10 - UK / UK (Yr2) / US / US (Yr2)`.
- Index tickers: ASX = FTSE All-Share, GSPC = S&P 500. Do NOT use the "FTSE All"/"US 500"
  top buttons for charts - they open constituent lists.
- No native date filter on the Cash view; the month scope is an OCR crop of the full
  statement. Yr2 statements are long - the current month sits below the fold, so the
  statement scroll div `.trans-view-scroll-div` is scrolled to the bottom before capture.
- Full UI map: `04-Projects\2026.04.04-ShareScope-Automation\ShareScope-data-cmd-Reference.md`.

## 8. Where this hands off

The images land in the folders the `End-of-Month Portfolio Posting` SOP reads from. That
routine (skill `portfolio-post-creator` -> `benchmark-fetcher` / `wordpress-image-uploader`
-> `wordpress-post-publisher`) builds the four WordPress DRAFT posts. This SOP stops at
filing the images.

## 9. Open items

- No-transactions months: DECIDED (Mick, 2026-08-01) - no image; the posting routine
  (`portfolio-post-creator`) adds a short line of text in the post instead ("There were
  no transactions during <Month>."). The capture correctly produces no image.
- Right-edge scrollbar on a scrolled (Yr2) transactions crop - cosmetic; left as-is
  (Mick, 2026-08-01).
- Unattended monthly schedule: run the capture with `--headless` (added 2026-08-01) so it
  never steals the screen; intended as a Windows Task Scheduler job in the early hours of
  the 1st. Needs Mick's PC on. Not yet set up - to be decided after the posting is verified.

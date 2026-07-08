---
name: portfolio-formatter
description: Turns a raw ShareScope "Current holdings" screenshot into a trimmed, branded portfolio image in Mick's house style - cropped to the holdings panel, grey border, a top-right annotation box with the calculated gain/loss and percentage, a red underline under the Total, and a bottom portfolio label box that never covers the date/time stamp. Use this skill whenever Mick asks to "format the portfolio image", "brand the ShareScope screenshot", "annotate the portfolio screenshot", "make the portfolio picture", "add the gain box to the portfolio image", "do the portfolio-formatter", "run the portfolio formatter", or any request to convert a portfolio holdings grab into the finished webinar/report image. Works for any Active 10 portfolio (UK, US, Yr2, etc.) and any screenshot size.
---

# Portfolio Formatter Skill

Converts a raw ShareScope "Current holdings" screenshot into the finished, branded
image Mick uses in webinars and reports. Reproduces the five steps he used to do by
hand.

## What it produces
From one screenshot (JPG or PNG, any size), a single PNG with:

1. **Trim** - cropped to the holdings panel, stopping at the grey "Total" summary bar
   (drops the empty area, the button row and the Windows taskbar).
2. **Grey border** - a 3px mid-grey frame around the whole image.
3. **Bottom label box** - blue-bordered box with the portfolio name + date in RED
   text, centred but inset from the right so it never covers the date/time stamp,
   which is preserved in the bottom-right corner.
4. **Top-right annotation box** - blue border, red title line (portfolio + date) and a
   blue line with the headline gain/loss and percentage.
5. **Red underline** - under the summary Total value.

## The headline calculation
- **Gain = Total - base**, where **base defaults to 10,000** in the portfolio's currency
  (the notional starting stake for an Active 10). Override with `--base` if a portfolio
  was topped up.
- **Percentage is TRUNCATED to 2dp, never rounded** - matches Mick's examples exactly:
  - UK Active 10: 12,367.62 - 10,000 = Up by £2,367.62 [+23.67%]  (not 23.68)
  - US Active 10: 9,827.18 - 10,000 = Down by $172.82 [-1.72%]    (not 1.73)
  - US Active 10 (Yr2): 18,541.80 - 10,000 = Up by $8,541.80 [+85.41%]

## Date convention - IMPORTANT (read before labelling)
The date/time stamp on the image is usually NOT the close date you want on the label.
Mick captures the snapshot the MORNING AFTER the close he wants to show: the US market
closes in the UK evening, so he grabs the figures the next morning, before the US
market re-opens. The figures therefore represent the CLOSE OF PLAY on the PREVIOUS day.

Rule of thumb: if the stamp shows an early UK morning time (before ~14:30 UK, i.e.
before the US open at 09:30 ET), the effective label date is the PREVIOUS calendar day.
  Example: stamp "01/07/2026 07:04" -> the close being shown is 30 June 2026, so label
  it "30th June 2026", NOT 1st July.

So: do NOT blindly use the OCR'd stamp date for the label. Check the stamp time, apply
the previous-day rule when it is an early-morning grab, and confirm the intended close
date with Mick if there is any doubt. Force the correct date with
`--label "US Active 10 (Yr2): 30th June 2026"`.

## Inputs
- One ShareScope holdings screenshot (JPG or PNG). Sizes vary - the script detects
  everything by feature, not fixed pixels, so do NOT assume a size.
- Values (currency, portfolio name, date, Total) are read by OCR (tesseract) and
  printed for eyeballing. Any can be overridden on the command line.
- The OCR'd date is the raw stamp date - apply the Date convention above before it
  goes on the label.

## How to run

1. Make sure the source image is on disk in a mounted folder (a pasted chat image is
   NOT a file - it must be saved first).
2. Install deps if needed:
   ```
   pip install --break-system-packages pillow numpy pytesseract
   ```
   (tesseract binary is already present in the sandbox at /usr/bin/tesseract.)
3. Run:
   ```
   python3 annotate_portfolio.py "SOURCE.jpg" --out "outputs/OUTPUT.png"
   ```
4. **Always check the printed `[OCR ]` and `[CALC]` lines** against the image before
   accepting the result. If OCR misread anything, re-run with overrides.

## Options
| Option        | Purpose                                                        |
|---------------|----------------------------------------------------------------|
| `--out PATH`  | output PNG path                                                |
| `--label ""`  | full label text, e.g. `"US Active 10 (Yr2): 6th July 2026"`     |
| `--total N`   | summary Total value, overrides OCR                             |
| `--currency`  | `GBP` or `USD`, overrides OCR-detected symbol                  |
| `--base N`    | notional starting stake (default 10000)                       |
| `--jpg`       | also write a quality-95 JPG alongside the PNG                  |

## Colours (closest match to Mick's examples)
- Red - annotation title line, Total underline, AND bottom label text: `(197, 0, 0)`
- Blue - annotation/label box borders and the annotation gain line: `(0, 0, 197)`
- Grey outer frame: `(128, 128, 128)`
- Font: DejaVu Sans Bold (Arial-equivalent)

## Output naming and location
- Follow Mick's convention:
  `YYYY.MM.DD - <Portfolio> - Portfolio Formatted - <event date>_vX.Y.png`
- Save the finished PNG to the project outputs folder
  (`C:\Vaults\Cowork\Projects\Portfolio-Formatter\outputs\`) and present it with
  `present_files`.
- **No provenance footer** - PNG is excluded from the footer rule (footers are for
  DOCX/PDF/XLSX only).

## How the detection works (for maintenance)
- **Table bottom**: first tall run (>=40 rows) of near-white full-width rows below 35%
  height - this is the empty area under the holdings Total bar.
- **Currency**: `$` vs `£` in the OCR text.
- **Portfolio name**: the `US`/`UK` + `(Yr?)` tokens in the green header row -> e.g.
  "US Active 10 (Yr2)".
- **Date**: first `dd/m/yy` token (the holding row date) -> "6th July 2026".
- **Total value + bbox**: OCR of the top-left value block; the lowest money row is the
  Total (Holdings / Cash / Total).
- **Clock**: a tight crop of the bottom-right corner (~9.3% W x 4.2% H) composited into
  the bottom-right of the finished image so the date/time is preserved.

## Standing rules
- Always output PNG (avoids JPEG artefacts on the sharp text and thin red lines).
- Never round the percentage - always truncate to 2dp.
- Never assume the screenshot size.
- ASCII only in any vault files this skill writes.

## Learning log
| Date       | Learning |
|------------|----------|
| 2026.07.06 | Skill created + live-tested on US Active 10 (Yr2) GGP example (957x866). Base = 10,000, truncated %, gave "Up by $8,541.80 [+85.41%]". Clock composite at 9.3% W x 4.2% H cleanly excluded the tray icons. Table-bottom white-gap detector cut exactly at the holdings Total bar (y=412). Confirmed with Mick: gain basis = Total minus 10k notional; inputs read by OCR. |
| 2026.07.06 | Mick feedback: bottom label TEXT should be red (box border stays blue). Changed label fill from BLUE to RED. |
| 2026.07.07 | First real run (US Active 10 Yr2, 30 June close). Real base images can be SHORT full-screen grabs (e.g. 987x479) where the taskbar follows the holdings Total bar with no white gap - the old white-gap crop fell back to 0.5*H and cut mid-table. Fixed detect_table_bottom to locate the holdings Total row by OCR (lowest 'Total' whose line carries >=3 column sums) and crop just below it; white-gap kept as fallback. Verified: full table retained on both short and tall grabs. Read source in place from C:\Users\pavey\Documents\...\DIY - Portfolios\<portfolio> folders (no source duplication). |
| 2026.07.06 | Mick clarified the DATE CONVENTION: he snapshots the morning after the close (before the US re-opens), so an early-morning stamp on the 1st represents the previous day's close. Added a "Date convention" section - apply the previous-day rule and confirm with Mick; never blindly use the OCR stamp date on the label. |
| 2026.07.06 | Generalisation fix after testing UK + US originals: the green header (white-on-green) OCRs to garbage at normal contrast, so portfolio name failed. Fix: threshold the header crop to black-on-white before OCR (detect_portfolio), with GBP->UK / USD->US fallback. Date detection made robust via upscaled both-polarity OCR of the bottom-right clock, falling back to the holdings date column (detect_date). Verified on all three: UK Active 10 (+23.67%), US Active 10 (-1.72%), US Active 10 (Yr2) (+85.41%) - all match Mick's manual examples. |

---
name: ii-to-xero
description: >
  Processes the Interactive Investor (ii) year-end transaction download for
  Ditty Box Ltd into an extended tracking spreadsheet (preserving full
  history from 2008) plus a detailed audit XLSX. Use this skill whenever
  Mick asks to "process the ii account", "do the ii import", "extend the
  ii spreadsheet", "run the ii to xero job", "build the ii tracking sheet",
  "do the Interactive Investor YE", "ii year-end conversion", or any
  request to fold the year's ii CSV download into the master tracking
  spreadsheet and prepare figures for Mick's manual journals. Always use
  this skill rather than parsing the CSV by hand. NOTE: unlike
  natwest-to-xero or cc1136-to-xero, this skill does NOT produce a Xero
  CSV directly - it produces a working spreadsheet that Mick uses to lift
  figures for manual journals (dividends, interest, withdrawals,
  purchases, stock valuation).
---

# Interactive Investor (ii) to Xero - Year End Workflow

This skill folds the year's ii transaction CSV into Mick's master
tracking spreadsheet (the 26-column, 1275-plus-row spreadsheet that
runs since 2008) and produces three outputs ready for Mick's manual
journal preparation.

## When to use

Once a year, during the Ditty Box Ltd annual accounts cycle, to process
the ii broker account. Interactive Investor is the company's stock
broking account (formerly Barclays Stockbrokers).

May also be used for interim spot-checks or when adding new transactions
mid-year (the skill is idempotent at the YE-block level - re-running
overwrites the latest YE block but preserves history).

## What this skill does NOT do

- Does NOT produce a Xero CSV. Mick prepares the journals manually from
  the figures the skill surfaces.
- Does NOT compute the YE stock value journal. Mick does this manually
  based on the stock valuation PDF and the prior-year journal pattern.
- Does NOT pull FX rates or USD/EUR cash balances. Mick supplies these
  from XE.com (rates) and the ii portal (positions).

## Prerequisites

Mick needs to provide:

1. **The ii transactions CSV** for the YE window. Downloaded from the ii
   portal: Account > Transactions > Date Range (set to 30/11/PRIORYEAR
   to 30/11/CURRENTYEAR) > Export as CSV.
2. **The existing tracking spreadsheet XLSX** (the prior-year FINAL
   version), used both as a template for styles and as the source of
   the ticker -> friendly-name lookup. Typical path:
   `C:\Users\pavey\Documents\0.2 - Areas (n)\M - Ditty Box\01 - Ditty
   Box Ltd - Xero\<YE folder>\<spreadsheet>.xlsx`
3. **The YE opening GBP cash balance** (= prior YE closing GBP cash
   after FX adjustment). For YE 2025 this was 4520.16.
4. **The YE date** in YYYY.MM.DD form (e.g. 2025.11.30).
5. **The date today** in YYYY.MM.DD form, for filenames.

Optional but useful (skill writes FLAG placeholders if missing):

6. **EUR/GBP rate at YE** (mid-market, 6 decimal places, from XE.com).
7. **USD/GBP rate at YE** (mid-market, 6 decimal places, from XE.com).
8. **EUR cash position at YE** (typically 1.59 - unchanged for years).
9. **USD cash position at YE** (varies - Mick checks the ii portal).
10. **The ii portfolio valuation PDF** (for stock value cross-check).

If Mick supplies 6-9, the skill plugs them in and computes Total Cash.
If not, the FX rows are left with FLAG placeholders for Mick to fill.

## The ii CSV format (background)

Downloaded ii transactions come as an 11-column CSV in REVERSE
chronological order. Columns:

| Col | Header | Notes |
|-----|--------|-------|
| 1 | Date | DD/MM/YYYY, trade date |
| 2 | Settlement Date | DD/MM/YYYY |
| 3 | Symbol | Ticker (or 'n/a' on some rows) |
| 4 | Sedol | SEDOL code |
| 5 | Quantity | Shares traded (or 'n/a') |
| 6 | Price | Price per share (or 'n/a') |
| 7 | Description | Free text - the most useful identifier |
| 8 | Reference | ii trade reference |
| 9 | Debit | Money out of ii cash (may have GBP-sign prefix and comma thousands) |
| 10 | Credit | Money into ii cash (same format) |
| 11 | Running Balance | GBP cash balance after this txn |

Important: the CSV file may have a UTF-8 BOM prefix (often multiple
BOM characters stacked) before the header. The parser strips these.

Money fields may appear as plain numbers (older exports) or with GBP
sign and comma thousands separators (current format, observed YE 2025).
The parser handles both.

## Transaction classification

Each ii row is classified into one of six categories:

| Category | Detection rule | Lands in tracking sheet column |
|---|---|---|
| INTEREST | Description = "GROSS INTEREST" | C: Int, S: Interest |
| DIVIDEND | Description starts "Div " | C: DIV, Q: Dividends |
| WITHDRAWAL | Description starts "PAYMENT", Debit set | C: Cash, N: Withdrawn |
| DEPOSIT | Description starts "PAYMENT", Credit set | C: In, M: Added |
| BUY | Symbol present + Debit set | C: P, U: Purch Total |
| SELL | Symbol present + Credit set | C: S, T: Sales Total |

Edge case: some sells appear with Symbol = "n/a" (observed YE 2024 SHG
sell). Fallback: regex-match the numeric quantity at the start of the
Description and treat as SELL if Credit is set.

## Tracking spreadsheet (target) layout

The master spreadsheet has 26 columns. The skill only writes to the
first 21 (col V-Z are historic, unused for new entries).

| Col | Header | Purpose |
|---|---|---|
| A | Date | YYYY.MM.DD format |
| B | Investment Detail | Friendly name (or "Account Interest", "BACS withdrawal", etc) |
| C | Purch/sale | P / S / DIV / Int / Cash / In / Fee |
| D | Shares | Quantity (where applicable) |
| E | Price (GBP)/share | Per-share price or implied div per share |
| F | Sub-total | Qty x Price |
| G | Commn. | Broker commission (often residual = J - F) |
| H | Stamp Duty | Usually 0 on AIM stocks |
| I | Levy | PTM levy |
| J | Total | Gross cost (buy) or net proceeds (sell) or amount (div/int) |
| K | Balance | Running cash GBP after this row (ties to ii Running Balance) |
| L | Av.price | Weighted average cost per share for this ticker |
| M | Account Added | Cash deposits in |
| N | Account Withdrawn | Cash withdrawals out |
| O | Capital Gain | On sells, where net proceeds > book cost |
| P | Capital Loss | On sells, where net proceeds < book cost |
| Q | Investm't Dividends | Dividend income |
| R | Account Charges | Admin fees etc |
| S | Account Interest | Cash interest received |
| T | Sales Total | GROSS sale proceeds (qty x price) |
| U | Purch Total | Total purchase cost (qty x price + fees) |

Note for SELLS: column T captures GROSS proceeds (qty x price), not
the net Credit received from ii. The difference is the broker
commission. For YE 2024 SHG sell: T = 3,678.40 (qty 24938 x 0.147502),
ii Credit = 3,674.43, residual GBP 3.97 = commission.

## YE summary block (writes 5 rows at the foot of each YE block)

After all transaction rows for the year, the skill writes:

1. **Rounding adjustment** (or "Foreign Exchange Revaln. Adjustment"
   if the drift is large). Col J = adjustment amount, col K = balance
   after adjustment. If the running balance ties cleanly to ii (which
   it should), the adjustment is 0 and the row is labelled "Rounding
   adjustment" (matching YE 2022 and YE 2023 convention).
2. **Cash Held in Euros**: F = EUR amount, G = "Euros", H = "x ",
   I = EUR/GBP rate, J = "=", K = GBP equivalent (= F x I).
3. **Cash Held in $US**: F = USD amount, G = "USD", H = "x ",
   I = USD/GBP rate, J = "=", K = GBP equivalent (= F x I).
4. **Total Cash (ii D.Box Account)**: K = sum of GBP cash + EUR equiv
   + USD equiv. Stored to 6dp to match Mick's historic precision.
5. **YE 30.11.YYYY : Totals : GBP**: row that sums each P&L analysis
   column for the year (G, H, M, N, O, P, Q, R, S, T, U).

## Stock valuation (basis for YE journal)

The basis is **whole-account lower of cost or net realisable value**.
NOT per-line. Confirmed by Mick on 2026.05.28.

Process:
1. Sum the cost column from the ii portfolio valuation PDF.
2. Sum the market value column from the same PDF.
3. The YE stock value = MIN(total cost, total market value).

For YE 2025 example: total cost 44,670.95, total market value
16,821.30 -> stock value = 16,821.30 (market value, because lower).

The stock value JOURNAL (movement vs prior YE) is prepared manually by
Mick based on the prior-year handwritten template. Account codes seen
in prior years: Dr 350 (Stock - shares held) / Cr 625 (Val'n of UK
Shares). Direction depends on whether stock has gone up or down -
check the prior year for the direction convention and confirm with
Jade if unsure.

## Ticker -> friendly name lookup

Mick names his investments "Company Name (TICKER)" - e.g. "Serica
Energy (SQZ)", "PetroTal Corp. (PTAL)". The skill builds the lookup
by scanning the Detail column of the existing tracking spreadsheet:
any string with a "(TICKER)" pattern is recorded as the friendly
name for that ticker. The most recent entry wins (in case Mick has
changed the name over time).

For NEW tickers not in history, the skill infers a friendly name
from the description text plus ticker (e.g. "Trellus Health" from
"TRELL HEALTH ORD" in the description + ticker "TRLS"). This is
ALWAYS flagged for Mick to confirm in the workings note.

## Output files

Three outputs land in `C:\Vaults\DB-Accounts-CW\YE_YYYY.11.30\workings\`:

1. **Extended tracking spreadsheet**:
   `YYYY.MM.DD - D.Box_ii_Investment_SpSheet_YE_YYYY.11.30_v.01.00_DRAFT.xlsx`
   - Preserves ALL historic rows untouched (typically 1275+)
   - Adds blank separator + YE header + 22-ish tx rows + 5-row summary
2. **Audit workings XLSX**:
   `YYYY.MM.DD - D.Box_ii_Audit_workings_YE_YYYY.11.30_DRAFT.xlsx`
   - Sheet 1 "Transactions": row-by-row cross-check with bal verification
   - Sheet 2 "YE Summary": cash position, P&L totals, reconciliation,
     numbered list of figures Mick lifts for journals
   - Sheet 3 "Stock Valuation 30.11.YYYY": holdings table + LCNRV
     calculation (whole-account basis)
3. **Workings note Markdown**:
   `YYYY.MM.DD - ii_Workings_Note.md`
   - Documents the run, flags anything needing Mick's input

## Running the script

```bash
python3 /path/to/skills/ii-to-xero/scripts/convert.py \
  --csv "/path/to/ii_transactions.csv" \
  --existing-xlsx "/path/to/prior_year_tracking_spreadsheet.xlsx" \
  --output-dir "C:/Vaults/DB-Accounts-CW/YE_2025.11.30/workings" \
  --opening-balance 4520.16 \
  --ye-date 2025.11.30 \
  --date-today 2026.05.28 \
  --eur-rate 0.876661 \
  --usd-rate 0.755396 \
  --eur-cash 1.59 \
  --usd-cash 209.90 \
  --portfolio-pdf "/path/to/portfolio_valuation.pdf"
```

The `--eur-rate`, `--usd-rate`, `--eur-cash`, `--usd-cash`, and
`--portfolio-pdf` flags are optional. If omitted, the corresponding
rows are written with FLAG placeholders.

The script prints the run summary, classification counts, and the YE
totals. Exits non-zero if running-balance reconciliation fails (the
single most important integrity check).

## Conversion process (script logic)

1. **Parse CSV**: read, strip BOM, parse money fields (handles both
   plain numeric and GBP-sign-with-commas), parse DD/MM/YYYY dates.
2. **Classify**: tag each row as INTEREST / DIVIDEND / WITHDRAWAL /
   DEPOSIT / BUY / SELL based on rules in the table above.
3. **Sort chronologically**: ascending by date, then DESCENDING by CSV
   row index for ties (because ii lists same-day txns in reverse-chron).
4. **Verify running balance**: chain from opening balance, check every
   row matches ii's reported Running Balance. Halt with detail on any
   drift.
5. **Build ticker lookup**: scan existing XLSX Detail column for
   "(TICKER)" patterns, build the map. New tickers seen in the CSV
   that aren't in the lookup get an inferred friendly name with FLAG.
6. **Generate tracking-sheet rows**: 26 columns per row, populating the
   right P&L analysis column based on category.
7. **Compute YE summary**:
   - Rounding adjustment (= 0 if balance ties, else drift amount)
   - EUR row (with rate / GBP-equiv if supplied)
   - USD row (with rate / GBP-equiv if supplied)
   - Total Cash row (computed only if both EUR and USD have rates+amounts)
   - YE totals row (sums P&L category columns)
8. **Write extended XLSX**: load existing workbook, append YE block
   from row max_row + 2 onwards, copy styles from prior year template
   rows.
9. **Write audit XLSX**: three sheets as described above.
10. **Write workings note**: Markdown summary with flags.

## Cowork sandbox null-pad workaround

When the script runs in a Cowork Windows-mounted sandbox, writes to
the Windows-mounted output folder can pad XLSX zip envelopes with
trailing null bytes, corrupting the file. The script writes XLSX to
`/tmp` first then `cp`s across. Verified end-of-file bytes against a
valid zip End-Of-Central-Directory record after each write.

## Known gotchas

1. **CSV money format varies**: older ii exports had plain numeric
   amounts; current (2025) exports include GBP sign and comma thousands
   separators. Parser handles both.
2. **Same-day ordering**: ii lists same-day transactions in reverse
   chronological order. Naive sort-by-date alone breaks the running
   balance check. Always secondary-sort by reverse CSV index.
3. **Symbol = n/a on some sells**: parser falls back to numeric-prefix
   detection in the description.
4. **UTF-8 BOM stacking**: some exports have multiple BOM characters
   stacked before the first header word. Parser strips all.
5. **Stock valuation basis**: WHOLE ACCOUNT lower of cost or NRV, not
   per-line. Easy mistake.
6. **FX revaluation = rounding adjustment when zero**: if the running
   balance ties cleanly to ii (it should), the summary row is labelled
   "Rounding adjustment" with value 0. The "Foreign Exchange Revaln.
   Adjustment" label is reserved for years where there is real drift
   (e.g. YE 2024 had 126.12 - the only year on record with one).
7. **USD dividends paid in GBP**: ii converts USD dividends (PTAL, JSE
   etc) to GBP before deposit. The spreadsheet records the GBP amount.
   The USD cash position is tracked separately and changes only via
   manual USD movements (rare).
8. **Default EUR amount = 1.59**: unchanged from at least YE 2022 onwards.

## If the script fails

If `scripts/convert.py` is not available or fails, Cedric can
replicate the logic from this SKILL.md - the parsing approach, the
column mapping table, and the summary block structure are all
documented above.

## After conversion

Tell Mick:
1. The YE cash position (GBP, EUR-equiv, USD-equiv, total).
2. The classification counts (e.g. "12 interest, 7 dividends, 1 buy,
   2 withdrawals").
3. The running-balance reconciliation result (CLEAN to the penny is
   the expected outcome).
4. The YE P&L totals (dividends, interest, sales, purchases,
   withdrawals).
5. Any new tickers that needed an inferred friendly name (flag for
   confirmation).
6. The stock value figures (cost, market value, LCNRV) for Mick's
   manual stock journal.

Then remind Mick to:
- Open the extended XLSX and eyeball the YE block
- Open the audit XLSX YE Summary sheet for the numbered list of
  figures to lift for journals
- Drop `_DRAFT` from filenames when copying to the live Xero folder
- Commit the workspace from PowerShell with a session-descriptive
  commit message

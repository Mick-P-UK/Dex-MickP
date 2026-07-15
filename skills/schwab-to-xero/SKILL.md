---
name: schwab-to-xero
description: >
  Processes the Charles Schwab (Corporate account ...366) year-end
  transaction download for Ditty Box Ltd into the figures Mick keys into
  Xero as two manual cash transactions (Receive Money and Spend Money) plus
  the year-end stock revaluation journal. Use this skill whenever Mick asks
  to "process the Schwab account", "do the Schwab import", "run the schwab to
  xero job", "do the Schwab year-end", "convert the Schwab CSV", "prepare the
  Schwab schedules for Xero", or any request to turn the year's Schwab
  transaction download into the Receive/Spend schedules and the stock journal.
  Always use this skill rather than parsing the CSV by hand. NOTE: like
  ii-to-xero (and unlike natwest-to-xero or cc1136-to-xero) this skill does
  NOT produce a Xero CSV import file. The Schwab account is USD and Xero is
  GBP-only, so it produces an audit XLSX and a posting schedule from which
  Mick keys two manual Receive/Spend transactions and posts the stock journal.
---

# Charles Schwab (...366) to Xero - Year End Workflow

This skill folds the year's Schwab transaction CSV download into Mick's
six-category cash analysis and surfaces the figures for three Xero postings:
a Receive Money transaction, a Spend Money transaction, and a manual stock
revaluation journal.

## When to use

Once a year, during the Ditty Box Ltd annual accounts cycle, to process the
Schwab USD brokerage account (Corporate account ending 366, "D.Box -
C.Schwab ($ Cash)" in Xero, formerly OptionsXpress).

## What this skill does and does NOT do

Does:
- Classify every Schwab cash row into Mick's six-code scheme.
- Total each category in USD and convert to GBP at the single year-end rate.
- Build the two Xero cash schedules (Receive / Spend) in USD and GBP.
- Compute the year-end stock revaluation journal (lower of cost or NRV,
  whole account).
- Produce a stock-adjustment audit PDF - a typeset replica of Mick's
  handwritten YE stock working (cost/market/lower table, GBP conversion,
  the increase/decrease line, and the Dr/Cr journal box) for the accountant.
- Reconcile net cash movement against the opening and closing cash balances
  (the key integrity check) and refuse to pass if it does not tie.

Does NOT:
- Produce a Xero CSV. Mick keys the two transactions and the journal manually.
- Pull FX rates or positions. Mick supplies the year-end USD/GBP rate (from
  XE.com) and the cost basis / market value / cash balances (from the Schwab
  Positions screen).
- Touch the live Xero folder. Outputs land in the workspace only.

## Key facts (Ditty Box specific)

- Xero is GBP-only. Every USD figure is converted at ONE year-end USD/GBP
  rate that Mick records himself to 6 dp from XE.com mid-market. The GBP
  figure is keyed into Xero; the USD is shown in brackets in the line
  description (matching prior years). Do not invent or estimate the rate.
- Stock valuation basis is WHOLE-ACCOUNT lower of cost or net realisable
  value (market), not per line. Compare the two account totals, take the
  lower. (Same basis as the ii account.)
- The stock journal posts the MOVEMENT vs the prior year's carrying value,
  not the absolute. Account codes: 637 "Val'n of Shares Held" (balance sheet
  asset) and 352 "Stock YE" (P&L closing stock). Increase = Dr 637 / Cr 352.
  Decrease = Dr 352 / Cr 637.

## Prerequisites - what Mick must provide

1. The Schwab transactions CSV for the YE window (Schwab portal >
   Transaction History > set range to the accounting year > Export CSV).
   It downloads in REVERSE chronological order with 8 columns:
   Date, Action, Symbol, Description, Quantity, Price, Fees & Comm, Amount.
2. The year-end USD/GBP rate (6 dp, XE.com mid-market on the YE date).
3. From the Schwab Positions screen at YE: Total cost basis (USD) and
   Total market value (USD).
4. The prior year's stock carrying value in GBP (last year's lower-value x
   last year's rate, AS BOOKED). For YE 2024 this was 11,181.33; that becomes
   the --prior-carrying-gbp input for YE 2025.
4a. For the audit PDF's prior-year row (optional but recommended for a
   complete sheet): the prior year's cost basis USD, market value USD, and
   USD/GBP rate. For YE 2025 these were 15,385.20, 14,240.13 and 0.785199.
   Pass as --prior-cost-basis, --prior-market-value, --prior-rate. If
   omitted, the PDF still produces but the prior row shows only the booked
   GBP carrying value.
5. Opening USD cash (= prior YE closing cash) and closing USD cash (YE
   Positions screen "Total cash & cash invest"). These drive the
   reconciliation. For YE 2025: opening 2,209.52, closing 3,454.49.
6. The YE date and today's date in YYYY.MM.DD form (for filenames).

## The six-code classification scheme

Each Schwab row carries one code in the analysis (column F in Mick's hand
sheet). Mapping of Schwab Action -> code -> Xero line:

| Code | Category            | Schwab Action(s)                      | Xero posting line                          |
|------|---------------------|---------------------------------------|--------------------------------------------|
| 1    | Dividends (+)       | Qualified Dividend, Special Qual Div  | Receive: Dividend Income                   |
| 2    | Sale of US shares(+)| Sell, Cash/Stock Merger (cash leg), Cash In Lieu* | Receive: Sale of Options/Shares (US) |
| 3    | Fees (-)            | ADR Mgmt Fee                          | Spend: SDRT Levy                           |
| 4    | Purchase (-)        | Buy                                   | Spend: Purchase of Options/Shares (US)     |
| 5    | Withholding Tax (-) | NRA Tax Adj, Foreign Tax Paid         | Spend: Provision for Corporation Tax       |
| 6    | Account Interest(+) | Credit Interest, ADR Mgmt Fee Adj     | Receive: Stockbroking Account Interest     |

Non-cash rows (no code, no posting): Stock Merger / Cash/Stock Merger share
legs, Reverse Split, and any share-receipt row with a blank Amount. These
change share counts only and are already reflected in the YE cost/market
figures used for the stock journal.

* Cash In Lieu is the cash paid for a fractional share - economically
  disposal proceeds, so the default is code 2 (Sale). One year (YE 2024) a
  cash-in-lieu was folded into Dividends instead; pass --cil-to-dividends to
  reproduce that treatment. The difference is normally immaterial - always
  flag it for Mick.

The Schwab "Amount" column is already NET of any sell commission (the
Fees & Comm column is informational), so sales use the net Amount, matching
how Mick has always done it.

## Xero postings built from the codes

RECEIVE MONEY (one transaction, dated YE, ref "Money Rec'd - YE <date>"):
- Sale of US shares      = code 2 total
- Dividend Income        = code 1 total
- Account Interest Rec'd = code 6 total

SPEND MONEY (one transaction, dated YE, ref "SChwab - Costs (YE <date>)"):
- Purchase of Shares (US)        = code 4 total
- Provision for Corporation Tax  = code 5 total (withholding)
- SDRT Levy                      = code 3 total (ADR mgmt fees; often nil)

## Stock revaluation journal

1. Lower value (USD) = MIN(cost basis, market value) at YE.
2. Carrying value (GBP) = lower value x year-end rate.
3. Movement (GBP) = this year's carrying value - prior carrying value.
4. Journal dated YE:
   - If movement > 0 (stock up): Dr 637 / Cr 352, amount = movement.
   - If movement < 0 (stock down): Dr 352 / Cr 637, amount = |movement|.

## The reconciliation (the integrity check)

opening cash + net cash movement (Receive total - Spend total) must equal
closing cash, to the cent. The script halts with a non-zero exit if it does
not. A clean tie proves the CSV captured the whole year with no gap or
overlap with the prior download. (For YE 2025: 2,209.52 + 1,244.97 =
3,454.49, clean.)

## Output files

Three outputs land in `C:\Vaults\DB-Accounts-CW\YE_YYYY.11.30\workings\`:

1. Audit XLSX: `YYYY.MM.DD - Schwab Account - YE YYYY.11.30 Workings and
   Schedules.xlsx`
   - Sheet 1 "Transactions": every row, date-ordered, with code and the six
     category columns; totals row at the foot.
   - Sheet 2 "Summary & Schedules": the Receive and Spend schedules (USD,
     rate, GBP), the cash reconciliation with a RECONCILED/CHECK flag, and
     the stock revaluation journal. All live formulas, zero errors.
2. Posting schedule Markdown: `YYYY.MM.DD - Schwab Account - YE YYYY.11.30
   Posting Schedule.md` - numbered Xero steps plus flags.
3. Stock-adjustment audit PDF: `YYYY.MM.DD - Schwab Account - YE YYYY.11.30
   Stock Adjustment (audit trail).pdf` - a typeset replica of Mick's
   handwritten YE stock working, for filing alongside the prior-year
   handwritten sheets and showing the accountant. Shows the prior and
   current year cost/market/lower table, the GBP conversion at each year-end
   rate, the increase/decrease line, and the Dr 637 / Cr 352 journal box.
   Needs reportlab (pip install reportlab --break-system-packages); if it is
   missing the PDF is skipped with a note and the other two outputs still
   produce. The prior-year row of the table is fully shown only if
   --prior-cost-basis, --prior-market-value and --prior-rate are supplied
   (see prerequisites); otherwise the prior year shows just its booked GBP
   carrying value.

## Running the script

```bash
python3 /path/to/skills/schwab-to-xero/scripts/convert.py \
  --csv "/path/to/schwab_transactions.csv" \
  --output-dir "C:/Vaults/DB-Accounts-CW/YE_2025.11.30/workings" \
  --ye-date 2025.11.30 \
  --date-today 2026.06.05 \
  --usd-rate 0.755396 \
  --cost-basis 15260.89 \
  --market-value 28968.16 \
  --prior-carrying-gbp 11181.33 \
  --prior-cost-basis 15385.20 \
  --prior-market-value 14240.13 \
  --prior-rate 0.785199 \
  --opening-cash 2209.52 \
  --closing-cash 3454.49
```

Optional flags:
- `--cil-to-dividends` routes Cash In Lieu to Dividends instead of Sale.
- `--prior-cost-basis`, `--prior-market-value`, `--prior-rate` populate the
  full prior-year row of the stock-adjustment audit PDF.

The script prints the run summary, category totals, the reconciliation
result, and the stock movement. It exits non-zero if the cash does not
reconcile - the single most important check before Mick posts anything.

## After conversion - tell Mick

1. The Receive and Spend totals (USD and GBP) and the three lines of each.
2. The reconciliation result (RECONCILED to the cent is expected).
3. The stock journal: lower value, GBP carrying value, movement, Dr/Cr.
4. Any flags - especially merger cash and cash-in-lieu treatment, and which
   way round the lower-of-cost-or-NRV fell this year.

Then remind Mick to:
- Open the audit XLSX Summary sheet and eyeball the schedules.
- Key the two Xero transactions and post the stock journal.
- Commit the workspace from PowerShell with a session-descriptive message.

## Cowork sandbox null-pad workaround

The script writes each XLSX to /tmp first then copies it to the
Windows-mounted output folder, to avoid the Cowork null-pad bug that
corrupts XLSX zip envelopes written directly to the mount. The Markdown is
written directly (text is unaffected).

## Known gotchas

1. Schwab dates may read "MM/DD/YYYY as of MM/DD/YYYY"; the parser uses the
   first (booking) date.
2. Amount is already net of sell commission - do not deduct Fees & Comm again.
3. New corporate-action Action types can appear year to year (YE 2025 had
   "Cash/Stock Merger" from the MAG->PAAS takeover, not seen in YE 2024).
   The classifier treats a Cash/Stock Merger row as Sale if it carries cash,
   non-cash otherwise. Any Action it cannot map but that carries cash is
   emitted as an UNCLASSIFIED FLAG rather than silently dropped - never let
   an unhandled cash row through.
4. Stock valuation basis is WHOLE-ACCOUNT lower of cost or NRV. Easy mistake.
5. The lower value can be cost in one year and market in another (YE 2024 it
   was market, lower than cost; YE 2025 it was cost, lower than market). The
   script picks MIN automatically and flags which one applied.
6. The rate must be Mick's recorded year-end rate, never estimated.

## If the script fails

If `scripts/convert.py` is unavailable or errors, Cedric can replicate the
logic from this SKILL.md - the classification table, the Receive/Spend
mapping, the stock journal steps, and the reconciliation check are all
documented above. Validated against the YE 2025 run on 2026.06.05
(reconciled to the cent; stock movement GBP 346.69).

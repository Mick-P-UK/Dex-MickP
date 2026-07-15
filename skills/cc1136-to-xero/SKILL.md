---
name: cc1136-to-xero
description: >
  Converts a folder of monthly Halifax Clarity Credit Card (account ending
  1136) PDF statements into a Xero-ready CSV for the Ditty Box Ltd annual
  accounts, plus a detailed audit XLSX. Use this skill whenever Mick asks
  to "convert the Halifax statements", "do the CC1136 import", "prepare
  the credit card statements for Xero", "create the Xero CSV from the
  Halifax PDFs", "do the CC1136 to Xero job", "run the cc1136 skill", or
  any request to turn the year's Halifax 1136 PDFs into a Xero bank
  statement import file. Always use this skill rather than parsing the
  PDFs manually.
---

# Halifax CC 1136 to Xero Statement Converter

This skill converts the year's worth of monthly Halifax Clarity 1136 PDF
statements into two output files for the Ditty Box Ltd annual accounts:

1. **Xero import CSV** - the 11-column file matching Mick's existing
   format. The first two columns (`*Date`, `*Amount`) are what Xero
   actually imports; the other nine are audit/working columns.
2. **Audit XLSX** - three sheets: Transactions, per-statement
   reconciliation, and a YE summary. For Mick's review and Jade's
   audit trail.

## When to use

Once a year, during the Ditty Box Ltd annual accounts cycle, to import
the year's credit card transactions into Xero. The Halifax CC 1136 is
the company credit card and the only Halifax account in the books.

May also be used for interim reconciliations.

## Prerequisites

Mick needs to provide:

1. **The 13 monthly Halifax 1136 PDF statements** covering the YE
   window plus the wrap-around months. For YE 30 Nov YYYY this means
   statements dated roughly:
   - 20 Dec (YYYY-1): supplies early-December txns inside the YE
   - 20 Jan through 20 Nov YYYY: the 11 monthly statements within
   - 20 Dec YYYY: supplies late-November txns inside the YE (these
     fell after the 20 Nov statement cut but before 30 Nov)
2. **The YE opening balance** (carry-forward from the prior year's
   closing CC1136 balance). For YE 2025 this was -1786.33 GBP.
3. **The YE year** (e.g. "2025" for YE 30 Nov 2025).
4. **The date today** in YYYY.MM.DD form, for filenames.

If Mick doesn't supply these, Cedric should ask.

## Halifax PDF layout (background)

Halifax Clarity 1136 statements are 4-page text-based PDFs:
- Page 1: account summary (Previous balance, Payments received,
  New transactions, New balance, statement date)
- Page 2: T&Cs and contact info (skipped)
- Page 3: the transaction table (the bit we parse)
- Page 4: Summary box (skipped)

The page 3 transaction table has had two layouts in the wild:

**OLD layout** (Dec 2023 - June 2025):
| Date of transaction | Date entered | Description | Amount £ |

**NEW layout** (from July 2025 onwards):
| Card Ending | Date of transaction | Date entered | Description | Amount £ |

Halifax added a leading "Card Ending" column (value always "1136").
The parser auto-detects which layout by inspecting the header row
words for the word "Ending".

Within Description, three sub-columns (merchant, location, state) are
positionally aligned but not labelled - the parser uses pdfplumber
word x-coordinates to split them.

Foreign currency transactions have a second line under the main row
giving the original amount and rate, e.g. "19.00 USD @ 1.2701" - the
parser attaches this to the preceding transaction as an FX detail.

## Output format

The CSV mirrors Mick's prior-year template, 11 columns:

| Col | Header | Notes |
|-----|--------|-------|
| 1 | *Date | DD/MM/YYYY, transaction date |
| 2 | *Amount | Signed (negative = spend, positive = payment/refund) |
| 3 | Date entered | DD/MM/YYYY, posting date |
| 4 | Description | Merchant + FX detail in parens for foreign txns |
| 5 | Descr.2 | Location (city or website) |
| 6 | Descr.3 | State code (US) or country code |
| 7 | Amount1 GBP | Absolute amount |
| 8 | Amount2 | Signed amount (same as *Amount) |
| 9 | Balance GBP | Running balance through the year |
| 10 | Check Bal GBP | Reconciliation marker at statement boundaries |
| 11 | Notes | "<- Start of Yr Bal." / "<- New Balance" / "<- EofYr_Balance" |

Sign convention:
- Spends are NEGATIVE
- Customer payments to Halifax (PAYMENT RECEIVED) are POSITIVE
- Merchant refunds are POSITIVE

This matches the Xero liability-account convention (negative balance =
amount owed).

## Conversion process

Run the bundled script at `scripts/convert.py`. The script handles
everything but here is the logic:

### Step 1: Locate and parse all PDFs

Read each PDF in the input directory matching the Halifax filename
pattern (or all `.pdf` files if filenames don't match). For each:
- Parse page 1 for statement date and summary figures
- Detect page 3 layout (OLD vs NEW)
- Extract words from page 3 with x-y coordinates
- Group by row (top-coordinate clustering)
- Assign each word to a column by x-coordinate
- Build Transaction objects (merging FX continuation lines)

### Step 2: Per-statement reconciliation

For each statement, verify that the sum of parsed transactions equals
(Payments received - New transactions). Halt with an error if any
statement fails to reconcile.

### Step 3: Filter to YE window

Keep only transactions dated 01/12/(YYYY-1) to 30/11/YYYY inclusive.
Sort by posted date then transaction date (matches Mick's YE 2024
ordering convention).

### Step 4: Build running balance

Seed running balance from the supplied opening balance (the prior
year's CC1136 closing). For each transaction in chronological order,
add the signed amount.

### Step 5: Populate Check Bal markers

- First row: Check Bal = opening balance, Notes = "<- Start of Yr Bal."
- Last YE-window row from each statement (except the very last): Check
  Bal = running balance after that row, Notes = "<- New Balance"
- Last row of year: Check Bal = running balance, Notes = "<- EofYr_Balance"

The interior statement boundaries should match Halifax's reported
New balance (negated) for that statement. The script asserts this and
fails with a detailed mismatch report if not.

### Step 6: Write outputs

Two files in the output directory:

- **CSV**: `YYYY.MM.DD - D.Box_HX-CC-1136_Xero-import_YE_<year>_DRAFT.csv`
- **XLSX**: `YYYY.MM.DD - D.Box_HX-CC-1136_Audit-workings_YE_<year>_DRAFT.xlsx`

The XLSX has three sheets:
- Transactions (same 11 columns plus three audit columns)
- Stmt Reconciliation (per-statement summary)
- YE Summary (opening, totals, closing)

Cedric should drop the `_DRAFT` suffix only after Mick confirms.

## Where to save

Both files go to: `C:\Vaults\DB-Accounts-CW\YE_<year>.11.30\workings\`

Mick then:
1. Reviews the XLSX audit sheets
2. Spot-checks a couple of months against the source PDFs
3. Copies the CSV (with `_DRAFT` removed) into the live Xero folder
   for upload
4. Records the year-end closing balance against the trial balance

## Running the script

```bash
python3 /path/to/scripts/convert.py \
  --input-dir "/path/to/folder/with/pdfs" \
  --output-dir "C:/Vaults/DB-Accounts-CW/YE_2025.11.30/workings" \
  --opening-balance -1786.33 \
  --ye-year 2025 \
  --date-today 2026.05.28
```

The script prints a per-statement reconciliation table and the YE
summary. Both output files are written to the specified output
directory. Exits non-zero if any reconciliation fails.

## After conversion

Tell Mick:
1. The YE opening balance (echoed) and YE closing balance (computed).
2. Total transaction count and net movement.
3. The per-statement reconciliation summary (should be 13 rows, all OK).
4. Any rows where the merchant/location split looks unusual (cosmetic
   only, doesn't affect Xero import).
5. Remind Mick to:
   - Open the XLSX and spot-check
   - Drop `_DRAFT` from the CSV filename before importing to Xero
   - Update the trial balance with the new YE closing CC1136 figure

## Known gotchas

- **Layout change mid-year**: Halifax changed page 3 layout from
  July 2025. The parser auto-detects but worth re-checking if
  Halifax changes layout again in future years.
- **"CR" with no space**: Some statements write "1,131.56CR" (no
  space before CR). The amount regex handles both.
- **Cowork sandbox null-padding**: When the script runs in a Cowork
  Windows-mounted sandbox, writes to the Windows-mounted output
  folder can be padded with null bytes. The script writes via /tmp
  and copies across to work around this.

## If the script fails

If `scripts/convert.py` is not available or fails, Cedric can
replicate the logic from this SKILL.md - the parsing approach is
documented in detail above.

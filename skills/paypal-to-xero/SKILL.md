---
name: paypal-to-xero
description: >
  Converts a PayPal transaction CSV/XLSX export into a Xero-ready bank
  statement import CSV plus a detailed audit XLSX. Designed for Ditty Box
  Ltd PayPal accounts (D.Box PayPal = code 058; Mick PayPal also supported
  if added). Use this skill whenever Mick asks to "convert the PayPal
  export", "do the PayPal import", "prepare the PayPal statement for Xero",
  "create the Xero CSV from PayPal", "do the PayPal-to-Xero job", "run
  the paypal skill", or any request to turn a PayPal year's transactions
  into a Xero bank statement import file. Always use this skill rather
  than parsing the PayPal CSV manually. Account code is a parameter, not
  hardcoded.
---

# PayPal to Xero Bank Statement Converter

This skill converts a PayPal transaction export into two output files
for Ditty Box Ltd bookkeeping:

1. **Xero import CSV** - a 5-column file (*Date, *Amount, Payee,
   Description, Reference) ready for Xero bank statement import. This
   is the primary deliverable.
2. **Audit XLSX** - a 20-column working spreadsheet preserving all the
   source detail plus a Review Annotation column (highlighted yellow)
   for Mick's manual notes before final import. SUM total formula on
   the Amount column for visual reconciliation.

## When to use

Once a year during the Ditty Box Ltd annual accounts cycle, to import
the year's PayPal transactions into the relevant Xero bank account.
Currently used for:

- **D.Box PayPal** - Xero code 058
- **Mick PayPal** - Xero code TBC (same skill, different code parameter)

May also be used for interim reconciliations.

## Prerequisites

Mick needs to provide:

1. **The PayPal transaction export** - downloaded from the PayPal
   business portal as CSV (preferred) or XLSX. The export covers the
   full YE window (01 Dec YYYY-1 through 30 Nov YYYY for Ditty Box).
2. **The Xero account code** (e.g. 058 for D.Box PayPal). If Mick
   doesn't specify, ask.
3. **The account short name** for filenames (e.g. "D.Box_PayPal" for
   the company account, "M_PayPal" for Mick's). If not obvious from
   context, ask.
4. **The YE year** (e.g. "2025" for YE 30 Nov 2025).
5. **The date today** in YYYY.MM.DD form for filenames.

Optional but helpful:
- The PDF version of the same statement (for cross-checking - the
  PayPal portal lets you download both).

## PayPal export format (background)

PayPal exports a verbose 62-column CSV/XLSX with UTF-8 BOM. The columns
include date/time, name, type, status, currency, gross/fee/net,
addresses, transaction event codes, balance, and many empty fields.

The key columns the skill uses:

| Column | Purpose |
|--------|---------|
| Date | DD/MM/YYYY transaction date |
| Name | Payee/payer name (only on parent rows) |
| Type | Transaction type description |
| Status | Completed/Pending |
| Currency | GBP/USD - skill drops all USD rows |
| Gross | Signed amount (negative = money out) |
| Fee | PayPal fee on this transaction (typically negative) |
| Transaction ID | Unique ID for this row |
| Reference Txn ID | Parent transaction ID (links child rows to parent) |
| Transaction Event Code | T-code identifying transaction type |
| Balance | Running balance after this row |

## Transaction Event Codes seen in Ditty Box exports

| Code | Type | Treatment |
|------|------|-----------|
| T0003 | Pre-approved Payment Bill User Payment | Keep GBP, drop USD |
| T0007 | Website Payment | Keep (split fee if present) |
| T0011 | Mobile Payment | Keep (split fee if present) |
| T0200 | General Currency Conversion | Keep GBP, drop USD; enrich GBP description with USD amount in brackets |
| T0300 | Bank deposit to PayPal account | Keep (GBP only) |
| T0403 | User Initiated Withdrawal | Keep - but Payee will be blank (PayPal does not link withdrawals to funding payments). Flag for Mick to fill via Review Annotation column |
| T0700 | General Credit Card Deposit | Keep (GBP only) |
| T6000 | Shopping Cart Item | ALWAYS DROP - line-item duplicate of parent |

## Transformation rules

1. **Drop all rows with Transaction Event Code T6000** (Shopping Cart
   Items - line-item duplicates of the parent transaction).
2. **Drop all rows with Currency = USD**. Xero PayPal accounts are
   GBP-only; PayPal always provides a mirroring GBP funding leg via
   `Bank deposit to PayPal account` and `General Currency Conversion`.
3. **For each remaining GBP row:**
   a. If Fee is non-zero, emit TWO output rows:
      - Main row: Amount = Gross, Description = source Type
      - Fee row: Amount = Fee, Description = "PayPal Fee"
   b. Otherwise emit a single row: Amount = Gross.
4. **Carry forward Payee Name** from parent transaction to child rows
   via `Reference Txn ID = parent Transaction ID`. PayPal puts the
   merchant/payer name only on the parent T0003/T0007/T0011 row;
   the child T0300/T0200/T0700 rows have blank Name.
5. **Enrich `General Currency Conversion` (T0200, GBP) descriptions**
   by appending the matching USD amount in brackets,
   e.g. `"General Currency Conversion ($26.39)"`. The USD amount
   comes from the paired USD T0200 row sharing the same Reference
   Txn ID.
6. **Sort output by date only**. Python's stable sort preserves
   PayPal's source order within a date. This matches Mick's manual
   convention (debit first for GBP-only payments, deposit first for
   USD-vendor conversions).

## What needs Mick's judgment (Review Annotation column)

The skill cannot infer these - they must be filled in manually by Mick
before final import (or after, during Xero reconciliation):

- **User Initiated Withdrawal** rows: no Reference Txn ID linking them
  to the funding payment. Auto-output has blank Payee. Mick fills in
  the source payer based on date and amount matching against earlier
  payments.
- **Contextual vendor annotations** Mick adds, e.g.
  `"(Plaza Subscription)"`, `"(Domain Name Renewal)"`,
  `"(Wordfence)"`. These come from Mick's knowledge of what the
  payments were for, not from any PayPal field.

The audit XLSX Review Annotation column is highlighted yellow to flag
these rows for manual review.

## Output format

### Xero import CSV (5 columns)

| Column | Notes |
|--------|-------|
| *Date | DD/MM/YYYY |
| *Amount | Signed decimal, 2dp (negative = money out) |
| Payee | Merchant/payer name (blank for User Initiated Withdrawals) |
| Description | Transaction type, enriched for currency conversions |
| Reference | PayPal Transaction ID |

### Audit XLSX (20 columns plus header block)

Columns: Date, Amount, Payee, Description, **Review Annotation**
(yellow), Reference, Status, Currency, Gross, Fee, Net, Balance,
Transaction ID, Reference Txn ID, Event Code, Balance Impact, From
Email, To Email, Note, Source Row.

Header block shows: account code (058), source filename, generation
timestamp, and a brief explanation of the transformation.

Footer row: SUM formula on the Amount column for visual reconciliation.

## File naming convention

Follow Mick's standard: `YYYY.MM.DD - description.ext`

- Xero CSV: `YYYY.MM.DD - <AccountPrefix>-<Code>_Xero-import_YE_<Year>_DRAFT.csv`
- Audit XLSX: `YYYY.MM.DD - <AccountPrefix>-<Code>_Audit-workings_YE_<Year>_DRAFT.xlsx`

Examples for D.Box PayPal (code 058):
- `2026.05.29 - D.Box_PayPal-058_Xero-import_YE_2025_DRAFT.csv`
- `2026.05.29 - D.Box_PayPal-058_Audit-workings_YE_2025_DRAFT.xlsx`

After Mick has filled in Review Annotations and confirmed, the suffix
becomes `_v.02_Mick-Confirmed` (matching the convention used for the
ii spreadsheet).

## Where to save

Both files go to: `C:\Vaults\DB-Accounts-CW\YE_<Year>.11.30\workings\`

## Running the script

```bash
python3 /path/to/scripts/convert.py \
  --input "/path/to/PayPal-export.CSV" \
  --output-dir "C:/Vaults/DB-Accounts-CW/YE_2025.11.30/workings" \
  --account-code "058" \
  --account-prefix "D.Box_PayPal" \
  --ye-year "2025" \
  --date-today "2026.05.29"
```

The script handles both CSV (with UTF-8 BOM) and XLSX inputs - the
file extension is auto-detected. Both output files are written to the
specified output directory.

## Verification checks (script runs these automatically)

The script prints a report after conversion:

1. **Source row count** - number of rows in the source.
2. **Output row count** - rows surviving the transformation (plus
   fee splits).
3. **Drop counts** by reason (T6000 Shopping Cart Items, USD rows).
4. **Fee splits** - count of rows where Gross+Fee were split into two
   output rows.
5. **Three-way reconciliation**:
   - Source GBP non-T6000 net movement (Gross + Fee for surviving rows)
   - Source PayPal final running balance (last GBP row's Balance)
   - Output Amount column total
   All three must agree to the penny. Script exits non-zero if not.
6. **Blank Payee count** - lists the User Initiated Withdrawal rows
   needing Mick's manual fill.
7. **New/unseen transaction types** - flags any T-codes not in the
   known list above, in case PayPal introduces new types.

## After conversion

Tell Mick:
1. Source rows / output rows / drop counts.
2. The three-way reconciliation result (closing balance figure).
3. The number of blank-Payee rows (User Initiated Withdrawals) needing
   his attention.
4. Any unseen transaction types that need investigation.
5. Remind Mick to:
   - Open the audit XLSX and fill in Review Annotations
   - Particularly fill in Payee for any User Initiated Withdrawal rows
     (match by date/amount to earlier payments)
   - Once confirmed, rename CSV with `_v.02_Mick-Confirmed` suffix
   - Import the CSV into Xero against the account code
   - Update the trial balance with the new YE closing PayPal figure

## Known gotchas

- **UTF-8 BOM**: PayPal CSV exports start with EF BB BF. Read with
  `encoding='utf-8-sig'` or the first column name parses garbled.
- **Fee column blank vs zero**: Some rows have `' '` (space) in Fee,
  others have `'0.00'`, others are truly blank. Treat all as 0.
- **User Initiated Withdrawal has no parent link**: Reference Txn ID
  is blank. Cannot infer Payee programmatically. Always flag for
  manual review.
- **Within-date order matters for Mick**: Use stable sort by date
  only. Do NOT sort by amount within a date - it puts deposits before
  payments and breaks Mick's manual convention.
- **Cowork sandbox null-padding**: Writes to Windows-mounted output
  folder can be padded with null bytes. Script writes via /tmp then
  copies across.

## If the script fails

If `scripts/convert.py` is not available or fails, Cedric can replicate
the logic from this SKILL.md - the transformation rules section
documents the algorithm in detail.

## Validation history

- Validated against YE 2024.11.30 source pair (Mick's manual v.07
  output): 25 rows, exact match for count, payees, descriptions,
  amounts, within-date order. Only deltas were Mick's contextual
  annotations (handled via Review Annotation column).
- Successfully run on YE 2025.11.30: 38 source rows -> 20 output rows,
  closing +234.38 GBP, imported clean into Xero account 058
  (confirmed by Mick 2026.05.29).

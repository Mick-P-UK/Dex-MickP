---
name: natwest-to-xero
description: >
  Converts a NatWest bank statement CSV export into a Xero-ready CSV for bank
  statement import, plus a detailed 11-column working XLSX for audit reference.
  Use this skill whenever Mick asks to "convert the NatWest CSV", "prepare the
  bank statement for Xero", "do the NatWest import", "process the bank
  transactions for Xero", "create the Xero CSV from NatWest", or any request
  to transform a NatWest bank download into Xero import format. Also triggers
  on "run the NatWest skill", "convert the bank statement", or "do the bank
  import for [account name]". Works for any NatWest account (GBP Current, No 2,
  USD, etc.) -- the account code is a parameter, not hardcoded. Always use this
  skill for NatWest-to-Xero conversions rather than doing them manually.
---

# NatWest to Xero Bank Statement Converter

This skill converts a NatWest online banking CSV statement export into two
output files ready for Ditty Box Ltd bookkeeping:

1. **Xero import CSV** -- the 6-column file Xero accepts for bank statement
   import. This is the primary deliverable.
2. **Working XLSX** -- an 11-column spreadsheet that preserves all the detail
   from the NatWest export (split description fields, running balances,
   transaction types) for Mick's reference and audit trail.

## When to use

Any time Mick uploads a NatWest CSV bank statement and wants it prepared for
Xero import. This happens at least once per year per bank account during the
annual accounts process, and potentially more often if Mick does interim
reconciliations.

## Prerequisites

Mick needs to upload:

1. **The NatWest CSV export** -- downloaded from NatWest online banking.
   Expected columns: Date, Type, Description, Value, Balance, Account Name,
   Account Number.
2. **The Xero bank code** -- which Xero account this maps to (e.g. 051 for
   NW GBP Current, 053 for NW Bus Reserve, 055 for NW USD, etc.). If Mick
   doesn't specify, ask.

Optional but helpful:
- The PDF version of the same statement (for cross-checking).
- The Xero import template CSV (for reference -- but the format is stable
  and documented below).

## Xero import format

Xero expects a CSV with these columns (asterisk = required):

| Column | Required | Notes |
|--------|----------|-------|
| *Date | Yes | DD/MM/YYYY for UK Xero accounts |
| *Amount | Yes | Signed decimal, 2dp (negative = money out) |
| Payee | No | Who the payment was to/from |
| Description | No | Additional detail |
| Reference | No | Payment reference if available |
| Check Number | No | Not used -- leave blank |

## NatWest CSV format

NatWest online banking exports a 7-column CSV:

| Column | Content |
|--------|---------|
| Date | DD Mon YYYY (e.g. "28 Nov 2025") |
| Type | Transaction type code (BAC, D/D, DPC, CHG, CDM, etc.) |
| Description | Comma-separated string with payee, reference, payment method |
| Value | Signed decimal (negative = money out) |
| Balance | Running balance after this transaction |
| Account Name | Company name |
| Account Number | Sort code and account number |

The CSV is exported in **reverse chronological order** (newest first). The
conversion must sort to chronological order (oldest first) before output.

## Conversion steps

Run the bundled Python script at `scripts/convert.py`. The script handles
everything, but here is the logic for reference:

### Step 1: Parse and validate the source CSV

- Read the NatWest CSV using Python's csv module.
- Confirm 7 columns with expected headers.
- Count data rows (exclude header).
- Parse all dates from "DD Mon YYYY" format.
- Confirm no blank rows or unparseable dates.

### Step 2: Sort chronologically

- Reverse the row list (NatWest exports reverse-chronological).
- Verify dates are now non-decreasing.

### Step 3: Derive the opening balance

- Opening balance = first row's Balance minus first row's Value.
- This should match the known closing balance from the previous year's
  accounts on this bank code. Cedric should confirm this with Mick.

### Step 4: Split the Description field

NatWest packs multiple pieces of information into the Description field,
separated by commas. Split on comma (preserving any leading/trailing spaces
on each segment, matching Mick's existing convention from prior years):

| Segment | Maps to |
|---------|---------|
| 1st | Payee |
| 2nd | Description-1 |
| 3rd | Pay't_Method |
| 4th | Reference |
| 5th+ | Ref.No. (join with commas if more than 5 segments) |

If fewer than 5 segments, the remaining columns are left empty/None.

For CHG-type rows (bank charges), the Description typically has no commas,
so the entire string goes into Payee and the rest stay empty.

### Step 5: Build the 11-column working XLSX

Columns (matching the convention from prior year files):

| Col | Header | Source |
|-----|--------|--------|
| A | *Date | Parsed datetime |
| B | *Amount | Value (signed) |
| C | Payee | Description segment 1 |
| D | Description-1 | Description segment 2 |
| E | Pay't_Method | Description segment 3 |
| F | Reference | Description segment 4 |
| G | Ref.No. | Description segment 5+ |
| H | Balance | Running balance |
| I | Orig_Amount | Copy of Value (for cross-ref) |
| J | Balance | Copy of running balance |
| K | Type | Transaction type code |

Format: dates as DD/MM/YYYY, amounts as #,##0.00, bold header row.

### Step 6: Build the 6-column Xero import CSV

Extract from the XLSX data:

| Xero column | Source |
|-------------|--------|
| *Date | DD/MM/YYYY string |
| *Amount | Value to 2dp |
| Payee | Segment 1, stripped of leading/trailing spaces |
| Description | Segment 2, stripped |
| Reference | Segment 4, stripped |
| Check Number | Empty string |

The CSV must use standard comma-delimited format with no BOM.

### Step 7: Run verification checks

The script runs these automatically and prints a report:

1. **Row count** -- data rows match source CSV.
2. **Date range** -- earliest and latest dates within the expected YE period.
3. **Chronological order** -- all dates non-decreasing.
4. **Opening balance** -- derived from first transaction, reported for Mick
   to confirm against prior year close.
5. **Closing balance** -- last row's balance.
6. **Sum of amounts** -- must equal closing minus opening balance.
7. **Running balance continuity** -- each row's balance equals previous
   balance plus current amount (no breaks).
8. **Amount consistency** -- *Amount matches Orig_Amount in every row.
9. **Spot-check** -- 5 randomly selected rows compared back to source CSV.
10. **Transaction type distribution** -- count by type for a quick sanity
    glance.

## File naming convention

Follow Mick's standard: `YYYY.MM.DD - description.ext`

- Working XLSX: `YYYY.MM.DD - D.Box_NW-<AccountShortName>-<Code>_Xero-import-ready_YE_<Year>.xlsx`
- Xero CSV: `YYYY.MM.DD - D.Box_NW-<AccountShortName>-<Code>_Xero-import_YE_<Year>.csv`

Examples for the GBP Current Account (code 051):
- `2026.05.27 - D.Box_NW-Curr-Acc-051_Xero-import-ready_YE_2025.xlsx`
- `2026.05.27 - D.Box_NW-Curr-Acc-051_Xero-import_YE_2025.csv`

Cedric should ask Mick for the short name if it is not obvious from context.

## Where to save

Both files go to: `C:\Vaults\DB-Accounts-CW\YE_<Year>.11.30\workings\`

The Xero CSV is the file Mick will import into Xero. The XLSX stays in
workings as an audit reference.

## After conversion

Tell Mick:
1. The row count and date range.
2. The opening and closing balances (ask Mick to confirm the opening balance
   ties to the prior year close on this bank code).
3. Any rows that might need a manual look (e.g. unusual transaction types,
   very large amounts, transactions on boundary dates).
4. Remind Mick to check for duplicates if Xero already has any transactions
   on this account for the period.

## Running the script

```bash
python3 /path/to/scripts/convert.py \
  --input "/path/to/natwest-export.csv" \
  --output-dir "/path/to/output/directory" \
  --account-code "051" \
  --account-name "Curr-Acc" \
  --ye-year "2025" \
  --date-today "2026.05.27"
```

The script prints the full verification report to stdout. Both output files
are written to the specified output directory.

If the script is not available or fails, Cedric can replicate the logic
manually using the steps above -- the SKILL.md documents everything needed.

## Account number masking (added 2026.07.14 - DO NOT REMOVE)

NatWest embeds the COUNTERPARTY ACCOUNT NUMBER in its own Description text:

    From A/C 06512917,PAVEY M A (current,Dir Loan to D.Box

Earlier versions passed the Description straight through, so the full 8-digit
number landed in the Payee field of the Xero import CSV, in the working XLSX,
and from there into the git repo. Found 2026.07.14: twenty rows of the YE 2025
051 import carried three full account numbers. That breaches the standing rule
in CLAUDE.md - "NEVER write bank account numbers in full in any file or chat -
mask middle digits".

split_description() now calls mask_account_numbers() FIRST. That is the single
funnel every output field passes through, so one mask covers Payee,
Description, Reference and Ref.No. across BOTH outputs.

Rule: an 8-digit run ANCHORED to an account marker (A/C, ACCOUNT, ACC NO) is
rewritten to house style ****<last 4>. "A/C 06512917" becomes "A/C ****2917" -
still identifiable to Mick, no longer disclosive.

Deliberately NOT masked: bare 8-digit runs with no account marker, and
alphanumeric references such as 82835006G22JAHOGSU. Those are genuine payment
references, and blanket-masking would corrupt the import.

Verified 2026.07.14 against the real YE 2025 strings: all four account-number
forms masked (From A/C, To A/C, and the "31JAN A/C ..." bank-charge references),
all genuine references (Google Cloud, Amazon, Slack) untouched, zero 8-digit
runs surviving. Only account 051 was ever affected - 053, 1136 and PayPal were
already clean.

NOTE: the YE 2025 files were deliberately NOT retro-masked. They are the record
of what was actually imported into Xero, and the original NatWest download lives
in the live Xero folder. This fix applies from YE 2026 onward.


---
title: Ditty Box Ltd Year End Accounts
tags:
  - SOP
type: SOP
status: draft
version: 0.9
created: 2026-07-26
owner: Mick
related-skills: natwest-to-xero, cc1136-to-xero, paypal-to-xero, ii-to-xero, schwab-to-xero, info-for-accountant
---

# SOP - Ditty Box Ltd Year End Accounts

## 0. Status of this document

Version 0.9, DRAFT. Written 2026-07-26 by reverse-engineering the six accounts skills,
the YE 30.11.2024 and YE 30.11.2025 working folders, and the pack sent to the
accountants for YE 30.11.2024.

Sections 5 and 6 describe what the evidence shows Mick did. Where a step is inferred
rather than documented, it is flagged **[CONFIRM]**. Mick should walk through the
sequence once, correct anything wrong, and promote this to version 1.0 status active.
Section 12 lists the open questions.

## 1. Purpose

This routine takes Ditty Box Ltd from a year's worth of raw bank, credit card, PayPal
and broker downloads through to a numbered pack of supporting evidence sent to the
accountants, from which they prepare the statutory accounts.

The company year end is 30 November. There is one run per year.

Six skills do the mechanical work. This SOP is the order they go in, what has to be
true before each one starts, and the manual steps between them that no skill covers.

## 2. When to Run It

Start once the year end has passed and the December statements have arrived, since
several accounts need a statement that straddles 30 November to evidence the closing
balance. In practice that means late December at the earliest.

Historically the work has run later than that - the YE 30.11.2024 pack went to the
accountants on 2025.06.26, and the YE 30.11.2025 pack was assembled 2026.07.26. Aim
earlier if possible; the Companies House filing deadline is nine months after the year
end. **[CONFIRM]** whether there is a date Mick works back from.

## 3. Environment and Prerequisites

**Environment.** The conversion skills (steps 1 and 2 below) read PDFs and CSVs from
the year folder and write outputs back to it. Run them wherever the year folder is
reachable - Claude Code locally, or Cowork with the year folder connected. The pack
assembly step is comfortable in Cowork, since device_bash can copy on Mick's own disk
without staging hundreds of megabytes through the cloud container.

Xero itself is browser work and Mick does it himself.

**Folder root:**

```
C:\Users\pavey\Documents\0.2 - Areas (n)\M - Ditty Box\01 - Ditty Box Ltd - Xero\
```

One folder per year end. Naming is not consistent between years - YE 30.11.2024 sits in
`01_YE 30.11.2024`, YE 30.11.2025 in `001_YE 30.11.2025`. Match on the `YE <date>`
portion, never the numeric prefix.

**Downloads needed before starting.** Gather these first; the skills cannot invent them:

| Source | What to download | Where it goes |
|--------|------------------|---------------|
| NatWest Current (0708) | Transactions CSV for 01.12 to 30.11, plus statements straddling both year ends | `Nat West - Curr Acc (GBP)` |
| NatWest No 2 (1208) | Same | `Nat West - No 2 Acc (GBP)` |
| NatWest USD | Currency revaluation, plus the year-end FX rate | `Nat West - $US Account` |
| Halifax Clarity CC-1136 | 13 monthly PDF statements (Dec prior year through Dec current) | `Halifax CC - 1136` |
| PayPal | Transactions CSV/PDF for 01.12 to 30.11, plus the year-end balance | `D.Box - PayPal` |
| Interactive Investor | Year's transactions CSV, portfolio valuation, cash position | `DB - ii Account` |
| Charles Schwab (...366) | Year's transactions CSV, valuation, holdings | `Schwab ($) Account` |

The Halifax download needs 13 statements, not 12. The 20 December statement of the
PRIOR year supplies early-December transactions that fall inside the year end, and the
20 December statement of the CURRENT year supplies late-November ones that fell after
the 20 November cut. See `cc1136-to-xero` for the detail.

## 4. The Accounts and How They Reach Xero

Not every account reaches Xero the same way, which is the single most confusing part of
this routine. Three different mechanisms:

| Account | Xero code | Mechanism |
|---------|-----------|-----------|
| NatWest Current | 051 | CSV bank statement import |
| NatWest No 2 / Bus Reserve | 053 | CSV bank statement import |
| NatWest USD | - | Manual currency revaluation |
| Halifax CC-1136 | 059 | CSV bank statement import |
| PayPal | 058 | CSV bank statement import |
| Interactive Investor | - | Manual journals lifted off a working spreadsheet |
| Schwab (USD) | 062 | Two manual cash transactions plus a stock journal |

The two broker accounts do NOT produce a Xero CSV. `ii-to-xero` and `schwab-to-xero`
produce working spreadsheets and posting schedules; Mick keys the figures into Xero by
hand. This is deliberate - Xero is GBP-only and the Schwab account is USD.

## 5. Step-by-Step Sequence

### Step 1 - Bank and card imports (CSV route)

Run in any order. Each produces a Xero import CSV plus an audit XLSX:

1. `natwest-to-xero` for the Current account (051).
2. `natwest-to-xero` for the No 2 account (053). The account code is a parameter.
3. `cc1136-to-xero` for the Halifax card (059).
4. `paypal-to-xero` for D.Box PayPal (058).

Before importing each CSV, screenshot the Xero bank account showing the balance BEFORE
data entry. The pack wants this (item J16 for PayPal). **[CONFIRM]** whether Mick does
this for all four or only PayPal - only the PayPal one appears in the 2024 pack.

Import each CSV into Xero, then reconcile.

### Step 2 - Broker accounts (manual journal route)

5. `ii-to-xero`. Produces the extended tracking spreadsheet carrying history back to
   2008, plus an audit XLSX. Mick lifts figures for manual journals covering dividends,
   interest, withdrawals, purchases and the year-end stock valuation.
6. `schwab-to-xero`. Produces an audit XLSX and a posting schedule. Mick keys two
   manual cash transactions (Receive Money, Spend Money) and posts the stock
   revaluation journal.

### Step 3 - Manual journals and adjustments

Posted by hand in Xero, filed as PDFs in `Manual Journals`. From YE 30.11.2025 the set
was: accountancy fees, depreciation, valuation of UK shares, small stock difference
adjustment, director's loans, and the Schwab US stock adjustment. **[CONFIRM]** whether
this is a fixed list Mick works through or varies year to year.

Also in this step: the NatWest USD currency revaluation, using the year-end FX rate.

### Step 4 - Reconciliation

Reconcile every account to its statement. Working papers from the YE 30.11.2024 cycle
live in `Mick - YE 30.11.2024 Reconciliation` and show the pattern: trial balance
before and after journals, the bank charges account transactions, and a note per
correction. **[CONFIRM]** what Mick's own tick-and-turn process is here - this is the
least documented step and the one a future Cedric can help with least.

### Step 5 - Year-end screenshots and prints

These are the items only Mick can produce, and they are consistently the thing holding
the pack up. Do them as a batch:

- Halifax CC-1136 opening balance at 01.12 and closing balance at 30.11.
- Interactive Investor portfolio as at the PRIOR year end.
- Xero Trial Balance at the year end (draft).
- Xero Profit and Loss for the year, with account codes (draft).
- Xero Balance Sheet at the year end (draft).

Save them into the relevant sub-folder of the year folder with a descriptive filename
including the figure, following house convention (see section 7).

### Step 6 - Assemble the pack for the accountants

Run `info-for-accountant`. It derives the J-number manifest from the prior year's
pack, inventories the current year folder, proposes a mapping for Mick's approval,
copies (never moves) with md5 verification, builds the checklist spreadsheet, and
reports anything still outstanding.

If step 5 was done properly there will be no gaps and the pack can be zipped in the
same run. If not, the skill copies what exists and hands back a list.

### Step 7 - Send and close out

Send the zip to Jade at the accountants. File anything that comes back into
`Z - From Jade_YE_<date>`.

**[CONFIRM]** how the zip is sent - email, portal, shared folder?

The accountants return year-end journals (the YE 2024 set came back 2025.12.08 as
`From Jade-YE 2024 Journals to send to client.xlsx`). Post those in Xero to close the
year. **[CONFIRM]** whether that posting is part of this routine or handled separately.

## 6. Safety Rules

1. **The pack takes copies. Originals never move.** Every source file stays in its
   working folder. Verify with a file count before and after.
2. **Never guess between candidate files.** If two files could be the year-end
   valuation, ask. A wrong statement in the pack costs the accountants time and Mick
   credibility.
3. **Never post a journal without the working behind it filed.** Each manual journal
   should have its calculation saved alongside as a JPG or PDF - the pack asks for
   several of these (J08, J08A, J15).
4. **Reconcile before printing.** The Xero prints in the pack are the reconciled
   position. Printing them before step 4 is finished wastes the effort.
5. **Do not renumber the J items.** The numbering is stable across years so Mick and
   the accountants can refer to "J14" in an email. A missing item leaves a gap in the
   sequence; new items go on the end.

## 7. Conventions

- **Filenames:** `YYYY.MM.DD - <description>_<figure><currency>.<ext>`. The date is
  usually the date the file was PRODUCED, not the period it covers - a file named
  `2026.05.27` belongs to YE 30.11.2025. Include the figure in the name wherever there
  is one; it makes the pack self-checking.
- **Pack items:** `J<nn> - <original filename>`, in a `For sending 2 Jade` sub-folder.
- **Zip:** `D.Box_YE <date>_From Mick Pavey_<YYYY.MM.DD>.zip`.
- **Spreadsheets:** Mick's standard print footer on every sheet, per CLAUDE.md
  "Spreadsheet Print Footer": `(&[Path]&[File] - Printed: &[Date] at &[Time])`, left
  section.
- **ASCII only** in anything written to the vault.

## 8. Troubleshooting

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| Halifax parser returns no rows for a month | Statement uses the newer page-3 layout with the leading "Card Ending" column | `cc1136-to-xero` auto-detects this; if it still fails, check the PDF is text-based and not a scan |
| A November transaction is missing from the card import | It fell after the 20 November statement cut | Include the 20 December statement of the current year in the download set |
| Xero rejects the import CSV | Date format or column order | Only columns 1 and 2 (`*Date`, `*Amount`) are imported; check dates are DD/MM/YYYY |
| Schwab figures will not reconcile | USD to GBP conversion, or Xero being GBP-only | This account is deliberately manual; work from the posting schedule, not the raw CSV |
| Pack step reports many gaps | Step 5 not done | Do the screenshot and print batch, then re-run |
| The prior year's pack folder has odd numbering | Known defects: a `J33` that should be `J23`, a truncated duplicate `J04` | Do not copy these forward; `info-for-accountant` knows about them |

## 9. What Cedric Can and Cannot Do

Cedric can run all six skills, propose the pack mapping, build and verify the copies,
and produce the checklist.

Cedric cannot log into Xero, take the year-end screenshots, post journals, or send the
pack. Those are Mick's, and step 5 is where the routine always stalls - which is why
the pack skill's gap report matters more than its copying.

## 10. Related Skills

| Skill | Step | Output |
|-------|------|--------|
| `natwest-to-xero` | 1 | Xero CSV + audit XLSX |
| `cc1136-to-xero` | 1 | Xero CSV + 3-sheet audit XLSX |
| `paypal-to-xero` | 1 | Xero CSV + audit XLSX |
| `ii-to-xero` | 2 | Tracking spreadsheet + audit XLSX (manual journals) |
| `schwab-to-xero` | 2 | Audit XLSX + posting schedule (manual entries) |
| `info-for-accountant` | 6 | Numbered pack, checklist XLSX, gap report, zip |

## 11. Related Documents

- `skills/info-for-accountant/reference/manifest.md` - the J01-J25 item manifest
- `skills/README.md` and `SKILLS_REGISTRY.md` - skill registration
- `CLAUDE.md` - "Spreadsheet Print Footer" rule
- `C:\Vaults\_SOPs\INDEX.md` - vault-level SOP index (this SOP must be registered there)

## 12. Open Questions

Answer these and this document goes to version 1.0:

1. Is there a target date Mick works back from, or does the run start when it starts?
2. Does Mick screenshot the Xero balance before data entry for all four CSV imports, or
   only PayPal?
3. Is the manual journal list fixed, or does it vary by year?
4. What is the reconciliation process in step 4, in enough detail to document?
5. How is the zip sent to the accountants?
6. Are the accountants' returned journals posted as part of this routine or separately?
7. Should `paypal-to-xero` be promoted to a Cowork skill? It is the only one of the
   five converters not currently visible there.

## 13. Revision History

- v0.9 (2026-07-26, Cedric) - First draft, reverse-engineered from the six accounts
  skills and the YE 30.11.2024 and YE 30.11.2025 working folders while building the
  `info-for-accountant` skill. Written because no SOP for this routine existed. Twelve
  open questions flagged for Mick; sections 5 and 6 need his walkthrough before this
  goes to status active.

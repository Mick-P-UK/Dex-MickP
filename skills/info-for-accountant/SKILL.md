---
name: info-for-accountant
description: >
  Assembles the annual year-end information pack that Mick sends to the
  accountants for Ditty Box Ltd. Copies (never moves) the supporting
  evidence out of the year's working folders into the "Z - For
  Jade_YE_<date>" folder, renames each copy with a J-number, builds the
  checklist spreadsheet, reports what is still outstanding, and zips the
  pack when Mick says it is complete. Use this skill whenever Mick asks
  to "do the pack for the accountant", "pull the info together for
  Jade", "build the Jade pack", "do the year end pack", "info for
  accountant", "run the info-for-accountant skill", "package up the year
  end files", or any request to gather the year's supporting documents
  for the accountants. Always use this skill rather than copying files
  ad hoc.
---

# Info for Accountant - Ditty Box Ltd Year End Pack

Once a year, at the end of the Ditty Box Ltd accounts cycle, Mick sends the
accountants a numbered pack of supporting evidence: bank statements, broker
valuations, PayPal and credit card balances, journals and Xero prints. This
skill assembles that pack.

The pack is the last step in the year-end chain. The four conversion skills
(`natwest-to-xero`, `cc1136-to-xero`, `ii-to-xero`, `schwab-to-xero`) feed
Xero during the year-end work; this skill packages the evidence afterwards.

## Non-negotiable rules

1. **COPY, NEVER MOVE.** Every original stays exactly where it is, in its
   working folder. Mick has said this explicitly. Verify it afterwards.
2. **Propose the mapping before copying anything.** Filenames drift year to
   year. Never assume - show Mick the proposed J-number mapping and get his
   approval first. He has asked for a plan and checklist up front.
3. **Never guess between candidates.** If a J item has two or more plausible
   source files, list them all and ask. A wrong statement in the pack is
   worse than a gap.
4. **Standard footer on the checklist.** See CLAUDE.md, "Spreadsheet Print
   Footer". `(&Z&F - Printed: &D at &T)`, left section, every worksheet.
5. **ASCII only** in any file written into the vault.
6. **UK English** throughout.

## Step 0 - Date verification (MANDATORY)

Never state or write a date from memory. Run this first:

```python
from datetime import datetime, timezone, timedelta
utc_now = datetime.now(timezone.utc)
bst_active = 4 <= utc_now.month <= 10
offset = timedelta(hours=1) if bst_active else timedelta(hours=0)
london_now = utc_now.astimezone(timezone(offset))
print(london_now.strftime('%Y.%m.%d'), london_now.strftime('%A %d %B %Y %H:%M'))
```

The `YYYY.MM.DD` string is used in output filenames.

## Step 1 - Establish the year and locate the folders

Ask Mick which year end if he has not said. Then locate:

```
<BASE>\01 - Ditty Box Ltd - Xero\
    <PRIOR>\Z - For Jade_YE_<prior date>\For sending 2 Jade\   <- the template
    <CURRENT>\Z - For Jade_YE_<current date>\                  <- the destination
```

Where `<BASE>` is `C:\Users\pavey\Documents\0.2 - Areas (n)\M - Ditty Box`.

Folder naming is not perfectly consistent between years - YE 30.11.2024 sits
in `01_YE 30.11.2024` while YE 30.11.2025 sits in `001_YE 30.11.2025`. Match
on the `YE <date>` portion, not the numeric prefix.

If either folder is not reachable, request access before reporting a blocker
(see CLAUDE.md, "MANDATORY - REQUEST ACCESS BEFORE REPORTING A BLOCKER"). In
Cowork the folders must be connected at session start; if they are not, ask
Mick to add them with the "Add folder" button.

## Step 2 - Derive the manifest from last year's pack

**The prior year's `For sending 2 Jade` folder is the authoritative record of
what the accountants want.** Do not rely on the checklist spreadsheet in that
folder - historically it was only ever filled in as far as line 1.

List that folder and read the J-numbered filenames. Each one tells you the
item and the year-relative date it applies to. That derived list, not a
hardcoded one, is the manifest for this year.

`reference/manifest.md` holds the baseline J01-J25 list as at YE 30.11.2025,
with the search patterns and habitual source sub-folder for each item. Use it
to interpret what you find and to catch items the prior year missed - but the
prior-year folder wins where the two disagree.

Watch for known defects in the prior-year folder and do not reproduce them:
- YE 30.11.2024 had a file numbered `J33` that should have been `J23`.
- YE 30.11.2024 had a duplicate `J04` with a truncated filename.
- Duplicate `J08` and `J09` files with different dates in the name.

## Step 3 - Inventory this year's folder

Walk the current year folder recursively. Expect 400+ files across roughly 30
sub-folders, so do not dump the raw listing into the conversation - collect it
and work from it.

Note the year-relative dating convention, which trips people up:

- Items dated **30.11.<YE year>** are the closing position.
- Items dated **30.11.<YE year - 1>** are the opening / comparative position.
- Working files carry the date they were *produced*, often 6-8 months after
  the year end (e.g. a file named `2026.05.27 -` belongs to YE 30.11.2025).

So "the NatWest statement showing the opening balance" for YE 30.11.2025 is a
statement covering **30.11.2024**, and its filename will usually start with a
2026 production date. Match on the period covered, not the filename prefix.

## Step 4 - Propose the mapping

Present a table to Mick: J number, what the item is, the candidate source
file, and its sub-folder. Mark clearly:

- **Matched** - one confident candidate.
- **Ambiguous** - two or more candidates, list them and ask.
- **Gap** - nothing found. Say what he needs to produce.

Then confirm with him, using a question tool where available:

- Destination: a `For sending 2 Jade` sub-folder (last two years' convention)
  or straight into the `Z - For Jade` folder.
- Naming: `J<nn> - <original filename>` (the convention, and preserves
  traceability) or a cleaned description.
- Gaps: copy what exists now and list the rest, or wait for everything.
- Extras: items this year has that last year's pack did not.

Do not start copying until he has answered.

## Step 5 - Copy

Copy with metadata preserved. On the Cowork device bridge, `device_bash` can
do this directly on Mick's machine, which is far faster than staging hundreds
of megabytes through the container:

```bash
cp -p "$SRC" "$DEST/J01 - $(basename "$SRC")"
```

Note that `device_bash` cannot delete files, which is a useful safety net
here - the originals cannot be removed even by accident.

Number gaps deliberately. If J11 is outstanding, leave J11 unused rather than
renumbering everything below it - the numbering must stay stable so Mick and
the accountants can talk about "J14" across years and emails.

Put genuinely new items at the end (J24, J25...) rather than inserting them
mid-sequence.

## Step 6 - Verify

Mandatory. Report only after these pass:

```bash
# every copy matches its source byte for byte
md5sum "$COPY" "$SRC"

# originals still in place - count before and after must agree
find "$YEAR_ROOT" -type f -not -path "$DEST/*" | wc -l
```

If any copy differs, stop and investigate. Do not report success.

## Step 7 - Build the checklist

Run `scripts/build_checklist.py`, or build the equivalent with openpyxl.
Columns: Ref, Item, Status, File name in the pack, Source sub-folder, Notes.

- Green fill for copied items, amber for outstanding.
- Arial throughout, freeze panes under the header, repeating header row.
- Landscape, fit to width, standard footer on every sheet.
- COUNTIF totals at the foot - copied, outstanding, total.
- Filename: `<YYYY.MM.DD> - D.Box_YE <YE date>_Checklist for Info to
  Accountant_v.01.00.xlsx`

Save it into the `Z - For Jade_YE_<date>` folder (the parent, not the
`For sending 2 Jade` sub-folder) and also send it to Mick in the chat.

Always run the xlsx skill's `recalc.py` afterwards and confirm zero formula
errors, then re-check the footer survived the round trip:

```bash
unzip -p book.xlsx xl/worksheets/sheet1.xml | grep -o '<oddFooter>[^<]*</oddFooter>'
```

## Step 8 - Report the gaps

Finish with a short, plain list of what Mick still has to produce himself.
This is the most useful output of the whole skill - most gaps are screenshots
and Xero prints only he can make. Typical recurring gaps:

- Xero Trial Balance, P&L with codes, and Balance Sheet for the year end.
- Halifax CC-1136 opening and closing balance screenshots.
- The broker portfolio print as at the *prior* year end.

## Step 9 - Zip (only when Mick says the pack is complete)

Do not zip automatically. Wait for Mick to confirm the outstanding items are
in. Then:

```bash
cd "$DEST/.." && zip -r "D.Box_YE <date>_From Mick Pavey_<YYYY.MM.DD>.zip" "For sending 2 Jade"
```

Naming follows the prior year: `D.Box_YE 30.11.2024_From Mick Pavey_2025.06.26.zip`.
Rebuild the checklist first so it shows everything green, and include it in
the zip.

## After the run

- Append a line to `CHANGELOG.md` under `[Unreleased]`.
- Update the memory file `/areas/ditty-box-accounts.md` with the year
  completed and any manifest changes, so next year starts warm.
- If the manifest changed materially (an account opened or closed, a new
  item the accountants asked for), update `reference/manifest.md` too.

---
name: pad-slide-numbers
description: Zero-pads the trailing numbers in exported slide filenames (Slide1.PNG -> Slide01.PNG) so a folder of slides sorts in true numeric order. Auto-detects the pad width from the highest slide number, is idempotent (safe to run twice), and is collision-safe. Use this skill whenever Mick says "pad the slide numbers", "renumber the slides", "fix the slide sort order", "zero-pad the slide filenames", "the slides are out of sequence", or after exporting webinar slides to PNG. Works for any numbered file series, not just slides.
---

# Pad Slide Numbers

Zero-pad the trailing numbers in a folder of filenames so they sort in true
numeric order. Turns Slide1.PNG ... Slide9.PNG into Slide01.PNG ... Slide09.PNG
(and Slide001 ... if a deck ever tops 99) while leaving Slide10 upwards untouched.

## When to use

- After exporting webinar / presentation slides to PNG, when they come out named
  Slide1, Slide2, ... Slide52 and sort in the wrong order (Slide1, Slide10, Slide11
  before Slide2).
- Any request like: "pad the slide numbers", "renumber the slides", "fix the slide
  sort order", "the slides are out of sequence", "zero-pad the filenames".
- Works for ANY numbered file series (frames, pages, exports), not only slides.

## What it does

1. Scans the folder (non-recursive) for files whose name-stem ENDS in digits.
2. Groups them by (prefix, extension) so multiple series in one folder are handled
   independently.
3. Auto-detects the pad width from the HIGHEST number in each group:
   - up to 9 slides   -> width 1 (no change needed)
   - 10 to 99 slides  -> width 2 (Slide01 ... Slide52)
   - 100+ slides      -> width 3 (Slide001 ... Slide120)
   It never shortens a number that is already wider.
4. Renames only the files that need it. Files already padded correctly are skipped,
   so the skill is IDEMPOTENT - running it twice does nothing the second time.
5. Is COLLISION-SAFE: it renames through unique temporary names (two-phase), and if
   a target name already exists as an unrelated file it ABORTS with a clear message
   and changes nothing.
6. Reports every rename it performs.

Only the TRAILING digits of the stem are treated as the number, so a dated prefix
like "2026.07.22 - Deck - Slide1.PNG" pads only the "1".

## Instructions

### Step 1 - Confirm the target folder

Use the folder Mick names. If he just exported slides and does not give a path,
ask which folder (or use the most recent slide-export folder under his Recordings /
Projects area).

### Step 2 - Preview first (recommended)

Run a dry run so Mick can see the planned changes before anything is renamed:

```powershell
python "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\pad-slide-numbers\pad_slide_numbers.py" "<folder>" --dry-run
```

### Step 3 - Apply

```powershell
python "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\pad-slide-numbers\pad_slide_numbers.py" "<folder>"
```

Optional: restrict to a single series with `--prefix Slide` if the folder holds
more than one numbered set and only one should be padded.

### Step 4 - Confirm

Report how many files were renamed, and optionally list the folder to show the new
numeric sort order.

## Options

| Flag | Effect |
|------|--------|
| `--dry-run` | Show the planned renames, change nothing. |
| `--prefix NAME` | Only process files whose stem prefix is NAME (e.g. `Slide`). Default: every numbered series in the folder. |

## Notes and safety

- Non-recursive: it only touches files directly in the named folder, not subfolders.
- Files whose names do not end in digits (covers, notes, readme) are ignored.
- Extension case is preserved (.PNG stays .PNG).
- If it aborts on a collision, nothing has been changed - resolve the clash and re-run.

## PowerShell fallback (no Python)

If Python is unavailable, this one-liner pads single-digit Slide files (fixed
two-digit width - use the script for auto-width and safety):

```powershell
Get-ChildItem "<folder>" -Filter "Slide?.PNG" | Rename-Item -NewName { $_.Name -replace '^Slide(\d)\.PNG$','Slide0$1.PNG' }
```

## Example

```
Mick: "Pad the slide numbers in the Plaza webinar recordings folder."

Step 1: folder =
  C:\Users\pavey\Documents\0.1 - Projects (n)\2026.07.22 - Plaza Group Webinar\Recordings\2026.07.22 - P. Plaza_Webnr__v01.14_FINAL_Slide_

Step 2 (dry run): shows Slide1.PNG -> Slide01.PNG ... Slide9.PNG -> Slide09.PNG

Step 3 (apply): renames the nine single-digit files; Slide10-Slide52 unchanged.

Step 4: folder now sorts Slide01 ... Slide52 in true order.
```

## Status

- **Version:** 1.0
- **Status:** Production ready
- **Created:** 2026-07-23
- **Script:** pad_slide_numbers.py (in this skill folder; also embedded logic documented above)
- **Dual-write:** vault (`skills/pad-slide-numbers/`) + user-level
  (`C:\Users\pavey\.claude\skills\pad-slide-numbers\`) so it loads in both
  claude.ai / Desktop / Cowork (vault) and C:\Vaults-rooted Claude Code (user-level).
- **SOP index:** listed in `C:\Vaults\_SOPs\INDEX.md`.

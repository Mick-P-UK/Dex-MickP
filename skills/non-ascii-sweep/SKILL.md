---
name: non-ascii-sweep
description: >
  Scans the Dex-MickP vault for non-ASCII ("corrupt") characters and cleans them.
  Use this skill whenever Mick asks to "run the non-ascii sweep", "do the ascii
  sweep", "clean the vault", "check the vault for non-ascii", "find corrupt
  characters", "sweep for smart quotes / em dashes", "tidy the encoding", "check for
  non-ascii lurking", or any request to detect or remove non-ASCII characters across
  the vault. Runs weekly (Saturday) in SAFE mode automatically, and on demand in any
  mode. Root cause it addresses: the original DEX templates were seeded on a Mac and
  carried smart punctuation that propagates into new notes.
---

# Non-ASCII Sweep

Detects and cleans non-ASCII characters across the whole Dex-MickP vault. Built after
the 2026.07.11 full clean; turns that one-off job into a repeatable, ASCII-safe tool.

## Modes

- **scan** - report only, changes nothing. Use to see what is there first.
- **safe** (default for the weekly schedule) - auto-fix ONLY the typography corruption
  (curly quotes, em/en dashes, ellipsis, non-breaking spaces, bullets, arrows, box
  drawing). Reports any remaining MEANINGFUL non-ASCII (currency, emoji, accents) for
  Mick to review. Never transliterates aggressively unattended.
- **full** - the complete pass, on demand only, with Mick's go-ahead: everything in
  safe PLUS currency to ASCII (GBP/EUR/c), status glyphs to tags ([x], [ ], [!], ^, v),
  drop decorative emoji + ShareScope private-use glyphs + broken U+FFFD, transliterate
  accented letters to base, and re-decode wrong-encoding (cp1252) text files to UTF-8.

## How to run (on demand)

1. Find the vault mount in this session (the path changes per Cowork session):
   `ls -d /sessions/*/mnt/*/Dex-MickP` (or use the C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP
   Windows path via the file tools).
2. Run the bundled script (it auto-detects the vault root if --root is omitted):

   ```
   VAULT=$(ls -d /sessions/*/mnt/*/Dex-MickP | head -1)
   python3 "$VAULT/skills/non-ascii-sweep/scripts/ascii_sweep.py" --mode scan
   python3 "$VAULT/skills/non-ascii-sweep/scripts/ascii_sweep.py" --mode safe
   python3 "$VAULT/skills/non-ascii-sweep/scripts/ascii_sweep.py" --mode full   # only with Mick's OK
   ```

3. Relay the printed summary line to Mick. A dated markdown report is written to
   `System/Debug_Logs/YYYY.MM.DD - Non-ASCII Sweep (mode).md` unless `--no-report` is passed.

## What it excludes (deliberately)

- `.git`, `node_modules`, `__pycache__`, `.obsidian` (app config), and binary file types.
- Credential/secret files (`.pickle`, `.pem`, `.key`, etc.) are never touched.
- Files that cannot be decoded as text (corrupt binaries, Word/temp files) are listed
  in the report and left alone - they are safe to delete by hand if unwanted.

## Known-legitimate non-ASCII - do NOT flag or convert (added 2026.08.02)

Some non-ASCII is meaningful content, not corruption. When relaying a SAFE-mode
summary, do NOT raise these for review and do NOT "fix" them - they are correct:

- Pound sign (U+00A3, the GBP currency symbol) in prices - share prices, market
  caps, AISC figures, targets - throughout the research notes and the
  company-research template. Mick's standing decision (2026.08.02): leave every
  pound sign as-is. Do NOT convert it to "GBP", including in FULL mode, without a
  fresh explicit go-ahead. It is data, not corruption, and the pound sign does NOT
  cause the Obsidian/Dex UnicodeDecodeError this sweep exists to prevent (that is
  caused by cp1252 smart quotes, em/en dashes and ellipsis).
- Cent sign (U+00A2) - legitimate price data (Mick's decision 2026.08.02). Same
  treatment as the pound sign: never flag it for review, leave it as-is.
- Accented letters inside machine-generated artefacts - the three Portico mapping
  HTML snapshots (portico/mapping/*.html) and the ShareScope CSV downloads. These
  are captured web pages and raw data exports, not notes; transliterating them
  risks changing data. Leave them alone.

The real targets are unchanged: cp1252 smart quotes, em/en dashes, ellipsis,
non-breaking spaces, bullets, arrows, box-drawing, U+FFFD. Keep fixing those in
SAFE mode. (Done 2026.08.02: the script excludes pound (U+00A3) and cent (U+00A2)
from the scan/safe review tally via the REVIEW_IGNORE set, so they no longer
appear in the weekly report. Any other currency - yen, euro, rupee - is still
reported. To silence one of those too, add its code point to REVIEW_IGNORE.)

## Design notes (important)

- The script `scripts/ascii_sweep.py` is written in PURE ASCII on purpose: every special
  character is referenced by its Unicode code point via `chr(...)`. This is so the sweep
  can never corrupt its own mapping tables when it cleans the vault that contains it.
  Do NOT rewrite the maps using literal smart quotes/dashes - keep them as code points.
- SAFE mode is idempotent: running it twice changes nothing the second time.
- After a run, vault edits ride the scheduled 9pm git sweep (single private repo, SSH
  auto-push), so every change is version-controlled and reversible.

## Weekly schedule

A scheduled task runs `--mode safe` every Saturday at 10:00 London and reports. To change
cadence, update the scheduled task (see the scheduled-tasks tool) rather than editing here.

## Provenance

- Created: 2026.07.11 (Cowork), built with Mick after the full vault ASCII cleanup.
- Author: Cedric (PAIDA).
- Script: scripts/ascii_sweep.py (modes scan/safe/full; auto-detects vault root).
- Vault: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\non-ascii-sweep\SKILL.md

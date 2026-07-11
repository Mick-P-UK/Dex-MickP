---
type: pickup-note
created: 2026-05-10
revised: 2026-05-10
purpose: Hand-off for resuming after Mick's second read-through of v2 (with yellow-highlighted edits)
status: awaiting-mick-second-review
project: 2026-05-10 - Gold Miners Q1 Realised Price Story (SRB+CDE)
supersedes: prior RESUMPTION-PICKUP-NOTE.md (used in late-PM session 2026-05-10)
---

# RESUMPTION PICKUP NOTE v2 - Gold Miners Q1 YT Script (SRB+CDE)

## Where things stand

Mick has v2 of the script in DOCX form, with all v2 changes highlighted in yellow
so he can scan the diff against his v1 read-through. He's doing a second read-through.

When he comes back, the next move depends on his decision. Three plausible paths.

## Files on disk (authoritative)

**v1 markdown source:**
`C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\05-Areas\YouTube_System\diy-investors.com\YT-Longform\2026-05-10 - Gold Miners Q1 Realised Price Story (SRB+CDE)\scripts\v1-draft.md`

**v1 DOCX (Mick's print copy):**
`...\scripts\2026.05.10 - Gold_SRB_n_CDE_YT-Script_v1-draft.docx`

**v2 markdown source (newest authoritative draft):**
`...\scripts\v2-draft.md`

**v2 DOCX (suggested filename when Mick saves):**
`...\scripts\2026.05.10 - Gold_SRB_n_CDE_YT-Script_v2-draft.docx`

**Project root:**
`C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\05-Areas\YouTube_System\diy-investors.com\YT-Longform\2026-05-10 - Gold Miners Q1 Realised Price Story (SRB+CDE)\`

**Voice DNA reference (re-read if drafting v3 from scratch):**
`C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\05-Areas\Writing_System\context\core\voice-dna-mick.json`

## What changed in v2 (yellow highlights in the DOCX)

1. Section 4: COMEX silver inventory line added after the ETF buying point. Verified
   across multiple sources (Coinweek, Sorafutures, ZeroHedge): registered stocks below
   100m oz threshold since Feb 2026.
2. Section 5: GUIA expanded to "Brazilian environmental installation licence"
3. Section 5: INCRA expanded to "National Institute for Colonisation and Agrarian Reform"
4. Section 5: FUNAI expanded to "National Foundation for Indigenous Peoples"
5. Section 6: copper figure (50-65m lbs) verified across SIX independent sources, KEPT.
6. Section 6: "New Afton is a copper-gold mine" clarifier added in [ASIDE] brackets per
   Mick's request, so he can read it as a camera aside.

Word count v2: 2,065 spoken (~14.8 min at 140 wpm). v1 was 2,004; v2 added ~60 words.

## Three resumption paths

### Path A: SHIP IT
Mick is happy with v2 and just needs the title locked.

**Trigger phrase:** *"Cedric, ship the gold miners script. Title [N], no further changes."*

**Action:**
1. Update v2 frontmatter status from "v2-draft" to "v1-final" (v1 in the
   product-versioning sense, not the iteration sense)
2. Apply chosen title throughout: working title at top of script, frontmatter, and the
   final-DOCX header/footer
3. Regenerate DOCX **WITHOUT** the yellow highlights (clean ship-ready version).
   Use the v1 build script as the template. Filename suggestion to Mick:
   `2026.05.10 - Gold_SRB_n_CDE_YT-Script_FINAL.docx`
4. Update Notion Micks Content Studio entry from "In Review" to "Ready":
   `Notion:notion-update-page` on entry id `35cdb32a-9b0a-8127-b9e9-ed66cb9b2c33`
5. Add v2-final filename and YouTube target publish date to Notion Notes field
6. Resolve charts handoff for editor (see below)
7. Optionally: write PROJECT.md to project root summarising the whole pipeline

### Path B: MORE EDITS (v3)
Mick has more changes. Apply them and produce v3.

**Trigger phrase:** *"Cedric, more edits on the gold miners script..."*

**Action:**
1. Take edits verbally or from a marked-up DOCX
2. If marked-up DOCX: read it from the scripts folder using the docx skill
   (`/mnt/skills/public/docx/SKILL.md` - extract-text or pandoc --track-changes=all)
3. Read v2-draft.md fresh, apply edits in memory, write v3-draft.md
4. Regenerate change-highlighted DOCX (highlights show v3 changes vs v2 - reset highlights
   from v2; only flag what's NEW in v3)
5. Apply the highlightCs strip post-process before delivery (see Key Conventions in
   CEDRIC_MEMORY)
6. QA: ASCII + word count + voice-guard checks in Python

### Path C: STRUCTURAL REWRITE
Mick wants a substantial restructure (e.g. trim to 10 mins, drop a section, swap stocks).

**Trigger phrase:** *"Cedric, the script needs a bigger rework..."*

**Action:**
1. Discuss the change scope before drafting
2. Re-read voice-dna-mick.json end-to-end before writing
3. Draft v3 from v2 source, mark changes with yellow highlights in DOCX
4. May need to revisit the chart references if the structure shifts significantly

## Charts handoff (still outstanding)

Both JPGs were uploaded by Mick at the very start of the morning session. They live at
`/mnt/user-data/uploads/` in that originating session's container, which may not be
accessible from a fresh session.

**For the editor's working files**, copies should sit alongside the script in the project
folder. Either Mick re-uploads them at v3/final stage, or Cedric copies them into a
`charts/` subfolder under the project root. Worth raising as a checklist item before recording.

## Voice DNA sanity check (apply to any v3 edits)

If editing prose, keep the 12 patterns intact:
1. Personal attribution / journey framing
2. Humility markers ("To me", "As far as I'm concerned", "In my opinion")
3. DIY-Investors capitalised
4. Conversational transitions ("OK, let me bring this all together", "To be honest with you")
5. Softer technical language ("reveals", "suggests")
6. Hedging on predictions, conviction on principles
7. AI assistants named (Cedric and Annie) - light mention only
8. British English (whilst, colour, realise)
9. Data first, interpretation second
10. Temporal precision ("at the time of writing", specific dates)
11. Self-aware concept references (kept light)
12. Full DYOR closing with date

## Standard QA after writing v3

```python
import re
with open('/path/to/v3-draft.md', encoding='utf-8') as f: c = f.read()

# ASCII check
non_ascii = [(i, hex(ord(ch))) for i, ch in enumerate(c) if ord(ch) > 127]
print('ASCII PASS' if not non_ascii else f'FAIL: {len(non_ascii)} non-ASCII')

# Word count (spoken portion only)
spoken = re.sub(r'^---\n.*?\n---\n', '', c, count=1, flags=re.DOTALL)
spoken = re.sub(r'^#+ .*$|\[.*?\]|^---$|\*\*.*?\*\*', '', spoken, flags=re.MULTILINE|re.DOTALL)
words = len(spoken.split())
print(f'{words} words = {words/140:.1f} min at 140 wpm')

# Voice guard
banned = ["let's crush", "to the moon", "game-changer", "absolutely", "10x"]
for b in banned:
    if b.lower() in c.lower(): print(f'BANNED PHRASE FOUND: {b}')
```

## DOCX regeneration recipe (v1 build script preserved at /home/claude/build_script_docx.js)

For SHIP-clean DOCX (Path A):
- A4, Arial 12pt body, 1.5x line spacing
- H1 bold black 16pt; H2 bold DIY blue (#1F4E79) 13pt
- Stage directions italic grey
- Section divider rules between blocks
- Header right-aligned with FINAL title; footer Page X of Y + name + date
- NO yellow highlights anywhere (this is the camera-ready script)

For change-highlighted DOCX (Path B):
- Same recipe + `highlight: "yellow"` on TextRuns marking v3 changes vs v2
- After build, post-process zip to regex-strip `<w:highlightCs[^/]*/>` for validator

REMEMBER: Filesystem MCP write_file is text-only. Binary DOCX must come through
outputs/present_files. Mick saves to vault under his own filename
(YYYY.MM.DD - Title format).

## Notion entry status

- Entry id: `35cdb32a-9b0a-8127-b9e9-ed66cb9b2c33`
- Database: Micks Content Studio (`a1983c632eb84e15b365a6e3e310ff96`)
- Current status: "In Review"
- URL: https://www.notion.so/35cdb32a9b0a8127b9e9ed66cb9b2c33
- Move to "Ready" only when v2-final or v3-final is signed off

## Trigger phrases reference (for fast routing)

- *"Cedric, ship the gold miners script. Title [N]..."* -> Path A
- *"Cedric, more edits on the gold miners script..."* -> Path B
- *"Cedric, the script needs a bigger rework..."* -> Path C

## End of resumption pickup note

Cedric, when Mick comes back: greet him with current London time, confirm environment
(Filesystem MCP probe), and route to A/B/C based on what he says.

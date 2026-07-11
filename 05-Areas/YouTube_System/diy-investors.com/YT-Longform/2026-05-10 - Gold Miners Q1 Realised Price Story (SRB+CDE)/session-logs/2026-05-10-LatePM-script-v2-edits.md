---
type: session-log
date: 2026-05-10
session: Late-PM (script v2 edits)
project: 2026-05-10 - Gold Miners Q1 Realised Price Story (SRB+CDE)
status: v2-complete-awaiting-second-review
---

# Session Log: 2026-05-10 Late-PM - Script v2 Edits

## Time
~16:25 to ~17:00 BST, Sunday 10 May 2026.

## Environment
Claude Desktop. Filesystem MCP confirmed (carried over from earlier sessions).

## Objective
Pick up cleanly from RESUMPTION-PICKUP-NOTE.md (Path A: verbal edits from Mick).
Apply five edits to v1, fact-check the queries, generate v2 markdown + change-highlighted DOCX.

## What was done

### 1. Resumption and edit intake
Mick provided five edits verbally:
1. Section 4: add line about COMEX inventory drop after the ETF buying point
2. Section 5: expand GUIA acronym
3. Section 5: expand INCRA acronym
4. Section 5: expand FUNAI acronym
5. Section 6: sanity check the copper guidance figure ("seems like an awful lot of copper relative to the ounces of silver and gold")

Edits 1-4 are mechanical; edit 5 was a fact-check request.

### 2. Fact-checks performed
**Copper figure (50-65m lbs):** verified across SIX independent sources:
- Coeur Mining press release (March 2026)
- MINING.com (23 March 2026)
- SME Mining Engineering (25 March 2026)
- Investing.com (23 March 2026)
- Mugglehead Investment Magazine (24 March 2026)
- Resource World Magazine (24 March 2026)

All confirm: 50 to 65 million pounds of copper for 2026 (9 months contribution).
New Afton in BC contributes ALL the copper output and is fundamentally a copper-gold mine
rather than a precious metals operation. Life-of-mine reserves at New Afton: 591 million
pounds of copper alongside gold and silver. The figure is correct.

**COMEX silver inventory claim:** verified registered stocks below 100m oz threshold
since February 2026 (Coinweek 13 February 2026 - dropped to 98.1m oz; Sorafutures
April 2026 - 76.88m oz; ZeroHedge 1 May 2026 - drawdown continuing). Edit on safe ground.

### 3. Unit-confusion gaffe (CRITICAL LESSON)
While explaining why the copper figure "looks big" relative to silver, Cedric stated:
"copper is measured in pounds (a much smaller unit than ounces)."

THIS IS WRONG. There are 16 ounces in 1 pound. A pound is LARGER than an ounce.
Mick caught it immediately: "When I went to School, there were 16oz to 1 pound -
so ounces are smaller than pounds!"

Cedric apologised and reasoned through it properly:
- 50-65m lbs of copper = ~800m-1bn avoirdupois ounces equivalent (genuinely large by weight)
- BUT this is correct because New Afton is a copper-gold mine
- By DOLLAR VALUE the mix is balanced: gold ~$3.6bn, silver ~$1.6bn, copper ~$0.26bn
  at current prices. Copper is the SMALLEST revenue stream despite being largest by weight.

**Pattern logged to CEDRIC_MEMORY Key Conventions:** when cross-source verification confirms
a figure, STOP THERE. Do not add hand-wavy unit-conversion reasoning post-hoc. The cross-
source check is the verification, not the unit comparison.

### 4. Copper clarifier decision
After the unit-confusion exchange, Mick agreed his concern was valid (the figure does look
big at first glance) and chose Option A: keep the figure, add a one-sentence "New Afton
is fundamentally a copper-gold mine" clarifier as a side-note in [ASIDE] brackets, so he
can read it as a camera aside.

### 5. v2 markdown written
Single Filesystem write to `scripts/v2-draft.md` with:
- Frontmatter version-bumped to v2-draft, revised date added, v2_changes list logged
- Stage direction header expanded to flag [ASIDE] convention
- All five edits applied in their respective sections
- ASCII-only throughout

### 6. Post-write QA validation
- ASCII compliance: PASS (zero non-ASCII chars)
- Voice guard: PASS (no banned phrases)
- Word count: 2,065 spoken (~14.8 min at 140 wpm), up ~60 from v1 due to acronym expansions
- All 6 edit checks: PASS
  - COMEX line present
  - GUIA expansion present
  - INCRA expansion present
  - FUNAI expansion present
  - Copper figure preserved
  - New Afton aside present

### 7. v2 DOCX built with change highlighting
Used docx-js with `highlight: "yellow"` on TextRun to mark v2 changes vs v1.
Recipe carried over from v1 (A4, Arial 12pt, 1.5x spacing, blue H2, dividers, headers/footers).
Header updated to "YT Script v2"; footer suffixed with "v2".

**docx-js validator quirk discovered and fixed:**
The validator flagged `<w:highlightCs/>` as an unexpected element. docx-js emits this
alongside `<w:highlight/>` for theming, but strict OOXML schema only accepts the latter.
Word opens both fine but validator blocks. Fix: post-process the .docx zip with Python,
regex-strip all `<w:highlightCs[^/]*/>` elements, repackage. Validator PASS after fix.

This pattern is now logged in Key Conventions in CEDRIC_MEMORY.

### 8. Delivery
- v2 DOCX staged to /mnt/user-data/outputs/v2-draft.docx
- Suggested filename for vault save: `2026.05.10 - Gold_SRB_n_CDE_YT-Script_v2-draft.docx`
- Markdown source already at `scripts/v2-draft.md`
- v1 files preserved alongside (no deletion)

## Key decisions taken

1. **Copper figure stays** - verified across 6 independent sources.
2. **Aside device** - [ASIDE] brackets used for camera-cue commentary, distinct from [stage directions].
3. **Yellow highlights in DOCX** - keeps the "what changed" obvious for second read-through.
4. **No further trim of length** - v2 is ~14.8 min, slightly longer than v1 due to expansions, but Mick already chose depth-over-compression in PM session.

## Patterns / lessons logged to CEDRIC_MEMORY

1. **NEVER add hand-wavy unit-conversion reasoning to verified figures.** Cross-source check
   IS the verification. Lesson came from the "pounds smaller than ounces" gaffe.

2. **DOCX change-highlighting recipe** with the highlightCs strip post-process, for any
   future v2/v3 deliverables where Mick needs to see what changed.

3. **Verbal-edit pickup pattern (Path A from RESUMPTION-PICKUP-NOTE)** worked cleanly. Read
   v1 source, apply edits in memory, write v2, regenerate highlighted DOCX, present.

4. **Side-note aside device:** [ASIDE - text] brackets for on-camera commentary cues distinct
   from production stage directions. Worth considering as a voice-DNA pattern if Mick uses
   it again.

## Outstanding for next session

1. Mick's second read-through of v2 DOCX (yellow highlights make changes scannable)
2. Decision: ship as v1-final, or v3 with more edits
3. Title locked from the four options
4. If shipping:
   - Regenerate clean DOCX without highlights (v1-final equivalent)
   - Update Notion entry 35cdb32a-9b0a-8127-b9e9-ed66cb9b2c33 from "In Review" to "Ready"
   - Charts handoff to editor (still unresolved - JPGs at /mnt/user-data/uploads/ in
     originating session, may need re-uploading or copying into project folder for permanence)

See updated `RESUMPTION-PICKUP-NOTE.md` for the full handoff.

## End of session log

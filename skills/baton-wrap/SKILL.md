---
name: baton-wrap
description: >-
  End-of-thread handover wrap. Secures everything before context is lost so the
  next thread starts cold with full continuity. Its hero deliverable is the
  handover note. Use whenever Mick says "baton", "baton wrap", "wrap the thread",
  "pass the baton", or "hand over", and typically just before he refreshes or
  starts a fresh thread. Cedric also nudges Mick to run it when the context is
  judged to be filling (around 70 percent). This is the thread-level wrap; for
  the daily consolidation use sundown-wrap instead.
license: Proprietary - Mick Pavey / DIY Investors internal use.
---

# baton-wrap

## Purpose

A relay handover. baton-wrap runs at the end of a working thread, or just before
the context is refreshed, and secures the session so the next thread can pick up
cold. The whole reason it exists is continuity: the next thread has no memory of
this one, so the handover note is the baton being passed. Fast and near-silent by
design.

Scope for now: Cowork and Claude Code only (both are vault-aware surfaces). Mobile
and claude.ai web are out of scope until MCSB Phase 1.5 gives them vault access.

## When to use

Manual triggers: "baton", "baton wrap", "wrap the thread", "pass the baton",
"hand over".

Proactive nudge: Cedric watches the thread and, when he judges the context is
approaching roughly 70 percent full (from thread length, volume of tool output,
and large file reads), nudges Mick with a one-liner suggesting a baton-wrap and
refresh. There is no exact context gauge to read, so Cedric estimates and errs
slightly early - a premature baton costs nothing, a late one loses work.

## Procedure

### 1. Verify the date and time (London)

Never guess. Run:

    from datetime import datetime, timezone, timedelta
    utc_now = datetime.now(timezone.utc)
    bst_active = 4 <= utc_now.month <= 10
    offset = timedelta(hours=1) if bst_active else timedelta(hours=0)
    london_now = utc_now.astimezone(timezone(offset))

Use london_now for the note date, the archive timestamp, and the changelog lines.

### 2. Scan the thread

Review the session and distil:
- The topic: a short, consistent name for what this thread was about. This is
  derived once here and reused everywhere - the archive filename, the note title,
  the Content Studio entry, and an Obsidian `[[topic]]` wikilink in the handover
  note. Reuse the exact same topic string across successive threads on the same
  subject so the notes link together in the Obsidian graph.
- Decisions made.
- Files created, updated, or deleted (with paths).
- Open questions and anything left unfinished.
- The next-thread pickup phrase and the first action for next time.

### 3. Flush memory

Update CEDRIC_MEMORY.md and the auto-memory index with only durable facts and
decisions - things that matter beyond this thread. Do not record ephemeral chatter.
Convert any relative dates to absolute. ASCII only.

PLACEMENT (critical). CEDRIC_MEMORY.md is read top-down at session start, so the newest
material MUST go at the TOP and never be appended at the bottom:
1. Prepend a new one-line "**Last Updated:** YYYY.MM.DD (day, surface, part-of-day) -
   <summary>" entry to the Last Updated stack directly under the "# CEDRIC MEMORY"
   heading, above the previous newest line.
2. Prepend a new "## Recent session: YYYY.MM.DD (weekday, surface, part-of-day) -
   <topic>" block immediately after the first "---" divider, above the previous newest
   Recent session block.
After writing, the top Last Updated line and the first Recent session block must both be
today's. Never append to the end of the file (that orphans the entry where session-start
does not see it).

### 4. Append the changelog

Append one line per create/update/delete to `_changelog/YYYY-MM.log` in the house
format:

    YYYY-MM-DD HH:MM [ACTION] path - description. Author: Cedric. Status: ...

ACTION is CREATE, UPDATE, or DELETE. One line per file touched this thread.

### 5. Write the handover note

Write to two places:
- `_handovers/LATEST.md` - overwrite every time. This is the single predictable
  place the next thread looks.
- `_handovers/archive/YYYY.MM.DD - HHMM - baton - <topic>.md` - a timestamped
  archive copy (HHMM is 24-hour London time, no colon). Several baton-wraps a day
  each leave their own archived copy.

ASCII only. UK English. Use the template in the Appendix.

### 6. Content Studio check (silent)

If anything content-worthy happened (a Meet Cedric episode developed, a script or
title created, a brain dump captured, etc.), log it silently to the Micks Content
Studio Notion database. Title `YYYY.MM.DD - <descriptive title>`. Include the
topic (from step 2) so the Content Studio entry ties back to the handover note and
its `[[topic]]` links. Set Project, Audience, Format, Status. A Meet Cedric item is
logged here too, with Project = Meet Cedric - it is the same database, the Project
field distinguishes it. No announcement, no asking. If nothing content-worthy
happened, skip silently.

### 7. Deliverables

Move any final outputs produced this thread to the outputs folder and surface them
with present_files. (This is the per-thread delivery step; it is separate from the
handover note, which lives in the vault.)

### 8. Git commit and push

Back up the vault:
1. Clear a stale `.git/index.lock` if one is present.
2. Stage the changed files.
3. Commit (the ASCII pre-commit hook must pass - steps 3 and 5 already enforce
   ASCII, so this should be clean).
4. Push to the configured remote.

Note: push currently goes to the local remote, so it versions and de-risks the
working copy but is not yet off-device backup. Off-device (GitHub) is a separate
decision, out of scope for baton-wrap.

### 9. Confirm (one line)

Report in a single line: what was saved plus the safe-to-refresh signal and the
opener for the next thread. Example:

    Baton passed. Safe to refresh now. New thread opener: "Cedric, resume from LATEST handover."

Do not show Mick the handover note. Do not narrate the steps.

## What baton-wrap does NOT do

- It does not roll up the whole day (that is sundown-wrap).
- It does not verify that scheduled jobs ran.
- It does not do calendar look-ahead.
- It does not ask questions or seek approval - it acts and confirms in one line.

## Guardrails

- ASCII only for all vault writes: no em dashes, smart quotes, or ellipsis.
- UK English throughout (organise, colour, behaviour).
- Verify date/time with code, never mental arithmetic.
- File naming: YYYY.MM.DD for dates, dots as separators, date first.

## Appendix: handover note template

    ---
    title: Baton Handover -- <topic>
    date: YYYY-MM-DD
    time: HH:MM (London)
    topic: <topic>
    thread: <short description>
    status: handover
    author: Cedric (PAIDA)
    generated-by: AI
    ---

    # Baton Handover -- <topic> (YYYY-MM-DD HHMM)

    Topic: [[<topic>]]

    ## Thread character
    One or two lines: what this thread was for.

    ## Decisions made
    - ...

    ## Files changed this thread
    - [CREATE/UPDATE/DELETE] path - one line why.

    ## Open questions / unfinished
    - ...

    ## Next-thread pickup
    - Opener phrase: "..."
    - First action: ...

    ## Content Studio logged
    - Item title and Project, or "none".

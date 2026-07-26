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
version: 2.0 (2026.07.26 - bulletproofing spec applied; see _handovers/2026.07.25 - Baton-Wrap Post-Mortem and Bulletproofing Spec.md)
---

# baton-wrap

## Purpose

A relay handover. baton-wrap runs at the end of a working thread, or just before
the context is refreshed, and secures the session so the next thread can pick up
cold. The whole reason it exists is continuity: the next thread has no memory of
this one, so the handover note is the baton being passed. Fast and near-silent by
design.

Scope: ALL surfaces. Claude Code and Cowork (cloud or desktop) write the vault
directly; claude.ai web has no vault access and uses the degraded-mode route in
"Surface routing" below. The baton must NEVER exist only in ephemeral memory.

## Registry independence (do not skip)

The vault copy of this file - skills/baton-wrap/SKILL.md - is the single source
of truth. The Cowork/web skill registry is only a convenience trigger, NEVER a
precondition. If a wrap is requested and the Skill tool does not list baton-wrap,
READ this file from the vault and EXECUTE it anyway. A missing registry entry is
not a reason to fall back to an ad-hoc pickup note (that is exactly how the
2026-07-25 relay break happened).

## Surface routing

One canonical read target for every session-start: `_handovers/LATEST.md`.
Delivery is routed by surface:

- **Claude Code** (vault + git): write archive copy, then LATEST.md, verify,
  then git commit/push. The full procedure below.
- **Cowork, cloud or desktop** (vault via Filesystem/device bridge; ephemeral
  sandbox): write the SAME vault files via the bridge, BEFORE the session ends -
  anything held only in the sandbox dies with it. Also deliver the baton note to
  Mick as a file (SendUserFile) so an out-of-vault copy exists regardless of
  sandbox lifetime. Git: commit via the device VM if the C:\Vaults mount is
  available (use `git -c core.autocrlf=true` - the mount shows CRLF/LF phantom
  diffs otherwise, and move any leftover .git/*.lock files to _to_delete/ since
  the mount cannot delete); push is not possible from the VM (no SSH route), it
  rides the next daily-commit run.
- **claude.ai web** (no vault): degraded mode. Output the full baton note
  in-chat AND email it to Mick as a self-note with the fixed subject tag
  `[BATON-ORPHAN] YYYY.MM.DD - <topic>`. The next vault-aware session promotes
  it into LATEST.md (see "Promote latest" below).

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

### 5. Write the handover note - ARCHIVE FIRST, VERIFY AFTER

Strict ordering. Never overwrite LATEST.md in a run that has not already written
its archive copy - archive-first guarantees that even a half-finished wrap leaves
a durable dated copy.

1. Write `_handovers/archive/YYYY.MM.DD - HHMM - baton - <topic>.md` (HHMM is
   24-hour London time, no colon). Several baton-wraps a day each leave their
   own archived copy.
2. Overwrite `_handovers/LATEST.md` - the single predictable place the next
   thread looks.
3. FRESHNESS GUARD (mandatory): RE-READ LATEST.md and assert its frontmatter
   date and time equal the london_now computed in step 1. If they do not match,
   the write did not land - raise it LOUDLY to Mick and do NOT report success.
   A stale baton is byte-indistinguishable from a fresh one; this check is the
   only thing that makes a broken relay visible at wrap time.

ASCII only. UK English. Use the template in the Appendix - including the
mandatory `surface:` and `working_dir:` frontmatter stamp, which records what
the authoring session could and could not do (git? vault bridge? sandbox?).

On claude.ai web, replace this whole step with the degraded-mode route in
"Surface routing".

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
handover note, which lives in the vault.) On Cowork, additionally send the baton
note itself to Mick as a file per "Surface routing".

### 8. Git commit and push

Back up the vault, per the surface routing above:
1. Clear a stale `.git/index.lock` if one is present (on the Cowork VM mount,
   MOVE it to _to_delete/ - the mount cannot delete files).
2. Stage the changed files (on the VM mount, always `-c core.autocrlf=true`).
3. Commit (the ASCII pre-commit hook must pass - steps 3 and 5 already enforce
   ASCII, so this should be clean).
4. Push to the configured remote (Claude Code only; from the Cowork VM there is
   no SSH route, so note in the confirm line that the push rides the next
   daily-commit run).

### 9. Confirm (one line)

Report in a single line: what was saved plus the safe-to-refresh signal and the
opener for the next thread. Example:

    Baton passed. Safe to refresh now. New thread opener: "Cedric, resume from LATEST handover."

Do not show Mick the handover note. Do not narrate the steps. If the freshness
guard failed, this line is replaced by the loud failure report - never confirm a
wrap that did not verify.

## Session-start staleness check (read side of the contract)

Any session that opens with "resume from LATEST handover" (or reads LATEST.md as
part of session start) must check LATEST.md's frontmatter date and flag a visible
"STALE HANDOVER" warning to Mick, before greeting pleasantries, if LATEST.md is:
(a) older than expected when a wrap was known to have happened,
(b) older than the newest file in `_handovers/archive/`, OR
(c) older than the newest project `PICKUP_POINT_*` file or `[BATON-ORPHAN]`
    email in Gmail.
Silent staleness is the failure mode that broke the relay on 2026-07-25; this
check turns it into a banner.

## Promote latest (reconciler)

When the staleness check fires, or on request ("promote latest"), any vault-aware
session runs this: scan the newest handover evidence across (i) `_handovers/archive/`,
(ii) project `PICKUP_POINT_*` files, and (iii) `[BATON-ORPHAN]` emails in Gmail.
If the newest is newer than LATEST.md, rebuild LATEST.md from it - archive-first,
verify-after, exactly as in step 5. Take a byte-perfect backup of the current
LATEST.md into `_handovers/_backups/` before overwriting.

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
- The baton must never exist only in ephemeral memory - vault write (or orphan
  email on web) comes before anything else can end the session.
- Mick must upload any amended SKILL.md to Cowork + web via Settings >
  Capabilities - Cedric cannot write those stores; the vault copy alone does not
  make the change live on the weaker surfaces.

## Appendix: handover note template

    ---
    title: Baton Handover -- <topic>
    date: YYYY-MM-DD
    time: HH:MM (London, BST/GMT, verified via code)
    topic: <topic>
    surface: <Claude Code | Cowork-cloud | Cowork-desktop | web>
    working_dir: <working directory / bridge routes available to this session>
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

---
name: sundown-wrap
description: >-
  End-of-day consolidation wrap. Closes the whole day into one dated rollup note,
  verifies the scheduled jobs actually ran, sweeps Content Studio, flushes memory,
  looks ahead to tomorrow via Annie, and does a final git commit. Its hero
  deliverable is the daily Sundown note. Use whenever Mick says "sundown", "wrap
  the day", "close out the day", "end of day wrap", "run sundown", "day wrap", or
  "put the day to bed", typically once when the day is done. Cedric may also nudge
  after about 18:00 London if the day had activity but no Sundown note yet. This is
  the day-level wrap and it consumes the per-thread baton-wrap handovers; for a
  single-thread handover before a refresh use baton-wrap instead.
license: Proprietary - Mick Pavey / DIY Investors internal use.
---

# sundown-wrap

## Purpose

The end-of-day close. Where baton-wrap hands one thread to the next, sundown-wrap
closes the whole day: one dated rollup note tying the day's separate threads
together, a check that the scheduled jobs fired, a memory flush, and a look at
tomorrow. Run it once, when the day is actually done.

Scope for now: Cowork and Claude Code only (both are vault-aware surfaces). Mobile
and claude.ai web are out of scope until MCSB Phase 1.5 gives them vault access.

## Relationship to baton-wrap

Do not duplicate baton-wrap. baton-wrap writes a per-thread handover to
`_handovers/archive/` every time a thread is wrapped. sundown-wrap CONSUMES those
notes. Its unique value is the three things baton-wrap never does: the cross-thread
rollup, the "did the robots run" check, and the tomorrow look-ahead. If a thread
today never got a baton, sundown-wrap catches it from the session transcripts
(where reachable) so nothing falls through.

## When to use

Manual triggers: "sundown", "wrap the day", "close out the day", "end of day wrap",
"run sundown", "day wrap", "put the day to bed".

Proactive nudge: after roughly 18:00 London, if the day had activity (a thread
wrapped, files changed, jobs ran) but no `_daily/YYYY.MM.DD - Sundown.md` exists
yet, Cedric may offer a one-line nudge: "Want me to run sundown for today?" The
nudge asks, it does not act. Do not nudge on a genuinely quiet day with nothing to
consolidate.

## Procedure

### 0. Vault access (ask first, skip-with-note is plan B)

The full run needs the vault ROOT reachable: the git repo (`.git`),
`CEDRIC_MEMORY.md` and the skills folder all sit at the vault root, above any Cowork
subfolder mount.

1. Detect reachability. In bash, test whether the repo root is a git work tree and
   whether `CEDRIC_MEMORY.md` is readable.
2. If NOT reachable (typical Cowork subfolder mount): ASK for vault-root access first
   via request_cowork_directory, pointing at the vault root, so git and memory can
   complete.
3. If access is granted: full run, all steps complete.
4. If access is declined (or a headless scheduled context where asking is not
   possible): fall back to SKIP-WITH-NOTE mode. Do every reachable step, and for each
   step that is not, write a clear deferred line into the daily note, e.g. "git
   commit deferred - vault root not mounted, run from Claude Code". Never hard-fail.

Skip-with-note is the safe default, not a failure. The day still gets a note.

### 1. Verify the date and time (London)

Never guess. Run:

    from datetime import datetime, timezone, timedelta
    utc_now = datetime.now(timezone.utc)
    bst_active = 4 <= utc_now.month <= 10
    offset = timedelta(hours=1) if bst_active else timedelta(hours=0)
    london_now = utc_now.astimezone(timezone(offset))

Use london_now for the note filename, the note title, and the changelog lines.

### 2. Gather the day's activity

- Read `_handovers/archive/` for today's baton notes (files starting today's
  YYYY.MM.DD). These are the day's threads.
- Read today's `_changelog/YYYY-MM.log` lines for creates, updates and deletes.
- Where session transcripts are reachable, scan the day's sessions to catch any
  thread that was never batoned. Summarise, do not transcribe.

### 3. Verify the scheduled jobs ran

The authoritative source is the SCHEDULER, not the changelog. Call
list_scheduled_tasks and compare each enabled task's lastRunAt to today's London
date. A task whose lastRunAt is not today has not run today. Do not infer job status
from the changelog - several jobs (the morning briefing, the gmail sweep) write to
the vault inbox or send email and never touch the changelog.

Known daily jobs (as of this writing - always trust the live list over this note):
- gmail-self-notes-sweep (06:24 daily) - self-emailed notes to the vault inbox.
- morning-daily-briefing (06:50 daily).
- uk-portfolios-daily / us-portfolios-daily (weekdays only - n/a at weekends).

Also check the manual weekly job that has no scheduler entry:
- yt-weekly-stats (run manually on Saturdays) - flag on a Saturday if no new stats
  row was logged.

Under "Jobs check" in the daily note, list each relevant job as ran / NOT RUN / n/a
with its last-run time. Flag anything that should have run but did not, so Mick can
act. Do not silently pass a missing job.

### 4. Write the daily rollup note

Write the canonical daily note to the dedicated daily folder:

    _daily/YYYY.MM.DD - Sundown.md

This canonical name is the single predictable place Mick finds today's Sundown -
one per day, no timestamp clutter. Same-day rerun safety (mirrors baton-wrap's
LATEST-plus-archive pattern): if a Sundown note ALREADY exists for today, first move
the existing one to a timestamped archive copy

    _daily/archive/YYYY.MM.DD - HHMM - sundown.md

(HHMM is the existing note's run time, 24-hour London, no colon) BEFORE writing the
fresh canonical note. Nothing is ever overwritten and lost; the canonical note stays
current. Test runs must use a distinct "(DRY RUN)" suffix and stay out of _daily so
they never collide with a real note.

ASCII only, UK English. Use the template in the Appendix. The `_daily/` folder holds
both Mick's own `YYYY.MM.DD - Journal.md` notes and Cedric's Sundown notes; they
share the date prefix so they sort together and the suffix keeps them distinct.
Never overwrite a Journal note. The Sundown note links to that day's Journal note if
one exists.

### 5. Content Studio check (silent)

If anything content-worthy happened today, log it silently to the Micks Content
Studio Notion database (collection cba41a78-6544-4f66-915d-18fc6a0bd933). Title
`YYYY.MM.DD - <descriptive title>`. Set Project, Audience, Format, Status. A Meet
Cedric item is logged here too via Project = Meet Cedric. No announcement, no asking.
If nothing content-worthy happened, skip silently.

### 6. Calendar look-ahead via Annie

Use the Annie sub-agent for tomorrow's schedule (read Annie's SKILL.md first, per the
standing rule that Annie handles any calendar or date request). Pull tomorrow's
events and fold them into the "Tomorrow" section of the daily note. Never do the date
maths yourself - Annie verifies dates.

### 7. Flush memory

If reachable, update `CEDRIC_MEMORY.md` and the auto-memory index with only the day's
durable facts and decisions - things that matter beyond today. Convert relative dates
to absolute. ASCII only. If `CEDRIC_MEMORY.md` is not reachable (subfolder mount),
update auto-memory only and record the deferral in the daily note per step 0.

PLACEMENT (critical). CEDRIC_MEMORY.md is read top-down at session start, so the newest
material MUST go at the TOP and never be appended at the bottom: prepend a new
"**Last Updated:** YYYY.MM.DD ..." line to the stack directly under the "# CEDRIC MEMORY"
heading, and prepend a new "## Recent session: YYYY.MM.DD ..." block immediately after
the first "---" divider. After writing, the top Last Updated line and the first Recent
session block must both be today's. Never append to the end of the file (that orphans the
entry where session-start does not see it).

### 8. Append the changelog

Append one line per create/update/delete to `_changelog/YYYY-MM.log` in the house
format:

    YYYY-MM-DD HH:MM [ACTION] path - description. Author: Cedric. Status: ...

At minimum: the Sundown note create and any Content Studio create.

### 9. Git commit and push

Back up the vault (only if the repo root is reachable):
1. Clear a stale `.git/index.lock` if one is present (only when no git process is
   running).
2. Stage the changed files.
3. Commit (the ASCII pre-commit hook must pass - steps 4, 7 and 8 already enforce
   ASCII, so this should be clean). Message e.g. "sundown YYYY.MM.DD - daily rollup".
4. Push to the configured remote (currently local - not yet off-device backup).

If the repo is not reachable, record "git deferred" in the daily note and move on.

### 10. Confirm (one line)

Report in a single line - never the note itself, never narrate the steps:

    Day wrapped - N threads, M files, jobs [ok / flags]. Tomorrow: <first thing>. Note: _daily/YYYY.MM.DD - Sundown.md

If anything was deferred, append a short tail, e.g. "(git + memory deferred - run
from Claude Code)".

## What sundown-wrap does NOT do

- It does not write per-thread handovers (that is baton-wrap) - it consumes them.
- It does not run the scheduled jobs; it only verifies they ran and flags misses.
- It does not seek approval mid-run - it acts, defers gracefully, and confirms in
  one line. (The only ask is the step 0 vault-access request when the root is not
  mounted.)

## Guardrails

- ASCII only for all vault writes: no em dashes, smart quotes, or ellipsis.
- UK English throughout (organise, colour, behaviour).
- Verify date/time with code, never mental arithmetic.
- File naming: YYYY.MM.DD for dates, dots as separators, date first.
- Run once per day. The canonical note is YYYY.MM.DD - Sundown.md; a same-day rerun
  archives the previous copy to _daily/archive/ (see step 4) rather than duplicating
  in place. Test runs use a "(DRY RUN)" suffix and never write to _daily.

## Appendix: Sundown note template

    ---
    title: Sundown -- YYYY.MM.DD
    date: YYYY-MM-DD
    day: <weekday>
    type: sundown
    author: Cedric (PAIDA)
    generated-by: AI
    ---

    # Sundown -- YYYY.MM.DD (<weekday>)

    ## Threads today
    - <topic> - one line. [[archive baton note]]

    ## Files changed
    - [CREATE/UPDATE/DELETE] path - one line.

    ## Jobs check
    - gmail-self-notes: ran / NOT RUN
    - portfolio / news reports: ran / NOT RUN / n/a
    - yt-weekly-stats: ran / NOT RUN / n/a (Saturdays)

    ## Decisions and open loops
    - Decided: ...
    - Still open: ...

    ## Tomorrow
    - Calendar (via Annie): ...
    - First thing: ...

    ## Links
    - Journal: [[YYYY.MM.DD - Journal]] (if one exists)
    - Batons: <archive note links>

    ## Deferred (if any)
    - git / memory deferred - reason.

---
title: Baton Handover -- Wrap Procedures
date: 2026-07-11
time: 12:28 (London)
topic: Wrap Procedures
thread: Designed and installed sundown-wrap; resolved the backup architecture; wrote the personal-backup runbook
status: handover
author: Cedric (PAIDA)
generated-by: AI
---

# Baton Handover -- Wrap Procedures (2026-07-11 1228)

Topic: [[Wrap Procedures]]

## Thread character

Continued from the baton-wrap design thread. This thread designed, installed and
dry-ran sundown-wrap, then pivoted into resolving the two-vault / GitHub-backup
problem that has dogged both wrap skills. Ended by writing a full backup runbook,
which Mick is now reviewing before we execute.

## Decisions made

- sundown-wrap BUILT and installed at Dex-MickP/skills/sundown-wrap/SKILL.md.
  Design locked: (1) trigger = manual plus a soft evening nudge after ~18:00 that
  asks, never acts; (2) daily-note home = a dedicated _daily/ folder holding BOTH
  Mick's Journal notes and Cedric's Sundown notes, distinguished by suffix; (3) mount
  friction = ask for vault-root access first, skip-with-note as the plan-B default.
- Rerun safety: canonical YYYY.MM.DD - Sundown.md plus archive-on-overwrite to
  _daily/archive/ (mirrors baton LATEST+archive). Test runs use a (DRY RUN) suffix and
  never write to _daily.
- Jobs check reads list_scheduled_tasks lastRunAt (authoritative), NOT the changelog
  (the gmail sweep and morning briefing never touch the changelog).
- Backup architecture LOCKED: keep the Dex-MickP fork clean and shareable; back up
  EVERYTHING personal to a SEPARATE private repo (Dex-MickP-Personal) via a nightly
  9pm mirror-and-push. Runbook written and filed at
  06-Resources/2026.07.11 - Personal Content Backup - Plan and Runbook.md.
- 9pm scheduler mystery solved: the Windows task is set for 21:00 with run-after-missed
  catch-up, so a PC-off evening pushes the run to next morning - hence the scattered
  commit times.

## Files changed this thread

- [CREATE] Dex-MickP/skills/sundown-wrap/SKILL.md - the installed skill. NOT yet
  git-committed or pushed (cloud cannot push; do from PC).
- [CREATE] Dex-MickP/06-Resources/2026.07.11 - Personal Content Backup - Plan and
  Runbook.md - the runbook. Also needs a PC commit/push.
- [CREATE] PAIDA Master/_daily/README.md - Journal vs Sundown naming (moves into
  Dex-MickP in Phase A).
- [UPDATE] auto-memory: project_wrap_skills, reference_dex_mickp_git_backup, MEMORY.md.
- Deliverables in outputs: sundown-wrap SKILL copy, the (DRY RUN) sample note, the
  runbook.

## Open questions / unfinished

- Mick is REVIEWING the runbook. Awaiting his go-ahead to run Phase A (consolidate
  _handovers/_changelog/_daily into Dex-MickP + gitignore them in the fork) and then
  Phase B (create Dex-MickP-Personal repo, mirror script, 9pm task) on his PC.
- Decision pending: 08-People, 09-Entities and Active are tracked by the fork today -
  move them out of the shareable fork or leave them?
- Verify on the PC whether the existing 9pm Dex-MickP job actually PUSHES - the cloud
  snapshot showed main ahead of origin by 1, but that view can be a stale mount.
- Cowork keeps defaulting to the PAIDA Master scratch folder, not Dex-MickP - that is
  why wrap output lands in the wrong place. Point Cowork's default at Dex-MickP.
- The new sundown-w
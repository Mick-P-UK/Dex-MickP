---
title: Choosing the Right Environment (Claude Code, Desktop, Cowork, claude.ai Web)
tags:
  - SOP
type: SOP
status: active
version: 1.0
created: 2026-07-10
owner: Mick
related:
  - SOP - End-of-Month Portfolio Posting.md
  - Quick Start - Run EOM Portfolio Posts in Claude Code.md
  - 2026.07.09 - Architecture Change Note - Cowork Cloud Migration and Credentials.md
  - 2026.07.10 - RUNBOOK - Push Dex-MickP to GitHub (Local)_v1.0.md
---

# SOP - Choosing the Right Environment

## 1. Purpose

Mick works across four different Claude surfaces (Claude Code, Claude Desktop, Cowork,
claude.ai Web), and since the 7 July 2026 Cowork cloud migration they no longer all have
the same reach into local files and credentials. This SOP is a quick decision guide for
"which one do I open for this task" - so a job does not get started in the wrong place
and fail halfway through (as happened with the June portfolio drafts and the GitHub push
backlog). For the full technical background on WHY this changed, see the architecture
note: 06-Resources/2026.07.09 - Architecture Change Note - Cowork Cloud Migration and
Credentials.md. This SOP is the short, practical companion to that longer reference.

## 2. The Four Surfaces at a Glance

| Surface | Where it runs | Reaches C:\Users\pavey\.env or other home-folder files | Reaches connected folders | Reaches connectors (Gmail, Drive, Notion, Slack, Calendar) | Needs the PC on |
|---------|---------------|----------------------------------------------------------|----------------------------|--------------------------------------------------------------|------------------|
| Claude Code (CLI) | Locally, on Mick's PC, with Mick's own Windows permissions | YES - full native access | YES | YES (via MCP where configured) | YES |
| Claude Desktop (Filesystem MCP) | Locally, on Mick's PC, via the Filesystem MCP | YES, for any folder the MCP is configured to see | YES | YES | YES |
| Cowork (the "Home" tab, incl. inside the Desktop app since 7 Jul 2026) | REMOTELY, in a temporary sandbox on Anthropic's servers | NO - cannot reach the home-folder root or any unconnected file | YES, but ONLY folders Mick has explicitly connected, and ONLY while the Desktop app stays open | YES - this is the intended path for these | NO for cloud-only work; YES if it needs a connected folder or the browser |
| claude.ai Web | REMOTELY, in the cloud | NO | NO local files at all | YES | NO |

## 3. The One Rule That Matters

**If the task needs to read C:\Users\pavey\.env, push to GitHub, log in to a website with
a saved local session (ShareScope, NotebookLM), or browse broadly across the PC's file
system - run it in Claude Code, locally, on Mick's PC. Nothing else can do this reliably
since 7 July 2026.**

Everything else (email triage, calendar, Notion, Drive files, an explicitly connected
folder) is a good fit for Cowork or claude.ai Web, and those are the right default for
anything that should also work with the PC switched off.

## 4. Decision Checklist

Ask these in order. Stop at the first YES.

1. Does the task need C:\Users\pavey\.env or any other file under C:\Users\pavey\ that
   has not been explicitly connected? -> **Claude Code**.
2. Does the task run `git push`, `git pull`, or anything needing locally-stored git/GitHub
   credentials? -> **Claude Code**.
3. Does the task drive a Playwright/browser automation with a saved local login
   (ShareScope, NotebookLM CLI, ax-trees-automation)? -> **Claude Code** (Desktop app must
   also be open if the flow depends on a visible browser window).
4. Does the task only need Gmail, Google Drive, Google Calendar, Notion, Slack, or another
   connector? -> **Cowork or claude.ai Web** - this is the intended, supported path and
   works with the PC off.
5. Does the task only need a SPECIFIC folder that Mick has already connected in the
   Desktop app (e.g. the DIY - Portfolios snapshots folder)? -> **Cowork** is fine for
   reading/writing that folder, but keep the Desktop app open, and remember it still
   cannot reach .env for any credential step later in the same job.
6. Unsure, or the job mixes local-file/credential steps with connector steps? -> Default
   to **Claude Code**. It is a superset of what Cowork can do locally, and it is the only
   surface proven to complete credential-touching jobs end to end.

## 5. Worked Examples (from real sessions)

| Job | Right surface | Why |
|-----|---------------|-----|
| End-of-month portfolio posting (WordPress drafts) | Claude Code | Needs the Poster Pete WordPress credentials from C:\Users\pavey\.env. See SOP - End-of-Month Portfolio Posting.md. |
| Pushing Dex-MickP commits to GitHub | Claude Code | Needs local git/GitHub credentials; a cloud sandbox has none. See the GitHub push RUNBOOK. |
| Cleaning non-ASCII characters out of a vault file and committing it | Claude Code | Same reason - the commit/push step needs local git credentials, even though the text-cleaning step itself has no credential dependency. |
| ShareScope chart/report automation | Claude Code | Logs in to ShareScope via a saved Playwright session and reads/writes local files; the Desktop app also needs to be open if the browser window must be visible. |
| gmail-self-notes vault ingestion | Cowork | Purely connector-based (Gmail, Google Drive) plus writes into an already-connected vault folder. No .env dependency. |
| Reading or summarising a Notion page | Cowork or claude.ai Web | Connector-only, no local files or credentials needed. |
| "Which environment am I in right now" | Either - self-detecting | Claude Desktop/Filesystem MCP sessions call Filesystem:list_allowed_directories and get a path list; claude.ai Web sessions get a failure/unavailable result. See CLAUDE.md "FIRST ACTION - DETECT ENVIRONMENT". |

## 6. If a Job Fails Partway Through

If a task starts in Cowork or claude.ai Web and then hits a wall (a folder it cannot
reach, a credential it cannot read, a git push it cannot authenticate), do NOT try to
work around it with a partial fix in the cloud session. Stop, tell Mick what step failed
and why, and either:

- Hand the WHOLE job to Claude Code (safest - re-run end to end locally), or
- Split it: let the cloud session do the connector-based / content-generation part it CAN
  do, write a plain-English handoff note (see the pattern used in the PATH ASCII cleanup
  NOTE and the GitHub push RUNBOOK), and let Claude Code finish the credential-touching
  part.

Never invent a workaround that stores a credential inside a cloud session, hardcodes a
secret in a script, or creates a second .env file. See the CREDENTIALS SINGLE-SOURCE rule
in the master CLAUDE.md.

## 7. Open Questions to Watch (carried from the architecture note)

- No first-class secrets mechanism exists for cloud Cowork sandboxes today. Re-check
  Anthropic's release notes periodically in case this changes.
- No managed connector/MCP exists yet for the self-hosted WordPress site
  (diy-investors.com). If one appears, the EOM portfolio posting job could move off
  Claude Code.
- Confirm the Section 7 "repercussions register" in the architecture note item by item as
  each workflow is actually run again, rather than assuming it is still accurate.

## 8. Related Documents

- 06-Resources/2026.07.09 - Architecture Change Note - Cowork Cloud Migration and
  Credentials.md - full technical background, dates, sources.
- 06-Resources/SOPs/SOP - End-of-Month Portfolio Posting.md - a worked example that
  requires Claude Code.
- 06-Resources/SOPs/Quick Start - Run EOM Portfolio Posts in Claude Code.md - short
  version of the same job.
- 06-Resources/SOPs/2026.07.10 - RUNBOOK - Push Dex-MickP to GitHub (Local)_v1.0.md -
  another worked example that requires Claude Code.
- CLAUDE.md (vault root) - "FIRST ACTION - DETECT ENVIRONMENT" section, and the
  CREDENTIALS SINGLE-SOURCE rule in the master global CLAUDE.md.

## 9. Revision History

- v1.0 (2026-07-10) - Created by Cedric, offered on 2026-07-09 during the SOP library
  session, built on 2026-07-10 at Mick's request.

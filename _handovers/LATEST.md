---
title: Baton Handover -- Config-Loading Fixes (Greeting v2.0 + Ron user-level) + NBLM Auth Self-Heal + Off-Machine Backups
date: 2026-07-23
time: 07:00 (London, verified via GMT Standard Time)
topic: Fixing the class of "config that loads in claude.ai but not Claude Code" problems, plus CREI housekeeping, an auth self-heal, and closing two backup gaps
thread: Fresh morning session in the C:\Vaults working directory (Claude Code). Started as a chat about which MCPs are connected, turned into diagnosing why the time-based greeting fires on claude.ai but only intermittently in Claude Code, then broadened into fixing the same root cause for the Ron sub-agent, hardening the NotebookLM auth flow, tidying the CREI research threads (retro items 1-3), and closing two backup blind spots.
status: handover
author: Cedric (PAIDA)
generated-by: AI
---

# Baton Handover -- Config-Loading Fixes + Auth Self-Heal + Backups (2026-07-23 07:00)

Topic: where Claude Code loads config from, and why nested-vault rules/agents were silently not loading; plus CREI housekeeping and backup gaps.
Working directory this session: C:\Vaults (Claude Code).

## Thread character

Conversational, diagnostic, and productive. Mick's instinct throughout was to ask "why did that happen?" about small anomalies, which repeatedly surfaced systemic gaps. NOTE: this session did NOT run the session-start routine at first (Cedric missed reading LATEST.md + CEDRIC_MEMORY.md before greeting) - Mick caught it, we diagnosed why, and it led directly to the greeting-rule fix. Startup routine was run properly mid-session.

## The core diagnosis (applies to more than the greeting)

In a Claude Code session rooted at C:\Vaults, the harness auto-loads ONLY: user-level C:\Users\pavey\.claude\ (CLAUDE.md + its @_rules.md import) and the working-dir-root C:\Vaults\CLAUDE.md (plus @-imports). It does NOT auto-load nested-vault config such as Mick's-Dex-2nd-Brain\Dex-MickP\.claude\agents\*.md or that vault's own CLAUDE.md unless the session is rooted inside that vault. That is why things defined only in nested vault .claude/ folders work on claude.ai / Desktop / Cowork (which load the vault directly) but not in a C:\Vaults-rooted Claude Code session. Captured as memory claude-code-config-loading-mick-vaults.

## What was done

**1. Greeting rule v2.0 (fixed the intermittency).** The time-based greeting lived only in the vault Dex-MickP\CLAUDE.md USER_EXTENSIONS block (loaded by claude.ai) and CEDRIC_MEMORY.md - neither auto-loads in Claude Code, hence intermittent. Fix: vault CLAUDE.md block is now CANONICAL and version-stamped v2.0; a MIRROR was added to C:\Users\pavey\.claude\_rules.md (loads every Claude Code session via @import) using a PowerShell London-time check instead of the vault copy's Python; CEDRIC_MEMORY.md "London Time Protocol" slimmed to a pointer to stop drift. Mick committed this himself (Dex-MickP commit f56af67, pushed). Greeting verified working live (06:03 -> "Good morning").

**2a. CREI notebook cleanup (retro item 2).** Deleted the stray untagged/error-status balance_sheet source (id 50761844) left by yesterday's manual retry, from notebook 53fd542b-e797-48cb-a6bc-7c0d0b4d74ef. Verified the six [PIPE] ShareScope sources remain intact. Notebook is now clean, so the next run's selective-clear will not trip over a duplicate.

**2b. Transport-timeout retry loop (retro item 2 root cause).** Added a bounded (3-attempt, 5s backoff) retry around the ADD_SOURCE call in upload_csvs_to_notebook() in sharescope_nlm_researcher.py, keyed off transient markers (TransportServerError, request timeout, "server-error retries exhausted"); non-transient errors still fail immediately. py_compile OK, 0 non-ASCII. This is the root-cause fix for yesterday's balance_sheet timeout. Committed to the ShareScope repo (ba053d1, local-only - see backups below).

**3. Ron sub-agent now loads everywhere (retro item 5).** ron.md existed only in the two nested vault .claude/agents/ folders, so subagent_type: "ron" never registered in a C:\Vaults-rooted session (restarts never helped). Fix: copied the byte-identical canonical (all three copies MD5-verified identical) to user-level C:\Users\pavey\.claude\agents\ron.md. Registers from ANY working directory next session. Still needs a restart to take effect THIS session (agent types load at startup), but the "must launch inside the vault" fragility is gone permanently.

**BONUS - NotebookLM auth self-heal (the session's best fix).** Mick ran an experiment: fired `notebooklm login` from Cedric's shell to see what happens. Result: it completed hands-off ("Already logged in.") because the CLI keeps its own persistent Chromium profile (C:\Users\pavey\.notebooklm\profiles\default\browser_profile) that was still logged into Google, and it re-saved fresh auth with ZERO manual input. This is the fix for the "auth-lie" (stale storage_state.json while the browser profile is still valid). Baked in at two levels: (a) preflight_auth_check() now auto-runs `notebooklm login` and re-verifies before halting; (b) a new _rules.md rule "NotebookLM auth - self-heal before asking Mick". Mick only needs to log in manually when the browser-profile session itself is dead. Ron's agent-def "Auth fallback" section and the ShareScope SOP auth step still say the old "ask Mick first" - flagged in-code and in _rules.md to align on the next retro pass.

**Two backup gaps closed / scheduled.**
- ~/.claude had NO version control at all (global CLAUDE.md, .CLAUDE.md, abbreviations.md, _rules.md, agents/ron.md - all single-home, unbacked). Interim fix DONE: snapshotted those 5 files into Dex-MickP\System\claude-config-backup\ (secret-scanned clean), committed 622b562 and PUSHED to GitHub. NOTE: this is a SNAPSHOT, not a live sync - it goes stale if those files change. Proper fix is a dedicated private repo for ~/.claude = spawned task (URGENT, target ~2026-07-26).
- ShareScope-Automation is its own nested git repo (branch post-webinar-dev) with NO remote - all commits incl. ba053d1 are local-only. Spawned task to add a private GitHub remote + push (URGENT, target ~2026-07-26).

**Session close-out.** Meet Cedric episode "The Case of the Missing Good Morning" drafted to Dex-MickP\00-Inbox AND created in Notion Content Studio (page 3a6db32a9b0a81c2bf53cb6ee7241f59; Project=Meet Cedric, Format=Video, Status=Draft, Audience=YouTube/Public) - third in the environment-loading mini-arc after "When the Job Moves House" and "Two Doors, Two Toolkits". Two learnings saved to the Claude Code memory system (claude-code-config-loading-mick-vaults; verify-git-state-before-committing) with a new MEMORY.md index.

## Decisions made

- Greeting rule: vault-canonical + _rules.md mirror + version stamp (not two independent copies). Ron: byte-identical copies, kept identical by hash rather than stamped, because unlike the greeting rule they are meant to be the same everywhere.
- Backup: interim snapshot into the existing private, GitHub-backed Dex-MickP repo now; dedicated ~/.claude repo deferred to the urgent task (avoids rushing a secrets-sensitive new repo before RNS).
- Cedric CAN run git directly in Claude Code on Mick's PC (the old "Cedric cannot run git" note was a Cowork/Desktop-era limitation). Verified: committed + pushed this session.
- Always verify real git state before committing here - nested repos + Mick's between-turn commits mean a pre-drafted commit block can be wrong. (Mick had already committed the greeting work himself as f56af67 before Cedric went to commit it.)

## Files changed this thread

- [MODIFY] Dex-MickP\CLAUDE.md - greeting block stamped v2.0 + canonical-source note. (Committed by Mick, f56af67.)
- [MODIFY] Dex-MickP\CEDRIC_MEMORY.md - London Time Protocol slimmed to pointer (in f56af67); plus this wrap's prepend.
- [MODIFY] C:\Users\pavey\.claude\_rules.md - greeting v2.0 mirror + NotebookLM auth self-heal rule. (NOT under git except via the new snapshot.)
- [CREATE] C:\Users\pavey\.claude\agents\ron.md - user-level Ron copy. (Backed up via snapshot.)
- [MODIFY] Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\sharescope_nlm_researcher.py - ADD_SOURCE retry loop + preflight_auth_check() self-heal. (ShareScope repo commit ba053d1, LOCAL ONLY.)
- [MODIFY] NBLM notebook 53fd542b... - deleted stray source 50761844.
- [CREATE] Dex-MickP\System\claude-config-backup\ (6 files) - config snapshot. (Committed + pushed, 622b562.)
- [CREATE] Dex-MickP\00-Inbox\2026.07.23 - Meet Cedric - The Case of the Missing Good Morning.md.
- [CREATE] Notion Content Studio page 3a6db32a9b0a81c2bf53cb6ee7241f59 (Meet Cedric episode).
- [CREATE] ~/.claude memory: claude-code-config-loading-mick-vaults.md, verify-git-state-before-committing.md, MEMORY.md.

## Open questions / unfinished

- URGENT (task, ~2026-07-26): dedicated private git repo for ~/.claude (snapshot is interim only; goes stale on edit).
- URGENT (task, ~2026-07-26): private GitHub remote for ShareScope-Automation (ba053d1 + prior work backed up nowhere off-machine).
- NEW (2026-07-23): the Cowork vault C:\Vaults\Cowork\ is NOT a git repo, so the CANONICAL ShareScope SOP (3-SKILL-sharescope-nlm-research.md) and everything else in Cowork has NO off-machine backup. Fold into the C:\Vaults backup strategy decision (task_c3efead7). Reminder also added to CEDRIC_MEMORY.md.
- CREI retro (item 1) CLOSED 2026-07-23 (afternoon). All five findings resolved: verdict drift (baked a "lead with stable price levels + chart date, treat the single BUY/HOLD/SELL word as secondary" line into Ron's template); auth-canary lie (fixed - self-heal, verified in code); balance-sheet transport timeout (fixed - retry loop, verified in code); P&amp;L HTML-entity leak (NOT a bug - Ron's markdown + template are clean, was a Notion-render artifact, spot-check on next push); Ron subagent-type restart (fixed - Ron registers now). Committed + pushed 658fe25.
- Align Ron's agent-def "Auth fallback" + the ShareScope SOP auth step to the self-heal - DONE 2026-07-23. All four ron.md copies edited byte-identical (hash 8afcc13); canonical SOP (Cowork, 4 spots) + both vault SKILL.md mirrors aligned so auth failure tries hands-off `notebooklm login` FIRST, escalating to Mick only if the browser-profile session is dead. In 658fe25 (2 ron.md tracked copies + 2 SKILL.md mirrors); the Cowork canonical SOP copy is NOT git-backed (see new open item above).
- Ron subagent-type: user-level ron.md added, but THIS session still lacks it (restart pending). Confirm it registers on the next fresh session.
- Meet Cedric episode: created in Notion as Draft - ready to script/produce when Mick wants.

## Next-thread pickup

- Opener: "Cedric, resume from LATEST handover."
- FIRST ACTION: run the session-start routine properly (read this file, then CEDRIC_MEMORY.md top) BEFORE greeting - and greet using the verified London time (greeting rule v2.0 should now load from _rules.md in Claude Code; confirm it fires).
- Likely first tasks: (1) either of the two urgent backup tasks (now also covering the Cowork-vault git gap); (2) whatever Mick brings. [CREI retro CLOSED 2026-07-23 - see Open questions.]
- What NOT to re-derive: the config-loading model (memory claude-code-config-loading-mick-vaults); the auth self-heal mechanism (baked into code + _rules.md); that ShareScope-Automation is a separate nested repo with no remote; that Cedric can run git here.

## Content Studio logged

Meet Cedric "The Case of the Missing Good Morning" - Draft in Notion Content Studio (3a6db32a9b0a81c2bf53cb6ee7241f59). Third in the environment-loading mini-arc.

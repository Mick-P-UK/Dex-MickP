# PAIDA Session Log

---

## Session: 2026-05-01 (Friday afternoon)

_Session started: ~17:20 BST_
_Environment: Cowork (Claude Desktop) - Dex vault + Cowork vault mounted_

### Context at Session Start

- Continuation of ShareScope automation work. Existing project lives at:
  04-Projects/2026.04.04-ShareScope-Automation/
- New work: setting up ax-trees-automation as a dedicated, structured home for
  all accessibility tree automation across DIY Investing apps.

### Actions Taken This Session

1. **ax-trees-automation folder created**
   - Location: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\ax-trees-automation\
   - README.md and memory.md created as initial files.

2. **Full folder structure planned (7 iterations, plan mode throughout)**
   - Primary use case: DIY Investing automation (ShareScope first, Stockopedia future)
   - Key structural decisions agreed:
     * App folders named simply (sharescope/, stockopedia/) - no suffix
     * ALL skills at root skills/ - globally callable by agents or verbally
     * skills/SKILLS-INDEX.md - master catalogue for agent lookups
     * mini-projects/ folder - one subfolder per automation project with PROGRESS.md
     * MINI-PROJECTS-MASTER.md - master to-do list for all automation routines
     * outputs/ - Obsidian markdown with YAML frontmatter (committed to GitHub)
     * templates/ - YAML frontmatter templates matching existing manual file formats
     * YAML author field: AI vs Mick to distinguish automated from manual outputs
     * screenshots/debug/ and auth/ - gitignored
     * PRD.md at root
     * CLAUDE.md at root (light - global rules + per-app guideline refs)
     * Per-app guidelines file (e.g. sharescope/sharescope-guidelines.md)
     * AX tree versions in versions/ subfolder per app
     * session-logs/ with summaries/ subfolder
     * plugin/ placeholder with README (future commercial/member distribution)
     * Anti-bot: random delays as global rule + shared delay-helper.js in skills/
     * .gitignore, package.json, playwright.config.js at root

3. **Meet Cedric - ShareScope sub-series agreed**
   - To be set up in Notion Content Studio as a separate series branch
   - Documents the ShareScope automation adventures as YouTube content
   - Action: pending (to be done this session)

### Actions Taken (continued)

4. **Task 1 COMPLETE - Folder structure built**
   Full v7 structure created in ax-trees-automation/:
   - All directories created and verified
   - CLAUDE.md (global rules, anti-bot policy, app guideline refs)
   - .gitignore (excludes .env, node_modules, auth/, screenshots/debug/)
   - .env.example (variable names only, safe to commit)
   - package.json + playwright.config.js (Node/Playwright project setup)
   - skills/SKILLS-INDEX.md (master skills catalogue)
   - skills/delay-helper.js (anti-bot random delay utility - first shared skill)
   - mini-projects/MINI-PROJECTS-MASTER.md (5 ShareScope mini-projects logged)
   - templates/ (chart, portfolio, metrics YAML frontmatter templates)
   - plugin/README.md (placeholder for future member distribution)
   - sharescope/sharescope-guidelines.md (app rules, quirks, migration notes)
   - sharescope/sharescope-ax-tree-master.md (placeholder pending migration)
   - stockopedia/stockopedia-guidelines.md (placeholder)
   - PRD.md (placeholder - to be written next session)
   - All empty folders: docs/, outputs/charts|portfolios|metrics,
     screenshots/debug/, auth/, session-logs/summaries/, sharescope/versions/,
     stockopedia/versions/

5. **Task 4 COMPLETE - Meet Cedric ShareScope series created in Notion**
   - New hub page created in Micks Content Studio
   - Title: "Meet Cedric - ShareScope Automation Series Hub"
   - Status: Brain Dump | Project: Meet Cedric | Audience: YouTube/Public + Inner Circle
   - Contains: series concept, episode ideas (8 episodes braindumped), episode log
   - Notion URL: https://app.notion.com/p/353db32a9b0a81018396c00fb2378db4

### Current Status

- Tasks 1 and 4 COMPLETE
- Tasks 2 and 3 deferred to next session (context reasons)
- Pickup document written: ax-trees-automation/session-logs/2026-05-01-session.md

### Deferred to Next Session

- [ ] Task 2: Write PRD.md (full product requirements)
- [ ] Task 3: Explore 04-Projects/2026.04.04-ShareScope-Automation/ and plan migration
- [ ] All items from previous sessions carried forward

_Session closed 2026-05-01 ~18:10 BST_

---

_This file is the current session working doc. Completed sessions are archived to Session_Archive/ (architecture TBC)._

---

## Session: 2026-04-29 (Wednesday - Webinar Day)

_Session started: 2026-04-29 ~09:43 BST_
_Environment: Cowork - full MCP suite confirmed_

### Context at Session Start

- Webinar day. Pipeline frozen at v1.0-webinar-ready. Plan B backup recording planned before tonight's live demo.
- /research skill and slash command live from yesterday's session.
- Mick setting up shortcodes for the two terminal commands.

### Actions Taken This Session

1. **/research skill explained** - full walkthrough of the slash command, where to use it (Cowork), syntax, what each step does.

2. **Bug 1 fixed: Square brackets in shortcode**
   - Mick typed `python sharescope_orchestrator.py [COST]` - brackets included literally.
   - ShareScope returned: `Error: Stock '[COST]' not found`.
   - Fix: clarified brackets are notation only. Correct syntax: `python sharescope_orchestrator.py COST`.

3. **Ticker ambiguity noted: COST**
   - COST is Costain Group on LSE and Costco on NASDAQ.
   - ShareScope covers both markets. Mick ran COST intentionally to test disambiguation.
   - Orchestrator ran cleanly - 6 CSV files downloaded.

4. **Bug 2 fixed: Colon in notebook title**
   - NLM researcher failed at notebook creation: `Failed to create notebook 'COST - Costain Group_Updated:2026.04.29': `
   - Cause: NotebookLM API rejects colons in notebook names.
   - Fix: patched two lines in sharescope_nlm_researcher.py: Updated:{date_str} -> Updated_{date_str}.
   - Mick requested underscore separator - keeping dots reserved for within the date itself.

5. **Bug 3 fixed: Chrome profile lock on notebooklm login**
   - notebooklm login crashed with TargetClosedError on page.goto(accounts.google.com).
   - Cause: Playwright persistent profile locked by open Chrome window.
   - Fix: close all Chrome windows before running notebooklm login.
   - notebooklm_auth_status.json showed ok throughout - cookies valid, failure was process conflict only.
   - Login confirmed: Authentication saved to C:\Users\pavey\.notebooklm\storage_state.json

6. **First new company added: COST (Costain Group)**
   - Full pipeline ran end-to-end cleanly after all three fixes.
   - 6 CSVs downloaded, new notebook created (ID: 1deb3e2f-d44b-44f1-81bb-c1f934704b9e).
   - CSVs + news uploaded in parallel. Nina analysis written.
   - Report saved: 2026.04.29 - COST - Costain Group - AI - Financial Analysis.md
   - Research Log index updated: 5 companies (SQZ, GGP, ACMR, HAL, COST).
   - Mick confirmed report opened via Obsidian deep-link.

7. **Memory, session log, Notion Episode 11 updated** (this entry).

### Current Status

- Pipeline confirmed in production on a new company.
- Three bugs found and fixed. All fixes in script.
- Pre-webinar checklist complete: NLM auth refreshed, test run done, shortcodes working.
- Plan B recording: Mick recording a clean run shortly for backup.
- Webinar tonight: live demo at v1.0-webinar-ready.

### Outstanding

- All items from previous sessions carried forward unchanged.
- Post-webinar: Phase 2 member distribution, GitHub repo, voice listener hardening.

_Session active as of 2026-04-29 ~11:00 BST_

---

## Session: 2026-04-28 (Tuesday morning)

_Session started: 2026-04-28 ~06:39 BST_
_Environment: Cowork (Claude Desktop) - full file access confirmed_

### Context at Session Start

- Mick has a webinar on Wednesday where he plans to demo the ShareScope automation live.
- stock-research skill exists in vault but NOT installed in Cowork skills system (gave "unknown skill" error).
- Ran the skill manually by reading SKILL.md from vault.

### Actions Taken This Session

1. **stock-research skill - diagnosed "unknown skill" error**
   - Skill exists at: Dex-MickP/skills/stock-research/SKILL.md
   - Not mirrored to Cowork's read-only skills system (can't self-install).
   - Ran pipeline manually by reading SKILL.md directly. Full pipeline works.
   - **TODO for Mick: get stock-research properly installed as a Cowork skill.**

2. **SQZ (Serica Energy) - first pipeline run**
   - NLM notebook check returned `found: false` (possible race condition on stale result file - needs investigation).
   - New permanent NLM notebook created: "SQZ - Serica Energy_Updated:2026.04.28"
   - Notebook ID: 0befe39a-d458-4392-9785-e2d808bafca9
   - ShareScope run FAILED: stock 'SQZ' not found - CSS locator bug in sharescope_search.py.

3. **sharescope_login.py - bring_to_front fix**
   - Added `page.bring_to_front()` after successful login.
   - Browser window was running visible (SHARESCOPE_HEADLESS=false confirmed) but opening behind other windows.

4. **sharescope_search.py - Step 6 rewrite (accessibility tree approach)**
   - Old code used CSS `[cursor='pointer']` attribute selector - not a DOM attribute, never worked.
   - New code uses `page.get_by_text(re.compile(r":{TICKER}\b"))` - exchange-agnostic regex.
   - Matches LSE:SQZ, NYSE:SQZ, AIM:SQZ etc. without hardcoding any exchange.
   - Dual listing handled: JS `el.closest('[class*="result"]')` walks up DOM, filters out Historical entries.
   - Falls back to plain text match if colon-prefix match finds nothing.

5. **sharescope_nlm_researcher.py - two CLI flag bugs fixed**
   - BUG 1: `--text` flag not supported in installed notebooklm CLI version.
     Fix: write source content to temp file, pass file path as positional arg.
   - BUG 2: `--wait` flag also not supported.
     Fix: removed `--wait` from `["source", "add", tmp_path, "--title", source_title]`.
   - CSV export confirmed working: 6 of 6 tabs downloaded in 18 seconds.
   - NLM upload fix (BUG 2) applied but NOT YET TESTED - requires one more watcher restart.

6. **Multiple watcher instance race condition - resolved**
   - Old pythonw.exe instances (without NLM researcher) were competing for the queue.
   - Fix: `taskkill /F /IM pythonw.exe` then fresh `start_watcher.bat`.
   - Key learning: watcher uses pythonw.exe (not python.exe) - must kill by that name.
   - Key learning: Python import caching means code changes require watcher restart.

### Current Status (session end - context full)

- ShareScope CSV export: CONFIRMED WORKING (6 of 6 tabs, 18 seconds)
- Search fix: CONFIRMED WORKING (LSE:SQZ selected over NYSE:SQZ#1 Historical)
- bring_to_front: CONFIRMED WORKING
- NLM upload: --wait flag fix applied, NOT YET TESTED
- **NEXT ACTION: Mick restarts watcher (taskkill /F /IM pythonw.exe + start_watcher.bat)**
- **THEN: Cedric confirms NLM enabled, writes run_queue.json to trigger final test run**
- Pickup point file: 04-Projects/2026.04.04-ShareScope-Automation/PICKUP_POINT_2026.04.28.md

### Outstanding from This Session (to carry forward)

- [ ] **IMMEDIATE: One more watcher restart + SQZ run to test NLM --wait fix**
- [ ] Install stock-research skill properly in Cowork (Mick flagged as important)
- [ ] Fix sharescope_logout.py: Page.press() missing 'key' argument (non-critical)
- [ ] Fix sharescope_orchestrator.py: SyntaxWarning on line 9 (non-critical)
- [ ] Investigate NLM check returning found:false for newly-created notebooks (race condition?)
- [ ] All outstanding items from 2026-04-20 session still open

_Session closed (context full) - updated 2026-04-28 ~07:30 BST_

---

## Session: 2026-04-20 (Monday morning)

_Session started: 2026-04-20 ~09:42 BST_
_Environment: claude.ai Web (Filesystem MCP confirmed via tool_search)_
_Session closed: ongoing_

### Context at Session Start

- Continuation of PAIDA development work.
- Mick has Plaza Group webinar prep today so limited PAIDA time.
- Key loose ends from 2026.04.19: NotebookLM skill suite built but mirror deploy not verified.

### Actions Taken This Session

1. **NotebookLM skills mirror gap diagnosed and fixed**
   - All 4 NLM skills (notebooklm-notebook-setup, notebooklm-add-content, notebooklm-chat, notebooklm-studio-output) were in vault but NOT in /mnt/skills/user/.
   - Root cause: dual-deploy from yesterday's session was not verified ("Test, Don't Trust" failure).
   - All 4 skills copied to mirror with head-verified confirmation.
   - Skills are now live and will surface at next Desktop session start.

2. **Mandatory Skill Deploy Protocol added to CLAUDE.md**
   - New section appended: 6-step checklist with mandatory vault write + verify, mirror write + verify, README update, and confirmation to Mick.
   - Root cause note included so future sessions understand why it exists.
   - Edit done via Filesystem:edit_file (targeted append, not full rewrite).

3. **CLAUDE.md restructure plan produced**
   - Current state: 1115 lines, 44KB, loaded in full every session.
   - Agreed plan: split into 3 files (CLAUDE.md ~280 lines, CEDRIC-RULES.md ~330 lines, CEDRIC-DEX.md ~460 lines).
   - Projected saving: ~75% reduction in session context load.
   - Backup created: 07-Archives/CLAUDE-backups/CLAUDE.backup.2026.04.20.md
   - Execution deferred to next PAIDA session (webinar prep today).

4. **Memory system audit conducted**
   - Layers reviewed: CEDRIC_MEMORY.md, session_log.md, Anthropic built-in memory, Meet Cedric Notion.
   - Gap identified: no enforced session-end write, no memory-read verification at start.
   - 18 April PAIDA Session Memory planning doc pulled and integrated into CEDRIC_MEMORY.
   - All 5 open questions from 18 April preserved as outstanding items.

5. **Session end /wrap protocol agreed**
   - Behaviour agreed: session log + CEDRIC_MEMORY update + Meet Cedric brain dump + confirmation.
   - /wrap skill to be built in next PAIDA session (vault + mirror).

6. **Three Meet Cedric brain dumps logged in Notion:**
   - Episode A: PAIDA Memory System Audit + CLAUDE.md Restructure Plan
   - Episode B: Why Session Memory Is the Foundation of a Reliable AI Assistant
   - Episode C: Claude Code vs Desktop vs Cowork -- Why Your AI Has a Different Brain in Every Tab
   Note: Episodes B and C are strong companion pieces -- potential two-parter or one definitive video.
   All three best produced AFTER /wrap skill and Memory Read Confirmed checkpoint are built.

### Outstanding from This Session (carried to next PAIDA session)

- [ ] CLAUDE.md restructure Pass 1 -- create CEDRIC-RULES.md and CEDRIC-DEX.md
- [ ] PAIDA Session Memory -- answer 5 open questions, create NLM notebook, build vault structure
- [ ] /wrap skill -- build as vault+mirror skill
- [ ] Memory reading verification -- "Memory Read Confirmed" checkpoint at session start
- [ ] notion-summary-generator vault copy (only in MCP mirror currently)
- [ ] Janusz Marecki IC webinar guest invite (task ^task-20260322-001)
- [ ] Micks-View Phase 1 build -- PRD v2.2 approved, not yet started
- [ ] /radar skill -- 5 items in Section 10 awaiting Mick sign-off

### Carried Forward (from 2026.04.18)

- [ ] NotebookLM: nlm setup add claude-code -- pending
- [ ] Create 3 NLM notebooks: IC Webinars, Plaza Group Webinars, AI for Investing Webinars
- [ ] radar_extractor.py --backfill
- [ ] Delete old PROPPS notebook index source copy (untimstamped version)
- [ ] Delete test notebook ee2a7ca3
- [ ] April 2026 portfolio batch -- end of April

_Session active as of 2026-04-20 ~10:30 BST_

---

## Session: 2026-04-18 (Saturday afternoon)

_Session started: 2026-04-18 ~14:03 BST_
_Environment: Claude Desktop (Filesystem MCP confirmed)_
_Session paused: 2026-04-18 ~14:33 BST (Mick heading out)_

### Context at Session Start

- Mick confirmed today's earlier tasks complete before 14:00: Portico Weekend Report done,
  Woolpack telephoned (11 people confirmed for Tuesday), Plaza Group Meeting prep started.
- Remainder of today: Gardening (14:00-17:00), Shatterford Village Hall band session (19:00-22:00).
- Busy week ahead: Elstead Investors Group Zoom (Tuesday, Mick chairing), Plaza Group Webinar (Wednesday 19:30).

### Actions Taken This Session

1. **/daily briefing delivered** - full today + rest of week calendar, priority reminders included.

2. **notion-summary skill upgraded (dual deploy)**
   - User provided improved spec block for the Notion announcement summary workflow.
   - Vault folder created (was missing): C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\notion-summary\
   - SKILL.md upgraded at both vault master and MCP mirror (/mnt/skills/user/notion-summary/)
   - skills README.md updated with full two-skill distinction section (see Skills Note below).

3. **PAIDA Session Memory - planning discussion (IN PROGRESS)**
   - Mick raised the issue of permanent session memory - no reliable cumulative archive exists.
   - Discussed storage options: vault, Notion, dual, NotebookLM.
   - Mick proposed NotebookLM as the query/RAG layer - strong fit for retrieval requirements.
   - Key insight: NLM Studio note feature allows short ad-hoc notes (typed or dictated)
     that persist and can be promoted to sources - solves the quick-note requirement.
   - Emerging architecture: vault (raw archive) + NLM (query layer).
   - Planning doc created at: System/Session_Notes/2026.04.18-PAIDA-Session-Memory-Planning.md
   - 5 open questions remain - to be resolved when Mick returns (later today or Sunday).
   - NOTHING BUILT YET - plan mode only.

### Skills Note: Two Notion Summary Skills

There are two separate summary skills serving different environments:

**notion-summary** (browser-control version)
- Location: skills/notion-summary/ + /mnt/skills/user/notion-summary/
- Method: Browser automation - get_page_text, click field, Ctrl+B for bold, Shift+Enter for line breaks
- Use when: Claude Code or Claude in Chrome (browser control available)
- Bold: Works correctly via Ctrl+B keyboard shortcut

**notion-summary-generator** (Notion MCP version)
- Location: /mnt/skills/user/notion-summary-generator/ (MCP mirror only - not yet in vault)
- Method: Notion MCP tools - notion-fetch to read, notion-update-page to write
- Use when: Claude Desktop with Notion MCP connected (no browser needed)
- Bold: Does NOT render - Summary (item) is plain text. Markers included for readability only.

Both produce structured summary max 200 words with adapted section headings.

### Outstanding from This Session

- [ ] PAIDA Session Memory architecture - 5 open questions to resolve on Mick's return
      -> Planning doc: System/Session_Notes/2026.04.18-PAIDA-Session-Memory-Planning.md
- [ ] Janusz Marecki IC webinar guest invite still pending (task ^task-20260322-001)
- [ ] Micks-View Phase 1 build - PRD v2.2 approved, build not yet started
- [ ] /radar skill build - awaiting Mick sign-off on 5 items in Section 10 of planning doc
- [ ] notion-summary-generator not yet added to vault skills folder (only in MCP mirror)

### Carried Forward (from previous sessions)

- [ ] NotebookLM: nlm setup add claude-code - pending investigation
- [ ] Create 3 NLM notebooks: Inner Circle Webinars, Plaza Group Webinars, AI for Investing Webinars
- [ ] radar_extractor.py --backfill --dry-run then --backfill
- [ ] Check Oct + Nov 2024 IC Webinar PDFs manually
- [ ] April 2025 IC Webinar - check manually for company slides
- [ ] CEDRIC Skills Index Cowork column - test and update

_Session paused 2026-04-18 ~14:33 BST - to resume later today or Sunday_

---

## Session: 2026-04-28 (Tuesday afternoon/evening - Part 3)

_Session started: ~16:30 BST_
_Environment: Cowork (Claude Desktop) - Dex vault mounted_

### Context at Session Start

- Picked up from earlier sessions via PICKUP_POINT.md and CEDRIC_MEMORY.md transfer notes.
- Pipeline confirmed stable at v1.0-webinar-ready. Post-webinar dev branch active.
- Mick requested: (1) pipeline walkthrough document for webinar, (2) skill to wrap the pipeline, (3) slash command.

### Actions Taken This Session

1. **Pipeline Walkthrough Document created**
   - File: `C:\Vaults\Cowork\2026.04.28 - ShareScope Pipeline Walkthrough.docx`
   - Three sections: v1.0 two-command workflow (with tech stack tables), voice-activated branch walkthrough (8 steps, new tech additions), Plan B recording guide (checklist + narration script).
   - Built with docx-js via Node.js.

2. **sharescope-nlm-research skill - BUILT and DUAL-DEPLOYED**
   - Replaces old `stock-research` skill (archived to `skills/_deprecated/stock-research/`).
   - SKILL.md covers: ticker/company resolution (Research Log lookup), pre-flight checks (NLM auth, existing notebook), orchestrator step with CSV verification, NLM researcher step with report monitoring, wrap-up with optional Notion logging. Troubleshooting table included.
   - Vault master: `Dex-MickP/skills/sharescope-nlm-research/SKILL.md`
   - MCP mirror: `Dex-MickP/.claude/skills/sharescope-nlm-research/SKILL.md`
   - Both copies verified identical (diff clean).

3. **`/research` slash command created**
   - File: `04-Projects/2026.04.04-ShareScope-Automation/.claude/commands/research.md`
   - In Claude Code: `/research [TICKER]` or `/research [company name]` triggers the full pipeline skill.
   - Supports partial names (e.g. `/research Halliburton` or `/research HAL`).

4. **Skills register (README.md) updated**
   - `sharescope-nlm-research` row added. `stock-research` row removed.

5. **Memory files, session log, and Notion updated** (this entry).

### Skill Plan discussed (Phase 2 - deferred post-webinar)

- Phase 2: generalised member-distributable version with configurable paths, setup wizard, GitHub repo, .skill packaging.
- Decision: build Phase 1 first, prove in production, then generalise.

### Current Status (session end)

- Webinar tomorrow: pipeline frozen at v1.0-webinar-ready. All four demo companies confirmed (SQZ, GGP, ACMR, HAL).
- `sharescope-nlm-research` skill live and accessible in Cowork.
- `/research` slash command ready in Claude Code project folder.
- Plan B recording deferred to Wednesday morning pre-webinar.

---

## 2026.05.04 - Monday - Building Poppy (Personal Assistant Project)

### Context

Mick wants a second AI assistant to handle inbox/diary work. Distinct role from Cedric (heavy local lifting) and Annie (calendar specialist). Will live in claude.ai Project (accessible from web and mobile), not Claude Desktop. Naming: Poppy.

Mick also flagged this build as the next Meet Cedric episode (or two-parter), pivoting the series from share research automation into second-brain/PA territory. Recording everything from this session for production.

### What was decided this session

**Email triage (primary job)**
- 12 categories agreed: Urgent / Needs Reply, YT Source, Stock Alert, DIY Members, Reading / Research, Newsletters, Household, DBox, H Group, Accountant, Personal, Junk?
- DBox (capital D, capital B) - voice-to-text correction noted
- Backfill: 7 days on first run
- Gmail labels nested under `Poppy/` prefix

**YT Source handling**
- Detection signature confirmed from Mick's screenshot: from:me + subject "Watch ... on YouTube" + body has YT URL + instruction phrase
- Notion DB name: `YT References` (top-level, not under Poppy - cross-cutting use)
- Schema approved: Title, URL, Instructions (multi-line accumulating), Intended Use (multi-select), Date First Received, Last Mention, Status, Channel, Duration
- Status values: New / Reviewing / Processed / Discarded
- Duplicate handling: append new instructions to existing row, update Last Mention, do not duplicate row

**Self-improvement loop**
- Rulebook.md as single source of rules (vault master + Drive copy that Poppy reads)
- Five sections: Abbreviations, Sorting Rules, Trusted Senders, Never Touch, Style Guardrails
- Rule suggestions appear in morning digest only, Mick approves/declines
- Decision: Drive sync via manual copy for v1

**Cadence**
- Three digests: 07:00 (full), 13:00 (urgent + new YT only), 17:00 (wrap-up)
- Delivery: Slack DM primary (mobile ping via app) + Notion archive (`Poppy's Daily Digests` database)
- n8n + Telegram flagged as future enhancement (Mick has prior n8n experience)
- Scheduling reality acknowledged: Projects don't run on cron; v1 = calendar reminders trigger manual open. v2 = n8n flow.

**Boundaries**
- Hard rule: Poppy NEVER sends, accepts, declines, or deletes without explicit Mick confirmation
- Never Touch list seeded with Debs and Leo (any address) - emails to be confirmed
- Privacy: summaries only in digests, verbatim only for Urgent items

**Tone & style**
- Address Mick as "Mick"
- Calibrated tone: matches Mick's prompt length and register
- UK English, simple English, no Americanisms
- Plain ASCII, no em dashes, no smart quotes, no ellipsis

**Memory architecture**
- Notion database `Poppy Memory` (not single page, per Mick's preference)
- Tags: Type (Pending Draft / Reminder / Decision / Active Thread / Rule Suggestion / Other) + Status (Active / Pending / Archive)
- Auto-archive rules built in (drafts on send, reminders on deadline+1, decisions after 30 days)
- PAIDA hub created in Notion as parent: Cedric and Poppy as siblings underneath. Existing Memory Vault and Knowledge Base move under Cedric.

### What was produced

1. **CLAUDE.md** (Poppy project instructions) - 16 sections, ASCII-clean
2. **Poppy-Settings-and-Connectors.md** - companion setup guide

Both delivered to Mick via outputs folder.

### Where Mick is now

Part-way through reading the Settings doc. Asked Cedric where to create the supporting files (Rulebook.md, Poppy-Reference.md, PAIDA-Architecture.md).

Cedric recommended: new vault folder `C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\Poppy\`, edited via Cursor as a workspace. Drive sync needed for Rulebook.md only.

Mick wrapping up session at 20:44 BST. Will continue tomorrow or day after.

### Outstanding for next session

See `PICKUP_NOTE_2026.05.04-Poppy.md` in vault root.

# CEDRIC MEMORY
**Last Updated:** 2026.06.30 (Tue evening, Cowork) - Set up the PROMPT LIBRARY single-source-of-truth in Dex (new 06-Resources\Prompts\: README, _Prompt-Template schema, 00-Index, Prompts.base). Schema aligned 1:1 with PROMPT_LIBRARY.md via shared `code` key. Also FIXED Git: pushed a 7-commit backlog to GitHub and edited daily_git_commit.py so it self-heals (pushes whenever local is ahead, even on no-change days) and logs to _git-commit.log; enabled Task Scheduler history. STILL TO DO: migrate 141 prompt .md files from Mick's Vault (pilot batch agreed). Full detail: PICKUP_NOTE_2026.06.30-Prompt-Library-Migration.md (Dex root).
**Prior update:** 2026.06.03 (Wed late morning) - Skill dual-write AUDIT across all three locations (Mirror /mnt/skills/user, PRIMARY C:\Vaults\Mick's Vault\.claude\skills, DEX skills). Heavy drift found: of 12 skills in 2+ places only 2 byte-identical. Fixed 3 in the mirror (image-cta-overlay v2.2; annie - fixed DEAD tool names; pdf-to-pptx-converter v1.1). Rest PAUSED for after tonight's webinar. FULL DETAIL + remaining work in PICKUP_NOTE_2026.06.03-Skill-Audit.md (Dex root). Key realisation: canonical model is ALREADY documented (Dex + mirror) but migration onto it is only partial, AND the four 2026.05.30-migrated skills are now MISSING from this project's mirror (mirror may be project-scoped or resetting).
**Earlier update:** 2026.06.01 (Mon afternoon) - Added two Key Conventions: (1) AI report template location + the new Sector_Screen_Report type, (2) mandatory Aptos 12pt default for all .docx body text. Created Sector_Screen_Report/ template folder (README + worked example: US Precious Metal Miners quarterly growth + performance/valuation overlay, 5 tables + 3 quadrant charts). CHANGELOG in AI_Report_Templates updated. MCSB Phase 1 Session 6 remains the active project pickup (see Top of Mind below).
**Older update:** 2026.05.30 (Sat afternoon) - Migrated Poster Pete's four end-of-month skills (portfolio-post-creator v2.2, benchmark-fetcher v1.0, wordpress-image-uploader v1.0, wordpress-post-publisher v1.1) from C-Pete into the Dex vault (V) + /mnt/skills/user mirror (M), both verified byte-identical; in-file path headers fixed; registry updated (CLAUDE.md, skills/README.md, SKILLS_REGISTRY.md); .env stays single-source in Mick's Vault by Mick's decision; originals left in place. MCSB Phase 1 Session 6 is still the active project pickup (see Top of Mind below).
**Environment:** Claude Desktop (Filesystem MCP confirmed) - this session. (Prior sessions: Cowork.)

---

## Recent session: 2026.06.30 (Tuesday evening, Cowork) - Prompt Library single-source-of-truth + Git fix

Mick asked where to store his prompt markdown notes (currently a dumping ground in Mick's
Vault) so they live in ONE place and are GitHub-backed. Agreed model: MOVE (not copy) them
into Dex-MickP\06-Resources\Prompts\ as the human-friendly SOURCE; keep PROMPT_LIBRARY.md
(C:\Vaults\Cowork) as the single OPERATIONAL file AHK + demos read.

### Built this session (scaffolding only - 141-file migration NOT started)
- 06-Resources\Prompts\README.md, _Prompt-Template.md, 00-Index.md, Prompts.base.
- Frontmatter schema aligned 1:1 with PROMPT_LIBRARY.md, linked by a shared `code` (CAT-NN).
  Fields: title, code, category (NBLM INV SUM CON ANL COM WEB GEN), ahk, version,
  date_created, date_updated, status, operational, tags (always starts with `prompt`).

### Git automation detour (now fixed)
- Repo had 7 local commits never pushed to GitHub. Pushed them (now in sync).
- Cause = holiday 12-24 June (PC off) + a logic gap (daily script skipped the push on
  no-change days) + scheduled push failing on commit days.
- Edited daily_git_commit.py: pushes whenever local is ahead (self-heals backlog), logs to
  _git-commit.log. Verified py_compile on Mick's PC. Enabled Task Scheduler history.
- LESSON: do NOT run git from the Cowork sandbox on this mount - it left a stale
  .git\index.lock that the sandbox could not remove (Mick deleted it on Windows). Sandbox
  also reads half-synced (truncated) copies of files on the cloud drive - trust the host
  Read tool, not bash, for file integrity on C:\Vaults.

### Still open (the actual job)
- Migrate 141 prompt .md files from Mick's Vault (131 in 0.0 - Inbox, 9 in Projects, 1
  template). Pilot ONE group first (NBLM or Perplexity), normalise frontmatter, dedupe
  near-identicals (flag before deleting), regenerate 00-Index.md, confirm Base in Obsidian.
- READ TO RESUME: PICKUP_NOTE_2026.06.30-Prompt-Library-Migration.md (Dex root).

---

## Recent session: 2026.06.03 (Wednesday late morning) - Skill dual-write audit (PAUSED for webinar)

Started with a routine task (add red "Click here for Report" CTA to a Coeur Mining CDE
report image via image-cta-overlay). Noticed the mirror copy of image-cta-overlay was a
STALE v1 (fixed 52px font, overflow bug) vs the correct v2.2 in PRIMARY. Synced it, then
ran a FULL audit of every skill across the three locations.

### Locations and headline
- MIRROR  /mnt/skills/user/                                 21 skills
- PRIMARY C:\Vaults\Mick's Vault\.claude\skills\            20 skills
- DEX     C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\  28 skills
Of the 12 skills that live in 2+ locations, only 2 were byte-identical
(yt-play-button-overlay; image-cta-overlay after today's fix).

### Fixed and VERIFIED this session (mirror writes only)
- image-cta-overlay: Mirror <- PRIMARY v2.2 (md5 6f5e4c5f).
- annie: Mirror <- PRIMARY (md5 9f133960). Fixed a FUNCTIONAL BUG - mirror used dead
  tool names (list_gcal_events, find_free_time); now Google Calendar:gcal_list_events etc.
- pdf-to-pptx-converter: Mirror <- DEX v1.1 (md5 fff2a7a3).
WARNING: these are mirror-only writes, not version-controlled. If the mirror resets they
are lost again.

### Important reconciliation with existing memory
- The "Mandatory Skill Deployment Protocol" already mandates DEX (master) + mirror, and
  SKILLS_REGISTRY.md is the declared source of truth. So the canonical model is NOT an
  open question - it is Dex + mirror.
- BUT in practice PRIMARY is still the live source for annie + image-cta-overlay, so the
  model is only partially realised on disk.
- The four skills migrated to Dex+mirror on 2026.05.30 are NOT in this project's mirror
  now. Either the mirror is project-scoped (that work was in the Poster Pete project) or
  it reset. This must be clarified before the mirror can be trusted as half the pair.

### Still open (deferred to after tonight's webinar)
- Re-establish the four migrated skills in the mirror from Dex; retire stale PRIMARY strays.
- Decide annie + image-cta-overlay home (migrate to Dex, or sanction PRIMARY as 2nd master).
- session-start FORK: PRIMARY v1.1 (correct) vs DEX (no frontmatter, OLD tool_search probe
  for env detection - contradicts the current Filesystem:list_allowed_directories protocol).
  Drop the Dex method.
- ai4inv-webinar-processor and notion-summary: parallel edits, manual pick needed.
- notion-summary vs notion-summary-generator namespace overlap to clarify.
- 15 mirror-only skills have NO disk backup anywhere - backup policy decision.

### Deliverables written
- Pickup note (comprehensive): PICKUP_NOTE_2026.06.03-Skill-Audit.md (Dex root) - READ THIS to resume.
- Full report: /mnt/user-data/outputs/2026.06.03 - Skill Dual-Write Audit.md (Mick downloaded).

### Resume phrase
"Cedric, I'm back. Let's pick up the skill dual-write audit from the pickup note."

---

## Recent session: 2026.06.01 (Monday) - AI report template library extended + Aptos font rule

Set up a reusable reference for sector-wide screening reports and locked in a font standard.
- New template type: `06-Resources/AI_Report_Templates/Sector_Screen_Report/` created
  alongside the existing `Research_Brief/`. Purpose: multi-company sector screens / rankings
  (landscape), distinct from the single-company portrait Research Brief.
- Worked example saved there by Mick: `PM_Miners_Quarterly_Growth_Consolidated.docx` - US
  Precious Metal Miners (63-stock ShareScope universe) quarterly growth report. 5 tables
  (OCF Top 10, turnover Top 10, full 23-name ranking, performance overlay, valuation overlay)
  + 3 matplotlib quadrant charts (turnover vs YTD price; turnover vs forecast PE; turnover
  vs PSR). 12 pages, landscape, Aptos 12pt.
- `Sector_Screen_Report/README.md` written: structure, house style (hex codes), methodology
  (sequential QoQ turnover, de-cumulation, SEC-XBRL-plus-web-research for foreign filers,
  state-exclusions-never-estimate), and build approach (docx-js + matplotlib).
- `AI_Report_Templates/CHANGELOG.md` updated with a 2026-06-01 entry.
- New standing style rule recorded: all .docx default to Aptos 12pt body (see Key Conventions).
- Key analytical finding from the example worth recalling: sequential turnover growth had
  near-zero correlation with YTD share-price performance (Pearson r approx 0.02) - the
  turnover ranking is an operational-momentum / candidate-generation tool, not a price-timing
  signal. The dual-metric names (Coeur, Kinross, Agnico) screened most internally consistent.

---

## Recent session: 2026.05.30 (Saturday) - End-of-month skills migrated to Dex vault

Migrated the four DIY Investors end-of-month portfolio skills from the Poster Pete
(C-Pete) claude.ai project into the Dex vault + mirror:
- Skills: portfolio-post-creator v2.2, benchmark-fetcher v1.0,
  wordpress-image-uploader v1.0, wordpress-post-publisher v1.1.
- Dual-registered V + M (verified byte-identical). In-file path headers fixed to Dex paths.
- Registry updated: CLAUDE.md, skills/README.md, SKILLS_REGISTRY.md (Section 1b -> 1a,
  portfolio-post-creator v2.0 -> v2.2, Pending Action #1 closed).
- Credentials: .env stays single-source in C:\Vaults\Mick's Vault\.env (Mick's decision -
  not duplicated to Dex, avoids drift when passwords change). WordPress skills point there.
- Originals left in C:\Vaults\Mick's Vault\.claude\skills\ for now (not deleted).
- CHANGELOG.md left as a pure Cedric Server CODE / SemVer log (Mick's decision 2026-05-30); this housekeeping recorded in this memory, the session log, and SKILLS_REGISTRY.
Full detail: System/session_log.md (2026-05-30 entry).
[2026.06.03 note: portfolio-post-creator is now v2.3 and wordpress-post-publisher v1.2 in
Dex (2026.05.30 tag rules); and these four are not visible in this project's mirror - see
the 2026.06.03 audit entry above.]

---

## Top of Mind - 2026.05.17 (Sunday)

### MCSB (Mick and Cedric Shared Brain) -- PHASE 1 IN PROGRESS
**Status:** Phases 1.1, 1.2, 1.3a-1.3g all COMPLETE and PROD-confirmed. Server at v0.4.0. Phase 1.3 (Cedric Server v0.1 series) is now FULLY COMPLETE. Phase 1 first publish to GitHub also done (16 files in milestone commit 2026-05-17 14:35 London). Next: Phase 1.4 (mostly done already, just needs ratification) + Phase 1.5 (MCP wrapper v0.1).
**PRD v0.3:** `PAIDA Master - Second Brain/04-Projects/2026.05.09 - MCSB/2026.05.13-MCSB-PRD_V0.3.docx` (includes D26)
**Pickup note:** `2026.05.17-MCSB-Phase1-Session5-Pickup-Note.md` in same folder -- READ THIS to resume
**Resume phrase:** "Cedric, I'm back. Session 6 -- let's confirm the autonomous tick fired since Session 5, then move to Phase 1.5 (MCP wrapper v0.1)."

**Build Tracker (Notion):** https://www.notion.so/b2462f490c7448cf8af9b51e91f1d159
**PROGRESS.md:** PAIDA Master - Second Brain/04-Projects/2026.05.09 - MCSB/PROGRESS.md
**Rule:** Both trackers updated together at end of every session / context refresh.

**Completed this session (2026.05.17 Session 5 -- afternoon):**
- cedric_server.py rewritten to v0.4.0 (22,017 -> 34,244 bytes): embedded the hourly worker as a FastAPI background scheduler task. Closes Phase 1.3g and seals the Cedric Server v0.1 series.
- APScheduler (AsyncIOScheduler) drives an hourly tick from inside the server, replacing the Windows Task Scheduler dependency.
- threading.Lock around each tick: non-blocking acquire so a slow tick can never overlap with the next; second call is recorded as status=skipped rather than queued.
- New endpoints (both PC-only via require_pc_token):
    GET  /worker/status   -- enabled / scheduler_started / lock_held / next_run / counts / last_run / last_skip / last_error
    POST /worker/run_now  -- manual trigger; optional ?dry_run=true override
- /health enriched with a worker block (next_run, lock_held, counts, last_run_summary).
- Clean @app.on_event("shutdown") hook so Ctrl+C exits the scheduler cleanly.
- Worker shim added (cedric_worker.py +1,401 bytes): run_worker_pipeline(dry_run, verbose) -- CLI-independent entry point. main() is now a 4-line CLI wrapper around it; CLI behaviour unchanged.
- Env vars: CEDRIC_WORKER_ENABLED / CEDRIC_WORKER_INTERVAL_MIN / CEDRIC_WORKER_DRY_RUN (sensible defaults).
- Sandbox tests: 25/25 paths green.
- PROD walkthrough (13:43-14:35 London on Mick's PC): every endpoint proven, scheduler started with first auto-tick scheduled, dry-run and real-run ticks both fired through, MCSB Phase 1 published to GitHub for the first time (16 files in milestone commit).
- Mid-walk hygiene: __pycache__/ added to .gitignore (line 94, confirmed by git check-ignore).
- Bug arc: stale .git/index.lock from old Task Scheduler racing first real tick. Recovered by Admin PowerShell + lock removal. Saved as the new "scheduler handover" feedback memory (always disable old driver BEFORE first real tick).
- Tooling note: Edit-tool apostrophe truncation hit again (Python this time). Memory broadened beyond JS to all languages. Used /tmp Python scripts as the apostrophe-safe alternative.

**Token env-var contract (locked Session 3):**
- MCSB_PC_TOKEN: full access including private + /search_all
- MCSB_MOBILE_TOKEN: restricted, no private, no /search_all
- Both live in C:\Users\pavey\.env -- NEVER copy elsewhere
- Mint with: `python generate_tokens.py` (helper in vault root)

**Pre-flight for next session: NONE.**
Server v0.4.0 is prod-installed and running with embedded scheduler. apscheduler dep installed. Old Windows Task Scheduler "Cedric Hourly Worker" job is DISABLED (still present, will be DELETED in Session 6 after one observation cycle). __pycache__/ now properly excluded from git. Phase 1 is on GitHub.

**Important: SECURITY ROTATION pending.**
The two tokens minted Session 3 were pasted into chat during the
walkthrough. Practical risk = zero today (server is 127.0.0.1 only),
but BEFORE the Cloudflare tunnel goes up, Mick must:
  cd C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP
  python generate_tokens.py
and swap the new tokens into .env. Flag this when tunnel work begins.

**Outstanding / Deferred:**
- Session 6 priorities: (1) confirm autonomous tick fired (tick_count > 3 with trigger=scheduler somewhere), (2) DELETE the disabled "Cedric Hourly Worker" Task Scheduler job via Admin PowerShell.
- Minor patch: surface git push failures as error_count++ rather than swallowing as pushed=False.
- Lifespan refactor (cedric_server uses deprecated @app.on_event; FastAPI 0.110+ prefers lifespan context manager). ~5 min, low priority.
- Windows service install for Cedric Server (still foreground dev mode).
- Token rotation before Cloudflare tunnel work.

**Meet Cedric episode arc:**
- Episode A: The 46-page PRD review (Content Studio logged 2026.05.13)
- Episode B: Building the Build Tracker (Content Studio logged 2026.05.13)
- Episode C: Building the Foundation -- vault restructure + hourly worker (Content Studio logged 2026.05.14)
- Episode D: The Server Awakens -- first endpoint live + final PRD decision logged (Content Studio logged 2026.05.15)
- Episode E: First Capture -- /memory/note plus two-tier bearer auth (Content Studio logged 2026.05.15 Session 3)
- Episode F: Cedric Catches His Own Bug -- 1.3d /agents/reload sandbox save (Content Studio logged 2026.05.17 Session 4). Bonus B-segment: PowerShell apostrophe quoting gotcha hit during PROD walkthrough.
- Episode G: Cedric Catches Phase 1 Crashing Lock-File Bug -- 1.3g handover race condition (Content Studio logged 2026.05.17 Session 5). Hero arc: deploying embedded scheduler raced the old Task Scheduler over .git/index.lock; teaches "disable old driver BEFORE first real tick". Bonus: milestone first publish of MCSB Phase 1 to GitHub.

### Subscription audit follow-ups (from 12 May afternoon session)
- Cancel Codia AI before 21 May (USD 20/month)
- Verify usage / decide on Synthesia (£201.60/yr renews 25 Nov), Ideogram ($180/yr renews 2 Sep), Text Blaze ($35.88/yr renews 18 Aug)
- Cancel Alex McFarland "AI Writing Systems" Substack before 18 May (£16/month - not actually cancelled despite earlier belief)
- Investigate hosting subs: Network Solutions (expired service notice 18 Apr), Bluehost, 123-reg, iPage
- ChatGPT Plus cancelled today, paid through to ~9 June - use it during the paid window
- Otter.ai Pro retained (Zoom auto-join workflow justifies it)
- OpenAI API billing plan cancelled 16 April (confirmed via platform.openai.com screenshot)

---

## SKILLS - SOURCE OF TRUTH

For any question about what skills exist, where they live, who built them, or how to invoke them, the canonical reference is:

  C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\SKILLS_REGISTRY.md

This file lists every skill across vault, mirror, plugin marketplace, scheduled tasks, and claude.ai PAIDA Projects (Pete, Cedric, Poppy). Update on every skill create / rename / version-bump / deprecate. See its Section 7 for maintenance rules.

[2026.06.03: A full audit found the on-disk reality has drifted from this registry's
intent - see the 2026.06.03 session entry and PICKUP_NOTE_2026.06.03-Skill-Audit.md.
Re-reconcile SKILLS_REGISTRY.md against all three locations when the audit resumes.]

---

## Session Log - 2026.05.17 Afternoon (MCSB Phase 1 Session 5 - 1.3g CLOSED, Phase 1.3 SERIES COMPLETE)

### What we did
- Built Cedric Server v0.4.0 (cedric_server.py 22,017 -> 34,244 bytes): embedded the hourly worker as a FastAPI background scheduler task. Closes Phase 1.3g and seals the Cedric Server v0.1 series.
- APScheduler (AsyncIOScheduler) drives an hourly tick from inside the server. threading.Lock guards re-entry (skipped, never queued). Two new PC-only endpoints: GET /worker/status, POST /worker/run_now. /health enriched with a worker block. Clean shutdown hook.
- Worker shim added: cedric_worker.run_worker_pipeline() is the CLI-independent entry point; main() is now a thin CLI wrapper. CLI behaviour unchanged.
- Env-var config: CEDRIC_WORKER_ENABLED / CEDRIC_WORKER_INTERVAL_MIN / CEDRIC_WORKER_DRY_RUN.
- Sandbox tests: 25/25 paths green (auth matrices on both new endpoints, dry-run tick, lock contention, regression on /memory/note and /agents/reload).

### PROD walkthrough (13:43-14:35 London, on Mick's PC)
- pip install apscheduler -> 3.11.2 clean.
- Server v0.4.0 booted with the new "embedded worker scheduler started (every 60 min, dry_run=False)" message.
- /health returned v0.4.0 + worker block populated + next_run 14:43:51.
- Auth matrix proven on both new endpoints (401/403/200).
- Dry-run tick completed -> tick_count=1, last_run populated.
- Mid-walk: noticed __pycache__/ untracked. Added to .gitignore via Add-Content. Line 94 confirmed by git check-ignore. Status dropped from 17 to 16 files.
- Real-run tick attempt 1: completed but pushed=False. Window A revealed "fatal: Unable to create '.git/index.lock': File exists." -- old Task Scheduler had raced our test (still enabled).
- Disabled Task Scheduler via Admin PowerShell (user mode denied). Removed lock file. Retry -> pushed=True, 14:35:09-14:35:12 (3 sec).
- MCSB Phase 1 published to GitHub for the first time (16 files in milestone commit).
- Final /worker/status: tick_count=3, last_run.git_pushed=true.

### Design decisions logged this session
- DEC-S5-01: APScheduler chosen over hand-rolled asyncio loop. Reason: scales cleanly when Phase 5 adds /briefing/today and Phase 6 adds theme-mining cadence; tiny dep; battle-tested.
- DEC-S5-02: First tick offset by WORKER_INTERVAL_MIN (no boot tick). Matches prior Task Scheduler behaviour and keeps the startup hook cheap.

### Lesson saved as feedback memory
- Scheduler handover rule: when moving a scheduled job from one driver to another, ALWAYS disable the old driver BEFORE the first real-run tick of the new one. The dry-run path won't catch this because it skips git add. (Saved as feedback_scheduler_handover.md in Cedric's auto-memory.)

### Files changed in vault this session
- cedric_server.py (v0.3.0 -> v0.4.0)
- cedric_worker.py (+ run_worker_pipeline shim, 16,451 bytes)
- CHANGELOG.md (v0.4.0 entry added at top, D25 format)
- .gitignore (+ __pycache__/ exclusion at line 94)
- PAIDA Master/04-Projects/2026.05.09 - MCSB/PROGRESS.md (Session 5 entry, 1.3g [x], header date/status)
- PAIDA Master/04-Projects/2026.05.09 - MCSB/2026.05.17-MCSB-Phase1-Session5-Pickup-Note.md (new)
- GitHub remote: first push of MCSB Phase 1 (16 files in milestone commit).

### Notion Content Studio
- New page: "2026.05.17 - Cedric Catches Phase 1 Crashing Lock-File Bug". Project: Meet Cedric. Format: Video. Status: Brain Dump. Hero arc + teachable rule + first-publish-to-GitHub bonus.

### Outstanding / next session
- Confirm autonomous tick fired (check tick_count > 3 with a trigger=scheduler entry in history).
- DELETE the disabled "Cedric Hourly Worker" Task Scheduler job via Admin PowerShell.
- Minor: surface git push failures as error_count++ rather than swallowing as pushed=False.
- Lifespan refactor (deprecated @app.on_event -> FastAPI 0.110+ lifespan context manager).
- Still deferred: Windows service install, token rotation before Cloudflare tunnel work.

### Resume phrase
"Cedric, I'm back. Session 6 -- let's confirm the autonomous tick fired since Session 5, then move to Phase 1.5 (MCP wrapper v0.1)."

---

## Session Log - 2026.05.17 Morning (MCSB Phase 1 Session 4 - 1.3d and 1.3e CLOSED)

### What we did
- Reviewed PROGRESS.md and the relevant PRD sections (Appendix B for the /agents/reload spec, sections 8.6 + 11.2 for agents.md and the hourly worker, section 20 for the phased plan).
- Built Cedric Server v0.3.0 (cedric_server.py 12,967 -> 22,017 bytes).
  - GET /agents/reload endpoint per PRD Appendix B, PC-token only (mobile token returns 403).
  - require_pc_token FastAPI dependency -- closes off 1.3e and provides a reusable PC-only auth tier for later /search_all and /briefing/today.
  - agents.md loader: parses frontmatter version, counts top-level rule blocks, hashes content for drift detection.
  - @app.on_event("startup") hook loads agents.md once on boot and writes a baseline snapshot.
  - Snapshot system: writes a versioned copy to agents.md-history/ on every content change, with filenames including seconds and a 6-char content hash so same-minute reloads do not collide. Auto-appends to agents.md-history/CHANGELOG.md (newest first).
  - Drift detection: when content changes but the frontmatter version does NOT, response sets content_drift: true and the CHANGELOG entry is tagged "(content drift -- version not bumped)".
  - /health enriched with an agents block (version, rules_loaded, loaded_at, snapshot_count).
- Sandbox tests: 18/18 paths green.
- Real bug caught by the sandbox: snapshot filenames using minute-level timestamps collided when two reloads happened in the same minute. Fixed by adding seconds + 6-char hash. Sandbox proved 6 rapid reloads now produce 6 unique files. This is the Meet Cedric Episode F hero arc.

### PROD walkthrough (10:48-11:05 London, on Mick's PC)
- Stumble at Step 2: unquoted vault path triggered PowerShell continuation prompt because of the apostrophe in "Mick's-Dex-2nd-Brain". Recovered with Ctrl+C + retry with the path in double quotes. New feedback memory saved so this never recurs.
- /health: confirmed v0.3.0, agents v1.0, 3 rules, baseline snapshot_count 1, both tokens configured.
- /agents/reload with PC token -> 200 + correct PRD-spec JSON, snapshot_written false (idempotent -- no content change since startup).
- /agents/reload with mobile token -> 403, detail "PC token required for this endpoint." 1.3e PROVEN in PROD.
- Cedric appended a 3-line test comment to agents.md (no version bump). Mick hit reload -> content_drift: true, snapshot_written: true, agents_version still 1.0. Two real snapshot files now in agents.md-history/. CHANGELOG auto-entry appeared at the top with the drift marker. Cedric reverted agents.md silently to its 1822-byte baseline.
- Server stopped cleanly with Ctrl+C and Y.

### Files changed in vault this session
- cedric_server.py (v0.2.0 -> v0.3.0)
- CHANGELOG.md (v0.3.0 entry added at top, D25 format)
- agents.md-history/CHANGELOG.md (2 new auto-entries: server-startup + manual-reload with drift marker)
- agents.md-history/agents-v1.0-2026.05.17T104843-c40c6f.md (baseline snapshot, retained as PROD evidence)
- agents.md-history/agents-v1.0-2026.05.17T105856-08a5a2.md (drift-edit snapshot, retained as PROD evidence)
- PAIDA Master/04-Projects/2026.05.09 - MCSB/PROGRESS.md (Session 4 entry, 1.3d [x], 1.3e [x], header date/status)
- PAIDA Master/04-Projects/2026.05.09 - MCSB/2026.05.17-MCSB-Phase1-Session4-Pickup-Note.md (new)

### Notion Content Studio
- New page: "2026.05.17 - Cedric Catches His Own Bug (1.3d Sandbox Save)". Project: Meet Cedric. Format: Video. Status: Brain Dump. Includes PROD success postscript and the apostrophe B-segment angle.

### Outstanding / next session
- Phase 1.3g: embed cedric_worker.py as a FastAPI background scheduler task inside the server (replaces the Windows Task Scheduler dependency). After 1.3g, the Cedric Server v0.1 series is fully complete.
- Then Phase 1.4 (agents.md framework finalisation), 1.5 (MCP wrapper v0.1), 1.6 (mobile sync), 1.7 (CLAUDE.md core + fragments + assembly script), 1.8 (private-content audit).
- Still deferred: Windows service install, token rotation before Cloudflare tunnel work.

### Resume phrase
"Cedric, I'm back. Let's continue Phase 1 -- ready for 1.3g (embed cedric_worker.py as a background scheduler task inside the server)."

---

## Session Log - 2026.05.13 Afternoon (MCSB PRD Review + v0.3 Production)

### MCSB PRD v0.3 approved. 46-page editorial review completed. Phase 1 ready.
**Session time:** ~16:00-17:30 BST (Wednesday afternoon, Cowork mode)
**Surfaces used:** Cowork, python-docx via bash sandbox

### What was done
- Picked up PRD v0.2.2_1 (Mick uploaded docx, 957 paragraphs)
- Worked through all 46 pages of Mick's markup in page-by-page passes
- Produced four intermediate versions: V0.2.2_2 (p.30), V0.2.2_3 (pp.31-36), V0.2.2_4 (pp.37-46)
- Key content changes: channel URLs added, website tier subfolders (Inner-Circle/Plaza, Free/Silver), Newsletters plural with subfolders, Events folder, Portico course, Case-Studies, CRM Address field, ax-trees global skills note, OQ6/7/12/14 resolved, D24-D25 added
- Produced PRD v0.3 (1,136 paragraphs): version bumped, Appendix A (folder schema ~80 lines) and Appendix B (API reference ~90 lines) written from scratch, Document History updated
- Phase 1 pickup note written: 2026.05.13-MCSB-Phase1-Pickup-Note.md
- Cedric memory (project_mcsb.md) updated to reflect Phase 1 ready status
- Two Meet Cedric episode brain dumps logged to Notion Content Studio
- Notion MCSB Build Tracker discussion begun; Option 3 agreed (Notion + PROGRESS.md)

### Decisions made this session
- D24: Notion bridge-not-migrate (Research DB, Companies Covered, Memory Vault stay in Notion)
- D25: Cedric Server CHANGELOG.md required
- OQ6 resolved: Backblaze B2 accepted
- OQ7 resolved: Obsidian Core Daily Notes; blank note deletion by hourly worker
- OQ12 resolved: agents.md-history/ + CHANGELOG.md
- OQ14 resolved: Notion permanent coexistence confirmed

### Outstanding / next session
- Create MCSB Build Tracker Notion database
- Create vault PROGRESS.md template
- Then: Phase 1 build (next separate session)

---

## Session Log - 2026.05.12 Evening (GitHub Backup Pipeline Diagnosis + Fix)

### Backup pipeline broken for 14 days. Diagnosed, fixed, push verified.
**Session time:** ~18:25-19:10 BST (Tuesday evening, Cowork mode)
**Trigger:** Mick asked "are the git commits actually being pushed to GitHub? Are our backups secure?"
**Answer (initially): NO - last commit was 28 April 2026, 14 days ago.**

### What was wrong
1. Stale `.git/index.lock` left over from a crashed git process c.28 April.
   Every subsequent `git add` since had been failing instantly with
   "Unable to create index.lock: File exists". The daily script silently
   bailed on this for two weeks.
2. Once Mick removed the lock, the pre-commit hook then correctly blocked
   the commit due to 21 .md files containing Unicode typographic chars
   (em dashes, smart quotes, ellipsis, box-drawing chars). Hook reads
   bytes not chars so its "Euro sign" / "Right double quote" labels are
   misleading - actual chars were U+2014 em dash, U+201C/D smart quotes,
   U+2013 en dash, U+2019 smart apostrophe, U+2500-251C box drawing.

### What was done
- Mick: removed `.git/index.lock` and `.git/objects/maintenance.lock`
- Cedric: wrote Python script to UTF-8-normalise 21 files in place
  (70 chars replaced total, verified clean afterwards)
- Mick: re-ran `python daily_git_commit.py` from vault root
- Result: commit cbf6b82 landed (100 files, 10,622 ins, 973 del)
  Push verified - local HEAD matches `ls-remote` HEAD on GitHub

### Outstanding (captured in pickup note)
1. **Problem 1b - root cause hunt**: how did Unicode typographic chars get
   past the "ASCII only" guardrails into 20 AI-research files and 1
   Poppy pickup note? Suspect: the skill/workflow producing AI Financial
   Analysis reports writes straight to disk without ASCII normalisation.
   Three hardening options documented.
2. **Problem 2 - ShareScope-Automation has no GitHub remote**: separate
   git repo at 04-Projects/2026.04.04-ShareScope-Automation/ has 2 local
   commits, 15 dirty files, NO remote configured. Not backed up anywhere.
   Decision needed from Mick.
3. **Problem 3 - verify Windows Scheduled Task still firing**: even though
   today's commit went through manually, the recurring task may have
   stopped firing. Check Task Scheduler history once Problem 1b is closed.
4. **Housekeeping**: small empty file `.cedric_write_test_2026_05_12.tmp`
   in vault root accidentally caught in tonight's commit (Cedric created
   it for a write-permissions test). `git rm` it tomorrow.
5. **Suggestion**: promote tonight's one-off fix script to a permanent
   vault tool at `tools/fix_typographic_chars.py`.

### Pickup note location
  C:\Vaults\Cowork\2026.05.12 - GitHub Backup Diagnosis - Pickup Note.md

### Lesson for Cedric (relevant to memory)
- ALWAYS investigate stale .git lockfile warnings rather than dismissing
  them as permissions quirks. In the first pass tonight Cedric saw the
  "unable to unlink index.lock" warning from his own `git fetch` and
  misread it as a Linux-mount artefact. It was actually the smoking gun.
  Test, Don't Trust - same principle as the dual-write rule.

---

## Session Log - 2026.05.10 Late-PM (YouTube Script v2 - Edits Applied)

### v2 drafted with 5 edits. All verified, change-highlighted DOCX delivered. Mick reviewing.
**Session time:** ~16:25-17:00 BST (Sunday late afternoon)
**Project:** YouTube content for diy-investors.com channel (@DIY-Investors)
**Status:** v2 complete. Mick has change-highlighted DOCX for second read-through.

**What we did:**
- Picked up cleanly from RESUMPTION-PICKUP-NOTE.md per "Path A" (verbal edits from Mick)
- Five edits requested: 1) COMEX inventory line in Section 4; 2-4) GUIA/INCRA/FUNAI acronym
  expansions in Section 5; 5) sanity check on copper guidance figure in Section 6
- Fact-checked the copper figure via web search across SIX independent sources
  (Coeur press release, MINING.com, SME Mining Engineering, Investing.com, Mugglehead,
  Resource World): 50-65 million pounds is correct. New Afton contributes all of it
  and is fundamentally a copper-gold mine, not a precious metals mine.
- Fact-checked the COMEX silver inventory claim: registered stocks below 100m oz, multi-source
  confirmed including ZeroHedge 1 May 2026. Edit on safe ground.
- Mick chose Option A on the copper clarifier: keep figure, add aside in [ASIDE] brackets
  noting New Afton is a copper-gold mine.
- v2-draft.md written via single Filesystem write (full overwrite, ASCII only)
- v2 DOCX built with v2 changes highlighted in YELLOW for easy comparison vs v1 read-through
- Validation hit a docx-js quirk: highlightCs element fails strict OOXML schema
  (Word opens fine but validator blocks). Fix: post-process the .docx zip, regex-strip
  all <w:highlightCs/> elements, repackage. PASS after fix.
- Final v2 DOCX delivered via /mnt/user-data/outputs/

**CRITICAL LESSON LEARNED THIS SESSION (Mick caught it):**
Cedric stated "copper is measured in pounds (a much smaller unit than ounces)" when
verifying the copper figure. THIS IS WRONG. There are 16 ounces in 1 pound, so a pound
is LARGER than an ounce, not smaller. Mick caught this immediately with "When I went to
School, there were 16oz to 1 pound - so ounces are smaller than pounds!"

The actual reasoning that justifies the figure: 50-65m lbs of copper IS large by weight
(~800m-1bn avoirdupois ounces equivalent), BUT this is correct because New Afton is a
copper-gold mine. By DOLLAR VALUE the mix is balanced: gold ~$3.6bn, silver ~$1.6bn,
copper ~$0.26bn at current prices. So copper is the SMALLEST revenue stream despite being
the largest by weight.

PATTERN TO REMEMBER: when cross-source verification confirms a figure, STOP THERE. Do
not add hand-wavy unit-conversion reasoning post-hoc. The cross-source check is the
verification, not the unit comparison. Adding spurious reasoning to "explain" a verified
figure is how unforced errors creep in.

**Files now on disk:**
- v1 markdown source (preserved): scripts/v1-draft.md
- v1 DOCX (Mick's name): scripts/2026.05.10 - Gold_SRB_n_CDE_YT-Script_v1-draft.docx
- v2 markdown source: scripts/v2-draft.md
- v2 DOCX (suggested filename): 2026.05.10 - Gold_SRB_n_CDE_YT-Script_v2-draft.docx

**Edits applied (all verified):**
1. Section 4: COMEX silver inventory line added after ETF buying point.
   Verified: registered stocks below 100m oz, multi-source confirmed.
2. Section 5: GUIA expanded to "Brazilian environmental installation licence"
3. Section 5: INCRA expanded to "National Institute for Colonisation and Agrarian Reform"
4. Section 5: FUNAI expanded to "National Foundation for Indigenous Peoples"
5. Section 6: copper figure (50-65m lbs) verified across 6 sources. KEPT.
   "New Afton is a copper-gold mine" clarifier added in [ASIDE] brackets per Mick's request.

**Word count v2:** 2,065 spoken words (~14.8 min at 140 wpm).
v1 was 2,004 -> v2 added ~60 words via acronym expansions and COMEX line.

**Validation:** ASCII PASS, voice-guard PASS, all 6 edit checks PASS, DOCX validator PASS
(after highlightCs strip).

**Patterns / lessons logged:**
- DOCX build with change-highlighting: docx-js TextRun supports `highlight: "yellow"`.
  But docx-js emits a non-standard <w:highlightCs/> alongside <w:highlight/> which
  fails strict OOXML schema validation. FIX: post-process the .docx zip, regex-strip
  all <w:highlightCs[^/]*/> elements, repackage. Word opens both versions fine; the
  strip is for validator compliance only.
- Verbal-edit pickup pattern (Path A from RESUMPTION-PICKUP-NOTE) worked well: read v1
  source, apply edits in memory, write v2 to scripts folder, regenerate DOCX with
  highlight-on-changes, present.
- When Mick queries a number that "feels wrong", do a real fact check (web search +
  cross-source) before answering. Don't rely on memory or hand-wave reasoning.
- "Side-note aside" device: use [ASIDE - text] brackets for camera cues that flag
  on-camera commentary distinct from stage directions in [square brackets]. Working
  pattern for this video; could be a voice-DNA addition if Mick uses it again.

**Outstanding (for next session):**
1. Mick reads through v2 DOCX, tracking the yellow-highlighted changes
2. Decision: ship as v1-final, or v3 with more edits
3. If shipping: lock title, regenerate clean DOCX without highlights, update Notion
   Micks Content Studio entry from "In Review" to "Ready"
   (entry id: 35cdb32a-9b0a-8127-b9e9-ed66cb9b2c33)
4. Charts handoff to editor (both JPGs originally at /mnt/user-data/uploads/, may need
   re-uploading or copying into the project folder for permanence)

**Notion update status:**
- Micks Content Studio entry already exists at "In Review" status from earlier today
  (id: 35cdb32a-9b0a-8127-b9e9-ed66cb9b2c33). Did NOT update this session - status
  still accurately reflects state (v2 produced, awaiting Mick's read-through).
- Will move to "Ready" when v2 (or v3) is signed off.

---

## Session Log - 2026.05.10 PM (YouTube Script v1 Drafted - SRB + CDE)

### Script v1 written, voice-DNA validated, DOCX delivered. Mick reviewing offline.
**Session time:** ~11:55-12:25 BST (Sunday afternoon, picked up after morning context refresh)
**Project:** YouTube content for diy-investors.com channel (@DIY-Investors)
**Status:** v1 complete. Mick has DOCX for printed read-through. v2 awaits his edits + title sign-off.
**Outcome:** v2 produced same day - see late-PM entry above.

**What we did:**
- Picked up cleanly from the morning pickup note in fresh context
- Read PICKUP-NOTE-for-fresh-context.md and voice-dna-mick.json end-to-end before drafting
- Sanity-checked the central-thesis numbers in Python: Q1 2026 vs 2025 actual gap is 52.2%
  ("roughly 50%" in the script stays honest); EDV gap is 61%; Q1 drawdown 26.8%
- Drafted v1 in one Filesystem write (full overwrite, ASCII only)
- Validated post-write: ASCII compliance PASS (no em dashes, smart quotes, ellipsis);
  voice-guard pass (no banned guru-speak); spoken word count 2,004 -> ~13-14 min at 140 wpm
- Flagged the length overrun to Mick (target was 8-12 min). Mick chose to keep the depth.
- Built print-friendly DOCX via docx-js + skill: A4, Arial 12pt, 1.5x line spacing,
  section dividers, blue sub-block labels, header + page-of-total-pages footer,
  appendix with title options + pre-record checklist
- Validated DOCX (90 paragraphs, all checks PASS)
- Delivered both files to /mnt/user-data/outputs/ for download
- Mick saved DOCX to vault scripts folder under his preferred filename convention

**Files now on disk:**
- Markdown source (Cedric's authoritative draft):
  C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\05-Areas\YouTube_System\diy-investors.com\YT-Longform\2026-05-10 - Gold Miners Q1 Realised Price Story (SRB+CDE)\scripts\v1-draft.md
- DOCX (Mick's read-through copy):
  C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\05-Areas\YouTube_System\diy-investors.com\YT-Longform\2026-05-10 - Gold Miners Q1 Realised Price Story (SRB+CDE)\scripts\2026.05.10 - Gold_SRB_n_CDE_YT-Script_v1-draft.docx

**Title options put to Mick (still awaiting choice as of late-PM):**
1. Gold's Pulled Back - But Miners Just Banked Record Q1 Prices. Two I'm Watching. (working)
2. Gold Hit $5,602 - But the Miners Are Still Cheap. Two I'm Watching.
3. Spot Gold Says Correction. Miner Earnings Say Re-rating. Two Stocks On My Radar.
4. The Q1 Gold Story Retail Is Missing - SRB and CDE.

**Lessons / patterns logged:**
- Filesystem MCP write_file is text-only -- binary DOCX must go via /mnt/user-data/outputs/
  with present_files. Always tell Mick to download and drop into the vault himself.
- str_replace is Claude-side only. For vault edits, always read full file -> modify in
  memory -> Filesystem:write_file with complete content. (Confirmed again, was already
  in Key Conventions.)
- DOCX skill at /mnt/skills/public/docx/SKILL.md works cleanly with docx-js. Print-friendly
  recipe to remember: A4, Arial 12pt, 1.5x spacing (line: 360), section divider rules
  (paragraph border-bottom), italic-grey stage directions, blue H2 for sub-blocks.
- Voice-DNA validation in Python after writing is now the standard QA step for any
  long-form Mick-voice content. ASCII check + word count + banned-phrase check.

**Notion update status (from PM session):**
- Micks Content Studio entry created during PM session shutdown.
- Entry id: 35cdb32a-9b0a-8127-b9e9-ed66cb9b2c33
- Status: "In Review"
- URL: https://www.notion.so/35cdb32a9b0a8127b9e9ed66cb9b2c33

---

## Session Log - 2026.05.10 AM (YouTube Video Brief: Gold Miners Q1 Realised Price - SRB + CDE)

### YouTube longform video brief built. Pickup note ready for fresh-context script drafting.
**Session time:** ~10:30-12:30 BST (Sunday morning)
**Project:** YouTube content for diy-investors.com channel (@DIY-Investors)
**Status:** Brief complete, voice DNA loaded, pickup note saved. Script draft NOT yet written
(picked up in afternoon session above).

**What we did:**
- Mick asked for two-phase research: trending YouTube investing topics + match against vault content
- Phase 1 vault research: read CEDRIC_MEMORY, YouTube_System config, voice DNA, ICP profile, channel YAML
- Phase 2 web research: ranked top 10 trending investing topics (gold/miner re-rating made the list)
- Confirmed last YouTube upload was Feb 2026 silver shortage; Sep 2025 video on AI miner research already proven on channel
- Mick chose: gold miners lagging the metal price, mixing UK + US listings
- Iterated structure: started with 4 stocks (SRB, EDV, CDE, WPM), Mick pivoted to 2-stock approach
- Final structure: SRB (UK, BUY 80.7% discount, with honest Coringa permit risk Jan 2027) + CDE (US/NYSE, room to run on 2026F multiples 8.9x P/E, 4.5x EV/EBITDA)

**Two charts uploaded by Mick (both saved at /mnt/user-data/uploads/):**
- 2026_04_08_-_GGP_-_Gold_n_Silver_Prices_Q1_2026-Estimated.jpg (Q1 monthly averages table)
- 2026_04_20_-_Gold_TradEcon__1yr_Chart_4805_1_USD_per_oz_JPG.jpg (1-year price arc)

**Central thesis identified:**
The Q1 2026 realised price disconnect. Spot gold "correcting" 10% from Jan ATH of $5,602, but
miners booking Q1 2026 sales received average ~$4,870/oz - roughly 50% higher than 2025 average
of ~$3,200/oz. EDV's Q1 confirmed it: realised $4,842 vs $3,000 guidance assumption. Q1 reports
landing now will show a re-rating retail hasn't priced in.

**Agreed video parameters:**
- Title direction: "Gold Hit $5,589 - But the Miners Are Still Cheap" (revised in PM session for 2-stock format)
- Two charts to feature in Section 1 as the visual hook
- Elliott Wave: GENERIC framing only ("corrective wave then continuation"), no specific count
- Inner Circle webinar coverage: soft mention, not hard CTA
- Charts attribution: "my research" without specifying source
- Tone: honest, down-to-earth, AI gets you to analysis quicker but you still own the call

**Voice DNA loaded fully (voice-dna-mick.json):**
- 12 patterns to deploy: personal attribution, humility markers, audience specificity (DIY-Investors capitalised),
  conversational transitions, softer technical language, hedging on predictions/conviction on principles,
  Cedric+Annie as named collaborators, British English throughout, data-first, temporal precision,
  self-aware concept references, full risk warning + DYOR signature

**Project folder created:**
C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\05-Areas\YouTube_System\diy-investors.com\YT-Longform\2026-05-10 - Gold Miners Q1 Realised Price Story (SRB+CDE)\
+ scripts/ subfolder

**Pickup note saved (CRITICAL for next session - now CONSUMED in PM session):**
2026-05-10 - Gold Miners Q1 Realised Price Story (SRB+CDE)\PICKUP-NOTE-for-fresh-context.md
Contains: full brief, both charts described, complete SRB + CDE financial data, script structure
section by section, voice DNA patterns, file writing requirements, frontmatter template.

**Mick's reason for context refresh:**
Context was filling up after extensive research and brief iteration. Smart move to clear before
the heaviest task (script writing). Pickup note designed so fresh Cedric has zero context loss.
PATTERN VALIDATED: PM session picked up cleanly with no information lost.

**Session intelligence to carry forward:**
- Channel ID UCaWdEBBHiV6P0i7X5fDCY0A (@DIY-Investors)
- Sister site diy-investors.ai active with Cedric/Nina AI content
- Notion Research Database ID: ac552ce5-2ceb-4ffb-a502-7d5da6c67cf8
- Notion Micks Content Studio DB ID: a1983c632eb84e15b365a6e3e310ff96
- SRB Notion: 353db32a-9b0a-8198-9801-cbb03e443ecf (Nina BUY 1 May 2026)
- CDE Notion: 34fdb32a-9b0a-8143-8cd0-e2e399711789 (Cedric Analysis 27 Apr 2026)
- EDV Notion: 351db32a-9b0a-8112-862e-cfe359ba4b6c (Nina 29 Apr 2026)
- 19 companies tracked in Research Log _index.md as of session

---

## Session Log - 2026.05.03 (ax-trees-automation: Sessions 6-7 - NotebookLM Bridge)

### notebooklm-bridge.js built and first live test passed. Two bugs found and fixed.
**Session time:** Sessions 6 and 7 -- 2026-05-03 afternoon
**Project:** ax-trees-automation
**Session logs:** C:\Vaults\Cowork\ax-trees-automation\session-logs\2026-05-03-session6.md
                 C:\Vaults\Cowork\ax-trees-automation\session-logs\2026-05-03-session7.md

**Session 6: notebooklm-bridge.js built**
- Decision 3 confirmed: do NOT rewrite Python NLM pipeline in JS -- bridge to it via child_process
- Python script: sharescope_nlm_researcher.py (handles Layers 2-5: notebook check/create,
  CSV upload, news search, Nina analysis, report save to vault)
- notebooklm-bridge.js written: spawns Python, streams output through Spinner, extracts JSON result
- Three supporting fixes: CSV filename suffixes, sharescope-search now returns companyName,
  sharescope-get-metrics passes companyName through to bridge
- Terminal Spinner class added (mirrors Python Spinner: rotating frames + alternating messages)
- notebookLM CLI: unofficial but working. Authenticate via: notebookLM login (once per session)
- Token stored at: C:\Users\pavey\.notebooklm\storage_state.json

**Session 7: Live test SQZ + bug fixes**
- First live test: pipeline ran end-to-end, report saved to vault. Two issues found.
- BUG 1 FIXED: extractJsonResult returned null (bridge reported success:false despite Python success)
  Root cause: Python prints Obsidian deep-link block AFTER JSON dict; stdout.slice(idx) included
  trailing ==== content, breaking JSON.parse. Fix: brace-depth counting to find matching }.
- ENHANCEMENT: flagNewsWarning() added. If IMPORT_RESEARCH fails (news search non-fatal timeout),
  bridge prepends Obsidian [!WARNING] callout to saved .md report so readers know news is absent.
- IMPORT_RESEARCH RPC: timed out 6x in first test (~4 min delay). Non-fatal. Google service issue.
  Monitor across runs. Not something we control in our code.

**JS file write rule (CRITICAL - confirmed again this session):**
  Edit tool ALWAYS truncates JS files at apostrophes in string literals.
  ALWAYS use bash heredoc: cat > filepath << 'ENDOFFILE' ... ENDOFFILE

**ax-trees-automation task status (as of 2026-05-03 Session 7):**
- [x] Layer 1: ShareScope data collection -- COMPLETE
- [T] Layers 2-5: notebooklm-bridge.js -- TESTED (retest needed to confirm extractJsonResult fix)
- [ ] Top-level orchestrator / run-research.bat -- NOT STARTED
- [ ] Portfolio-screenshots mini-project -- NOT STARTED
- [ ] Sharescope-stock-filter mini-project -- NOT STARTED

**Session 8 first task:**
  Run retest command (see SESSION8-PICKUP.md). If success:true confirmed, mark [x] COMPLETE.
  Then run full --run-layer1 end-to-end test.

**Mandatory reads at Session 8 start:**
  1. session-logs/SESSION8-PICKUP.md
  2. PIPELINE-PROGRESS.md
  3. skills/SKILLS-INDEX.md

---

## Session Log - 2026.05.03 (ax-trees-automation: Sessions 3-5 Complete, Layer 1 Done)

### ax-trees-automation Layer 1 (ShareScope Data Collection) FULLY COMPLETE
**Session time:** All-day sessions 3, 4, 5 -- 2026-05-03
**Project:** ax-trees-automation
**Session logs:** C:\Vaults\Cowork\ax-trees-automation\session-logs\2026-05-03-session5.md

**Session 3: AX tree master + project reorganisation**
- sharescope-ax-tree-master.md v1.2 created with all confirmed selectors
- Project folder structure cleaned up and standardised

**Session 4: Login/logout/screenshot skills**
- skills/sharescope-login.js -- [x] COMPLETE
- skills/sharescope-logout.js -- [x] COMPLETE (Options menu selector discovered and confirmed)
- skills/sharescope-screenshot.js -- [x] COMPLETE
- Logout discovery: must use #cogwheel-menu-main button[title="Options menu"] (not .first())

**Session 5: Search/export/metrics skills + live tests + infrastructure**
- .env restored to correct location C:\Users\pavey\.env (had been placed in project subfolder)
- .env protection rule added to THREE CLAUDE.md levels:
    C:\Users\pavey\.claude\CLAUDE.md (global -- Mick created in Cursor)
    C:\Vaults\Cowork\CLAUDE.md (vault level)
    C:\Vaults\Cowork\ax-trees-automation\CLAUDE.md (project level)
- skills/sharescope-search.js -- [x] COMPLETE
- skills/sharescope-export-financials.js -- [x] COMPLETE
- skills/sharescope-get-metrics.js -- [x] COMPLETE (orchestrator: login->search->export->logout)
- Live test GGP (Greatland Resources): PASS (selector bugs found and fixed)
- Live test SQZ (Serica Energy): PASS (clean run, all 6 tabs, logout confirmed)
- Auto-test policy added to CLAUDE.md: always test before reporting, never ask permission
- PIPELINE-PROGRESS.md created: master view of all 5 pipeline layers
- PROGRESS-TEMPLATE.md created: standard for all mini-projects
- PROGRESS.md standard locked: [ ] NOT STARTED | [~] WIP | [B] BUILT | [T] TESTED | [x] COMPLETE
- Dex vault mounted this session (request_cowork_directory): CEDRIC_MEMORY.md now writable directly
- Folder access rule added to CLAUDE.md (see Key Conventions below)

**ax-trees-automation task status (as of 2026-05-03 Session 5):**
- [x] Layer 1: ShareScope data collection -- COMPLETE (all 6 skills, both live tests)
- [ ] Layer 2: NotebookLM check/create -- SESSION 6 NEXT
- [ ] Layer 3: NotebookLM upload CSVs -- NOT STARTED
- [ ] Layer 4: NotebookLM run research -- NOT STARTED
- [ ] Layer 5: Research report format/return -- NOT STARTED

**Session 6 trigger:** "Cedric, please pick up the ax-trees-automation project for Session 6."
**First task Session 6:** Create mini-projects/notebooklm-check/ folder and PROGRESS.md.
  Key question: does NotebookLM have an API, or does it require browser automation?

**Mandatory reads at Session 6 start:**
  1. ax-trees-automation/CLAUDE.md
  2. PIPELINE-PROGRESS.md
  3. skills/SKILLS-INDEX.md
  4. sharescope/sharescope-ax-tree-master.md (v1.2)

**Key confirmed selectors (live-tested 2026-05-03):**
- Search results: #find-share-dlg-results > div.find-dlg-row > span.find-dlg-row-tidm
- Tab buttons: data-cmd attributes ONLY (role/name selectors are ambiguous)
- Forecasts tab: data-cmd="ShowBrokers" (NOT ShowForecasts -- different sub-toggle)
- Logout: #cogwheel-menu-main button[title="Options menu"] then #logout2

---

## Session Log - 2026.05.02 Evening (ax-trees-automation: Rebuild + PRD + Notion + Pickup)

### ax-trees-automation: folder rebuilt in Cowork vault. PRD v1.0 written. Session 3 ready.
**Session time:** ~19:00-20:30 BST
**Project:** ax-trees-automation

**Context:**
Mick asked to pick up the ax-trees-automation project. Previous session's files
(folder structure, session log) were found in a temporary session workspace, not
persisted to the Cowork vault. Full session transcript was recovered via session history.
All work was rebuilt cleanly this session.

**NOTE on 2026.05.01 Evening entry below:**
That entry records Tasks 2 and 3 as complete (PRD written, migration survey done, Python
pipeline discovered, SS-01 staged). Those outputs were written to a temporary workspace
and are not accessible in the Cowork vault. They may or may not exist in a session archive.
This session rebuilt Task 1 and wrote a fresh PRD (Task 2). Task 3 is still to be done.

**Completed this session:**
- Rebuilt full v7 folder structure into C:\Vaults\Cowork\ax-trees-automation\ (36 files, 23 dirs)
- Wrote PRD.md v1.0 (14 sections: purpose, platforms, skills architecture, mini-projects model,
  output standards, anti-bot approach, tech stack, full folder tree, plugin roadmap, migration plan)
- Updated Notion Meet Cedric / ShareScope hub (corrected SS-02, added SS-03 stub)
- Wrote full session log with Session 3 pickup instructions
- Updated CEDRIC_MEMORY.md (this update)

**ax-trees-automation current task status (as of 2026-05-02 Session 2 -- superseded by 2026-05-03 entry above):**
1. [x] Build v7 folder structure -- COMPLETE
2. [x] Write PRD.md -- COMPLETE (v1.1)
3. [x] Explore existing ShareScope project + plan migration -- COMPLETE (Session 3)
4. [x] Set up Meet Cedric / ShareScope series in Notion -- COMPLETE
5. [x] Layer 1: ShareScope skills built and tested -- COMPLETE (Sessions 4-5)

**See 2026-05-03 session log above for full Session 6 pickup details.**

**Key file locations (all in C:\Vaults\Cowork\ax-trees-automation\):**
- PRD.md -- full project requirements document
- CLAUDE.md -- global rules for all sessions
- skills/SKILLS-INDEX.md -- master skill catalogue
- mini-projects/MINI-PROJECTS-MASTER.md -- all project status
- session-logs/2026-05-01-session.md -- full session history + Session 3 pickup instructions

**Session 3 pickup:**
Say: "Cedric, pick up the ax-trees-automation project for Session 3."
Task 3: explore C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\
and plan the migration into ax-trees-automation.

**Notion series hub:** https://app.notion.com/p/353db32a9b0a81018396c00fb2378db4

---

## Critical Learning Requirement (Active)

**CODING GUIDANCE MANDATE (2026.04.04):**
Mick is a relative newbie to coding. For ALL coding-related tasks:
- Always provide step-by-step instructions with exact directory paths
- Always show exactly what to type in command prompts
- Always specify file locations and directory names
- Explain what each command does
- Provide clear "before you start" setup instructions
- This requirement remains active until Mick explicitly requests we change it after gaining experience

This applies to ALL .MD files, CLAUDE.MD, and CHANGELOG.md updates.

---

## Key Conventions (Never Forget)
- **Folder access:** If Cedric needs a folder not currently mounted (e.g. Dex vault, a project subfolder), use request_cowork_directory to prompt Mick for access BEFORE attempting any file operations. Never assume access -- always request it. This is the standard pattern for all sessions.
- YYYY.MM.DD prefix: ALL project folders, files, Notion titles, SOURCE titles in NotebookLM
- Notebook titles in NotebookLM: NO date prefix
- Index titles in NotebookLM: Index_Updated:YYYY.MM.DD - HH.MM (dots, no colons)
- ASCII only in vault file writes
- Transactions: month-scoped, non-strikethrough rows only
- No featured image on portfolio posts
- Real image dimensions always from WordPress media_details API
- Yr2 benchmark: always uses 1 Jan of CURRENT year as start point
- **Filesystem MCP write_file OVERWRITES -- never use for partial updates. Always read full file, modify in memory, write complete content back. (Learned 2026.04.29.)**
- **Filesystem MCP write_file is text-only -- binary deliverables (DOCX, PDF, PPTX, XLSX, images) MUST be staged via /mnt/user-data/outputs/ and shared with present_files. Confirmed 2026.05.10. (Note: there is no Claude-to-user binary-copy tool, so Cedric cannot place a binary file straight into the vault - Mick downloads and drops it in. Reconfirmed 2026.06.01.)**
- **AI report templates live at C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\06-Resources\AI_Report_Templates. Two report types so far: (1) Research_Brief/ - single-company portrait stock brief (DIY_Investors_Report_Template.docx); (2) Sector_Screen_Report/ - multi-company landscape sector screen / ranking, with a worked example (PM_Miners_Quarterly_Growth_Consolidated.docx) and a README documenting structure, house style and methodology. Each report type has its own README.md; the folder has a top-level README.md and CHANGELOG.md. Check here before building any new report so style stays consistent. (Added 2026.06.01.)**
- **DOCX font default: always Aptos 12pt for body text, headings scaled proportionally, unless Mick specifies otherwise. For wide tables, keep cell text at a size that fits the page rather than forcing 12pt (do not let columns wrap); small-print caveat notes may be one point smaller than body. This is also stored as a cross-project memory edit. (Locked 2026.06.01, superseding the earlier Arial 12pt print-DOCX recipe.)**
- **NEVER add hand-wavy unit-conversion or "common sense" reasoning to back up a verified figure.** Cross-source verification IS the verification. Adding spurious post-hoc reasoning is how unforced errors creep in. (Learned 2026.05.10 - the "pounds smaller than ounces" gaffe; Mick caught it. There are 16 oz in 1 lb, so a pound is LARGER than an ounce.)
- **DOCX with change-highlighting:** docx-js TextRun supports `highlight: "yellow"`, but emits a non-standard `<w:highlightCs/>` element that fails strict OOXML schema validation. After build, post-process the .docx zip to regex-strip all `<w:highlightCs[^/]*/>` elements before delivery. Word opens both versions fine; the strip is for validator compliance only.
- **Skill dual-write integrity (2026.06.03):** A full audit found the mirror /mnt/skills/user/ drifts from the vault and is not reliably populated per project. NEVER trust the mirror as authoritative; treat the vault as source of truth and verify (md5, normalised for CRLF) after any mirror write. When fixing a skill, confirm which of the three locations (Mirror, PRIMARY .claude/skills, DEX skills) is canonical FIRST - see PICKUP_NOTE_2026.06.03-Skill-Audit.md.

---

## London Time Protocol (MANDATORY)
NEVER use raw system clock. Always run python3 to verify London time.
BST (UTC+1): late March to late October. GMT (UTC+0): otherwise.

```python
from datetime import datetime, timezone, timedelta
utc_now = datetime.now(timezone.utc)
bst_active = 4 <= utc_now.month <= 10
offset = timedelta(hours=1) if bst_active else timedelta(hours=0)
london_now = utc_now.astimezone(timezone(offset))
print(london_now.strftime('%H:%M'), 'BST' if bst_active else 'GMT')
```

Greeting: before 12 = Good morning / 12-17 = Good afternoon / 18+ = Good evening

---

## Mandatory Skill Deployment Protocol
EVERY skill MUST be deployed to BOTH locations. No exceptions.
- Vault master: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\<skill-name>\
- MCP mirror:   /mnt/skills/user/<skill-name>/
Verify both copies match after deployment.
/mnt/skills/user/ IS writable from bash_tool in Claude Desktop (confirmed).
In claude.ai Web: vault writes via Filesystem MCP work; /mnt/skills/user/ is read-only.
[2026.06.03 audit caveat: this protocol is the INTENT, but on-disk reality has drifted -
some skills' newest copy lives in PRIMARY (Mick's Vault\.claude\skills) not DEX, and the
mirror does not always retain skills across projects/resets. Reconcile when the audit resumes.]

---

## NOTE: Earlier session log entries (pre-2026.05.10) preserved in git history.
This memory file was streamlined on 2026.05.10 to keep recent sessions front-of-mind.
For older session details (NotebookLM skill suite, ShareScope build, Poppy planning, etc.),
see git log on this file or the per-project session-logs/ folders.

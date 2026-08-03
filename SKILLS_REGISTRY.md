# SKILLS REGISTRY

**Single source of truth for every skill Mick can run from any runtime.**

- Last updated: 2026-08-02 (yt-transcript bumped to v1.1 and INSTALLED AS AN ACCOUNT SKILL, so it is now available cross-session in claude.ai web, Cowork and Claude Code without any mirror step. New Lives-In code `A` introduced for this. v1.1 adds a runtime table and three execution paths after Cedric tested the engine from a Cowork cloud container and YouTube returned `IpBlocked`: the caption fetch only works from Mick's home IP, so Path A = script (Claude Code / Cowork-on-computer), Path B = Claude in Chrome capture then Filesystem MCP write (Cowork cloud), Path C = deliver the note as a .md file (claude.ai web). The oembed metadata lookup is NOT blocked and still works everywhere. Vault master and .skill bundle verified byte-identical at 9,773 bytes.)
- Prior update: 2026-08-02 (added yt-transcript v1.0: fetch a YouTube transcript and file it as a Source-Template note - Summary / Key Takeaways / Notes/Transcript, tags [YT], Reference Link = URL, plus SEPARATE Channel (auto from oembed) and By (the person, filled by Cedric) fields - split because a channel can have several authors and is not always eponymous. Modes --url and --scan-inbox (inbox root by default; --include-queue for the backlog), with dedupe, --dry-run and --force. Engine scripts/yt_transcript.py, pure ASCII. Output 06-Resources/Transcripts. Dependency youtube-transcript-api installed permanently, no API key. Built with Mick; proven on Nick Milo, Wanderloots and Artem Zhutov videos.)
- Prior update: 2026-08-02 (non-ascii-sweep: added REVIEW_IGNORE to ascii_sweep.py so the pound sign (0x00A3) and cent sign (0x00A2) are no longer flagged for review in scan/safe reports - Mick's standing decision that this price notation is legitimate content, not corruption. Tested in isolation and against the live vault; pounds and cents excluded, other currency still flagged. Also cleared a ReadOnly flag on ii-to-xero/convert.py that was failing the weekly sweep, and recycled six junk files.)
- Prior update: 2026-08-01 (added eom-portfolio-capture v1.0: the month-end ShareScope image grab - four Active 10 portfolios' current-holdings + OCR-cropped month transactions, plus ASX and SP500 verified 12-month charts at two 16:9 sizes, filed into the live folders that feed portfolio-post-creator. Built with Mick this session.)
- Prior update: 2026-07-31 (added image-cta-overlay v2.0: diagonal CTA overlay for thumbnails, now with the light grey banded house style for dark blue webinar slides. Discovered during the same session that this skill had NEVER been in the vault - it existed only in the Cowork skill store - so it is registered here for the first time.)
- Maintained by: Cedric (PAIDA)
- Update rule: see CLAUDE.md "MANDATORY SKILL DEPLOY PROTOCOL". This file MUST be updated on every skill create, rename, version-bump, or deprecation.

---

## How to read this file

Each row tells you four things: who built it, where it lives, how to invoke it, what it does.

**Source codes:**

- `mick-cedric` = Mick built with Cedric
- `mick` = Mick built solo
- `anthropic` = ships with the Cowork plugin marketplace (Anthropic-provided)
- `external` = transferred in from a third party

**Lives-In codes (a skill can live in more than one place):**

| Code | Meaning |
|------|---------|
| `V` | Vault: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\ |
| `M` | Mirror: /mnt/skills/user/ (Cowork session mirror) |
| `A` | Account skill: uploaded to Mick's Claude account (Settings - Capabilities - Skills). Syncs to EVERY runtime automatically, survives sessions. Preferred over `M` - no per-session mirror step. |
| `P` | Plugin marketplace (Cowork plugin, also reachable in Claude Code via plugin) |
| `C-Pete` | claude.ai PAIDA Project "Poster Pete" |
| `C-Cedric` | claude.ai PAIDA Project "Cedric" |
| `C-Poppy` | claude.ai PAIDA Project "Poppy" |
| `C-?` | claude.ai PAIDA project, exact project to be confirmed |
| `S` | Cowork Scheduled Task (path: C:\Users\pavey\OneDrive\Documents\Claude\Scheduled\) |

**Runtime visibility:**

| Location | claude.ai web | Cowork | Claude Code |
|----------|---------------|--------|-------------|
| V (vault) | Yes (Filesystem MCP) | Yes (mounted) | Yes (filesystem) |
| A (account) | Yes | Yes | Yes |
| M (mirror) | Yes | Yes | Partial |
| P (plugin) | No | Yes | Yes (if plugin installed) |
| C-* (claude.ai) | Yes (only inside that project) | No | No |
| S (scheduled) | No | Yes | No |

**Status codes:** `active` / `WIP` / `deprecated` / `unverified` (registry has the name but Cedric has not confirmed presence this session).

---

## Section 1 - Custom Skills (Mick + Cedric)

### 1a. Confirmed in vault and mirror this session

| Name | Trigger | Source | Lives In | Status | Description |
|------|---------|--------|----------|--------|-------------|
| ai4inv-webinar-processor | /ai4inv or "process [month] webinar" | mick-cedric | V, M, P | active | Monthly AI for Investors webinar pipeline: NotebookLM source + Word user guide + index update |
| batch-process-webinars | /batch-process-webinars | mick-cedric | V, M | active | Batch version of /process-webinar for an entire archive folder |
| cedric-note-fetcher | "download the note I emailed myself" / "fetch the Cedric note" | mick-cedric | V, P (M pending) | active | On-demand: fetch a self-sent Gmail attachment to a real file (browser Add-to-Drive then Google Drive connector; decode+validate) |
| eom-portfolio-capture | "do the end-of-month capture" / "grab the month-end portfolio images" / "run the EOM capture" | mick-cedric | V (+ user-level C:\Users\pavey\.claude\skills; M pending) | active | v1.0 (2026-08-01): month-end ShareScope image grab. One login: 4 Active 10 portfolios (current-holdings screenshot + OCR-cropped month transactions) + ASX & SP500 12-month charts at 1200px/1920px (16:9 JPEG, verified 12m). Files into the six live folders that feed portfolio-post-creator. Scripts eom_capture_full.py (+ --commit) and crop_transactions.py in 04-Projects\2026.04.04-ShareScope-Automation. UPSTREAM of the End-of-Month Portfolio Posting SOP. |
| gmail-self-notes | "sweep my Gmail notes" / scheduled morning run | mick-cedric | V, P (M pending) | LIVE - scheduled gmail-self-notes-sweep daily ~06:20 (catch-up-on-wake); MCSB-Filed label+archive on success; representative 48h test sweep PASSED. YouTube overlap resolved (vault wins; yt-inbox-sweeper retired for YT; 44 Sheet rows migrated; Sheet archived 2026.07.05). OPEN: 48h backlog backfill; mirror (M) re-sync | Ingest self-sent Gmail into 00-Inbox as Obsidian notes: body text + attachment(md) + YouTube link, shared xref + two-way links, author Mick/MCSB, catch-up-on-wake |
| logo-masking | "mask the logo" / "remove the branding" | mick-cedric | V, M | active | Remove watermarks/logos from PNG/JPG via auto-sampled colour matching |
| micks-stocknote | (Micks-View write command) | mick-cedric | V, M | active | Capture brain dump on a stock and write as structured Obsidian note to Micks-View Inbox |
| micks-view-query | (Micks-View query command) | mick-cedric | V, M | active | Read mechanism for Micks-View library; chronological results |
| newsletter-wp-publisher | "publish the newsletter" / "upload the newsletter to WordPress" | mick-cedric | V (M pending) | active | v1.0 (2026.07.19): end-to-end newsletter media upload (any local file, not folder-scanned) + WordPress post create-or-update via REST API. Multi-site aware (diy-investors-com proven; diy-investors-ai credentials ready, untested). Draft-only, never auto-publishes. First run: July 2026 Freedom Blueprint, post 15514. |
| nina-to-notion | "post Nina's report to Notion" / "log this to Notion" | mick-cedric | V, M | active | Post Nina's research markdown to Notion Research Database with EPIC, summary, tags |
| non-ascii-sweep | "run the non-ascii sweep" / "clean the vault for non-ascii" / weekly Sat ~10am | mick-cedric | V, S (M pending) | active - scan/safe/full modes; SAFE auto-fixes typography and reports meaningful for review; script ascii_sweep.py is pure-ASCII by design (chr code points) so it cannot corrupt its own maps; weekly SAFE schedule non-ascii-sweep-weekly. 2026.08.02: added REVIEW_IGNORE set ({0x00A3} pound, {0x00A2} cent) so legitimate price notation is no longer flagged for review each week; SKILL.md carries a "Known-legitimate non-ASCII" section recording that decision. | Sweep the whole Dex-MickP vault for non-ASCII (corrupt) characters and clean them; dated report to System/Debug_Logs |
| notebooklm-add-content | (on request) | mick-cedric | V, M | active | Add content to a NotebookLM notebook |
| notebooklm-chat | (on request) | mick-cedric | V, M | active | Chat with a NotebookLM notebook |
| notebooklm-notebook-setup | (on request) | mick-cedric | V, M | active | Set up a new NotebookLM notebook |
| notebooklm-studio-output | (on request) | mick-cedric | V, M | active | Generate Studio outputs from a NotebookLM notebook |
| notion-summary | (on request, browser-control) | mick-cedric | V, M | active | Notion announcement summary via browser control with Ctrl+B/Shift+Enter |
| pdf-to-pptx-converter | (on request) | mick-cedric | V, M | active | Convert NotebookLM PDF slide decks into branded PowerPoint with logo masking |
| pns | /pns | mick-cedric | V, M | active | Post Notion Summary via Notion MCP (200-word structured summary) |
| pptx-editable-graphics | "make an infographic" / "rebuild the graphic as shapes" / "match the deck theme" | mick-cedric | V, M | active | Build slide diagrams as fully editable native PowerPoint shapes (never a flat PNG) and skin them to the house theme read straight out of the target deck. Includes ppt_shapes helper library, extract_theme, qa_render and a worked concentric-jigsaw example |
| process-webinar | /process-webinar | mick-cedric | V, M | active | Single Inner Circle / Plaza webinar PDF; populate Radar Log + Companies Covered |
| session-start | (automatic) | mick-cedric | V, M | active | Mandatory session start protocol; environment probe + announcement |
| sharescope-financials | "download [TICKER] financials" / /sharescope-financials | mick-cedric | V, M | active | Financial data export for any ShareScope stock; verifies 6 CSVs |
| sharescope-nlm-research | /research [TICKER] / "research [company]" | mick-cedric | V, M | active | Full ShareScope plus NotebookLM pipeline (v1.2). Resolves ticker, runs orchestrator, parallel upload + Nina analysis, Research Log entry, Notion publish |
| sharescope-start | "sharescope start" / /sharescope-start | mick-cedric | V, M | active | ShareScope session opener; vault + project folder, PICKUP_POINT, briefing |
| image-cta-overlay | "add CTA to thumbnail" / "add click here text" / "add diagonal text to image" | mick-cedric | V (P = v1.0 old; M pending) | active | v2.0 (2026-07-31): diagonal call-to-action overlay on an image thumbnail. Two styles: plain text (red, original) and BANDED - a narrow angled light grey band (224,224,224 at alpha 240) carrying bright green text (0,255,0) with a 3px dark outline and soft drop shadow. Banded light grey is the confirmed house style for diy-investors.ai monthly webinar thumbnails and any dark blue .ai Webinar slide. WARNING: the vault copy is v2.0 but the Cowork skill store still runs v1.0 until Mick uploads the delivered image-cta-overlay.skill file. |
| thumbnail-play-button | (on request) | mick-cedric | V, M | active | YouTube-style play button overlay on image thumbnails |
| week-plan-print | /week-plan-print | mick-cedric | V, M | active | Print-ready A4 Word doc of current week's calendar |
| yt-transcript | "get the transcript of [video]" / "transcribe this YouTube video" / "process my YouTube inbox" / paste a YouTube link | mick-cedric | V, A (S-candidate) | active | v1.1 (2026-08-02): fetch a YouTube transcript (youtube-transcript-api, no key) and file it as a Source-Template note in 06-Resources/Transcripts (Summary + Key Takeaways written by Cedric, tags [YT], Reference Link, separate Channel (auto) + By (person) fields, ## Notes/Transcript). Modes: --url and --scan-inbox (root by default; --include-queue for the 200+ backlog) with dedupe, --dry-run, --force. Engine scripts/yt_transcript.py (pure ASCII). Near-daily tool - Mick emails himself YT links. RUNTIME LIMIT (tested 2026-08-02): YouTube returns `IpBlocked` for caption fetches from any datacentre IP, and device_bash has no network, so the SCRIPT only runs from Mick's home IP. v1.1 therefore carries a runtime table and three paths - A: script (Claude Code / Cowork-on-computer); B: Claude in Chrome capture then Filesystem MCP write (Cowork cloud); C: Mick pastes the transcript and Cedric delivers a .md file (claude.ai web). oembed metadata is NOT blocked and works everywhere. Installed as an account skill so all three runtimes see it. |
| yt-play-button-overlay | (on request) | mick-cedric | V, M | active | YouTube play button overlay (image processing) |
| yt-weekly-stats-v2 | "log YouTube stats" / "update YT stats" | mick-cedric | V, M, P | active | Pull DIY Investors channel analytics from YouTube Studio and write to Google Sheets tracker |
| portfolio-post-creator | (monthly portfolio batch) | mick-cedric | C-Pete, V, M | active | Orchestrator (v2.3): builds HTML post bodies for the four DIY Investors portfolio pages; calls benchmark-fetcher + wordpress-image-uploader, hands off to wordpress-post-publisher. v2.3 (2026-05-30) added blue-line month-boundary rule and portfolio tag rule. |
| benchmark-fetcher | (called by portfolio-post-creator) | mick-cedric | C-Pete, V, M | active | v1.0: month-end FTSE All-Share + S&P 500 closes from Yahoo Finance; updates Indices spreadsheet. Migrated to V+M 2026-05-30. |
| wordpress-image-uploader | (called by portfolio-post-creator) | mick-cedric | C-Pete, V, M | active | v1.0: upload portfolio screenshots to WordPress media library; returns real media IDs + dimensions. Migrated to V+M 2026-05-30. |
| wordpress-post-publisher | (called by portfolio-post-creator, or ad-hoc) | mick-cedric | C-Pete, V, M | active | v1.2: push post objects to WordPress as drafts via REST API. Content-agnostic. v1.2 (2026-05-30) added tags field to payload for portfolio post tagging. |
| natwest-to-xero | "convert the NatWest CSV" / "do the NatWest import" | mick-cedric | V, P (M pending) | active | Ditty Box year-end chain, step 1. NatWest CSV export to Xero bank statement import CSV + 11-column audit XLSX. Account code is a parameter; works for GBP Current, No 2 and USD. Registered 2026-07-26. |
| cc1136-to-xero | "convert the Halifax statements" / "do the CC1136 import" | mick-cedric | V, P (M pending) | active | Ditty Box year-end chain, step 1. Halifax Clarity 1136 monthly PDF statements to Xero CSV + 3-sheet audit XLSX. Auto-detects the two page-3 table layouts (Card Ending column added July 2025). Registered 2026-07-26. |
| paypal-to-xero | "convert the PayPal export" / "do the PayPal import" | mick-cedric | V only | active | Ditty Box year-end chain, step 1. PayPal CSV/XLSX export to Xero bank statement import CSV + audit XLSX. D.Box PayPal = code 058. NOTE: unlike its three siblings this one is NOT visible as a Cowork skill - vault only. Registered 2026-07-26. |
| ii-to-xero | "process the ii account" / "do the Interactive Investor YE" | mick-cedric | V, P (M pending) | active | Ditty Box year-end chain, step 2. Folds the ii year-end download into the master tracking spreadsheet (history from 2008) + audit XLSX. Produces figures for MANUAL journals, not a Xero CSV. Registered 2026-07-26. |
| schwab-to-xero | "process the Schwab account" / "do the Schwab year-end" | mick-cedric | V, P (M pending) | active | Ditty Box year-end chain, step 2. Schwab corporate ...366 download to audit XLSX + posting schedule. USD account, Xero is GBP-only, so no CSV - Mick keys two manual cash transactions and the stock revaluation journal. Registered 2026-07-26. |
| info-for-accountant | "do the pack for the accountant" / "build the Jade pack" | mick-cedric | V (M not possible from Cowork cloud; .skill file delivered to Mick 2026-07-26) | active | Ditty Box year-end chain, FINAL step. Assembles the numbered evidence pack for the accountants: derives the J-manifest from the prior year's pack, proposes the mapping for approval, copies (never moves) with md5 verification, builds the checklist xlsx, reports gaps, zips on request. Baseline manifest J01-J25 in reference/manifest.md. Created 2026-07-26. |

### 1b. claude.ai PAIDA Project skills (NOT yet mirrored to vault)

These were referenced in CEDRIC_MEMORY.md (line 920-933, snapshot 2026-04-19) but are not present in the vault skills folder. Action: capture each from its claude.ai project and dual-write to vault + mirror.

| Name | Source | Lives In | Status | Description | Mirror priority |
|------|--------|----------|--------|-------------|-----------------|
| webinar-radar-extractor | mick-cedric | C-? | unverified | Extracts entries for Radar Log (likely superseded by /process-webinar) | LOW - check for overlap |
| my-view-notion-writer | mick-cedric | C-? | unverified | Writes "My View" narrative on Radar Log entries (possibly same as micks-stocknote/micks-view-query family) | MEDIUM - check for overlap |
| vault-file-mover | mick-cedric | C-? | unverified | Move files within the vault | LOW |
| obsidian-frontmatter | mick-cedric | C-? | unverified | YAML frontmatter manipulation for Obsidian notes | LOW |
| empty-note-detector | mick-cedric | C-? | unverified | Find empty Obsidian notes | LOW |
| epic-ticker-enricher | mick-cedric | C-? | unverified | Enrich notes with EPIC/ticker metadata | MEDIUM |
| sensitivity-scanner | mick-cedric | C-? | unverified | Scan vault content for sensitive info | MEDIUM |
| batch-approval-processor | mick-cedric | C-? | unverified | Batch approve queued items | LOW |
| run-stock-analysis v1.1 | mick-cedric | C-Cedric | unverified | Sub-agent stock analysis (1,200-word target). May be superseded by sharescope-nlm-research v1.2. | LOW - check for overlap |

---

## Section 2 - Anthropic plugin marketplace skills (NOT in vault)

These ship with the Cowork plugin marketplace and are managed by Anthropic. We do NOT mirror them to the vault.

| Name | Source | Lives In | Description |
|------|--------|----------|-------------|
| algorithmic-art | anthropic | P | Generative art via p5.js with seeded randomness |
| annie | anthropic + mick-cedric | V (extended), M, P | Calendar management; date verification protocol. Mick has extended local copy. |
| brand-guidelines | anthropic | P | Anthropic brand styling for artifacts |
| canvas-design | anthropic | P | Visual art in PNG/PDF using design philosophy |
| consolidate-memory | anthropic | P | Merge duplicates and prune memory index |
| content-extraction | anthropic | P | Extract content ideas from long-form content |
| diy-ai-logo-placement | mick-cedric | P (mirror only) | Batch DIY Investors logo placement on PNG slides |
| doc-coauthoring | anthropic | P | Structured doc co-authoring workflow |
| docx | anthropic | P | Word document creation/editing |
| image-cta-overlay | mick-cedric | P (mirror only) | "Click here for Report" CTA overlay on thumbnails |
| internal-comms | anthropic | P | Internal communications templates |
| key-takeaways | anthropic | P | Bullet summary of long-form content |
| linkedin-post | anthropic | P | LinkedIn post writing |
| lse-news-checker | mick-cedric | P (mirror only) | UK LSE RNS portfolio news (used by uk-portfolios-daily scheduled task) |
| mcp-builder | anthropic | P | Build new MCP servers |
| motion-design-prompt | anthropic | P | Generate motion design prompts |
| notion-summary-generator | mick-cedric | P (mirror only) | Notion MCP version of summary skill (200-word structured) |
| pdf | anthropic | P | PDF processing toolkit |
| portfolio-risers-fallers | mick-cedric | P (mirror only) | Daily/EOD portfolio movers report |
| pptx | anthropic | P | PowerPoint creation/editing |
| researcher-agent | anthropic | P | Research and analysis filtered by business context |
| schedule | anthropic | P | Create scheduled tasks |
| setup-cowork | anthropic | P | Cowork onboarding |
| skill-creator | anthropic | P | Create/edit/test skills |
| theme-factory | anthropic | P | Apply preset themes to artifacts |
| title-generator | anthropic | P | Generate titles/headlines |
| twitter-thread | anthropic | P | Twitter/X thread writing |
| us-news-checker | mick-cedric | P (mirror only) | US stock news digest (used by us-portfolios-daily scheduled task) |
| web-artifacts-builder | anthropic | P | Multi-component HTML artifacts |
| xlsx | anthropic | P | Excel processing |

---

## Section 3 - Productivity plugin skills

From the `productivity` plugin (separate from the main marketplace).

| Name | Source | Lives In | Description |
|------|--------|----------|-------------|
| memory-management | anthropic | P | Two-tier memory system (CLAUDE.md plus memory directory) |
| start | anthropic | P | Initialize productivity system and dashboard |
| task-management | anthropic | P | Simple task tracking via TASKS.md |
| update | anthropic | P | Sync tasks and refresh memory |

---

## Section 4 - Cowork plugin management skills

| Name | Source | Lives In | Description |
|------|--------|----------|-------------|
| cowork-plugin-customizer | anthropic | P | Customise a Claude Code plugin for specific tools/workflows |
| create-cowork-plugin | anthropic | P | Scaffold a new plugin from scratch |

---

## Section 5 - Scheduled Tasks (Cowork)

Live at: C:\Users\pavey\OneDrive\Documents\Claude\Scheduled\

| Task ID | Schedule | Source | Lives In | Status | Description |
|---------|----------|--------|----------|--------|-------------|
| morning-daily-briefing | 06:50 daily | mick-cedric | S | active | Daily briefing: calendar, email, Slack, portfolio/markets highlights |
| uk-portfolios-daily | 07:34 Mon-Fri | mick-cedric | S | active | UK Active 10 / Yr2 LSE RNS news summary (uses lse-news-checker) |
| us-portfolios-daily | 14:04 Mon-Fri | mick-cedric | S | active | US Active 10 / Yr2 news digest (uses us-news-checker) |
| non-ascii-sweep-weekly | 10:00 Sat (cron 0 10 * * 6) | mick-cedric | S | active | Weekly SAFE non-ASCII sweep of the vault (uses non-ascii-sweep skill); reports meaningful non-ASCII for review |

---

## Section 6 - Deprecated / Archived

| Name | Lives In | Replaced by | Notes |
|------|----------|-------------|-------|
| stock-research | V/_deprecated/ | sharescope-nlm-research | Old stock research skill |
| yt-weekly-stats-v1 | V/_deprecated/ | yt-weekly-stats-v2 | Tab-separated entry did not work in browser Sheets |

---

## Section 7 - Maintenance Rules

1. **Source of truth**: this file. The skills/README.md table is now a derived/scoped extract for vault skills only.
2. **Update on every change**: any time a skill is created, renamed, version-bumped, or deprecated, update this file in the same session. Add an entry to CHANGELOG.md too.
3. **Verification before edits**: when editing this file, re-verify the affected row by listing the actual location (vault folder, mirror folder, or scheduled task list).
4. **claude.ai PAIDA Project skills**: these can only be added to this registry by hand because Cowork cannot read claude.ai server-side data. When Mick adds a new skill to a PAIDA project, he should tell Cedric so this file is updated.
5. **No emojis, no smart quotes, no em dashes**: ASCII only, per CLAUDE.md vault rule.
6. **Git commit**: this file lives at the vault root and is committed to GitHub via the standard daily commit. No separate handling.

---

## Section 8 - Pending actions (as of 2026-05-09)

0. **DONE (2026-05-30, later)**: portfolio-post-creator bumped to v2.3 (blue-line month-boundary rule + portfolio tag rule) and wordpress-post-publisher bumped to v1.2 (tags field added to payload). Both promoted to V + M and verified byte-identical. NOTE: the portfolio-post-creator vault file had been corrupted in a separate manual session (it contained wordpress-post-publisher content at 35,267 bytes); fully overwritten from Mick's clean download and confirmed healthy at 27,758 bytes. Portfolio tag IDs (UK A10 = 513, UK A10 Yr2 = 890, US A10 = 512, US A10 Yr2 = 891) were auto-pulled by another Cedric instance and are ASSUMED correct; to be visually confirmed on the draft posts during the end-of-June run.
1. **DONE (2026-05-30)**: Poster Pete's four end-of-month skills (portfolio-post-creator, wordpress-post-publisher, wordpress-image-uploader v1.0, benchmark-fetcher v1.0) migrated from C-Pete to V + M. Vault and mirror verified byte-identical. Credentials: by Mick's decision (2026-05-30) the .env stays solely in C:\Vaults\Mick's Vault\.env as the single source of truth - deliberately NOT duplicated into the Dex vault, so passwords can be changed in one place with no risk of divergence. The two WordPress skills correctly point at that single .env. Original copies left in C:\Vaults\Mick's Vault\.claude\skills\ for now (not deleted).
2. **Verify and reconcile** the eight `unverified` C-? rows in Section 1b. Several may be superseded by current vault skills (e.g. micks-stocknote and micks-view-query may already cover my-view-notion-writer).
3. **Confirm which PAIDA project hosts each unverified skill** so the C-? cells can be replaced with C-Pete / C-Cedric / C-Poppy.
4. **Add registry update step to CLAUDE.md MANDATORY SKILL DEPLOY PROTOCOL** (currently Step 5 says "Update skills/README.md" - change to "Update SKILLS_REGISTRY.md and skills/README.md").

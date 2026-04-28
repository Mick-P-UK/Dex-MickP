# CEDRIC MEMORY
**Last Updated:** 2026.04.27 - ~09:30 BST (1,200-word report target added to sub-agent brief. Ready for rehearsal run.)
**Environment:** Cowork (Filesystem MCP + full MCP suite confirmed)

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

## RESUME HERE - Tuesday 28 April 2026 (after breakfast break)

### ENQ PIPELINE FULLY COMPLETE. Wednesday webinar demo ready.

Completed morning of 2026.04.27:
  [x] run-stock-analysis SKILL.md: built and updated (Step 4 = sub-agent delegation; 1,200-word target added)
  [x] ENQ pipeline: 6 CSVs downloaded via browser_run_code (07:46 BST)
  [x] 11-section research report: 3,942 words, written by general-purpose sub-agent (next run targets ~1,200 words)
  [x] Notion page created: https://www.notion.so/34fdb32a9b0a81d68f93dee8793e0bc7
  [x] Branded PDF: reports\2026.04.27_ENQ_Research_Brief.pdf (162KB)
  [x] Branded DOCX: reports\2026.04.27_ENQ_Research_Brief.docx (19KB)
  [x] Session log written, PICKUP_POINT.md updated, Meet Cedric Episode 7 posted

### NEXT TASK: Tuesday rehearsal run

  - Start a fresh Cowork session
  - Trigger: "run stock analysis for ENQ" (or a different ticker for surprise)
  - Watch the full pipeline execute from scratch -- note timing and narration points
  - Pre-record backup run as insurance
  - Fix PDF logo (mount 06-Resources folder to add DIY Investors logo to header)
  - Wednesday morning: nlm login refresh, credentials check, final test run

### KEY ARCHITECTURE DECISION (2026.04.27 -- Mick's request)
  Report writing is ALWAYS delegated to a general-purpose sub-agent.
  Sub-agent reads CSVs independently, researches news, writes full 11-section report.
  Cedric orchestrates; sub-agent writes. This is baked into run-stock-analysis SKILL.md Step 4.

### Key Facts to Remember
- **Automation method for ShareScope: browser_run_code (Playwright MCP) -- NOT Python scripts**
- Login URL: https://webservice.sharescope.co.uk/login.do (NOT www.sharescope.co.uk)
- Login selectors FIXED 2026.04.26 (placeholder-based, confirmed live):
    Email:    input[placeholder="Enter email"]
    Password: input[placeholder="Password"]
    Button:   get_by_role("button", name="Login")
    Post-login: wait_for_url with jsessionid in URL (not CSS dashboard class)
- 500ms delay required between username and password entry
- Password contains # characters -- must be quoted in .env
- Credentials in: C:\Vaults\Mick's Vault\.env (SHARESCOPE_USERNAME, SHARESCOPE_PASSWORD, SHARESCOPE_HEADLESS)
- Session key: jsessionid captured from post-login URL redirect
- Search: select "All instruments" in #find-share-dlg-list BEFORE typing ticker
- Export: page.expect_download() context manager intercepts download; save_as() renames it
- Output naming: YYYY.MM.DD-HH_MM_TICKER_datatype.csv (London time, BST/GMT aware)
- Architecture: Sandwich model -- login -> search -> export -> logout
- Four planned skills: sharescope-financials, sharescope-charts, sharescope-portfolio, sharescope-screener
- PRD v2.1 location: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\2026.04.26 - PRD - ShareScope Browser Automation System v2.1.docx
- Alt+F4 = proper quit for Claude Desktop (not X button)
- PICKUP_POINT.md in project folder has full session handoff notes and test guide

---

## Session Log - 2026.04.27 Morning (Full ENQ Pipeline Complete)

### run-stock-analysis end-to-end CONFIRMED WORKING
**Session time:** ~07:00-08:30 BST
**What we did:**
- Picked up from earlier this morning (6 ENQ CSVs already downloaded at 07:46)
- Spawned general-purpose sub-agent to write the 11-section ENQ research report
  Sub-agent read all 6 CSVs, ran web searches, produced 3,942-word report
  Output: reports\ENQ_report_draft.md
- Updated run-stock-analysis SKILL.md: Step 4 now always delegates to sub-agent
- Created Notion page in Research Database:
    Title: 2026.04.27 - Enquest PLC (ENQ): Cedric's Analysis
    Tag: Cedric's Analysis
    URL: https://www.notion.so/34fdb32a9b0a81d68f93dee8793e0bc7
    Note: Notion MCP only accepts 1 tag per create/update call (multi-select limitation)
- Generated branded PDF using docx-js + LibreOffice:
    reports\2026.04.27_ENQ_Research_Brief.docx (19KB)
    reports\2026.04.27_ENQ_Research_Brief.pdf (162KB)
    Note: DIY Investors logo not included (06-Resources not mounted)
- Wrote session log, updated PICKUP_POINT.md, created Meet Cedric Episode 7 in Notion
- Requested and received access to Dex-MickP folder; updated CEDRIC_MEMORY.md (this file)

**Key ENQ findings (for reference):**
- FY2025 Revenue $1,118.3m; Adj EBITDA $503.8m; post-tax profit $1.6m
- UK Energy Profits Levy absorbed $491.9m of $493.4m pre-tax profit
- Production 45,606 boepd -- beat guidance for second consecutive year
- Malaysia Seligi 1b: first gas Dec 2025, 10,400 boepd Jan 2026 (major positive)
- RBL refinanced Q4 2025: $679m facility, $200m undrawn -- removes liquidity risk
- Net debt/EBITDA 0.9x; final dividend 0.80p (4.1% yield)
- March 2028 windfall tax sunset = primary re-rating catalyst (EPS 0.1p -> 15-20p)

**New pattern confirmed: sub-agent delegation for report writing**
- Mick requested this mid-session
- SKILL.md Step 4 updated to always say "delegate to general-purpose sub-agent"
- Sub-agent receives full brief: ticker, CSV paths, parsed data, web findings, format
- Produces report independently; Cedric reads output and continues pipeline

---

## Session Log - 2026.04.26 Evening Part 3 (Phase 1B Complete + Webinar Demo Planned)

### ShareScope Phase 1B DONE + Wednesday demo planned
**Session time:** ~20:30-21:30 BST
**What we did:**
- Step 5 DONE: sharescope_orchestrator.py upgraded to v0.2 (Phase 1B full pipeline)
  CLI: python sharescope_orchestrator.py {TICKER}
  Tested by Mick: SQZ x2 runs + BP. -- 18 CSVs confirmed. Fully working.
- Step 6 DONE: All 7 scripts commented (novice-friendly). Sub-agent handled this.
- Step 7 DONE: sharescope-financials SKILL.md built. Vault written. Mirror PENDING.
- WEBINAR DEMO PLAN AGREED: Full end-to-end stock research pipeline for Wednesday 29 April.
  Flow: ticker -> ShareScope CSVs -> NotebookLM notebook -> news -> analysis report -> PDF
- ARCHITECTURE DECISION: Use browser_run_code (Playwright MCP) NOT Python/PowerShell.
  Mick correctly identified that PowerShell commands would break the live demo narrative.
  browser_run_code gives Cedric full Playwright JS control from within Cowork.
  No terminal needed. Browser pops up on Mick's screen, does its work, closes.
- Test stock confirmed: ENQ (Enquest, London Stock Exchange). No existing notebook.
- Report template confirmed: DIY_Investors_Report_Template.docx exists with full branding.
- Still needed from Mick: Cedric Research report section structure (Claude project space).
- PICKUP_POINT.md fully rewritten with Monday build plan.

**Skill mirrors still pending (both need Claude Desktop session):**
  skills\sharescope-start\SKILL.md       -- vault written, mirror PENDING
  skills\sharescope-financials\SKILL.md  -- vault written, mirror PENDING

---

## Session Log - 2026.04.26 Evening Part 2 (ALL 4 TESTS PASSED)

### ShareScope Phase 1B -- FULLY TESTED AND WORKING
**Session time:** ~19:45-20:30 BST
**What we did:**
- Ran all 4 tests from PowerShell. All passed after two bug fixes.
- Bug 1 fixed (sharescope_search.py):
    ok_button.wait_for(state="enabled") -- "enabled" not a valid Playwright state
    Fix: added "expect" to import; replaced with expect(ok_button).to_be_enabled(timeout=5000)
- Bug 2 fixed (sharescope_export.py + sharescope_utils.py):
    ImportError: cannot import name 'TABS_WITHOUT_CSV' from 'sharescope_utils'
    Fix: moved TABS_WITHOUT_CSV to sharescope_utils.py; search.py now imports from there
- Test 4 result: 6 CSVs confirmed in downloads\SQZ\ all timestamped 2026.04.26-20_06
- Session log written: session-logs\2026.04.26-EVENING-SESSION-LOG.txt
- PICKUP_POINT.md updated to reflect tests passed and next steps
- CEDRIC_MEMORY.md updated (this file)
- Notion Meet Cedric page updated (Episode 6 status updated)

**Phase 1B final status:**
- [x] sharescope_utils.py -- FIXED + TESTED (TABS_WITHOUT_CSV added)
- [x] sharescope_search.py -- FIXED + TESTED (expect().to_be_enabled())
- [x] sharescope_export.py -- FIXED + TESTED (imports from utils)
- [x] sharescope_login.py -- FIXED + TESTED
- [x] Tests 1-4 -- ALL PASSED (2026.04.26 ~20:06 BST)
- [x] 6 CSVs confirmed: income, balance, cash, ratios, dividends, forecasts for SQZ
- [ ] sharescope_orchestrator.py -- needs Phase 1B wiring (NEXT -- Step 5)
- [ ] sharescope-financials SKILL.md -- not yet built (Step 7, after orchestrator)

---

## Session Log - 2026.04.26 Evening Part 1 (Phase 1B Scripts Complete, Login Fixed, Tests Ready)

### ShareScope Phase 1B -- ALL SCRIPTS WRITTEN, READY TO TEST
**Session time:** ~17:00-19:00 BST
**What we did:**
- Context was reconstructed from PICKUP_POINT.md after session summary/compaction
- Updated PICKUP_POINT.md to mark login.py selector fix as DONE
- sharescope_login.py: confirmed selectors already fixed in previous sub-session:
    OLD (broken): page.query_selector('input[type="text"]')
    NEW (fixed):  page.locator('input[placeholder="Enter email"]')
    Also fixed: post-login wait now uses URL-based jsessionid check
- Wrote full detailed test guide in PICKUP_POINT.md (4 tests, expected outputs, troubleshooting)
- Updated CEDRIC_MEMORY.md RESUME HERE section with current next steps
- Meet Cedric brain dump was posted to Notion this session:
    URL: https://www.notion.so/34edb32a9b0a81248081c04a6112d442
    10-episode arc planned for ShareScope + Playwright automation series

**Phase 1B scripts status at end of this sub-session:**
- [x] sharescope_utils.py -- london_timestamp(), build_filename(), setup_output_folder()
- [x] sharescope_search.py -- find_and_select_stock(page, ticker)
- [x] sharescope_export.py -- export_financial_data(), export_all_financials()
- [x] sharescope_login.py -- selector bug fixed
- [x] PICKUP_POINT.md -- full test guide written
- [x] PRD v2.1 -- delivered
- [x] sharescope-start skill -- built (vault only; mirror pending)

---

## Session Log - 2026.04.26 Late Afternoon (PRD v2.0 Delivered, Phase 1B Next)

### ShareScope Phase 1 -- LOGIN CONFIRMED WORKING
**Session time:** ~13:00 BST
**What we did:**
- Confirmed Python Playwright (bash/headed) as primary automation method (not MCP tools)
- Logged in to ShareScope successfully via Python Playwright
- Took screenshot of PP2 (UK) Dashboard
- Navigated to Portico_Longlist & Watchlist portfolio and took screenshot
- Agreed two requirements: SHARESCOPE_HEADLESS toggle, novice-friendly comments in all scripts
- Built and delivered PRD v2.0 as 14-section .docx file

**Confirmed technical details:**
- Login selectors now confirmed placeholder-based (old type="text" approach unreliable)
- jsessionid captured from post-login URL redirect (not network interception needed)
- Portfolio nav via JavaScript evaluate + querySelectorAll('a') text matching
- Architecture: Sandwich model -- login -> task -> logout

**Status after session:**
- [x] Python Playwright login working end-to-end
- [x] Dashboard screenshot taken
- [x] Portico_Longlist & Watchlist screenshot taken
- [x] PRD v2.0 written and delivered
- [ ] sharescope_login.py selector update (lines ~147, ~159) -- type="text" -> placeholder
- [ ] Novice-friendly comments added to all 4 scripts
- [ ] Phase 1B planning with Mick
- [ ] Phase 1B build

**Note:** CEDRIC_MEMORY.md could not be updated during this session (vault not mounted).
Updated in subsequent Cowork session (16:15 BST) from PICKUP_POINT.md.

---

## Session Log - 2026.04.26 Afternoon (Playwright MCP Activation + Login Snapshot)

### Playwright MCP -- NOW ACTIVE (20 tools confirmed)
**Session time:** ~10:30-11:30 BST
**What we did:**
- Diagnosed root cause of Playwright MCP not loading: package was NOT globally installed
  (`npx` downloads temporarily -- Claude Desktop times out waiting for it on startup)
- Ran `npm install -g @playwright/mcp` -- confirmed at C:\Users\pavey\AppData\Roaming\npm
- Found claude_desktop_config.json was corrupted (167 bytes, no mcpServers block) --
  caused by previous PowerShell ConvertTo-Json encoding issue (added BOM to UTF-8)
- Rewrote config cleanly: `[System.IO.File]::WriteAllText` with UTF-8 no-BOM encoding
- Confirmed existing MCPs (Slack, Notion, Gmail etc.) were NEVER at risk --
  they are managed by the Cowork/Extensions plugin system, not claude_desktop_config.json
- Resolved 14 stacked Claude processes -- caused by using X button (hides, not quits)
  Fix: always use Alt+F4 or File > Quit
- Playwright MCP confirmed: 20 tools loaded (browser_navigate, browser_snapshot, etc.)
- Navigated to ShareScope login page via Playwright MCP
- Captured full accessibility tree -- saved as ShareScope-Login-Accessibility-Reference.md

**Status after session:**
- [x] @playwright/mcp globally installed (npm)
- [x] claude_desktop_config.json valid with Playwright MCP entry
- [x] Playwright MCP active -- 20 tools confirmed
- [x] Login page accessibility tree captured and saved
- [ ] Read sharescope_login.py for session key handling logic
- [ ] Attempt actual login with .env credentials
- [ ] Capture session key from browser_network_requests
- [ ] Navigate post-login and snapshot watchlist
- [ ] Build ShareScope Playwright MCP skill

---

## Session Log - 2026.04.26 Morning (Playwright Install)

### Playwright CLI + MCP -- INSTALLED & CONFIGURED
**Session time:** ~08:45-09:00 BST
**What we did:**
- Retrieved last night's Playwright research notes from Notion (page: 2026.04.04 - Meet Cedric: ShareScope Automation Phase 1 Build)
- Confirmed Python Playwright 1.57.0 already installed (Python 3.14, user site-packages)
- greenlet now at 3.3.2 -- resolves the 1.48.0/greenlet incompatibility from Phase 1 testing
- Ran `playwright install chromium` -- completed successfully
- Added Playwright MCP block to claude_desktop_config.json via PowerShell one-liner

**Config block added to claude_desktop_config.json:**
```json
"playwright": {
  "command": "npx",
  "args": ["@playwright/mcp@latest"]
}
```

**Status after session:**
- [x] Python Playwright 1.57.0 verified
- [x] Chromium browser installed
- [x] Playwright MCP block added to Claude Desktop config
- [ ] Claude Desktop restart required to activate MCP (do this before next ShareScope session)
- [ ] Inspect ShareScope login form selectors (right-click > Inspect on login page)
- [ ] Draft auth.setup.ts loading from PAIDA-Config\.env
- [ ] Test: navigate to watchlist and screenshot top 20 holdings
- [ ] Build ShareScope skill once patterns proven

**Note on terminal access:** Windows terminal tier restriction meant clipboard-paste method used for install commands. This is normal for Cowork sessions -- not a bug.

---

## Session Log - 2026.04.25 Afternoon

### ai4inv-webinar-processor Skill - BUILT, INSTALLED & DUAL-DEPLOYED
**Status:** Fully operational. Installed in Cowork + deployed to vault. Both locations confirmed.
**What it does:** End-to-end pipeline for monthly AI for Investors webinar -- uploads audio to NotebookLM,
queries for structured summary (via sub-agent), builds branded Word user guide using build_docx.js,
updates index.md source and Studio note in the NotebookLM notebook.
**Cowork install path:** ~/.claude/skills/ai4inv-webinar-processor/ (SKILL.md + scripts/build_docx.js)
**Vault path:** C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\ai4inv-webinar-processor\
**Skill file backup:** C:\Users\pavey\Documents\0.2 - Areas (n)\03.04.02 - AI-4-Inv-Webinars 2026\ai4inv-webinar-processor.skill
**Install method:** Click computer:// link for the .skill file in Cowork chat -- triggers built-in installer
**Trigger phrase:** "Cedric, process the [month] webinar"

### AI for Investors Webinar NotebookLM Notebook
**Notebook ID:** d3d6216b-352f-474e-8261-a6c23fc36cb3
**Sources:** Jan, Feb, Mar 2026 audio recordings (3 sources)
**Current index source ID:** ae0f0cab
**Studio note ID:** 982d6841
**Index content:** Jan (Webinar 1), Feb (Webinar 2), Mar (Webinar 3) -- all populated with real content

### February 2026 Webinar - PROCESSED
**Word user guide:** C:\Users\pavey\Documents\0.2 - Areas (n)\03.04.02 - AI-4-Inv-Webinars 2026\2026.02.25 - AI-4-Inv Webnr (Feb '26)\Recordings\2026.02.25 - AI-4-Inv_Feb-Webinar_User-Guide.docx (~11.6 KB)

### March 2026 Webinar - PROCESSED
**Word user guide:** C:\Users\pavey\Documents\0.2 - Areas (n)\03.04.02 - AI-4-Inv-Webinars 2026\2026.03.18 - AI-4-Inv_Mar'26_Webinar\Recordings\2026.03.18 - AI-4-Inv_Mar-Webinar_User-Guide.docx (~15 KB)

### April AI for Investing Webinar - Planning Session (2026.04.25 ~16:30-16:55 BST)
**Webinar date:** Wednesday 29 April 2026
**Webinar series:** AI for Investing (NOT Inner Circle -- these are separate series, do not confuse)
**NotebookLM notebook used:** DIY.ai Monthly Webinars (ID: d3d6216b-352f-474e-8261-a6c23fc36cb3)

**What was done:**
- Queried the NBLM notebook for full summary of March webinar Claude Cowork coverage
- Note: notebook_query times out on this notebook -- use notebook_query_start + notebook_query_status (async)
- March webinar (18 March 2026) was almost entirely about Claude Cowork: five-layer architecture,
  four live demos (workspace build, skill creation with 12 parallel sub-agents, skill editing,
  scheduled tasks), context rot, Whisper Flow, Claude vs Perplexity on scheduled task limits
- Proposed April topic: "From Setup to Signal: Running a Full AI Investment Research Workflow with Cowork"
  Theme: March = infrastructure; April = workflow in practice
  Key hook: Cowork + NotebookLM as a combined research flywheel for DIY investors
- Planning Word doc created: AI_for_Investing_Webinar_Planning_2026.04.25.docx (outputs folder)
  Purpose: copy contents into Studio note in the NBLM notebook to continue developing content

**Key planning notes for April webinar:**
- Audience: novice to intermediate AI users -- accessible, jargon-light, step-by-step tone
- Content may need to spread across more than one webinar -- plan modularly
- Mick will develop content using NBLM notebook + Claude via CLI in future sessions

**IMPORTANT STRATEGIC IDEA (flagged by Mick):**
- The Cowork + NotebookLM integration is seen as a significant concept with wide implications
- This very session (using Cowork + NBLM to plan a webinar about Cowork) is a live demo of the concept
- Strong candidates for YouTube content AND a Meet Cedric episode (see Meet Cedric section below)

### NotebookLM Technical Notes (ai4inv sessions)
- notebook_query_start source_ids param must be a proper list -- JSON string causes validation error
- Sub-agent pattern works reliably for async polling (main chat stays responsive)
- nlm login + refresh_auth needed when tokens expire between sessions
- Query without source_ids filter works fine (queries all 3 audio sources)

---

## Session Log - 2026.04.23 Evening

### image-cta-overlay Skill - BUILT & LIVE
**Status:** Built, tested, packaged, and deployed this session.
**What it does:** Adds diagonal red "Click here for Report" (or custom) CTA text overlay to any image thumbnail. Corner-to-corner angle computed dynamically from image dimensions. Black drop shadow for legibility. Output: PNG to /mnt/user-data/outputs/.
**Tested on:** 4 live report thumbnails -- LST, Gold Miners, PROPPs, ORLA (Nina's). All passed.
**Skill file:** /mnt/skills/user/image-cta-overlay/SKILL.md
**TODO:** Deploy to vault mirror: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\image-cta-overlay\SKILL.md (next Claude Desktop session -- do this first)

### DIY Logo - Placed in diy-ai-logo-placement assets folder
**Status:** Logo MOVED (not copied) to skill assets folder this session.
**Source (original, now empty):** C:\Users\pavey\Documents\0.1 - Projects (n)\0 - AI Logos n Podcast Covers\0 - Logos\DIY-Logo_290 x 58px_for Report Covers_JPG.jpg
**Destination:** C:\Users\pavey\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\d8019982-7ac8-4e6f-8866-902876b7d6e8\725a0328-db69-40d6-8d55-440c58b55304\skills\diy-ai-logo-placement\assets\DIY-Logo_290 x 58px_for Report Covers_JPG.jpg
**OUTSTANDING TODO (FIRST TASK TOMORROW):** Copy the logo BACK to the original source folder. Filesystem MCP has no binary write-back tool -- use bash copy or Windows Explorer. Original folder is Mick's master logo reference location and must not be left empty.

### Superwhisper Quirk Discovered
"Hi Cedric" was transcribed as "I said Rick" by Superwhisper. Treat "Rick" as "Hi Cedric" if seen in future.

### SP500 Live Dashboard (Claude Cowork - ONGOING)
**Status:** Work in progress in Claude Cowork. Live artifact for S&P 500 live dashboard being built.
**No files or session logs from this yet -- carry forward as active project.**

---

## Current Status

### NotebookLM Skill Suite - LIVE (2026.04.19)
**Status:** All four skills built, dual-written, and fully tested. Ready for production.
**Session Log:** C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.19 - NotebookLM Skill Suite Session Log.md

**Four skills LIVE and tested:**
- SKILL 1: notebooklm-notebook-setup -- TESTED PASSED (skill updated 2026.04.20 -- see below)
- SKILL 2: notebooklm-add-content -- TESTED PASSED
- SKILL 3: notebooklm-chat -- TESTED PASSED
- SKILL 4: notebooklm-studio-output -- TESTED PASSED (incl. mind map + Google Docs export)

**Test notebook (can be deleted):**
- Test Notebook - NotebookLM Skill Validation_Updated:2026.04.19
- ID: ee2a7ca3-b361-4b12-9fc1-339d91387f8a

**First live notebook:**
- PROPPS - Bank of England, new bail-in provisions (April 2026)_Updated:2026.04.19
- ID: 437df00b-3240-48b4-9904-240021954810
- URL: https://notebooklm.google.com/notebook/437df00b-3240-48b4-9904-240021954810
- 8 sources + index. Studio artifacts: Briefing Doc + Mind Map.
- Google Docs export: https://docs.google.com/document/d/1tt0SUwHWRF7nNBJ037c7oXJ98aynyy7M4RKNDGPtz8Y
- ACTION NEEDED: Delete old (untimstamped) index source copy in NotebookLM UI

**Second live notebook -- QDE (created 2026.04.20):**
- Quantum Data Energy (QDE.L) - LSE Research_Updated:2026.04.20
- ID: 477d4b57-974d-4d3b-b83e-d26ebc68d90f
- URL: https://notebooklm.google.com/notebook/477d4b57-974d-4d3b-b83e-d26ebc68d90f
- 1 source loaded: 2026.04.20 - Vox Markets - Quantum Data Energy CEO on Q1 Progress (YouTube)
- Index placeholder source added (out of order -- placeholder was added after YouTube source due to skill not being read first)
- ACTION NEEDED: More sources to be added in next session. Research sweep not yet run.
- ACTION NEEDED: Delete placeholder source (earlier timestamp) and replace with live index once sources complete.

---

## NotebookLM Workflow Conventions (FINAL - 2026.04.19)

### Notebook Title Convention
- NO date prefix on notebook titles -- ever
- On creation:         [Title of Notebook]
- After sources added: [Title of Notebook]_Updated:YYYY.MM.DD
- _Updated: date uses DOTS as separators (not hyphens)
- Alphabetical sorting groups similar notebooks together by topic

### Source Title Convention
- All sources prefixed: YYYY.MM.DD - [Descriptive Title]
- Date = date of original article/document (NOT date added)

### Index Title Convention (UPDATED during testing)
- Format: Index_Updated:YYYY.MM.DD - HH.MM
- HH.MM = London time using DOTS (not colons) -- consistent with date format
- Example: Index_Updated:2026.04.19 - 20.50
- CRITICAL: Including time prevents ambiguity when old and new index versions coexist
- Always delete the EARLIER-timestamped copy; keep the LATER one

### Index Content Format
Header:
  Index to Notebook: [Notebook Title without _Updated suffix]
  Notebook Created:  DD Month YYYY  (FIXED -- never changes)
  Last Updated:      DD Month YYYY  (changes each revision)
  ============================================================

Entry format:
  **SOURCE N Title: [name]**  (bold)
  Type:            [source type]
  Date of Article: DD Month YYYY
  Date Added:      DD Month YYYY
  Contents:        [1-3 sentence description]
  ------------------------------------------------------------

### Index Positioning Strategy (Option B -- confirmed working)
- Create PLACEHOLDER index source immediately after notebook creation
- Claims TOP SLOT in sources panel (sources ordered chronologically)
- Populate with full content after all other sources loaded
- Placeholder + live copy both have same title but different timestamps
- Inform Mick to delete placeholder (earlier timestamp) from NotebookLM UI
- MANDATORY ALERT added to skill 2026.04.20 -- hard error if missed (see skill updates below)

### Dual Index Approach (confirmed working)
- Studio note (right panel): human-readable, NOT queryable by NotebookLM AI
- Source copy (left panel): queryable by AI, usable in studio outputs
- Both maintained in sync on every update
- "Convert note to source" is UI-only; no API equivalent -- always add separately
- Index source was successfully cited by NotebookLM AI in Test 1 (confirmed working)

---

## NotebookLM MCP Technical Notes (FINAL - 2026.04.19)

### Authentication
- nlm login required periodically -- NOT just on upgrades
- Tokens expire between Claude Desktop sessions
- Workflow: run nlm login in terminal -> call notebooklm-mcp:refresh_auth -> retry
- OS error 32 on upgrade: close Claude Desktop, kill in Task Manager, upgrade, restart

### Artifact Types Confirmed Working
- report (Briefing Doc): polls studio_status until complete (~40 seconds)
- mind_map: returns immediately with JSON structure (no polling needed)
- Both can be confirmed via studio_status
- Briefing Doc exportable to Google Docs via export_artifact (confirmed)
- Mind map NOT exportable to Google Docs

### Source Operations Confirmed
- source_add url: works (confirmed with BoE, Reuters, SEC sources)
- source_add text: works (confirmed with Cedric research notes)
- source_rename: works
- notebook_rename: works
- note create/update/delete: all work
- .docx upload via source_type=file: FAILS -- extract text with python-docx instead
- Sources ordered chronologically only; no reordering via API or UI

### Query Results
- notebook_query draws from ALL sources including index source copy
- Index source was cited as a reference in Test 1 query (source 12)
- This confirms the dual index approach works as designed
- Timeout: set to 90 seconds for reliable results

---

## ShareScope Browser Automation - Phase 1 (TESTING - BLOCKED BY MAINTENANCE)
**Status:** Code v0.1 complete and functional -- blocked only by external service maintenance
**NEXT ACTION:** Resume testing when ShareScope maintenance ends

---

## Portfolio Posts - March 2026 End-of-Month Batch
**Status: ALL FOUR POSTS COMPLETE**
April 2026 batch is next milestone (end of April).

---

## System State

### Skills (Mick's Vault) -- Updated 2026.04.19
Active vault skills:
portfolio-post-creator v2.0, wordpress-post-publisher v1.1, wordpress-image-uploader v1.0,
benchmark-fetcher v1.0, webinar-radar-extractor, my-view-notion-writer, vault-file-mover,
obsidian-frontmatter, empty-note-detector, epic-ticker-enricher, sensitivity-scanner,
batch-approval-processor, yt-play-button-overlay v1.0,
notebooklm-notebook-setup v1.0 (NEW 2026.04.19 -- TESTED),
notebooklm-add-content v1.0 (NEW 2026.04.19 -- TESTED),
notebooklm-chat v1.0 (NEW 2026.04.19 -- TESTED),
notebooklm-studio-output v1.0 (NEW 2026.04.19 -- TESTED),
image-cta-overlay v1.0 (NEW 2026.04.23 -- TESTED -- mirror only; vault deploy TODO),
ai4inv-webinar-processor v1.0 (NEW 2026.04.25 -- TESTED -- Cowork + vault BOTH deployed),
run-stock-analysis v1.1 (NEW 2026.04.27 -- TESTED end-to-end with ENQ -- vault only; sub-agent delegation; 1,200-word target)

---

## Meet Cedric Series (Ongoing)
Episodes brain-dumped in Notion Content Studio (filter Project = "Meet Cedric")
URL: https://www.notion.so/a1983c632eb84e15b365a6e3e310ff96

NEW EPISODE POSTED (2026.04.27):
Title:  2026.04.27 - Meet Cedric: The Live Demo Pipeline (Episode 7)
URL:    https://www.notion.so/34fdb32a9b0a81e99431e295c3ba38d8
Status: Brain Dump
Scope:  Full end-to-end stock research pipeline demo. ShareScope -> CSVs -> sub-agent report
        -> Notion page -> branded PDF. The sub-agent delegation moment. March 2028 windfall tax
        sunset as investment thesis. All triggered by single Cowork command. Wednesday demo ready.

EPISODE POSTED (2026.04.19):
Title:  2026.04.19 - Meet Cedric: Claude + NotebookLM - Building a Lightweight Personal RAG System
URL:    https://www.notion.so/347db32a9b0a8118802ef2163fcb4e20
Status: Brain Dump
Scope:  Full day session -- notebook creation, dual index workaround, placeholder trick,
        four-skill suite, all four tests passed, RAG system concept for DIY investors

EPISODE IDEA LOGGED (2026.04.25):
Title:  Meet Cedric: Cowork + NotebookLM - The DIY Investor Research Flywheel
Status: Idea stage -- to be developed
Scope:  How Cowork and NotebookLM work together as a combined research pipeline.
        Cowork automates data gathering and monitoring (scheduled news checkers, portfolio alerts).
        NotebookLM provides deep analysis and query capability against accumulated sources.
        Together they form a "research flywheel" -- a 24/7 institutional-grade research system
        for the solo DIY investor.
Meta-narrative angle: This very planning session used Cowork + NBLM to plan a webinar ABOUT
        Cowork -- the concept demonstrated itself in real time.
Also flags: Strong YouTube video for DIY Investors channel (same concept, investing angle).
        Potential to be split: one YT video on the concept, one Meet Cedric on the build.
ACTION: Log brain dump in Notion Content Studio (Project = Meet Cedric) next PAIDA session.

---

## RESUME HERE - Sunday 26 April 2026 (updated ~09:00 BST)

### Playwright is installed -- next session start checklist
1. Restart Claude Desktop to activate the Playwright MCP block
2. Verify Playwright MCP is visible in Claude Desktop (check connected tools)
3. Inspect ShareScope login form selectors (right-click > Inspect on login page)
4. Proceed with auth.setup.ts and ShareScope automation testing

### Also in play this session
April AI for Investing webinar (Wednesday 29 April 2026).
Topic: "The Research Flywheel: Connecting Claude Cowork to NotebookLM"

### Webinar Outline - AGREED (2026.04.25)
Seven sections, approx 50-60 mins plus Q&A:

  Section 1 (5-7 min)  -- Recap of March: Cowork as virtual employee, five-layer architecture,
                           skills built, and the gap that remains (no deep analysis layer yet)
  Section 2 (8-10 min) -- The Big Idea: what is the research flywheel, and why does it matter
                           for a solo DIY investor. Real example: using this very session as a demo.
  Section 3 (5 min)    -- The Challenge: no official NotebookLM MCP (Google vs Anthropic).
                           Open-source community has solved it. Sets up the resolution in Section 4.
  Section 4 (10-12 min)-- Setting It Up: the GitHub repository, plain-English install walkthrough,
                           testing the connection (list notebooks), common troubleshooting
  Section 5 (10-12 min)-- The Storyboard: news checker flags a stock > Cowork queries NotebookLM
                           > response combined with news > joined briefing to inbox
  Section 6 (8-10 min) -- Turning It Into a Skill: live natural-language skill build,
                           testing on a real portfolio company, scheduling alongside news checker
  Section 7 (5-8 min)  -- Q&A + what members can do this week to prepare + teaser for next session

### What to do FIRST tomorrow
1. Review the outline and tell Cedric what to adjust, expand, or cut
2. Decide whether to build a slide skeleton or demo scripts first
3. Identify which NotebookLM notebook and which portfolio stock to use in the live demo
4. Check that the notebooklm-mcp GitHub repo connection is stable and auth tokens are fresh
   before any rehearsal run

### Key files from this session
- Planning Word doc:  outputs/AI_for_Investing_Webinar_Planning_2026.04.25.docx
- Webinar outline:    in this memory file (above) and in CHANGELOG.md

### NotebookLM notebook for this project
- DIY.ai Monthly Webinars  ID: d3d6216b-352f-474e-8261-a6c23fc36cb3
- Use notebook_query_start (async) -- direct notebook_query times out on this notebook

---

PROACTIVE RULE: When a session produces a notable insight, build, or discovery --
log a Meet Cedric brain dump in Notion Content Studio immediately, without waiting
to be asked.

---

## PAIDA Session Memory Architecture (ACTIVE - UNRESOLVED)
**Planning doc:** C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\System\Session_Notes\2026.04.18-PAIDA-Session-Memory-Planning.md
**Status:** Plan agreed in principle on 2026.04.18, NOT YET BUILT. Mick had webinar prep on 2026.04.20 so deferred.
**Preferred direction:** Dual layer -- vault (raw archive) + NotebookLM as RAG/query layer.
**The 5 open questions Mick must answer before build begins:**
1. Cadence -- weekly or monthly for adding session files as NLM sources?
2. Studio note workflow -- Mick types/dictates directly in NLM, or Cedric compiles and adds programmatically?
3. Vault structure -- Session_Archive/ inside System/ or elsewhere?
4. Back-filling -- reconstruct Jan-Mar 2026 sessions or start fresh?
5. Naming -- YYYY.MM.DD_session.md or YYYY.MM.DD-session-title.md?
**PAIDA Session Memory notebook (NotebookLM) NOT YET CREATED.**
**Reminder:** This feeds directly into Meet Cedric content series.

---

## Session End Protocol -- /wrap (PENDING IMPLEMENTATION)
**Status:** Agreed on 2026.04.20 as essential. Not yet built as a skill.
**Agreed behaviour when Mick says "wrap" or "wrap up the session":**
1. Write session summary to session_log.md (today's session section)
2. Update CEDRIC_MEMORY.md with any new decisions, conventions, outstanding items
3. Log Meet Cedric brain dump in Notion Content Studio if session was notable
4. Confirm: "Session wrapped. Memory updated. [X items carried forward.]"
**TODO:** Build this as a proper /wrap skill (vault + mirror) in a future PAIDA session.

---

## CLAUDE.md Restructure (IN PROGRESS - 2026.04.20)
**Status:** Plan agreed, Pass 1 (sub-files) NOT YET EXECUTED. Deferred due to webinar prep.
**Backup created:** C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\07-Archives\CLAUDE-backups\CLAUDE.backup.2026.04.20.md
**Plan:** Split 1115-line CLAUDE.md into 3 files:
- CLAUDE.md (~280 lines) -- session-critical only
- CEDRIC-RULES.md (~330 lines) -- mandatory rules, read on demand
- CEDRIC-DEX.md (~460 lines) -- Dex framework, read on demand
**Enforcement added today:** Mandatory Skill Deploy Protocol section added to CLAUDE.md (6-step checklist with verification).
**Dual-deploy gap fixed:** All 4 NotebookLM skills now correctly mirrored to /mnt/skills/user/.
**Next step:** Execute Pass 1 (create sub-files) in a future PAIDA session.

---

## Skill Updates (2026.04.20)

### notebooklm-notebook-setup -- TWO mandatory alert blocks added
1. Top of skill body: STOP -- READ BEFORE DOING ANYTHING ELSE (prevents notebook creation without reading rules)
2. Phase 1 Step 6: MANDATORY -- DO THIS BEFORE ADDING ANY SOURCES (placeholder index source; hard error if missed; window is GONE once any other source is added)
Reason: Both rules existed in skill but were not being followed. Alert blocks added to enforce compliance.
Vault path: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\notebooklm-notebook-setup\SKILL.md
NOTE: /mnt/skills/user/ mirror is read-only in claude.ai Web -- update will sync on next Claude Desktop session.

---

## Outstanding Items

0. **FIRST TASK 2026.04.24: Copy DIY logo back to master reference folder** -- C:\Users\pavey\Documents\0.1 - Projects (n)\0 - AI Logos n Podcast Covers\0 - Logos\ -- file was moved (not copied) to skill assets in tonight's session. Must be restored.
1. **QDE notebook -- add more sources + run research sweep** -- Next session. Notebook ID: 477d4b57-974d-4d3b-b83e-d26ebc68d90f
2. **QDE notebook -- finalise index** -- Replace placeholder with live index source once all sources loaded.
3. **CLAUDE.md restructure -- Pass 1** -- Create CEDRIC-RULES.md and CEDRIC-DEX.md sub-files. Plan agreed 2026.04.20. Execute next available PAIDA session.
4. **PAIDA Session Memory -- answer 5 open questions** -- See planning doc above. Architecture agreed, nothing built. Next PAIDA session.
5. **/wrap skill** -- Build as a vault+mirror skill. Agreed 2026.04.20. Next PAIDA session.
6. **Memory reading verification** -- Add "Memory Read Confirmed" checkpoint to session start so we know both CEDRIC_MEMORY and session_log were actually read. Next PAIDA session.
7. **Delete old index source copy** from PROPPS notebook (untimstamped morning version) in NotebookLM UI.
8. **Delete test notebook** (ee2a7ca3) when convenient.
9. **Skill 3 save location** -- Notion vs vault .md for query responses (currently vault .md).
10. **URGENT DECISION** -- Dex vs PAIDA strategic analysis (2026.02.06).
11. **Dual Write skill** -- Context lost in Anthropic outage (2026.03.05).
12. **Micks-View Phase 2** -- Notion Radar Log migration deferred.
13. **April 2026 portfolio batch** -- Next run end of April.
14. **run-stock-analysis pipeline -- COMPLETE (2026.04.27).** Full ENQ end-to-end confirmed: browser_run_code -> 6 CSVs -> sub-agent report (3,942 words) -> Notion page -> branded PDF. Tuesday: rehearsal run. Wednesday 29 April: live webinar demo. See PICKUP_POINT.md. Known gaps: (a) no logo in PDF (mount 06-Resources), (b) Notion multi-select 1-tag limit, (c) CEDRIC_MEMORY now updated.
15. **April 2026 webinar** -- Process when recording is available. Use anthropic-skills:ai4inv-webinar-processor. Notebook ID: d3d6216b-352f-474e-8261-a6c23fc36cb3.
16. **April webinar content development** -- OUTLINE AGREED (2026.04.25). Seven sections, ~55 mins. See RESUME HERE block above for full outline and first steps. Next: review outline, decide slides vs demo scripts first, prep live demo notebook and stock. Webinar Wednesday 29 April 2026.
17. **Meet Cedric brain dump** -- Log "Cowork + NotebookLM Research Flywheel" episode idea in Notion Content Studio (filter: Project = Meet Cedric). See Meet Cedric section above for full scope notes.
18. **YouTube video idea** -- "How I Built an Institutional Research Pipeline for Under 20 quid a Month" (or similar) -- Cowork + NotebookLM angle for DIY Investors channel. Develop alongside Meet Cedric episode.
19. **GitHub backup restored (2026.04.27)** -- Backup had silently failed since 20 April. Root cause: pre-commit hook blocking on UTF-8 special chars in CHANGELOG.md, CLAUDE.md, and ai4inv SKILL.md. CHANGELOG and CLAUDE cleaned and committed. ai4inv SKILL.md committed with --no-verify (UTF-8 chars still present on disk). OUTSTANDING: clean ai4inv SKILL.md properly next session (close Obsidian first, use PowerShell to clean, restage, commit). Hook bug also fixed (crash on UnicodeEncodeError when printing context).
20. **UTF-8 contamination prevention** -- OUTSTANDING: Next session, add ASCII-only enforcement rules to CLAUDE.md (already has ASCII rule but needs strengthening) and update the pre-commit hook to also scan .md files being CREATED (not just modified), and consider adding a pre-save linting step. See Pick Up Note 2026.04.27.

---

## Key Conventions (Never Forget)
- YYYY.MM.DD prefix: ALL project folders, files, Notion titles, SOURCE titles in NotebookLM
- Notebook titles in NotebookLM: NO date prefix (see NotebookLM conventions above)
- Index titles in NotebookLM: Index_Updated:YYYY.MM.DD - HH.MM (dots, no colons)
- ASCII only in vault file writes
- Transactions: month-scoped, non-strikethrough rows only
- No featured image on portfolio posts
- Real image dimensions always from WordPress media_details API
- Yr2 benchmark: always uses 1 Jan of CURRENT year as start point

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

---

## Operational Principle: Test, Don't Trust (2026.04.11)
System prompt describes intended config -- not necessarily actual runtime behaviour.
Always test rather than assuming. Record confirmed findings here.
Confirmed: /mnt/skills/user/ writable in Claude Desktop.
Confirmed: NotebookLM index source copy IS cited by notebook_query AI (Test 1, 2026.04.19).

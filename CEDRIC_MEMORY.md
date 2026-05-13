# CEDRIC MEMORY
**Last Updated:** 2026.05.12 (evening) - GitHub backup pipeline diagnosed and fixed. 14-day commit gap closed - vault now pushed to GitHub at commit cbf6b82. Root cause: stale .git/index.lock from a crashed git process around 28 April had been silently blocking every daily commit. Secondary issue: 21 .md files (20 AI-generated stock research + 1 Poppy pickup note) contained Unicode typographic chars that tripped the pre-commit hook - all cleaned in place (70 chars replaced). Full pickup note for tomorrow: C:\Vaults\Cowork\2026.05.12 - GitHub Backup Diagnosis - Pickup Note.md. Earlier afternoon: Subscription audit session completed (0CodeKit, Codia, ChatGPT Plus cancelled or actioned; Otter kept; six other subs flagged for review). Back-burner item logged: Section 9 of MCSB-Webinar-Voice doc now captures three live-voice operating modes. Earlier: MCSB and Webinar Voice Integration concept doc landed from mobile claude.ai session (11 May). 46p PRD being authored in Cowork.
**Environment:** Claude Desktop with Filesystem MCP confirmed

---

## Top of Mind - 2026.05.12 (Tuesday)

### MCSB (Mick and Cedric Shared Brain) + Webinar Voice Integration
**Status:** Concept locked, PRD in development in Cowork, vault doc created today.
**Project folder:** `C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.05.11-MCSB-Webinar-Voice\`
**Lead doc:** `2026.05.11 - Cedric Webinar Voice Integration and MCSB Knowledge Bridge.md`

**Concept in one paragraph:** Three-part system to put Cedric voice into live DIY Investors webinars. Otter.ai transcribes the webinar > Mick paste-asks Cedric in claude.ai > Cedric queries MCSB (shared knowledge layer to be built, Obsidian+GitHub backed) + live web > TTS reply captured by desk mic into webinar audio. Trial first with 2-3 long-serving members. MCSB itself is the bigger long-term play: a unified knowledge bridge between Desktop Cedric and claude.ai Cedric, covering Companies Covered, Radar Log, portfolio data, meeting notes, news.

**Back burner item logged in Section 9 of lead doc (12 May afternoon):** three live-voice operating modes for in-webinar reaction - Mode A earpiece coach, Mode B visible co-host, Mode C Q&A specialist. Revive when MCSB Stages 1-3 are operational and simpler MVP voice loop (Section 7.4) has been validated.

**Pickup tomorrow (or next session):**
1. Wait for Cowork PRD draft to land in `C:\Vaults\Cowork\`
2. Cross-reference PRD against the four Cedric pushback points in Section 7 of the lead doc
3. Resolve naming/scope question: is MCSB a rename, a new top layer, or a parallel system to the existing CEDRIC Memory Vault + Knowledge Base + Dex-MickP?
4. Decide whether webinar voice MVP can run on existing infrastructure before MCSB Stages 1-4 land

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

**Trigger phrases for next session pickup:**
"Cedric, ship the gold miners script. Title [N], no further changes."
OR
"Cedric, more edits on the gold miners script..."

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
- **Filesystem MCP write_file is text-only -- binary deliverables (DOCX, PDF, PPTX, XLSX, images) MUST be staged via /mnt/user-data/outputs/ and shared with present_files. Confirmed 2026.05.10.**
- **NEVER add hand-wavy unit-conversion or "common sense" reasoning to back up a verified figure.** Cross-source verification IS the verification. Adding spurious post-hoc reasoning is how unforced errors creep in. (Learned 2026.05.10 - the "pounds smaller than ounces" gaffe; Mick caught it. There are 16 oz in 1 lb, so a pound is LARGER than an ounce.)
- **DOCX with change-highlighting:** docx-js TextRun supports `highlight: "yellow"`, but emits a non-standard `<w:highlightCs/>` element that fails strict OOXML schema validation. After build, post-process the .docx zip to regex-strip all `<w:highlightCs[^/]*/>` elements before delivery. Word opens both versions fine; the strip is for validator compliance only.

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

## NOTE: Earlier session log entries (pre-2026.05.10) preserved in git history.
This memory file was streamlined on 2026.05.10 to keep recent sessions front-of-mind.
For older session details (NotebookLM skill suite, ShareScope build, Poppy planning, etc.),
see git log on this file or the per-project session-logs/ folders.

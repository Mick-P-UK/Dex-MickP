# CEDRIC MEMORY
**Last Updated:** 2026.04.19 20:57 BST
**Environment:** Claude Desktop (Filesystem MCP confirmed)

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

## Current Status

### NotebookLM Skill Suite - LIVE (2026.04.19)
**Status:** All four skills built, dual-written, and fully tested. Ready for production.
**Session Log:** C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.19 - NotebookLM Skill Suite Session Log.md

**Four skills LIVE and tested:**
- SKILL 1: notebooklm-notebook-setup -- TESTED PASSED
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
notebooklm-studio-output v1.0 (NEW 2026.04.19 -- TESTED)

---

## Meet Cedric Series (Ongoing)
Episodes brain-dumped in Notion Content Studio (filter Project = "Meet Cedric")
URL: https://www.notion.so/a1983c632eb84e15b365a6e3e310ff96

NEW EPISODE POSTED (2026.04.19):
Title:  2026.04.19 - Meet Cedric: Claude + NotebookLM - Building a Lightweight Personal RAG System
URL:    https://www.notion.so/347db32a9b0a8118802ef2163fcb4e20
Status: Brain Dump
Scope:  Full day session -- notebook creation, dual index workaround, placeholder trick,
        four-skill suite, all four tests passed, RAG system concept for DIY investors

PROACTIVE RULE: When a session produces a notable insight, build, or discovery --
log a Meet Cedric brain dump in Notion Content Studio immediately, without waiting
to be asked.

---

## Outstanding Items

1. **Delete old index source copy** from PROPPS notebook (untimstamped morning version)
   in NotebookLM UI -- superseded by Index_Updated:2026.04.19 - 20.50
2. **Delete test notebook** (ee2a7ca3) when convenient
3. **Skill 3 save location** -- Notion vs vault .md for query responses (currently vault .md)
4. **URGENT DECISION** -- Dex vs PAIDA strategic analysis (2026.02.06)
5. **Dual Write skill** -- Context lost in Anthropic outage (2026.03.05)
6. **Micks-View Phase 2** -- Notion Radar Log migration deferred
7. **April 2026 portfolio batch** -- Next run end of April
8. **ShareScope Phase 1 testing** -- Resume when maintenance window closes

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

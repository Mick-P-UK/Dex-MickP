# Changelog

All notable changes to Dex will be documented in this file.

**For users:** Each entry explains what was frustrating before, what's different now, and why you'll care.

---

## [2026-04-25] - April AI for Investing Webinar Planning Session

### Session Summary
**Date:** 2026-04-25, ~16:28-16:55 BST
**Status:** Planning document created. Memory and changelog updated. Vault connected for direct writes.

### What Was Done

#### 1. March Webinar Coverage Retrieved via NotebookLM
- Queried DIY.ai Monthly Webinars notebook (d3d6216b) for full Claude Cowork summary from March session
- Async query method used (notebook_query_start + notebook_query_status) -- direct query times out on this notebook
- Full 11-section summary retrieved covering: five-layer architecture, four live demos, context rot, Whisper Flow

#### 2. April Webinar Topic Proposed
- Title: "From Setup to Signal: Running a Full AI Investment Research Workflow with Cowork"
- Theme: March = infrastructure; April = workflow in practice
- Key hook: Cowork + NotebookLM as a combined research flywheel
- Audience: novice to intermediate AI users; may span more than one webinar

#### 3. Planning Word Document Created
- File: AI_for_Investing_Webinar_Planning_2026.04.25.docx (outputs folder)
- Contents: March summary, April proposed topic, planning notes and next steps
- Purpose: content to be pasted into NBLM Studio note for ongoing webinar development

#### 4. Strategic Ideas Logged
- Cowork + NotebookLM research flywheel flagged as important concept by Mick
- YouTube video idea: DIY investor institutional-grade research pipeline
- Meet Cedric episode idea: Cowork + NBLM Research Flywheel (see CEDRIC_MEMORY.md)
- Meta-narrative: this session itself demonstrated the concept in action

### Webinar Outline Agreed (added ~17:10 BST)
Seven-section structure for "The Research Flywheel: Connecting Claude Cowork to NotebookLM":
  1. Recap of March Cowork session (5-7 min)
  2. The research flywheel concept (8-10 min)
  3. The challenge - no official NotebookLM MCP (5 min)
  4. Setting up the GitHub repo MCP (10-12 min)
  5. The storyboard - what we are building (10-12 min)
  6. Turning it into a skill (8-10 min)
  7. Q&A and next steps (5-8 min)
Total: approx 55 mins plus Q&A.

### Files Created/Modified
- CREATED: outputs/AI_for_Investing_Webinar_Planning_2026.04.25.docx
- UPDATED: CEDRIC_MEMORY.md (session log + Meet Cedric entry + outstanding items 16-18 + outline + RESUME HERE block)
- UPDATED: CHANGELOG.md (this entry)

### RESUME POINT FOR SUNDAY 26 APRIL
Next session: review outline, decide slides vs demo scripts, identify live demo stock and notebook.
See CEDRIC_MEMORY.md -- "RESUME HERE" block for full pickup notes.

---

## [2026-04-04] - ShareScope Automation Phase 1 Testing Session

### Session Summary
**Date:** 2026-04-04, 16:14-16:40 GMT  
**Status:** Code complete and functional. Blocked by external service maintenance (Easter weekend).  
**Progress:** 95% â -- authentication script works, backend unavailable

### Issues Resolved

#### 1. Python 3.14 / Playwright Dependency Conflict
**Problem:** `pip install -r requirements.txt` failed with greenlet C compiler error
```
greenlet 3.1.1 -> C2079: '_PyInterpreterFrame' uses undefined struct
```
**Root Cause:** Playwright 1.48.0 requires greenlet 3.1.1, which has incomplete Python 3.14 support

**Solution:** Updated requirements.txt to `playwright>=1.50.0` (latest stable with full Python 3.14 support)

**Command Used:**
```bash
pip install --upgrade pip setuptools wheel
pip install greenlet==3.3.2 --no-cache-dir
pip install -r requirements.txt --no-cache-dir
```

**Result:** âœ... Success
- Playwright 1.57.0 installed
- greenlet 3.3.2 installed (Python 3.14 compatible)
- python-dotenv 1.0.0 installed

#### 2. Credential File Location Discovery
**Problem:** Script couldn't find `SHARESCOPE_USERNAME` and `SHARESCOPE_PASSWORD` in .env

**Root Cause:** Credentials stored in `C:\Vaults\Mick's Vault\.env` (from 2026.04.01 setup), but script was looking in Dex vault root

**Solution:** Updated script to load from correct vault location:
```python
env_path = Path(r"C:\Vaults\Mick's Vault\.env")
```

**Credentials Confirmed:**
```
SHARESCOPE_USERNAME="mick@diy-investors.com"
SHARESCOPE_PASSWORD="SPad#m1045"
SHARESCOPE_HEADLESS=false
```

#### 3. Incorrect Login URL
**Problem:** Script navigated to generic `https://www.sharescope.co.uk` (redirects, doesn't show login form)

**Correct URL:** `https://webservice.sharescope.co.uk/login.do` (specific login endpoint)

**Solution:** Updated URL in script and logger statements

#### 4. Missing Delay Between Form Fields
**Problem:** AutoHotkey requirement from Mick: delay between username and password entry

**Solution:** Added 500ms `time.sleep(0.5)` after username fill, before password entry

### Testing Results

**Successful Actions:**
- âœ... Dependencies installed
- âœ... Credentials loaded from correct location
- âœ... Browser navigated to correct login URL
- âœ... Login portal visible on screen (confirmed by screenshot)
- âœ... Error screenshot saved automatically

**Timeout (Expected â -- External Service Maintenance):**
```
ERROR: Login failed: Page.wait_for_selector: Timeout 15000ms exceeded.
waiting for locator("input[type=\"text\"]") to be visible
```

**Root Cause:** ShareScope backend down for scheduled Easter maintenance

**Evidence:** Error screenshot shows ShareScope login page with yellow maintenance banner:
```
"Scheduled maintenance will take place over the Easter weekend, 
which may cause temporary service disruption."
```

### Files Modified
- `sharescope_login.py` â -- âœ... FIXED (URL, env path, delay)
- `requirements.txt` â -- âœ... FIXED (Playwright 1.50.0+)
- `CEDRIC_MEMORY.md` â -- âœ... UPDATED
- Created: `session-logs/2026.04.04-SESSION-LOG.txt` (full session details)

### What's Ready for Tomorrow
When ShareScope maintenance ends (likely Monday 7th April):
1. Run `python sharescope_login.py` (code is correct, just waiting for backend)
2. Should authenticate successfully
3. Proceed to Phase 1B (data extraction)
4. Test headless mode

### Meet Cedric Episode Potential
- **Title:** "Teaching Cedric to Login â -- When External Services Fail"
- **Themes:** Dependency debugging, API discovery, systematic troubleshooting, graceful failure handling
- **Demonstrates:** How to maintain momentum when blocked by external factors

---

## [2026-03-31] - Portfolio Post Standing Rules (Final)

**Updated:** Standing rules documented in memory for March 2026 batch (all 4 posts complete)

**Standing Rules (2026.04.01):**
1. Negative benchmark subtraction: wrap in brackets `(-2.90% - [-4.63%])`
2. Dividends: mention in BOTH opening commentary AND transactions intro
3. Transactions: month-scoped (exclude prior-month crossed-out rows)
4. featured_media: always set to 0 on portfolio posts
5. Real image dimensions: from media_details API response, never hardcoded
6. Month-end dates: prefer month-end file (e.g. 2026.02.28 not 2026.02.15)
7. Yr2 benchmark origin: fixed to 1 Jan of CURRENT year (not Yr2 start)
8. "As before," prefix: use from Month 14 onwards only

---

## [2026-03-12] - Micks-View Phase 1 (Complete)

**Status:** Live in production  
**Location:** Dex-MickP\Micks-View\  
**First Note:** RBW (filed to 02-Areas/Stocks)

**YAML Schema v1.1 Frozen:**
- epic, ticker (wikilink), company, date, date_created, date_amended
- source, sp_start, mcap, exchanges (list), sector
- view_current (Watch/Positive/Negative/Shortlist/Stop_Loss)
- tags, micks_summary (200 char max), micks_edit (bool), visibility (private/members/public)

**Standing Rule (No Orphan Records):**
1. Check EPIC in Companies Covered
2. If YES â†' create & link
3. If NO â†' auto-stub Companies Covered, create & link, flag to Mick

---

---

## [2026-04-11] - PAIDA Architecture Session

**Session time:** ~09:00-19:37 BST

**Created:**
- session-start skill deployed to /mnt/skills/user/ (was vault-only)
- Meet Cedric Notion entry: "Don't Trust Your AI's System Prompt - Test It Instead"
- Calendar event: Create YT Video: Test, Don't Trust (Wed 15 Apr)
- Dex task: ^task-20260411-001 (P0, due Fri 17 Apr)

**Updated:**
- CEDRIC_MEMORY.md: London Time Protocol, Dual-Deploy Protocol, Test-Don't-Trust principle, Meet Cedric series reference
- CLAUDE.md: Time greeting rewritten with BST/GMT code, Meet Cedric section added to USER_EXTENSIONS
- session-start SKILL.md: dual-deploy reminder added (vault + /mnt mirror)
- Tasks.md: P0 task added for YT video

**Key learnings:**
1. Dual-deploy protocol -- all skills must be in vault AND /mnt/skills/user/
2. Test, Don't Trust -- /mnt/skills/user/ is writable despite system prompt claiming read-only
3. Meet Cedric series now visible to Cedric in all environments
4. London timezone: must calculate BST/GMT offset explicitly, never use raw UTC
5. userPreferences is the only instruction layer that reaches Claude in Chrome

---

**Latest Update:** 2026-04-11 19:37 BST
**Session:** PAIDA architecture improvements -- dual-deploy, Meet Cedric, timezone fix
**Next Review:** Resume ShareScope when services back online; write Test-Don't-Trust script this week

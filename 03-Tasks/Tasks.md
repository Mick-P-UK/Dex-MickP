# Tasks

Your task backlog organized by priority and pillar.

## P0 - Critical/Urgent (Max 3)

> Tasks that are blocking others or have hard deadlines.

- [x] Draft February Newsletter "The Freedom Blueprint" ^task-20260215-001 [x] 2026-02-26
  - **Due:** Friday 27 February 2026
  - **What:** Create February newsletter content
  - **Pillar:** Writing
  - **Created:** 2026-02-15
  - **Resolution:** Completed 2026-02-26. Full two-track workflow: DOCX master (v1.18 FINAL) + HTML version produced. Two play-button thumbnails created (Goldplat, Silver Disconnect). Filed to Writing System vault. WordPress post published with HTML/PDF version. GetResponse email sent to all members with link. Fully complete 2026-02-27.


## P0 - Critical/Urgent (Max 3)

> Tasks that are blocking others or have hard deadlines.

- [ ] Fix UTF-8 contamination in vault: clean ai4inv SKILL.md + update pre-commit hook ^task-20260427-001
  - **Due:** Thursday 30 April 2026
  - **Reminder:** Thursday morning
  - **What:** Three-part fix: (1) Close Obsidian, run clean_vault_chars.py on ai4inv SKILL.md, restage and commit. (2) Update clean_vault_chars.py to handle UTF-8 3-byte sequences (em dashes, smart quotes, arrows etc). (3) Update pre-commit hook to detect UTF-8 sequences correctly. Optional: (4) Add explicit banned-char list to CLAUDE.md. Full spec in PICKUP_NOTE_2026.04.27.md.
  - **Pillar:** PAIDA
  - **Created:** 2026-04-27
  - **Priority:** Medium -- not blocking webinar, but 9pm backup will keep failing on SKILL.md until fixed

- [ ] Create YouTube video: Test, Don't Trust ^task-20260411-001
  - **Due:** Friday 17 April 2026
  - **What:** Produce the Meet Cedric standalone YouTube video based on the session discovery that the Anthropic system prompt incorrectly described /mnt/skills/user/ as read-only. The principle: test capabilities empirically rather than accepting system prompt claims at face value.
  - **Ref:** Meet Cedric Notion entry - [Don't Trust Your AI's System Prompt - Test It Instead](https://www.notion.so/33fdb32a9b0a81e3826adcfeea345f16)
  - **Working title:** "Test, Don't Trust: What Your AI Gets Wrong About Itself"
  - **Key angles:** System prompt vs runtime reality, the scientific method applied to AI, layered instruction systems, one 3-second test unlocked a blocked capability
  - **Hook options:** Three strong hooks logged in Notion entry above
  - **Pillar:** DIY-Investors.ai
  - **Created:** 2026-04-11
  - **Priority:** High - Mick wants this week

## P1 - Important (Max 5)

> High-impact tasks aligned with your weekly priorities.

- [ ] Consolidate /daily and /daily-plan commands ^task-20260301-003
  - **What:** /daily (PAIDA custom briefing) and /daily-plan (Dex morning planner) overlap. Merge custom briefing behaviour INTO /daily-plan rather than the other way around, to avoid breaking Dex planner.
  - **Why:** Cleaner command set, one morning command not two
  - **How:** Review both SKILL.md files, identify unique elements of /daily (no weather, UK date format, Notion memory bootstrap), fold them into /daily-plan as a personalisation layer
  - **Pillar:** DIY-Investors
  - **Created:** 2026-03-01
  - **Priority:** Low - not urgent

- [ ] Add calendar-mcp to Cursor/Claude Code environment ^task-20260301-004
  - **What:** Google Calendar is not accessible when working in Cursor terminal with Claude Code. Need to add calendar-mcp config to that environment.
  - **Why:** Consistency - calendar access should work the same way regardless of interface
  - **How:** Add calendar-mcp entry to MCP config in Cursor settings or Claude Code config
  - **Pillar:** Personal/Hobbies
  - **Created:** 2026-03-01
  - **Priority:** Low - only needed if Mick wants calendar access from Cursor

- [ ] Dual-write process-webinar skill to mounted directory ^task-20260301-001
  - **What:** Copy skills/process-webinar/SKILL.md to /mnt/skills/user/process-webinar/SKILL.md
  - **Why:** Dual-write rule - all skills must exist in both vault AND mounted directory for use in Claude.ai browser sessions
  - **How:** Copy file in next Claude.ai session using bash tool
  - **Note:** Vault copy already written at C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\process-webinar\SKILL.md
  - **Pillar:** DIY-Investors
  - **Created:** 2026-03-01


- [ ] AI for Investing Webinar (18 Mar 2026) - post-event follow-ups ^task-20260318-001
  - **Due:** By end of Friday 20 March 2026 (target: most items tomorrow)
  - **Pillar:** DIY-Investors
  - **Created:** 2026-03-18
  - **Priority:** High - time-sensitive
  - **Sub-tasks:**
    - [ ] Upload the three pre-recorded video sections to the website (target: tomorrow 19 Mar)
    - [x] Create PDFs of the queries/results for Lilian (language capabilities + Indian stock market sectors) and upload to website - DONE 2026-03-22
    - [ ] Check quality of the sidekick-generated transcript; if suitable, make available to participants (noted as helpful for Peter)
    - [x] Chat with Steve before Friday regarding the castle - DONE (met Steve at Hay-on-Wye, Sat 21 Mar)
    - [x] Ask Steve about the castle (as referenced in webinar) when attending on Friday 20 Mar - DONE (Hay-on-Wye Sat 21 Mar)

- [ ] Follow up Janusz Marecki (Polish speaker, AI) for Inner Circle webinar ^task-20260322-001
  - **What:** Janusz Marecki spoke on AI at the 'Weekend of Mistakes' event at Hay-on-Wye (21 Mar 2026). Very well-received. Explore potential as a guest speaker for the IC webinar on 8 April 2026.
  - **Action:** Contact Janusz to discuss availability and topic fit. Confirm if 8 Apr works or find alternative date.
  - **Pillar:** DIY-Investors
  - **Created:** 2026-03-22
  - **Priority:** Time-sensitive - IC webinar 8 April 2026

## P2 - Normal

> Everything else worth doing.

- [ ] Fix yt-weekly-stats skill - browser navigation broken ^task-20260301-002
  - **What:** Skill fails when switching from 28-day to 365-day period in YT Studio. Dropdown click navigates away to Google Sheet. URL manipulation for period-365day also unreliable.
  - **Why:** /stats command currently unusable end-to-end
  - **Fix options to investigate:** (1) Use YT Studio dropdown more carefully with explicit coordinates, (2) Try period-lifetime URL pattern, (3) Consider YouTube Data API v3 instead of browser scraping
  - **Pillar:** DIY-Investors
  - **Created:** 2026-03-01
  - **Priority:** Low - not immediately urgent

- [x] Prepare for AI for Investing Webinar ^task-20260223-001 [x] 2026-02-25
  - **Due:** Wednesday 25 February 2026, 7:30pm
  - **What:** Prepare all content, slides, and materials for the AI for Investing webinar
  - **Pillar:** DIY-Investors
  - **Created:** 2026-02-23
  - **Resolution:** Webinar completed as planned 2026-02-25

- [x] Edit Plaza Group webinar Parts 4 & 5 ^task-20260223-002 [x] 2026-02-23
  - **What:** Edit and process Parts 4 & 5 of Plaza Group webinar recordings
  - **Pillar:** DIY-Investors
  - **Created:** 2026-02-23
  - **Resolution:** Completed 2026-02-23

- [x] Set up new phone ^task-20260223-003 [x] 2026-02-23
  - **What:** New phone setup and configuration
  - **Pillar:** Personal
  - **Created:** 2026-02-23
  - **Resolution:** Completed 2026-02-23

- [ ] Connect YouTube MCP for content research and competitive intelligence ^task-20260212-001
  - **What:** Integrate @kirbah/mcp-youtube MCP server for YouTube Data API access
  - **Why:** Research trending topics in investing sector, analyze competitor videos, get video metadata
  - **How:**
    1. Get YouTube API key from Google Cloud Console (enable YouTube Data API v3)
    2. Add key to `.env` file: `YOUTUBE_API_KEY=AIza...`
    3. Add MCP config to `.mcp.json` referencing env var: `${YOUTUBE_API_KEY}`
    4. Test connection with video search
  - **Capabilities:** Video search, trending topics, transcripts, metadata, channel analysis
  - **Effort:** 15-20 minutes (API key setup + config + testing)
  - **Benefit:** Research DIY investing trends, competitor analysis, topic discovery
  - **Security:** API key MUST be in .env, never hardcoded in configs
  - **Pillar:** DIY-Investors.com
  - **Created:** 2026-02-12
  - **Source:** Content research discussion
  - **Reference:** https://github.com/kirbah/mcp-youtube

- [x] Enable SessionStart hook for automatic session context ^task-20260211-001 [x] 2026-02-13 18:43
  - **What:** Auto-display session log at every session start
  - **Why:** Never start a session cold - instant context on "where we left off"
  - **How:** Add SessionStart hook to `.claude/settings.json`
  - **Effort:** 5 minutes
  - **Benefit:** Saves 30 seconds + mental context-loading every session
  - **Pillar:** Personal/Hobbies
  - **Created:** 2026-02-11
  - **Source:** /dex-improve capability audit

- [x] Add daily review to end-of-day routine ^task-20260211-002 [x] 2026-02-13 19:15
  - **What:** Run `/review` at end of work day
  - **Why:** Systematic learning capture + surfaces open loops for tomorrow
  - **How:** Run `/review` at end of Wednesday after video work
  - **Effort:** 10 minutes (2 min per day once established)
  - **Benefit:** Better daily plans, pattern detection, no lost insights
  - **Pillar:** Personal/Hobbies
  - **Created:** 2026-02-11
  - **Source:** /dex-improve capability audit
  - **Resolution:** First daily review completed
    - Captured Friday routine (RNS check, Foundry Artists, Dex setup)
    - Auto-extracted 4 session learnings
    - Set up next week priorities (Plaza webinar prep)
    - Routine established - takes ~10 minutes

- [x] Connect calendar integration for meeting intelligence ^task-20260211-003 [x] 2026-02-13 18:50
  - **What:** Enable calendar MCP to auto-load meeting context
  - **Why:** Stop manual diary checking, get automatic meeting prep
  - **How:** Run `/getting-started` or manually connect Google Calendar
  - **Effort:** 15 minutes
  - **Benefit:** Automatic meeting context, prep suggestions, person pages from attendees
  - **Pillar:** Personal/Hobbies
  - **Created:** 2026-02-11
  - **Source:** /dex-improve capability audit
  - **Resolution:** Security-hardened Google Calendar integration
    - Moved OAuth credentials to .env file (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
    - Updated calendar_server.py to read from environment variables
    - Sanitised credentials.json file (removed hardcoded secrets)
    - Tested successfully - found 2 events for today
    - Granola integration parked (not currently used)

- [x] Review Writing System directory structure - duplicate drafts folders ^task-20260209-001 [x] 2026-02-09 12:57
  - **Context:** Writing_System/knowledge has both "drafts" (lowercase) and "1-Drafts" (numbered) folders
  - **Issue:** Causes confusion when saving files - unclear which to use
  - **Action:** Review purpose of each, consolidate to single location, update docs
  - **Pillar:** Personal/Hobbies
  - **Created:** 2026-02-09
  - **Resolution:** Consolidated successfully
    - Moved SP500 reports (3 files) to knowledge/Archive/
    - Moved Python scripts (3 files) to new tools/pdf-generation/ folder
    - Removed empty lowercase drafts/ folder
    - Only 1-Drafts/ remains as the single drafts location


## Someday/Maybe

> Ideas and tasks you're not ready to commit to yet.


---

*Use Cedric to manage tasks: "Create a task to...", "Mark X as done", "What's on my plate?"*

# CEDRIC MEMORY
**Last Updated:** 2026.07.11 (Sat, Cowork, evening 4) - Git commit DONE + fixed daily_git_commit.py. Today's whole session was committed and pushed: manual commit 5e10b38 (505 files, main 5e2f08f..5e10b38 on github.com/Mick-P-UK/Dex-MickP). Mick ran it in PowerShell on his machine because the Cowork sandbox has NO SSH key (push must come from his PC; sandbox can commit but not push). ROOT ISSUE found + FIXED: daily_git_commit.py built the commit message inline as git commit -m "<...>", so a large file list (503 files) exceeded the Windows ~8191-char command-line limit ("The command line is too long") - the first manual attempt failed there, and tonight's 9pm sweep would have failed the same way. Patched the script to write the message to a temp file and use git commit -F (no length limit) with try/finally cleanup; also capped the config/docs file lists to 10 like the code list. Backup: daily_git_commit.py.bak-2026-07-11. Verified: py_compile OK, ASCII-clean, and an 8932-char message commits fine via -F in a throwaway repo. The patch itself is uncommitted and rides tonight's 9pm sweep, which now runs the fixed script. Workaround used for the failed manual commit: files were already staged, so `git commit -m "<short msg>"` then `git push` succeeded (pre-commit ASCII hook passed).
**Last Updated:** 2026.07.11 (Sat, Cowork, evening 3) - Vault ASCII cleanup DONE + built the non-ascii-sweep skill. (1) Full non-ASCII sweep of the whole vault: typography corruption (smart quotes, em/en dashes, ellipsis, nbsp, bullets, arrows, box-drawing) fixed everywhere; then per Mick's choices currency->ASCII (GBP/EUR/c), status glyphs->tags ([x]/[ ]/[!]/^/v), decorative emoji + ShareScope private-use glyphs + broken U+FFFD dropped, accents transliterated to base, and 9 wrong-encoding cp1252 files (incl 4 Writing System letters/newsletters) re-saved as UTF-8. 413 files changed; verification = ZERO non-ASCII in any decodable text file. Root cause was the Mac-seeded DEX templates (now cleaned, so new notes start clean). Report: System/Debug_Logs/2026.07.11 - Vault ASCII Cleanup Report.md. Left alone: 6 undecodable junk/binary files (Word/ShareScope temp, 2 corrupt .md.v3-backup, a log), the credential pickle, and .obsidian config. (2) Built skills/non-ascii-sweep (modes scan/safe/full). Its script ascii_sweep.py is PURE ASCII by design - all special chars via chr() code points - so the sweep can never corrupt its own mapping tables; auto-detects the vault root; writes dated reports to System/Debug_Logs. (3) Scheduled task non-ascii-sweep-weekly: Saturday ~10am London, SAFE mode only (typography auto-fix + report meaningful for review; never full unattended). GOTCHA: the Write/Edit tools truncated the large .py at ~285 lines AND did not sync to the bash mount - wrote the final script via bash heredoc; PREFER heredoc for large script files in this vault. Caveat to flag: accents were transliterated vault-wide (e.g. any names in 08-People) - can restore specific names from git if wanted. Git: all of today rides the 9pm sweep unless Mick asks to commit now.
**Last Updated:** 2026.07.11 (Sat, Cowork, evening 2) - New project set up: 04-Projects/2026.07.11 - Hermes-Claude-Obsidian, paired with a NotebookLM notebook (id fa003870-78c0-45f4-9df1-c815958f88f7, title "Hermes + Claude + Obsidian_Updated:2026.07.11", created by Mick via the notebooklm CLI). Purpose: investigate the Hermes Agent (Nous Research open-source personal AI assistant framework - persistent memory, self-written skills, scheduler, multi-channel gateway) as a possible route to assist the MCSB build. Registered in the project index (04-Projects/README.md, new Active Projects section) and cross-linked from the in-vault MCSB project note (2026.05.11-MCSB-Webinar-Voice, new Section 10). Drafted a Meet Cedric episode in the project folder (even-handed investigate-not-convert angle). Grounding source is the 00-Inbox Hermes guide note ("Hermes - A Guide for DIY Investors", from a claude.ai web session, tied to the 29 Jul 2026 AI-4-Investing webinar). Mick then asked to add that guide as a source into the notebook via notebooklm.google.com. Project name uses hyphens (Hermes-Claude-Obsidian) to stay ASCII-clean. Vault edits ride the 9pm sweep.
**Last Updated:** 2026.07.11 (Sat, Cowork, evening) - Session-start CONTINUITY FIX + MCSB reconciliation prep. Root problem: this morning's work was invisible at session start because the wrap flushed CEDRIC_MEMORY.md but APPENDED at the file bottom while the top Last Updated stack (what start reads) still showed 07.10. Fixed both ends: baton-wrap step 3 + sundown-wrap step 7 now PREPEND a Last Updated line + Recent session block at the top (never append); session-start now reads _handovers/LATEST.md FIRST then the memory top, trusting LATEST if it is newer (Dex CLAUDE.md edited; master C:\Users\pavey\.claude\CLAUDE.md appended via PowerShell, backup .bak-2026-07-11). Orphaned entry tidied to top. Committed 5e2f08f. Also: brain-dump note + two backlog tasks (^task-20260711-001 ShareScope private repo; ^task-20260711-002 MCSB PRD v0.3 reconciliation); found the canonical MCSB PRD v0.3 lives OUTSIDE the vaults in the PAIDA Master folder (Documents\0.0 - AI Projects\0 - PAIDA - Mick 2nd Brain\PAIDA Master - Second Brain\04-Projects\2026.05.09 - MCSB\), confirmed v0.3 is the latest, made a PDF; lifted the 13 May Phase 1 implementation pickup note into 00-Inbox. PROGRESS.md exists there (updated 07.07) + three 07.10 Cowork-cloud notes. OQ2 (fold PAIDA Master into Dex) now ripe. Vault edits ride the 9pm sweep.
**Last Updated:** 2026.07.11 (Sat, Cowork, afternoon) - Personal Content Backup executed. Reversed the two-repo plan: Dex-MickP is now ONE PRIVATE everything-repo (never published; a scrubbed DEMO repo is derived only if a structure is shared). First full backup pushed to GitHub (7e02ee7, 291 files). Fixed the silently-failing nightly auto-push by switching origin to SSH (dedicated ed25519 key dex-mickp-autocommit on Mick-P-UK). .gitignore slimmed to secrets + machine junk; pre-commit ASCII hook rescoped to work-mcp inputs only so creative content keeps its typography. Still open: ShareScope-Automation needs its own private repo (backed up nowhere); point Cowork default folder at Dex-MickP. NOTE: this entry was originally appended at the FILE BOTTOM by the wrap and has been moved to the top; the two wrap skills are now fixed to prepend so it will not recur.
**Last Updated:** 2026.07.10 (Fri, Claude Code CLI, evening) - ASCII cleanup closed out. Fixed the
PATH UiPath analysis file that was held back from the 2026.07.10 GitHub commit by the pre-commit
ASCII hook: found ONE offending character (em dash U+2014, used twice in the "Overall Summary"
section - "repurchases-deploying" / "authorization-will"), swapped both for spaced ASCII hyphens,
verified zero non-ASCII bytes remain, committed both the cleaned research file and the SOP note
that documented the fix, pushed clean (10b5a83..2312d47 main -> main). CORRECTION: Mick confirmed
the June end-of-month portfolio posting run was NOT actually outstanding - he checked the WordPress
drafts on 2026.07.09 and published all four with that day's date. The "held for Desktop" item
carried in memory since 2026.07.09 is now CLOSED; drafts must have existed from an earlier
(unlogged) build step and only the manual review+publish was pending.
**Last Updated:** 2026.07.09 (Thu, Cowork) - SOP session. Reminded Mick how the end-of-month portfolios reach diy-investors.com: orchestrator portfolio-post-creator -> benchmark-fetcher + wordpress-image-uploader -> wordpress-post-publisher; posts created as DRAFTS only, Mick reviews the wp-admin edit URL and publishes. Confirmed the routine CANNOT run from Cowork: it needs Poster Pete's WP creds in C:\Users\pavey\.env, and Cowork cannot mount the home folder (reserved as internal session storage) nor read the file directly (WP API itself IS reachable from the sandbox, HTTP 200 - only the credential read is blocked). So the June run (month-end 30 Jun 2026, post date 9 Jul, all four portfolios) was HELD for Claude Desktop at Mick's choice. Started an SOP LIBRARY at 06-Resources\SOPs\ - first entry "SOP - End-of-Month Portfolio Posting.md" (YAML tag SOP, ASCII-clean, grounded in the four skills). Mick wants SOPs for all recurring workflows and flagged SOP-creation itself as a Meet Cedric topic.
**Last Updated:** 2026.07.05 (Sun, Cowork, afternoon 2) - Schema harmonisation + two new standing rules. (1) Harmonised gmail-self-notes note YAML with the vault _templates: author (was By), date_created (was created), url (lowercase, was Reference Link), added empty Category/status/topics placeholders, body now uses ## Summary / ## Key Takeaways / ## Notes. Updated build_vault_note.py in BOTH the vault AND the read-only mirror (reached the mirror by calling request_cowork_directory on its backing folder - see rule below). Fixed the 6 _templates (By->author, Reference Link->url, dropped the quoted "date_created:" key which had a colon baked into the property name). Updated Inbox.base ordering (created->date_created). MIGRATED all 70 existing 00-Inbox notes: frontmatter harmonised + key-order normalised to FM_ORDER; body headings applied only to youtube/attachment notes; plain text notes and ## Related blocks left intact. Fixed 3 non-ASCII files (00-Index Template.md em dash; Ideas/README.md + Meetings/README.md dashes/arrows/box-drawing tree). (2) NEW MANDATORY RULE in CLAUDE.md: ALWAYS request file/folder access (request_cowork_directory) BEFORE reporting a file/folder as unavailable / read-only / needs-a-restart. Root cause: I wrongly reported the skill mirror as un-syncable when a single folder request fixed it instantly. (3) NEW behaviour: whenever I find a non-ASCII file, flag it AND offer to fix it (do not just mention it). DONE (after reboot): the new mandatory rule is now also in the master global config C:\Users\pavey\.claude\CLAUDE.md (Mick appended it via PowerShell; backup CLAUDE.md.bak-20260705). Rule now lives in all three CLAUDE homes + this memory.
**Last Updated:** 2026.07.05 (Sun, Cowork, afternoon) - gmail-self-notes taken live-ish. Created two Obsidian Bases (root _All-Notes.base + 00-Inbox/Inbox.base). Resolved YouTube overlap (vault wins; yt-inbox-sweeper retired for YT); migrated 44 old Sheet rows to 00-Inbox/YouTube-Queue and archived the Sheet ([ARCHIVED 2026.07.05]). Ran a representative 48h test sweep (all pathways pass: youtube/text/attachment, xref + two-way links, MCSB authorship). Two skill fixes: YouTube title from email SUBJECT not web_fetch oEmbed (provenance-blocked), and youtube notes -> 00-Inbox/YouTube-Queue. Scheduled gmail-self-notes-sweep daily ~06:20 (self-contained prompt; processed-log seeded last_run 13:07). Added MCSB-Filed Gmail label (Label_534, light grey) + archive-out-of-inbox on success (never delete/mark read); search excludes -label:MCSB-Filed as 2nd dedupe. OPEN: backfill ~35 remaining 48h emails; re-sync installed .skill + mirror (M) with today's changes; click Run now to pre-approve tools; bookmark the base.
**Last Updated:** 2026.07.05 (Sun, Cowork) - Built + installed TWO Gmail self-note skills. cedric-note-fetcher (on-demand: fetch a self-sent attachment to outputs). gmail-self-notes (scheduled vault ingestion: body text + attachment + YouTube link each become Obsidian notes in 00-Inbox, with a shared xref datetime key and two-way related wikilinks; attachment author MCSB when built with Cedric else Mick; YouTube notes carry url + add-to-nblm + summary:pending). Attachment bridge: Gmail cannot download attachments, so browser Add-to-Drive then Google Drive connector (decode+validate). Created two Obsidian Bases (_All-Notes.base at vault root: Everything + Notes-only; 00-Inbox/Inbox.base: 5 views). OPEN: gmail-self-notes YouTube branch OVERLAPS existing yt-inbox-sweeper (Sheet-based, daily 06:30) - reconcile before scheduling. Skills backed up to vault (V) + installed (P); mirror (M) pending.
**Last Updated:** 2026.07.04 (Sat, Cowork) - Big ax-trees-automation session (Session 18). Built ax-mapper (generic AX-tree UI mapper: engine + per-app adapters) in the vault; converged the ShareScope mapper onto it (live proof passed, bespoke scripts archived+deleted); extended the map to v1.5 (news categories + Design; full portfolio download flow PP1/PP2). Split ShareScope into TWO adapters (stock + portfolio). New Key Convention saved: always give Mick commands in PowerShell, baby steps (he is not a coder).
**Last Updated:** 2026.07.02 (Thu late morning, Claude Desktop) - ShareScope chart shape + .env fixes. (1) CHART now exports true 16:9: sharescope_chart.py ticks the bitmap dialog's Custom option and sets 1200x675 - CONFIRMED exactly 1200x675 on HDD (right proportions for docx + 16:9 slides). (2) LOGIN failed after Mick rotated the ShareScope password because the script read the WRONG .env (a stale old Vault copy); repointed sharescope_login.py to C:\Users\pavey\.env (the single canonical creds file), added load_dotenv(override=True) + path logging - CONFIRMED working. (3) Credential SWEEP: repointed wordpress-post-publisher + wordpress-image-uploader to C:\Users\pavey\.env. (4) Added a top-level CREDENTIALS SINGLE-SOURCE rule to the master CLAUDE.md (v1.3) and reconciled all lower-level CLAUDE.md files to point at it; verified Poster Pete/WP creds are safely in the canonical .env before Mick deletes the redundant Vault copy. Detail in the 2026.07.02 session block below.
**Prior update:** 2026.07.01 (Wed early evening, Claude Desktop) - Built the ShareScope CHART + REPORT automation. NEW: sharescope-get-chart (v1.0, native 12-month PNG export), sharescope_session.py session runner (ONE login, many tickers/tasks, ONE logout - confirmed on HDD: chart + 6 CSVs in 26s), and sharescope-report (v0.1, chart embedded in the branded DIY template - proven on a Hardide brief). Selectors confirmed + logged. Produced a webinar crib sheet + a Meet Cedric episode (Content Studio, Draft). URGENT open item: strip the ShareScope password from PLAIN TEXT in sharescope-financials SKILL.md. NOTE: .env SHARESCOPE_HEADLESS is currently FALSE for tonight's live demo - flip back to true after. Full detail: 04-Projects\2026.07.01-ShareScope-Chart-Export\BUILD_LOG.md.
**Earlier update:** 2026.06.30 (Tue evening, Cowork) - Set up the PROMPT LIBRARY single-source-of-truth in Dex (new 06-Resources\Prompts\: README, _Prompt-Template schema, 00-Index, Prompts.base). Schema aligned 1:1 with PROMPT_LIBRARY.md via shared `code` key. Also FIXED Git: pushed a 7-commit backlog to GitHub and edited daily_git_commit.py so it self-heals (pushes whenever local is ahead, even on no-change days) and logs to _git-commit.log; enabled Task Scheduler history. STILL TO DO: migrate 141 prompt .md files from Mick's Vault (pilot batch agreed). Full detail: PICKUP_NOTE_2026.06.30-Prompt-Library-Migration.md (Dex root).
**Older update:** 2026.06.03 (Wed late morning) - Skill dual-write AUDIT across all three locations (Mirror /mnt/skills/user, PRIMARY C:\Vaults\Mick's Vault\.claude\skills, DEX skills). Heavy drift found: of 12 skills in 2+ places only 2 byte-identical. Fixed 3 in the mirror (image-cta-overlay v2.2; annie - fixed DEAD tool names; pdf-to-pptx-converter v1.1). Rest PAUSED for after tonight's webinar. FULL DETAIL + remaining work in PICKUP_NOTE_2026.06.03-Skill-Audit.md (Dex root). Key realisation: canonical model is ALREADY documented (Dex + mirror) but migration onto it is only partial, AND the four 2026.05.30-migrated skills are now MISSING from this project's mirror (mirror may be project-scoped or resetting).
**Environment:** Claude Code CLI (this session, on Mick's PC). (Prior sessions: Cowork, Claude Desktop.)

---

## Recent session: 2026.07.11 (Saturday, Cowork, evening) - Hermes project, full vault ASCII cleanup, non-ascii-sweep skill, git fix

- NEW project 04-Projects/2026.07.11 - Hermes-Claude-Obsidian (index note carries the NotebookLM
  id/url/title in YAML), paired with the notebook Mick made via the notebooklm CLI (id
  fa003870-78c0-45f4-9df1-c815958f88f7). Registered in the project index (04-Projects/README.md
  Active Projects) and cross-linked from the in-vault MCSB note (2026.05.11-MCSB-Webinar-Voice, new
  Section 10). Drafted a Meet Cedric episode (investigate Hermes Agent as a route to help the MCSB
  build). Added the Hermes guide as a source into the notebook via notebooklm.google.com (Copied text).
- FULL vault ASCII cleanup: typography corruption fixed everywhere; then per Mick's choices currency
  -> ASCII (GBP/EUR/c), status glyphs -> tags, decorative emoji + ShareScope PUA glyphs + broken
  U+FFFD dropped, accents transliterated, 9 cp1252 files re-decoded (incl 4 Writing System pieces).
  413 files; verification = ZERO non-ASCII in any decodable text file. Root cause: Mac-seeded DEX
  templates (now cleaned). Report: System/Debug_Logs/2026.07.11 - Vault ASCII Cleanup Report.md.
  Left alone: 6 undecodable junk/binary files + credential pickle + .obsidian. CAVEAT: accents were
  transliterated vault-wide (e.g. any 08-People names) - restorable from git if wanted.
- Built skills/non-ascii-sweep (scan/safe/full). ascii_sweep.py is PURE ASCII by design (chr code
  points) so it can never corrupt its own maps; auto-detects the vault root; writes dated reports.
  Scheduled non-ascii-sweep-weekly Sat ~10am London, SAFE mode only. Registered in SKILLS_REGISTRY
  (Section 1a + Section 5). GOTCHA: Write/Edit truncated the large .py at ~285 lines and did not sync
  to the bash mount - wrote the final script via bash heredoc; PREFER heredoc for large script files.
- Fixed daily_git_commit.py: it built the message inline (git commit -m), so 503 files exceeded the
  Windows ~8191-char command-line limit ("command line too long"); patched to git commit -F tempfile
  and capped the config/docs lists. Backup .bak-2026-07-11. Would also have failed tonight's 9pm sweep.
- Git: today's main body committed + pushed by Mick from PowerShell (5e10b38, 505 files, to
  github.com/Mick-P-UK/Dex-MickP). Sandbox has NO SSH key so pushes must come from his PC. Later edits
  (script patch, registry, this wrap) ride the 9pm sweep (now the fixed script) or a manual push.

---

## Recent session: 2026.07.11 (Saturday, Cowork, evening 2) - Hermes-Claude-Obsidian project + NotebookLM

- Mick created a NotebookLM notebook (via the notebooklm Windows CLI, which he runs
  himself - I cannot type into a Windows terminal from Cowork). Title "Hermes + Claude +
  Obsidian_Updated:2026.07.11"; id fa003870-78c0-45f4-9df1-c815958f88f7.
- Set up the matching project in the vault: 04-Projects/2026.07.11 - Hermes-Claude-Obsidian/
  with an index note carrying the notebook id/url/title in YAML frontmatter. Date-first per
  our naming rule; name hyphenated (Hermes-Claude-Obsidian) to stay strictly ASCII.
- Registered it in the PROJECT index (04-Projects/README.md - added an Active Projects
  section) rather than a vault-level index, at Mick's steer.
- Cross-linked it FROM the in-vault MCSB project note (2026.05.11 - Cedric Webinar Voice
  Integration and MCSB Knowledge Bridge) via a new "Section 10 - Related Explorations", so
  the MCSB thread does not lose sight of it. NOTE: the canonical MCSB PRD/PROGRESS still
  live OUTSIDE the vaults in the PAIDA Master folder; the webinar-voice note is the closest
  in-vault MCSB anchor.
- Drafted a Meet Cedric episode in the project folder ("Could an Open-Source Assistant Help
  Build Our Shared Brain?") - investigate-not-convert framing, weighs Hermes's memory/skills/
  scheduler upside against skill-poisoning / infrastructure-not-app risk.
- Purpose of the whole thread: assess whether Hermes Agent shortcuts or informs the MCSB
  build. Grounding doc is the 00-Inbox Hermes guide (prepared for the 29 Jul 2026 webinar).
- Mick then asked to add that Hermes guide as a source into the notebook via
  notebooklm.google.com (browser route, not the CLI).

---

## Recent session: 2026.07.11 (Saturday, Cowork, evening) - Session-start continuity fix + MCSB prep

- Mick asked "where were we"; the morning's Personal Content Backup work was missing from the
  top of memory. Diagnosed: the 14:05 baton flushed CEDRIC_MEMORY.md but APPENDED the block at
  the file bottom while the top Last Updated stack still read 07.10, so a top-down session-start
  missed it. Not a "memory never written" bug - a "written in the wrong place" bug.
- Fixed BOTH ends. Write side: baton-wrap step 3 + sundown-wrap step 7 now carry an explicit
  PLACEMENT rule to PREPEND a new Last Updated line (under the heading) + a new Recent session
  block (after the first ---), never append to the bottom. Read side: session-start now reads
  _handovers/LATEST.md FIRST, then the memory top, and trusts LATEST if it is newer. Applied to
  the Dex CLAUDE.md (edited here) and the master C:\Users\pavey\.claude\CLAUDE.md (appended by
  Mick via PowerShell; backup CLAUDE.md.bak-2026-07-11).
- Tidied the orphaned 07.11 entry to the top; committed the whole fix (5e2f08f) over SSH.
- Brain dump captured to 00-Inbox; two tasks added to 03-Tasks/Tasks.md: ^task-20260711-001
  (give ShareScope-Automation its own private repo - unbacked-up) and ^task-20260711-002
  (reconcile MCSB PRD v0.3 with recent work + update PROGRESS.md and the Notion Build Tracker).
- MCSB PRD located: it lives OUTSIDE the vaults, in the PAIDA Master folder at
  C:\Users\pavey\Documents\0.0 - AI Projects\0 - PAIDA - Mick 2nd Brain\PAIDA Master - Second
  Brain\04-Projects\2026.05.09 - MCSB\2026.05.13-MCSB-PRD_V0.3.docx. Confirmed v0.3 is latest
  (v0.2.1 was an earlier draft). Converted it to PDF next to the docx. That folder also holds a
  maintained PROGRESS.md (updated 07.07) and three 07.10 Cowork-cloud/GitHub impact notes.
- Lifted the 13 May Phase 1 implementation pickup note into 00-Inbox (ASCII-normalised). It
  flags OQ2 "fold PAIDA Master into Dex?" - deferred then, ripe now given the PRD sits outside.
- Git: this afternoon/evening vault edits (brain dump, tasks, pickup note, this wrap) left for
  the 9pm sweep at Mick's choice. PDF sits in the PAIDA Master folder (not a git repo).

---

## Recent session: 2026.07.11 (Saturday, Cowork, afternoon) - Personal Content Backup executed

- Decision reversed: NO separate personal repo. Dex-MickP is now ONE PRIVATE repo holding
  everything, never published; a scrubbed DEMO repo would be derived if structure is shared.
- .gitignore rewritten: ignore only machine junk + secrets (.env, .mcp.json,
  System/.credentials/, tokens, pickles, *.log except _changelog/). All PARA content now tracked.
- Pre-commit ASCII hook rescoped to work-mcp inputs only (03-Tasks, 02-Week_Priorities,
  01-Quarter_Goals, 00-Inbox/Meetings, 05-Areas/People). Creative content backs up with typography.
- Fixed a corrupted Week_Priorities.md (injected python fragment) + 4 other in-scope files.
- First full backup committed + pushed (7e02ee7, 291 files). Repo current with GitHub.
- Auto-push FIXED: nightly daily_git_commit.py always pushed but GCM/wincredman failed headlessly.
  Switched origin to SSH (dedicated ed25519 key on Mick-P-UK). Verified push works (commit 1ca585c).
- Still open: ShareScope-Automation own private repo (unbacked-up); minor cruft tidy; point
  Cowork default folder at Dex-MickP.
- Handover baton: _handovers/archive/2026.07.11 - 1404 - baton - Personal Content Backup.md.

---

## Recent session: 2026.07.10 (Friday, Claude Code CLI, evening) - PATH file ASCII cleanup closed out

- Picked up the SOP note left from 2026.07.10: "2026.07.10 - NOTE - Clean the PATH UiPath File
  for ASCII (Local)_v1.0.md" flagged that the PATH (UiPath Inc.) financial analysis file was held
  back from the same-day GitHub commit because the Dex-MickP pre-commit hook blocks non-ASCII bytes.
- Read the file, grepped for non-ASCII bytes: found exactly ONE offending character used twice, an
  em dash (U+2014) in the "Overall Summary and Recommendation" section - "share repurchases-
  deploying a fresh $500 million authorization-will help put a floor under the stock price."
  Replaced both instances with spaced ASCII hyphens; meaning unchanged.
- Re-grepped: zero non-ASCII bytes remain. Confirmed both the research file and the SOP note were
  untracked (first commit, not edits of an existing tracked file).
- Committed both files together (2312d47) with the pre-commit hook reporting "UTF-8 check passed (2
  .md file(s) clean)", then pushed to origin main (10b5a83..2312d47).
- OUTSTANDING (carried forward, unchanged): the held June end-of-month portfolio posting run (month-
  end 30 Jun, post date 9 Jul, all four portfolios) still needs to be run from Claude Desktop -
  Cowork cannot reach the WordPress credentials in C:\Users\pavey\.env. Also still open: the second
  SOP on "which environment runs what" (Desktop vs Cowork vs claude.ai), offered but not yet built.

---

## Recent session: 2026.07.09 (Thursday, Cowork) - SOP library started

- Mick asked how the end-of-month portfolios get posted to diy-investors.com. Walked him through
  the four-skill chain: portfolio-post-creator (orchestrator) -> benchmark-fetcher +
  wordpress-image-uploader -> wordpress-post-publisher. Posts are created as DRAFTS only; Mick
  reviews the wp-admin edit URL and publishes. Four portfolios (UK/US Active 10, Yr1 + Yr2).
- CONSTRAINT confirmed: the routine cannot run from Cowork because Poster Pete's WP creds live in
  C:\Users\pavey\.env and Cowork cannot mount the home folder (reserved as internal session
  storage) nor read the file directly. The WP API itself IS reachable from the sandbox (HTTP 200);
  only the credential read is blocked.
- June run (month-end 30 Jun 2026, post date 9 Jul, all four portfolios) HELD for Claude Desktop at
  Mick's choice. Re-issue there: "Run the end-of-month portfolio posts for 30 June, all four
  portfolios, post date 9 July."
- Started an SOP LIBRARY at 06-Resources\SOPs\. First entry: "SOP - End-of-Month Portfolio
  Posting.md" (YAML tag SOP; ASCII-clean; grounded in the four skills). Mick wants SOPs for all
  recurring workflows; flagged SOP-creation itself as a Meet Cedric topic. Offered a second SOP on
  "which environment runs what" (Desktop vs Cowork vs claude.ai) - pending.

---

## Recent session: 2026.07.04 (Saturday, Cowork) - ax-mapper + ShareScope map v1.5

- Imported an overnight claude.ai conversation + attachments (Playwright agent CLI proposal) into
  the ax-trees-automation project.
- Built ax-mapper in the Dex vault (skills/ax-mapper/): a GENERIC, read-only accessibility-tree UI
  mapper. Engine is app-agnostic; each app is a small adapter. Offline suite 18/18. Reusable for ANY
  Playwright-drivable web app - copy adapter-template.js to add one.
- CONVERGED the ShareScope mapper onto ax-mapper. 3-test live proof passed (179 controls, exact parity
  with master v1.4). Bespoke Node scripts archived (with sha256 manifest) then deleted.
- Extended the map to v1.5: news category selection (All/Share/List/RNS/Hot/Latest) + List design
  dialog; and the full PORTFOLIO download flow - selector -> pick portfolio -> holdings/transactions
  -> Sharing -> Export holdings/transactions -> Export options dialog (Holdings / latest / Transactions).
- TWO ShareScope adapters now: sharescope.adapter.example.js (stock; searches a ticker) and
  sharescope-portfolio.adapter.js (portfolio; NO stock search - the correct flow, Mick's steer).
- Key gotchas (in the master map): portfolio toolbar hidden in the single-stock Financials view;
  run the browser wide or rightmost toolbar buttons overflow; print-to-PDF is a Chrome/OS dialog and
  is NOT automatable (use CSV export).
- Meet Cedric episode drafted: meet-cedric/2026.07.04-teaching-cedric-to-read-any-app.md (TODO: post
  the brain dump to Notion Content Studio when the Notion connector is authorised).
- PENDING (Desktop): mirror skills/ax-mapper to /mnt/skills/user (dual-write rule - could not be done
  from Cowork). Git: project committed via git-save.bat; vault syncs its own way.
- Full detail: ax-trees-automation/session-logs/2026-07-04-session18.md and SESSION19-PICKUP.md.

---

## Recent session: 2026.07.02 (Thursday late morning, Claude Desktop) - ShareScope 16:9 chart + .env consolidation

Continuation of the ShareScope automation WIP. Two fixes plus a credential-path sweep.

### 1. Chart now exports true 16:9 (docx + PowerPoint ready)
- Problem: the chart PNG came out near-square (~631x560) because the export took the default
  on-screen size.
- First attempt (reverted): widening the browser viewport before capture. Mick then spotted
  the real lever - the "Save chart as PNG (bitmap)" dialog has a Custom size option.
- Fix (sharescope_chart.py): the save step now ticks Custom and sets CHART_PNG_WIDTH x
  CHART_PNG_HEIGHT (1200 x 675) then clicks OK. Diagnostic logging added for the dialog fields.
- CONFIRMED: HDD chart came out exactly 1200 x 675 (aspect 1.778 = 16:9). Tunable via the two
  constants at the top of sharescope_chart.py.

### 2. Login .env fix (password rotation exposed a two-.env problem)
- Mick rotated the ShareScope password and thought he had updated the .env, but login kept
  failing "invalid password". Cause: the script read C:\Vaults\Mick's Vault\.env which still
  held the OLD password. Mick's real/canonical creds file is C:\Users\pavey\.env (the same file
  MCSB tokens + ax-trees already use). The Vault copy was a stale second file.
- Fix (sharescope_login.py): primary env_path repointed to C:\Users\pavey\.env; old Vault path
  dropped as primary. Added load_dotenv(env_path, override=True) so the .env always beats any
  stale OS env var, plus a "Reading credentials from: <path>" log line so the file in use is
  never ambiguous. CONFIRMED working - login clean, chart saved.

### 3. Credential-path SWEEP (repoint scripts off the old Vault .env)
- Canonical creds file is now C:\Users\pavey\.env for everything.
- Repointed to C:\Users\pavey\.env:
    - skills\wordpress-post-publisher\SKILL.md (2 refs: Credentials note + load_env code)
    - skills\wordpress-image-uploader\SKILL.md (1 ref: load_env default)
- Checked, NO change needed:
    - benchmark-fetcher (uses Yahoo Finance + a local xlsx, no .env)
    - portfolio-post-creator (delegates creds to the two WP skills, no .env of its own)
    - sharescope_login.py (already repointed in fix 2)
- NOTE: mirror copies (/mnt/skills/user/) NOT updated - vault is source of truth; mirror sync
  is part of the deferred 2026.06.03 skill audit and is unreliable anyway.

### 4. Credentials SINGLE-SOURCE rule added at the top level + all CLAUDE.md files reconciled
- Root cause of the recurring stray/stale .env problem: no top-level rule saying WHERE the one
  .env lives, so copies keep appearing (a project-subfolder copy on 2026-05-03; today's stale
  Vault copy). Fix = one authoritative rule at the highest level, everything else points to it.
- MASTER config C:\Users\pavey\.claude\CLAUDE.md bumped to v1.3 (changelog updated) with a new
  CRITICAL RULE: "Credentials - Single Source". In brief: ALL local script/skill credentials,
  keys and tokens live in ONE file only, C:\Users\pavey\.env; never create another .env; never
  hardcode; read with load_dotenv(override=True); FAIL (do not fall back) if a key is missing.
  Scoped to LOCAL contexts (claude.ai Web / Cowork sandbox have no local disk - secrets there
  arrive via connectors, not this file).
- Condensed copy added to CEDRIC_MEMORY.md Key Conventions (loaded every session).
- Reconciled every older/duplicate .env mention to POINT AT the master rule (stops drift):
    - C:\Users\pavey\.claude\.CLAUDE.md               -> converted to a pointer
    - C:\Vaults\Cowork\CLAUDE.md                      -> pointer (old block had em dashes)
    - C:\Vaults\Cowork\ax-trees-automation\CLAUDE.md  -> pointer (kept its placeholder-.env note)
    - C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\CLAUDE.md -> reframed its generic "Security & API
      Keys" section. That section was inherited from the Dex template and actually taught the
      OPPOSITE habit (create a per-project gitignored .env); now it defers to the single-source rule.

### 5. Verified Poster Pete / WordPress creds are safe BEFORE deleting the old .env
- Mick spotted Poster Pete (WordPress user 'posterpete', Editor) credentials in the redundant
  Vault .env and asked whether a routine would break when he deletes them.
- Traced: the only Poster Pete users are the wordpress-post-publisher + wordpress-image-uploader
  skills (called by the monthly portfolio-post-creator routine). BOTH were repointed to
  C:\Users\pavey\.env in the sweep (fix 3).
- CONFIRMED the WP keys are present in C:\Users\pavey\.env (WP_DIY_INVESTORS_URL/USER/APP_PASSWORD
  and WP_DIY_AI_URL/USER/APP_PASSWORD). So deleting the old Vault copy is SAFE - the monthly
  WordPress posting routine will still find its credentials. Values not recorded here.
- Note: WP_DIY_AI_APP_PASSWORD is still a placeholder (posting to diy-investors.ai was never
  wired up) - pre-existing, unaffected by the move.

### Endgame for Mick
- Once satisfied, DELETE / empty the ShareScope + WP credentials from the redundant
  C:\Vaults\Mick's Vault\.env so there is genuinely one source. Any straggler script still
  pointing there will then fail loudly with "missing credentials" - which flushes it out
  safely. Mick to locate any such stragglers (news checkers etc. - not confirmed to use .env).

### Still open (carried forward)
- Flip .env SHARESCOPE_HEADLESS back to true (currently false from the demo/testing).
- Fold the 6 financial CSVs into sharescope-report as tables (v0.2).
- Fix the harmless sharescope_logout.py cleanup warnings (project-wide, non-blocking).
- COWORK: test whether Cowork can run the local Playwright automation; bundle skill scripts.
- ASCII clean-up of the Cowork + Dex CLAUDE.md rulebooks (legacy em dashes + mangled tick marks) - logged as a non-urgent memory task 2026.07.02.

### Resume phrase
"Cedric, I'm back. Let's pick up the ShareScope work - report financials tables next."

---

## Recent session: 2026.07.01 (Wednesday early evening, Claude Desktop) - ShareScope chart + report automation

Started from "find the old ShareScope work"; ended with a working single-session automation
that captures a chart, pulls financials, and folds the chart into a branded report. Built on
the existing 04-Projects\2026.04.04-ShareScope-Automation modules (login/search/export/logout/
utils reused UNCHANGED - only new orchestration + a chart module were added).

### Built this session
- sharescope-get-chart skill (v1.0): native 12-month "Save chart as PNG (bitmap)" export for
  any ticker. Files: sharescope_chart.py + sharescope_chart_orchestrator.py.
- sharescope_session.py (SESSION RUNNER): one login, many tickers/tasks, one logout. The
  standard multi-task entry point; report skills import run_sharescope_session(). Confirmed
  on HDD: chart + 6 financial CSVs in a single 26s session.
- sharescope-report skill (v0.1): embeds the chart into DIY_Investors_Report_Template.docx.
  Proven with a real Hardide (HDD) Stock Research Brief - chart embedded, branding intact.

### Selectors confirmed live (2026.07.01)
- Chart view button: button[data-cmd="ViewChart"] (name "Chart" matches TWO elements).
- 12-month period control: labelled "1 year".
- Save item: "Save chart as PNG (bitmap)..." (a scaling dialog appears - click OK).

### Deliverables
- 2026.07.01 - HDD - Stock Research Brief.docx (sample report with embedded chart).
- 2026.07.01 - ShareScope Demo - Webinar Crib Sheet (pdf + docx) - six-step live runsheet.
- Meet Cedric episode in Content Studio (Draft, Video):
  https://app.notion.com/p/390db32a9b0a81b0a74dfab05fe44686
- Build record + pickup + episode pack: 04-Projects\2026.07.01-ShareScope-Chart-Export\
  (BUILD_LOG.md is the primary handoff doc).

### RESOLVED 2026.07.02
- DONE: Stripped the ShareScope username + password from PLAIN TEXT in
  skills\sharescope-financials\SKILL.md - replaced with <your-sharescope-username> /
  <your-sharescope-password> placeholders pointing at the .env only. Swept the other
  four sharescope skills and reference files - no other copies of those credentials.
  Mick to rotate the exposed ShareScope password and update C:\Vaults\Mick's Vault\.env.

### Other open items (post-webinar)
- Fold the 6 financial CSVs into the report as summary tables (sharescope-report v0.2).
- COWORK GOAL: (a) TEST whether Cowork can execute the local headless Playwright automation
  before assuming it (Test, Don't Trust); (b) bundle each skill's scripts into its own folder
  so they are self-contained/portable rather than pointing at the April project.
- Fix the harmless sharescope_logout.py cleanup warnings (project-wide, non-blocking).
- Dual-write the new SKILL.md files to the /mnt/skills/user mirror.

### Note for next session
- .env SHARESCOPE_HEADLESS is currently FALSE (set for tonight's live webinar demo so the
  browser is visible). Flip back to true for hands-off runs after the webinar.

### Resume phrase
"Cedric, I'm back. Let's pick up the ShareScope report automation - financials tables next."

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
- Verify usage / decide on Synthesia (GBP 201.60/yr renews 25 Nov), Ideogram ($180/yr renews 2 Sep), Text Blaze ($35.88/yr renews 18 Aug)
- Cancel Alex McFarland "AI Writing Systems" Substack before 18 May (GBP 16/month - not actually cancelled despite earlier belief)
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
- **Commands = PowerShell + baby steps (Mick is NOT a coder):** ALWAYS give terminal commands in PowerShell syntax (his default shell), never Command Prompt / cmd.exe. Use `cd "path"` (no `/d`), set variables with `$env:NAME = "value"` (not `set NAME=value`), and quote comma-separated arg values (e.g. `--only "a,b"`). Always double-quote vault paths (apostrophe in "Mick's-Dex-2nd-Brain" breaks unquoted). Feed steps ONE small copy-paste block at a time, wait for the result, then give the next; explain each step in plain English and assume NO shell/coding knowledge. (Added 2026.07.04 after a cmd-style `cd /d` command failed in his PowerShell window.)
- **Credentials single source (MANDATORY):** All LOCAL script/skill credentials, API keys and tokens live ONLY in C:\Users\pavey\.env. Never create another .env (no project-subfolder or vault copies), never hardcode secrets in any skill/script/doc/CLAUDE.md, read with load_dotenv(override=True), and FAIL clearly if a key is missing (never fall back to another location). Local contexts only - in claude.ai Web / Cowork sandbox there is no local disk, so secrets arrive via connectors. Full rule in the master C:\Users\pavey\.claude\CLAUDE.md (v1.3, 2026.07.02). (Added 2026.07.02 after a stale second .env caused silent login failures.)
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

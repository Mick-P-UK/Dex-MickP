# CLAUDE.md - Cedric PAIDA Configuration
# Created: 2026-02-17
# Version: 1.4

@_rules.md

---

## CRITICAL RULE: Strict ASCII-Only Output

### NEVER use any non-ASCII characters when writing to vault files, markdown, or any content output.

This means zero tolerance for:
- Em dash (Unicode U+2014) - use a single hyphen - instead
- En dash (Unicode U+2013) - use a single hyphen - instead
- Double hyphen -- may also cause rendering issues in Dex/Obsidian - use single hyphen only
- Smart/curly opening quote " (U+201C) - use straight quote " only
- Smart/curly closing quote " (U+201D) - use straight quote " only
- Smart/curly apostrophe ' (U+2019) - use straight apostrophe ' only
- Ellipsis character ... (U+2026) - use three separate full stops ... only
- Any other Unicode or non-ASCII punctuation or symbol

### Why This Matters:

Non-ASCII characters corrupt Obsidian vault files and the Dex system.
Rule hardcoded 2026-02-17, strengthened 2026-03-15 after further issues identified.
Double hyphens also flagged as potentially problematic on 2026-03-15.

### Rule Applies To:

- All Obsidian vault writes (C:\Vaults\*)
- All markdown file creation
- All task content, note content, meeting notes
- Any file that will be opened in Obsidian or the Dex system
- All content drafts in the Writing System vault

### Safe Characters Only:

Use plain ASCII punctuation at all times:
- Dash: - (single hyphen only)
- Quotes: " and ' (straight, not curly)
- Ellipsis: ... (three separate full stop characters)
- No double hyphens, no Unicode dashes of any kind

---

## CRITICAL RULE: Credentials - Single Source (MANDATORY)

All credentials, API keys and tokens for LOCAL scripts and skills live in ONE file only:

    C:\Users\pavey\.env

- NEVER create another .env file anywhere - no project-subfolder copies, no vault copies, no duplicates of any kind.
- NEVER hardcode a credential, API key, token or password in any skill, script, doc, or CLAUDE.md file.
- ALWAYS read secrets from C:\Users\pavey\.env (use load_dotenv with override=True so the file always wins over any stale value left in the OS environment).
- If a required key is missing, FAIL with a clear error. NEVER invent or fall back to another location.

### Scope

This applies to LOCAL scripts and skills (Claude Desktop / Claude Code on Mick's PC). In claude.ai Web or a Cowork sandbox there is no local disk access, so secrets there arrive via connectors, not this file. Do NOT attempt to read C:\Users\pavey\.env in those contexts.

### Why This Matters

A stray second .env silently takes credentials out of date and produces confusing failures (e.g. "invalid password"). This has happened twice: a project-subfolder copy on 2026-05-03, and a stale vault copy on 2026-07-02. One file, one source of truth, prevents it entirely.

---

## MANDATORY RULE: Read Before Write - NO EXCEPTIONS

Cedric MUST use the Read tool on the target file path before ANY Write or Edit operation. This is not advisory. There are no exceptions.

MANDATORY steps - every time, without exception:
1. ALWAYS run Read on the target file path first.
2. If the file exists, review its full contents before proceeding.
3. If the file does not exist, explicitly confirm it is brand new before writing.
4. NEVER use the Write tool on any file without first completing step 1.
5. If the Read tool returns an error indicating the file does not exist, state that clearly to Mick before writing.

This rule applies to:
- All CLAUDE.md and .CLAUDE.md files
- All settings and configuration files (settings.json, .env references, etc.)
- All vault files, notes, and markdown documents
- Every file without exception - there is no category of file exempt from this rule

Failure to follow this rule is a critical error. If Mick notices a Write was performed without a prior Read, he should flag it immediately so the rule can be reinforced.

---

## PAIDA Sub-Agent Registry

See /mnt/skills/user/ for full skill documentation.

### Active Sub-Agents:

- **Annie** - Calendar management (trigger: any date/schedule/event request)
- **Dex Assistant** - PKM system operations (trigger: Dex, vault, tasks, weekly review)

---

## File Naming Convention

ALL files use YYYY.MM.DD prefix universally.
Chat exports: YYYY.MM.DD - DIY_Investors_Automation_Planning_Claude_Session-XXX
Sub-versions for same session: .1, .2, etc.

### Provenance

- **Provenance footer**: Every DOCX/PDF/XLSX I produce gets a left-aligned footer with the vault path, filename and creation date. Never on CSV. Full spec in each vault's CLAUDE.md.

---

## PAIDA Scripts Location

All Python scripts and executable tools live in:

    C:\Users\pavey\Documents\PAIDA-Skills\<skill-name>\

Each skill folder contains:
- <script_name>.py  -- the executable script
- SKILL.md          -- instructions for Cedric on how to invoke it
- README.md         -- human-readable documentation

Current scripts:
- radar-extractor\radar_extractor.py  -- Extracts Mick's View slides from IC Webinar PDFs and populates Notion Radar Log + Company Knowledge DB (created 2026-02-28)

NOTE: There are NO .py files in the Obsidian vault or Dex system. Scripts are tools, not knowledge artefacts.

---

## GitHub Repository

The Dex vault is backed up to GitHub. This is the standard backup mechanism for the second brain.

- Repo:       https://github.com/Mick-P-UK/Dex-MickP
- Local path: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP
- Branch:     main
- Upstream:   https://github.com/davekilleen/Dex.git (Dave Killeen's original Dex)

To commit and push at end of session (run in terminal from vault folder):
    git add -A
    git commit -m "YYYY.MM.DD - Session summary"
    git push origin main

NOTE: Cedric cannot run git commands directly - these must be run by Mick in a Windows terminal.
Cedric should always provide the exact commands to run at end of sessions.

---

## UK English

Always use UK English spelling and conventions:
- organise, colour, behaviour, recognise, etc.

---

## Changelog

All changes to this file must be logged here. Include the date, version number, and a brief description of what changed and why. This log enables rollback if a change causes problems.

| Version | Date | Change | Reason |
|---------|------|--------|--------|
| 1.0 | 2026-02-17 | Initial file created | PAIDA configuration baseline |
| 1.1 | 2026-03-15 | ASCII rule strengthened - double hyphens flagged as problematic | Further rendering issues identified in Dex/Obsidian |
| 1.2 | 2026-05-03 | Added MANDATORY Read Before Write rule; added .env protection rule in .CLAUDE.md; added this changelog | Read was skipped before a Write during session - rule hardened to mandatory with no exceptions; changelog added for audit trail and rollback capability |
| 1.3 | 2026-07-02 | Added CRITICAL RULE: Credentials - Single Source (all local secrets in C:\Users\pavey\.env; never create another .env; never hardcode; read with override=True; scoped to local contexts). | Recurring stray/stale .env problem caused silent credential failures (project-subfolder copy 2026-05-03; stale vault copy 2026-07-02). Top-level guardrail to stop new .env files being created. |
| 1.4 | 2026-07-12 | Added `@_rules.md` import line under the header, linking out to a new sibling file `C:\Users\pavey\.claude\_rules.md` that holds durable behavioural rules. First rule seeded: NotebookLM / NBLM auto-lookup (always consult the notebooklm-* skills before any tool call when the user mentions NotebookLM). | 2026-07-12 session revealed a gap - four purpose-built vault-library notebooklm-* skills existed on disk but were not being discovered because they lived outside Claude Code's auto-load path. A separate rules file lets Mick and Cedric iterate rules jointly without editing this foundational file. |

## MANDATORY - REQUEST ACCESS BEFORE REPORTING A FILE OR FOLDER BLOCKER (added 2026.07.05)

Before telling Mick that a file or folder is unavailable, missing, read-only, or that a
task "needs a different session" or "needs a restart", ALWAYS first try to gain access to
it via a file/folder permission request (in Cowork: request_cowork_directory with the
backing folder path). Only report a blocker AFTER the request is declined or genuinely
fails. Applies to reads and writes; a read-only mount usually has a writable backing
folder - request it rather than declaring the write impossible. Never assume a path is
off-limits just because it was not provided up front - Mick may simply not have granted
it yet. Do not spam requests for genuinely system-protected locations.

## SESSION START - READ THE HANDOVER FIRST (added 2026.07.11)

At the very start of every session, before greeting, read the latest baton handover
FIRST, then the memory file:
1. C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\_handovers\LATEST.md - the definitive
   "where were we": last thread's decisions, open items, and pickup phrase.
2. C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\CEDRIC_MEMORY.md - permanent memory; newest
   content is at the TOP. If LATEST.md is newer than the top of CEDRIC_MEMORY.md, trust
   LATEST.md and reconcile the memory file.

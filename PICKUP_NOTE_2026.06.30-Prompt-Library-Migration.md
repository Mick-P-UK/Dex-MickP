# PICKUP NOTE - Prompt Library Migration

**Date:** 2026.06.30 (Tuesday evening)
**Environment:** Cowork
**Status:** Scaffolding DONE + Git automation FIXED. Main job (migrating 141 files) NOT started.
**Resume phrase:** "Cedric, resume the prompt library migration - start the pilot batch."

---

## The goal (one source of truth each)

MOVE (not copy) Mick's prompt markdown notes out of Mick's Vault (C:\Vaults\Mick's Vault)
into Dex-MickP, which is GitHub-backed, so they become the single human-friendly SOURCE
for prompts. PROMPT_LIBRARY.md (C:\Vaults\Cowork\PROMPT_LIBRARY.md) stays the single
OPERATIONAL file that AutoHotkey and the investing demos read. No duplication. Mick's Vault
is eventually retired once this is bedded in.

Destination folder (created this session):
  C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\06-Resources\Prompts\

---

## What is DONE this session

1. Folder + scaffolding created at 06-Resources\Prompts\:
   - README.md        - the system, schema, category vocabulary, link to PROMPT_LIBRARY.md,
                        versioning rules, and the sync-check idea.
   - _Prompt-Template.md - the agreed YAML frontmatter, ready to copy for each new note.
   - 00-Index.md      - generated plain-markdown catalogue (GitHub-readable). Empty for now.
   - Prompts.base     - Obsidian Bases views: All Prompts, By Status, Operational, Drafts.

2. Agreed frontmatter schema (aligned 1:1 with PROMPT_LIBRARY.md so the two never drift):
   - title        - plain name (matches library Title)
   - code         - CAT-NN shared key (e.g. INV-01). This is the LINK between a note and its
                    PROMPT_LIBRARY.md entry. "TBD" until the prompt is promoted.
   - category     - fixed list, same as library: NBLM INV SUM CON ANL COM WEB GEN
   - ahk          - shortcode (e.g. ::us1#) or "none"
   - version      - X.Y (bump minor for tweaks, major for rewrites)
   - date_created / date_updated - YYYY.MM.DD
   - status       - draft | active | archived
   - operational  - true ONLY when the prompt lives in PROMPT_LIBRARY.md
   - tags         - ALWAYS starts with `prompt`, then free-form keywords
   The baseline `prompt` tag means the existing "All Notes.base > Prompts" view at the vault
   root picks these up automatically too.

3. Git automation FIXED in Dex-MickP (this was a detour, now closed):
   - Found 7 daily commits sitting locally, never pushed to GitHub. PUSHED them - GitHub now
     in sync (main -> main, 7c6276a..b3f8542).
   - Causes: (a) holiday 12-24 June, PC off; (b) logic gap - the daily script exited before
     pushing on no-change days, so a backlog never got retried; (c) scheduled push failing
     on the commit days themselves.
   - Edited daily_git_commit.py (Dex root):
       * now pushes on EVERY run if local is ahead of GitHub, even with no new changes
         (self-heals any backlog at the next run);
       * writes a line to _git-commit.log each run (Push succeeded / Push FAILED: ...).
         Already covered by the *.log ignore rule, so it will not trigger commits.
     Verified: python -m py_compile passed on Mick's machine.
   - Enabled "All Tasks History" in Task Scheduler for future visibility.
   - The 9PM daily task runs as user `pavey`, "only when logged on". PC is usually off at
     9PM, so it actually runs as a catch-up next morning (~07:48) - hence morning commit
     timestamps. This is normal, not a fault.

---

## What is PENDING - the actual job

Migrate 141 prompt-named .md files from Mick's Vault:
  - 131 in "0.0 - Inbox"
  - 9 in "0.1 - Projects" (Claude Code\02-Prompts, Comet Browser\01-Prompts)
  - 1 in _templates
Many are iterations / near-duplicates (multiple Comet, Perplexity, NBLM, Claude variants).
A straight lift would just relocate the dumping ground, so frontmatter normalising and light
dedupe ARE the job, not a separate step.

Agreed approach: PILOT a single coherent group first (NotebookLM or Perplexity are tidy
candidates). For that group: move the files across, fit each to the schema, dedupe
near-identicals (FLAG to Mick before deleting anything), regenerate 00-Index.md, and confirm
Prompts.base renders them in Obsidian. Mick reviews. If happy, roll out the rest the same way.

---

## Next action when resuming

1. Confirm with Mick which group to pilot.
2. Move that group's files into 06-Resources\Prompts\ (MOVE, delete the originals only after
   Mick confirms - this is a move not a copy).
3. Add schema frontmatter to each; set operational:false and code:TBD unless already in
   PROMPT_LIBRARY.md (the 9 codes already in the library: NBLM-01..06, INV-01 us1#,
   INV-02 dpr#, INV-03 uk1#).
4. Regenerate 00-Index.md from the migrated notes.
5. Ask Mick to open Prompts.base in Obsidian and confirm the views populate.

---

## Watch / open items

- Tonight's daily job will commit and push the new Prompts\ folder automatically. Check
  _git-commit.log (or Task Scheduler history) tomorrow to confirm it logged "Push succeeded".
  If it logs "Push FAILED", the scheduled-context GitHub auth (Git Credential Manager) needs
  a look - the manual push worked, so creds exist, but the background task may not reach them.
- Prompts.base filtered views (Operational, Drafts) use property comparisons; Bases syntax
  varies by Obsidian version. If either shows nothing, it is a one-line tweak in Obsidian.
- The big migration can later be its own clean, single commit if Mick wants a tidy history
  entry rather than letting the daily job sweep it in with a generic message.

---

## Key file paths

- Prompts scaffolding: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\06-Resources\Prompts\
- Operational file:    C:\Vaults\Cowork\PROMPT_LIBRARY.md
- Daily git script:    C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\daily_git_commit.py
- Source notes to move: C:\Vaults\Mick's Vault\0.0 - Inbox\ (and 0.1 - Projects\)

---

C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\PICKUP_NOTE_2026.06.30-Prompt-Library-Migration.md  |  Created 2026.06.30

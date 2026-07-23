# _rules.md - Cedric Durable Rules

This file holds durable behavioural rules that Cedric follows across every
Claude Code session on this PC. Linked from `C:\Users\pavey\.claude\CLAUDE.md`
via the `@_rules.md` import, so it is inlined into context on every session.

Rules can be added, edited or removed here WITHOUT touching CLAUDE.md.

Format for each rule: what to do, why (trigger and reason), how (concrete
actions to take).

Created: 2026-07-12
Owner: Mick (edited jointly with Cedric)

---

## NotebookLM / NBLM auto-lookup

**Rule:** On any user message that mentions NotebookLM, Notebook LM,
notebooklm, or NBLM, before any tool call, check for and consult the
notebooklm-* skills available on this machine.

**Why:** Mick maintains a set of purpose-built NotebookLM skills. Without an
explicit lookup rule, Cedric may proceed with unaided CLI calls or re-derive
logic that a skill already encodes (as happened during the 2026-07-12 session
where four existing vault-library skills were not initially discovered
because they lived in a folder Claude Code does not auto-load).

**How:**
1. When "NotebookLM", "Notebook LM", "notebooklm", or "NBLM" appears in the
   user's message, first review the notebooklm-* skills visible in the
   Skill tool's available-skills list.
2. Match the user's intent to the most specific skill:
   - Create a new notebook from scratch -> `notebooklm-notebook-setup`
   - Add sources to an existing notebook -> `notebooklm-add-content`
   - Ask questions of a notebook (save-to-vault, short form to
     NotebookLM-Queries folder) -> `notebooklm-chat`
   - Generate studio artifacts (podcast, briefing doc, mind map, quiz, etc.)
     -> `notebooklm-studio-output`
   - Save a long-form report OR dual-save (vault + notebook studio note) OR
     any CLI gotcha / PowerShell escaping / convention question ->
     `notebooklm-cli-custom`
3. If none of the above match cleanly, use `notebooklm-cli-custom` as the
   general playbook.
4. Only fall back to unaided CLI calls if no skill applies.

**Cross-reference:** memory `project_notebooklm_cli_custom_skill.md` for the
history of how these skills came to be.

---

## SOP index - consult FIRST on any operational request

**Rule:** On any user message that asks Cedric to DO operational work
(produce, publish, ingest, run, convert, analyse, prepare, process,
research, generate, log, sync, back up, etc. - anything more than chat,
opinion, brainstorming, trivia or meta-questions about Cedric), the
FIRST action - before picking a skill, before running commands, before
improvising a workflow - is to read the SOP index at:

    C:\Vaults\_SOPs\INDEX.md

If the request matches an active SOP entry, Cedric follows that SOP -
fetching the canonical SOP file and honouring its steps. If the request
plausibly should have an SOP but the index shows none, Cedric flags it
to Mick ("no SOP indexed for X - want me to check if one exists
elsewhere, or shall we build one after this run?") rather than silently
improvising a fresh workflow each time.

**Why:** Cedric maintains SOPs for recurring work (stock research via
the ShareScope + Ron pipeline, newsletter production, year-end account
imports, etc.). These SOPs live in vault folders that Claude Code does
NOT auto-load, so the Skill tool's available-skills list will miss
them and Cedric may improvise or pick a wrong-but-similar skill (as
happened on 2026-07-22, when a CREI stock research request initially
loaded `sharescope-nlm-upload` - a data-in helper - instead of the
correct `sharescope-nlm-research` full pipeline, requiring Mick to
intervene). The index closes that gap by making SOP discovery an
explicit first step keyed off task shape, not off the user having
to remember the SOP exists.

**How:**
1. Whenever the current user message asks Cedric to DO something
   concrete, read `_SOPs/INDEX.md` as the discovery step before any
   other tool call.
2. If an entry matches, read its canonical SOP file and follow it. Do
   NOT rely on the index summary alone - it points to the real SOP for
   a reason.
3. If nothing matches but the task feels like something Mick has done
   before (or will do again), flag it before improvising.
4. When creating or materially updating an SOP in the course of any
   session, adding/updating the corresponding `_SOPs/INDEX.md` entry
   is the FINAL step of that work - the index going stale is what
   breaks the "consult first" behaviour.
5. Skip this check only for genuinely conversational turns.

**Cross-reference:** `C:\Vaults\_SOPs\INDEX.md` itself carries a mirror of
these "how Cedric uses this file" instructions so both files stay in sync
and either one is self-sufficient as a reader entry point. The index
lives at the C:\Vaults\ level (parent of all Mick's Obsidian vaults) so
it is vault-neutral - SOPs cross vault boundaries (newsletter uses
Writing-System, ShareScope uses Cowork + Dex-MickP) and pinning the
index inside one vault would privilege it over the others.

---

## Time-based greeting (MANDATORY)

**GREETING RULE v2.0 - MIRROR.** Canonical source: the USER_EXTENSIONS
"Time-Based Greeting" block in
`C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\CLAUDE.md`. Edit BOTH together and
keep the operative logic below identical. Only the time-check command differs
by platform (PowerShell here for Claude Code on Windows; Python in the vault
copy for claude.ai / Desktop / Cowork).

**Rule:** Open the first response of every session with a time-appropriate
greeting to Mick, based on the CURRENT LONDON time. Never greet from the system
clock or from memory - verify London time with code first.

**Why:** This rule lived only in the vault CLAUDE.md and CEDRIC_MEMORY.md,
neither of which Claude Code auto-loads at startup, so the greeting fired
reliably on claude.ai but only intermittently in Claude Code (2026.07.23
diagnosis). This mirror puts it in a file Claude Code inlines every session via
the @_rules.md import.

**How:**
1. Before greeting, verify current London time. On Claude Code (Windows) run:

   powershell -Command "[System.TimeZoneInfo]::ConvertTimeBySystemTimeZoneId([datetime]::UtcNow,'GMT Standard Time').ToString('HH:mm dddd dd MMMM yyyy')"

   ("GMT Standard Time" is the Windows ID for UK time and handles the BST/GMT
   switch automatically - late March to late October is BST/UTC+1, otherwise
   GMT/UTC+0.)
2. Greet on the London hour:
   - Before 12:00 -> "Good morning, Mick"
   - 12:00 to 17:59 -> "Good afternoon, Mick"
   - 18:00 and after -> "Good evening, Mick"
3. Never skip the check. The UTC/BST error has caused wrong greetings before
   (2026.04.11).

**Cross-reference:** canonical partner block in Dex-MickP\CLAUDE.md; the
CEDRIC_MEMORY.md "London Time Protocol" is now a pointer to this rule, not a
third definition.

---

## NotebookLM auth - self-heal before asking Mick

**Rule:** When any `notebooklm` CLI call fails with an auth error
("Authentication expired or invalid", a redirect to accounts.google.com, or a
failing `notebooklm auth check --test`), do NOT immediately ask Mick to log in.
FIRST run `notebooklm login` yourself and inspect its output. If it reports
"Already logged in." (or a re-run of `notebooklm auth check --test` then
passes), auth has been refreshed hands-off - continue silently and do NOT
bother Mick. Only escalate to Mick - asking him to run `notebooklm login` in a
terminal and complete the Google sign-in - if that hands-off login does NOT
self-heal, i.e. the CLI's persistent Chromium profile session is itself dead.

**Why:** The CLI keeps its own persistent Chromium profile at
`C:\Users\pavey\.notebooklm\profiles\default\browser_profile`. The on-disk auth
(`storage_state.json`) can go stale while that browser profile is still logged
into Google - this is the "auth-lie" behind the 2026.07.22 CREI pipeline
failure. A 2026.07.23 experiment confirmed that in exactly this state,
`notebooklm login` completes with ZERO manual input ("Already logged in.") and
re-saves fresh auth. So the common failure is silently recoverable; Mick only
needs to act when the browser-profile session has genuinely expired. Asking him
every time was unnecessary friction.

**How:**
1. On a notebooklm auth failure, run `notebooklm login`. It is effectively
   non-interactive WHEN the browser profile session is valid - it opens the
   CLI's own Chromium, sees the live session, and re-saves auth.
2. Check the result. "Already logged in." -> healed; or re-run
   `notebooklm auth check --test` and if it passes -> healed. Continue silently.
3. Only if login surfaces a Google sign-in page / does not self-heal -> tell
   Mick: "The notebooklm browser-profile session has expired - please run
   `notebooklm login` in a terminal and complete the Google sign-in, then I will
   continue." Mick's Google password / 2FA is his to enter; never Cedric's.

**Cross-reference:** the pipeline's `preflight_auth_check()` in
`sharescope_nlm_researcher.py` now performs this same self-heal automatically
before halting (added 2026.07.23). Ron's agent-def "Auth fallback" section and
the ShareScope SOP auth step should be aligned to this on the next retro pass.

---

---
title: AI4Inv Monthly Webinar Processing
tags:
  - SOP
type: SOP
status: active
version: 1.0
created: 2026-07-27
owner: Mick
related-skills: ai4inv-webinar-processor
related-notebook: DIY.ai - Monthly Webinars (d3d6216b-352f-474e-8261-a6c23fc36cb3)
---

# SOP - AI4Inv Monthly Webinar Processing

## 1. Purpose

This routine turns a monthly "AI for Investors" (diy-investors.ai) members' webinar
recording into three deliverables:

1. A NotebookLM audio source added to the "DIY.ai - Monthly Webinars" notebook.
2. A formatted Word user guide (branded DIY-Investors house style) built from a
   NotebookLM summary of that audio.
3. A short whiteboard-style "explainer" Video Overview (past-tense recap) generated
   from the same source, plus a local .mp4 copy for editing.

It also keeps the notebook's Source Index (studio note + index source) and title up to
date so each month's entry is tracked.

The heavy lifting is codified in the `ai4inv-webinar-processor` skill. This SOP is the
readable end-to-end procedure, including the manual decisions the skill cannot make and
the CLI syntax corrections found on the 2026-07-27 run.

## 2. When to Run It

Run when a new monthly webinar recording is available and Mick asks to "process the
[month] webinar", "add the [month] webinar to NotebookLM", "create the user guide", or
"do the webinar summary video".

## 3. Environment and Prerequisites

- Run in CLAUDE CODE on Mick's PC (local session). The `notebooklm` CLI, `node`,
  `python` and the webinar recordings all live on the local disk.
- NotebookLM auth must be live. Check with `notebooklm auth check --test`. If it fails
  at "Token fetch" and `notebooklm login` hangs without detecting the sign-in, this is
  the Gemini Notebook rebrand bug - do NOT ask Mick to re-login first. Re-export the
  live cookies from the CLI's persistent browser profile with a small Playwright script
  (launch_persistent_context headless on
  C:\Users\pavey\.notebooklm\profiles\default\browser_profile, goto
  https://notebooklm.google.com, verify no accounts.google.com redirect,
  ctx.storage_state(path=storage_state.json)). See CEDRIC_MEMORY 2026-07-27 and the
  auto-memory `notebooklm-login-detection-rebrand-fix`.
- `node` and `npm` present. The `docx` npm module must be installed in a Windows-path
  working dir (NOT /tmp - node.exe cannot resolve the Git-Bash /tmp path). Install it in
  a scratchpad dir and `require('docx')` with that dir as the process cwd.

## 4. Fixed Constants

| Item | Value |
|------|-------|
| Notebook name | DIY.ai - Monthly Webinars |
| Notebook ID | d3d6216b-352f-474e-8261-a6c23fc36cb3 |
| Recordings live under | C:\Users\pavey\Documents\0.0 - AI Projects\<YYYY.MM.DD - ...Webnr>\Recordings\ |

Note: source IDs, index source ID and studio note IDs change every run (the index update
is a delete + re-create cycle). Always fetch current IDs at runtime; never hardcode them.

## 5. CRITICAL - Edition vs Held-Date

The audio FILENAME carries the date the webinar was HELD, which is not always the edition
month. Example: the JUNE 2026 edition was postponed (Mick's illness) and held on
1 July 2026, so its file is dated 2026.07.01. There can be two webinars in one calendar
month (e.g. the 1 July "June edition" and a separate 29 July edition).

Therefore, ALWAYS confirm with Mick which EDITION a recording is before labelling. Then:
- Label the user guide, summary and video by the EDITION month ("June 2026 Webinar").
- Label the Source Index row by the HELD date, noting the edition and any postponement.

## 6. Procedure

### Phase A - Ingest and summarise

0. Inventory check (avoid duplicates):
   - `notebooklm use d3d6216b-352f-474e-8261-a6c23fc36cb3`
   - `notebooklm source list` and `notebooklm note list`
   - Confirm the target edition's audio is not already present. Note the current index
     source ID (title "index.md") and the "Source Index" studio note ID.

1. Locate the audio in the edition's Recordings folder. Prefer the clean .m4a over an
   .mp3 or the RAW .mp4. If only .mp4 exists, extract audio:
   `ffmpeg -i "<raw.mp4>" -vn -acodec copy "<out.m4a>" -y`.

2. Upload and wait for indexing (NOTE: this CLI has NO `--wait` flag on `source add`):
   - `notebooklm source add "<WINDOWS_PATH.m4a>" --title "<YYYY.MM.DD - ... (Month YYYY edition)>" --timeout 600`
   - Capture the returned source ID.
   - `notebooklm source wait <source_id> -n <notebook> --timeout 1200`

3. Generate the summary / user guide, SCOPED to just this source so earlier months do
   not bleed in:
   - `notebooklm ask -n <notebook> -s <source_id> "Create a comprehensive user guide for the <Month YYYY> AI for Investors webinar ... Use UK English ... at least 600 words."`
   - The response is the guide_text. It contains inline citations like [1], [2] - strip
     them for the member-facing Word doc.

4. Build the Word user guide from guide_text:
   - Parse the markdown into sections (heading / body / bullets / task-list checkboxes).
   - Fill the skill template `scripts/build_docx.js` (MONTH_NAME, WEBINAR_DATE = held
     date, OUTPUT_PATH, SECTIONS_JSON). Change `require('/tmp/docx_work/node_modules/docx')`
     to `require('docx')` and run node from a dir where docx is installed.
   - Save to the edition's Recordings folder. Verify the .docx is a valid zip and 100%
     ASCII (Mick's rule) before delivery. Member deliverable uses the branded DIY footer,
     NOT the internal provenance footer (no local paths in a members' document).

5. Update the index source (this CLI uses `source delete`, not `source remove`):
   - `notebooklm source fulltext <index_source_id>` (may just hold a stale path - the
     real index lives in the studio notes; read the "Source Index" note instead).
   - Add a Sources row (held date, audio title, Audio, edition + postponement note), a
     2-3 sentence edition summary and a Tags line; bump "Last Updated".
   - `notebooklm source delete <old_index_source_id> -y`
   - Add the refreshed index as a text/markdown source titled "index.md".

6. Update the studio note(s). There is NO `note update` command - delete and re-create:
   - `notebooklm note delete <source_index_note_id> -y`
   - `cat index_new.txt | notebooklm note create --content - -t "Source Index" -n <notebook>`
   - Also create a per-edition summary note titled
     "<YYYY.MM.DD - AI-4-Investing Webinar Summary (Month YYYY)>" from the cleaned guide.
   - Bump the notebook title: `notebooklm rename "DIY.ai - Monthly Webinars_Updated:YYYY.MM.DD" -n <notebook>`
     (title is POSITIONAL; the notebook goes via -n).

### Phase B - Explainer video

7. Generate the whiteboard past-tense recap, scoped to the edition source. Put the prompt
   in a file to avoid PowerShell/Bash quote escaping:
   - `notebooklm generate video --prompt-file video_prompt.txt -n <notebook> -s <source_id> --format explainer --style whiteboard --wait --timeout 2400`
   - `--format explainer` is the standard Video Overview (works on Mick's paid plan).
     `--format cinematic` is Veo 3 / AI Ultra only and takes 30-40 min - do not use unless
     asked.

8. Download the .mp4 (only if Mick asks; state size). The media URL printed by the
   generate step needs the authenticated session - a plain `curl` returns a Google
   sign-in page. Fetch it through the CLI's logged-in browser profile:
   launch_persistent_context on the browser_profile, `ctx.request.get(url)`, save the
   body when content-type is application/octet-stream / video. Apply any filename suffix
   Mick asks for (e.g. `_Unedited`). Save into the edition's Recordings folder.

## 7. Reusable Video Prompt

Past-tense members' recap (swap the edition month each run):

```
Using the selected source, please prepare a whiteboard style explainer video,
specifically addressed to members of diy-investors.ai. This should be voiced in the
'past tense' - acting as a review summary (reminder) of what was covered last month
i.e. a 'Summary of the <Month YYYY> Webinar'. Focus on just the main sections -
ignoring anything from the members session/Q&A part. The tone should be Professional
Investor to diy-investor (adult to adult) - in UK English throughout please.
```

Source of truth for the prompt: Mick's Vault note
"0.0 - Inbox/2026.06.28 - NBLM Video Prompt (Webinar Summary).md".

## 8. Outputs

- Audio source in the notebook (indexed).
- Word user guide .docx in the edition's Recordings folder.
- Refreshed index source + "Source Index" studio note + per-edition summary note.
- Notebook title date bumped.
- Video Overview artifact in the notebook Studio; local .mp4 in Recordings if requested.

## 9. Gotchas (from the 2026-07-27 build)

- `source add` has no `--wait`; use `source wait <id>` afterwards.
- `note update` does not exist; delete + `note create --content -` (stdin).
- `source remove`/`--confirm` are gone; use `source delete`/`-y`.
- `rename` takes the new title as a positional arg, notebook via `-n`.
- node.exe cannot read a Git-Bash `/tmp` path; install and require `docx` from a real
  Windows-path dir with that dir as cwd.
- Scope the summary query with `ask -s <source_id>` or the guide mixes months.
- The video media URL needs the authenticated browser profile to download.

## 10. Related Skill and Maintenance

- Skill: `ai4inv-webinar-processor` (vault `skills/ai4inv-webinar-processor/`). Its
  SKILL.md was updated on 2026-07-27 to the corrected CLI syntax above and to add the
  Phase B video step. The `/mnt/skills/user` mirror sync is pending a Desktop/Cowork
  session.
- SOP index: this SOP is registered in C:\Vaults\_SOPs\INDEX.md. Any material change here
  must update that entry as the final step.

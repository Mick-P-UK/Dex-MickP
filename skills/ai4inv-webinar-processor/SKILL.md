---
name: ai4inv-webinar-processor
description: >
  Processes a monthly "AI for Investors" (ai4inv) webinar recording into a full NotebookLM
  source, a formatted Word user guide, and an updated notebook index. Use this skill whenever
  Mick asks to "process the [month] webinar", "add the [month] webinar to NotebookLM",
  "create the user guide for [month]", "do the webinar workflow for [month]", or any request
  to run the monthly webinar pipeline for the AI for Investors series. Also triggers on
  "run the webinar skill" or "do the webinar processor for [month]". Always use this skill
  for the webinar workflow - do not attempt it manually without reading it first.
---

# AI for Investors - Monthly Webinar Processor

Automates the end-to-end workflow for ingesting a monthly "AI for Investors" webinar into
NotebookLM and producing a Word user guide and updated index. Uses a sub-agent for the
NotebookLM query so the main chat stays responsive while results are fetched.

Uses: notebooklm-py CLI (teng-lin/notebooklm-py)
Auth: notebooklm-auth-monitor handles session monitoring automatically.
      If auth has lapsed, run: notebooklm login.
      NOTE (2026-07-27): after Google's "Gemini Notebook" rebrand, `notebooklm login`
      can hang and never detect the sign-in. If `notebooklm auth check --test` fails at
      "Token fetch", do NOT ask Mick to re-login first - re-export the live cookies from
      the CLI browser profile with Playwright (launch_persistent_context headless on
      C:\Users\pavey\.notebooklm\profiles\default\browser_profile, goto
      notebooklm.google.com, ctx.storage_state(path=storage_state.json)).
      See memory notebooklm-login-detection-rebrand-fix and the SOP.

---

## Fixed Constants (do not ask Mick for these)

| Item | Value |
|------|-------|
| NotebookLM notebook ID | d3d6216b-352f-474e-8261-a6c23fc36cb3 |
| Notebook name | DIY.ai - Monthly Webinars |
| Webinars base folder (Windows) | C:\Users\pavey\Documents\0.2 - Areas (n)\03.04.02 - AI-4-Inv-Webinars 2026\ |
| Webinars base folder (bash) | /sessions/[session]/mnt/03.04.02 - AI-4-Inv-Webinars 2026/ |
| docx node_modules | /tmp/docx_work/node_modules/docx |
| build_docx.js template | scripts/build_docx.js (in this skill directory) |

Note on source IDs: These change every time the index is updated (delete + re-add cycle).
Always fetch current sources via CLI at runtime - do not hardcode source IDs.

---

## CLI REFERENCE (key commands for this skill)

  notebooklm use <notebook_id>         -- set active notebook
  notebooklm source list               -- list all sources with IDs
  notebooklm source add "<path>" --title "T" --timeout 600  -- add file source (NO --wait flag)
  notebooklm source wait <id> --timeout 1200  -- wait for a source to finish indexing
  notebooklm source add --type text "..."  -- add text source
  notebooklm source delete <id> -y     -- delete source (NOT `source remove --confirm`)
  notebooklm source fulltext <id>      -- get full indexed text of a source
  notebooklm ask -s <source_id> "question"  -- query the notebook, scoped to one source
  notebooklm note list                 -- list studio notes
  notebooklm note create --content - -t "T"  -- create note (reads content from stdin)
  notebooklm note delete <id> -y       -- delete note (NO `note update` exists - delete+create)
  notebooklm rename "<new title>" -n <id>    -- rename notebook (title is positional)
  notebooklm generate video --prompt-file f -s <id> --format explainer --style whiteboard --wait  -- Video Overview

---

## Inputs

Ask Mick for these if not clear from context. If he says "do February" - list the base folder
to confirm the exact subfolder name before proceeding.

1. month_name  -- The EDITION month, human-readable (e.g., "June 2026")
2. webinar_date  -- The HELD date, YYYY.MM.DD (e.g., "2026.07.01")
3. folder_name  -- Exact subfolder name (e.g., "2026.07.01 - AI-4-Investing Webnr")

CRITICAL - EDITION vs HELD DATE: the audio filename carries the date the webinar was HELD,
which is not always the edition month. The June 2026 edition was postponed and held on
1 July 2026 (file dated 2026.07.01); there can be two webinars in one calendar month.
ALWAYS confirm with Mick which EDITION a recording is. Label the guide/summary/video by the
EDITION month; label the Source Index row by the HELD date, noting the edition + postponement.

---

## STEP 0 - Inventory Check (always run first)

Before doing anything, get the current state of the notebook to avoid duplicates:

  notebooklm use d3d6216b-352f-474e-8261-a6c23fc36cb3
  notebooklm source list
  notebooklm note list

From the output, note:
- Which audio sources already exist (check titles for month name or date)
- The current index.md source ID (title contains "index.md")
- The studio note ID for "Source Index"

If the target month's audio is already present -> skip Steps 1 and 2, note its source_id.

---

## STEP 1 - Locate or Extract Audio (skip if already in notebook)

Scan the Recordings subfolder for audio:

  find "/sessions/[session]/mnt/03.04.02 - AI-4-Inv-Webinars 2026/<folder_name>/Recordings/" \
    -maxdepth 4 \( -iname "*.m4a" -o -iname "*.mp3" \) | sort

Audio found: Use it. Prefer .m4a over .mp3 if both exist. Note full Windows and bash paths.

No audio (only .mp4): Extract from the RAW MP4:

  ffmpeg -i "<raw_mp4_path>" -vn -acodec copy "<output_m4a_path>" -y

Name the output M4A by replacing _RAW_ with _RAW-Audio_ and changing extension to .m4a,
saved in the same Recordings folder. Confirm file size after extraction.
If ffmpeg is not installed: apt-get install -y ffmpeg

---

## STEP 2 - Upload Audio to NotebookLM (skip if already in notebook)

  notebooklm use d3d6216b-352f-474e-8261-a6c23fc36cb3
  notebooklm source add "<WINDOWS_PATH_to_audio_file>" --title "<YYYY.MM.DD - AI-4-Inv Webinar Audio (Month YYYY edition)>" --timeout 600

Note the source_id returned in the CLI output.
There is NO --wait flag on `source add` in this CLI. Wait separately:

  notebooklm source wait <source_id> -n d3d6216b-352f-474e-8261-a6c23fc36cb3 --timeout 1200

A 50-60MB m4a takes a couple of minutes to index. Only query once `source wait` returns
"Source ready".

---

## STEP 3 - Generate User Guide via Sub-Agent

Why a sub-agent?
The NotebookLM query on large audio files takes 1-3 minutes. Running it in a sub-agent keeps
the main chat free while results come back.

Spawn a sub-agent with this exact briefing (fill in the placeholders):

  -------
  You are a task runner. Query NotebookLM for a webinar user guide.

  notebook_id: d3d6216b-352f-474e-8261-a6c23fc36cb3
  month_name: <MONTH_NAME>

  Your job:
  1. Run these bash commands (scope to the new source with -s so earlier months do not bleed in):
       notebooklm use d3d6216b-352f-474e-8261-a6c23fc36cb3
       notebooklm ask -s <source_id> "Create a comprehensive user guide for the <month_name> AI for Investors webinar covering all key topics, tools and workflows demonstrated in the main teaching sessions. Ignore the members Q&A. Use UK English. At least 600 words."
  2. Wait up to 3 minutes for the response.
  3. If you receive a full guide text (500+ words): return the FULL response verbatim --
     every word, do not summarise, truncate, or paraphrase.
  4. If the command errors, times out, or returns fewer than 100 words: return exactly
     QUERY_FAILED: <reason or timeout> -- nothing else.

  Do NOT generate, invent, or supplement any content yourself under any circumstances.
  -------

On receiving the sub-agent result:
- If it starts with "QUERY_FAILED": stop and tell Mick the query failed -- suggest waiting
  2 minutes for audio indexing to complete, then retrying. Do NOT proceed to Step 4.
- If it returns a full guide text: proceed to Step 4 with that text as guide_text.

The content in guide_text must come from the actual webinar audio. Never substitute
invented or generic content if the query fails.

---

## STEP 4 - Build Word Document (only if Step 3 returned real content)

Ensure docx module is installed in a WINDOWS-PATH working dir. node.exe cannot resolve a
Git-Bash /tmp path, so do NOT use /tmp/docx_work on Windows. Use the session scratchpad:

  WD="<scratchpad>/docx_work"; mkdir -p "$WD"; (cd "$WD" && npm install docx)

In the copy of build_docx.js you run, change
  require('/tmp/docx_work/node_modules/docx')  ->  require('docx')
and run node with that working dir as the cwd (`cd "$WD" && node build_guide.js`) so the
relative require resolves.

Read scripts/build_docx.js from this skill's directory. Adapt it by substituting placeholders:

  MONTH_NAME   -> e.g., "February 2026"
  WEBINAR_DATE -> e.g., "25 February 2026"
  OUTPUT_PATH  -> bash path to Recordings folder + date + filename
  SECTIONS_JSON -> parsed sections array

Parsing guide_text into SECTIONS_JSON:
Parse each ### or ## heading as a new section object:
  { "heading": "...", "body": ["..."], "bullets": ["..."], "checkboxes": ["..."] }
- Plain paragraphs -> body array
- Lines starting with -, *, + -> bullets array
- Lines with - [ ] checkbox markers -> checkboxes array

Write adapted script to /tmp/build_<month>_guide.js and run it.
Confirm the .docx file exists in the Recordings folder and is >10KB.

---

## STEP 5 - Update index.md Source

Get the current index.md content:

  notebooklm source fulltext <current_index_md_source_id>

Build the updated content:
1. Increment the source # from the last row in the Sources table
2. Add a new Sources row: <N> | <today_YYYY.MM.DD> | <audio_filename> | Audio | <month_name> webinar
3. Write a 2-3 sentence Webinar Summary from guide_text
4. Extract Tags from guide_text -- look for: Perplexity, NBLM, System Prompts, User Prompts,
   Spaces, Google Sheets, Live Data, Privacy Settings, n8n, Claude, Cowork, ShareScope,
   Portfolio Analysis, Prompting, Mind Maps, TA, Scheduled Tasks, Automation, Descript,
   Otter.ai, Zoom, NotebookLM, Gemini
5. Update "Last Updated" date at the top

Delete old source and re-add (this CLI uses `source delete`, not `source remove`).
Write the updated index to a real .md file to avoid quote-escaping, then add it:

  notebooklm source delete <old_index_md_source_id> -y
  notebooklm source add "<scratchpad>/index.md" --title "index.md"

Note the new source_id from the CLI output. (The old index source may just hold a stale
file path - the authoritative index content lives in the "Source Index" studio note.)

---

## STEP 6 - Update Studio Note(s)

There is NO `note update` command in this CLI. Delete the note and recreate it, reading
the content from stdin (avoids all quote-escaping):

  notebooklm note delete <source_index_note_id> -y
  cat "<scratchpad>/index_new.txt" | notebooklm note create --content - -t "Source Index" -n d3d6216b-352f-474e-8261-a6c23fc36cb3

Also create a per-edition summary note (matches the existing per-webinar notes), from the
cleaned guide text:

  cat "<scratchpad>/guide_clean.md" | notebooklm note create --content - -t "<YYYY.MM.DD - AI-4-Investing Webinar Summary (Month YYYY)>" -n d3d6216b-352f-474e-8261-a6c23fc36cb3

Then bump the notebook title (title is POSITIONAL, notebook via -n):

  notebooklm rename "DIY.ai - Monthly Webinars_Updated:YYYY.MM.DD" -n d3d6216b-352f-474e-8261-a6c23fc36cb3

---

## STEP 7 - Generate the Explainer Video (Phase B)

Generate a whiteboard-style, past-tense members' recap, SCOPED to this edition's source.
Put the prompt in a file to avoid PowerShell/Bash quote escaping:

  notebooklm generate video --prompt-file "<scratchpad>/video_prompt.txt" \
    -n d3d6216b-352f-474e-8261-a6c23fc36cb3 -s <source_id> \
    --format explainer --style whiteboard --wait --timeout 2400

- --format explainer is the standard Video Overview (fine on Mick's paid plan). Do NOT use
  --format cinematic (Veo 3 / AI Ultra only, 30-40 min) unless asked.
- The prompt template lives in Mick's Vault: "0.0 - Inbox/2026.06.28 - NBLM Video Prompt
  (Webinar Summary).md". Swap in the EDITION month (which may differ from the held date -
  see Inputs). Confirm the exact wording with Mick before generating.

Download the .mp4 ONLY if Mick asks (state the size). The media URL printed by the generate
step needs the authenticated session - a plain curl returns a Google sign-in page. Fetch it
through the CLI's logged-in browser profile: launch_persistent_context on the browser_profile,
`ctx.request.get(url)`, save the body when content-type is application/octet-stream / video.
Apply any filename suffix Mick asks for (e.g. _Unedited) and save into the Recordings folder.

---

## Completion Report to Mick

Report:
- Status for each of the 7 steps (done / skipped / failed)
- Path to the Word user guide (.docx in the edition's Recordings folder)
- The Video Overview status + notebook link:
  https://notebooklm.google.com/notebook/d3d6216b-352f-474e-8261-a6c23fc36cb3
- Local .mp4 path if downloaded
- Tags applied for this edition
- New index.md source_id + new Source Index note_id (so the next run can find them)
- Any issues or things to watch for next time

---

## Error Reference

| Problem | Action |
|---------|--------|
| ffmpeg not found | apt-get install -y ffmpeg |
| NBLM query fails/times out | Stop; tell Mick to wait 2 min and retry |
| docx module missing | Install in a Windows-path dir: (cd <scratchpad>/docx_work && npm install docx); require('docx') with that cwd |
| `--wait` not a valid option | Correct: `source add ...` then `source wait <id>` |
| `source remove` / `note update` not found | Use `source delete -y` / delete + `note create --content -` |
| source add times out | Raise --timeout; then check `notebooklm source list` - it may have landed anyway |
| Audio already in notebook | Skip Steps 1+2; use existing source_id for Step 3 query |
| Auth check fails at Token fetch / login hangs | Gemini rebrand bug - re-export cookies from the browser profile with Playwright (see header + SOP); do NOT ask Mick to re-login first |
| Video won't download via curl | URL needs auth; fetch through the browser profile (ctx.request.get) |

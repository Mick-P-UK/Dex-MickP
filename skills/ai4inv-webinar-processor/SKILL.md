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
      If auth has lapsed, run: notebooklm login

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
  notebooklm source add "<path>"       -- add file source
  notebooklm source add "<path>" --wait  -- add and wait for indexing
  notebooklm source add --text "..."   -- add text source
  notebooklm source remove <id> --confirm  -- delete source
  notebooklm source fulltext <id>      -- get full indexed text of a source
  notebooklm ask "question"            -- query the notebook
  notebooklm note list                 -- list studio notes
  notebooklm note create --title "T" --content "C"   -- create note
  notebooklm note update <id> --title "T" --content "C"  -- update note
  notebooklm note delete <id> --confirm  -- delete note

---

## Inputs

Ask Mick for these if not clear from context. If he says "do February" - list the base folder
to confirm the exact subfolder name before proceeding.

1. month_name  -- Human-readable (e.g., "February 2026")
2. webinar_date  -- YYYY.MM.DD format (e.g., "2026.02.25")
3. folder_name  -- Exact subfolder name (e.g., "2026.02.25 - AI-4-Inv Webnr (Feb '26)")

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
  notebooklm source add "<WINDOWS_PATH_to_audio_file>" --wait

Note the source_id returned in the CLI output.
The --wait flag ensures indexing completes before querying.
If indexing is slow, wait an additional 30 seconds before querying.

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
  1. Run these bash commands:
       notebooklm use d3d6216b-352f-474e-8261-a6c23fc36cb3
       notebooklm ask "Create a user guide for the <month_name> webinar covering all key topics and tools demonstrated"
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

Ensure docx module is installed:

  node -e "require('/tmp/docx_work/node_modules/docx'); console.log('ok')" 2>/dev/null || \
    (cd /tmp && mkdir -p docx_work && cd docx_work && npm install docx 2>&1 | tail -2)

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

Delete old source and re-add:

  notebooklm source remove <old_index_md_source_id> --confirm
  notebooklm source add --text "<full updated index content>"

Note the new source_id from the CLI output.

---

## STEP 6 - Update Studio Note

  notebooklm note update <note_id_from_Step_0> \
    --title "Source Index" \
    --content "<identical to updated index.md content>"

If note update is not available, delete and recreate:

  notebooklm note delete <note_id> --confirm
  notebooklm note create --title "Source Index" --content "<updated index content>"

---

## Completion Report to Mick

Report:
- Status for each of the 6 steps (done / skipped / failed)
- computer:// link to the Word doc
- NotebookLM link: https://notebooklm.google.com/notebook/d3d6216b-352f-474e-8261-a6c23fc36cb3
- Tags applied for this month
- New index.md source_id (so the next run can find it)
- Any issues or things to watch for next time

---

## Error Reference

| Problem | Action |
|---------|--------|
| ffmpeg not found | apt-get install -y ffmpeg |
| NBLM query fails/times out | Stop; tell Mick to wait 2 min and retry |
| docx module missing | cd /tmp && mkdir -p docx_work && cd docx_work && npm install docx |
| source add times out | Check notebooklm source list -- it may have landed anyway |
| Audio already in notebook | Skip Steps 1+2; use existing source_id for Step 3 query |
| Auth expired | Run: notebooklm login (browser opens, 30 seconds) |

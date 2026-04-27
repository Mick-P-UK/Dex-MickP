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

---

## Fixed Constants (do not ask Mick for these)

| Item | Value |
|------|-------|
| NotebookLM notebook ID | `d3d6216b-352f-474e-8261-a6c23fc36cb3` |
| Notebook name | DIY.ai - Monthly Webinars |
| Webinars base folder (Windows) | `C:\Users\pavey\Documents\0.2 - Areas (n)\03.04.02 - AI-4-Inv-Webinars 2026\` |
| Webinars base folder (bash) | `/sessions/quirky-nifty-edison/mnt/03.04.02 - AI-4-Inv-Webinars 2026/` |
| docx node_modules | `/tmp/docx_work/node_modules/docx` |
| build_docx.js template | `scripts/build_docx.js` (in this skill directory) |

> **Note on index.md source_id:** This changes every time the index is updated (delete + re-add
> cycle). Always fetch the current source_id via `notebook_get` at runtime - do not hardcode it.

---

## Inputs

Ask Mick for these if not clear from context. If he says "do February" - list the base folder
to confirm the exact subfolder name before proceeding.

1. **month_name** — Human-readable (e.g., "February 2026")
2. **webinar_date** — YYYY.MM.DD format (e.g., "2026.02.25")
3. **folder_name** — Exact subfolder name (e.g., "2026.02.25 - AI-4-Inv Webnr (Feb '26)")

---

## STEP 0 - Inventory Check (always run first)

Before doing anything, get the current state of the notebook to avoid duplicates:

```
Tool: mcp__notebooklm-mcp__notebook_get
  notebook_id: d3d6216b-352f-474e-8261-a6c23fc36cb3
```

From the response, note:
- Which audio sources already exist (check titles for month name or date)
- The current `index.md` source_id (title = "index.md")
- The current Studio note_id for "Source Index" (use `note action=list` if needed)

If the target month's audio is already present → **skip Steps 1 and 2**, note its source_id.

---

## STEP 1 - Locate or Extract Audio (skip if already in notebook)

Scan the Recordings subfolder for audio:
```bash
find "/sessions/quirky-nifty-edison/mnt/03.04.02 - AI-4-Inv-Webinars 2026/<folder_name>/Recordings/" \
  -maxdepth 4 \( -iname "*.m4a" -o -iname "*.mp3" \) | sort
```

**Audio found:** Use it. Prefer .m4a over .mp3 if both exist. Note full Windows and bash paths.

**No audio (only .mp4):** Extract from the RAW MP4:
```bash
# Find RAW MP4
find "/sessions/quirky-nifty-edison/mnt/03.04.02 - AI-4-Inv-Webinars 2026/<folder_name>/Recordings/" \
  -maxdepth 1 -iname "*RAW*.mp4" | head -1

# Extract audio (stream copy - no re-encode, very fast)
ffmpeg -i "<raw_mp4_path>" -vn -acodec copy "<output_m4a_path>" -y
```
Name the output M4A by replacing `_RAW_` with `_RAW-Audio_` and changing extension to .m4a,
saved in the same Recordings folder. Confirm file size after extraction.
If ffmpeg is not installed: `apt-get install -y ffmpeg`

---

## STEP 2 - Upload Audio to NotebookLM (skip if already in notebook)

```
Tool: mcp__notebooklm-mcp__source_add
  notebook_id: d3d6216b-352f-474e-8261-a6c23fc36cb3
  source_type: file
  file_path: <WINDOWS_PATH_to_audio_file>
  wait: false
```

Note the returned `source_id`. Wait 30 seconds to allow NotebookLM to begin indexing before querying.

---

## STEP 3 - Generate User Guide via Sub-Agent

### Why a sub-agent?
The NotebookLM query on large audio files takes 1-3 minutes. Running it in a sub-agent keeps
the main chat free while results come back.

### Start the async query
Critically, pass **only** the target audio source_id to keep the query fast and focused:

```
Tool: mcp__notebooklm-mcp__notebook_query_start
  notebook_id: d3d6216b-352f-474e-8261-a6c23fc36cb3
  query: "Create a user guide for the <month_name> webinar covering all key topics and tools demonstrated"
  source_ids: [<audio_source_id_for_this_month>]
```

Note the returned `query_id`.

### Spawn a sub-agent with this exact briefing (fill in the placeholders):

---
You are a task runner. A NotebookLM query has been started.

- query_id: `<QUERY_ID>`
- notebook_id: `d3d6216b-352f-474e-8261-a6c23fc36cb3`

Your only job:
1. Call `mcp__notebooklm-mcp__notebook_query_status` with that query_id
2. If status is "in_progress", run `bash sleep 20` and poll again
3. Poll up to 15 times (about 5 minutes total)
4. When status is "completed": return the FULL response text verbatim — every word, do not
   summarise, truncate, or paraphrase. The response should be 2000+ words.
5. If status is "error" or all 15 polls exhaust without completion: return exactly
   "QUERY_FAILED: <reason or 'timeout'>" — nothing else.

Do NOT generate, invent, or supplement any content yourself under any circumstances.
---

### On receiving the sub-agent result:
- If it starts with "QUERY_FAILED": stop and tell Mick the query failed — suggest waiting
  2 minutes for audio indexing to complete, then retrying. Do NOT proceed to Step 4.
- If it returns a full guide text: proceed to Step 4 with that text as `guide_text`.

**The content in guide_text must come from the actual webinar audio. Never substitute
invented or generic content if the query fails.**

---

## STEP 4 - Build Word Document (only if Step 3 returned real content)

Ensure docx module is installed:
```bash
node -e "require('/tmp/docx_work/node_modules/docx'); console.log('ok')" 2>/dev/null || \
  (cd /tmp && mkdir -p docx_work && cd docx_work && npm install docx 2>&1 | tail -2)
```

Read `scripts/build_docx.js` from this skill's directory. Adapt it by substituting these
placeholders with actual values:

| Placeholder | Value |
|-------------|-------|
| `{{MONTH_NAME}}` | e.g., "February 2026" |
| `{{WEBINAR_DATE}}` | e.g., "25 February 2026" |
| `{{OUTPUT_PATH}}` | bash path: `.../Recordings/<webinar_date> - AI-4-Inv_<MonAbbr>-Webinar_User-Guide.docx` |
| `{{SECTIONS_JSON}}` | Parsed sections array (see below) |

**Parsing guide_text into SECTIONS_JSON:**
The guide will have markdown headings. Parse each `###` or `##` heading as a new section:
```json
[
  {
    "heading": "1.  Introduction and Objectives",
    "body": ["paragraph text...", "second paragraph..."],
    "bullets": ["bullet item 1", "bullet item 2"],
    "checkboxes": ["process step 1", "process step 2"]
  }
]
```
- Plain paragraphs → `body` array
- Lines starting with `•`, `-`, or `*` → `bullets` array
- Lines with `□`, `- [ ]`, or checkbox markers → `checkboxes` array
- Sub-headings within a section → add as `body` entry prefixed with `##`

Write the adapted script to `/tmp/build_<month>_guide.js` and run it.
Confirm the .docx file exists in the Recordings folder and is >10KB.

---

## STEP 5 - Update index.md Source

Fetch the current index.md content (use the source_id found in Step 0):
```
Tool: mcp__notebooklm-mcp__source_get_content
  source_id: <current_index_md_source_id>
```

Build the updated content:
1. Increment the source # from the last row in the Sources table
2. Add a new Sources row: `<N> | <today_YYYY.MM.DD> | <audio_filename> | Audio | <month_name> webinar`
3. Write a 2-3 sentence Webinar Summary from guide_text covering: main themes, key tools, standout workflows
4. Extract Tags from guide_text — look for: Perplexity, NBLM, System Prompts, User Prompts,
   Spaces, Google Sheets, Live Data, Privacy Settings, n8n, Claude, Cowork, ShareScope,
   Portfolio Analysis, Prompting, Mind Maps, TA, Scheduled Tasks, Automation, Descript,
   Otter.ai, Zoom, NotebookLM, Gemini
5. Update "Last Updated" date at the top

Delete old source and re-add:
```
Tool: mcp__notebooklm-mcp__source_delete (confirm: true)
Tool: mcp__notebooklm-mcp__source_add (source_type: text, title: "index.md")
```
Note the new source_id returned.

---

## STEP 6 - Update Studio Note

```
Tool: mcp__notebooklm-mcp__note
  action: update
  notebook_id: d3d6216b-352f-474e-8261-a6c23fc36cb3
  note_id: <note_id_from_Step_0>
  title: Source Index
  content: <identical to updated index.md>
```

---

## Completion Report to Mick

Report:
- ✅/❌ status for each of the 6 steps
- computer:// link to the Word doc
- NotebookLM link: https://notebooklm.google.com/notebook/d3d6216b-352f-474e-8261-a6c23fc36cb3
- Tags applied for this month
- New index.md source_id (so the next run can find it)
- Any issues or things to watch for next time

---

## Error Reference

| Problem | Action |
|---------|--------|
| ffmpeg not found | `apt-get install -y ffmpeg` |
| NBLM query fails/times out | Stop; tell Mick to wait 2 min and retry |
| docx module missing | `cd /tmp && mkdir -p docx_work && cd docx_work && npm install docx` |
| source_add times out | Check `notebook_get` first — it may have landed |
| Audio already in notebook | Skip Steps 1+2; use existing source_id for Step 3 query |

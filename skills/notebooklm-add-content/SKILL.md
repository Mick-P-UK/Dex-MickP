---
name: notebooklm-add-content
description: >
  Adds new sources to an existing NotebookLM notebook, updates the dual index
  (studio note + queryable source copy), and refreshes the notebook title
  _Updated: date. Use this skill whenever Mick says "add sources to a notebook",
  "add this to the notebook", "update the notebook with...", "load these files
  into the notebook", or any request to add content to an existing NotebookLM
  notebook. Also use when Mick wants to run a research sweep on an existing
  notebook. Always preserves original date_added for existing index entries.
---

# Skill 2: NotebookLM Add Content

Adds new sources to an existing NotebookLM notebook, keeps the dual index
current, and updates the notebook title with today's _Updated: date.

Uses: notebooklm-py CLI (teng-lin/notebooklm-py)
Auth: notebooklm-auth-monitor handles session monitoring automatically.
      If auth has lapsed, run: notebooklm login

---

## CLI REFERENCE (key commands for this skill)

```bash
# List notebooks
notebooklm list

# Set active notebook context
notebooklm use <notebook_id>

# Add sources
notebooklm source add "https://example.com"           # URL
notebooklm source add "./path/to/file.pdf"            # local file
notebooklm source add --text "raw text content"       # pasted text
notebooklm source add "./file.pdf" --wait             # wait for indexing

# List sources in active notebook
notebooklm source list

# Remove a source
notebooklm source remove <source_id> --confirm

# Rename notebook
notebooklm notebook rename <notebook_id> "New Title"

# Research sweep (web)
notebooklm source add-research "topic query"

# Notes (studio notes)
notebooklm note list
notebooklm note create --title "Title" --content "body text"
notebooklm note delete <note_id> --confirm
```

---

## MANDATORY NAMING RULES

Identical to notebooklm-notebook-setup skill. Summary:
- Notebook title: [Title]_Updated:YYYY.MM.DD (no date prefix, dots in date)
- Source titles:  YYYY.MM.DD - [Descriptive Title] (date = article date)
- Index titles:   Index_Updated:YYYY.MM.DD - HH.MM (date + London time)
  The HH.MM timestamp prevents confusion when old and new index versions
  coexist. Always delete the earlier-timestamped one; keep the later one.

---

## PHASE 1 -- IDENTIFY THE TARGET NOTEBOOK

1. Ask Mick which notebook to add to, if not specified
2. If no ID known, run: notebooklm list
3. Get today's London date AND time via python3
4. Set the active notebook: notebooklm use <notebook_id>
5. Read the existing index source to extract:
   - Notebook Created date (FIXED -- never change this)
   - All existing source entries with their original date_added values
   - Current source count (to continue numbering sequentially)
   Run: notebooklm source list  (to see all sources and identify the index copy)
   Run: notebooklm ask "Show me the full current index" (to read index content)

---

## PHASE 2 -- ADD NEW SOURCES

Accept new sources in any combination: local file paths, URLs, raw text.

### Local Files
- .docx: extract text via python3 (python-docx) then add as text source
- .md / .txt: read content then add as text source
- .pdf / .mp3 / .m4a: add directly as file
```bash
notebooklm source add "<windows_path_or_bash_path>" --wait
```
- Title format: YYYY.MM.DD - [filename without extension]

### URLs
- Research publication date via web search before adding
```bash
notebooklm source add "https://..." --wait
```
- Title format: YYYY.MM.DD - [descriptive title]

### Raw Text
```bash
notebooklm source add --text "content here"
```

### Source Log
Append each new source to internal log:
  source_number | title | type | date_of_article | date_added | contents_summary

IMPORTANT: Existing entries retain their ORIGINAL date_added. Only new entries
get today's date as date_added.

After all new sources added, rename the notebook:
```bash
notebooklm notebook rename <notebook_id> "[Title without existing _Updated suffix]_Updated:YYYY.MM.DD"
```

---

## PHASE 3 -- RESEARCH SWEEP (offer automatically)

Always offer after new sources are loaded:
"Would you like a NotebookLM research sweep for additional sources?
  Fast -- approx 30 seconds, approx 10 sources
  Deep -- approx 5 minutes, approx 40 sources"

If accepted:
```bash
notebooklm source add-research "relevant topic query"
```
Append imported sources to internal source log (date_added = today).
Update notebook title _Updated: date.

If declined: proceed to Phase 4.

---

## PHASE 4 -- UPDATE THE INDEX

Regenerate the full index from the internal source log (existing + new entries).

### Index Header (exact format):
  Index to Notebook: [Notebook Title without _Updated suffix]
  Notebook Created:  DD Month YYYY  <-- FIXED from original creation date
  Last Updated:      DD Month YYYY  <-- today
  ============================================================

### Entry Format:
  **SOURCE N Title: [full source title]**
  Type:            [source type]
  Date of Article: DD Month YYYY
  Date Added:      DD Month YYYY  <-- original date for existing, today for new
  Contents:        [1-3 sentence description]
  ------------------------------------------------------------

### Update Studio Note:
```bash
# List existing notes to find old index note ID
notebooklm note list

# Delete old index note
notebooklm note delete <old_note_id> --confirm

# Create new note
notebooklm note create \
  --title "Index_Updated:YYYY.MM.DD - HH.MM" \
  --content "<full regenerated index text>"
```

### Update Index Source Copy:
```bash
# Remove old index source (identified by "Index_Updated" in title)
notebooklm source remove <old_index_source_id> --confirm

# Add new index source
notebooklm source add --text "<full index content>" --wait
# Note: title the source "Index_Updated:YYYY.MM.DD - HH.MM" in the UI
# (notebooklm-py CLI uses the content as title fallback if not specified)
```

---

## PHASE 5 -- CONFIRM AND REPORT

Output a clean summary:
- Notebook title (updated) and URL
- New sources added: N (list with titles and dates)
- Research sweep: sources found and imported (if run)
- Index updated: studio note and source copy both refreshed with new timestamp
- Total sources now in notebook: N
- Reminder to delete old index source copy (identified by earlier timestamp)

---

## TECHNICAL NOTES

- Always read existing index first to preserve Notebook Created date
- Source order is chronological only -- new sources always appear after existing
- notebooklm use <id> sets context for all subsequent commands in that session
- If a source add times out, run: notebooklm source list to check if it landed
- Sessions last days to weeks; CSRF tokens auto-refresh transparently
- If auth expired: notebooklm login (browser opens, 30-second fix)

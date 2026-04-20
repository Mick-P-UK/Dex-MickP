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
2. Retrieve notebook by name search or direct ID
3. Get today's London date AND time via python3
4. Read the existing index source copy to extract:
   - Notebook Created date (FIXED -- never change this)
   - All existing source entries with their original date_added values
   - Current source count (to continue numbering sequentially)
5. Log all existing sources in internal source log before adding anything new

---

## PHASE 2 -- ADD NEW SOURCES

Accept new sources in any combination: local file paths, URLs, raw text.

### Local Files
- Copy: Filesystem:copy_file_user_to_claude
- .docx: extract text via bash_tool + python3-docx
- .md / .txt: read via Filesystem:read_text_file
- Add: notebooklm-mcp:source_add, source_type=text
- Title: YYYY.MM.DD - [filename without extension]

### URLs
- Research publication date via web_search before adding
- Add: notebooklm-mcp:source_add, source_type=url
- Title: YYYY.MM.DD - [descriptive title]

### Raw Text
- Add: notebooklm-mcp:source_add, source_type=text

### Source Log
Append each new source to the internal log:
  source_number | title | type | date_of_article | date_added | contents_summary

IMPORTANT: Existing entries retain their ORIGINAL date_added. Only new entries
get today's date as date_added.

After all new sources added:
- Update notebook title: notebooklm-mcp:notebook_rename
- New title: [Title without existing _Updated suffix]_Updated:YYYY.MM.DD

---

## PHASE 3 -- RESEARCH SWEEP (offer automatically)

Always offer after new sources are loaded:
"Would you like a NotebookLM research sweep for additional sources?
  Fast -- approx 30 seconds, approx 10 sources
  Deep -- approx 5 minutes, approx 40 sources"

If accepted:
1. notebooklm-mcp:research_start (mode: fast or deep, source: web)
2. Poll notebooklm-mcp:research_status until complete
3. Import results
4. Append imported sources to internal source log (date_added = today)
5. Update notebook title _Updated: date

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
1. List existing notes: notebooklm-mcp:note, action=list
2. Delete old index note: notebooklm-mcp:note, action=delete, confirm=true
3. Create new note: notebooklm-mcp:note, action=create
   - title: Index_Updated:YYYY.MM.DD - HH.MM (current London time)
   - content: full regenerated index

### Update Index Source Copy:
- Add new text source with full index content
- Title: Index_Updated:YYYY.MM.DD - HH.MM (current London time)
- Inform Mick the old index source copy can be manually deleted in the UI
  The newer timestamp makes it obvious which one to keep

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

- Always read existing index first to preserve Notebook Created date and
  existing source entries with original date_added values
- Source order is chronological only -- new sources always appear after existing
- Index timestamps (HH.MM) make it unambiguous which copy is current
- nlm login may be required at the start of each Claude Desktop session

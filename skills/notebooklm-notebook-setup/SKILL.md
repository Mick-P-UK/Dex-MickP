---
name: notebooklm-notebook-setup
description: >
  Creates a new NotebookLM notebook from scratch and fully initialises it with
  sources, an optional research sweep, and a dual index (studio note + queryable
  source copy). Use this skill whenever Mick says "set up a new notebook",
  "create a NotebookLM notebook called...", "new notebook with these sources",
  "set up a notebook and index it", or any request to create and populate a
  NotebookLM notebook. Always use this skill for new notebook creation -- do
  not attempt to create notebooks without reading this skill first.
---

# Skill 1: NotebookLM Notebook Setup

> **STOP -- READ BEFORE DOING ANYTHING ELSE**
> The FIRST action when setting up any notebook is to READ THIS SKILL IN FULL.
> Do NOT create a notebook before reading the naming rules below.
> Failure to apply naming rules at creation is a hard error.

Fully initialises a new NotebookLM notebook: creates it, adds sources,
optionally runs a research sweep, builds a dual index (studio note + queryable
source copy), and applies the correct title convention.

---

## MANDATORY NAMING RULES (apply throughout all phases)

### Notebook Title Convention
- NO date prefix on notebook titles -- ever
- On creation:         [Title of Notebook]
- After sources added: [Title of Notebook]_Updated:YYYY.MM.DD
- _Updated: date uses DOTS as separators (not hyphens or slashes)
- GOOD: PROPPS - Bank of England bail-in provisions_Updated:2026.04.19
- BAD:  2026.04.19 - PROPPS... (date prefix never allowed)
- BAD:  PROPPS..._updated 20 April (wrong suffix format)

### Source Title Convention
- All sources prefixed: YYYY.MM.DD - [Descriptive Title]
- Date = date of the original article/document (NOT the date added)
- Example: 2026.04.13 - BoE Operational Guide to Bail-in Resolution (2026)

### Index Title Convention (studio note AND source copy use same title)
- Format: Index_Updated:YYYY.MM.DD - HH.MM
- Date = date of most recent revision; HH.MM = London time (BST or GMT)
- Example: Index_Updated:2026.04.19 - 20.50
- IMPORTANT: Including the time prevents ambiguity when two index versions
  exist simultaneously (old and new). Always delete the earlier-timestamped
  one -- keep the later one.

---

## PHASE 1 -- CREATE THE NOTEBOOK

1. Accept notebook title from Mick (title only -- no date prefix)
2. Verify title follows naming rules above; correct silently if needed
3. Get today's London date AND time via python3 (needed for index title)
4. Create notebook: notebooklm-mcp:notebook_create
5. Log internally: notebook_id, URL, creation_date (FIXED permanently)
6. > **MANDATORY -- DO THIS BEFORE ADDING ANY SOURCES**
   > Create a placeholder index source IMMEDIATELY after notebook creation.
   > This claims position 1 in the sources panel permanently.
   > Once any other source is added, this window is GONE -- the index
   > will be out of order forever. This is a hard error if missed.
   - notebooklm-mcp:source_add, source_type=text
   - title: Index_Updated:YYYY.MM.DD - HH.MM (use current London time)
   - text: "INDEX PLACEHOLDER -- will be populated once all sources are loaded."
   - This ensures the index appears at position 1 in the sources panel
     (NotebookLM orders sources chronologically; earliest = top)
7. Notebook title stays as [Title] at this stage -- suffix added after sources

---

## PHASE 2 -- ADD SOURCES

Accept sources in any combination of: local file paths, URLs, raw text.

### Local Files
- Copy to Claude environment: Filesystem:copy_file_user_to_claude
- .docx: extract text via bash_tool using python3 + python-docx:
    from docx import Document
    doc = Document('/mnt/user-data/uploads/filename.docx')
    text = '\n'.join([p.text for p in doc.paragraphs if p.text.strip()])
- .md / .txt: read via Filesystem:read_text_file
- Add via notebooklm-mcp:source_add, source_type=text
- Title: YYYY.MM.DD - [filename without extension]

### URLs
- Research publication date via web_search before adding
- Add via notebooklm-mcp:source_add, source_type=url
- Title: YYYY.MM.DD - [descriptive title of the article/document]

### Raw Text
- Add directly via notebooklm-mcp:source_add, source_type=text

### Source Log (maintain internally throughout)
After each source added, append one entry:
  source_number | title | type | date_of_article | date_added | contents_summary

After ALL sources added:
- Rename notebook: notebooklm-mcp:notebook_rename
- New title: [Title]_Updated:YYYY.MM.DD

---

## PHASE 3 -- NOTEBOOKLM RESEARCH SWEEP (offer automatically)

Always offer after initial sources are loaded:
"Would you like a NotebookLM research sweep for additional sources?
  Fast -- approx 30 seconds, approx 10 sources
  Deep -- approx 5 minutes, approx 40 sources"

If accepted:
1. notebooklm-mcp:research_start (mode: fast or deep, source: web)
2. Poll notebooklm-mcp:research_status until complete
3. Import results
4. Add imported sources to internal source log (date_added = today)
5. Update notebook title _Updated: date if new sources added

If declined: proceed to Phase 4.

---

## PHASE 4 -- FINALISE THE INDEX

Generate full index content from the internal source log.

### Index Header (exact format):
  Index to Notebook: [Notebook Title without _Updated suffix]
  Notebook Created:  DD Month YYYY  <-- FIXED, use creation_date from Phase 1
  Last Updated:      DD Month YYYY  <-- today
  ============================================================

### Entry Format (repeat for each source):
  **SOURCE N Title: [full source title]**
  Type:            [e.g. URL - Bank of England Official Publication]
  Date of Article: DD Month YYYY
  Date Added:      DD Month YYYY
  Contents:        [1-3 sentence description of what this source covers]
  ------------------------------------------------------------

  N starts at 1. Exclude the placeholder from numbered entries.
  Order entries in sequence sources were added.

### Create Studio Note:
- notebooklm-mcp:note, action=create
- title: Index_Updated:YYYY.MM.DD - HH.MM (current London time)
- content: full index text as above

### Finalise Index Source:
- Add full index content as new text source
- Title: Index_Updated:YYYY.MM.DD - HH.MM (current London time)
- The placeholder (position 1) can be manually deleted in the NotebookLM UI
  The new live index source will have a later timestamp -- keep that one

---

## PHASE 5 -- CONFIRM AND REPORT

Output a clean summary covering:
- Final notebook title and URL
- Notebook ID
- Table of all sources: #, Title, Type, Date of Article, Date Added
- Confirmation of index studio note and index source copy (both timestamped)
- Research sweep results if run
- Reminder to Mick to manually delete the placeholder from the sources panel

---

## TECHNICAL NOTES

- .docx files CANNOT be uploaded directly via MCP (source_type=file fails)
- Source order is chronological only; no reordering via API or UI
- "Convert note to source" is UI-only; no API equivalent
- Always verify London time via python3 before using any date or time
- notebook_rename, source_rename, note create/update/delete all confirmed working
- nlm login may be required at the start of each Claude Desktop session
  If authentication errors occur: run nlm login in terminal, then call
  notebooklm-mcp:refresh_auth before retrying

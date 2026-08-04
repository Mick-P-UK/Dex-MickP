---
name: md-to-docx
description: Document conversion for Mick's system. Two entry points - (1) markdown to a formatted Word document (.docx), optionally with a matching PDF, with real Word structure (heading styles, native tables, embedded images, lists, hyperlinks, code blocks), the mandatory left-aligned provenance footer and an ASCII check; and (2) standalone Word to PDF for any .docx that did not come from markdown, single file or whole folder, with PDF bookmarks built from the Word headings. Use this skill whenever Mick says "make a Word document from this MD", "convert this markdown to Word", "turn the report into a docx", "create a Word version", "docx of this note", "convert this Word doc to PDF", "PDF this document", "make a PDF of the newsletter", "save these as PDFs", or asks for a Word or PDF copy of any vault or project document - including Ron research reports, the Freedom Blueprint newsletter, SOPs and meeting notes.
---

# MD to DOCX (and DOCX to PDF)

Document conversion for Mick's system, in one skill with two entry points:

| Script | Converts | Use when |
|--------|----------|----------|
| `md_to_docx.py` | markdown -> .docx (+ optional .pdf) | The source is a markdown file - Ron research reports, SOPs, vault notes. |
| `docx_to_pdf.py` | .docx -> .pdf (single or batch) | The .docx did NOT come from markdown - the newsletter, the year-end accountant pack, webinar user guides, anything hand-edited in Word. |

`docx_to_pdf.py` is also the SHARED PDF engine: `md_to_docx.py --pdf` calls
straight into it, so there is exactly one Word COM implementation to maintain
and no risk of the two drifting apart.

Built 2026-08-04 out of the HOC (Hochschild Mining) research report conversion,
where the one-off script was good enough to be worth keeping. The DOCX-to-PDF
half was added the same evening after a vault-wide search found NO existing
implementation anywhere - despite the Freedom Blueprint newsletter SOP (Phase 5)
calling for exactly that step since July, which meant it was being improvised
from scratch every month.

## When to use

- Any request like: "make a Word document from this MD", "convert this markdown
  to Word", "turn the report into a docx", "create a Word version", "I need a
  docx of this note", "give me that as a Word file (and a PDF)".
- Ron research reports coming out of the ShareScope + NotebookLM pipeline
  (SOP #1) - these need a DOCX for the webinar / Radar pack.
- Quarterly production updates (SOP #6), which specify vault markdown + DOCX +
  PDF as standard output.
- Any SOP, meeting note or draft that needs to leave the vault as a document.
- **DOCX to PDF (entry point 2):** "convert this Word doc to PDF", "PDF this
  document", "make a PDF of the newsletter", "save these as PDFs", "PDF
  everything in that folder". Covers the Freedom Blueprint newsletter SOP
  Phase 5 step, the year-end accountant pack, and webinar user guides.

Do NOT use `md_to_docx.py` to BUILD the Freedom Blueprint newsletter - that has
its own templated DOCX workflow in the diy-newsletter skill and SOP #2. That
half of the skill converts existing markdown; it does not lay out a designed
publication. `docx_to_pdf.py`, on the other hand, IS the right tool for the
newsletter's final PDF step.

## What it does

1. Reads the markdown and runs an ASCII pass. Typographic characters (em dash,
   en dash, curly quotes, ellipsis, non-breaking space, zero-width space, BOM)
   are converted to their ASCII equivalents automatically. The pound and cent
   signs are LEFT ALONE - Mick's standing decision that they are legitimate
   content, matching the REVIEW_IGNORE list in non-ascii-sweep. Anything else
   non-ASCII is REPORTED with its line number and left untouched, so the source
   gets fixed at source rather than silently mangled.
2. Skips the YAML frontmatter by default (machine metadata, not reader-facing).
   `--frontmatter` renders it as a small grey line at the top instead.
3. Builds the document:
   - `#` to `######` become real Word Heading styles (so the navigation pane and
     any table of contents work), sized 16/14/12/11pt in house dark blue.
   - Pipe tables become native Word tables with gridlines and a shaded header
     row, at 8.5pt so wide tables fit A4 portrait.
   - `![alt](image.png)` images are embedded (not linked), resolved relative to
     the markdown file, centred, 6.6in wide by default.
   - Bullets (two levels), numbered lists, blockquotes and fenced code blocks
     each get appropriate styling. Wrapped source lines are joined back into
     single paragraphs.
   - `[text](url)` becomes a real clickable Word hyperlink.
   - `---` becomes a horizontal rule; `<!-- pagebreak -->` forces a page break.
   - A line starting `**Header:**` (the Ron / Nina report convention) becomes a
     centred document title.
4. Adds the MANDATORY left-aligned provenance footer on every page: full path,
   filename, creation date. `--no-footer` strips it for a going-to-press copy,
   per the standing draft-vs-final footer rule.
5. Optionally exports a PDF via Word COM (`--pdf`).

## Instructions

### Step 1 - Confirm the source and destination

Use the markdown path Mick gives. Default output is the SAME folder with the
SAME basename and a .docx extension - that is almost always what he wants
(the Word copy sits next to the markdown). Only use `-o` if he asks for
somewhere else.

Read the markdown first (Read Before Write rule) - it also tells you whether
the document has images, wide tables or anything needing landscape.

### Step 2 - Convert

```powershell
python "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\md-to-docx\md_to_docx.py" "<path to .md>"
```

With a PDF as well:

```powershell
python "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\md-to-docx\md_to_docx.py" "<path to .md>" --pdf
```

### Step 3 - Check the output before reporting

Do not trust the save message. Confirm:

- The console reported no NON-ASCII CHARACTERS block (if it did, fix the source
  markdown and re-run - do not ship a document with stray Unicode).
- No "image not found" warning.
- Tables and images are present. Check this WITHOUT driving Word:

```powershell
python -c "from docx import Document; d=Document(r'<path to .docx>'); print('paras',len(d.paragraphs),'tables',[(len(t.rows),len(t.columns)) for t in d.tables],'images',sum(1 for r in d.part.rels.values() if 'image' in r.reltype))"
```

**Do NOT verify with `New-Object -ComObject Word.Application` followed by
`$w.Quit()`.** Word registers as a single-instance COM server, so that attaches
to the Word session Mick already has open and then closes it under him - which
is exactly what happened on 2026-08-04 while this skill was being built. If a
page count is genuinely needed, ask Mick to look, or convert to PDF with
`docx_to_pdf.py` (which uses a private Word instance) and count pages there.

### Step 4 - Report

Tell Mick the output path, page count, and anything the converter flagged
(non-ASCII characters, missing images, tables that may need landscape).

## Entry point 2 - standalone DOCX to PDF

For a .docx that did not come from markdown. Single file:

```powershell
python "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\md-to-docx\docx_to_pdf.py" "<path to .docx>"
```

Every .docx in a folder (one Word launch for the whole batch, not one per file):

```powershell
python "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\md-to-docx\docx_to_pdf.py" "<folder>"
```

Files and folders can be mixed in one call, and `--recurse` descends into
subfolders. PDFs land beside each source document unless `-o` names a folder.

**Why this beats the usual improvised one-liner:** it uses Word's
`ExportAsFixedFormat`, not `SaveAs(FileFormat=17)`. That carries the Word
heading structure through as PDF BOOKMARKS, so an eight-page research report or
a six-page newsletter opens with a working navigation pane. It also writes a
tagged (accessible) PDF and keeps the document properties. Verified on the HOC
report: 12 headings became 12 correctly nested bookmarks. It falls back to
`SaveAs` automatically (with a printed NOTE) if a document refuses the rich
export.

### docx_to_pdf.py options

| Flag | Effect |
|------|--------|
| `-o PATH` | Output .pdf path (single file) or a folder for the PDFs. Default: beside each source. |
| `--recurse` | Descend into subfolders when a folder is given. |
| `--skip-existing` | Leave any PDF that already exists untouched - safe to re-run over a big folder. |
| `--no-bookmarks` | Do not build PDF bookmarks from the Word headings. |
| `--screen` | Optimise for on-screen (smaller file) instead of print quality. |

Word lock files (`~$name.docx`) are ignored automatically, and the source
document is opened READ-ONLY so it can never be modified by the conversion.

## md_to_docx.py options

| Flag | Effect |
|------|--------|
| `-o PATH` | Output .docx path. Default: same folder, same basename. |
| `--pdf` | Also export a PDF via Word COM (needs Word installed). |
| `--no-footer` | Omit the provenance footer - use for going-to-press / final copies only. |
| `--frontmatter` | Render the YAML frontmatter as a grey metadata line instead of dropping it. |
| `--landscape` | Landscape A4. Use for documents with very wide tables. |
| `--font NAME` | Body font. Default Calibri. |
| `--size N` | Body font size in points. Default 11. |
| `--table-size N` | Table font size in points. Default 8.5. |
| `--image-width N` | Embedded image width in inches. Default 6.6. |
| `--margin N` | Page margin in inches. Default 0.7. |
| `--no-justify` | Left-align body text instead of justifying it. |
| `--date YYYY.MM.DD` | Creation date shown in the footer. Defaults to today. |

## Notes and gotchas

- **Wide tables:** a 7-column table fits A4 portrait at the default 8.5pt. If a
  table has more columns than that, or very long cell text, use `--landscape`
  or drop `--table-size` to 8.
- **Images must exist on disk** at the path the markdown references, relative to
  the markdown file. A missing image does not fail the run - it inserts a
  visible `[image not found: ...]` marker and prints a warning, so it can never
  pass unnoticed.
- **PDF export needs Word.** Both entry points drive Word via COM. If Word is
  busy with a modal dialog the export can hang - close any open Word dialogs
  first. If pywin32 is missing the DOCX still saves and only the PDF is skipped.
- **Your own Word session is safe.** The engine uses `DispatchEx`, which starts
  a PRIVATE Word instance, rather than `Dispatch`, which would attach to the
  Word Mick already has open and then close it - with alerts suppressed, that
  could discard unsaved work. Never change this to `Dispatch`.
- **A .docx open in Word** can still be converted (it is opened read-only), but
  close it if anything behaves oddly.
- **Batch runs** open Word once and convert everything through that single
  instance. Do not loop the script per file - it is far slower and leaves more
  chances for a stranded Word process.
- **Overwriting:** if the target .docx already exists the script prints a NOTE
  and overwrites. Check with Mick first if the existing file might be a version
  he has edited by hand (version-bump-on-handback rule).
- **Not a newsletter tool.** See SOP #2 / diy-newsletter for that.

## Example

```
Mick: "Create a Word document from the HOC financial analysis MD and drop it
       in the same folder."

Step 1: source =
  ...\2026.08.05 - IC.Webnr\HOC - 2026.08.04 - Micks Radar\
       2026.08.04 - HOC - Hochschild Mining - AI - Financial Analysis_v2.md
  output defaults to the same folder and basename, .docx

Step 2: python md_to_docx.py "<that path>"

Step 3: console clean (no non-ASCII, no missing images); Word COM reports
  8 pages, 3,630 words; 2 tables (10x7 forecast, 28x5 calculations appendix);
  the 12-month ShareScope chart embedded in Technical Analysis.

Step 4: report path, page count, and that the frontmatter was omitted.
```

## Status

- **Version:** 1.1
- **Status:** Production ready
- **Created:** 2026-08-04 (v1.0 markdown to DOCX; v1.1 the same evening added
  the standalone DOCX to PDF entry point and made it the shared PDF engine)
- **Scripts:** `md_to_docx.py` and `docx_to_pdf.py` (both in this skill folder,
  both pure ASCII). `md_to_docx.py` needs python-docx; `docx_to_pdf.py` needs
  pywin32 and Word. `md_to_docx.py --pdf` imports `convert_one()` from
  `docx_to_pdf.py` - keep the two files together.
- **Dual-write:** vault (`skills/md-to-docx/`) + user-level
  (`C:\Users\pavey\.claude\skills\md-to-docx\`) so it loads in both
  claude.ai / Desktop / Cowork (vault) and C:\Vaults-rooted Claude Code
  (user-level). Cowork mirror `/mnt/skills/user/` pending a Desktop session.
- **SOP index:** listed in `C:\Vaults\_SOPs\INDEX.md` (entry #10).
- **First live use:** the HOC Hochschild Mining research report, 2026-08-04.
- **Referenced by:** SOP #2 Freedom Blueprint newsletter, Phase 5 ("Convert
  final DOCX to PDF") - that step now points at `docx_to_pdf.py` instead of
  being improvised each month.

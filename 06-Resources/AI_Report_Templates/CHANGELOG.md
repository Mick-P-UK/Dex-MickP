# AI Report Templates - Changelog

---

## 2026-02-18 | Session: Logo Library & Template Foundation

### Actions

**CREATE** - Template folder structure established
- `AI_Report_Templates/` created as canonical home for AI-generated report assets
- `logos/` subfolder at top level (shared across all report types)
- `Research_Brief/` subfolder for stock research brief template

**CREATE** - Report template: Research Brief
- `Research_Brief/DIY_Investors_Report_Template.docx` - A4 format, 1" margins
- Header: DIY Investors logo (left) + Claude logo (right)
- Footer: Blue border | "Research prepared by Cedric (PAIDA) for Mick Pavey | DIY Investors | Page X of Y"
- Placeholder fields: [COMPANY NAME], [TICKER] | [EXCHANGE] | [SECTOR], [REPORT SUBTITLE/EVENT] | [DATE]
- Source: Derived from corrected Savannah Energy (SAVE.L) Plaza Group webinar report

**CREATE** - Logo library: 22 assets catalogued
- DIY Investors brand (5 files)
- DIY.ai brand (1 file)
- DIY.com website headers (2 files)
- AI Tools & Partners - Claude, NotebookLM, Perplexity, Google AI Studio (9 files)
- Research tools - ShareScope, Stockopedia (2 files)
- People assets - Cedric illustration, Mick photo (2 files)
- UI elements (1 file)

**UPDATE** - Folder structure revised mid-session
- logos/ initially placed inside Research_Brief/ (incorrect)
- Moved up one level to AI_Report_Templates/logos/ on Mick's recommendation
- Rationale: shared assets should not be duplicated per report type
- READMEs updated to reference ../logos/ path

**CREATE** - Documentation
- `README.md` (top level) - folder structure, full logo catalogue with dimensions
- `Research_Brief/README.md` - template usage, placeholder fields, style guide

### Notes
- `DIY-Logo_290 x 58px_for Report Covers_JPG.jpg` and `diy_investors_logo.jpg` are identical (290x58px) - consider removing one
- Three large NotebookLM banner PNGs (3176x800) are high-res; likely for web/slide use rather than docx headers

---

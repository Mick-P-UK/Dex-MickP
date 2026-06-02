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

## 2026-06-01 | Session: Sector Screen Report Example

### Actions

**CREATE** - New report type: Sector Screen Report
- `Sector_Screen_Report/` subfolder created alongside Research_Brief/
- Purpose: multi-company sector screening / ranking reports (landscape), distinct
  from the single-company portrait Research Brief
- `Sector_Screen_Report/README.md` - structure, house style, methodology and build
  notes documented for reproducibility

**PENDING (Mick to action)** - Worked example .docx
- `Sector_Screen_Report/PM_Miners_Quarterly_Growth_Consolidated.docx` to be saved
  into the folder by Mick from the chat download
- Reason: no Claude-to-user binary-copy tool exists; write_file is text-only, so
  Cedric cannot place the binary .docx into the vault directly
- File: US Precious Metal Miners (63-stock ShareScope universe) quarterly growth
  report - 5 tables + 3 quadrant charts, 12 pages, Aptos 12pt landscape

### Notes
- New standing style rule recorded this session: Word/.docx documents default to
  Aptos font at 12pt body (headings scaled proportionally) unless specified otherwise
- Worked example demonstrates: SEC-XBRL-plus-web-research turnover methodology,
  de-cumulation of YTD figures, explicit exclusion (never estimate) handling, and
  performance/valuation overlay with embedded matplotlib quadrant charts
- Key analytical finding preserved in the example: sequential turnover growth had
  near-zero correlation with YTD share-price performance (r approx 0.02)

---

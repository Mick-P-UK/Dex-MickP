# SKILL: /batch-process-webinars

**Version**: 1.0
**Created**: 2026.03.06
**Updated**: 2026.03.06
**Author**: Cedric (PAIDA)
**Trigger**: User types `/batch-process-webinars` or asks to batch process a year of IC webinar PDFs

---

## Purpose

Backfill historical Inner Circle webinar data into Notion by processing an entire
year's worth of webinar PDFs in one run. Extracts all "Mick's View" company slides
and populates the Radar Log and My View - AI Research Notes databases.

This skill is for HISTORICAL BACKFILL ONLY. For ongoing monthly processing,
use /process-webinar instead.

Run order: Start with the most recent complete year and work backwards.
Suggested sequence: 2025 -> 2024 -> 2023 -> 2022 -> 2021

---

## Year Folder Paths (Reference)

| Year | Path |
|------|------|
| 2025 | C:\Users\pavey\Documents\0.2 - Areas (n)\02.04 - DIY - I.C.Webinars\02.04.01 - DIY - I.C.Webinars 2025 |
| 2024 | C:\Users\pavey\Documents\0.2 - Areas (n)\02.04 - DIY - I.C.Webinars\00 - I.C.Webinars (2024) |
| 2024 (alt) | C:\Users\pavey\Documents\0.3 - Resources (n)\DIY - I.C.Webinars_2020-2024\0.00 - DIY - I.C.Webinars (2024) - (n) |
| 2023 | C:\Users\pavey\Documents\0.3 - Resources (n)\DIY - I.C.Webinars_2020-2024\DIY - I.C.Webinars 2023 |
| 2022 | C:\Users\pavey\Documents\0.3 - Resources (n)\DIY - I.C.Webinars_2020-2024\00 - I.C.Webinars (2022) |
| 2021 | C:\Users\pavey\Documents\0.3 - Resources (n)\DIY - I.C.Webinars_2020-2024\00 - I.C.Webinars (2021) |

Note for 2024: Two folder locations exist. Use the Areas (n) path as primary.
Check Resources (n) alt path if months are missing from primary.

---

## Step 1 - Confirm Year and Folder

Ask Mick:
> "Which year shall I process? I'll scan [folder path] - does that look right?"

Wait for confirmation before proceeding.

---

## Step 2 - Scan for Month Folders and PDFs

Use Filesystem tools to list all subfolders of the year folder.
Each subfolder whose name starts with YYYY.MM is a webinar month.

For each month folder, search for the canonical PDF using this priority order:

### PDF Search Order (per month folder - search all levels)

1. Root of month folder
2. Any named subfolder in root (e.g. a FINAL_4_Slides folder)
3. Recordings\ subfolder
4. Any named subfolder inside Recordings\

### PDF Selection Criteria

INCLUDE if filename contains:
- Webnr OR Webinar (case-insensitive)
- .pdf extension

EXCLUDE if filename contains any of:
- Reduced (compressed duplicate - always skip in favour of full version)
- _PRF (proof copy)

When multiple PDFs match for the same month, prefer in this order:
1. Filename containing FINAL (case-insensitive)
2. Filename containing Slides
3. Largest file size (use Filesystem:get_file_info to check)

### Scan Script:

```python
import os

year_folder = r"YEAR_FOLDER_PATH"
results = {}

for month_dir in sorted(os.listdir(year_folder)):
    month_path = os.path.join(year_folder, month_dir)
    if not os.path.isdir(month_path):
        continue
    parts = month_dir.split(' ')[0].split('.')
    if len(parts) < 2 or not parts[0].isdigit():
        continue

    found_pdfs = []
    for root, dirs, files in os.walk(month_path):
        for f in files:
            fl = f.lower()
            if not fl.endswith('.pdf'):
                continue
            if 'reduced' in fl or '_prf' in fl:
                continue
            if 'webnr' in fl or 'webinar' in fl or 'slides' in fl:
                found_pdfs.append(os.path.join(root, f))

    results[month_dir] = found_pdfs

for month, pdfs in results.items():
    print(f"\n{month}:")
    if not pdfs:
        print("  *** NO PDF FOUND ***")
    for p in pdfs:
        print(f"  {p}")
```

---

## Step 3 - Present Scan Report to Mick

Before extracting anything, show Mick the scan results:

```
BATCH SCAN REPORT - [YEAR]
===========================
Months found: [N]
PDFs located: [N]
Missing PDFs: [N]

MONTH-BY-MONTH:
[YYYY.MM.DD] [Month folder name]
  PDF: [filename]
  [or]
  *** NO PDF FOUND ***

MISSING MONTHS:
  [List any months with no PDF]

Ready to proceed with extraction? (Phase 1 - no Notion writes yet)
```

Wait for Mick to confirm before proceeding.

---

## Step 4 - Phase 1: Extract All Company Data (No Notion Writes)

For each confirmed PDF, copy to Claude's computer and extract with pdfplumber.

Copy file: use Filesystem:copy_file_user_to_claude for each PDF.

Install pdfplumber if needed: pip install pdfplumber --break-system-packages

### Extraction Script:

```python
import pdfplumber

def extract_webinar_companies(pdf_path, webinar_date):
    companies = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue
            keywords = ["Mick's View", "\u2019s View", "Mick\u2019s View",
                       "LSE:", "AIM:", "SP=", "MCAP", "Radar"]
            if not any(kw in text for kw in keywords):
                continue
            companies.append({
                "page": i + 1,
                "webinar_date": webinar_date,
                "raw_text": text
            })
    return companies
```

### Fields to extract per company slide:

| Field | Source |
|-------|--------|
| Company Name | Text after "Mick's View of" |
| EPIC/Ticker | In brackets e.g. [FRES] or [LSE: ITH] |
| Exchange | Near ticker: AIM, LSE, NYSE, TSX, TSX-V |
| Webinar Date | YYYY.MM.DD prefix of month folder - NEVER from slide text |
| Share Price | SP= or Price= or "at close" |
| MCAP | MCAP= or Market Cap= |
| Commentary | All bullet points on the slide |

DATE ARTEFACT WARNING: Slides sometimes show the wrong month in the closing
price line due to copy/paste errors in the slide template. ALWAYS use the
folder date. Never trust the date from "At close tonight" or similar.

---

## Step 5 - Infer Verdict from Commentary

**Positive** - Actively bullish:
- "strong buy", "adding to position", "excellent progress", "on target",
  "growing revenues", "first gold pour", "included in portfolio", "in portfolio"

**Neutral** - Watching and waiting:
- "watching", "want a pullback", "not adding yet", "monitoring",
  "too early", "headwinds", "wait and see", "keep an eye"

**Negative** - Concerns outweigh:
- "disappointing", "reducing", "sold out", "avoid", "risks increasing",
  "structural problems", "not convinced", "exited"

Default to Neutral when unclear. Flag for Mick to confirm.

---

## Step 6 - Present Phase 1 Preview Report

After extracting all PDFs, present consolidated preview. Do NOT write to Notion yet.

```
PHASE 1 EXTRACTION REPORT - [YEAR]
====================================
Total webinars processed: [N]
Total company appearances: [N]
Unique companies (EPICs): [N]

EXTRACTION RESULTS:
-------------------
[YYYY.MM.DD] - [Webinar Month]
  [EPIC] [Company Name] - [Verdict] - SP: [price] | MCAP: [cap]
  [EPIC] [Company Name] - [Verdict] - SP: [price] | MCAP: [cap]

COMPANIES APPEARING MULTIPLE TIMES:
  [EPIC] [Company Name] - [N] times: [date1], [date2], ...

FLAGGED FOR REVIEW (ambiguous verdict or missing data):
  [EPIC] [date] - [reason]

MISSING MONTHS (no PDF found):
  [month] - skipped

Proceed with Notion writes? (Phase 2)
```

Wait for Mick's approval before any Notion writes.

---

## Step 7 - Phase 2: Write to Notion (After Mick Approves)

Process each company appearance in chronological order.

### 7a - Check / Create Companies Covered Entry

Data Source ID: 2f3b567d-5dd5-4a64-ae9b-a33df0ee53e5

For each unique EPIC:
- Search Companies Covered by EPIC/ticker
- If found: note the page URL
- If NOT found: create stub entry (EPIC as title + company name), note URL
- Flag all new stubs to Mick at end of run

### 7b - Write Radar Log Entry

Data Source ID: 71d4ac5c-5dc0-48de-8831-0e3ed3e9062e

One entry per company per webinar date. Check for existing entry first
(search EPIC + webinar date). If exists: skip. If not: create.

| Notion Field | Value |
|-------------|-------|
| Feature Title | "YYYY.MM.DD - Micks View of [Company Name] [[EPIC]]" |
| Feature Type | "Micks Radar" |
| Date Featured | Webinar date |
| Price At Date | Share price from PDF |
| MCAP At Date | Market cap from PDF |
| Verdict | From Step 5 |
| Summary | Commentary text (max ~200 words) |
| Companies Covered | Link to Companies Covered page |

### 7c - Write My View Entry

Data Source ID: 3a33ca8c-a353-46e0-9787-839c4256bcca

One entry per company per webinar date (historical journal).
This is different from /process-webinar which maintains a single living record.
The batch processor builds a full timeline so Mick can back-test his views
against actual share price performance over time.

Check for existing entry (EPIC + webinar date). If exists: skip. If not: create.

| Notion Field | Value |
|-------------|-------|
| Company | "YYYY.MM.DD - [Company Name]" |
| EPIC | Ticker code |
| Exchange | "LSE:AIM", "LSE:Main", "TSX", "NYSE" etc. |
| Sector | Inferred from business description |
| Status | "Watch List" (default for historical entries) |
| Verdict | From Step 5 |
| My View | Full commentary from slide bullets |
| Notes | "IC Webinar YYYY.MM.DD - SP: [price] - MCAP: [cap]" |
| Date Added | Webinar date |
| Companies Covered Link | Link to Companies Covered page |

---

## Step 8 - Final Report

```
BATCH PROCESS COMPLETE - [YEAR]
================================
Webinars processed: [N]
Company appearances written: [N]
  - Radar Log entries: [N]
  - My View entries: [N]
Companies Covered: [N] existing / [N] new stubs created

NEW STUBS (need review in Companies Covered):
  [EPIC] [Company Name]

SKIPPED (already existed - idempotent):
  [EPIC] [date]

MISSING MONTHS:
  [month] - no PDF found

Links:
  Radar Log:         https://www.notion.so/3a2b2c0a68dc4011b7482fc4fd10ac47
  My View:           https://www.notion.so/3a33ca8ca35346e097878394c4256bcca
  Companies Covered: https://www.notion.so/2f3b567d5dd54a64ae9ba33df0ee53e5
```

---

## Notion Database Reference

| Database | Purpose | Data Source ID |
|----------|---------|---------------|
| Radar Log | One entry per webinar appearance (log) | 71d4ac5c-5dc0-48de-8831-0e3ed3e9062e |
| My View - AI Research Notes | One entry per company per webinar date | 3a33ca8c-a353-46e0-9787-839c4256bcca |
| Companies Covered | Master registry, EPIC as anchor | 2f3b567d-5dd5-4a64-ae9b-a33df0ee53e5 |

---

## Key Differences vs /process-webinar

| | /process-webinar | /batch-process-webinars |
|---|---|---|
| Use case | Monthly ongoing | Historical backfill only |
| Input | Single PDF (auto-finds latest) | Year folder path |
| My View | One living record per company | One entry per company per webinar date |
| Interactive | Confirms before writing | Phase 1 preview then batch write |
| Idempotent | No | Yes - safe to re-run, skips existing entries |

---

## Error Handling

- PDF not readable: log it, skip the month, flag in report
- Company slide ambiguous (no EPIC visible): flag as "TICKER UNKNOWN"
- Image-only PDF (scanned): flag as "IMAGE-ONLY PDF - manual review needed"
- Notion write fails: log error + raw data so Mick can add manually
- Never guess a ticker - if not clearly on the slide, flag it
- Re-runs are safe: existence checks prevent duplicates

---

## Notes on Older Years

2021: Only June has a confirmed PDF. Other months are unlikely to have PDFs.
2022: PDFs exist but slide templates were less standardised. Flag ambiguous entries.
Pre-2022: Treat all extractions as best effort. Flag rather than guess.

---

## Plain ASCII Rule

ALL text written to Notion or vault files must use plain ASCII only.
No smart quotes, em dashes, ellipsis or other typographic characters.
Replace: -- with -, and use plain straight quotes only.

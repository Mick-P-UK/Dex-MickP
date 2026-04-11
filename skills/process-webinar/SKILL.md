# SKILL: /process-webinar

**Version**: 2.0
**Created**: 2026.03.01
**Updated**: 2026.03.05
**Author**: Cedric (PAIDA)
**Trigger**: User types `/process-webinar` or asks to process a webinar PDF / extract Radar stocks

---

## Purpose

Extracts all "Mick's View of..." company slides from an Inner Circle or Plaza Group
webinar PDF and populates BOTH:
1. The **Radar Log** - one entry per webinar appearance (historical log)
2. **My View - AI Research Notes** - Mick's current investment view (living record)

Also checks Companies Covered and creates a stub entry for any company not already present.

---

## Step 1 - Determine Webinar Type

If not already stated by Mick, ask:
> "Is this an Inner Circle or Plaza Group webinar?"

This determines the Feature Type tag used in the Radar Log:
- Inner Circle -> "Micks Radar"
- Plaza Group -> "Plaza Case Study"

---

## Step 2 - Find the PDF

Scan for the PDF using Filesystem tools. Standard path patterns:

Inner Circle 2026:
  C:\Users\pavey\Documents\0.2 - Areas (n)\02.04.01 - I.C.Webinars 2026\

Inner Circle 2025 (batch archive):
  C:\Users\pavey\Documents\0.2 - Areas (n)\02.04 - DIY - I.C.Webinars\02.04.01 - DIY - I.C.Webinars 2025\

Plaza Group:
  C:\Users\pavey\Documents\0.2 - Areas (n)\02.04.02 - Plaza.Webinars 2026\

File pattern: *FINAL_Slides_PDF.pdf or *FINAL_4_Slides_PDF.pdf

"Most recent" = highest YYYY.MM.DD date prefix in the folder name.

Confirm with Mick before proceeding:
> "Found: [filename] dated [date]. Shall I process this one?"

---

## Step 3 - Extract Company Data from PDF

Use pdfplumber to read the PDF text:

```python
import pdfplumber

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if not text:
            continue
        keywords = ["Mick's View", "\u2019s View", "LSE:", "AIM:", "SP=", "MCAP", "Radar"]
        if any(kw in text for kw in keywords):
            print(f'=== PAGE {i+1} ===')
            print(text)
```

Install if needed: pip install pdfplumber --break-system-packages

For each matching slide, extract:

| Field | Source in PDF |
|-------|--------------|
| Company Name | Text after "Mick's View of" on the slide |
| Ticker/EPIC | Usually in brackets e.g. [MTL] or [GDP] or [LSE: ITH] |
| Exchange | Listed near ticker e.g. AIM, LSE Main Market, NYSE, TSX |
| Webinar Date | From folder/filename YYYY.MM.DD prefix - NOT from closing price line |
| Share Price | Look for "SP=" or "Price=" |
| MCAP | Look for "MCAP=" or "Market Cap=" |
| Commentary | All remaining bullet points on the slide |

**DATE ARTEFACT WARNING**: The closing price line sometimes shows the WRONG month
due to a copy/paste error in the slide template. ALWAYS use the webinar date from
the folder name or filename as the authoritative date. Never use the date from the
"At close tonight" line.

---

## Step 4 - Infer Verdict

Derive verdict from commentary tone:

**Positive** - Actively bullish:
- "strong buy", "adding to position", "excellent progress", "on target",
  "growing revenues", "first gold pour expected", "included in portfolio"

**Neutral** - Watching and waiting:
- "watching", "want a pullback", "not adding yet", "monitoring",
  "too early", "headwinds but potential", "wait and see"

**Negative** - Concerns outweigh positives:
- "disappointing", "reducing", "sold out", "avoid", "risks increasing",
  "structural problems", "not convinced"

When in doubt, default to Neutral and flag for Mick to confirm.

---

## Step 5 - Check Companies Covered (NO ORPHAN RECORDS)

For each EPIC, search Companies Covered:
- Data Source ID: 2f3b567d-5dd5-4a64-ae9b-a33df0ee53e5
- Search by EPIC/ticker

If found: note the page URL (https://www.notion.so/[id-without-hyphens])

If NOT found:
1. Create a stub entry in Companies Covered: EPIC as title, company name
2. Note the new page URL
3. Flag to Mick: "Created stub for [EPIC] in Companies Covered - please review"

---

## Step 6 - Create Radar Log Entries

For each company, create a page in the Radar Log:
- Data Source ID: 71d4ac5c-5dc0-48de-8831-0e3ed3e9062e

| Notion Field | Value |
|-------------|-------|
| Feature Title | "YYYY.MM.DD - Micks View of [Company Name] [[Ticker]]" |
| Feature Type | "Micks Radar" or "Plaza Case Study" |
| Date Featured | Webinar date |
| Price At Date | Share price from PDF |
| MCAP At Date | Market cap from PDF |
| Verdict | From Step 4 |
| Summary | Commentary text from PDF (condensed if very long) |
| Companies Covered | Link to Companies Covered page URL from Step 5 |

---

## Step 7 - Create My View Entries

For each company, ALSO create a page in My View - AI Research Notes:
- Data Source ID: 3a33ca8c-a353-46e0-9787-839c4256bcca

See /my-view-writer skill for full field reference.

Quick reference:

| Notion Field | Value |
|-------------|-------|
| Company | "YYYY.MM.DD - Company Name" |
| EPIC | Ticker code |
| Exchange | "LSE:AIM" or "LSE:Main" or "TSX" etc. |
| Sector | Inferred from business description |
| Status | "Watch List" (default for new Radar entries) |
| Verdict | From Step 4 |
| My View | Full investment thesis from slide bullets |
| Notes | "IC Webinar YYYY.MM.DD | SP: XXXp | MCAP: XXXBn | [TA notes] | [catalyst dates]" |
| Date Added | Webinar date |
| Companies Covered Link | Link to Companies Covered page URL from Step 5 |

**Note**: If a My View entry already exists for this EPIC, UPDATE it rather than
creating a duplicate. Check first with notion-search.

---

## Step 8 - Report to Mick

> Processed: [webinar name] - [date]
>
> Companies added to Radar Log and My View:
> - [Company 1] [Ticker] - [Verdict] - SP: [Price] | MCAP: [Cap]
> - [Company 2] [Ticker] - [Verdict] - SP: [Price] | MCAP: [Cap]
>
> Companies Covered: [X] already existed / [Y] new stubs created
>
> Links:
> - Radar Log: https://www.notion.so/3a2b2c0a68dc4011b7482fc4fd10ac47
> - My View: https://www.notion.so/3a33ca8ca35346e097878394c4256bcca

---

## Notion Database Reference

| Database | Purpose | Data Source ID |
|----------|---------|---------------|
| Radar Log | One entry per webinar appearance (log) | 71d4ac5c-5dc0-48de-8831-0e3ed3e9062e |
| My View - AI Research Notes | Mick's current view per stock (living) | 3a33ca8c-a353-46e0-9787-839c4256bcca |
| Companies Covered | Master company registry, EPIC as anchor | 2f3b567d-5dd5-4a64-ae9b-a33df0ee53e5 |

---

## Architecture Notes

- EPIC (ticker) is the anchor that links all databases together
- Companies Covered is the hub - all other databases link back to it
- Radar Log = historical log (one entry per webinar occurrence)
- My View = living record (one entry per company, updated over time)
- Two-way relations appear automatically on each Companies Covered record

---

## Error Handling

- If PDF not found: tell Mick and ask for the path manually
- If company slide is ambiguous: extract what you can and flag for confirmation
- If Notion write fails: report the error and the data so Mick can add manually
- Never guess a ticker - if not clearly stated on the slide, ask Mick
- If My View entry already exists: update it, do not duplicate

---

## Plain ASCII Rule

ALL text written to vault files or Notion fields must use plain ASCII only.
No smart quotes, em dashes, ellipsis characters, or other typographic characters.
See CLAUDE.md section on UTF-8 Rule for full details.

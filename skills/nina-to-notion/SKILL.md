---
name: nina-to-notion
description: >
  Posts a completed Nina financial analysis report to the Notion Research
  Database. Reads the Nina .md report file, generates a structured summary
  (180-200 words, section headings + bullet points), creates a correctly
  titled and tagged page in the Research Database, populates the EPIC
  relation field, and writes the summary to the Summary (item) property.
  Use this skill whenever Mick says "post Nina's report to Notion",
  "log this to Notion", "add to the research database", or when offered
  automatically at the end of a sharescope-nlm-research run.
---

# Skill: nina-to-notion

Posts a Nina financial analysis report to the Notion Research Database.
Auto-offered at the end of every sharescope-nlm-research run.

---

## KEY CONSTANTS (never ask Mick for these)

```
Research Database data source ID : ac552ce5-2ceb-4ffb-a502-7d5da6c67cf8
Companies Covered data source ID  : 2f3b567d-5dd5-4a64-ae9b-a33df0ee53e5
Research Log root                 : C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\06-Resources\Research-Log
Reports folder                    : Research-Log\Research\[TICKER]\
```

---

## STEP 1 -- RESOLVE THE REPORT FILE

If called at the end of a research run, the ticker and company name are
already known. Use them directly.

If called standalone ("post Nina's report to Notion"):
  - Ask Mick: "Which ticker? I will find the latest report automatically."
  - Once ticker confirmed, list: Research-Log\Research\[TICKER]\
  - Select the most recent .md file (highest YYYY.MM.DD prefix).
  - If multiple same-day files (_v2, _v3), use the highest version.

Read the full report file content into memory.

Extract from the filename:
  - Date     : YYYY.MM.DD (first 10 characters of filename)
  - Ticker   : e.g. SRB
  - Company  : e.g. Serabi Gold (from filename segment after TICKER -)

---

## STEP 2 -- LOOK UP THE EPIC RELATION PAGE URL

Search the Companies Covered data source for an entry matching the ticker.
Data source ID: 2f3b567d-5dd5-4a64-ae9b-a33df0ee53e5

Use notion-search with query = "[TICKER] [Company Name]" and
data_source_url = "collection://2f3b567d-5dd5-4a64-ae9b-a33df0ee53e5"

From the results, find the page whose title matches the EPIC ticker exactly.
Note its page URL in the format: https://app.notion.com/p/[page-id]

If no match found:
  DO NOT proceed to create the Research Database page yet.
  The EPIC relation field requires a full Notion page URL -- plain ticker
  strings are rejected by the API. The solution is to create the Companies
  Covered entry first, then use its page URL for the EPIC field.

  Step 2a -- Create the Companies Covered entry:
  Use notion-create-pages with:
    parent.data_source_id : 2f3b567d-5dd5-4a64-ae9b-a33df0ee53e5
    properties:
      "EPIC" : "[TICKER]"          (this is the title field in that database)
      "Company/Source Name" : "[Company Name]"

  Step 2b -- Capture the new page URL from the response.
  It will be in the format: https://app.notion.com/p/[page-id]

  Step 2c -- Use that URL as the EPIC relation value when creating the
  Research Database page in Step 5.

  Tell Mick: "[TICKER] was not in Companies Covered -- I have added it
  automatically before creating the research entry."

---

## STEP 3 -- SELECT TAGS

Always include both of these tags:
  "Nina's Research"
  "Cedric's Analysis"

Then add up to 3 content-appropriate tags from this list based on what the
report covers. Read the report content to decide:

  Period tags    : "Final Results", "Interim Results", "Trading Update",
                   "FY2025", "FY2026", "FY2024", "FY2023",
                   "Interim Results", "interim results"
  Sector tags    : "Gold Miner", "Oil & Gas Exploration/Production",
                   "Metals & Mining", "Basic Materials", "Miner",
                   "Crypto Currency", "fintech", "Energy",
                   "Industrials", "Healthcare", "Pharmaceuticals"
  Geography tags : "Brazil", "China", "USA", "UK"

CRITICAL: The Tags field has a strict fixed list of allowed values. Only
use tags from this list -- the API will reject any tag not on it. If in
doubt, use only the two mandatory tags. Do NOT use:
  "Banking Services", "Software & IT Services", "FY2026 Forecast",
  or any tag not explicitly confirmed in the list above.
If you need a tag that does not exist, flag this to Mick -- the data
source schema must be updated to add it before it can be used.

---

## STEP 4 -- GENERATE THE SUMMARY

Write a summary of the Nina report following these rules:

LENGTH: 180-200 words. This is a firm target range -- do not go under 180
or over 200. Count words before finalising.

FORMAT:
  - Section headings as plain text labels (the Summary (item) field is
    plain text -- bold does not render via the API)
  - Each heading on its own line, NO bullet point on the heading itself
  - Each bullet item begins with the bullet character (U+2022) and a space: "* "
    (Use ASCII asterisk * as the bullet character in the skill -- Notion API
    stores and displays this correctly as a bullet. Do NOT use a hyphen.)
  - One bullet per line
  - No pipe separators (|)
  - No putting everything on a single line

SECTIONS (use these headings, or substitute headings appropriate to the
report type if these do not fit):

  Financial Highlights
  Financial Position
  Operations
  Key Developments

Include specific numbers, percentages and metrics wherever available.
Lead with the most material information under each heading.
End the summary with the Nina recommendation (BUY / HOLD / SELL) as the
final bullet under Key Developments or as a standalone line.

EXAMPLE FORMAT (illustrative only -- numbers are not real):

Financial Highlights
* Revenue $151.2m (FY2025); forecast $243.3m (FY2026, +61% YoY)
* PBT $62.4m (FY2025); forecast $134.0m (FY2026, +115%)
* EPS 68.0c (FY2025); forecast 138.9c (FY2026, +104%)

Financial Position
* Debt-free as of Q1 2026; cash $64.4m (up from $38.8m at year-end)
* FCF $26.4m (FY2025); forecast $66.3m (FY2026)
* Fourth ball mill installation funded from cash -- no dilution risk

Operations
* Record annual production 44,169 oz gold (FY2025)
* Q1 2026 production 12,042 oz (+20% YoY); FY2026 guidance 53,000-57,000 oz
* Processing capacity expanding to 330ktpa at Palito Complex

Key Developments
* M&I Resources +29% to 730,800 oz; Inferred +50% to 653,300 oz
* Coringa GUIA licence expiring Jan 2027 -- key permitting risk
* Recommendation: BUY (stock at estimated 80.7% discount to fair value)

---

## STEP 5 -- CREATE THE NOTION PAGE

Use notion-create-pages with:

  parent.data_source_id : ac552ce5-2ceb-4ffb-a502-7d5da6c67cf8

  properties:
    "Date & Title" : "YYYY.MM.DD - {Company Name}: Nina's Financial Analysis"
    "Tags"         : ["Nina's Research", "Cedric's Analysis", ...selected tags]
    "EPIC"         : ["https://app.notion.com/p/{companies-covered-page-id}"]
    "Summary (item)" : {summary text from Step 4}

TITLE FORMAT RULES (non-negotiable):
  CORRECT : 2026.05.01 - Serabi Gold: Nina's Financial Analysis
  WRONG   : 2026.05.01 - SRB - Serabi Gold - Nina's Financial Analysis
  WRONG   : 2026.05.01 - Serabi Gold - Nina's Financial Analysis
  WRONG   : 2026.05.01 - SRB: Nina's Financial Analysis

  - EPIC ticker code NEVER appears in the title
  - Separator after date is a space-dash-space ( - )
  - Separator after company name is a colon-space (: )
  - Always ends with "Nina's Financial Analysis"

---

## STEP 6 -- CONFIRM

Once the page is created, report back to Mick with:
  - The Notion page URL
  - The title as created
  - Confirmation that EPIC, tags, and summary were all populated
  - A one-line note on the recommendation (e.g. "Nina rates SRB a BUY")

---

## TROUBLESHOOTING

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| EPIC field not accepted | Page URL format wrong | Use full https://app.notion.com/p/[id] format (no dashes in ID) |
| Tags not accepted | Tag text does not exactly match allowed values | Check tags list in Step 3 -- use exact strings |
| Summary truncated | Over 200 words | Trim to 200 words; cut least material bullet first |
| Company not in Companies Covered | New company, no prior entry | Still set EPIC -- Notion auto-creates two-way relation |
| Page created with wrong title | Title format drift | Re-read STEP 5 title rules; never include ticker in title |
| Summary (item) appears on one line | Newlines lost | Each heading and bullet must be separated by \n in the API call |

---

## TITLE FORMAT REMINDER

```
CORRECT  : 2026.05.01 - Serabi Gold: Nina's Financial Analysis
WRONG    : 2026.05.01 - SRB - Serabi Gold - Nina's Financial Analysis
WRONG    : 2026.05.01 - Serabi Gold - Nina's Financial Analysis
```

The EPIC ticker code NEVER appears in the Notion page title.

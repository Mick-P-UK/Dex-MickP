# micks-stocknote Skill v1.0
# Micks-View Write Command
# Created: 2026-03-10 | PRD v2.2 Phase 1

## Purpose

Capture Mick's brain dump about a stock or sector and write it as a
structured Obsidian markdown note to the Micks-View Inbox. This is the
PRIMARY write mechanism for Micks-View. It does NOT query - it only writes.

## Trigger

User says any of:
- "stocknote [TICKER]"
- "micks-stocknote [TICKER]"
- "note on [TICKER]"
- "brain dump [TICKER]"
- Any request to capture Mick's view of a specific stock

## Vault Location

All new notes land in the Inbox for review before filing:
  C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\Micks-View\00-Inbox\

## File Naming Convention

  YYYY-MM-DD-[TICKER]-[slug].md

Example:
  2026-03-10-SLP-quarterly-results.md

## YAML Schema (frozen per PRD v2.2)

```yaml
---
epic: TICKER
ticker: "[[TICKER]]"
company: Company Full Name
date: YYYY-MM-DD
date_created: "YYYY-MM-DD"
date_amended: "YYYY-MM-DD"
source: IC Webinar | Plaza | AI | Brain Dump | Research | News
sp_start: 0.00
mcap: 0
exchanges:
  - AIM
sector: Precious Metals | Mining | Technology | Other
view_current: Watch | Positive | Negative | Shortlist | Stop_Loss
tags:
  - tag1
micks_summary: "200 char max plain-text summary"
micks_edit: false
visibility: private
---
```

## Field Rules

| Field | Rule |
|-------|------|
| epic | Plain uppercase ticker. No brackets. e.g. SLP |
| ticker | Wikilink in quotes. e.g. "[[SLP]]" |
| company | Full company name |
| date | ISO date YYYY-MM-DD - the event/note date (webinar date, news date, etc.) |
| date_created | ISO date YYYY-MM-DD - when the note file was first written. Set once, never change. |
| date_amended | ISO date YYYY-MM-DD - update this whenever the note is edited. |
| source | One of the enum values above |
| sp_start | Share price at time of note. 0.00 if unknown |
| mcap | Market cap in thousands GBP. 0 if unknown |
| exchanges | List of exchange codes |
| sector | One of the enum values |
| view_current | One of: Watch, Positive, Negative, Shortlist, Stop_Loss |
| tags | Multi-value list |
| micks_summary | 200 char MAX. Plain text. No markdown. Mick's verdict in a line |
| micks_edit | false = AI-generated. true = Mick has edited/verified |
| visibility | private (default). members or public for future Portico Plaza |

## Workflow

1. Ask Mick for the TICKER if not provided
2. Ask for brain dump content (or accept dictated voice input)
3. Look up company name if not stated (use web search if needed)
4. Confirm current date using verified date (never mental maths)
5. Populate YAML from Mick's input - mark any unknown fields as 0 or "unknown"
6. Write date_created and date_amended as the actual verified date (ISO YYYY-MM-DD)
   -- Do NOT use Templater syntax {{date:}} -- that only works inside Obsidian
   -- Write the real date directly, e.g. date_created: "2026-03-10"
7. Write file to 00-Inbox using naming convention
8. Confirm to Mick: file written, path shown, next action suggested

## Content Section

Below the YAML frontmatter, write a clean structured note:

```markdown
# [[TICKER]] - Company Full Name

## Mick's View

[Brain dump content - preserve Mick's voice, clean up dictation errors]

## Notes

[Any additional data points, links, context]

## Links

- [[TICKER]]
```

## IMPORTANT Rules

- ALWAYS use verified date from calendar/clock - never calculate dates mentally
- ALWAYS write to 00-Inbox - never directly to 02-Areas
- NEVER overwrite an existing file - if filename exists, append -v2 suffix
- ASCII only in file content - no em dashes (--), no smart quotes, no ellipsis (...)
- micks_summary must be 200 chars MAX - truncate if needed
- micks_edit defaults to false unless Mick explicitly confirms he has reviewed it

## After Writing

- Confirm file path to Mick
- Offer to query related notes (micks-view-query)
- Remind Mick: file is in Inbox, needs filing to 02-Areas\Stocks when reviewed

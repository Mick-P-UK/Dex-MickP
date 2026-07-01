# ShareScope Report Skill

## Trigger Phrases
Use this skill when Mick says any of the following:
- "build a research brief for [TICKER]"
- "make the report for [TICKER] with the chart"
- "stock research brief for [TICKER]"
- "chart + report for [TICKER]"
- "/sharescope-report [TICKER]"

---

## Purpose
Produce a branded DIY Investors Stock Research Brief for a stock, with the
12-month ShareScope chart embedded, from a single ShareScope session. Pulls the
chart (and the financial CSVs) via the session runner, then drops the chart into
the branded Word template.

Status: v0.1 (proven end to end for the chart embed 2026.07.01 on HDD).
Next iteration: fold the six financial CSVs in as summary tables (see below).

---

## Inputs and key paths
- Template:  C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\06-Resources\AI_Report_Templates\Research_Brief\DIY_Investors_Report_Template.docx
- Data:      produced by the session runner into
             04-Projects\2026.04.04-ShareScope-Automation\downloads\{TICKER}\
             (chart PNG: {date}_{TICKER}_chart_12m.png ; plus 6 financial CSVs)
- Output:    a dated .docx named "YYYY.MM.DD - {TICKER} - Stock Research Brief.docx"

Template placeholder fields (fill these):
  [COMPANY NAME] | [TICKER] | [EXCHANGE] | [SECTOR] |
  [REPORT SUBTITLE/EVENT] | [DATE] | [SECTION HEADING] | [Report content goes here]
Template geometry: A4, 1in margins, ~6.27in usable width. Embed the chart at
about 5.6in wide, centred, with a "Source: ShareScope..." caption beneath.

---

## Step 1 -- Get the data (ONE ShareScope session)
Use the session runner - do NOT open ShareScope separately for the chart and the
financials. From the automation project:

    python sharescope_session.py --chart --financials {TICKER}

Or import it (preferred when the report is built by the agent):

    from sharescope_session import run_sharescope_session
    results = run_sharescope_session(["{TICKER}"], do_financials=True, do_chart=True)
    chart = results["tickers"]["{TICKER}"]["chart"]
    csvs  = results["tickers"]["{TICKER}"]["financials"]

Confirm the chart PNG exists before building the report.

---

## Step 2 -- Build the report (python-docx)
Open the branded template, fill the placeholder fields for the stock, insert the
chart, save with the dated filename. python-docx opens the existing template and
preserves its branding (logos, header/footer, styles). Reference build:

    from docx import Document
    from docx.shared import Inches, Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = Document(TEMPLATE)
    # replace placeholder text in paragraphs, preserving the first run's format
    # then: pic = d.add_paragraph(); pic.alignment = CENTER
    #       pic.add_run().add_picture(CHART, width=Inches(5.6))
    #       add an italic 9pt "Source: ShareScope..." caption
    d.save(OUT)

Verify by converting to PDF and eyeballing page 1 before handing it over.

---

## Step 3 -- Financials tables (NEXT ITERATION - not yet built)
Read the six CSVs from the downloads folder and add summary tables (headline
income, balance-sheet, ratios, dividends, forecasts) beneath the chart. Keep
tables narrow enough for the 6.27in width. Skip tabs that are empty for the
stock (small caps often have empty dividends/forecasts - genuine, not an error).

---

## Notes / known items
- The ShareScope chart PNG carries ShareScope's own day-change overlay
  (e.g. "-4.23%"). Toggle it off in ShareScope's chart display before capture
  if a cleaner chart is wanted.
- Template footer currently shows "Page 1 of 3" (hardcoded/stale) - fix in the
  template itself.

---

## Skill Metadata

Version:  0.1 (chart embed proven 2026.07.01; financials tables pending)
Created:  2026.07.01
Author:   Cedric (PAIDA)
Depends:  sharescope_session.py (session runner) + python-docx + the template
Vault:    C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\sharescope-report\SKILL.md
Mirror:   /mnt/skills/user/sharescope-report/SKILL.md  (PENDING dual-write)
Build:    C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.07.01-ShareScope-Chart-Export\

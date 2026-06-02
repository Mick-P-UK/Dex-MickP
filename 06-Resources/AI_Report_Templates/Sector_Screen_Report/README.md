# Sector Screen Report Template

Multi-company sector screening / ranking report prepared by Cedric (PAIDA).

Used for: sector-wide quantitative screens that rank a universe of stocks on one
or more metrics (turnover growth, cash flow growth, performance, valuation), with
cross-references, data-quality notes and quadrant charts. Distinct from the
single-company Research_Brief template (which is a portrait, one-stock brief).

---

## Worked Example

| File | Description |
|------|-------------|
| `PM_Miners_Quarterly_Growth_Consolidated.docx` | Reference example: US Precious Metal Miners (63-stock ShareScope universe), quarterly growth + performance + valuation overlay. Save this file into THIS folder from the chat download. |

NOTE: Cedric cannot copy a binary .docx from its container into the vault
directly (no Claude-to-user binary copy tool exists; write_file is text only).
The .docx must be dropped into this folder by Mick from the presented download.

---

## What this report type contains (structure of the worked example)

1. Title block - report name, subtitle, universe / period / date line.
2. Introduction - what the report covers, plus a method note.
3. Table 1 - Top 10 by a primary screen metric (here: operating cash flow growth).
4. Table 2 - Top 10 by a second screen metric (here: sequential QoQ turnover),
   with a cross-reference column flagging overlap with Table 1.
5. Table 3 - Full ranking of all qualifying names.
6. Coverage and Data Quality - honest account of what could and could not be
   computed, and why (exclusions stated explicitly, never estimated).
7. Cross-reference section - names appearing in more than one screen.
8. Overlay tables (4 and 5) - performance and valuation layered onto the ranking.
9. Overlay interpretation - what the overlay shows (here: turnover growth had
   near-zero correlation with YTD price; r approx 0.02).
10. Quadrant charts (3) - embedded PNG scatter charts in house style.
11. Overall Summary.
12. Risk Warning + DYOR sign-off.

---

## House Style (current standard)

| Element | Style |
|---------|-------|
| Default body font | Aptos, 12pt (standing rule as of 2026-06-01) |
| Headings | Aptos, scaled proportionally (H1 ~16pt bold, H2 ~13pt bold) |
| Page | Landscape, A4/Letter, ~0.75in top/bottom, 1in left/right margins |
| Navy (titles, H1, sign-off) | hex 1F3864 |
| Blue (H2, subtitle, header rule) | hex 2E75B6 |
| Table header fill | 1F3864, white text |
| Zebra row shading | EEF3F9 |
| Overlap-highlight row shading | FCE9D6 |
| Performance positive / negative | green 1F7A3D / red B3261E |
| Chart attractive-quadrant shade | green 70AD47 at 10% alpha |
| Footer | Blue top border, centred: "Cedric, Mick's AI Research Assistant - DATE - Page N" |

Wide tables: keep cell text at a size that fits the landscape width (do NOT
enlarge cell text to 12pt if it forces column wrap). Body prose is 12pt; small-
print caveat notes one point smaller (11pt).

---

## Methodology notes (for reproducibility)

- Sequential QoQ turnover compares each company's latest reported quarter with the
  immediately preceding quarter. Calendar-year filers: Q1 2026 vs Q4 2025. Flag any
  offset fiscal calendars (e.g. Silvercorp Dec-qtr vs Sep-qtr; TRX Nov vs Aug).
- Foreign filers (40-F / 6-K) often do not tag quarterly turnover in SEC XBRL.
  Approach: pull what is available from SEC XBRL (data.sec.gov; note www.sec.gov
  may rate-limit the container IP - efts.sec.gov works for CIK resolution), then
  gather the rest company-by-company from filings and investor-relations pages.
- De-cumulate year-to-date figures into discrete quarters before comparing.
- State exclusions explicitly; never estimate. Examples handled this way:
  discontinued-operations distortions (SSR Mining Copler sale; Equinox Brazil
  disposal), unpinned prior-quarter lines (Fortuna Q4, B2Gold Q4), revenue-
  recognition changes (Vox, Metalla, Gold Royalty), pre-revenue explorers, and
  M&A (New Gold acquired by Coeur, closed 2026-03-20, so no standalone quarter).
- Verify any single figure that drives a ranking position against the actual filing.

---

## Build approach

- Generated with docx-js (npm "docx") via a Node build script, then validated with
  the docx skill validator and visually QA'd by rendering to PDF/images.
- Charts generated with matplotlib (Agg), saved as 150dpi PNG, embedded via ImageRun
  at ~720px wide in the landscape body.
- Source data: ShareScope Google Sheet (20-min delayed) for prices/valuation;
  parse with a proper CSV reader (MCAP etc. contain quoted commas - naive split
  breaks column alignment). Sheet prices are pence-style: divide by 100 for USD.

---

## Created

2026-06-01 by Cedric (PAIDA) | Source: US Precious Metal Miners quarterly growth
research (63-stock ShareScope universe), built across the prior session.

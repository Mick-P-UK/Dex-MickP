---
title: SOP - Quarterly Production Update
version: 0.9 PROVISIONAL
status: PROVISIONAL - awaiting Mick's review
created: 2026-07-29
owner: Mick (drafted by Cedric)
review_flag: Not yet reviewed or walked through by Mick. Follow with care and treat all [REVIEW] items as unverified until Mick signs off and promotes to v1.0.
---

# SOP - Quarterly Production Update

> PROVISIONAL DRAFT (v0.9) - NOT YET REVIEWED BY MICK.
> This SOP was drafted by Cedric on 2026-07-29 straight after the first live run
> (Greatland Resources, GGP, June 2026 quarterly). It captures that process while
> fresh. It has NOT been reviewed or walked through by Mick. Steps marked [REVIEW]
> are Cedric's generalisations from a single run and may need adjusting. Cedric may
> follow this SOP in the meantime, but must flag [REVIEW] steps as unverified and
> must not treat this as settled practice until Mick promotes it to v1.0 active.

---

## 1. Purpose and when to use

This SOP covers the recurring routine of UPDATING an existing company view when a
new quarterly production / activities report (RNS) is released. It bolts the new
quarter onto the prior quarters, refreshes turnover and profitability using ONLY
real data, compares the updated view against the previous view, and produces a
Ron-authored report plus formatted deliverables.

Use this SOP when:
- A company Mick already follows releases a new quarterly production or activities
  report, and he wants the existing analysis updated.
- Trigger phrases: "process the Q_ production report for [TICKER]", "update
  [TICKER] with the new quarterly", "new quarterly for [company] - update the
  analysis", "add this quarterly and re-run the numbers".

Do NOT use this SOP for a first-time, from-scratch analysis. For that, use SOP #1
(Stock research - ShareScope + NotebookLM + Ron pipeline). This SOP assumes a
NotebookLM notebook and a prior analysis already exist.

---

## 2. Prerequisites

- The company already has a NotebookLM notebook (id known or discoverable via
  `notebooklm list`).
- A prior analysis or snapshot marker exists in the vault to compare against.
- The new quarterly RNS is saved (usually a PDF) in the company's research folder
  on the PC.
- NotebookLM CLI auth is healthy (see gotchas for the auth-failure rule).

---

## 3. Parameters (do NOT hardcode to any one company)

- TICKER and company name.
- Notebook id.
- Company research folder path.
- Commodity set - the company's actual products (do NOT assume gold + copper).
- Financial year-end date (drives which calendar quarter equals which fiscal quarter).
- Revenue-disclosed flag - whether the quarterly discloses revenue (see the branch
  in section 5).

---

## 4. Process

### Phase 1 - Preflight
1. Verify NotebookLM auth. If it fails, go STRAIGHT to the Playwright cookie
   re-export (do not run `notebooklm login` first - see gotchas).
2. Confirm the company's notebook exists (`notebooklm list`).
3. Locate the new quarterly RNS in the company's research folder.
4. Read the prior analysis / snapshot marker to establish the comparison baseline.

### Phase 2 - Ingest the RNS
1. Extract the RNS text. PDF page-rendering (pdftoppm/poppler) is NOT installed in
   this environment - use pymupdf (fitz) or pdfplumber to pull text.
2. Add the RNS to the notebook via the notebooklm-add-content skill.
3. Refresh the notebook title _Updated:YYYY.MM.DD stamp (today's London date).

### Phase 3 - Build the quarter-on-quarter picture
1. Bolt the new quarter onto the prior quarters to show the full-period trend
   (production, sales, AISC / unit cost, realised prices, revenue where given).
2. Note the guidance position (beat / in line / miss) on production and cost.

### Phase 4 - Real commodity and FX data (NO assumptions)
1. Fetch ACTUAL prices for the reporting quarter from documented sources
   (section 6). Never estimate visually off a chart if a real figure can be sourced.
2. Run the realisation cross-check: compare the company's realised prices against
   sourced spot / market averages, converted at the real FX rate, and explain any
   gap (e.g. concentrate sold net of TC/RC and payability deductions).
3. Save the quarter's commodity and FX averages to Cedric's memory for reuse.

### Phase 5 - Turnover and profitability (see the branch in section 5)
1. Turnover per the branch below.
2. Profitability built bottom-up from the disclosed cost lines. Flag gaps; do not
   guess (see section 7).

### Phase 6 - Compare updated view vs prior view
1. Quantify the deltas: prior estimates vs now-real figures (production, prices,
   revenue), and note what genuinely changed (usually: financials now confirmed).
2. Note valuation drift and whether it is a commodity-price story or a company one.

### Phase 7 - Ron authors the report
1. Hand Ron a complete real-data pack (do not make Ron re-derive or assume).
2. Ron writes the structured analysis PLUS a calculations appendix in which every
   derived figure shows formula, inputs, result and per-input source, and reported
   figures are marked "Reported - no calculation" with their source location.
3. Ron signs off as Ron; DYOR risk caveat included.

### Phase 8 - Outputs and conventions
1. Save the markdown report to the vault NotebookLM-Queries folder.
2. Produce a formatted DOCX in the company research folder (house style) with the
   mandatory left-aligned provenance footer.
3. Produce a PDF from the DOCX (Word COM export - no LibreOffice installed).
4. STRICT ASCII only in all vault-bound output.

### Phase 9 - Confirm and report
1. Verify each file exists on disk (path + size) before telling Mick it is done.
2. Give Mick the folder path and file names.

---

## 5. KEY BRANCH - is turnover reported or must it be estimated?

This is the most important conditional and the one most likely to vary by company.

- IF the quarterly DISCLOSES revenue (as GGP's June 2026 activities report did):
  report the actual net revenue as turnover. Do NOT estimate. State clearly that
  turnover is reported, not estimated, and that it supersedes any prior estimate.

- IF the quarterly gives PRODUCTION ONLY (no revenue):
  estimate turnover as production sold x real realised/spot price, using sourced
  prices and real FX. Label every such figure ESTIMATE and show the working.
  Never present an estimate as a reported figure.

[REVIEW] The threshold for "discloses revenue" and how to handle partial
disclosure (e.g. revenue given for one metal only) needs Mick's steer.

---

## 6. Real-data sources (from the first run - extend as needed)

- Gold (USD/oz monthly averages): exchange-rates.org.
- Copper (LME cash, USD/t): Investing News Network; procurementresource.com.
  Note regional CIF quotes run above LME cash (they include premiums) - use LME
  cash as the clean reference.
- FX / AUD-USD (monthly averages): x-rates.com.
- [REVIEW] Add per-commodity source rows as new commodities are encountered
  (silver, tungsten, nickel, etc.). Always prefer a real monthly/quarterly average
  over any visual chart read.

---

## 7. Discipline rules (non-negotiable)

- Real data only. If a figure cannot be sourced, say so and mark it a GAP - never
  fill it with a guess.
- Profitability: EBITDA and EBIT can usually be built from the disclosed cost
  table. Statutory net profit (NPAT) generally CANNOT be finalised from a quarterly
  (corporate overhead, net finance and the accounting tax charge are not disclosed)
  - flag it as pending the audited annual report and give at most a clearly labelled
  indicative pre-tax figure.
- ASCII only in vault output; single hyphens; straight quotes; no unicode.
- Provenance footer on every DOCX/PDF (left-aligned: path, filename, created date).
- Capture the quarter's commodity/FX prices to memory for reuse.

---

## 8. Output naming conventions

- Vault markdown: `NotebookLM-Queries/YYYY.MM.DD - [TICKER] [Company] - [Period] Updated Analysis.md`
- Formatted DOCX: `[research folder]/YYYY.MM.DD - [TICKER] - Ron_[Period] Updated Analysis_Formatted.docx`
- PDF: same as DOCX with `_PDF.pdf` suffix.
- Report author: Ron. Notebook title stamp: _Updated:YYYY.MM.DD.

---

## 9. Gotchas learned on the first run (GGP, 2026-07-29)

- PDF text: poppler/pdftoppm is NOT installed; the Read tool cannot render PDF
  pages. Use pymupdf (fitz) or pdfplumber to extract text.
- `notebooklm source add --wait` does NOT exist in this CLI build; add the source
  then poll `notebooklm source list` for status "ready".
- DOCX to PDF: no LibreOffice/soffice installed; use Microsoft Word via PowerShell
  COM (`Documents.Open` then `SaveAs` with format 17). WINWORD.EXE is present.
- NotebookLM auth failure: go straight to the Playwright cookie re-export; do NOT
  run `notebooklm login` first (it hangs post-rebrand).

---

## 10. Open questions for Mick's review (v0.9 -> v1.0)

1. [REVIEW] Confirm the trigger phrases and that this should stay separate from
   SOP #1 rather than folding into it.
2. [REVIEW] Confirm the turnover branch logic (section 5), including partial
   revenue disclosure.
3. [REVIEW] Confirm profitability depth - how far to push an indicative pre-tax
   figure vs stopping at EBITDA.
4. [REVIEW] Confirm output locations and whether a PDF is always wanted alongside
   the DOCX.
5. [REVIEW] Decide whether/when to build the standalone `quarterly-production-update`
   skill (Mick's decision on 2026-07-29 was: draft this SOP first, build the skill
   later against a live quarterly).
6. [REVIEW] Confirm the memory-capture-of-prices step is wanted every run.

---

## 11. Future skill (deferred - not yet built)

Per Mick's 2026-07-29 decision, a standalone skill `quarterly-production-update`
will be built later (not an extension of sharescope-nlm-research). When built it
must be dual-written (vault + user-level / mirror), honour the provenance and ASCII
rules, carry its own trigger phrases, and update the SOP index entry to point at it.

---

## 12. Changelog

| Version | Date | Change | Reason |
|---------|------|--------|--------|
| 0.9 | 2026-07-29 | Initial provisional draft written straight after the first live run (GGP June 2026 quarterly). Marked PROVISIONAL - awaiting Mick's review. | Capture the process while fresh; Mick busy with webinar prep, to review later. |

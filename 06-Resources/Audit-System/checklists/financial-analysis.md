# Checklist - Financial Analysis audit (ShareScope + Ron pipeline)

*Report-type-specific checks for a full financial analysis report produced by Ron from the six ShareScope CSVs, the 12-month chart, and NotebookLM news/RNS. Use ALONGSIDE the global `rules.md`. Mick edits this file to add checks specific to this report type.*

Owner: Mick (edited jointly with Cedric)
Created: 2026.08.04

---

## Source files (verify inputs against these)

The six ShareScope CSVs for the run, in:
`04-Projects\2026.04.04-ShareScope-Automation\downloads\<TICKER>\*.csv`
- income_statement, balance_sheet, cash_flow, ratios, dividends, forecasts (all dated for the current run).

Confirm the CSVs are dated for THIS run before trusting any figure (R3 stale-source).

---

## Known traps for this report type

### T1 - EPS pence-vs-cents (HIGH RISK)
ShareScope's income-statement CSV labels EPS "(p)" (pence) but for a USD-reporting company the values are actually US cents. The forecasts CSV labels the same series "(c)". Cross-check: attributable profit (USD m) / shares (m) x 100 should match the "EPS reported" value in cents. If the analyst has treated EPS as pence, every P/E and per-share figure is wrong.

### T2 - NAV per share pence-vs-cents (HIGH RISK - the HOC catch)
Forecast NAV in the forecasts CSV is in USD millions. NAV per share = NAV / shares gives a figure in US cents, NOT pence. Price-to-NAV must put price and NAV in the SAME currency (convert the pence price to cents, or the cents NAV to pence). Cross-check against ShareScope's own Price-to-NAV in the ratios CSV. (On HOC, 1.87x was wrong; correct was ~2.5x vs ShareScope 2.4x.)

### T3 - Reporting currency
Many UK-listed miners/producers report in USD. Aggregate CSV figures are USD; some per-share extras (FCF per share, Graham number) can be GBp. Confirm the reporting currency and that USD/GBP conversions use a single, stated FX rate.

### T4 - Net debt/cash basis mismatch
ShareScope "net borrowing" often INCLUDES leases and differs from the company's own reported net debt/cash. A few-million gap is a basis difference, not an error - but the analyst should flag which basis is used. Check the swing arithmetic uses a consistent basis at both ends.

### T5 - Attributable vs consolidated (JV producers)
For companies with less-than-100%-owned mines (JVs), production quoted "by mine" may be on a 100% basis while the group total is attributable. The sum of the mines can legitimately exceed the attributable total. Do not treat the difference as an arithmetic error - but check any revenue proxy uses the right basis.

---

## Calculation checks (recompute each)

- **Margins:** gross, operating, PBT margins = the profit line / turnover x 100. Cross-check against the ratios CSV where it states the same margin.
- **Growth rates:** YoY and forecast growth = (new - old) / old x 100. Confirm the old/new values are the right periods (watch H1 vs full-year columns).
- **Variances:** (your forecast - consensus) / consensus x 100. Confirm sign and base.
- **Per-share scaling:** an EPS scaled by a PBT ratio must use the same PBT basis (normalised vs reported) at both ends.
- **P/E:** price and EPS in the SAME currency (see T1). Forward vs trailing uses the right EPS.
- **EV/EBITDA:** EV = market cap +/- net debt/cash (subtract net cash, add net debt), in one currency; / EBITDA. Cross-check the ratios CSV.
- **Dividend yield:** dividend / price, same currency (both usually pence). Dividend cover = EPS / DPS in consistent units.
- **Dividend total:** sum the interim + final for the year; confirm against the forecasts CSV growth figure.
- **Net-cash / net-debt swing:** end value - start value, consistent basis (see T4).
- **Effective tax rate:** tax / pre-tax profit x 100; cross-check ratios CSV.
- **Production vs guidance (if an operational RNS is used):** H1 actual / guidance midpoint; implied H2 = midpoint - H1.

---

## Consistency checks

- Every derived body figure has an appendix Calc ID (R5). The HOC first run had the effective tax rate quoted without an ID - assign one.
- Any corrected calc is fixed in ALL places it is quoted (body table, prose, appendix, summary).
- The Full Year Forecast Table figures match the appendix and the prose.

## Changelog

| Date | Change |
|------|--------|
| 2026.08.04 | Initial checklist seeded from the HOC financial-analysis audit. Traps T1-T5 and the calculation/consistency checks captured. |

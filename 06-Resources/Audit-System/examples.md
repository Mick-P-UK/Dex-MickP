# Ava the Auditor - Worked Examples

*Curated worked audits, one strong example per report type, to calibrate Ava on what a good audit and a real catch look like. Keep this file CURATED, not a dump - one or two high-quality examples per report type beats many mediocre ones (and it is read on every run, so it costs context). When a real error slips through in future, add a concise entry here so Ava learns the pattern.*

Owner: Mick (edited jointly with Cedric)
Created: 2026.08.04

---

## Example 1 - Financial Analysis: Hochschild Mining (HOC), 4 Aug 2026

**Context:** Ron produced a full financial analysis of HOC (a USD-reporting, LSE-listed gold/silver producer) with a 24-line calculations appendix. Ava audited all calculations against the six ShareScope CSVs before issue.

**Result:** 26 calculations present; 24 correct; 1 material error; 1 minor; 1 traceability gap.

**The material catch (C26 - Price-to-forward-NAV):**
- Ron wrote: `NAV per share = 1248.2 / 514.5 = 242.6p; 453.5 / 242.6 = 1.87x`.
- The trap: forecast NAV of 1,248.2 is in USD millions (balance-sheet basis). So NAV per share = 1248.2 / 514.5 = 2.426 USD = **242.6 US cents**, NOT 242.6 pence. Ron then divided a pence share price (453.5p) by a US-cent NAV as if both were pence.
- Correct: convert to one currency. 453.5p x 1.35 = 612.2c; 612.2 / 242.6 = **2.52x**. Or NAV 242.6c / 1.35 = 179.7p; 453.5 / 179.7 = 2.52x.
- Independent corroboration: ShareScope's own Price-to-NAV for 2026 (ratios CSV) = 2.4x - close to 2.52x, and far from 1.87x. The error made the shares look a third cheaper against NAV than they are.
- Note the tell: another calc in the SAME report (C23, EV/EBITDA) DID convert GBP/USD for the same share price, but C26 did not. An internal FX inconsistency between two calcs is a red flag worth chasing.

**The minor (C27 - OCF estimate):** 0.8297 x 922.8 = 765.6, so "~766", not the "~760" stated. Flagged as a rounding-direction nit; not material (it was an explicit estimate).

**The traceability gap (C5):** the effective tax rate of 33.6% (125.4 / 372.8) was quoted in the body with no appendix Calc ID. Ava flagged it; an ID was added.

**Lesson captured (now in the checklist as trap T2):** for USD-reporting UK stocks, NAV per share and EPS derived from USD aggregates come out in US cents - always reconcile currency before forming a price multiple, and cross-check against ShareScope's own stated ratio.

---

## (Add further examples below as new report types are audited or new error patterns are found.)

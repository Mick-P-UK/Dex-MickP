# J-item manifest - Ditty Box Ltd accountant pack

Baseline as at YE 30.11.2025 (pack built 2026.07.26). J01-J23 inherited from
the YE 30.11.2024 pack; J24-J25 added at Mick's request in 2026.

**This file is a guide, not the authority.** The prior year's
`For sending 2 Jade` folder is the authoritative record - derive the live
manifest from there each year and use this file to interpret it.

## Date convention

`<YE>` = the year end year (e.g. 2025 for YE 30.11.2025).
`<PY>` = the prior year (e.g. 2024).

Filenames usually carry the date the file was *produced*, not the period it
covers. A file named `2026.05.27 - ...` is normal for YE 30.11.2025. Always
match on the period covered.

## Items

| J | Item | Period | Habitual sub-folder | Search hints |
|---|------|--------|---------------------|--------------|
| J01 | NatWest Current Account statement, opening balance | 30.11.`<PY>` | `Nat West - Curr Acc (GBP)` | `NW-Curr-Acc_Statement-0708`, month range spanning 30 Nov `<PY>` |
| J02 | NatWest Current Account statement, closing balance | 30.11.`<YE>` | `Nat West - Curr Acc (GBP)` | same pattern, range spanning 30 Nov `<YE>` |
| J03 | NatWest No 2 Account statement, opening balance | 30.11.`<PY>` | `Nat West - No 2 Acc (GBP)` | `No2-Acc_1208_Statement`, range spanning 30 Nov `<PY>` |
| J04 | NatWest No 2 Account statement, closing balance | 30.11.`<YE>` | `Nat West - No 2 Acc (GBP)` | same pattern, range spanning 30 Nov `<YE>` |
| J05 | NatWest USD Account currency revaluation | 30.11.`<YE>` | `Nat West - $US Account` | `Currency Revaluation_30 Nov <YE>` |
| J06 | USD exchange rate at year end | 30.11.`<YE>` | year folder root | `FX Exchange Rates`, or `USD Exchange Rate` |
| J07 | ii Account transactions spreadsheet, year end | 30.11.`<YE>` | `DB - ii Account` | `Investment SpSheet` or `Transactions_YE ..._FINAL` |
| J08 | ii Account adjustment of valuation of shares held | 30.11.`<YE>` | `DB - ii Account` | `Adj Valn Shares Held`, usually carries the MJ number |
| J08A | ii Account calculations behind that adjustment | 30.11.`<YE>` | `DB - ii Account` | `Calcs for Adj Valn` |
| J09 | ii Account valuation and stocks held | 30.11.`<YE>` | `DB - ii Account` | `Account Valn`, `Account Valuation`, amount in filename |
| J09A | ii Account cash position breakdown | 30.11.`<YE>` | `DB - ii Account` | `Cash Position`, `Cash Balances` |
| J10 | ii Account transactions for the year | year to 30.11.`<YE>` | `DB - ii Account\YE 30.11.<YE>` | `Transactions_Past Year_PDF` |
| J11 | ii Account portfolio at prior year end | 30.11.`<PY>` | `DB - ii Account` | `Account_Portfolio`, `_4 Ref` sub-folders. **Commonly missing.** |
| J12 | Schwab valuation and cash, prior year end | 30.11.`<PY>` | `Schwab ($) Account` | `Valuation_n_Cash`, or the Nov `<PY>` statement jpg |
| J13 | Schwab valuation and cash at year end | 30.11.`<YE>` | `Schwab ($) Account` | `YE Valuation`, `Valuation_n_Cash` |
| J14 | Schwab holdings / transactions for the year | year to 30.11.`<YE>` | `Schwab ($) Account` | `Holdings n Valuation`, `Transactions_Past 12mths` |
| J15 | Schwab year end stock adjustment | 30.11.`<YE>` | `Schwab ($) Account` | `Adj of US Stocks Held`, `YE Stock Adjustment`, MJ number |
| J16 | PayPal Xero bank account before data entry | pre-entry | `D.Box - PayPal` | `Before Data Entry`, `Pre-Upload of CSV` |
| J17 | PayPal transactions for the year | 01.12.`<PY>` to 30.11.`<YE>` | `D.Box - PayPal` | `DB-PayPal_01.12.<PY>-to-30.11.<YE>_PDF` |
| J18 | PayPal balance at year end | 30.11.`<YE>` | `D.Box - PayPal` | `YE Balance`, amount in filename |
| J19 | Halifax CC-1136 start of year balance | 01.12.`<PY>` | `Halifax CC - 1136` | `Start of Yr Bal`. **Commonly missing - a screenshot Mick takes.** |
| J20 | Halifax CC-1136 end of year balance | 30.11.`<YE>` | `Halifax CC - 1136` | `End of Yr Bal`. **Commonly missing - a screenshot Mick takes.** |
| J21 | Xero Trial Balance, draft | 30.11.`<YE>` | `Xero Files`, `Mick - YE ... Reconciliation` | `Trial_Balance_<YE>_11_30`. **Mick prints from Xero.** |
| J22 | Xero Profit and Loss with codes, draft | YE `<YE>` | as above | `P_n_L`, `With_Codes`. **Mick prints from Xero.** |
| J23 | Xero Balance Sheet, draft | 30.11.`<YE>` | as above | `Bal_Sheet`, `Bal-Sheet`. **Mick prints from Xero.** |
| J24 | Director's salary - payslip | in-year | `Directors Salary` | `Payslip`, gross/PAYE/net in filename |
| J25 | Director's salary - PAYE payment set up | in-year | `Directors Salary` | `Set up PAYE Paymt` |

## Numbering rules

- Numbers are stable across years. If an item is missing this year, leave its
  number unused rather than renumbering below it.
- Sub-items use a letter suffix (J08A, J09A) for supporting detail that backs
  up the item above it.
- New items go on the end, from J24 upwards.

## Candidates considered and rejected as extras (2026.07.26)

Mick was offered these and declined all but the payslip items. Offer again
each year, since the answer may change:

- Manual Journal PDFs from the `Manual Journals` folder.
- The Amazon per-item purchase schedule from `AZ - Orders`.
- Director's loan account documents from `Dir Loan Account`.

## Known filename defects in prior packs

- YE 30.11.2024: final item numbered `J33`, should have been `J23`.
- YE 30.11.2024: duplicate `J04` with a truncated filename ending `Balance - `.
- YE 30.11.2024: duplicate `J08` and `J09` entries differing only by date.

Do not reproduce these.

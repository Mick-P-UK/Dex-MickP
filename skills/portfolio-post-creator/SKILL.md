# SKILL: portfolio-post-creator
**Version:** 2.3
**Created:** 2026.03.12
**Updated:** 2026.05.30 (v2.3 - blue-line month-boundary rule; portfolio tag rule)
**Prior update:** 2026.05.09 (v2.2 - dividend type accuracy; transactions intro kept clean)
**Location (vault):** C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\portfolio-post-creator\SKILL.md
**Location (mirror):** /mnt/skills/user/portfolio-post-creator/SKILL.md
**Author:** Cedric (PAIDA)

---

## Purpose

Generate fully-formatted HTML post bodies for the four DIY Investors portfolio pages on diy-investors.com. Produces a structured post object ready to hand off to `wordpress-post-publisher`.

This skill handles ALL content creation and calculations. It has no knowledge of WordPress credentials or API calls.

---

## Portfolio Configurations

| Portfolio ID | Display Name | Heading Name | WP Category Slug | WP Category ID | Currency | Benchmark | Benchmark Ticker | Year | Heading Size |
|-------------|-------------|-------------|-----------------|----------------|----------|-----------|-----------------|------|-------------|
| `uk-active-10` | UK Active 10 | Active 10 (UK) | 2026-active-10-uk | 1036 | GBP | All-Share Index | ASX | 1 | 18pt |
| `uk-active-10-yr2` | UK Active 10 (Year 2) | Active 10 (UK) Yr2 | 2026-active-10-uk-yr2 | 1037 | GBP | All-Share Index | ASX | 2 | 14pt |
| `us-active-10` | US Active 10 | Active 10 (US) | 2026-active-10-us | 1038 | USD | SP500 index | SP500 | 1 | 18pt |
| `us-active-10-yr2` | US Active 10 (Year 2) | Active 10 (US) Yr2 | 2026-active-10-us-yr2 | 1039 | USD | SP500 index | SP500 | 2 | 14pt |

---

## Portfolio Start Values (hardcoded - do NOT ask Mick)

All four portfolios started at 10,000 in their respective currencies. Never ask Mick for start values.

| Portfolio ID | Start Value | Currency | Start Date | Notes |
|-------------|-------------|----------|-----------|-------|
| `uk-active-10` | 10,000.00 | GBP | 2026-01-01 | Year 1 baseline |
| `uk-active-10-yr2` | 10,000.00 | GBP | 2025-01-01 | Year 2 baseline (cumulative from Jan 2025) |
| `us-active-10` | 10,000.00 | USD | 2026-01-01 | Year 1 baseline |
| `us-active-10-yr2` | 10,000.00 | USD | 2025-01-01 | Year 2 baseline (cumulative from Jan 2025) |

---

## Post Type Detection

Determine post type from portfolio ID and month number:

| Condition | Post Type |
|-----------|-----------|
| Year 1, Month 1 (January) | `M1_YR1_START` |
| Year 1, Months 2-11 | `MID_YR1` |
| Year 1, Month 12 (December) | `M12_YR1_END` |
| Year 2, Month 1 (January) | `M13_YR2_START` |
| Year 2, Months 2-11 | `MID_YR2` |
| Year 2, Month 12 (December) | `M24_YR2_END` |

---

## Required Inputs

The following inputs are still needed from Mick at session start. Everything else Cedric derives autonomously.

```
Portfolio(s): [uk-active-10 / uk-active-10-yr2 / us-active-10 / us-active-10-yr2]
Portfolio month end date: [YYYY-MM-DD]
Post date (date of publishing): [YYYY-MM-DD]
Post-benchmark commentary (optional): [free text or omit]
```

Do NOT ask Mick for:
- Portfolio start values (hardcoded above)
- Transaction counts or types (read from screenshots)
- Cash balances (read from screenshots)
- Benchmark values (fetched from Yahoo Finance via benchmark-fetcher skill)
- Image filenames (detected from folder listing)

---

## Autonomous Workflow (MANDATORY order)

1. Detect environment (Claude Desktop required - Filesystem MCP must be active)
2. List portfolio folder using Filesystem:list_directory
3. Identify month-end image and transactions image using detection logic in wordpress-image-uploader SKILL.md
4. Copy both images to Claude computer using Filesystem:copy_file_user_to_claude
5. View both images directly to read: portfolio value, individual stock returns, transaction rows, cash balance
6. Fetch benchmark data via benchmark-fetcher skill (Yahoo Finance)
7. Run all calculations in Python (never mental arithmetic)
8. Upload images to WordPress via wordpress-image-uploader skill
9. Build HTML post body
10. Create WordPress draft via wordpress-post-publisher skill

---

## Calculations (ALWAYS Python-verified)

Run all calculations in Python. Never use mental arithmetic. Show working to Mick before generating post.

```python
# YTD percentage (Year 1 posts)
ytd_pct = (current_value - start_of_year_value) / start_of_year_value * 100

# Cumulative percentage (Year 2 posts - from Year 1 start)
cumulative_pct = (current_value - yr1_start_value) / yr1_start_value * 100

# Index percentage (same formula, applied to benchmark values)
index_pct = (current_benchmark - start_benchmark) / start_benchmark * 100

# Outperformance
outperformance = portfolio_pct - index_pct

# Point change (Year 2 posts only)
point_change = current_benchmark - start_benchmark

# Cash as percentage of portfolio (Month 12 and Month 24 only)
cash_pct = cash_balance / portfolio_value * 100
```

Round all percentages to 2 decimal places. Round point changes to 2 decimal places.

---

## Filename Generation

Generate the expected ShareScope screenshot filename for Mick's reference. Use these patterns:

**Character safety rules (no exceptions):**
- Letters, numbers, hyphens, underscores only
- No spaces (use hyphens)
- No em dashes, smart quotes, ampersands, percent signs
- No double underscores (single only)
- Dots only for date prefix (YYYY.MM.DD) and file extension
- Percentage shown as `pc` not `%`

**Patterns by post type:**

```
M1_YR1_START:    YYYY.MM.DD-[Portfolio]_[Value]-[Currency]_Month-End.jpg
MID_YR1:         YYYY.MM.DD-[Portfolio]_[Value]_Up-[X.XX]pc_Month-End.jpg
M12_YR1_END:     YYYY.MM.DD-[Portfolio]_[Value]_Up-[X.XX]pc_Year-End.jpg
M13_YR2_START:   YYYY.MM.DD-[Portfolio]_Yr2_[Value]_Up-[X.XX]pc_since-1st-Jan-[YYYY].jpg
MID_YR2:         YYYY.MM.DD-[Portfolio]_Yr2_[Value]-[Currency]_Up-by-[X.XX]pc.jpg
M24_YR2_END:     YYYY.MM.DD-[Portfolio]-Yr2_End-of-Year_[Value][Currency]_up-by-[X.XX]pc.jpg
```

Transactions screenshot pattern:
```
Year 1: YYYY.MM.DD-[Portfolio]_Transactions_[Month]-[YYYY].jpg
Year 2: YYYY.MM.DD-[Portfolio]_Yr2_Transactions_[Month]-[YYYY].jpg
```

Output both expected filenames to Mick before generating the post.

---

## HTML Post Template

### Heading

Year 1 (18pt):
```html
<h2><span style="font-size: 18pt;"><strong><span style="color: #ff6600;">[Heading Name] - [Dth Month YYYY]</span></strong></span></h2>
```

Year 2 (14pt):
```html
<h2><strong><span style="font-size: 14pt; color: #ff6600;">[Heading Name] - [Dth Month YYYY]</span></strong></h2>
```

Format date as: `31st January 2026` (ordinal suffix: st/nd/rd/th)

### Portico Plaza Notice (all posts)

```
As usual, the trades will be reported to the Portico Plaza members via the Slack system (usually on the same day).
```

### Date Line (varies by post type)

```
M1_YR1_START:  "This is the end of month position for this portfolio."
MID_YR1:       "This is the end of month position for [Dth Month YYYY]."
M12_YR1_END:   "This is the end of month and End of Year position for this portfolio."
M13_YR2_START: "The end of month position, for the [Full Portfolio Name] Portfolio, is shown below:"
MID_YR2:       "The end of month position, for the [Full Portfolio Name] Portfolio, is shown below:"
M24_YR2_END:   "This portfolio is a continuation of the [Year1 Portfolio Name] portfolio, which started on 1st January [YYYY]. The portfolio, as at [Dth Month YYYY], is shown below:"
```

### Main Screenshot

```html
<a href="https://diy-investors.com/wp-content/uploads/[YYYY]/[MM]/[filename]"><img class="alignnone size-full wp-image-XXXXX" src="https://diy-investors.com/wp-content/uploads/[YYYY]/[MM]/[filename]" alt="[alt text]" width="1000" height="500" /></a>
```

Note: wp-image ID and exact dimensions are unknown until uploaded. Use `wp-image-XXXXX` as placeholder and `width="W" height="H"` as temporary values. After upload, the publisher skill MUST replace these with the real media ID and real pixel dimensions from the WordPress media API (`media_details.width` and `media_details.height`). Never leave placeholder dimensions in the final post. Alt text = filename with underscores replaced by spaces, hyphens replaced by spaces.

Upload folder: `[YYYY]/[MM]` where MM is the month the post is published (not the portfolio month end date).

### Continuity Paragraph (M13_YR2_START only - insert after main screenshot, before transactions)

```
This portfolio is a continuation of the [YYYY] Active 10 ([UK/US]) portfolio, which started on 1st January [YYYY].
```

### Transactions Section (when trades occurred)

Year 1 subheading:
```html
<h3><strong><span style="color: #ff6600;">Transactions ([Month Name YYYY])</span></strong></h3>
```

Year 2 subheading:
```html
<h3><span style="color: #ff6600; font-size: 12pt;"><strong>Transactions:</strong></span></h3>
```

Transactions intro line:
```
There were [number written out] transactions during [Month YYYY], as detailed below.
```

Keep the intro line clean. Do NOT add parenthetical detail (e.g. dividend types, company names) after "as detailed below" - that detail belongs in the commentary paragraph, not repeated here. The screenshot that follows shows the full detail anyway.

Transactions screenshot:
```html
<a href="https://diy-investors.com/wp-content/uploads/[YYYY]/[MM]/[filename]"><img class="alignnone size-full wp-image-XXXXX" src="https://diy-investors.com/wp-content/uploads/[YYYY]/[MM]/[filename]" alt="[alt text]" width="950" height="180" /></a>
```

Cash balance line (when provided):
- Standard: `The resulting cash balance, within the portfolio, is [currency symbol][value].`
- Month 12/24 (include percentage): `The cash at the month end was [currency symbol][value] ([X.X]% of the portfolio value).`

### Benchmark Section

**Year 1 posts (M1_YR1_START, MID_YR1, M12_YR1_END):**

```html
The 'Bench Mark' for the portfolio is the [Benchmark Name] ([Ticker]), which started the year at <span style="color: #0000ff;"><strong>[start_value]</strong></span>. [By/At] [Dth Month YYYY], it had increased by [index_pct]% to [current_benchmark]. The Portfolio, which is <strong>up by [portfolio_pct]%</strong> at [Dth Month], is therefore currently outperforming the index by [outperformance]% ([portfolio_pct]% - [index_pct]%)[! if M1 or M12, no ! otherwise]
```

Use "By" for month-end framing, "At" for mid-month. Month 12 uses "finished" instead of "is":
```
The Portfolio, which finished <strong>up by [portfolio_pct]%</strong> at the year end, has beaten the index convincingly. It has out-performed the index by [outperformance]% ([portfolio_pct]% - [index_pct]%)!
```

**Year 2 posts (M13_YR2_START, MID_YR2):**

```html
[As before, ]the 'Bench Mark' for the portfolio is the [Benchmark Name] ([Ticker]), using the start point of <span style="color: #0000ff;"><strong>1st January [YYYY] (i.e. [start_value])</strong></span>. At [Dth Month YYYY], the [Ticker] was up by [point_change] points (+[index_pct]%) from 1st January [YYYY]. This means that the [UK/US] Year 2 portfolio is now out-performing the index by +[outperformance]% (+[portfolio_pct]% - [index_pct]%)
```

Add "As before, " from Month 14 onwards (not Month 13).

**Month 24 (M24_YR2_END):**

```html
The 'Bench Mark' for the portfolio is the [Benchmark Name] ([Ticker]), at the start of [YYYY] <span style="color: #0000ff;"><strong>[i.e. [start_value]].</strong> <span style="color: #000000;">This is</span></span> the benchmark for the progress of the portfolio in its second year.
At the end of [Month YYYY], the index stood at <span style="color: #0000ff;">[current_benchmark]</span>, a rise of <strong>[point_change] points</strong> since 1st Jan [YYYY] (in percentage terms, <span style="color: #0000ff;"><strong>+[index_pct]%</strong></span> over the 24 month period). At the end of the two year life of the portfolio, it had <strong>outperformed the [Ticker] by [outperformance]%</strong> points ([portfolio_pct]% - [index_pct]%).
```

### Post-Benchmark Editorial Commentary

Insert after benchmark section when Mick provides commentary:

```
[Mick's commentary text verbatim]
```

### Disclaimer (boilerplate - identical every post)

```html
<strong>Please Note:</strong> This post is for educational purposes only and is not a recommendation to buy or sell any share (or other investment vehicle). <strong>Do your own research <span style="color: #ff0000;">(DYOR)</span></strong> before buying or selling any share or other investment and make up your own mind accordingly or seek appropriate professional financial advice.
```

### Contact Link (boilerplate - identical every post)

```html
If you have any comments or observations, regarding the above, then please use the <span style="color: #0000ff; font-size: 12pt;"><strong><a style="color: #0000ff;" href="https://diy-investors.com/contact-us-2/" target="_blank" rel="noopener noreferrer">contact us form Here</a></strong></span>.
```

### Sign-off

```html
<span style="color: #3366ff;"><strong>Mick ([Dth Month YYYY])</strong></span>
```

Use the POST DATE (date of publishing) not the portfolio month-end date.

---

## Output Format

Return a structured post object to be handed to `wordpress-post-publisher`:

```json
{
  "portfolio_id": "uk-active-10",
  "title": "Active 10 (UK) - 31st January 2026",
  "html_body": "[full HTML content]",
  "category_slug": "uk-active-10",
  "target_site": "diy-investors-com",
  "expected_main_filename": "2026.01.31-UK-Active-10_10957.84-GBP_Month-End.jpg",
  "expected_transactions_filename": "2026.01.31-UK-Active-10_Transactions_January-2026.jpg",
  "post_date": "2026-02-27",
  "status": "draft"
}
```

---

## Portfolio Images

Delegate entirely to the `wordpress-image-uploader` skill.

Call it with: `portfolio_id`, `year`, `month`, `target_site`.

It returns `main_image` and `transactions_image` objects, each containing `media_id`, `source_url`, `width`, `height`, `alt_text`, and `filename`.

Use these values directly when assembling the HTML img tags. Never use placeholder dimensions.

See `wordpress-image-uploader/SKILL.md` for full implementation details.

---

## Benchmark Data

Delegate entirely to the `benchmark-fetcher` skill.

Call it with: `year`, `month`, `mode: month-end`, `update_spreadsheet: true`.

It returns FTSE and S&P 500 objects containing `year_start`, `month_end_value`, `month_end_date`, and `ytd_pct`. It also updates the Indices DRAFT spreadsheet automatically.

Use these values directly in the calculations and HTML benchmark section.

See `benchmark-fetcher/SKILL.md` for full implementation details.

---

## Mick's Voice & Commentary Guide

This section defines how to write the performance commentary paragraphs. Study these patterns before drafting any post. The goal is to match Mick's natural, conversational-but-informative writing style.

### Core Principles

- Write like a knowledgeable investor talking to a friend, not like a financial report
- Be specific: name individual stocks that are doing well or poorly, don't just say "some stocks"
- Keep it positive but honest - acknowledge laggards without dwelling on them
- Short, punchy sentences work well. Vary sentence length for rhythm.
- Never use: "robust", "impressive gains", "notable", "significant", "it is worth noting"
- Do not use em dashes in post content
- One exclamation mark maximum per post, and only when genuinely merited (strong outperformance)

### Commentary Structure (MID_YR1 posts)

Paragraph 1 - Performance overview:
- State the overall gain/loss position plainly
- Name 2-3 specific outperforming stocks with their approximate % gains
- Name the one laggard (if any) with its approximate % loss
- Keep it factual and observational, not promotional
- MANDATORY: If the transactions screenshot shows dividend payments, these MUST be mentioned in the commentary paragraph as well as appearing in the transactions section. Describe the dividend(s) accurately: read the Note column on EACH dividend row individually - do not assume all dividends in a batch are the same type. Example: "one ordinary and one special dividend" if the notes differ. Example: "two special dividends" only if both Note fields confirm this. Never collapse distinct dividend types into a single description.

Example from Jan 2026 post:
"The portfolio has started well, with three stocks already up by more than 20%. Only one stock (Smiths News) is in negative territory (-9.3%). The overall portfolio is up by 9.57% after one month."

Paragraph 2 - Portfolio value statement:
- State the total portfolio value
- Mention the YTD gain in pounds and percentage
- Brief comment on spread/diversity if noteworthy

Paragraph 3 - Benchmark comparison (use the template from HTML Post Template section):
- Always reference the specific benchmark start value in blue bold
- State what it did during the period
- State the outperformance clearly
- Keep the exact linking phrase: "The Portfolio, which is up by X% at [date], is therefore currently outperforming the index by Y% (X% - Z%)"

### Key Phrases Mick Uses

- "The portfolio has started well..." (Month 1)
- "The portfolio has continued its [strong/steady/solid] start..." (Month 2+)
- "Only one stock ([Name]) is in negative territory ([X]%)"
- "Three/Four stocks are already up by more than [X]%"
- "The overall portfolio is up by X% after [N] months"
- "The 'Bench Mark' for the portfolio is the [Index] ([Ticker]), which started the year at [value]"
- "The Portfolio, which is up by X%, is therefore currently outperforming the index by Y%"
- "Please Note:" (always bold, starts disclaimer)
- "Do your own research (DYOR)" - DYOR always in brackets, bold, orange/red colour
- "If you have any comments or observations, regarding the above, then please use the contact us form Here"
- "Mick ([Dth Month YYYY])" in teal/blue bold for sign-off

### What to Derive From the Portfolio Screenshot

When Mick provides the portfolio screenshot, extract:
- Total portfolio value (from Total row)
- Individual stock holding values and % returns (rightmost column)
- Which stocks are up most (top performers to name in commentary)
- Which stock(s) are negative (to acknowledge honestly)
- Cash balance if visible
- Benchmark comparison value (shown separately or in header annotation)

### Tone Calibration by Month

| Month | Tone |
|-------|------|
| 1 (Jan) | Cautiously optimistic - "started well", "early signs are encouraging" |
| 2-3 | Building confidence if positive - "continued its strong start" |
| 4-6 | Mid-year assessment - more analytical, comment on which stocks driving gains |
| 7-9 | Three-quarter review tone - begin flagging full-year trajectory |
| 10-11 | Late-year tone - "heading into the final months" |
| 12 (Dec) | Year-end summary tone - "finished the year", annual totals, full comparison |

### Reference Examples

The following example post text (January 2026 UK Active 10) is the canonical reference for voice matching. When in doubt, ask: "would Mick write it this way?"

Canonical example (commentary paragraphs only):

```
The portfolio has started well, with three stocks already up by more than 20%. Only one
stock (Smiths News) is in negative territory (-9.3%). The overall portfolio is up by
9.57% after one month.

The 'Bench Mark' for the portfolio is the All-Share Index (ASX), which started the year
at 5350.38. By 31st January, it had increased by 3.01% to 5511.52. The Portfolio, which
is up by 9.57% at 31st January, is therefore currently outperforming the index by 6.56%
(9.57% - 3.01%)!
```

Key observations from this example:
- Three-sentence structure for the performance para: overview, laggard, total
- Exact benchmark start value linked in blue bold in HTML
- Outperformance calculated and stated as a subtraction: (X% - Y%)
- Exclamation mark used here because Month 1 with clear outperformance
- Conversational month reference: "By 31st January" not "By the 31st of January 2026"

---

## Style Rules & Learnings

### 2026.03.12 - Initial rules from example posts
- Heading size: Year 1 = 18pt, Year 2 = 14pt (intentional distinction)
- Exclamation mark on outperformance: Month 1 and Month 12/24 only
- "As before," prefix on benchmark: Year 2 from Month 14 onwards, not Month 13
- Transactions subheading: Year 1 includes month name in brackets, Year 2 uses plain "Transactions:" with colon
- Cash as % of portfolio: Month 12 and Month 24 only, auto-calculated
- Month 13: always include continuity paragraph (confirmed 2026.03.12 - was missing from original examples)
- Do NOT use double underscores in filenames
- Never use the word "robust"
- All percentage calculations Python-verified, never mental arithmetic
- Sign-off uses post date (date of publishing), not portfolio month-end date
- wp-image IDs are placeholders only - Mick updates after upload
- Grammar: "its second year" not "it's second year"

### 2026.03.14 - Always use real image dimensions (standing rule)
- Never use hardcoded placeholder dimensions (e.g. width="1000" height="500") in img tags. WordPress will stretch or blur images that have incorrect dimensions declared. Always fetch the real width and height from the WordPress media API after upload (`media_details.width` and `media_details.height`) and use those exact values in the img tag. This applies to both the main portfolio image and the transactions image.

### 2026.03.14 - No featured image (standing rule)
- Never set a featured image on portfolio posts. The portfolio screenshot is placed directly in the post body HTML. Setting a featured image causes it to display above the post heading (wrong position) and also renders as a blurred duplicate image in the post body. The wordpress-post-publisher skill has been updated accordingly.

### 2026.03.14 - Standing rules from February 2026 batch
- Transactions are month-scoped: ONLY count and describe transactions that occurred within the post's month. The transactions screenshot may show earlier transactions crossed out with a strikethrough - these are siloed to their own month and must NOT be counted or mentioned in the current post. Count only the rows without strikethrough when writing the transaction count.
- Transactions file preference: when multiple transactions files exist for a month (e.g. a mid-month newsletter version and a month-end version), always use the file with the month-end date prefix (YYYY.MM.DD of the last day of the month). The month-end file is the definitive version.

### 2026.04.01 - Dividends must appear in commentary paragraph as well as transactions section (standing rule)
- When the transactions screenshot shows dividend payments (cash account credits with "Dividend" in the description), these must be referenced in BOTH places: (1) the opening commentary paragraph describing portfolio activity for the month, AND (2) the transactions section. It is not sufficient to mention dividends only in the transactions intro. The commentary paragraph is the reader's summary of the month - omitting dividends from it gives an incomplete picture.

### 2026.04.01 - Negative benchmark in outperformance calculation (standing rule)
- When the benchmark figure in the outperformance subtraction is negative, wrap it in square brackets to avoid a confusing minus-minus display. Format: (-2.90% - [-4.63%]) NOT (-2.90% - -4.63%). This applies to the closing outperformance sentence in the benchmark section for both Year 1 and Year 2 posts, whenever the index YTD or cumulative figure is negative. If both figures are negative, only the second (index) figure gets square brackets, e.g. (-1.50% - [-4.63%]). If the portfolio figure is negative but the index is positive, no brackets are needed as there is no minus-minus.

### 2026.05.09 - Portfolio start values are fixed and must never be asked (standing rule)
- All four portfolios started at exactly 10,000 in their respective currencies. This is a permanent known fact. Never ask Mick for start-of-year or start-of-period values. Use the hardcoded values in the Portfolio Start Values table above. Confirmed by Mick on 2026.05.09.

### 2026.05.09 - Transactions are read from screenshots autonomously (standing rule)
- Cedric must copy the transactions screenshot from Mick's PC and view it directly to extract: transaction count, transaction types (purchase/sale/dividend), company names, and the final cash balance (last Balance figure in the screenshot). Do NOT ask Mick for any of this information. The cash balance is the Balance figure in the last row of the screenshot. The transaction count is the number of non-strikethrough rows. Company names for dividends are in the Description column prefixed with "Dividend". All of this is readable from the image - treat it as a mandatory autonomous step.

### 2026.05.09 - Read each dividend row's Note column individually (standing rule)
- When multiple dividend transactions appear in the transactions screenshot, read the Note column on EVERY row separately. Do not assume all dividends in a batch are the same type. Describe them accurately in the commentary paragraph: e.g. "one ordinary and one special dividend" if the notes differ; "two special dividends" only if both Note fields explicitly confirm this. Collapsing distinct dividend types into a single label (e.g. calling both "special dividends" when one is ordinary) is an error. If the Note column is blank for a row, describe it simply as a dividend without specifying type.

### 2026.05.09 - Transactions intro line must be kept clean (standing rule)
- The transactions intro line ends cleanly after "as detailed below." with no parenthetical additions. Do NOT append dividend types, company names, or any other detail after this phrase - that context belongs in the commentary paragraph. The screenshot that follows the intro line shows the full detail. Correct: "There were two transactions during April 2026, as detailed below." Incorrect: "There were two transactions during April 2026, as detailed below. Both were special dividends from Valterra Platinum Ltd."

### 2026.05.30 - Horizontal blue line in transactions screenshot is a month boundary separator (standing rule)
- A horizontal blue line drawn across the transactions screenshot separates the CURRENT month's transactions (above the line) from PRIOR months' transactions (below the line). Only count and describe the rows ABOVE the blue line. Rows below the line belong to earlier months and must be completely ignored, exactly as strikethrough rows are ignored. This rule applies even when no strikethrough rows are present - the blue line alone is sufficient to identify the boundary. The blue line separator is used when Mick has chosen to show a longer run of transaction history in the screenshot rather than filtering to the current month only.

### 2026.05.30 - Portfolio tags: each post must include the portfolio tag (standing rule)
- Every portfolio post must have the correct WordPress tag applied, in addition to the category. The four tag IDs are: UK Active 10 = 513, UK Active 10 (Yr2) = 890, US Active 10 = 512, US Active 10 (Yr2) = 891. Add these via the `tags` field in the WordPress post payload when calling wordpress-post-publisher. The tag slug matches the portfolio name. Never publish a portfolio post without its tag.

---

## Feedback Loop (MANDATORY - run after every monthly batch)

After Mick reviews the four drafts and provides corrections:

1. Classify each correction: ONE-OFF (this month only) or STANDING RULE (every time)
2. For STANDING RULES: add to the Style Rules & Learnings section above with today's date
3. Update both copies of this file:
   - `C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\portfolio-post-creator\SKILL.md`
   - `/mnt/skills/user/portfolio-post-creator/SKILL.md`
4. Confirm updates to Mick

This step is NOT optional. It is Stage 4 of the monthly batch runner.

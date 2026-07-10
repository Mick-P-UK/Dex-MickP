---
title: End-of-Month Portfolio Posting
tags:
  - SOP
type: SOP
status: active
version: 1.1
created: 2026-07-09
owner: Mick
related-skills: portfolio-post-creator, wordpress-image-uploader, benchmark-fetcher, wordpress-post-publisher
---

# SOP - End-of-Month Portfolio Posting

## 1. Purpose

This routine produces the four monthly portfolio update posts for the DIY Investors
website (diy-investors.com). Each run creates FOUR draft posts, one per portfolio:

- UK Active 10 (Year 1)
- UK Active 10 Year 2
- US Active 10 (Year 1)
- US Active 10 Year 2

Every post is a fully formatted HTML article showing the portfolio's month-end
screenshot, any transactions for the month, the cash balance, a benchmark comparison
against the relevant index, Mick's commentary, and the standard disclaimer and sign-off.

All four posts are created as WordPress DRAFTS. They are never published automatically.
Mick reviews each one in wp-admin and publishes manually.

## 2. When to Run It

Run this at the end of each month, AFTER the month-end housekeeping is done:

- The month-end ShareScope portfolio snapshots have been saved to the four portfolio
  folders (the "current holdings" images).
- The transactions screenshots for the month have been saved to the same folders.

If the screenshots are not yet saved, stop and save them first. The routine reads the
portfolio values, the individual stock returns, the transaction rows, and the cash
balance directly off those images, so they must exist before the run starts.

## 3. Environment and Prerequisites

Run this in CLAUDE CODE on Mick's PC (a local session). Claude Code runs with Mick's own
Windows permissions, so it reads the WordPress credentials for the "Poster Pete"
application-password account directly from the single canonical env file at
C:\Users\pavey\.env, reads the portfolio screenshots, and runs the four skills end to end.

Do NOT rely on Cowork or any cloud/remote session for the end-to-end run. Since the
Anthropic update of 7 July 2026, Cowork sessions run remotely on Anthropic servers and can
reach only folders that have been explicitly connected through the desktop app - never the
home-folder root where .env lives. So the credential read, image upload and draft-creation
steps cannot run from Cowork. Cowork can still build the content and calculations, but the
end-to-end job is a Claude Code local task.

On-demand trigger: open Claude Code with access to the vault and say, for example,
"run the end-of-month portfolio posts for [month], all four portfolios, post date [date]".
Cedric reads this SOP and the four skills and runs the whole sequence, finishing with the
four wp-admin draft edit URLs for Mick to review and publish manually. The run also updates
the Indices Monthly Performance DRAFT spreadsheet (step 5 below) - Cedric does this as part
of the routine, so Mick does not need to update it by hand.

Background: for the full account of the 7 July 2026 Cowork cloud migration, why it changed
.env access, the repercussions on other work, and the credential options going forward, see
the reference note at:
06-Resources/2026.07.09 - Architecture Change Note - Cowork Cloud Migration and Credentials.md

Prerequisites checklist:

- Run in Claude Code on Mick's PC (local session, native file access to .env and folders).
- C:\Users\pavey\.env present and readable, containing the Poster Pete WordPress
  credentials (URL, user, application password). Never print, log, or copy these values.
- The four portfolio folders populated with the month-end and transactions screenshots,
  under: C:\Users\pavey\Documents\0.2 - Areas (n)\02 - DIY - Investors\DIY - Portfolios\
- Internet access for Yahoo Finance (benchmark data) and the WordPress REST API.

Portfolio folder paths:

| Portfolio | Folder |
|-----------|--------|
| UK Active 10 | ...\DIY - Portfolios\2026_UK_Active 10 |
| UK Active 10 Yr2 | ...\DIY - Portfolios\2026_UK Active 10_Yr2 |
| US Active 10 | ...\DIY - Portfolios\2026_US_Active 10 |
| US Active 10 Yr2 | ...\DIY - Portfolios\2026_US Active 10_Yr2 |

## 4. The Four Portfolios

| Portfolio ID | Display Name | WP Category (slug / ID) | Portfolio Tag ID | Currency | Benchmark | Year |
|--------------|--------------|-------------------------|------------------|----------|-----------|------|
| uk-active-10 | UK Active 10 | 2026-active-10-uk / 1036 | 513 | GBP | All-Share Index (ASX) | 1 |
| uk-active-10-yr2 | UK Active 10 (Year 2) | 2026-active-10-uk-yr2 / 1037 | 890 | GBP | All-Share Index (ASX) | 2 |
| us-active-10 | US Active 10 | 2026-active-10-us / 1038 | 512 | USD | S&P 500 (SP500) | 1 |
| us-active-10-yr2 | US Active 10 (Year 2) | 2026-active-10-us-yr2 / 1039 | 891 | USD | S&P 500 (SP500) | 2 |

UK portfolios are benchmarked against the FTSE All-Share (Yahoo ticker ^FTAS, referred
to as ASX in the posts). US portfolios are benchmarked against the S&P 500 (Yahoo ticker
^GSPC). Year 1 posts use an 18pt heading; Year 2 posts use a 14pt heading.

## 5. Inputs and Derived Values

### What Mick provides at the start

- Which portfolio(s) to run (usually all four).
- Portfolio month-end date (YYYY-MM-DD).
- Post date, i.e. the date of publishing (YYYY-MM-DD).
- Optional post-benchmark commentary (free text, or omit).

### What the routine derives autonomously (do NOT ask Mick for these)

- Start values: always 10,000 in the portfolio's currency. Every portfolio started at
  exactly 10,000. This is fixed - never ask.
- Transaction count, transaction types, company names, and the closing cash balance:
  read directly off the transactions screenshot.
- Benchmark values: fetched from Yahoo Finance.
- Image filenames: detected by listing the portfolio folder.

## 6. Step-by-Step Sequence

The orchestrator (portfolio-post-creator) runs these steps in this mandatory order for
each portfolio:

1. Confirm the environment is Claude Desktop (Filesystem MCP active).
2. List the portfolio folder and identify the month-end image and the transactions
   image (detection logic sits in the wordpress-image-uploader skill).
3. Copy both images from Mick's PC into Claude's workspace.
4. View both images directly and read off: total portfolio value, individual stock
   returns, the transaction rows, and the closing cash balance.
5. Fetch benchmark data (FTSE All-Share and S&P 500) from Yahoo Finance via the
   benchmark-fetcher skill; this also updates the Indices monthly DRAFT spreadsheet.
6. Run all calculations in Python (see Section 7). Show the working to Mick before
   generating the post.
7. Upload the two images to the WordPress media library via the wordpress-image-uploader
   skill, capturing the real media IDs, source URLs, and pixel dimensions.
8. Assemble the HTML post body in Mick's house style, using the real image URLs and
   dimensions (never placeholders).
9. Create the WordPress DRAFT via the wordpress-post-publisher skill, applying the
   correct category and the portfolio tag.

Reading rules for the transactions screenshot:

- Count only the rows for the CURRENT month. Ignore any struck-through rows and any rows
  below a horizontal blue line - those belong to earlier months.
- The closing cash balance is the Balance figure in the last valid row.
- Read the Note column on each dividend row individually - do not assume every dividend
  in a batch is the same type.

## 7. Key Calculations

All calculations are verified in Python. Never use mental arithmetic. Percentages are
rounded to 2 decimal places.

```
# Year 1 posts - year-to-date
ytd_pct = (current_value - start_of_year_value) / start_of_year_value * 100

# Year 2 posts - cumulative from the Year 1 start (Jan of the prior year)
cumulative_pct = (current_value - yr1_start_value) / yr1_start_value * 100

# Index percentage - same formula applied to the benchmark
index_pct = (current_benchmark - start_benchmark) / start_benchmark * 100

# Outperformance
outperformance = portfolio_pct - index_pct

# Cash as a percentage of the portfolio (Month 12 and Month 24 posts only)
cash_pct = cash_balance / portfolio_value * 100
```

Note: for Year 2 posts the benchmark section also reports the index point change
(current benchmark minus the start benchmark). When the index figure in an
outperformance subtraction is negative, wrap it in square brackets to avoid a confusing
minus-minus display, e.g. (-2.90% - [-4.63%]).

## 8. Safety Rules

- Posts are ALWAYS created as drafts. The publisher hardcodes status = draft. Nothing is
  auto-published.
- Mick reviews each draft via the wp-admin edit URL returned by the publisher, checks the
  preview, and publishes manually when happy.
- No featured image is ever set. The portfolio screenshot is embedded in the post body
  only; a featured image would duplicate and mis-position it.
- Image dimensions always come from the WordPress media API (media_details.width and
  media_details.height). Never declare placeholder dimensions in the img tags.
- Credentials are read fresh from C:\Users\pavey\.env on every run and are never logged,
  cached, or written into any file, changelog, or memory.

## 9. Conventions

- Category and tag: each post gets BOTH its category (see Section 4) and its portfolio
  tag ID. Tag IDs: UK Active 10 = 513, UK Active 10 Yr2 = 890, US Active 10 = 512,
  US Active 10 Yr2 = 891. Never publish a portfolio post without its tag.
- Sign-off date: uses the POST date (the publishing date), not the month-end date.
- Heading date: reflects the portfolio MONTH-END date, formatted with an ordinal suffix,
  e.g. "31st January 2026".
- Post title format: "[Heading Name] - [Dth Month YYYY]", e.g. "Active 10 (UK) - 31st
  January 2026".
- Upload folder on WordPress: YYYY/MM using the month the post is PUBLISHED, not the
  month-end month.
- Filename and character safety: letters, numbers, hyphens and underscores only; no
  spaces, no double underscores, no ampersands or percent signs (use "pc" for percent);
  dots only for the date prefix and the file extension.
- ASCII only in all post content and filenames: no em dashes, en dashes, smart quotes or
  ellipsis characters. Maximum one exclamation mark per post, and only for genuine strong
  outperformance.

## 10. Troubleshooting

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| 401 Unauthorized on publish or upload | Wrong credentials or the Poster Pete application password was revoked | Check C:\Users\pavey\.env; verify the Poster Pete account and its application password in WP Admin > Users |
| Upload rejected / no upload permission | Poster Pete role lacks the upload_files capability | Confirm Poster Pete has upload rights in WP Admin > Users |
| Month-end or transactions image not found | Screenshot missing or named unexpectedly | Check the portfolio folder; confirm the file starts with the month-end date prefix and is not a Newsletter/Webinar/Transactions variant (for the main image) |
| Benchmark values missing or Yahoo returns no data | Yahoo Finance rate-limit or outage | Retry; if it still fails, use the known year-start fallback values and flag to Mick that the figure is unverified before publishing |
| 422 Unprocessable on publish | Malformed payload, usually a category slug that does not exist on the site | Check the category slug in Section 4 matches the target site |
| Dimensions not returned after upload | WordPress accepted the file but returned no media_details | Check the media library, then supply the real dimensions manually so the HTML can be completed |

## 11. Related Skills

- portfolio-post-creator: the orchestrator. Runs the whole sequence, does all content
  creation and calculations, and hands a finished post object to the publisher.
- wordpress-image-uploader: finds the portfolio screenshots on Mick's PC and uploads them
  to the WordPress media library, returning real media IDs, URLs and pixel dimensions.
- benchmark-fetcher: fetches month-end FTSE All-Share and S&P 500 closes from Yahoo
  Finance and updates the Indices monthly performance spreadsheet.
- wordpress-post-publisher: pushes the finished post object to WordPress as a draft via
  the REST API, applying the category and portfolio tag.

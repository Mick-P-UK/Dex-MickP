---
name: yt-weekly-stats (DEPRECATED - v1)
deprecated: true
deprecated_date: 2026.04.11
superseded_by: yt-weekly-stats-v2
reason: >
  v1 used basic tab-separated entry and relied on visual page scraping with no
  duplicate detection. v2 introduces proven JavaScript DOM scrapers embedded in
  the skill, robust duplicate detection before writing, cell-by-cell Name Box
  entry protocol, a Realtime subscriber scraper for accurate totals, and a
  comprehensive error handling table. v2 is significantly more reliable in
  practice.
retained_for: >
  Historical reference and rollback. Contains the original column mapping,
  workflow logic, and gotchas that informed v2 development. Also contains
  Future Enhancements notes (n8n, YouTube Data API v3, delta columns, alerts)
  that feed the GitHub Actions automation project logged in CEDRIC Memory Vault.
---

> [!WARNING]
> DEPRECATED SKILL - Do not use. Superseded by yt-weekly-stats-v2 on 2026.04.11.
> Retained for reference and rollback only. See _deprecated/README.md for policy.

---

# YT Weekly Stats - YouTube Analytics Tracker (v1 - DEPRECATED)

Collects weekly YouTube channel statistics from YouTube Studio and logs them to the DIY Investors tracking spreadsheet.

---

## Resources

- **YouTube Studio Analytics**: https://studio.youtube.com/channel/UCaWdEBBHiV6P0i7X5fDCY0A/analytics/tab-overview/period-default
- **Google Sheet**: https://docs.google.com/spreadsheets/d/1Z4X_-cmhYeRhajxgN0TM6T8OpJSwT9rsQbEDttJTVlc/edit?gid=0#gid=0

---

## Sheet Structure

Row 1 is headers. New data always goes in the next empty row.

| Col | Header                | Value Source              | Notes                          |
|-----|-----------------------|---------------------------|--------------------------------|
| A   | Date                  | Today's date              | Format: YYYY.MM.DD (dots)      |
| B   | Total Views           | Lifetime analytics        | All-time cumulative            |
| C   | Subscribers           | Realtime sidebar          | Current total, not change      |
| D   | New Subs (28d)        | Last 28 days analytics    | Net gain figure (e.g. 20)      |
| E   | Views (28d)           | Last 28 days analytics    | Exact integer                  |
| F   | Watchtime [hrs] (28d) | Last 28 days analytics    | Hours, 1 decimal (e.g. 58.6)   |
| G   | Avge WT/view (28d)    | Calculated                | Minutes per view, 2dp          |
| H   | Views (365d)          | Last 365 days analytics   | Exact integer from headline    |
| I   | Watchtime [hrs] (365d)| Last 365 days analytics   | Hours, 1 decimal (e.g. 3840.0) |
| J   | Subs (365d)           | Last 365 days analytics   | Net subscriber change          |
| K   | Avge WT/view (365d)   | Calculated                | Minutes per view, 2dp          |

---

## Workflow

### Step 1: Navigate to YouTube Studio

```
URL: https://studio.youtube.com/channel/UCaWdEBBHiV6P0i7X5fDCY0A/analytics/tab-overview/period-default
```

Use browser navigation, then wait 3 seconds for the page to load.
Take a screenshot to confirm the analytics page is showing.

### Step 2: Collect 28-day stats

The default period is "Last 28 days". Extract text from the page.

Extract:
- **Views (28d)**: Exact integer from "Views [number]" in stat cards
- **Watch time (28d)**: From "Watch time (hours) [number]" (e.g. 58.6)
- **New Subs (28d)**: From "Subscribers +[number]" - take just the number, drop the +
- **Current Subscribers**: From "[number] Subscribers" in the Realtime sidebar

> **GOTCHA**: The stat cards show rounded values (e.g. "72.4k") but page text contains
> the exact figures in tooltip/aria text. Always use the exact figures.

### Step 3: Collect 365-day stats

Click the period dropdown (top-right of the analytics page) and select "Last 365 days".
Wait 3 seconds, then extract page text.

Extract:
- **Views (365d)**: Exact figure in headline: "Your channel got [X,XXX] views in the last 365 days"
- **Watch time (365d)**: "Watch time (hours) [X,XXX.X]"
- **Subs (365d)**: "Subscribers +[X,XXX]" - net change over the year

### Step 4: Collect Lifetime total views

Click the period dropdown again and select "Lifetime".
Wait 3 seconds, then extract page text.

Extract:
- **Total Views (lifetime)**: From headline: "Your channel has had [XX,XXX] views so far"

> NOTE: Only Total Views is needed from Lifetime. Current subscriber total was
> already captured from the sidebar in Step 2.

### Step 5: Calculate average watch time per view

NEVER use mental arithmetic. Always verify with code:

```python
# Replace with actual figures collected
views_28d = 986
watchtime_28d = 58.6

views_365d = 72353
watchtime_365d = 3840.0

avg_28d = round((watchtime_28d * 60) / views_28d, 2)
avg_365d = round((watchtime_365d * 60) / views_365d, 2)

print(f"Avg WT/view (28d): {avg_28d} min")
print(f"Avg WT/view (365d): {avg_365d} min")
```

### Step 6: Navigate to the Google Sheet

```
URL: https://docs.google.com/spreadsheets/d/1Z4X_-cmhYeRhajxgN0TM6T8OpJSwT9rsQbEDttJTVlc/edit?gid=0#gid=0
```

Wait 2 seconds for load.

### Step 7: Navigate to the next empty row

Use the Name Box (cell reference input, top-left of sheet) to navigate directly:
- Set Name Box value to "A[next_row]" (e.g. A19, A20)
- Press Return to jump to that cell

To find the correct row number: check the screenshot from sheet load to see the last populated row, then add 1.

### Step 8: Type the data row

With the first cell selected, type all values using Tab to move between columns
and Enter to confirm the row:

```
YYYY.MM.DD[Tab][TotalViews][Tab][Subs][Tab][NewSubs28d][Tab][Views28d][Tab][WTHrs28d][Tab][AvgWT28d][Tab][Views365d][Tab][WTHrs365d][Tab][Subs365d][Tab][AvgWT365d][Enter]
```

Example (22 Feb 2026):
```
2026.02.22	85328	2609	20	986	58.6	3.57	72353	3840.0	2426	3.18
```

### Step 9: Verify

Take a screenshot, then zoom into the new row to confirm all 11 columns are correct.

---

## Common Gotchas

| Issue | Detail |
|-------|--------|
| Rounded vs exact figures | YT Studio cards show "72.4k" but page text has exact numbers - always use exact |
| Lifetime period navigation | Use the on-page dropdown - URL manipulation for period-lifetime is unreliable |
| Date format | Must be YYYY.MM.DD with dots, not dashes, to match existing sheet |
| Subs (365d) | Shown as "+2,426" - enter just the integer 2426 (no plus sign) |
| New Subs (28d) | Shown as "+20" - enter just 20 (no plus sign) |
| Watch time units | Already in hours - do not convert |
| Page load timing | Always wait 3s after changing period before extracting text |

---

## Verification Checklist

Before confirming completion:

- [ ] Date in column A matches today in YYYY.MM.DD format
- [ ] Total Views (col B) is higher than previous row (lifetime always grows)
- [ ] Subscribers (col C) is current total (should be >= previous row)
- [ ] All 11 columns populated (A through K)
- [ ] Average WT/view values calculated via code, not mental arithmetic
- [ ] Screenshot taken confirming new row in sheet

---

## Example Completed Row

From 2026.02.22:

```
A: 2026.02.22
B: 85,328    (lifetime total views)
C: 2,609     (current subscribers)
D: 20        (new subs last 28 days)
E: 986       (views last 28 days)
F: 58.6      (watch time hrs last 28 days)
G: 3.57      (avg watch time per view in minutes, 28d)
H: 72,353    (views last 365 days)
I: 3,840.0   (watch time hrs last 365 days)
J: 2,426     (net subscriber gain last 365 days)
K: 3.18      (avg watch time per view in minutes, 365d)
```

---

## Future Enhancements (carried forward to GitHub Actions project)

- **n8n / GitHub Actions automation**: Trigger automatically every Saturday 10am BST
- **YouTube Data API v3**: Replace browser navigation with direct API calls for more reliable extraction
- **Delta column**: Add week-on-week change in total views for trend spotting
- **Alerts**: Flag if views drop more than a set threshold week-on-week

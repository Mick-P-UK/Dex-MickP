---
name: yt-weekly-stats-v2
description: Collects DIY Investors YouTube channel analytics from YouTube Studio and writes a new row to the Google Sheets stats tracker. Use this skill whenever Mick asks to "log YouTube stats", "update the YouTube stats sheet", "record weekly YT stats", "run the YouTube stats tracker", "capture channel analytics", or any request to pull YouTube analytics data and save it to the spreadsheet. Runs weekly (Saturday preferred). Handles duplicate detection automatically and writes all 11 columns in one pass. Requires Claude in Chrome MCP.
---

# YT Weekly Stats v2

Collects YouTube Studio channel analytics and appends one new row to the DIY Investors stats Google Sheet.

## Target spreadsheet
- URL: https://docs.google.com/spreadsheets/d/1Z4X_-cmhYeRhajxgN0TM6T8OpJSwT9rsQbEDttJTVlc/edit?gid=0#gid=0
- Sheet ID: `1Z4X_-cmhYeRhajxgN0TM6T8OpJSwT9rsQbEDttJTVlc`

## Column mapping
| Col | Header                  | Source                                             |
|-----|-------------------------|-----------------------------------------------------|
| A   | Date                    | Today YYYY.MM.DD                                   |
| B   | Total Views             | YT Studio > Lifetime > Views (exact headline)      |
| C   | Subscribers             | YT Studio > Realtime panel > total count           |
| D   | New Subs (28d)          | YT Studio > Last 28 days > Subscribers (delta)     |
| E   | Views (28d)             | YT Studio > Last 28 days > Views (exact headline)  |
| F   | Watchtime [hrs] (28d)   | YT Studio > Last 28 days > Watch time (hours)      |
| G   | Avge WT/view (28d)      | Calculated: (F / E) * 60  [minutes, 2dp]           |
| H   | Views (365d)            | YT Studio > Last 365 days > Views (exact headline) |
| I   | Watchtime [hrs] (365d)  | YT Studio > Last 365 days > Watch time (hours)     |
| J   | Subs (365d)             | YT Studio > Last 365 days > Subscribers (delta)    |
| K   | Avge WT/view (365d)     | Calculated: (I / H) * 60  [minutes, 2dp]           |

**Key rules:**
- Avge WT/view = minutes. Formula: (watchtime_hrs / views) * 60. Round to 2dp.
- Cols D, J = net subscriber change (signed integer, strip '+' for positives).
- Col C = current subscriber total (integer, no prefix). From Realtime panel.
- Watch time stored as hours as-is (e.g. 42.3, 3907.4). Do NOT convert.

---

## Proven JavaScript scraper

Run this after each period switch (wait 4s for data to load first).
It reliably extracts exact values from the DOM leaf nodes with label context.

```javascript
const results = {};
document.querySelectorAll('*').forEach(el => {
  if (el.children.length === 0) {
    const text = el.textContent.trim();
    if (!/^\+?[\d,]+\.?\d*$/.test(text) || text.length < 2) return;
    let parent = el.parentElement;
    let context = '';
    for (let i = 0; i < 6 && parent; i++) {
      context = parent.textContent.trim().replace(/\s+/g, ' ');
      parent = parent.parentElement;
    }
    const ctx = context.toLowerCase();
    if (ctx.includes('watch time') && ctx.includes('hour') && text.includes('.')) {
      results.watchtime = text;                          // e.g. "3,907.4"
    } else if (ctx.includes('subscriber') && text.startsWith('+')) {
      results.subs_delta = text;                         // e.g. "+2,440"
    }
  }
});
JSON.stringify(results)
```

Parse numbers: strip commas. `3,907.4` -> `3907.4`. `+2,440` -> `2440`.

**Headline scraper** (exact Views figures - always reliable):
```javascript
// For 28d: "Your channel got 646 views in the last 28 days"
const m28  = document.body.innerText.match(/got ([\d,]+) views in the last 28/i);
// For 365d: "Your channel got 73,413 views in the last 365 days"
const m365 = document.body.innerText.match(/got ([\d,]+) views in the last 365/i);
// For Lifetime: "Your channel has had 86,577 views so far"
const mLT  = document.body.innerText.match(/had ([\d,]+) views so far/i);
[m28, m365, mLT].map(m => m ? m[1].replace(/,/g,'') : 'not found').join(' | ')
```

**Realtime subscriber total** (Col C - run on any period, panel is always visible):
```javascript
// The Realtime panel shows total subs as a plain number e.g. "2,624"
// It appears as a leaf node with value > 500, distinct from delta values (which have '+')
const candidates = [];
document.querySelectorAll('*').forEach(el => {
  if (el.children.length === 0) {
    const t = el.textContent.trim();
    if (/^\d[\d,]+$/.test(t) && parseInt(t.replace(/,/g,'')) > 500) {
      let p = el.parentElement;
      for (let i = 0; i < 5 && p; i++) {
        if (p.textContent.toLowerCase().includes('subscriber')) {
          candidates.push(t); break;
        }
        p = p.parentElement;
      }
    }
  }
});
[...new Set(candidates)].join(' | ')
```
Cross-check the result against the Realtime panel in the screenshot.

---

## Step-by-step workflow

### STEP 0 - Duplicate check

Navigate to the spreadsheet URL. Run:

```javascript
const sheetId = '1Z4X_-cmhYeRhajxgN0TM6T8OpJSwT9rsQbEDttJTVlc';
fetch(`https://docs.google.com/spreadsheets/d/${sheetId}/gviz/tq?tq=SELECT%20A&gid=0`,
  {credentials: 'include'})
  .then(r => r.text()).then(t => { window._dates = t; });
```

Wait 2s then run:
```javascript
const today = new Date();
const todayStr = today.getFullYear() + '.' +
  String(today.getMonth()+1).padStart(2,'0') + '.' +
  String(today.getDate()).padStart(2,'0');
const dupe = (window._dates||'').includes(todayStr);
const rows = ((window._dates||'').match(/"v":"\d{4}\.\d{2}\.\d{2}"/g)||[]).length;
`Today: ${todayStr} | Duplicate: ${dupe} | Data rows: ${rows}`
```

- Duplicate = true -> **STOP**. Tell Mick entry already exists for today.
- Duplicate = false -> note `rows`. New row number = `rows + 2`.

---

### STEP 1 - Last 28 days

Navigate to:
`https://studio.youtube.com/channel/UCaWdEBBHiV6P0i7X5fDCY0A/analytics/tab-overview/period-default`

Wait 4s. Take a screenshot to confirm metric cards are loaded.

Run headline scraper -> capture `m28` value -> **Col E** (Views 28d).
Run standard scraper -> `results.watchtime` -> **Col F**, `results.subs_delta` (strip '+') -> **Col D**.
Run Realtime subscriber scraper -> **Col C**.

---

### STEP 2 - Last 365 days

Click the period dropdown (top-right of analytics page). Select **Last 365 days**.
Wait 4s. Screenshot to confirm.

Run headline scraper -> capture `m365` value -> **Col H** (Views 365d).
Run standard scraper -> `results.watchtime` -> **Col I**, `results.subs_delta` (strip '+') -> **Col J**.

---

### STEP 3 - Lifetime

Click the period dropdown. Select **Lifetime**.
Wait 4s. Screenshot to confirm.

Run headline scraper -> capture `mLT` value -> **Col B** (Total Views).

---

### STEP 4 - Calculate averages

```python
# Run via bash_tool
E = {views_28d}
F = {watchtime_28d}
H = {views_365d}
I = {watchtime_365d}

G = round((F / E) * 60, 2) if E > 0 else 0
K = round((I / H) * 60, 2) if H > 0 else 0

print(f"G (Avge WT/view 28d):  {G} mins")
print(f"K (Avge WT/view 365d): {K} mins")
```

---

### STEP 5 - Confirm with Mick

Show this table and ask "Shall I write this to the sheet?":

```
  Row {N} ready to write:
  A  Date:                  {YYYY.MM.DD}
  B  Total Views:           {B}
  C  Subscribers:           {C}
  D  New Subs (28d):        {D}
  E  Views (28d):           {E}
  F  Watchtime hrs (28d):   {F}
  G  Avge WT/view (28d):    {G} mins
  H  Views (365d):          {H}
  I  Watchtime hrs (365d):  {I}
  J  Subs (365d):           {J}
  K  Avge WT/view (365d):   {K} mins
```

Wait for explicit confirmation before writing.

---

### STEP 6 - Write to Google Sheet

Navigate to the sheet URL. Wait 3s for it to load.

**CRITICAL: Enter each value separately -- type value, press Tab, type next value, press Tab, etc.**
Do NOT type all values in one `type` call with tab characters -- they will be concatenated into one cell.

1. Click the **Name Box** (top-left cell reference box, shows current cell like "A1").
2. Type `A{N}` (e.g. `A24`), press Enter. Cursor jumps to that cell.
3. Type the Date value. Press Tab (cursor moves to B{N}).
4. Type Total Views. Press Tab (cursor moves to C{N}).
5. Type Subscribers. Press Tab.
6. Type New Subs 28d. Press Tab.
7. Type Views 28d. Press Tab.
8. Type Watchtime hrs 28d. Press Tab.
9. Type Avge WT/view 28d. Press Tab.
10. Type Views 365d. Press Tab.
11. Type Watchtime hrs 365d. Press Tab.
12. Type Subs 365d. Press Tab.
13. Type Avge WT/view 365d. Press Enter (commits the row).
14. Wait 2s. Zoom into the new row to verify all 11 cells are populated and correct.
15. Confirm success to Mick with the row number written.

---

## Error handling

| Situation | Action |
|-----------|--------|
| Analytics page shows error / spinner | Refresh, wait 5s, retry once |
| Headline regex returns 'not found' | Screenshot the page, read value visually |
| Standard scraper returns empty watchtime | Scroll down, wait 2s more, re-run |
| Realtime subscriber ambiguous | Cross-check screenshot of sidebar |
| Sheet write fails / row looks wrong | Screenshot, report to Mick, do not retry blindly |
| Duplicate date found | Stop immediately, do not write |
| Views = 0 for any period | Set Avge WT/view = 0, flag to Mick |

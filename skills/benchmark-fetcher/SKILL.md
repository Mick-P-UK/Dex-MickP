# SKILL: benchmark-fetcher
**Version:** 1.0
**Created:** 2026.03.30
**Location (vault):** C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\benchmark-fetcher\SKILL.md
**Location (mirror):** /mnt/skills/user/benchmark-fetcher/SKILL.md
**Author:** Cedric (PAIDA)

---

## Purpose

Fetch month-end closing values for FTSE All-Share and S&P 500 from Yahoo Finance, and update the Indices Monthly Performance spreadsheet on Mick's PC.

Usable at month-end (last trading day of the month) or mid-month (returns latest available close). Reusable by any skill or ad-hoc request needing benchmark data.

---

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `year` | int | Yes | e.g. `2026` |
| `month` | int | Yes | e.g. `3` for March |
| `mode` | string | No | `month-end` (default) or `mid-month` |
| `update_spreadsheet` | bool | No | `true` (default) - update the indices DRAFT file |

---

## Tickers

| Index | Yahoo Ticker | Portfolio use |
|-------|-------------|---------------|
| FTSE All-Share | `^FTAS` | UK portfolios (ASX) |
| S&P 500 | `^GSPC` | US portfolios (SP500) |

---

## Step 1: Fetch Data from Yahoo Finance

Run in Python via `bash_tool`:

```python
import requests
import datetime
import calendar

def get_month_end_close(ticker, year, month):
    """
    Returns (closing_value, date_string) for the last trading day of the given month.
    Works for any past or current month.
    """
    start = int(datetime.datetime(year, month, 1).timestamp())
    end_month = month + 1 if month < 12 else 1
    end_year = year if month < 12 else year + 1
    end = int(datetime.datetime(end_year, end_month, 1).timestamp())

    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    params = {'interval': '1d', 'period1': start, 'period2': end}
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, params=params, headers=headers, timeout=15)
    data = r.json()['chart']['result'][0]
    closes = [
        (ts, c)
        for ts, c in zip(data['timestamp'], data['indicators']['quote'][0]['close'])
        if c is not None
    ]
    if closes:
        last_ts, last_close = closes[-1]
        return round(last_close, 2), datetime.datetime.fromtimestamp(last_ts).strftime('%Y-%m-%d')
    return None, None


def get_year_start_close(ticker, year):
    """
    Returns the closing value on 31st December of the prior year (= year start baseline).
    """
    return get_month_end_close(ticker, year - 1, 12)


# Fetch both benchmarks
ftse_value, ftse_date = get_month_end_close('^FTAS', year, month)
sp500_value, sp500_date = get_month_end_close('^GSPC', year, month)

ftse_start, _ = get_year_start_close('^FTAS', year)
sp500_start, _ = get_year_start_close('^GSPC', year)

# Calculate YTD percentages
ftse_ytd = round((ftse_value - ftse_start) / ftse_start * 100, 2)
sp500_ytd = round((sp500_value - sp500_start) / sp500_start * 100, 2)

print(f"FTSE All-Share: {ftse_value} (as of {ftse_date}) | YTD: +{ftse_ytd}% from {ftse_start}")
print(f"S&P 500:        {sp500_value} (as of {sp500_date}) | YTD: +{sp500_ytd}% from {sp500_start}")
```

### Known Year-Start Values (hardcoded fallback only)

| Index | 1 Jan 2026 | 1 Jan 2025 |
|-------|-----------|-----------| 
| FTSE All-Share | 5,350.38 | 4,467.80 |
| S&P 500 | 6,845.50 | 5,881.63 |

Always use the API value. Only use hardcoded values if the API call fails, and flag the fallback to Mick.

---

## Step 2: Update the Indices Spreadsheet

After fetching values, update the DRAFT spreadsheet on Mick's PC.

### File Location Pattern

```
C:\Users\pavey\Documents\0.2 - Areas (n)\02 - DIY - Investors\001 - DIY - Images\01 - Indices\A_Indices Monthly Performance\YYYY.MM.DD - Indices Monthly Performance_YYYY_v.01.MM_[MonthAbbr]-DRAFT.xlsx
```

Use `Filesystem:list_directory` on the folder to find the current DRAFT file - do not guess the exact filename.

### Column Mapping

| Month | Excel Column |
|-------|-------------|
| Jan | E |
| Feb | F |
| Mar | G |
| Apr | H |
| May | I |
| Jun | J |
| Jul | K |
| Aug | L |
| Sep | M |
| Oct | N |
| Nov | O |
| Dec | P |

### Rows to Update (End row only - all other rows use formulas)

| Index | Row |
|-------|-----|
| FTSE All-Share End | 8 |
| S&P 500 End | 17 |

Example: for March 2026, update cells G8 (FTSE) and G17 (S&P 500).

### Update Process

```python
import openpyxl

# 1. Copy file from Mick's PC using Filesystem:copy_file_user_to_claude
# 2. Load workbook
wb = openpyxl.load_workbook(local_path)
ws = wb.active

# 3. Map month to column letter
col_map = {1:'E', 2:'F', 3:'G', 4:'H', 5:'I', 6:'J',
           7:'K', 8:'L', 9:'M', 10:'N', 11:'O', 12:'P'}
col = col_map[month]

# 4. Write End values (row 8 = FTSE, row 17 = SP500)
ws[f'{col}8'] = ftse_value
ws[f'{col}17'] = sp500_value

# 5. Save
wb.save(output_path)
```

### Spreadsheet Notes

- Only update the End row. All other rows (Start, Change, % Change) are formulas already present.
- The G7 Start formula was corrected in March 2026 to `=F8` (not `=E$8`). Do not overwrite formula rows.
- After updating, use `present_files` to deliver the file to Mick.
- Remind Mick to save the updated file back to the correct path and rename from DRAFT when the month is closed.

---

## Output

Return a structured result for use by calling skills:

```json
{
  "ftse": {
    "ticker": "^FTAS",
    "label": "All-Share Index (ASX)",
    "year_start": 5350.38,
    "month_end_value": 5489.12,
    "month_end_date": "2026-03-31",
    "ytd_pct": 2.59
  },
  "sp500": {
    "ticker": "^GSPC",
    "label": "SP500 index (SP500)",
    "year_start": 6845.50,
    "month_end_value": 5611.85,
    "month_end_date": "2026-03-31",
    "ytd_pct": -18.01
  },
  "spreadsheet_updated": true,
  "spreadsheet_path": "[path to updated DRAFT file on Claude's computer]"
}
```

---

## Error Handling

### Yahoo Finance API failure

```
Yahoo Finance API returned no data for [ticker] for [Month YYYY].
Falling back to hardcoded year-start value: [value].
Please verify this value is correct before publishing.
```

### Spreadsheet DRAFT file not found

```
Could not find the Indices DRAFT spreadsheet for [YYYY].
Looked in: C:\Users\pavey\Documents\0.2 - Areas (n)\02 - DIY - Investors\001 - DIY - Images\01 - Indices\A_Indices Monthly Performance\
Files found:
  [list files in folder]
Please confirm the correct filename.
```

---

## Mid-Month Usage

When called mid-month (e.g. for a newsletter or market commentary):
- `get_month_end_close` returns the most recent available close
- The `month_end_date` field will show the actual date of the last close (not necessarily the last day of the month)
- Do NOT update the spreadsheet when called mid-month (set `update_spreadsheet: false`)
- Flag to the caller that the value is a mid-month snapshot, not a definitive month-end close

---

## Style Rules & Learnings

### 2026.03.30 - Skill created
Extracted from portfolio-post-creator. Now the single source of truth for benchmark data
across all skills (portfolio posts, sector posts, market commentary, newsletter, etc.).

# ShareScope - AX Tree Master Reference

**Project:** ax-trees-automation
**Source:** Migrated from 04-Projects/2026.04.04-ShareScope-Automation/
**Original capture date:** 2026-04-26 (live via Playwright MCP)
**Last updated:** 2026-05-01

---

## 1. Login Page

**URL:** https://webservice.sharescope.co.uk/login.do
(IMPORTANT: NOT https://www.sharescope.co.uk -- that is the marketing homepage and does not work)

### Confirmed Selectors

| Element | Selector (Python) | Selector (JS) | Notes |
|---------|------------------|--------------|-------|
| Email field | get_by_role("textbox", name="Email:") | getByRole("textbox", {name: "Email:"}) | Active/focused on load |
| Password field | get_by_role("textbox", name="Password:") | getByRole("textbox", {name: "Password:"}) | Standard input |
| Login button | get_by_role("button", name="Login") | getByRole("button", {name: "Login"}) | Submits form |

### Login Sequence (confirmed working)

1. navigate(https://webservice.sharescope.co.uk/login.do) -- wait: networkidle
2. fill email field
3. wait 500ms (REQUIRED -- established during Phase 1 testing)
4. fill password field
5. click Login button
6. wait for URL to change away from login page (timeout: 20s)
7. verify: 'login' absent from current URL

### Post-Login URL Pattern

  https://engine-N.sharescope.co.uk/SSWeb/app.do;jsessionid={SESSION_KEY}

Engine number varies per session (engine-2, engine-7, etc.) -- handled automatically.
jsessionid is maintained by the Playwright browser session -- no manual handling needed.

### Credentials

Location: C:\Vaults\Mick's Vault\.env
  SHARESCOPE_USERNAME=mick@diy-investors.com
  SHARESCOPE_PASSWORD="SPad#m1045"
  SHARESCOPE_HEADLESS=false

Note: Password contains # -- must be in double quotes in .env file.

---

## 2. Main Application Navigation

### Top Navigation Buttons

| Element | Selector | Notes |
|---------|---------|-------|
| Search | button "Search" | Opens "Find a share" dialog |
| Chart | button "Chart" | Chart view |
| Financials | button "Financials" | Switches to financials panel |
| News | button "News" | News view |
| More | button "More" | Additional options |

### Index / List Buttons

| Element | Selector |
|---------|---------|
| FTSE 100 | button "FTSE 100" |
| FTSE All | button "FTSE All" |
| US 500 | button "US 500" |
| Portfolios | button "Portfolios" |

### Portfolio Navigation (confirmed pattern)

Portfolio switching via My Ports button. Most reliable method: JavaScript click
on the anchor element matching the portfolio name:

  page.evaluate("""() => {
    const links = document.querySelectorAll('a');
    for (const link of links) {
      if (link.textContent.trim().includes('Portico_Longlist')) {
        link.click();
        return 'clicked: ' + link.textContent.trim();
      }
    }
    return 'not found';
  }""")

Known portfolio names (as of April 2026):
  "0 - 0 - 2026 - PP2 (UK)"                    -- main UK active portfolio (19 holdings)
  "0 - 0 - 2026 - Portico_Longlist & Watchlist" -- research watchlist (30+ stocks)

---

## 3. Stock Search

### Search Dialog Selectors

| Element | Selector | Notes |
|---------|---------|-------|
| Search button | button "Search" | Opens dialog |
| Dialog heading | heading "Find a share" | Confirms dialog open |
| Index combobox | combobox [id="find-share-dlg-list"] | MUST set to "All instruments" |
| Search text | searchbox "Name, TIDM, Sedol or ISIN" | Use pressSequentially() |
| OK button | button "OK" | Disabled until result selected |
| Cancel button | button "Cancel" | Closes dialog |

### CRITICAL: Combobox Default

The combobox may default to the last-used index (e.g. "Belgium top 20").
ALWAYS set it to "All instruments" before searching, or results will be empty.

Python: page.locator("#find-share-dlg-list").select_option("All instruments")
JS:     await page.locator('#find-share-dlg-list').selectOption('All instruments')

### Search Input Behaviour

- Element type: searchbox (NOT a standard text input)
- Must use pressSequentially() -- types character by character
- If field has old text, clear it first before typing
- Results appear dynamically as you type (no Enter needed)

Python: page.get_by_role("searchbox", ...).press_sequentially("SQZ", delay=100)
JS:     await page.getByRole("searchbox", ...).pressSequentially("SQZ", {delay: 100})

### Result Structure

Each result in the list is a clickable generic containing:
  - Ticker/exchange (e.g. "LSE:SQZ" or "NASDAQ:AAPL")
  - ISIN (where available)
  - Instrument type (e.g. "Ord", "Preference", "Unit Trust")
  - Company name
  - Exchange info

To select: click the result generic matching target ticker, then click "OK".

---

## 4. Financial Data Tabs

### Tab Buttons

| Tab | Selector | CSV Available |
|-----|---------|--------------|
| Summary | button "Summary" | NO (visual only) |
| Company | button "Company" | NO (qualitative text) |
| Income | button "Income" | YES |
| Balance | button "Balance" | YES |
| Cash | button "Cash" | YES |
| Ratios | button "Ratios" | YES |
| Dividends | button "Dividends" | YES |
| Forecasts | button "Forecasts" (.first() if multiple) | YES |
| Custom | button "Custom" | YES |
| Sharing | button "Sharing" | N/A (opens export dropdown) |

### CSV Download Filenames (confirmed)

| Tab | Filename |
|-----|---------|
| Income | LSE_{TICKER}_income_statement.csv |
| Balance | LSE_{TICKER}_balance_sheet.csv |
| Cash | LSE_{TICKER}_cash_flow.csv |
| Ratios | LSE_{TICKER}_ratios.csv |
| Dividends | LSE_{TICKER}_dividends.csv |
| Forecasts | LSE_{TICKER}_forecasts.csv |
| Custom | LSE_{TICKER}_custom_sheet.csv |

---

## 5. Export Mechanism

### Step-by-Step

1. Click tab button (e.g. button "Income")
2. Wait for tab to load
3. Click button "Sharing" -- opens dropdown
4. Click "Export data..." -- TRIGGERS IMMEDIATE DOWNLOAD (no dialog, no confirmation)

### CRITICAL: Download Behaviour

Files download IMMEDIATELY on click with NO save dialog.

Python -- use expect_download() context manager:
  with page.expect_download() as download_info:
      page.get_by_text("Export data...").click()
  download = download_info.value
  download.save_as(output_path / f"{ticker}_{tab_name}.csv")

JS -- use waitForEvent('download'):
  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.getByText('Export data...').click()
  ]);
  await download.saveAs(path.join(outputPath, `${ticker}_${tabName}.csv`));

Browser context must be created with accept downloads enabled:
  Python: context = browser.new_context(accept_downloads=True)
  JS:     const context = await browser.newContext({ acceptDownloads: true })

### Sharing Dropdown Contents

After clicking Sharing button:
  - listitem: "Print..."
  - listitem: "Export data..."

Use text matching -- NOT ref IDs (refs are dynamic per page load).

---

## 6. Known Quirks and Gotchas

1. 500ms delay REQUIRED between email and password entry on login (server-side)
2. Combobox ALWAYS defaults to last-used index -- always reset to "All instruments"
3. Forecasts button: use .first() if multiple matches appear on the page
4. Search input type is searchbox not text -- pressSequentially(), not fill()
5. Engine number (engine-2, engine-7, etc.) varies per session -- do not hardcode
6. jsessionid in URL is auto-maintained by browser context -- no manual handling needed
7. Downloads happen immediately on "Export data..." -- download listener must be ready first
8. US stocks: tested and working (see HAL - Halliburton, COIN - Coinbase, COST - Costain)

---

## 7. Version History

| Date | File | Notes |
|------|------|-------|
| 2026-04-26 | versions/2026-04-26-login-ax-tree.md | Original login page capture |
| 2026-04-26 | versions/2026-04-26-export-ax-tree.md | Export and search mechanism capture |

See versions/ subfolder for dated snapshots of the raw AX tree data.

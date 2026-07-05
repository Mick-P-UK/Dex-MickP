// sharescope.adapter.example.js
// ax-mapper - WORKED EXAMPLE adapter for ShareScope.
//
// This is the reference showing how the generic ax-mapper engine reproduces the
// original ShareScope mapper. It ports the nav table from the ax-trees-automation
// project (mini-projects/sharescope-mapper/scripts/nav-table.js).
//
// STATUS: EXAMPLE. --dry-run works standalone (requiring this file has no side
// effects). A LIVE harvest additionally needs:
//   - the ax-trees-automation project's ShareScope skills (login/search/logout),
//   - Playwright installed,
//   - C:\Users\pavey\.env credentials (read by the login skill; NEVER hardcoded).
// Point the engine at the project's skills folder via the env var
//   AX_MAPPER_SHARESCOPE_SKILLS=<abs path to ax-trees-automation/skills>
// Live runs are a Windows/Desktop task (headed browser), not a sandbox task.

'use strict';

const path = require('path');

// Ticker to map (frontmatter/target). Override with AX_MAPPER_TICKER=SQZ etc.
const TICKER = (process.env.AX_MAPPER_TICKER || 'GGP').toUpperCase();

// Resolve the ShareScope skills folder from the parent project (live runs only).
function skillsDir() {
  const dir = process.env.AX_MAPPER_SHARESCOPE_SKILLS;
  if (!dir) {
    throw new Error('Set AX_MAPPER_SHARESCOPE_SKILLS to the ax-trees-automation/skills path for a live ShareScope harvest.');
  }
  return dir;
}

// --- ShareScope-specific navigation helpers (ported from the project) ---------
function financialsPane(page) { return page.locator('div.window.secondary'); }

async function ensureFinancials(page, helpers) {
  await page.getByRole('button', { name: 'Financials' }).click();
  await helpers.delay('medium');
}

function financialTabReach(dataCmd) {
  return async function (page, helpers) {
    await ensureFinancials(page, helpers);
    await financialsPane(page).locator('button[data-cmd="' + dataCmd + '"]').click();
    await helpers.delay('medium');
  };
}

async function closeOverlay(page, helpers) {
  try { await page.keyboard.press('Escape'); await helpers.delay('short'); } catch (e) { /* non-fatal */ }
}

module.exports = {
  name: 'sharescope',
  target: TICKER,

  // ShareScope tags controls with data-cmd - the stable selector attribute.
  controls: { customAttribute: 'data-cmd' },

  // Right-hand data pane holds the financial statements.
  mainRegionSelector: 'div.window.secondary',

  // ShareScope-specific additions to the core denylist.
  denylist: ['dealing', 'portdelete', 'viewtrades'],

  openSession: async function (opts) {
    const { sharescopeLogin } = require(path.join(skillsDir(), 'sharescope-login'));
    const { sharescopeSearch } = require(path.join(skillsDir(), 'sharescope-search'));
    const { sharescopeLogout } = require(path.join(skillsDir(), 'sharescope-logout'));

    const session = await sharescopeLogin({ headless: !!opts.headless });
    const page = session.page;
    try { await page.setViewportSize({ width: 1920, height: 1080 }); } catch (e) { /* headed window may ignore */ }
    await sharescopeSearch(page, TICKER, {}); // leaves page on the Financials panel

    return {
      page: page,
      close: async function () {
        try { await sharescopeLogout(page, {}); } catch (e) { /* best effort */ }
        if (session.browser) { try { await session.browser.close(); } catch (e) { /* ignore */ } }
      },
    };
  },

  returnHome: async function (page, helpers) {
    try { await page.getByRole('button', { name: 'Financials' }).click(); await helpers.delay('short'); }
    catch (e) { /* non-fatal */ }
  },

  states: [
    { key: 'home-after-login', label: 'Home (post-login landing)', note: 'Baseline; no navigation.',
      reach: async function (page, helpers) { await helpers.delay('short'); } },
    { key: 'search-dialog-open', label: 'Find a share dialog', note: 'Open, capture, Cancel.',
      reach: async function (page, helpers) {
        await page.getByRole('button', { name: 'Search' }).click();
        await page.getByRole('heading', { name: 'Find a share', level: 4 }).waitFor({ timeout: 10000 });
        await helpers.delay('short');
      },
      cleanup: async function (page, helpers) {
        try { await page.getByRole('button', { name: 'Cancel' }).click({ timeout: 3000 }); await helpers.delay('short'); }
        catch (e) { await closeOverlay(page, helpers); }
      } },
    { key: 'financials-summary',   label: 'Financials: Summary',   reach: financialTabReach('ShowSummary') },
    { key: 'financials-company',   label: 'Financials: Company',   reach: financialTabReach('ShowCompany') },
    { key: 'financials-income',    label: 'Financials: Income',    reach: financialTabReach('ShowIncomeStatement') },
    { key: 'financials-balance',   label: 'Financials: Balance',   reach: financialTabReach('ShowBalanceSheet') },
    { key: 'financials-cashflow',  label: 'Financials: Cash Flow', reach: financialTabReach('ShowCashFlow') },
    { key: 'financials-ratios',    label: 'Financials: Ratios',    reach: financialTabReach('ShowRatios') },
    { key: 'financials-dividends', label: 'Financials: Dividends', reach: financialTabReach('ShowDividends') },
    { key: 'financials-forecasts', label: 'Financials: Forecasts', note: 'Uses ShowBrokers.', reach: financialTabReach('ShowBrokers') },
    { key: 'financials-custom',    label: 'Financials: Custom',    reach: financialTabReach('ShowCustom') },
    { key: 'chart-view', label: 'Chart view', note: 'button[data-cmd=ViewChart].',
      reach: async function (page, helpers) {
        await page.locator('button[data-cmd="ViewChart"]').first().click();
        await helpers.delay('medium');
      } },
    { key: 'news-view', label: 'News view',
      reach: async function (page, helpers) {
        await page.getByRole('button', { name: 'News' }).click();
        await helpers.delay('medium');
      } },
    { key: 'more-menu', label: 'More menu', note: 'Open, capture, close.',
      reach: async function (page, helpers) {
        await page.getByRole('button', { name: 'More' }).click();
        await helpers.delay('short');
      }, cleanup: closeOverlay },
    { key: 'options-menu-open', label: 'Options (cog) menu', note: 'Never click logout here.',
      reach: async function (page, helpers) {
        const cog = page.locator('#cogwheel-menu-main button[title="Options menu"]');
        await cog.waitFor({ state: 'visible', timeout: 10000 });
        await cog.click();
        await helpers.delay('short');
      }, cleanup: closeOverlay },
    // --- news types (stays in the STOCK adapter; News is a stock/list view) ---
    { key: 'news-categories-design', label: 'News categories + Design dialog (news types)',
      note: 'News types: ShowAllNews/ShowShareNews/ShowListNews/RNS/HotStory/LatestNewsHeadlines + Design sub-options.',
      reach: async function (page, helpers) {
        await page.getByRole('button', { name: 'News' }).click();
        await helpers.delay('medium');
        await page.locator('button[data-cmd="Design"]').first().click();
        await helpers.delay('medium');
      }, cleanup: closeOverlay },
  ],
};

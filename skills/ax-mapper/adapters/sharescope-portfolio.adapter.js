// sharescope-portfolio.adapter.js
// ax-mapper - ShareScope PORTFOLIO adapter (clean portfolio-first flow).
//
// Deliberately does NOT search for a stock. The correct portfolio flow is:
//   log in -> portfolio selector -> pick the portfolio -> display it -> export.
// (The stock adapter searches a ticker because its job is mapping a stock; that
// is the wrong flow for portfolios, per Mick 2026-07-04.)
//
// STATUS: EXAMPLE. --dry-run works standalone. A LIVE harvest needs the project
// ShareScope skills, Playwright, and C:\Users\pavey\.env (creds never hardcoded).
//   AX_MAPPER_SHARESCOPE_SKILLS=<abs path to ax-trees-automation/skills>
// Portfolio button labels (PP1/PP2) are Mick-account-specific.
// Read-only: dialogs are cancelled, nothing is downloaded. Selecting PP1 changes
// the active portfolio (reversible - reselect your Active 10 afterwards).

'use strict';

const path = require('path');

function skillsDir() {
  const dir = process.env.AX_MAPPER_SHARESCOPE_SKILLS;
  if (!dir) throw new Error('Set AX_MAPPER_SHARESCOPE_SKILLS to the ax-trees-automation/skills path for a live harvest.');
  return dir;
}

async function closeOverlay(page, helpers) {
  try { await page.keyboard.press('Escape'); await helpers.delay('short'); } catch (e) { /* non-fatal */ }
}

// The portfolio to map. Override with AX_MAPPER_PORTFOLIO="0 - 0 - 2026 - PP2 (UK)".
const PORTFOLIO = process.env.AX_MAPPER_PORTFOLIO || '0 - 0 - 2026 - PP1 (UK)';

async function selectPortfolio(page, helpers) {
  await page.getByRole('button', { name: PORTFOLIO, exact: true }).click();
  await helpers.delay('long');
}

module.exports = {
  name: 'sharescope-portfolio',
  target: PORTFOLIO,
  controls: { customAttribute: 'data-cmd' },
  denylist: ['dealing', 'portdelete', 'viewtrades'],

  // Log in, widen the window, and STOP - land on the default view (no stock search).
  openSession: async function (opts) {
    const { sharescopeLogin } = require(path.join(skillsDir(), 'sharescope-login'));
    const { sharescopeLogout } = require(path.join(skillsDir(), 'sharescope-logout'));
    const session = await sharescopeLogin({ headless: !!opts.headless });
    const page = session.page;
    try { await page.setViewportSize({ width: 1920, height: 1080 }); } catch (e) { /* headed may ignore */ }
    return {
      page: page,
      close: async function () {
        try { await sharescopeLogout(page, {}); } catch (e) { /* best effort */ }
        if (session.browser) { try { await session.browser.close(); } catch (e) { /* ignore */ } }
      },
    };
  },

  states: [
    { key: 'pf-landing', label: 'Post-login landing (should show the top portfolio toolbar)',
      note: 'Baseline: capture whatever the app opens on after login (no stock search).',
      reach: async function (page, helpers) { await helpers.delay('long'); } },
    { key: 'pf-selector-dropdown', label: 'Portfolio selector dropdown (recent + manage)',
      note: 'CONFIRM: click the Portfolios / portfolio-selector button; capture dropdown; Escape.',
      reach: async function (page, helpers) {
        await page.getByRole('button', { name: 'Portfolios' }).click();
        await helpers.delay('medium');
      }, cleanup: closeOverlay },
    { key: 'pf-manage-dialog', label: 'Select or manage portfolios dialog (full list incl PP1 PP2)',
      note: 'CONFIRM: Portfolios -> Select or manage portfolios; capture dialog; Cancel.',
      reach: async function (page, helpers) {
        await page.getByRole('button', { name: 'Portfolios' }).click();
        await helpers.delay('short');
        await page.locator('li[data-cmd="PortManage"] a').first().click();
        await helpers.delay('medium');
      },
      cleanup: async function (page, helpers) {
        try { await page.getByRole('button', { name: 'Cancel' }).click({ timeout: 3000 }); await helpers.delay('short'); }
        catch (e) { await closeOverlay(page, helpers); }
      } },
    { key: 'pf-holdings', label: 'Selected portfolio holdings view',
      note: 'CONFIRM: click the portfolio button (default PP1). SWITCHES active portfolio (reversible).',
      reach: async function (page, helpers) { await selectPortfolio(page, helpers); } },
    { key: 'pf-transactions', label: 'Selected portfolio Transactions view',
      note: 'CONFIRM: on the portfolio, click the top-menu Transactions button.',
      reach: async function (page, helpers) {
        await selectPortfolio(page, helpers);
        await page.getByRole('button', { name: 'Transactions', exact: true }).click();
        await helpers.delay('medium');
      } },
    { key: 'pf-export-options', label: 'Export options dialog (Holdings / latest / Transactions)',
      note: 'CONFIRM: portfolio -> Transactions -> Sharing -> Export holdings/transactions (TransExportDataOption); capture dialog; Cancel (no download).',
      reach: async function (page, helpers) {
        await selectPortfolio(page, helpers);
        await page.getByRole('button', { name: 'Transactions', exact: true }).click();
        await helpers.delay('medium');
        await page.getByRole('button', { name: 'Sharing' }).first().click();
        await helpers.delay('short');
        await page.locator('li[data-cmd="TransExportDataOption"] a').first().click();
        await helpers.delay('medium');
      },
      cleanup: async function (page, helpers) {
        try { await page.getByRole('button', { name: 'Cancel' }).click({ timeout: 3000 }); await helpers.delay('short'); }
        catch (e) { await closeOverlay(page, helpers); }
      } },
  ],
};

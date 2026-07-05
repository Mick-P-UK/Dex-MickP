// adapter-template.js
// ax-mapper - ADAPTER TEMPLATE. Copy this file to make a mapper for a new app.
//
// An adapter is the ONLY app-specific part of ax-mapper. It teaches the generic
// engine three things:
//   1. How to open a logged-in session (openSession).
//   2. Which states to visit and how to reach each (states[]).
//   3. Any app-specific hints (custom attribute, main region, extra denylist).
//
// IMPORTANT: requiring this file must have NO side effects (no browser launch,
// no network). Do the work inside openSession() only. That keeps --dry-run safe.

'use strict';

module.exports = {
  // Short machine name; used for output filenames and the source-app frontmatter.
  name: 'template-app',

  // Optional: what was mapped (e.g. a ticker, a URL, an account). Frontmatter only.
  target: null,

  // Optional hints for the generic capture pass.
  controls: {
    // If the app tags controls with a stable attribute, name it here and the
    // engine will build a consolidated catalogue + suggested selectors from it.
    // Leave undefined for apps that only expose ARIA roles/names.
    customAttribute: undefined, // e.g. 'data-cmd', 'data-testid'
  },

  // Optional: CSS selector for the main content region (trimmed DOM is grabbed
  // from here). Defaults to <body> when omitted.
  mainRegionSelector: undefined, // e.g. 'main', 'div.content'

  // Extra denylist tokens merged with the engine core list. Add anything that,
  // for THIS app, must never be navigated to or clicked.
  denylist: [], // e.g. ['exportall', 'reset']

  /**
   * Open a live, logged-in Playwright session.
   * MUST return { page, close } where close() logs out and closes the browser.
   * @param {{headless:boolean}} opts
   * @returns {Promise<{page: import('playwright').Page, close: () => Promise<void>}>}
   */
  openSession: async function (opts) {
    // Example skeleton (uncomment and adapt; requires `playwright` installed):
    //
    // const { chromium } = require('playwright');
    // const browser = await chromium.launch({ headless: !!opts.headless });
    // const context = await browser.newContext();
    // const page = await context.newPage();
    // await page.goto('https://your-app.example/login');
    // ... perform login here (read credentials from an .env, NEVER hardcode) ...
    // return {
    //   page: page,
    //   close: async function () { /* log out if needed */ await browser.close(); },
    // };
    throw new Error('adapter-template: implement openSession() before running a live harvest.');
  },

  // Optional: return the UI to a neutral baseline between states so a
  // mis-navigation cannot cascade. Called after each state's capture+cleanup.
  returnHome: async function (page, helpers) {
    // e.g. await page.goto(HOME_URL); await helpers.delay('short');
  },

  // Ordered list of read-only states to visit.
  // Each: { key, label, note?, reach(page, helpers), cleanup?(page, helpers) }
  // - reach(): navigate to the state. helpers.delay('short'|'medium'|'long').
  // - cleanup(): optional; close any transient overlay opened by reach().
  states: [
    {
      key: 'home',
      label: 'Home (post-login landing)',
      note: 'Baseline snapshot; no navigation.',
      reach: async function (page, helpers) { await helpers.delay('short'); },
    },
    // {
    //   key: 'some-dialog-open',
    //   label: 'Some dialog',
    //   note: 'Open, capture, then Cancel (non-mutating).',
    //   reach: async function (page, helpers) {
    //     await page.getByRole('button', { name: 'Open thing' }).click();
    //     await helpers.delay('short');
    //   },
    //   cleanup: async function (page, helpers) {
    //     await page.keyboard.press('Escape');
    //     await helpers.delay('short');
    //   },
    // },
  ],
};

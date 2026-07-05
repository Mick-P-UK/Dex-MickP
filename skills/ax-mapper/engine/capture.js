// capture.js
// ax-mapper - generic four-artefact capture helper (READ-ONLY).
//
// Given a live Playwright page already in a known state, records:
//   1. AX snapshot        - the accessibility tree (locator.ariaSnapshot()).
//   2. Control inventory  - every interactive control by role + accessible name.
//   3. Custom-attr catalogue (optional) - e.g. [data-cmd] for apps that expose one.
//   4. Trimmed DOM + screenshot for selector confirmation.
//
// This helper NEVER clicks anything. It only observes the current state.
// It is app-agnostic: everything app-specific arrives via `controlConfig`
// (from the adapter). The default control scan uses ARIA roles, so it works on
// any web app - the custom-attribute catalogue is a bonus for apps like
// ShareScope that tag controls with a stable attribute.

'use strict';

const path = require('path');

const MAX_DOM_CHARS = 20000;

// Roles/tags considered "interactive" for the generic inventory.
const INTERACTIVE_SELECTOR = [
  'button', 'a[href]', 'input', 'select', 'textarea',
  '[role="button"]', '[role="link"]', '[role="menuitem"]',
  '[role="tab"]', '[role="checkbox"]', '[role="radio"]', '[role="combobox"]',
].join(', ');

/**
 * Generic interactive-control inventory: role + accessible name for every
 * interactive element on the current screen. Runs in the page context.
 */
async function scrapeControls(page) {
  return page.$$eval(INTERACTIVE_SELECTOR, function (els) {
    function nameOf(el) {
      var n = el.getAttribute('aria-label') || el.getAttribute('title') ||
        (el.textContent || '').trim() || el.getAttribute('name') ||
        el.getAttribute('placeholder') || el.getAttribute('value') || '';
      return n.replace(/\s+/g, ' ').slice(0, 120);
    }
    return els.map(function (el) {
      return {
        tag: el.tagName.toLowerCase(),
        role: el.getAttribute('role') || el.tagName.toLowerCase(),
        name: nameOf(el),
        visible: !!(el.offsetParent !== null || el.getClientRects().length),
      };
    });
  });
}

/**
 * Optional custom-attribute catalogue (e.g. data-cmd). Only runs if the adapter
 * supplies controlConfig.customAttribute. Returns [] otherwise.
 */
async function scrapeCustomAttr(page, attr) {
  if (!attr) return [];
  const selector = '[' + attr + ']';
  return page.$$eval(selector, function (els, attrName) {
    return els.map(function (el) {
      return {
        value: el.getAttribute(attrName) || '',
        label: (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 120),
        role: el.getAttribute('role') || el.tagName.toLowerCase(),
        visible: !!(el.offsetParent !== null || el.getClientRects().length),
      };
    });
  }, attr);
}

/**
 * Grab a trimmed outerHTML of the main content region for selector confirmation.
 * Uses the adapter's mainRegionSelector when provided; falls back to body.
 */
async function grabMainDom(page, mainRegionSelector) {
  return page.evaluate(function (args) {
    var el = (args.sel && document.querySelector(args.sel)) || document.body;
    var html = el ? el.outerHTML : '';
    return html.length > args.max ? html.slice(0, args.max) + '\n<!-- TRIMMED -->' : html;
  }, { sel: mainRegionSelector || null, max: MAX_DOM_CHARS });
}

/**
 * Capture the current state into a record object.
 * @param {import('playwright').Page} page  Active page, already in target state.
 * @param {string} stateKey                 Stable key (e.g. "financials-income").
 * @param {object} [options]
 * @param {boolean} [options.screenshot=true]
 * @param {string}  [options.screenshotDir]
 * @param {object}  [options.controlConfig]     { customAttribute, mainRegionSelector }
 * @param {function}[options.isDenied]          matcher; flags custom-attr controls
 * @returns {Promise<object>} record
 */
async function captureState(page, stateKey, options) {
  options = options || {};
  const cfg = options.controlConfig || {};
  const doShot = options.screenshot !== undefined ? options.screenshot : true;
  const screenshotDir = options.screenshotDir || path.join(process.cwd(), 'output', 'screenshots');
  const isDenied = typeof options.isDenied === 'function' ? options.isDenied : function () { return false; };

  console.log('[capture] ' + stateKey + ' ...');

  // 1. Accessibility snapshot (version-agnostic).
  let axSnapshot = null;
  try {
    if (page.accessibility && typeof page.accessibility.snapshot === 'function') {
      axSnapshot = await page.accessibility.snapshot();
    } else {
      axSnapshot = await page.locator('body').ariaSnapshot();
    }
  } catch (e) {
    console.log('[capture] AX snapshot failed for ' + stateKey + ': ' + e.message);
  }

  // 2. Generic control inventory.
  let controls = [];
  try {
    controls = await scrapeControls(page);
  } catch (e) {
    console.log('[capture] control scan failed for ' + stateKey + ': ' + e.message);
  }

  // 3. Optional custom-attribute catalogue.
  let customControls = [];
  try {
    customControls = await scrapeCustomAttr(page, cfg.customAttribute);
    customControls = customControls.map(function (r) {
      r.denied = isDenied(r.value, r.label);
      return r;
    });
  } catch (e) {
    console.log('[capture] custom-attr scan failed for ' + stateKey + ': ' + e.message);
  }

  // 4. Main-region DOM (trimmed).
  let mainDomHtml = '';
  try {
    mainDomHtml = await grabMainDom(page, cfg.mainRegionSelector);
  } catch (e) {
    console.log('[capture] DOM grab failed for ' + stateKey + ': ' + e.message);
  }

  // 5. Screenshot (generic Playwright; no app-specific skill needed).
  let screenshotPath = null;
  if (doShot) {
    try {
      const fs = require('fs');
      fs.mkdirSync(screenshotDir, { recursive: true });
      const abs = path.join(screenshotDir, stateKey + '.png');
      await page.screenshot({ path: abs, fullPage: false });
      screenshotPath = path.join('screenshots', path.basename(abs));
    } catch (e) {
      console.log('[capture] screenshot failed for ' + stateKey + ': ' + e.message);
    }
  }

  // Suggested selectors: prefer stable custom-attribute selectors when present.
  const suggestedSelectors = customControls
    .filter(function (r) { return r.value; })
    .map(function (r) { return r.role + '[' + (cfg.customAttribute || 'data-attr') + '="' + r.value + '"]'; });

  return {
    state_key: stateKey,
    captured_at: new Date().toISOString(),
    url: page.url(),
    ax_snapshot: axSnapshot,
    controls: controls,
    custom_controls: customControls,
    suggested_selectors: suggestedSelectors,
    main_dom_html: mainDomHtml,
    screenshot_path: screenshotPath,
  };
}

module.exports = {
  captureState: captureState,
  scrapeControls: scrapeControls,
  scrapeCustomAttr: scrapeCustomAttr,
};

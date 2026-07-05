// mapper.js
// ax-mapper - generic, adapter-driven orchestrator (Phase 1, read-only harvest).
//
// The engine knows nothing about any specific app. All app knowledge lives in an
// ADAPTER (see ../adapters/adapter-template.js). The engine:
//   open session (adapter) -> walk adapter.states -> capture each -> cleanup ->
//   return to baseline -> write JSON inventory + generated markdown -> close.
//
// Read-only: it visits only the states the adapter lists, never clicks a control
// matching the denylist, and never actuates logout during the walk (the adapter's
// close() handles teardown).
//
// Usage:
//   node engine/mapper.js --adapter <path> --dry-run
//   node engine/mapper.js --adapter <path> --out ./output
//   node engine/mapper.js --adapter <path> --headless
//   node engine/mapper.js --adapter <path> --only home,chart-view   (subset of states)
//
// --dry-run prints the plan WITHOUT launching a browser (safe anywhere).
// --only restricts the walk to the named state keys (comma-separated) - handy for
//   a light single-screen live proof before a full harvest.

'use strict';

const fs = require('fs');
const path = require('path');

const { captureState } = require('./capture');
const { renderMarkdown } = require('./render-md');
const { makeIsDenied } = require('./denylist');
const { delay } = require('./delay');

function parseArgs(argv) {
  const args = { adapter: null, out: null, dryRun: false, headless: false, only: null };
  const rest = argv.slice(2);
  for (let i = 0; i < rest.length; i++) {
    const a = rest[i];
    if (a === '--dry-run') args.dryRun = true;
    else if (a === '--headless') args.headless = true;
    else if (a === '--adapter') args.adapter = rest[++i];
    else if (a === '--out') args.out = rest[++i];
    else if (a === '--only') args.only = rest[++i];
  }
  return args;
}

function loadAdapter(adapterPath) {
  if (!adapterPath) throw new Error('No adapter given. Use --adapter <path>.');
  const resolved = path.isAbsolute(adapterPath) ? adapterPath : path.resolve(process.cwd(), adapterPath);
  const adapter = require(resolved);
  if (!adapter.name) throw new Error('Adapter missing "name".');
  if (!Array.isArray(adapter.states) || !adapter.states.length) {
    throw new Error('Adapter missing non-empty "states" array.');
  }
  return adapter;
}

// Select the states to walk, honouring an optional --only filter (by state key).
function selectStates(adapter, only) {
  if (!only) return adapter.states.slice();
  const wanted = String(only).split(',').map(function (s) { return s.trim(); }).filter(Boolean);
  const chosen = adapter.states.filter(function (s) { return wanted.indexOf(s.key) > -1; });
  const missing = wanted.filter(function (w) {
    return !adapter.states.some(function (s) { return s.key === w; });
  });
  if (missing.length) console.log('[ax-mapper] WARNING: --only names unknown state(s): ' + missing.join(', '));
  return chosen;
}

// ---------------------------------------------------------------------------
// Dry-run: print the ordered plan and per-state denylist decision. No browser.
// ---------------------------------------------------------------------------
function dryRun(adapter, args) {
  const isDenied = makeIsDenied(adapter.denylist);
  const states = selectStates(adapter, args && args.only);
  console.log('[ax-mapper] DRY RUN - no browser launched, nothing actuated.');
  console.log('[ax-mapper] adapter: ' + adapter.name);
  console.log('[ax-mapper] custom attribute: ' + ((adapter.controls && adapter.controls.customAttribute) || '(none)'));
  console.log('[ax-mapper] extra denylist tokens: ' + ((adapter.denylist || []).join(', ') || '(none)'));
  if (args && args.only) console.log('[ax-mapper] --only filter active: ' + args.only);
  console.log('[ax-mapper] planned states (' + states.length + ' of ' + adapter.states.length + '):');
  states.forEach(function (s, i) {
    const denied = isDenied(s.key, s.label);
    console.log('  ' + String(i + 1).padStart(2, '0') + '. ' + s.key +
      '  [' + (denied ? 'DENIED - WOULD SKIP' : 'allowed') + ']' +
      (s.cleanup ? '  (has cleanup)' : '') +
      (s.note ? '  - ' + s.note : ''));
  });
  console.log('[ax-mapper] dry run complete.');
}

// ---------------------------------------------------------------------------
// Live harvest.
// ---------------------------------------------------------------------------
async function liveHarvest(adapter, args) {
  const outDir = args.out ? path.resolve(process.cwd(), args.out) : path.resolve(process.cwd(), 'output');
  const shotsDir = path.join(outDir, 'screenshots');
  const inventoryPath = path.join(outDir, adapter.name + '-inventory.json');
  const generatedMdPath = path.join(outDir, adapter.name + '-ax-tree-map.generated.md');

  const isDenied = makeIsDenied(adapter.denylist);
  const controlConfig = {
    customAttribute: adapter.controls && adapter.controls.customAttribute,
    mainRegionSelector: adapter.mainRegionSelector,
  };
  const helpers = { delay: delay };
  const plan = selectStates(adapter, args.only);

  fs.mkdirSync(shotsDir, { recursive: true });
  console.log('[ax-mapper] LIVE harvest for adapter "' + adapter.name + '", headless=' + args.headless +
    (args.only ? ', only=' + args.only : ''));
  console.log('[ax-mapper] walking ' + plan.length + ' of ' + adapter.states.length + ' states.');

  let session = null;
  const records = [];

  try {
    session = await adapter.openSession({ headless: args.headless });
    if (!session || !session.page) throw new Error('adapter.openSession() did not return { page, close }.');
    const page = session.page;
    await delay('long');

    for (let i = 0; i < plan.length; i++) {
      const state = plan[i];
      if (isDenied(state.key, state.label)) {
        console.log('[ax-mapper] SKIP (denylist): ' + state.key);
        continue;
      }
      console.log('[ax-mapper] state ' + (i + 1) + '/' + plan.length + ': ' + state.key);
      try {
        await state.reach(page, helpers);
        await delay('long');
        const record = await captureState(page, state.key, {
          screenshotDir: shotsDir,
          controlConfig: controlConfig,
          isDenied: isDenied,
        });
        records.push(record);
        if (typeof state.cleanup === 'function') await state.cleanup(page, helpers);
      } catch (e) {
        console.log('[ax-mapper] state failed (' + state.key + '): ' + e.message + ' - continuing.');
        records.push({ state_key: state.key, error: e.message, captured_at: new Date().toISOString() });
      }
      if (typeof adapter.returnHome === 'function') {
        try { await adapter.returnHome(page, helpers); } catch (e) { /* non-fatal */ }
      }
    }

    const inventory = {
      generated_at: new Date().toISOString(),
      source_app: adapter.name,
      target: adapter.target || null,
      custom_attribute: controlConfig.customAttribute || null,
      state_count: plan.length,
      only_filter: args.only || null,
      states: records,
    };
    fs.mkdirSync(outDir, { recursive: true });
    fs.writeFileSync(inventoryPath, JSON.stringify(inventory, null, 2), 'utf8');
    console.log('[ax-mapper] wrote inventory: ' + inventoryPath + ' (' + records.length + ' states).');

    fs.writeFileSync(generatedMdPath, renderMarkdown(inventory), 'utf8');
    console.log('[ax-mapper] wrote generated map: ' + generatedMdPath);
  } finally {
    if (session && typeof session.close === 'function') {
      try { await session.close(); } catch (e) { console.log('[ax-mapper] close note: ' + e.message); }
    }
    console.log('[ax-mapper] session closed.');
  }
}

async function main() {
  const args = parseArgs(process.argv);
  const adapter = loadAdapter(args.adapter);
  if (args.dryRun) { dryRun(adapter, args); return; }
  await liveHarvest(adapter, args);
}

if (require.main === module) {
  main().catch(function (err) {
    console.error('[ax-mapper] fatal: ' + err.message);
    process.exit(1);
  });
}

module.exports = { parseArgs: parseArgs, dryRun: dryRun, loadAdapter: loadAdapter, selectStates: selectStates };

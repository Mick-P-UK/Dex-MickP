// verify-inventory.js
// ax-mapper - generic post-harvest verifier. Confirms a live harvest inventory
// contains the controls you expect and enough coverage. App-agnostic: you pass
// the anchors to require.
//
// Usage:
//   node test/verify-inventory.js --inventory <path> --require a,b,c --min-count N
// Exit code 0 = PASS, 1 = FAIL, 2 = bad usage.

'use strict';
const fs = require('fs');

function arg(name, def) { const i = process.argv.indexOf(name); return i > -1 ? process.argv[i + 1] : def; }

const invPath = arg('--inventory');
const required = (arg('--require', '') || '').split(',').map(function (s) { return s.trim(); }).filter(Boolean);
const minCount = parseInt(arg('--min-count', '0'), 10) || 0;

if (!invPath) { console.error('usage: --inventory <path> [--require a,b,c] [--min-count N]'); process.exit(2); }

const inv = JSON.parse(fs.readFileSync(invPath, 'utf8'));
const seen = new Set();
(inv.states || []).forEach(function (s) {
  (s.custom_controls || []).forEach(function (c) { if (c.value) seen.add(c.value); });
});

let ok = true;
console.log('[verify] inventory: ' + invPath);
console.log('[verify] source-app: ' + (inv.source_app || '?') + ', states: ' + ((inv.states || []).length));
console.log('[verify] unique custom-attr controls: ' + seen.size);
required.forEach(function (r) {
  const has = seen.has(r); if (!has) ok = false;
  console.log('  ' + (has ? 'PASS' : 'FAIL') + '  anchor present: ' + r);
});
if (minCount) {
  const has = seen.size >= minCount; if (!has) ok = false;
  console.log('  ' + (has ? 'PASS' : 'FAIL') + '  unique count >= ' + minCount + ' (got ' + seen.size + ')');
}
const errStates = (inv.states || []).filter(function (s) { return s.error; });
console.log('  ' + (errStates.length ? 'WARN' : 'PASS') + '  states with capture errors: ' + errStates.length +
  (errStates.length ? ' [' + errStates.map(function (s) { return s.state_key; }).join(', ') + ']' : ''));
console.log('[verify] RESULT: ' + (ok ? 'PASS' : 'FAIL'));
process.exit(ok ? 0 : 1);

// render.test.js
// ax-mapper - offline test for the renderer + engine wiring.
//   node test/render.test.js

'use strict';

const fs = require('fs');
const path = require('path');
const assert = require('assert');

const { renderMarkdown } = require('../engine/render-md');
const { makeIsDenied } = require('../engine/denylist');
const { parseArgs, loadAdapter, selectStates } = require('../engine/mapper');

let passed = 0;
function check(name, fn) {
  try { fn(); passed++; console.log('  PASS  ' + name); }
  catch (e) { console.log('  FAIL  ' + name + ' -> ' + e.message); process.exitCode = 1; }
}

console.log('[ax-mapper test] renderer + engine offline checks');

const inv = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'mock-inventory.json'), 'utf8'));
const md = renderMarkdown(inv);

check('output is a non-empty string', function () { assert.ok(typeof md === 'string' && md.length > 200); });
check('frontmatter carries source-app', function () { assert.ok(md.indexOf('source-app: mockapp') > -1); });
check('custom-attr catalogue lists ShowSummary', function () { assert.ok(md.indexOf('ShowSummary') > -1); });
check('denied control (Logout) flagged YES', function () {
  const line = md.split('\n').find(function (l) { return l.indexOf('Logout') > -1; });
  assert.ok(line && line.indexOf('YES') > -1);
});
check('generic control inventory lists Financials', function () { assert.ok(md.indexOf('Financials') > -1); });
check('per-state error is surfaced', function () {
  assert.ok(md.indexOf('broken-state') > -1 && md.indexOf('ERROR during capture') > -1);
});
check('suggested selector rendered', function () { assert.ok(md.indexOf('button[data-cmd="ShowIncomeStatement"]') > -1); });
check('output is pure ASCII', function () {
  const bad = md.split('').findIndex(function (ch) { return ch.charCodeAt(0) > 127; });
  assert.strictEqual(bad, -1, 'non-ASCII char at index ' + bad);
});

const isDenied = makeIsDenied(['dealing']);
check('core denylist blocks "buy"', function () { assert.strictEqual(isDenied('buyBtn', 'Buy'), true); });
check('adapter extra blocks "dealing"', function () { assert.strictEqual(isDenied('x', 'Dealing'), true); });
check('safe control not denied', function () { assert.strictEqual(isDenied('ShowSummary', 'Summary'), false); });
check('landing/home state NOT falsely denied (post-login regression)', function () {
  const core = makeIsDenied([]);
  assert.strictEqual(core('home', 'Home (post-login landing)'), false);
  assert.strictEqual(core('home-after-login', 'Home (post-login landing)'), false);
});

check('parseArgs reads --adapter/--dry-run', function () {
  const a = parseArgs(['node', 'mapper.js', '--adapter', './adapters/adapter-template.js', '--dry-run']);
  assert.strictEqual(a.dryRun, true);
  assert.strictEqual(a.adapter, './adapters/adapter-template.js');
});
check('parseArgs reads --only', function () {
  const a = parseArgs(['node', 'mapper.js', '--adapter', 'x', '--only', 'a,b']);
  assert.strictEqual(a.only, 'a,b');
});
check('template adapter loads and satisfies contract', function () {
  const adapter = loadAdapter(path.join(__dirname, '..', 'adapters', 'adapter-template.js'));
  assert.strictEqual(adapter.name, 'template-app');
  assert.ok(Array.isArray(adapter.states) && adapter.states.length >= 1);
});
check('sharescope example adapter loads (no side effects on require)', function () {
  const adapter = loadAdapter(path.join(__dirname, '..', 'adapters', 'sharescope.adapter.example.js'));
  assert.strictEqual(adapter.name, 'sharescope');
  assert.strictEqual(adapter.controls.customAttribute, 'data-cmd');
  assert.ok(adapter.states.length >= 14);
});
check('selectStates filters by key (order preserved)', function () {
  const adapter = loadAdapter(path.join(__dirname, '..', 'adapters', 'sharescope.adapter.example.js'));
  const sub = selectStates(adapter, 'home-after-login,chart-view');
  assert.strictEqual(sub.length, 2);
  assert.deepStrictEqual(sub.map(function (s) { return s.key; }), ['home-after-login', 'chart-view']);
});
check('selectStates with no filter returns all', function () {
  const adapter = loadAdapter(path.join(__dirname, '..', 'adapters', 'sharescope.adapter.example.js'));
  assert.strictEqual(selectStates(adapter, null).length, adapter.states.length);
});

console.log('[ax-mapper test] ' + passed + ' checks passed; exit code ' + (process.exitCode || 0));

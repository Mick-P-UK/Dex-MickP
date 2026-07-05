// render-md.js
// ax-mapper - JSON inventory -> Obsidian markdown map (generic).
//
// Reads an inventory object (the authoritative machine record) and emits a
// human-readable markdown map. The generated file is a RENDERED VIEW - never
// hand-edited. Promotion into any canonical reference is a separate, manual,
// diffed step. Output is ASCII-only (vault rule).

'use strict';

// ASCII guard: normalise common curly punctuation, then drop anything else.
// \u escapes keep THIS source file pure ASCII too.
function ascii(text) {
  return String(text == null ? '' : text)
    .replace(/[\u2018\u2019]/g, "'")
    .replace(/[\u201C\u201D]/g, '"')
    .replace(/[\u2013\u2014]/g, '-')
    .replace(/\u2026/g, '...')
    .replace(/[^\x00-\x7F]/g, '');
}

function esc(text) {
  return ascii(text).replace(/\|/g, '\\|');
}

// Consolidated catalogue of every unique custom-attribute control across states.
function buildCustomCatalogue(states) {
  const byVal = {};
  states.forEach(function (s) {
    (s.custom_controls || []).forEach(function (d) {
      if (!d.value) return;
      if (!byVal[d.value]) {
        byVal[d.value] = { value: d.value, label: d.label || '', role: d.role || '', states: [], denied: !!d.denied };
      }
      if (byVal[d.value].states.indexOf(s.state_key) === -1) byVal[d.value].states.push(s.state_key);
      if (!byVal[d.value].label && d.label) byVal[d.value].label = d.label;
    });
  });
  return Object.keys(byVal).sort().map(function (k) { return byVal[k]; });
}

// Consolidated catalogue of every unique generic control (role + name).
function buildControlCatalogue(states) {
  const byKey = {};
  states.forEach(function (s) {
    (s.controls || []).forEach(function (c) {
      if (!c.name) return;
      const key = (c.role || '') + '|' + (c.name || '');
      if (!byKey[key]) byKey[key] = { role: c.role || '', name: c.name || '', states: [] };
      if (byKey[key].states.indexOf(s.state_key) === -1) byKey[key].states.push(s.state_key);
    });
  });
  return Object.keys(byKey).sort().map(function (k) { return byKey[k]; });
}

// Render an inventory object into a markdown string.
function renderMarkdown(inventory) {
  const states = inventory.states || [];
  const today = (inventory.generated_at || new Date().toISOString()).slice(0, 10);
  const sourceApp = inventory.source_app || 'unknown-app';
  const lines = [];

  lines.push('---');
  lines.push('author: AI');
  lines.push('date: ' + today);
  lines.push('source-app: ' + ascii(sourceApp));
  lines.push('output-type: ax-tree-map');
  lines.push('generator: ax-mapper/engine/render-md.js');
  if (inventory.target) lines.push('target: ' + ascii(String(inventory.target)));
  lines.push('---');
  lines.push('');
  lines.push('# ' + ascii(sourceApp) + ' - AX Tree Map (generated)');
  lines.push('');
  lines.push('Generated view of ax-mapper output. Do NOT hand-edit; re-run the mapper.');
  lines.push('States captured: ' + states.length + '. Generated: ' + ascii(inventory.generated_at || today) + '.');
  lines.push('');

  const customCat = buildCustomCatalogue(states);
  if (customCat.length) {
    const attr = inventory.custom_attribute || 'custom-attr';
    lines.push('## Consolidated ' + ascii(attr) + ' catalogue (' + customCat.length + ' unique)');
    lines.push('');
    lines.push('| ' + esc(attr) + ' | Label | Role | Seen in | Denied |');
    lines.push('|---|---|---|---|---|');
    customCat.forEach(function (c) {
      lines.push('| `' + esc(c.value) + '` | ' + esc(c.label) + ' | ' + esc(c.role) +
        ' | ' + c.states.length + ' state(s) | ' + (c.denied ? 'YES' : '') + ' |');
    });
    lines.push('');
  }

  const controlCat = buildControlCatalogue(states);
  lines.push('## Consolidated control inventory (' + controlCat.length + ' unique by role+name)');
  lines.push('');
  lines.push('| Role | Name | Seen in |');
  lines.push('|---|---|---|');
  controlCat.forEach(function (c) {
    lines.push('| ' + esc(c.role) + ' | ' + esc(c.name) + ' | ' + c.states.length + ' state(s) |');
  });
  lines.push('');

  lines.push('## Per-state detail');
  lines.push('');
  states.forEach(function (s) {
    lines.push('### ' + esc(s.state_key));
    if (s.error) {
      lines.push('');
      lines.push('ERROR during capture: ' + esc(s.error));
      lines.push('');
      return;
    }
    lines.push('');
    lines.push('- URL: ' + esc(s.url || ''));
    lines.push('- Screenshot: ' + esc(s.screenshot_path || '(none)'));
    lines.push('- Controls: ' + ((s.controls || []).length) +
      '; custom-attr: ' + ((s.custom_controls || []).length));
    if ((s.suggested_selectors || []).length) {
      lines.push('- Suggested selectors:');
      s.suggested_selectors.slice(0, 40).forEach(function (sel) {
        lines.push('  - `' + esc(sel) + '`');
      });
    }
    lines.push('');
  });

  return ascii(lines.join('\n')) + '\n';
}

module.exports = {
  renderMarkdown: renderMarkdown,
  buildCustomCatalogue: buildCustomCatalogue,
  buildControlCatalogue: buildControlCatalogue,
};

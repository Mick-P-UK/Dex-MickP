# ax-mapper

A generic, **read-only** accessibility-tree mapper for any Playwright-drivable
web app. Log in once, walk a defined set of screens, and at each stop capture the
AX tree, an inventory of every interactive control, an optional custom-attribute
catalogue, a trimmed DOM, and a screenshot. Output: one JSON inventory plus a
generated Obsidian markdown map.

This is the generalised fork of the ShareScope mapper from the
`ax-trees-automation` project. ShareScope is now just one adapter.

## Design: engine + adapter

- `engine/` is app-agnostic and never changes per app.
- `adapters/` holds one small file per target app - the only app-specific code.

To map a new app you write an adapter, not engine code. See
`adapters/adapter-template.js` and the worked `sharescope.adapter.example.js`.

## Quick start

```bash
# 1. Always dry-run first (no browser, safe anywhere)
node engine/mapper.js --adapter ./adapters/adapter-template.js --dry-run

# 2. Live harvest (Desktop, headed browser, needs Playwright + credentials)
node engine/mapper.js --adapter ./adapters/<app>.adapter.js --out ./output

# 3. Offline test the renderer
node test/render.test.js
```

## Outputs

| File | What |
|------|------|
| `output/<app>-inventory.json` | Authoritative machine record |
| `output/<app>-ax-tree-map.generated.md` | Rendered markdown view (never hand-edited) |
| `output/screenshots/<state>.png` | One screenshot per state |

## Safety

- Read-only: a core denylist blocks any control that could change state, spend
  money, or end the session. Adapters may add tokens, not remove them.
- Anti-bot: every step waits a human-paced random delay.
- Credentials live only in an `.env`, read by the adapter - never hardcoded.

## Status

- Engine + renderer: built, offline-tested (dry-run + render).
- ShareScope adapter: example/reference, ported from the project nav table.
  Live harvest is a Desktop task and should be proved one state at a time first.

See `SKILL.md` for how Cedric invokes this.

## ShareScope adapters (two flows)

- `adapters/sharescope.adapter.example.js` - STOCK/instrument screens. Searches a
  ticker (AX_MAPPER_TICKER, default GGP). Maps financials tabs, chart, news + Design.
- `adapters/sharescope-portfolio.adapter.js` - PORTFOLIO flow. NO stock search: logs
  in and goes straight to the portfolio selector, picks a portfolio (AX_MAPPER_PORTFOLIO,
  default "0 - 0 - 2026 - PP1 (UK)"), then holdings / transactions / Export options.

Run the portfolio flow:
```
$env:AX_MAPPER_SHARESCOPE_SKILLS = "C:\Vaults\Cowork\ax-trees-automation\skills"
node engine\mapper.js --adapter .\adapters\sharescope-portfolio.adapter.js --out .\output
```
Notes: run wide (the engine sets 1920x1080) or the rightmost toolbar buttons overflow.
Print-to-PDF is a Chrome/OS dialog and is NOT automatable; use CSV export.

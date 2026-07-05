# AX Mapper Skill

## Trigger Phrases
Use this skill when Mick says any of the following:
- "map [app/site] with ax-mapper"
- "run the ax mapper on [app]"
- "harvest the AX tree for [app/site]"
- "build a UI map / control inventory of [app]"
- "make an adapter for [app] in ax-mapper"
- "/ax-mapper"

---

## Purpose
ax-mapper is a GENERIC, read-only UI cartographer for any Playwright-drivable
web app. It logs into an app once, walks a defined list of screens/states, and
at each stop records the accessibility tree, an inventory of every interactive
control (by role + accessible name), an optional custom-attribute catalogue
(e.g. data-cmd, data-testid), a trimmed DOM, and a screenshot. Output is one
authoritative JSON inventory plus a generated Obsidian markdown map.

It is the generalised fork of the ShareScope mapper (ax-trees-automation
project). The engine is app-agnostic; each target app is one small ADAPTER.

Read-only by design: it only observes. A safety denylist blocks any control that
could change state, spend money, or end the session.

---

## IMPORTANT: Architecture (engine + adapter)
- engine/  - app-agnostic. Never edit per app.
    - mapper.js    orchestrator (open -> walk -> capture -> write -> close)
    - capture.js   four-artefact capture (AX tree, controls, DOM, screenshot)
    - render-md.js JSON inventory -> markdown map (ASCII, Obsidian frontmatter)
    - denylist.js  read-only safety matcher
    - delay.js     human-paced random delays (anti-bot)
- adapters/ - ONE file per app. The only app-specific code.
    - adapter-template.js              copy this to add a new app
    - sharescope.adapter.example.js    worked reference (ShareScope)

An adapter supplies: name, openSession() -> {page, close}, an ordered states[]
list (each with reach()/optional cleanup()), and optional hints
(customAttribute, mainRegionSelector, extra denylist tokens).

---

## Runtime note (where it can run)
- --dry-run works ANYWHERE (no browser, no login). Always run it first to review
  the plan and denylist decisions.
- A LIVE harvest needs Playwright installed and real credentials, so it is a
  Windows/Desktop task with a headed browser. Cedric cannot drive a live browser
  from the Linux sandbox - give Mick the exact command and verify the output.
- Credentials are read from an .env by the adapter's openSession; NEVER hardcode
  a secret in an adapter, script, or doc (single-source rule).

---

## Step 1 - Confirm the target and adapter
Identify the app to map. If an adapter already exists in adapters/, use it. If
not, offer to create one from adapter-template.js (this is the main design work:
deciding which screens/menus/dialogs to visit).

## Step 2 - Dry run (always)
```
cd <path>/skills/ax-mapper
node engine/mapper.js --adapter ./adapters/<app>.adapter.js --dry-run
```
Review the ordered states and confirm nothing is wrongly allowed/denied.

## Step 3 - Live harvest (Desktop, headed)
```
node engine/mapper.js --adapter ./adapters/<app>.adapter.js --out ./output
```
For the ShareScope example, first set:
```
set AX_MAPPER_SHARESCOPE_SKILLS=C:\Vaults\Cowork\ax-trees-automation\skills
set AX_MAPPER_TICKER=GGP
```

## Step 4 - Outputs
- output/<app>-inventory.json          authoritative machine record
- output/<app>-ax-tree-map.generated.md rendered view (never hand-edited)
- output/screenshots/<state>.png        one per state

The generated markdown is a VIEW. Promoting anything into a canonical reference
(e.g. a project's ax-tree-master map) is a separate, manual, diffed step.

---

## Adding a new app (checklist)
1. Copy adapters/adapter-template.js to adapters/<app>.adapter.js.
2. Fill in openSession() (login + landing) and close() (logout + close browser).
3. List the states to visit in states[]; write each reach()/cleanup().
4. Set customAttribute / mainRegionSelector / extra denylist if useful.
5. Dry-run, then a single-state live proof, then the full harvest.

---

## Guardrails
- Read-only: never remove core denylist tokens; the mapper must not click
  send/submit/buy/delete/logout-style controls during the walk.
- Anti-bot: keep the delay helper on every step; never actuate at machine speed.
- ASCII only for any file the skill writes into a vault.
- Test before reporting: run --dry-run (and offline tests) before claiming a
  build works; run a single-state live proof before a full harvest.

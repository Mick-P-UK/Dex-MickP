---
author: AI
date: 2026-07-04
source-app: mockapp
output-type: ax-tree-map
generator: ax-mapper/engine/render-md.js
target: DEMO
---

# mockapp - AX Tree Map (generated)

Generated view of ax-mapper output. Do NOT hand-edit; re-run the mapper.
States captured: 3. Generated: 2026-07-04T09:30:00.000Z.

## Consolidated data-cmd catalogue (3 unique)

| data-cmd | Label | Role | Seen in | Denied |
|---|---|---|---|---|
| `Logout` | Log out | button | 1 state(s) | YES |
| `ShowIncomeStatement` | Income | button | 1 state(s) |  |
| `ShowSummary` | Summary | button | 1 state(s) |  |

## Consolidated control inventory (2 unique by role+name)

| Role | Name | Seen in |
|---|---|---|
| button | Financials | 2 state(s) |
| button | Search | 1 state(s) |

## Per-state detail

### home

- URL: https://mockapp.example/home
- Screenshot: screenshots/home.png
- Controls: 2; custom-attr: 2
- Suggested selectors:
  - `button[data-cmd="ShowSummary"]`

### financials-income

- URL: https://mockapp.example/financials
- Screenshot: screenshots/financials-income.png
- Controls: 1; custom-attr: 1
- Suggested selectors:
  - `button[data-cmd="ShowIncomeStatement"]`

### broken-state

ERROR during capture: reach failed: selector not found


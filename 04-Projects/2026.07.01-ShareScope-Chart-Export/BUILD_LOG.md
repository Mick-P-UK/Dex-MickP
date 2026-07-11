# 2026.07.01 - ShareScope Chart Export - Build Log

Component: sharescope-get-chart skill
Author: Cedric (PAIDA)
Started: 2026.07.01, ~16:50 BST
Goal: 12-month price chart PNG export from ShareScope, to fold into member
reports. Native "Save chart as PNG (Scaled)..." route for a clean image.
Wanted usable for tonight's webinar (19:30 BST).

---

## Design decisions (agreed with Mick)
- Fetch mechanism: headless Playwright script + .env credentials (NOT Claude in
  Chrome - too slow/token-heavy; Chrome is last resort only).
- Capture route: native ShareScope PNG export (cleaner than element screenshot).
- Scope kept simple: 12-month period only for now.
- Skill name: sharescope-get-chart (chosen over sharescope-chart-fetch).
- Small discrete component, callable by any report skill/prompt that needs a chart.
- Reuse the existing 04-Projects\2026.04.04-ShareScope-Automation modules
  (login, search, logout, utils) - do NOT duplicate them.

## Why the runnable code lives in the April project, not here
The new .py modules must sit beside sharescope_login/_search/_logout/_utils so
they can import them. This dated folder is the BUILD RECORD only (spec, log,
pickup). The live code is in:
  C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\

---

## Files created 2026.07.01
1. sharescope_chart.py                (NEW - chart capture module)
     -> April project folder
2. sharescope_chart_orchestrator.py   (NEW - entry point: login>search>chart>logout)
     -> April project folder
3. skills\sharescope-get-chart\SKILL.md   (NEW - skill wrapper)
     -> vault skills folder
4. sharescope_session.py               (NEW - SESSION RUNNER: one login,
     many tickers/tasks, one logout. The standard multi-task entry point and
     the function a report skill imports: run_sharescope_session(...).)
     -> April project folder. Confirmed live 2026.07.01 on HDD (6 CSVs + chart,
     single session, 26s).
5. This build log
     -> 04-Projects\2026.07.01-ShareScope-Chart-Export\

## Files changed
- None. Existing modules reused unchanged.

## Added later in the session (embed work)
6. skills\sharescope-report\SKILL.md   (NEW - v0.1 report skill: session runner
     -> embed 12m chart into the branded template. Financials tables pending.)
7. Sample deliverable: "2026.07.01 - HDD - Stock Research Brief.docx" - chart
     embedded into DIY_Investors_Report_Template.docx, branding preserved.
     Proven end to end. (Built in the agent sandbox; handed to Mick to save.)

## Memory
- Added URGENT task (memory #17, replacing the completed 2025 IC archive note):
  strip the ShareScope password out of plain text in
  skills\sharescope-financials\SKILL.md (and check for the same leak elsewhere).

---

## SELECTORS - CONFIRMED LIVE 2026.07.01 (end-to-end SQZ run)
1. Chart view button: button[data-cmd="ViewChart"]
   (get_by_role name="Chart" matched TWO - the view button + a disabled Graph
    button - so we target the stable data-cmd attribute.)
2. 12-month period control: labelled "1 year" (first candidate hit).
3. Save-as-PNG menu item: "Save chart as PNG (bitmap)..." - NOT "(Scaled)".
   A scaling confirmation dialog appears; the OK click inside expect_download
   handles it. Output PNG ~119 KB for SQZ - a healthy real chart.

All three added to the SKILL.md metadata. TODO: also fold into
ShareScope-Export-Accessibility-Reference.md as a new CHART section.

---

## How to test / run
First (headed) confirmation run:
  1. Set SHARESCOPE_HEADLESS=false in C:\Vaults\Mick's Vault\.env
  2. cd "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation"
  3. python sharescope_chart_orchestrator.py SQZ
  4. Watch: Chart view opens, period set to 1yr, Sharing > Save chart as PNG,
     OK if a scaling dialog appears. Confirm the PNG lands in downloads\SQZ\.
Then flip SHARESCOPE_HEADLESS=true for hands-off use.

---

## PICKUP / next steps
- [x] First headed confirmation run - selectors locked (2026.07.01).
- [x] Skill promoted to v1.0. .env flipped back to headless=true.
- [x] Session runner built + confirmed (sharescope_session.py). One login,
      all tasks, one logout. Use this as the default; single-task orchestrators
      remain as shortcuts. CLI: python sharescope_session.py --chart --financials TICKER
      Import: run_sharescope_session(["TICKER"], do_financials=True, do_chart=True)
- [ ] Fold the three chart selectors into ShareScope-Export-Accessibility-Reference.md.
- [ ] Fix the pre-existing sharescope_logout.py cleanup warnings (logout button
      not found + playwright.stop on None). Non-blocking. Affects whole project,
      so do it deliberately AFTER the webinar - not mid-deadline.
- [ ] Dual-write SKILL.md to /mnt/skills/user/sharescope-get-chart/SKILL.md.
- [x] Wire the docx embed - PROVEN 2026.07.01. sharescope-report skill (v0.1)
      created; sample HDD brief built with chart embedded in the branded template.
- [ ] NEXT: fold the six financial CSVs into the report as summary tables (v0.2).
- [ ] COWORK GOAL: (a) TEST whether Cowork can execute the local headless
      Playwright automation before assuming it - per "Test, Don't Trust".
      (b) Bundle each skill's scripts into its own skill folder so they are
      self-contained/portable rather than pointing at the April project folder.
- [ ] STRETCH: trigger via sharescope_watcher.py for fully unattended runs.
- [ ] Do the URGENT password strip (memory #17).

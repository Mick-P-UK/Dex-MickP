# PICKUP - Next Session
# ax-trees-automation | SS-01: ShareScope Login (JS)

**Created:** 2026-05-01
**Use this file to start the next working session on this project.**

---

## Step 1 -- Paste this into Cowork to start the session

---

Cedric, please pick up the ax-trees-automation project. Mount the folder at:

  C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\ax-trees-automation

Then read these files in order:

1. ax-trees-automation/CLAUDE.md                           (global rules)
2. ax-trees-automation/session-logs/2026-05-01-session.md  (full history)
3. ax-trees-automation/mini-projects/sharescope-login/PROGRESS.md  (what we're building)
4. ax-trees-automation/sharescope/sharescope-ax-tree-master.md     (confirmed selectors)

We are starting mini-project SS-01: writing sharescope-login.js.
Before writing any code, also mount and read:

  C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\sharescope_login.py

That is the working Python version we are rewriting in JavaScript.
When you have read everything, confirm what you know and propose the plan.
Do NOT start coding until we have agreed the approach.

---

## Step 2 -- What Cedric should know after reading those files

### Project summary
ax-trees-automation is a JS/Playwright skill library for DIY Investor automation.
Each automation routine is a mini-project that produces a callable skill in skills/.

### Where we are
- Task 1 (folder structure): COMPLETE
- Task 2 (PRD): COMPLETE
- Task 3 (migration survey): COMPLETE
- Next: SS-01 -- write sharescope-login.js

### What SS-01 needs to do
1. Load credentials from .env (SHARESCOPE_USERNAME, SHARESCOPE_PASSWORD, SHARESCOPE_HEADLESS)
2. Launch Playwright browser (acceptDownloads: true)
3. Navigate to https://webservice.sharescope.co.uk/login.do
4. Fill email, wait 500ms (REQUIRED), fill password, click Login
5. Verify login by checking URL no longer contains 'login'
6. Export the active page object for the next skill to use

### Key rules (from CLAUDE.md)
- Use delay-helper.js for all delays (anti-bot -- mandatory)
- Credentials via process.env only -- never hardcoded
- Full header comment block on every script
- Plan mode first -- agree approach before writing

### Key paths
- Predecessor Python:   04-Projects/2026.04.04-ShareScope-Automation/sharescope_login.py
- AX tree selectors:   ax-trees-automation/sharescope/sharescope-ax-tree-master.md
- Delay helper:        ax-trees-automation/skills/delay-helper.js
- Output skill goes to: ax-trees-automation/skills/sharescope-login.js

---

## Step 3 -- After SS-01 is done

Next mini-project is SS-02 (sharescope-get-metrics.js).
PROGRESS.md is ready at: ax-trees-automation/mini-projects/sharescope-metrics-extraction/PROGRESS.md
Depends on SS-01 being complete first.

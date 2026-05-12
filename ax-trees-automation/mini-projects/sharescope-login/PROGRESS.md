# SS-01: ShareScope Login (JS)
# Mini-Project Progress Tracker

**Output skill:** skills/sharescope-login.js
**Status:** [ ] Not started
**Last updated:** 2026-05-01

---

## Context

A working Python login script exists in the predecessor project:
  04-Projects/2026.04.04-ShareScope-Automation/sharescope_login.py (310 lines)

This mini-project rewrites the login in JavaScript (Node.js + Playwright)
as a proper callable skill. The Python version is the reference -- do not
discard it until the JS version is confirmed working.

---

## What the Skill Must Do

1. Read credentials from .env (SHARESCOPE_USERNAME, SHARESCOPE_PASSWORD, SHARESCOPE_HEADLESS)
2. Launch Playwright browser with correct context (accept_downloads: true)
3. Navigate to https://webservice.sharescope.co.uk/login.do
4. Fill email field
5. Wait 500ms (REQUIRED -- server-side validation needs this)
6. Fill password field
7. Click Login button
8. Wait for URL to leave the login page (timeout: 20s)
9. Verify login succeeded (confirm 'login' absent from URL)
10. Return the active page object for the next skill to use

---

## Selector Reference

All confirmed selectors are in:
  sharescope/sharescope-ax-tree-master.md (Section 1 - Login Page)

Key selectors:
  Email:    page.getByRole('textbox', {name: 'Email:'})
  Password: page.getByRole('textbox', {name: 'Password:'})
  Login:    page.getByRole('button', {name: 'Login'})

---

## Script Requirements (from CLAUDE.md)

- Import randomDelay from skills/delay-helper.js
- Use at minimum the 500ms login delay (see CLAUDE.md anti-bot rules)
- SHARESCOPE_HEADLESS flag must be documented in header comment
- Full header comment block per documentation standard:
    Script name / Purpose / Requires / Produces / Headless note
- Credentials via process.env only -- never hardcoded
- Error screenshot on failure saved to screenshots/debug/

---

## Tasks

- [ ] Read sharescope_login.py from predecessor project (understand the full logic)
- [ ] Write sharescope-login.js to skills/ folder
- [ ] Test: headed mode, confirm login + dashboard visible
- [ ] Test: headless mode, confirm same result
- [ ] Test: deliberate wrong password -- confirm error screenshot saved
- [ ] Update SKILLS-INDEX.md with sharescope-login entry
- [ ] Mark SS-01 as [x] complete in MINI-PROJECTS-MASTER.md

---

## Reference Files

- Predecessor script: 04-Projects/2026.04.04-ShareScope-Automation/sharescope_login.py
- AX tree selectors: sharescope/sharescope-ax-tree-master.md (Section 1)
- Anti-bot delays: skills/delay-helper.js
- .env template: .env.example

---

## Notes / Decisions

*(Add notes here as work progresses)*

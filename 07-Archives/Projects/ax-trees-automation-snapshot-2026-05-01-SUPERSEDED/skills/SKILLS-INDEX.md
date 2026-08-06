# Skills Index - ax-trees-automation

This is the master catalogue of all available automation skills.
An agent or Claude should read this file first to discover what automations are available.

**Last Updated:** 2026-05-01

---

## How to Call a Skill

Skills can be invoked:
- **Verbally**: "Use the sharescope-login skill to log in to ShareScope"
- **By agent**: Import or reference the skill JS file directly
- **Via research agent**: Agent reads this index, identifies the skill, calls it

All skills import delay-helper.js automatically. All skills read credentials from .env.

---

## Shared Utilities

| Skill | File | Purpose |
|-------|------|---------|
| delay-helper | skills/delay-helper.js | Random human-paced delays (anti-bot). Import in every script. |

---

## ShareScope Skills

| Skill | File | Status | Purpose |
|-------|------|--------|---------|
| *(migration pending)* | | | Skills from 04-Projects to be migrated here |

---

## Stockopedia Skills

*(Not yet started)*

---

## Notes

- Skills marked `(migration pending)` exist in 04-Projects/2026.04.04-ShareScope-Automation/
  and will be migrated to this skills/ folder as mini-projects complete.
- When a new skill is added, update this index immediately.
- Include: skill name, file path, status (active/draft/deprecated), one-line purpose.

# AGENTS.md - Master Agent Registry

*The single "who's who" of Mick's AI agents and personas. This is the authoritative list: who each agent is, when they are used, where their definition and any editable rules live. Consult it when you want to know what agents exist or where to change one.*

Owner: Mick (edited jointly with Cedric)
Created: 2026.08.04

**Maintenance rule:** whenever a new named agent or persona is created (or an existing one materially changes), add or update its row here as the FINAL step of that work. A stale registry defeats the purpose.

---

## The research pipeline team

These are the named personas in the ShareScope + NotebookLM research pipeline (SOP #1). Cedric orchestrates; the others are spawned or driven per run.

| Agent | Role | When used | Definition | Editable rules / config | Notes |
|-------|------|-----------|------------|-------------------------|-------|
| **Cedric** | Orchestrator / personal knowledge assistant. Runs tools, manages the workflow and the other agents, saves outputs. | Always - the main assistant persona. | `CLAUDE.md` (user + vault) and `_rules.md`; not a spawnable sub-agent. | `C:\Users\pavey\.claude\CLAUDE.md`, `_rules.md`; vault `CLAUDE.md`. | The "you" in most sessions. |
| **Nina** | Research librarian inside NotebookLM. Builds the notebook, uploads the ShareScope CSVs, runs the news/RNS fast-search. Does NOT write the analysis. | Step 3 of SOP #1, run by the `sharescope_nlm_researcher.py` script. | The researcher script + the notebooklm-* skills. | notebooklm-* skills; pipeline scripts. | Cannot read chart graphics (that is Ron's job). |
| **Ron** (Researcher Ron) | Analyst. Reads Nina's notebook AND the 12-month chart (vision), writes the full structured report + calculations appendix. | Step 4 of SOP #1. `subagent_type: "ron"`. | `.claude\agents\ron.md` (Dex-MickP + Writing-System, kept in sync). | Report template in his agent def; SOP #1. | Signs off as Ron. |
| **Ava** (Ava the Auditor) | Independent verification. Recomputes every calculation from the raw sources, checks units/currency/consistency, returns a verdict. Never rewrites the report. | After the analyst, before issue. `subagent_type: "ava"` (after a Claude Code restart; interim via a general-purpose agent with an inline prompt). | `.claude\agents\ava.md` (Dex-MickP + Writing-System, kept in sync). | `06-Resources\Audit-System\` (rules.md + examples.md + checklists\). Mick edits these anytime. | Signs off as Ava. Built 2026-08-04 from the "Ron Output-checker" idea; first pilot = HOC. Distinct from the calendar Annie. |

## Other named agents and assistants

| Agent | Role | When used | Definition | Notes |
|-------|------|-----------|------------|-------|
| **Annie** | Calendar / scheduling assistant (Google Calendar). Date verification, events, availability. | Any date/schedule/event request. | `annie` skill (`.claude\skills\annie`). | The ORIGINAL Annie - calendar, not audit. Ava (not "Annie the Auditor") is the auditor, to avoid a name clash. |
| **Dex Assistant** | PKM system operations (vault, tasks, weekly review). | Dex/vault/task operations. | Dex skills (`.claude\skills\`). | Part of the PAIDA sub-agent registry. |

## Writing-System task agents

Spawnable agents used for long-form writing work (Writing-System vault):

| Agent | Role | Definition |
|-------|------|------------|
| **article-writer** | Long-form articles. | `Mick's-Writing-System\.claude\agents\article-writer.md` |
| **newsletter-writer** | Email newsletters. | `Mick's-Writing-System\.claude\agents\newsletter-writer.md` |
| **researcher-agent** | Research and synthesis. | `Mick's-Writing-System\.claude\agents\researcher-agent.md` |

---

## Notes on how agent definitions load

- Spawnable agent types (`ron`, `ava`, the writing agents) are defined by markdown files in a vault's `.claude\agents\` folder and are picked up as `subagent_type` options at Claude Code session start - so a NEW agent type is only available after a restart. Until then, spawn via a `general-purpose` agent with an inline prompt.
- Ron and Ava are kept in sync across the Dex-MickP and Writing-System vaults so they are available in either vault's session.
- Ava's rules/checklists deliberately live OUTSIDE her persona file (in `06-Resources\Audit-System\`) so Mick can evolve the audit discipline without touching the agent definition.

## Cross-references

- SOP index: `C:\Vaults\_SOPs\INDEX.md` (SOP #1 = the research pipeline these agents run).
- Ava's home: `06-Resources\Audit-System\` (README, rules, examples, checklists).
- Skills registry: `SKILLS_REGISTRY.md` (skills, as distinct from agent personas).

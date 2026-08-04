# Audit-System - Ava the Auditor

This folder is the home of **Ava the Auditor**, the independent verification agent in Mick's research pipeline. Ava is spawned AFTER an analyst (e.g. Ron) writes a report and BEFORE it is issued; she recomputes every calculation from the raw sources and returns a structured verdict. She never rewrites the report.

## What is here

| File | Purpose | Who edits |
|------|---------|-----------|
| `rules.md` | Global, report-type-agnostic audit rules. The heart of the system. | Mick, anytime |
| `examples.md` | Curated worked examples (one strong one per report type) that calibrate Ava. HOC = example 1. | Mick, when a new pattern is worth teaching |
| `checklists\financial-analysis.md` | Checks specific to a ShareScope + Ron financial analysis. | Mick, anytime |
| `checklists\<other>.md` | Add a file per new report type (technical-analysis, production-analysis, ...). | Mick, when a new report type is audited |

The **persona** (Ava's identity and method) lives separately, in the agent definition `.claude\agents\ava.md` (mirrored in the Writing-System vault, like Ron). The persona rarely changes; the rules pack here is what you evolve.

## How it works

1. Cedric spawns Ava (`subagent_type: "ava"` after a Claude Code restart; interim, via a general-purpose agent with an inline prompt).
2. Ava's FIRST action is to read `rules.md`, `examples.md`, and the checklist for the report type Cedric names.
3. She reads the raw source files, recomputes every figure, checks units/currency/consistency, and returns a verdict (summary, verdict table, material errors, minor notes, consistency, sign-off).
4. Cedric applies any fixes and records the audit (e.g. as Appendix B in the report).

## To evolve the audit

- New general check -> add a rule to `rules.md`.
- New check specific to one report type -> add it to that type's checklist.
- New report type -> add `checklists\<type>.md` and (once audited) a worked example in `examples.md`.
- Nothing else needs changing: Ava re-reads this pack on every run.

## Cross-references

- Master agent registry: `..\AGENTS.md`
- Pipeline SOP this plugs into: SOP #1 in `C:\Vaults\_SOPs\INDEX.md` (ShareScope + NotebookLM + Ron).
- Origin: the "Ron Output-checker" enhancement (Mick, 2026-07-30), first built and piloted as Ava on the HOC run, 2026-08-04.

---
title: NotebookLM Notebook Registry
date_created: 2026.04.28
tags:
  - notebooklm
  - reference
  - research-log
---

# NotebookLM Notebook Registry

This note is a reference map of NotebookLM notebook IDs to company Research Log profiles.
The authoritative ID for each company is stored in its Company Profile YAML frontmatter
(see `Companies/{TICKER} - {Company Name}.md`). This note is a human-readable backup.

**To refresh the full list:** run `notebooklm list` in the project folder and paste
the output here (or ask Cedric to update this note).

Project folder: `C:/Vaults/Mick's-Dex-2nd-Brain/Dex-MickP/04-Projects/2026.04.04-ShareScope-Automation/`

---

## Active Research Log Notebooks (mapped to Company Profiles)

| EPIC | Company | Notebook ID | Notebook Title | Notes |
|------|---------|-------------|----------------|-------|
| SQZ | Serica Energy | `0befe39a-d458-4392-9785-e2d808bafca9` | SQZ - Serica Energy... | Confirmed working 2026.04.28 |
| GGP | Greatland Gold | `7473143f-712f-4d6e-8ccd-e62e194ea087` | GGP - Greatland Gold Analysis_Updated:2026.04.08 | Use THIS one (see note below) |

---

## Duplicate / Retired Notebooks

| EPIC | Notebook ID | Notebook Title | Status |
|------|-------------|----------------|--------|
| GGP | `68ceea40-9423-4f59-8bd0-689283e9e741` | GGP - Greatland Resources | Old notebook - do NOT use. Superseded by the dated one above. |

---

## How Notebook IDs Are Used

1. The pipeline (`sharescope_nlm_researcher.py`) checks the Research Log Company Profile first.
2. If a `nlm_notebook_id` is set in the profile YAML, it uses that ID directly (no search needed).
3. If no ID is set, it searches NotebookLM by ticker name and takes the first match.
4. After creating a new notebook, the ID is saved back to the Company Profile automatically.

**Lesson learned (2026.04.28):** When two notebooks share the same ticker prefix (e.g. both start
"GGP -"), always pre-seed the Company Profile with the correct ID before running the pipeline.
This prevents the wrong notebook being selected.

---

## Full Notebook List (as at 2026.04.28)

Full `notebooklm list` output was captured on 2026.04.28 and contains approximately 160 notebooks.
Key notebooks relevant to the ShareScope pipeline are mapped in the table above.

Run `notebooklm list > notebooks_YYYY.MM.DD.txt` from the project folder to capture a fresh snapshot.

---

_Last updated: 2026.04.28 by Cedric_

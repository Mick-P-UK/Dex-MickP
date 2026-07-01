# Prompts

Human-friendly source library for Mick's reusable AI prompts. These notes are
where prompts are written, developed and versioned. The best of them are
promoted into the single operational file that AutoHotkey and the investing
demos read:

  Operational file: C:\Vaults\Cowork\PROMPT_LIBRARY.md

This folder is the development history. PROMPT_LIBRARY.md is the lean extract.

## How it fits together

- Write and refine a prompt here as a markdown note (one note per prompt).
- Each note carries YAML frontmatter (see _Prompt-Template.md).
- When a prompt is good enough to use operationally, set `operational: true`,
  give it a `code`, and Cedric copies the prompt text into PROMPT_LIBRARY.md.
- The shared `code` (e.g. INV-01, NBLM-02) links a note to its library entry
  both ways, so the two never drift apart silently.

## Frontmatter schema

Every prompt note uses these fields:

| Field        | Purpose                                                       |
|--------------|---------------------------------------------------------------|
| title        | Plain-language name (matches the library Title)               |
| code         | Shared key in CAT-NN form, e.g. INV-01. "TBD" until promoted  |
| category     | One of the fixed list below (matches the library Category)    |
| ahk          | AutoHotkey v1 shortcode e.g. ::us1#, or "none"                |
| version      | X.Y - bump minor for tweaks, major for rewrites               |
| date_created | YYYY.MM.DD - the date the note was made                       |
| date_updated | YYYY.MM.DD - the date the prompt text last changed            |
| status       | draft, active or archived                                     |
| operational  | true once the prompt lives in PROMPT_LIBRARY.md               |
| tags         | Always starts with `prompt`, then free-form keywords          |

## Category vocabulary (shared with PROMPT_LIBRARY.md)

- NBLM - NotebookLM
- INV  - Investment Research
- SUM  - Summarisation
- CON  - Content Creation
- ANL  - Analysis
- COM  - Communication
- WEB  - Webinar / Presentation
- GEN  - General Purpose

## Versioning

- One note per prompt. As a prompt develops, bump `version` and update
  `date_updated` in place. The frontmatter differentiates the iterations.
- For a substantial rewrite worth keeping the old text, copy the superseded
  note into `_archive/` keeping its name, then continue the live note.
- `code` stays stable across all versions of the same prompt, so the indexes
  can group versions together.

## Finding things

- Prompts.base - live Obsidian view. Filter and sort by category, status,
  date and tag. Works inside Obsidian.
- 00-Index.md - generated plain-markdown catalogue. Readable on GitHub and
  anywhere outside Obsidian. Cedric regenerates it when prompts change.

Every prompt note also carries the baseline `prompt` tag, so the existing
"All Notes.base > Prompts" view at the vault root picks them up automatically.

## Sync check

Because every promoted note carries `operational: true` plus a `code`, Cedric
can check on request:

- notes marked operational but missing from PROMPT_LIBRARY.md
- library entries with no source note here
- notes whose `date_updated` is newer than the library copy (drift)

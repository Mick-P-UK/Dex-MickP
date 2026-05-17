---
managed-by: Cedric Server
reloaded: hourly
version: 1.0
last-updated: 2026-05-14
---

# agents.md
# Declarative rule file. Loaded by Cedric Server on startup and reloaded hourly.
# Changes versioned automatically to agents.md-history/ on each reload.
# To force reload without restarting server: GET /agents/reload

---

## Section 1: Data Ingestion and Wiki Processing Rules

# Items dropped into 00-Inbox/raw/ are processed by the hourly worker.
# Processing steps:
#   1. Classify item (note / idea / meeting / reference / task)
#   2. Attempt wiki-linking (match entities in 09-Entities/ and 08-People/)
#   3. Move processed file to 00-Inbox/raw/processed/ (original preserved -- never deleted)
#   4. Write audit line to log.md

ingestion:
  inbox_path: 00-Inbox/raw/
  processed_path: 00-Inbox/raw/processed/
  wiki_link_sources:
    - 09-Entities/Tickers/
    - 09-Entities/Companies/
    - 09-Entities/Concepts/
    - 08-People/
  classification_types:
    - note
    - idea
    - meeting
    - reference
    - task

---

## Section 2: Interactive Journaling Rules
# STUB -- full implementation in Phase 5.
# Trigger words: journal / brainstorm / idea
# Journal files live in: journal/
# Daily notes: Core Daily Notes plugin (Obsidian). Confirmed-blank daily notes deleted by worker before commit.

journaling:
  status: stub
  trigger_words: [journal, brainstorm, idea]
  journal_path: journal/
  daily_notes: obsidian-core-plugin

---

## Section 3: CRM Automation Rules
# STUB -- full implementation in Phase 5.
# People records live in: 08-People/
# Naming convention: YYYY.MM.DD - Firstname Lastname.md
# Every people record must include: private: true in frontmatter

crm:
  status: stub
  people_path: 08-People/
  naming: YYYY.MM.DD - Firstname Lastname.md
  required_frontmatter:
    - private: true

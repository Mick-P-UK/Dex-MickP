# PAIDA Memory System - State of Play

State as at: 2026.06.28 (verified against disk)
Maintained by: Cedric
Canonical location: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\06-Resources\Dex_System\PAIDA_Memory_System_Map.md
Status: living reference - update the "State as at" date when revised

---

## Summary

The PAIDA memory system currently spans FIVE distinct layers. Three live in
the cloud, two live on the PC. Only one of them - CEDRIC_MEMORY.md - is the
canonical anchor. The rest are convenience layers, query layers, or designed
but not yet running.

Key point to hold in mind: these layers are NOT automatically kept in sync
with one another. That is the main architectural risk in the present setup.

---

## Layer 1 - claude.ai / Claude app memory (CLOUD)

- Where: Anthropic servers, tied to Mick's claude.ai account.
- What: a running auto-generated summary of past conversations. This is the
  layer that feeds Cedric context at the start of a session.
- Managed files: none. It regenerates in the background and lags real time
  by design.
- Status: OPERATIONAL, but passive and outside Mick's control.
- Caution: NOT authoritative. Can be incomplete or out of date. Treat it as a
  helpful prompt, never as the record of truth.

## Layer 2 - Notion (CLOUD)

- Where: Notion servers, accessed via Notion MCP.
- What: structured databases.
  - CEDRIC Memory Vault
  - CEDRIC Knowledge Base
  - Micks Content Studio
  - Companies Covered hub (with Radar Log and AI Company Research)
  - CEDRIC Skills Index
- Status: OPERATIONAL as the structured long-term store.

## Layer 3 - NotebookLM (CLOUD)

- Where: Google servers, accessed via NotebookLM MCP (v0.5.16, live).
- What: intended SEARCHABLE QUERY LAYER over content.
- Status: MCP live, but the memory notebooks are NOT yet created.
  - "PAIDA Session Memory" notebook - PLANNED, not created.
  - IC Webinars / Plaza Group / AI-4-Investing notebooks - PLANNED.

## Layer 4 - The Dex vault (PC) - CANONICAL STORE

- Where: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\
- Nature (confirmed from disk):
  - IS an Obsidian vault (.obsidian present)
  - IS Git-backed (.git present) - every write is version controlled
  - Sits NESTED inside a parent Obsidian vault. The parent folder
    Mick's-Dex-2nd-Brain ALSO has its own .obsidian folder, with Dex-MickP as
    a sub-vault inside it. See "Flags" below.
- Physical memory files confirmed present:
  - CEDRIC_MEMORY.md - the cross-session anchor, read at every Desktop session
    start. This is the real working memory.
  - CLAUDE.md, agents.md - operating rules / behaviour
  - CHANGELOG.md, log.md - change history
  - PICKUP_NOTE_2026.04.27.md
  - PICKUP_NOTE_2026.05.04-Poppy.md
  - PICKUP_NOTE_2026.06.03-Skill-Audit.md
  - journal\ - intended dated session-file archive. Currently holds only
    index.md. EFFECTIVELY EMPTY.
  - NotebookLM-Queries\ - one file. Barely used.
  - skills\ - the skill set, mirrored to /mnt/skills/user/ for claude.ai
    sessions (22 skills counted in the mirror).
- Status: OPERATIONAL and authoritative.

## Layer 5 - Ordinary PC folders (PC, NOT vaults)

- Plain Windows folders, not Obsidian vaults:
  - C:\Users\pavey\Documents\0.0 - AI Projects\ (e.g. radar-extractor)
  - C:\Users\pavey\Documents\0.1 - 0.4 (PARA folders)
- Separate Obsidian vaults that exist but are NOT part of PAIDA memory:
  Mick's Vault, DIY-Research, Mick's-Writing-System, Cowork.

---

## Operational today vs planned

OPERATIONAL NOW:
- CEDRIC_MEMORY.md read at session start (working memory)
- Git history of the vault as a permanent audit trail
- PICKUP_NOTE_*.md files for manual session handover
- Notion databases as structured long-term store
- claude.ai cloud memory as a passive convenience feed

DESIGNED BUT NOT YET RUNNING (PAIDA Session Memory Architecture, drafted
April 2026):
- Vault-based DATED SESSION FILES as a permanent archive. The journal\ folder
  exists but is unpopulated, so this is NOT live.
- NotebookLM "PAIDA Session Memory" searchable query layer - not created.
- The /wrap session-end protocol to automate writing session memory - agreed,
  skill NOT built. THIS IS THE KEY MISSING PIECE.
- Five open design questions still unresolved: cadence, Studio note workflow,
  vault folder choice, back-fill, naming convention.

Honest position: memory CAPTURE today is manual and anchor-file-based. The
systematic, searchable session archive is designed but not switched on.

---

## Flags / recommendations

1. NESTED VAULT. A vault inside a vault (Dex-MickP inside Mick's-Dex-2nd-Brain,
   both with .obsidian) can confuse Obsidian and Git (duplicate indexing,
   ambiguous vault root). Worth a deliberate decision about whether Dex-MickP
   should be the single vault root or stay nested.

2. EMPTY journal\ FOLDER. This is the gap between design and reality. If
   session memory matters, the /wrap skill is the missing piece that would
   start populating it. Small, well-scoped build.

---

## Action items

- [ ] BUILD /wrap SKILL - low-hanging fruit to start populating session memory.
      (Reminder set in Cedric memory to prompt Mick every 2-3 days.)
- [ ] Decide nested-vault question (single root vs nested).
- [ ] Create NotebookLM "PAIDA Session Memory" notebook once /wrap is feeding it.
- [ ] Resolve the five open design questions (cadence, Studio note workflow,
      vault folder, back-fill, naming).

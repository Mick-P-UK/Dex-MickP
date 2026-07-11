# MCP: From Helpful to Reliable

**Purpose:** Model Context Protocol (MCP) servers that transform Dex from "mostly works" to "always works" - guaranteed operations, automatic syncing, and deterministic behavior.

**The key insight:** AI is probabilistic by nature. Ask it to do a 5-step task where each step is 85% accurate? Overall success is 0.85^5 = 44%. Less than a coin flip.

**MCP solves this.** Instead of Claude improvising, MCP servers provide guaranteed operations with validation and error handling. Same input, same reliable output. Every time.

---

## The Transformation: Probabilistic to Deterministic

**Without MCP:**
- You: "Create a task to follow up with John"
- Claude: *Guesses format, hopes for the best*
- Result: Maybe correct, maybe duplicates, maybe wrong file, maybe breaks task sync

If you ask Claude to create 10 tasks and each has 85% accuracy? Only ~20% chance all 10 are correct. The system isn't reliable enough to trust.

**With MCP (Work server):**
- You: "Create a task to follow up with John"  
- Claude: Calls `create_task` tool with proper validation
- Result: Task created with unique ID, deduplication checked, synced everywhere automatically

Ask it to create 100 tasks? All 100 work correctly. The system is reliable enough to build on.

**This is the difference between helpful assistant and operating system.**

---

## The Two MCPs That Transform Dex

### Work MCP: Task Sync That Actually Works

**The problem MCP solves:** Traditional systems can't sync tasks across multiple files. Check off a task in your meeting note, but it stays open in Tasks.md and person pages. They get out of sync.

**What Work MCP does:**
- [x] Assigns unique IDs to every task (`^task-20260128-001`)
- [x] Syncs status across ALL locations (meeting notes, Tasks.md, person pages, project files)
- [x] Detects duplicates before creating them
- [x] Enforces priority limits (won't let you overcommit)
- [x] Validates strategic alignment (every task tagged to a pillar)

**In practice:**
```
You: "Mark the proposal task done"
Work MCP:
  -> Finds task ID via fuzzy match
  -> Updates Tasks.md
  -> Updates meeting note where it was created
  -> Updates Sarah's person page
  -> Timestamps: [x]2026-01-28 14:35
```

Check off once, updates everywhere. No manual syncing. No duplicates getting out of sync. One source of truth.

**This is why Python installation is required** - the Work MCP server is the automation engine that makes task management reliable.

### Career MCP: Progression You Can Actually Track

**The problem MCP solves:** Career progression evidence disappears. Six months later you're reconstructing achievements from fragmented memory. Performance reviews become stressful scrambles.

**What Career MCP does:**
- [x] Captures evidence automatically (achievements, feedback, skills demonstrated)
- [x] Maps work to career ladder requirements
- [x] Tracks promotion readiness with gap analysis
- [x] Generates reviews from accumulated evidence, not reconstructed memory
- [x] Links daily work to career goals bidirectionally

**In practice:**
```
You: Run /daily-review
Career MCP:
  -> Detects: "Led migration to new payment system"
  -> Maps to career ladder: "System Design" + "Technical Leadership"
  -> Tags evidence with next-level requirements
  -> Files to career folder automatically

Later:
You: "Generate my self-review"
Career MCP:
  -> Pulls 6 months of accumulated evidence
  -> Organizes by competency
  -> Shows progression narrative
  -> Review ready in 30 seconds
```

**The integration that matters:** Career MCP and Work MCP work bidirectionally. Daily work feeds up (evidence, skills, gaps). Career goals push down (tasks tagged to development areas, quarters aligned to promotion criteria).

Everything compounds toward progression.

---

## Other Included MCPs

| MCP | What It Does | Why It Matters |
|-----|--------------|----------------|
| **Calendar** | Read Apple Calendar events, detect conflicts | Meeting prep knows your day, never books over existing meetings |
| **Granola** | Process meeting transcripts into structured notes | Meeting intelligence without manual note-taking |
| **Onboarding** | Stateful setup with validation and resume | Guided role-based setup that adapts to your answers |
| **Update Checker** | GitHub release detection for `/dex-update` | System stays current without manual checking |
| **Resume Builder** | Stateful resume creation with validation | Build resume through guided conversation, not blank page |

**Learn more:** [Anthropic's MCP Documentation](https://docs.anthropic.com/en/docs/build-with-claude/mcp)

---

## What Goes Here

JSON configuration files that define:
- MCP server connections
- Tool availability and permissions
- Environment variables and settings
- Integration-specific options

## When to Use

Create an MCP config when:
- **External integration** - Connecting to calendar, tasks, CRM, analytics, etc.
- **Specialized tools** - Adding capabilities beyond file operations
- **Live data** - Accessing real-time information from external systems
- **Bidirectional sync** - Reading and writing to external services

## Structure

Each `.json` file in this folder connects one external system (Calendar, Granola meetings, etc.). You don't need to understand the technical details - the `/create-mcp` skill will create these files for you when you want to add a new integration.

## Examples

- **calendar.json** - Apple Calendar integration (events, scheduling)
- **career.json** - Career development (evidence aggregation, ladder parsing, competency analysis)
- **granola.json** - Meeting transcription and processing
- **onboarding.json** - Stateful onboarding with validation (session management, dependency checks, vault creation)
- **resume.json** - Resume builder (stateful resume building, achievement validation, LinkedIn generation)
- **update-checker.json** - GitHub update detection for `/dex-update` (changelog checking, version comparison)
- **work.json** - Task management (create, update, complete tasks)

## External Integrations

Some integrations are **hosted externally** and don't use local config files:

- **Pendo MCP** - Hosted by Pendo with OAuth. Add directly to AI client config (see onboarding Step 8 or https://support.pendo.io/hc/en-us/articles/41102236924955)

## Setup Process

Use `/create-mcp` skill to:
1. Generate MCP server code
2. Create configuration file
3. Test integration
4. Document usage

## Related

- **Reference** (`.claude/reference/mcp-servers.md`) - Technical MCP documentation
- **Core MCP** (`core/mcp/`) - MCP server implementations
- **Skills** (`.claude/skills/create-mcp/`) - MCP creation wizard
- **Integrations** (`06-Resources/Dex_System/Integrations/`) - Integration guides

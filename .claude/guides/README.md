# Guides: How Dex Actually Works

**Purpose:** System conventions, patterns, and best practices that explain how to use Dex effectively. The "how things connect" layer.

**When you'd read guides:** You want to understand how planning works (pillars -> goals -> priorities -> tasks), how person pages aggregate context, or why tasks have unique IDs. Not required for daily use, but illuminating when you're curious.

## What Goes Here

Documentation that explains:
- System conventions (how files are organized, what goes where)
- Patterns across features (how everything connects to pillars)
- Best practices (effective ways to use the system)
- Design decisions (why things work the way they do)

## When to Create a Guide

Add a guide when:
- **System-wide pattern** - Convention applies across multiple features (e.g., "Every piece of work must align to a strategic pillar")
- **Reference needed** - Users or Claude need to look up standards (e.g., "How do I structure a project file?")
- **Conceptual explanation** - Core concept requires more than a command (e.g., "How the planning system works")
- **Architectural context** - Explaining how major components work together (e.g., "How Work MCP keeps tasks in sync")

## Structure

Guides should be:
- **Reference-focused** - Describe what exists, not what to do
- **Evergreen** - Updated as system evolves
- **Scannable** - Use clear headings and examples
- **Linked** - Referenced from CLAUDE.md or flows

## Examples in Dex

Future guides might include:

- **planning-system.md** - How everything connects
  - Strategic Pillars -> Quarter Goals -> Week Priorities -> Daily Plans -> Tasks
  - Why work backwards from career impact
  - How rollup tracking surfaces progress
  
- **person-pages.md** - Relationship intelligence patterns
  - How person pages aggregate meetings, tasks, and context
  - Internal vs External routing (email domain matching)
  - When context injects automatically (hooks + person mentions)
  
- **task-sync.md** - Why unique IDs matter
  - How Work MCP keeps tasks in sync everywhere
  - Deduplication and priority limits
  - Strategic alignment enforcement
  
- **career-tracking.md** - Evidence that compounds
  - How daily work becomes documented progression
  - Career ladder mapping and gap analysis
  - Bidirectional flow: goals push down, evidence feeds up

## Related

- **Reference** (`.claude/reference/`) - Technical implementation details
- **Flows** (`.claude/flows/`) - Step-by-step interactive processes
- **CLAUDE.md** - Core system prompt that references guides

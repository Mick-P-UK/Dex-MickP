# Reference: The Architecture Layer

**Purpose:** Technical deep dives for Claude when building features, developers extending Dex, and curious users who want to understand how it actually works.

**[!] Skip this if you're just using Dex** - the system works perfectly without reading technical docs. This folder is for when you want to build or understand internals.

**When these docs matter:** You want to add a new MCP server, understand why something works the way it does, debug an integration, or contribute to Dex core. Reference docs are the "how it's built" layer.

---

## What Is Reference Documentation?

**Reference docs** explain implementation details and architectural decisions. They're conversation between builders - "here's why we did it this way, here's how to extend it, here are the trade-offs."

**Audience:**
- Claude when implementing new features (reads these to understand patterns)
- Developers extending Dex (learn how to integrate without breaking things)
- Advanced users debugging issues (understand what should happen vs what is happening)
- Contributors understanding the architecture (how pieces fit together)

**Most users don't need these files** - Dex works great without understanding internals. But if you're curious or building, this is where the depth lives.

### Reference vs User Documentation

| Type | Audience | Content | Example |
|------|----------|---------|---------|
| **Reference** | Developers, Claude, advanced users | Technical details, architecture, implementation | "MCP server protocol", "Hook execution order" |
| **User docs** | End users | How to use features | "Run /daily-plan to start your day" |
| **Skills** | End users | Commands and workflows | `/meeting-prep` instructions |

### When Claude Uses Reference Docs

Claude reads reference docs when:
- Implementing new features that integrate with existing systems
- Debugging issues (understanding how something should work)
- Extending functionality (knowing what patterns to follow)
- Setting up integrations (MCP servers, external APIs)

**Example scenario:**
- User: "Add Slack integration to Dex"
- Claude reads: `mcp-servers.md` to understand MCP patterns
- Claude reads: `System/user-profile.yaml` to understand configuration
- Claude implements: New Slack MCP server following established patterns

---

## What Goes Here

Technical reference docs that:
- Explain implementation details
- Document system architecture
- Describe integration patterns
- Define technical specifications

## When to Use

Create reference docs for:
- **Implementation details** - How features work under the hood
- **Integration guides** - Setting up external connections
- **API documentation** - Tool interfaces and parameters
- **Architecture decisions** - Why things work the way they do

## Audience

Reference docs are for:
- Claude when implementing features
- Developers extending Dex
- Advanced users customizing their setup
- Contributors debugging issues

## Structure

Reference docs should:
- Be technically precise
- Include code examples
- Link to related files
- Explain trade-offs and decisions

## Examples in Dex

- **mcp-servers.md** - MCP architecture deep dive
  - How Work MCP achieves task sync across all files
  - Why Career MCP uses bidirectional mapping
  - Integration patterns for building new MCP servers
  
- **meeting-intel.md** - Meeting processing pipeline
  - How Granola transcripts become structured notes
  - Action item extraction and routing logic
  - Person page update triggers
  
- **demo-mode.md** - Demo mode architecture
  - How sample data demonstrates all 8 Jobs to Be Done
  - Why demo runs in System/Demo/ (isolation from real vault)
  - Reset and cleanup implementation

## Related

- **MCP** (`.claude/mcp/`) - MCP server configurations
- **Core** (`core/`) - Implementation code

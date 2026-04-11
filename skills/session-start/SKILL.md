# Session Start Skill

## Purpose
Mandatory environment detection at the start of every session.

## Protocol
1. Call tool_search with a generic query (e.g. "list") as an MCP environment probe
2. SUCCESS (tools returned) = Claude Desktop - announce: "Running in Claude Desktop - full MCP confirmed"
3. FAILURE = claude.ai - announce: "Running in claude.ai - MCP unavailable"
4. NEVER assume or guess - always probe first

## Why tool_search?
tool_search works regardless of which specific MCPs are installed. It is always available in Claude Desktop and always absent in claude.ai, making it the most reliable probe.

## Announcement Format
- Desktop: "Running in **Claude Desktop - full MCP confirmed** [checkmark]"
- claude.ai: "Running in **claude.ai - MCP unavailable**"

## After Announcement
Proceed with the session normally. No further environment checks needed.

## Reminder: Dual-Deploy Protocol (2026.04.11)
Whenever a skill is created or updated during this session, BOTH locations must be updated:
- Vault master: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\<skill-name>\
- MCP mirror: /mnt/skills/user/<skill-name>/
Do not declare any skill complete until both copies are confirmed. See CEDRIC_MEMORY.md for full protocol.

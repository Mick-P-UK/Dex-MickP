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

## NotebookLM Auth Recovery Protocol (2026.04.20)

When any notebooklm-mcp tool returns an authentication error, follow this standard recovery pattern:

### Important: bash_tool is always Linux
bash_tool runs in a Linux container in ALL environments (Claude Desktop AND claude.ai web).
It cannot reach Windows-installed tools like nlm.exe regardless of session environment.
Filesystem MCP confirms Claude Desktop, but that does NOT mean bash_tool has Windows access.

### Recovery steps (ALL environments):
1. Detect the failure (error message contains "Authentication expired" or similar)
2. Tell Mick: "NLM auth has expired - please run 'nlm login' in a PowerShell terminal on your Windows machine. A browser window will open - just click through, then let me know."
3. Wait for Mick to confirm login is complete
4. Call notebooklm-mcp:refresh_auth to pick up the new tokens
5. Retry the original notebooklm action

This requires ONE action from Mick (run nlm login in PowerShell + click through browser OAuth).

NOTE: nlm is a Python package installed on Windows. Claude cannot invoke it directly.
NOTE: nlm login is an interactive browser OAuth flow - Claude cannot complete the Google sign-in step itself.

## Reminder: Dual-Deploy Protocol (2026.04.11)
Whenever a skill is created or updated during this session, BOTH locations must be updated:
- Vault master: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\<skill-name>\
- MCP mirror: /mnt/skills/user/<skill-name>/
Do not declare any skill complete until both copies are confirmed. See CEDRIC_MEMORY.md for full protocol.

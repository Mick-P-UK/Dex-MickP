# MCP Configuration Fix Investigation

**Date:** 2026-02-15
**Issue:** Claude Code CLI not loading project MCPs
**Root Cause:** Architecture mismatch between Dex system and Claude Code CLI

---

## Problem Summary

**What's broken:**
- ALL 8 Dex core MCPs (work, calendar, granola, career, dex-improvements, resume, update-checker, onboarding)
- NotebookLM MCP cannot be added using current setup
- Dex fundamental functionality non-operational (tasks, planning, calendar, meetings)

**Why it's broken:**
- **Dex assumption:** Claude Code CLI reads project `.mcp.json`
- **Reality:** Claude Code CLI reads `~/.claude.json` (user-level config)
- **Current state:** `~/.claude.json` has empty MCP config for this project
- **Evidence:** gdrive MCP works because it's in user-level config, project MCPs don't

---

## Key Discovery: `/dex-add-mcp` Skill Already Exists!

**Finding:** Dex has a `/dex-add-mcp` skill (`.claude/skills/dex-add-mcp/SKILL.md`) that:
- Recommends **user scope by default** (exactly what we need!)
- States: "Add MCP server without touching `.mcp.json`"
- Documents both `--scope user` and `--scope project` options
- Says user scope "survives Dex updates and applies across all projects"

**The problem:**
- `/dex-add-mcp` skill exists for adding NEW MCPs
- But Dex's OWN core MCPs (work, calendar, granola, etc.) were installed in project `.mcp.json`
- Project `.mcp.json` isn't being read by Claude Code CLI
- Result: Dex core MCPs broken, even though Dex documents the correct approach!

**The solution:** Re-register all Dex core MCPs using user scope (as `/dex-add-mcp` recommends)

---

## Solution Options

### Option 1: Use `claude mcp add` Commands (RECOMMENDED - Matches `/dex-add-mcp` approach)

**Approach:** Register each project MCP at user-level using official CLI commands

**Commands to run (AFTER this Claude session exits):**

```bash
# Work MCP
claude mcp add --scope user work-mcp python "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\core\mcp\work_server.py"

# Calendar MCP
claude mcp add --scope user calendar-mcp python "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\core\mcp\calendar_server.py"

# Granola MCP
claude mcp add --scope user granola-mcp python "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\core\mcp\granola_server.py"

# Career MCP
claude mcp add --scope user career-mcp python "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\core\mcp\career_server.py"

# Dex Improvements MCP
claude mcp add --scope user dex-improvements-mcp python "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\core\mcp\dex_improvements_server.py"

# Resume MCP
claude mcp add --scope user resume-mcp python "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\core\mcp\resume_server.py"

# Update Checker
claude mcp add --scope user update-checker python "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\core\mcp\update_checker.py"

# Onboarding MCP
claude mcp add --scope user onboarding-mcp python "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\core\mcp\onboarding_server.py"

# NotebookLM MCP (the original goal!)
claude mcp add --scope user notebooklm-mcp "C:\Users\pavey\.local\bin\notebooklm-mcp.exe"
```

**Note:** Each MCP needs environment variable `VAULT_PATH` set. May need to add `--env` flag:
```bash
claude mcp add --scope user work-mcp python "..." --env VAULT_PATH="C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP"
```

**Pros:**
- ✅ Uses official Claude Code CLI API
- ✅ Properly updates `~/.claude.json`
- ✅ Should work immediately
- ✅ Commands are idempotent (can run multiple times safely)

**Cons:**
- ⚠️ Manual process (9 commands to run)
- ⚠️ Need to verify exact command syntax
- ⚠️ Need to confirm how to pass environment variables

**Testing steps:**
1. Exit this Claude Code session
2. Run the commands above in PowerShell/terminal
3. Restart Claude Code CLI
4. Check if MCP tools are available

---

### Option 2: Manually Edit `~/.claude.json`

**Approach:** Copy MCP config from project `.mcp.json` into `~/.claude.json` project section

**File to edit:** `C:\Users\pavey\.claude.json`

**Section to update (lines 411-471):**
```json
"C:/Vaults/Mick's-Dex-2nd-Brain/Dex-MickP": {
  "allowedTools": [],
  "mcpContextUris": [],
  "mcpServers": {
    "work-mcp": {
      "type": "stdio",
      "command": "python",
      "args": ["C:\\Vaults\\Mick's-Dex-2nd-Brain\\Dex-MickP\\core\\mcp\\work_server.py"],
      "env": {
        "VAULT_PATH": "C:\\Vaults\\Mick's-Dex-2nd-Brain\\Dex-MickP"
      }
    },
    "calendar-mcp": { ... },
    "granola-mcp": { ... },
    // ... all other MCPs
  },
  "enabledMcpjsonServers": [
    "work-mcp",
    "calendar-mcp",
    "granola-mcp",
    "career-mcp",
    "dex-improvements-mcp",
    "resume-mcp",
    "update-checker",
    "onboarding-mcp",
    "notebooklm-mcp"
  ],
  ...
}
```

**Pros:**
- ✅ Direct control over configuration
- ✅ Can copy entire MCP definitions from project `.mcp.json`
- ✅ One-time edit

**Cons:**
- ❌ Manual JSON editing (error-prone)
- ❌ Need to escape backslashes properly
- ❌ May conflict with Claude Code CLI's config management
- ❌ Might get overwritten by CLI

---

### Option 3: Test `--scope project` Flag

**Approach:** Try using `--scope project` instead of `--scope user`

**Command to test:**
```bash
claude mcp add --scope project work-mcp python "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\core\mcp\work_server.py"
```

**Pros:**
- ✅ Would update `~/.claude.json` project-specific config
- ✅ Keeps MCPs scoped to this project only
- ✅ Uses official CLI

**Cons:**
- ⚠️ Unknown if `--scope project` is supported
- ⚠️ Documentation only mentions `--scope user`
- ⚠️ May fail with "unknown scope" error

**Testing steps:**
1. Exit this Claude session
2. Try one command with `--scope project`
3. If it fails, fall back to Option 1
4. If it works, run for all MCPs

---

## Recommended Approach

**Phase 1: Quick Test (5 minutes)**
1. Exit Claude Code CLI session
2. Test `--scope project` for one MCP:
   ```bash
   claude mcp add --scope project work-mcp python "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\core\mcp\work_server.py"
   ```
3. Check if it updated `~/.claude.json` project config
4. Restart Claude and test if work-mcp tools are available

**Phase 2: Full Migration (15-20 minutes if Phase 1 works)**
- Run `claude mcp add --scope project` for all 8 Dex MCPs
- Run `claude mcp add --scope user` for NotebookLM MCP (since it's not project-specific)
- Restart Claude Code CLI
- Verify all 9 MCPs are loaded

**Phase 3: Fallback (if Phase 1 fails)**
- Use `--scope user` for all MCPs (Option 1)
- Accept that MCPs will be user-level, not project-specific
- Document this as the correct Dex installation method

---

## Environment Variable Handling

**All Dex MCPs need:** `VAULT_PATH` environment variable

**Check if `claude mcp add` supports `--env` flag:**
```bash
claude mcp add --help | grep env
```

**If `--env` is NOT supported:**
- May need to use absolute paths that don't require VAULT_PATH
- Or manually edit `~/.claude.json` to add env vars after running commands

---

## Verification Checklist

After running commands, verify:
- [ ] Check `~/.claude.json` - should have MCPs in project config OR user-level config
- [ ] Restart Claude Code CLI in project directory
- [ ] Run `ToolSearch("work")` - should find work-mcp tools
- [ ] Run `ToolSearch("notebooklm")` - should find NotebookLM tools
- [ ] Try creating a task with work-mcp
- [ ] Try listing NotebookLM notebooks

---

## Long-Term Fix for Dex System

**Issue:** Dex installation assumes project `.mcp.json` works, but it doesn't for Claude Code CLI

**Fix needed in Dex distribution:**
1. Update `install.sh` / installation script to use `claude mcp add` commands
2. OR provide post-install instructions: "Run these commands to enable MCPs"
3. Update documentation to explain user-level vs project-level MCP config
4. Add to Dex Technical Guide: "Claude Code CLI Configuration"

**Affects:** Potentially all Dex users running Claude Code CLI

---

## Next Steps

**Immediate (this session):**
1. ✅ Log all findings
2. ✅ Create this investigation document
3. ⏳ Present findings and recommendation to user

**After this session (user actions):**
1. ⏳ Exit Claude Code CLI
2. ⏳ Test `claude mcp add --scope project` (Phase 1)
3. ⏳ Run full migration commands (Phase 2)
4. ⏳ Restart Claude and verify all MCPs load
5. ⏳ Report back findings

**Future (Dex system improvements):**
1. ⏳ Update Dex installation to use `claude mcp add` commands
2. ⏳ Document this issue for other users
3. ⏳ Consider filing feature request with Claude Code team for better project `.mcp.json` support

---

**Created by:** Cedric (Claude Code AI Assistant)
**Related:** `System/Debug_Logs/2026-02-15-NotebookLM-MCP-Setup.md` (full troubleshooting log)

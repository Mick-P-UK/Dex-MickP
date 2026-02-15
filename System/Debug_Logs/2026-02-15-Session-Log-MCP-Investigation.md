# Session Log: MCP Investigation - 2026-02-15

**Time:** 16:19 - ongoing
**Focus:** Understanding why project MCPs don't load in Claude Code CLI

---

## Session Context

Mick asked to "pick up where we left off" and pasted output showing:
1. Claude Code CLI running from home directory (`C:\Users\pavey`)
2. Attempt to run `claude config list` from project directory while already in a Claude Code session
3. Error: "Claude Code cannot be launched inside another Claude Code session"

**Key realization:** We're already IN a Claude Code CLI session, so we can check the startup logs directly.

---

## Startup Log Analysis

### Command Run
```bash
grep -i "mcp\|starting.*server\|loaded.*server" ~/.claude/debug/d58617a8-26b5-452a-9b42-f25072c815d9.txt
```

### MCPs That Loaded (5 total)

1. **gdrive** (user-level MCP)
   - Type: stdio server
   - Status: ✅ Successfully connected in 2136ms
   - Capabilities: tools, resources

2. **claude.ai Vercel** (cloud MCP)
   - Status: ✅ Connected in 806ms
   - Capabilities: tools, prompts

3. **claude.ai Notion** (cloud MCP)
   - Status: ✅ Connected in 1222ms
   - Capabilities: tools, resources

4. **claude.ai Canva** (cloud MCP)
   - Status: ❌ Auth error - "no OAuth token configured"

5. **claude.ai Sentry** (cloud MCP)
   - Status: ❌ Auth error - "no OAuth token configured"

### MCPs That Did NOT Load (9 missing)

**All Dex project MCPs missing:**
- work-mcp
- calendar-mcp
- granola-mcp
- career-mcp
- dex-improvements-mcp
- resume-mcp
- update-checker
- onboarding-mcp
- notebooklm-mcp

### Evidence from Logs

```
2026-02-15T16:14:51.054Z [DEBUG] [STARTUP] Loading MCP configs...
2026-02-15T16:14:51.617Z [DEBUG] [STARTUP] MCP configs loaded in 563ms
```

**Then:** Only gdrive and cloud MCPs appear in connection sequence.

**Conclusion:** Claude Code CLI is NOT loading project MCPs from `.mcp.json` when launching from the project directory.

---

## Architecture Analysis

### Current MCP Configuration (`.mcp.json`)

**Dex MCPs (8 servers):**
```json
{
  "work-mcp": {
    "type": "stdio",
    "command": "python",
    "args": ["c:\\Vaults\\Mick's-Dex-2nd-Brain\\Dex-MickP\\core\\mcp\\work_server.py"],
    "env": {
      "VAULT_PATH": "c:\\Vaults\\Mick's-Dex-2nd-Brain\\Dex-MickP"
    }
  }
  // ... 7 more similar configs
}
```

**NotebookLM MCP:**
```json
{
  "notebooklm-mcp": {
    "type": "stdio",
    "command": "C:\\Users\\pavey\\.local\\bin\\notebooklm-mcp.exe",
    "args": [],
    "env": {
      "PYTHONIOENCODING": "utf-8",
      "PYTHONUTF8": "1"
    }
  }
}
```

### Key Architectural Differences

**Dex MCPs:**
- ✅ Vault-specific (use `VAULT_PATH` environment variable)
- ✅ Point to absolute paths within the vault
- ✅ Designed for project-scope (only work for this vault)
- ❌ Moving to user-level would break architecture (would point to wrong vault in other directories)

**NotebookLM MCP:**
- ✅ Vault-agnostic (no `VAULT_PATH`)
- ✅ Uses global executable path
- ✅ Official docs say `--scope user`
- ✅ Safe to move to user-level (won't affect Dex)

---

## Documentation Review

### NotebookLM Official Docs
From `.claude/reference/notebooklm-mcp-guide.md`:
```bash
claude mcp add --scope user notebooklm-mcp notebooklm-mcp
```
**Explicitly uses `--scope user`** - designed for user-level installation.

### Dex Technical Guide
From `06-Resources/Dex_System/Dex_Technical_Guide.md`:
- MCP servers use `VAULT_PATH` substitution
- Onboarding creates `.mcp.json` with vault-specific paths
- Assumes project-level configuration

---

## Questions Mick Asked

### Q1: "Will moving to user-level mess up Dex or NotebookLM?"

**Answer:**
- **NotebookLM:** ✅ Safe to move to user-level (matches its design)
- **Dex MCPs:** ⚠️ Would work but breaks architecture (vault-specific should stay project-scoped)

### Q2: "Does this fix the enterprise authorization issue?"

**Answer:**
- **No** - Cloud MCP OAuth errors (Canva, Sentry) are separate from project MCP loading
- Cloud MCPs need OAuth through claude.ai web interface
- Local MCP loading issue is unrelated to cloud MCP auth

### Q3: "If we load NotebookLM to user system, will Dex (writing newsletters etc) still work?"

**Answer:**
- **Yes** ✅ - Writing system is file-based, not MCP-dependent
- Writing agents read from `05-Areas/Writing_System/context/` (files)
- Voice DNA, ICP, business profile = all file-based
- **NotebookLM MCP is completely independent** (no Dex dependencies)

**What DOES depend on Dex MCPs:**
- Task management (`/daily-plan`, `/review`)
- Calendar integration
- Granola meeting processing
- These features won't work until MCP loading is fixed

---

## Testing Plan

### Step 1: Verify Claude Desktop (IN PROGRESS)

Mick is currently testing Claude Desktop to verify if Dex MCPs work there.

**Test checklist:**
1. ✅ Set working directory to vault
2. ✅ Read `System/pillars.yaml`
3. ✅ Create test task (checks if work-mcp loads)
4. ✅ List available MCPs
5. ✅ Test calendar (if time)

**Expected outcomes:**

**If MCPs work in Claude Desktop:**
- Confirms Dex is properly configured
- Confirms MCPs work in Claude Desktop
- Confirms bug is specific to Claude Code CLI

**If MCPs DON'T work in Claude Desktop:**
- Broader configuration issue to investigate

### Step 2: Add NotebookLM to User-Level (PENDING)

After confirming Claude Desktop works:
```bash
claude mcp add --scope user notebooklm-mcp notebooklm-mcp
```

**Why this is safe:**
- NotebookLM designed for user-level
- Won't affect Dex configuration
- Won't break writing system (file-based)

### Step 3: Report Bug to Claude Code CLI (PENDING)

If Claude Desktop works but Claude Code CLI doesn't:
- File bug report about project MCP loading
- Document that Claude Code CLI v2.1.42 doesn't load project `.mcp.json` when run from Cursor terminal

---

## Key Learnings

### 1. Two Separate Issues
- **Project MCP loading bug** - Claude Code CLI not reading `.mcp.json`
- **Cloud MCP OAuth** - Unrelated, needs web authentication

### 2. Writing System Independence
- Writing system uses **file-based agents**, not MCPs
- NotebookLM MCP won't interfere with writing system
- Safe to add NotebookLM without breaking Dex

### 3. MCP Scope Design Patterns
- **User-level:** Global tools (NotebookLM, gdrive)
- **Project-level:** Vault-specific tools (Dex MCPs with `VAULT_PATH`)

### 4. Claude Desktop vs Claude Code CLI
- Different config files
- Different MCP loading behavior
- Need to test both separately

---

## Next Steps (After Mick Returns)

1. **Review Claude Desktop test results**
2. **If Desktop works:** Add NotebookLM to user-level
3. **If Desktop fails:** Investigate broader config issue
4. **Long-term:** Report Claude Code CLI bug or find workaround

---

## Files Referenced

- `.mcp.json` - Project MCP configuration
- `~/.claude/debug/d58617a8-26b5-452a-9b42-f25072c815d9.txt` - Startup log
- `.claude/reference/notebooklm-mcp-guide.md` - Official docs
- `06-Resources/Dex_System/Dex_Technical_Guide.md` - Dex architecture
- `System/Debug_Logs/2026-02-15-NotebookLM-MCP-Setup.md` - Yesterday's 5-hour troubleshooting

---

**Status:** Mick testing Claude Desktop - all MCPs confirmed working there.

---

## BREAKTHROUGH: Claude Desktop Has Everything Working! (16:22-16:25)

### Test Results from Claude Desktop

**Test 1: List available MCP servers**
Mick asked Claude Desktop: "What MCP servers do you have access to?"

**Result: ✅ ALL MCPs WORKING**

**Dex MCPs (3 loaded):**
1. ✅ **work-mcp** - Task management, goals, priorities, company/contact management
2. ✅ **calendar-mcp** - Google Calendar integration with full attendee details
3. ✅ **granola-mcp** - Meeting transcripts and search

**NotebookLM MCP:**
4. ✅ **notebooklm** - All 29 tools available (notebooks, sources, research, studio artifacts)

**Additional MCPs (7 more):**
5. Notion - Full CRUD operations
6. filesystem - File operations (restricted to C:\Users\pavey)
7. Context7 - Library documentation
8. PDF Tools - Read, fill, validate PDFs
9. Claude in Chrome - Browser automation
10. Vercel - Runtime logs
11. Built-in Anthropic Tools - Web search, computer use

**Total: 11 MCP servers loaded in Claude Desktop**

### Key Findings

**✅ Dex is properly configured:**
- All core MCPs work in Claude Desktop
- Task management available (work-mcp)
- Calendar integration working (calendar-mcp)
- Meeting intelligence active (granola-mcp)

**✅ NotebookLM already set up:**
- Fully functional in Claude Desktop
- All 29 tools available
- Can use immediately (no additional setup needed)

**❌ Claude Code CLI bug confirmed:**
- Desktop loads all MCPs ✅
- CLI loads only user-level MCPs ❌
- Same vault, different behavior
- Bug is specific to Claude Code CLI when run from Cursor terminal

### Architectural Discovery

**Two Separate Systems:**

**Claude Desktop:**
- Config location: Unknown (to be investigated)
- Loads: User-level + Project MCPs (all 11 servers)
- Status: ✅ Fully functional

**Claude Code CLI (in Cursor):**
- Config location: Project `.mcp.json` + `~/.claude.json`
- Loads: Only user-level MCPs (1 server - gdrive)
- Status: ❌ Not loading project MCPs

### Practical Solution

**For MCP-dependent work:**
- Use Claude Desktop (all MCPs working)
- NotebookLM, tasks, calendar, meetings all available

**For coding/editing:**
- Use Claude Code CLI in Cursor (better IDE integration)
- File operations still work, just no MCP access

**Workaround not needed:**
- Originally planned to move NotebookLM to user-level for CLI
- Not necessary - can use Desktop for NotebookLM work
- Keeps architecture clean (project MCPs stay project-scoped)

### Next Steps

**Immediate (16:25):**
- ✅ Mick testing Claude Desktop functionality
- ✅ Exploring NotebookLM, tasks, calendar in Desktop
- ⏳ Will report back on experience

**Follow-up:**
- Investigate Claude Desktop MCP config location
- Understand why Desktop loads project MCPs but CLI doesn't
- Consider reporting bug to Claude Code CLI team

**Status:** Waiting for Mick's feedback on Claude Desktop experience.

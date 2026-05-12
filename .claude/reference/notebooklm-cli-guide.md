# NotebookLM CLI Guide - VERIFIED

**Verified:** 2026.04.28 via `nlm_help_check.py` against installed binary
**Binary name:** `notebooklm` (NOT `nlm` - the old guide was for a different tool)
**Note:** A previous version of this guide documented a different tool (`nlm`).
Everything below is confirmed against what is actually installed.

---

## Quick Start

```
notebooklm login              # Authenticate first
notebooklm list               # List your notebooks
notebooklm create "My Notes"  # Create a notebook
notebooklm ask "Hi"           # Ask the current notebook a question
```

---

## Global Options

```
--version       Show version
--storage PATH  Path to storage_state.json (default: C:\Users\pavey\.notebooklm\storage_state.json)
-v, --verbose   Increase verbosity (-v INFO, -vv DEBUG)
--help
```

---

## Session Commands

```
notebooklm login                    # Authenticate via browser
notebooklm use <NOTEBOOK_ID>        # Set active notebook (supports partial IDs)
notebooklm status                   # Show current notebook + conversation context
notebooklm clear                    # Clear current notebook context
```

---

## Notebook Commands

```
notebooklm list                     # List all notebooks
notebooklm create "Title"           # Create a notebook
notebooklm delete <id>              # Delete a notebook
notebooklm rename <id> "New Title"  # Rename a notebook
notebooklm summary                  # AI-generated notebook summary
```

---

## Source Commands

### Add Sources

```
notebooklm source add <CONTENT>              # Auto-detects type
notebooklm source add https://example.com   # URL source
notebooklm source add ./doc.md              # File (text)
notebooklm source add "My notes here"       # Inline text
notebooklm source add "text" --title "Name" # Text with title
```

**source add options:**
```
-n, --notebook TEXT             Notebook ID (uses current if not set)
--type [url|text|file|youtube]  Override auto-detection
--title TEXT                    Title for text sources
--mime-type TEXT                MIME type for file sources
--json                          JSON output
```

**CONFIRMED WORKING in pipeline:**
- `notebooklm source add <filepath.txt> --title "Title"` - uploads file as text source
- No --wait flag (use `notebooklm source wait` separately if needed)
- No --text flag (pass inline text as positional arg, or write to file first)

### Research / Web Search (Fast Search)

**Correct workflow - confirmed from CLI help:**

```bash
# Start research (non-blocking)
notebooklm source add-research "query" --mode fast --no-wait

# Wait for completion and import all sources
notebooklm research wait --import-all
```

OR blocking (waits automatically):
```bash
notebooklm source add-research "query" --mode fast
```

Modes: `fast` (quick), `deep` (thorough)

### Other Source Commands

```
notebooklm source list              # List all sources in current notebook
notebooklm source get <id>          # Get source details
notebooklm source fulltext <id>     # Get full indexed text
notebooklm source guide <id>        # AI-generated source summary + keywords
notebooklm source stale <id>        # Check if URL source needs refresh
notebooklm source refresh <id>      # Refresh a URL/Drive source
notebooklm source delete <id>       # Delete a source
notebooklm source delete-by-title "Title"  # Delete by exact title
notebooklm source rename <id> "New Title"  # Rename a source
notebooklm source wait <id>         # Wait for source to finish processing
notebooklm source add-drive <url>   # Add Google Drive document
```

---

## Chat / Ask

```
notebooklm ask "question"                        # Ask using current notebook + conversation
notebooklm ask "question" --new                  # Start a fresh conversation
notebooklm ask "question" -c <conversation_id>   # Continue a specific conversation
notebooklm ask "question" -s <source_id>         # Limit to specific source(s)
notebooklm ask "question" --json                 # Structured output with source references
notebooklm ask "question" --save-as-note         # Save response as a note
notebooklm ask "question" --save-as-note --note-title "Title"
```

**ask options:**
```
-n, --notebook TEXT         Notebook ID (uses current if not set)
-c, --conversation-id TEXT  Continue a specific conversation
-s, --source TEXT           Limit to source IDs (repeatable)
--json                      Output as JSON (includes references)
--save-as-note              Save response as a note
--note-title TEXT           Note title (with --save-as-note)
```

---

## Research Commands (monitoring only)

```
notebooklm research status             # Check research status (non-blocking)
notebooklm research wait               # Wait for research to complete
notebooklm research wait --import-all  # Wait AND import all discovered sources
```

Note: Use `notebooklm source add-research` to START research.
The `research` command group is only for monitoring.

---

## Artifact Generation

```
notebooklm generate audio
notebooklm generate report
notebooklm generate quiz
notebooklm generate flashcards
notebooklm generate slide-deck
notebooklm generate infographic
notebooklm generate mind-map
notebooklm generate data-table
notebooklm generate video
notebooklm generate cinematic-video
```

---

## Notes

```
notebooklm note create "Title" "Content"
notebooklm note list
notebooklm note get <id>
notebooklm note rename <id> "New Title"
notebooklm note delete <id>
notebooklm note save
```

---

## Sharing

```
notebooklm share public
notebooklm share add <email>
notebooklm share remove <email>
notebooklm share status
```

---

## Pipeline Usage Notes (ShareScope)

Commands confirmed working in `sharescope_nlm_researcher.py`:

```python
# Set notebook context
run_nlm(["use", notebook_id])

# Upload CSV as text source (temp file approach - CORRECT)
run_nlm(["source", "add", tmp_path, "--title", source_title])

# Ask a question
run_nlm(["ask", prompt])

# Fast search for news (Step 2.5)
run_nlm(["source", "add-research", query, "--mode", "fast", "--no-wait"])
run_nlm(["research", "wait", "--import-all"])
```

**Flags that do NOT exist in this version:**
- `--text` (on source add) - pass inline text as positional arg instead
- `--wait` (on source add) - use `notebooklm source wait <id>` separately
- `research start` - use `source add-research` instead
- `research import` - use `research wait --import-all` instead

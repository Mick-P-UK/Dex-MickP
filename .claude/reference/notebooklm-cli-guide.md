# NotebookLM CLI Guide

**Source:** https://github.com/jacob-bd/notebooklm-mcp-cli/blob/main/docs/CLI_GUIDE.md

## Core Commands Overview

The CLI supports two command styles—noun-first (resource-oriented) and verb-first (action-oriented). Both are functionally equivalent.

### Authentication

- `nlm login` — Initiates browser-based authentication with automatic cookie extraction
- `nlm login --check` — Verifies current authentication status
- Supports multiple named profiles for managing different Google accounts
- Profile management includes switching, listing, and deletion options

### Notebook Management

Basic operations include creating, listing, renaming, and deleting notebooks. The CLI supports:
- `nlm notebook list` — Display all notebooks
- `nlm notebook create "Title"` — Create new notebook
- `nlm notebook query <id> "question"` — Chat with notebook sources
- `nlm notebook rename <id> "New Title"` — Rename notebook
- `nlm notebook delete <id>` — Delete notebook

### Source Management

Users can add sources via URLs, files, YouTube videos, or Google Drive documents. Key flags:
- `--url`, `--file`, `--youtube`, `--drive` — Specify source type
- `--wait` — Ensures sources are processed before proceeding
- Sources can be synchronized or removed as needed

**Examples:**
```bash
nlm source add <notebook-id> --url https://example.com
nlm source add <notebook-id> --file document.pdf --wait
nlm source add <notebook-id> --youtube https://youtube.com/watch?v=...
```

### Content Generation

The CLI generates multiple artifact types:

**Audio**: Podcasts with format options
- Formats: deep_dive, brief, critique, debate
- `nlm audio create <notebook-id> --format deep_dive`

**Video**: Explainer or brief formats with multiple visual styles
- `nlm video create <notebook-id> --format explainer`

**Reports**: Briefing docs, study guides, blog posts
- `nlm report create <notebook-id> --type study_guide`

**Educational**: Quizzes, flashcards, mind maps, slide decks
- `nlm quiz create <notebook-id>`
- `nlm flashcards create <notebook-id>`

**Visual**: Infographics and data tables
- `nlm infographic create <notebook-id>`

All generation commands use `--confirm` flag to prevent accidental execution.

### Downloads & Exports

Downloads support format-specific output:
- Audio/video to media files (mp3, mp4)
- Reports to markdown
- Interactive formats (quiz, flashcards) to HTML or markdown
- Data tables to CSV

**Examples:**
```bash
nlm audio download <artifact-id> --output podcast.mp3
nlm report download <artifact-id> --output study-guide.md
```

### Advanced Features

#### Research
`nlm research start <notebook-id> "query"` — Performs fast or deep web searches
- Status polling with `nlm research status <research-id>`
- Import discovered sources with `nlm research import <research-id>`

#### Sharing
Control notebook access via public links or email invitations:
```bash
nlm notebook share <id> --public
nlm notebook invite <id> user@example.com --role editor
```

#### Configuration
Customize output format, color, ID display, and default profile:
```bash
nlm config set output.format json
nlm config set display.color false
```

#### Aliases
Create shortcuts for frequently-used notebook IDs:
```bash
nlm alias set my-research <notebook-id>
nlm query my-research "What are the key findings?"
```

#### Skills & Setup
Install tools for AI assistants:
```bash
nlm skill install claude-code
nlm skill install cursor
nlm skill install gemini
```

Configure MCP servers with one-command setup:
```bash
nlm setup mcp --client claude-code
```

#### Diagnostics
`nlm doctor` — Troubleshoots:
- Installation status
- Authentication status
- Chrome availability
- AI tool configuration

## Output Formats

Results display as rich tables by default, with options for:
- `--json` — JSON output
- `--quiet` — IDs only
- `--title` — ID: Title format
- `--full` — All columns

## Practical Tips

- **Session expiry**: Sessions expire after ~20 minutes; re-run `nlm login` if operations fail
- **Confirmations**: Use `--confirm` in automated scripts for destructive operations
- **Source processing**: Employ `--wait` when adding sources before querying
- **Generation time**: Content generation (audio/video) typically requires 1–5 minutes
- **Diagnostics**: Run `nlm doctor` to diagnose setup or authentication issues
- **Context management**: With 29 tools, use `@notebooklm-mcp` in Claude Code to enable only when needed

## Common Workflows

### Research to Podcast Workflow
```bash
# 1. Create notebook
nlm notebook create "AI Research"

# 2. Add sources
nlm source add <id> --url https://research-paper.com --wait

# 3. Generate podcast
nlm audio create <id> --format deep_dive

# 4. Check status
nlm audio status <artifact-id>

# 5. Download when ready
nlm audio download <artifact-id> --output research-podcast.mp3
```

### Study Material Generation
```bash
# 1. Add sources to notebook
nlm source add <id> --file textbook.pdf --wait

# 2. Generate study materials
nlm quiz create <id>
nlm flashcards create <id>
nlm report create <id> --type study_guide

# 3. Download materials
nlm quiz download <quiz-id> --output quiz.html
nlm flashcards download <fc-id> --output flashcards.html
nlm report download <report-id> --output study-guide.md
```

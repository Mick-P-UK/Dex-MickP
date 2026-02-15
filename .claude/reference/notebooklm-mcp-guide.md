# NotebookLM MCP Setup Guide

**Source:** https://github.com/jacob-bd/notebooklm-mcp-cli/blob/main/docs/MCP_GUIDE.md

## Installation

Install the package via:
```bash
uv tool install notebooklm-mcp-cli
```

Then integrate with your AI assistant:
- **Claude Code**: `claude mcp add --scope user notebooklm-mcp notebooklm-mcp`
- **Gemini CLI**: `gemini mcp add --scope user notebooklm-mcp notebooklm-mcp`
- **Cursor/VS Code**: Add to `~/.cursor/mcp.json` or `~/.vscode/mcp.json`

## Authentication

Before using tools, authenticate with:
```bash
nlm login
```

This loads your NotebookLM credentials for API access.

## Core Tool Categories (29 Total)

**Notebooks**: Create, list, retrieve, describe, rename, delete notebooks

**Sources**: Unified `source_add()` handles URLs, text, files, or Google Drive documents with optional `wait=True` parameter for processing completion

**Querying**: Query notebooks and configure chat behavior

**Studio Content**: Generate podcasts, videos, reports, quizzes, flashcards, mind maps, slides, infographics, and data tables

**Downloads/Exports**: Retrieve artifacts or export to Google Workspace

**Research**: Conduct web or Drive searches, then import discovered sources

**Notes**: Manage notebook annotations via list/create/update/delete actions

**Sharing**: Control visibility and invite collaborators

**Auth/Server**: Refresh tokens and check version status

## Configuration Options

**Server Flags**:
- `--transport` (stdio, http, sse) — default: stdio
- `--port` — HTTP/SSE listening port — default: 8000
- `--debug` — Enable verbose logging — default: false

**Environment Variables**:
- `NOTEBOOKLM_MCP_TRANSPORT`
- `NOTEBOOKLM_MCP_PORT`
- `NOTEBOOKLM_MCP_DEBUG`
- `NOTEBOOKLM_QUERY_TIMEOUT`

## Key Workflows

**Research to Podcast**: Start research → poll status → import sources → create audio artifact → download MP3

**Source Management**: Use unified `source_add()` with `wait=True` to ensure "source is fully processed and ready for queries"

**Study Material Generation**: Create quizzes, flashcards, and guides in sequence

## Context Window Best Practices

With 29 tools consuming context tokens, consider:
- Disabling MCP when not needed (use `@notebooklm-mcp` in Claude Code)
- Leveraging unified tools (`source_add`, `studio_create`, `download_artifact`)
- Polling status endpoints sparingly — artifacts require 1-5 minutes to generate

## IDE-Specific Setup

**Cursor/VS Code Configuration**:
```json
{
  "mcpServers": {
    "notebooklm-mcp": {
      "command": "/path/to/notebooklm-mcp"
    }
  }
}
```

## Troubleshooting

If MCP server doesn't load:
1. Verify installation: `which notebooklm-mcp` or `where notebooklm-mcp`
2. Test manual startup: `notebooklm-mcp server`
3. Check authentication: `nlm login --check`
4. Run diagnostics: `nlm doctor`
5. For Claude Code, use: `claude mcp add --scope user notebooklm-mcp notebooklm-mcp`

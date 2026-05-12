---
name: notebooklm-chat
description: >
  Queries an existing NotebookLM notebook via Claude and returns a structured,
  Cedric-formatted answer with source attributions, then saves the response as
  a markdown file to the vault. Use this skill whenever Mick asks "query the
  notebook", "ask the notebook about...", "what does the notebook say about...",
  "research question for the notebook", "chat with the notebook", or any
  request to extract information or answers from a NotebookLM notebook via
  Claude. Always saves responses to the vault. Read-only -- does not modify
  the notebook, index, or title.
---

# Skill 3: NotebookLM Chat (Query via CLI)

Queries a NotebookLM notebook and returns a structured Cedric-formatted
answer with source attributions. Saves response to vault as a markdown file.
Read-only operation -- notebook, index, and title are never modified.

Uses: notebooklm-py CLI (teng-lin/notebooklm-py)
Auth: notebooklm-auth-monitor handles session monitoring automatically.
      If auth has lapsed, run: notebooklm login

---

## CLI REFERENCE (key commands for this skill)

```bash
# List notebooks (find ID by name)
notebooklm list

# Query a notebook
notebooklm use <notebook_id>
notebooklm ask "your question here"

# Or in one shot without changing context:
notebooklm --json ask "your question" 2>/dev/null

# Check auth status
notebooklm auth check --test
```

---

## PHASE 1 -- IDENTIFY THE TARGET NOTEBOOK

1. If Mick has not specified a notebook, ask which one to query
2. If no notebook_id known, run via bash:
   ```bash
   notebooklm list
   ```
   Find the notebook by name and note its ID.
3. Confirm the notebook name to Mick before querying.

---

## PHASE 2 -- ACCEPT THE QUERY

1. Accept Mick's question or research brief
2. If the query is vague, offer to clarify or suggest a more specific phrasing
3. Note today's London date via python3 (for file naming)

---

## PHASE 3 -- RUN THE QUERY

Run via bash:
```bash
notebooklm use <notebook_id>
notebooklm ask "<Mick's question>"
```

If the command returns an authentication error:
- Check status: notebooklm auth check --test
- If auth expired: tell Mick "NotebookLM session has expired - please run:
  notebooklm login  (takes 30 seconds, browser will open)"
- Once Mick confirms re-login done, retry the ask command once.

If query succeeds, capture the full response text.

---

## PHASE 4 -- FORMAT AND PRESENT THE RESPONSE

Format the response in Cedric style:

  # [Query Summary -- 5-8 words]
  Notebook: [Notebook Title]
  Query date: DD Month YYYY
  Query: "[Mick's exact question]"
  ============================================================

  ## Answer
  [Full answer in clear, plain English paragraphs]

  ## Sources Referenced
  [List of sources cited in the response, with titles and dates where available]

  ## Suggested Follow-up Queries
  [2-3 suggested follow-up questions based on the response]

  ============================================================
  Risk note: This response is derived from the sources loaded into the
  notebook. Always verify key facts against primary sources before acting.
  DYOR: Cedric, Mick's AI Research Assistant ([date])

Present the formatted response in the Claude conversation first.

---

## PHASE 5 -- SAVE TO VAULT

Save the formatted response as a markdown file:

Path:     C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\NotebookLM-Queries\
Filename: YYYY.MM.DD - [Notebook Name short] - [Query Summary].md

- YYYY.MM.DD = today's date
- Notebook Name short = first meaningful word(s) of notebook title (max 4 words)
- Query Summary = 3-5 word summary of the query (no special characters)
- Example: 2026.04.19 - PROPPS BoE - What are PROPPs.md

Use the Write tool to save. Confirm save path to Mick on completion.

---

## PHASE 6 -- OFFER FOLLOW-UP

After presenting and saving:
"I've saved this response to the vault. Would you like me to:
  - Run another query on this notebook?
  - Query a different notebook?
  - Generate a studio artifact from this notebook (briefing doc, study guide, etc.)?"

---

## TECHNICAL NOTES

- This skill is READ-ONLY: never update notebook title, index, or sources
- If notebooklm ask times out or returns empty, retry once before reporting failure
- Auth is managed by notebooklm-auth-monitor running in the watcher background
- The notebooklm CLI uses ~/.notebooklm/profiles/default/storage_state.json
- Sessions last days to weeks; CSRF tokens auto-refresh transparently
- If all else fails: notebooklm login (browser opens, 30-second fix)

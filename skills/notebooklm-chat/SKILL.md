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

# Skill 3: NotebookLM Chat (Query via Claude)

Queries a NotebookLM notebook and returns a structured Cedric-formatted
answer with source attributions. Saves response to vault as a markdown file.
Read-only operation -- notebook, index, and title are never modified.

---

## PHASE 1 -- IDENTIFY THE TARGET NOTEBOOK

1. If Mick has not specified a notebook, ask which one to query
2. Retrieve notebook by name search or direct ID
3. Confirm the notebook name to Mick before querying

---

## PHASE 2 -- ACCEPT THE QUERY

1. Accept Mick's question or research brief
2. If the query is vague, offer to clarify or suggest a more specific phrasing
3. Note today's London date via python3 (for file naming)

---

## PHASE 3 -- RUN THE QUERY

1. Run: notebooklm-mcp:notebook_query
   - notebook_id: [target notebook ID]
   - query: [Mick's question]
   - timeout: 90
2. If authentication error: call notebooklm-mcp:refresh_auth then retry once
3. Receive and process the full response including source citations

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
  [List of sources cited in the response, with titles and dates]

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

Use Filesystem:write_file to save.
Confirm save path to Mick on completion.

---

## PHASE 6 -- OFFER FOLLOW-UP

After presenting and saving:
"I've saved this response to the vault. Would you like me to:
  - Run another query on this notebook?
  - Query a different notebook?
  - Generate a studio artifact from this notebook (briefing doc, FAQ etc.)?"

---

## TECHNICAL NOTES

- This skill is READ-ONLY: never update notebook title, index, or sources
- If notebook_query times out, retry once before reporting the issue
- Authentication: if nlm login needed, run in terminal then call refresh_auth
- If the query returns no useful result, suggest reformulating the question
- Always save to vault even for short responses -- the log builds over time

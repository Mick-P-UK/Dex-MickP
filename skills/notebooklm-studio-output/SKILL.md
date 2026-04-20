---
name: notebooklm-studio-output
description: >
  Generates NotebookLM studio artifacts (briefing docs, FAQs, study guides,
  blog posts, audio overviews, mind maps) from an existing notebook via Claude,
  and optionally exports them to Google Docs. Use this skill whenever Mick asks
  to "generate a briefing doc", "create a FAQ from the notebook", "make a
  study guide", "produce an audio overview", "create a mind map", "generate a
  studio output", or any request to produce a NotebookLM studio artifact.
  Read-only -- does not modify the notebook, index, or title.
---

# Skill 4: NotebookLM Studio Output

Generates studio artifacts from a NotebookLM notebook and optionally exports
to Google Docs. Read-only -- notebook, index, and title are never modified.

---

## SUPPORTED ARTIFACT TYPES

| Type         | Description                                      | Exportable?  |
|--------------|--------------------------------------------------|--------------|
| briefing_doc | Executive summary of all sources                 | Yes (Docs)   |
| faq          | Frequently asked questions with answers          | Yes (Docs)   |
| study_guide  | Structured learning guide with key concepts      | Yes (Docs)   |
| blog_post    | Accessible article suitable for general audience | Yes (Docs)   |
| mind_map     | Visual mind map of topics and relationships      | No           |
| audio        | AI-generated audio overview (podcast style)      | No           |

NOTE: mind_map returns structured JSON immediately (no polling needed).
All other types require polling studio_status until complete.

---

## PHASE 1 -- IDENTIFY THE TARGET NOTEBOOK

1. If Mick has not specified a notebook, ask which one to use
2. Retrieve notebook by name search or direct ID
3. Confirm notebook name to Mick before proceeding

---

## PHASE 2 -- SELECT ARTIFACT TYPE

If Mick has not specified an artifact type, offer the menu:
"Which studio artifact would you like me to generate?
  1. Briefing Doc -- executive summary of all sources
  2. FAQ -- key questions and answers from the sources
  3. Study Guide -- structured learning guide
  4. Blog Post -- accessible article for a general audience
  5. Mind Map -- visual map of topics and relationships
  6. Audio Overview -- AI podcast-style audio summary"

Note any special instructions from Mick (e.g. tone, focus area, length).

---

## PHASE 3 -- GENERATE THE ARTIFACT

1. Trigger: notebooklm-mcp:studio_create
   - notebook_id: [target notebook ID]
   - artifact_type: [selected type]
   - confirm: true
   - Include any special instructions if supported
2. For mind_map: result returned immediately, no polling needed
3. For all others: poll notebooklm-mcp:studio_status until status = complete
   - Poll every 15 seconds; report progress to Mick
   - Timeout after 10 minutes; report if exceeded
4. On completion: retrieve artifact URL and ID from studio_status response

---

## PHASE 4 -- REPORT AND OFFER EXPORT

Present the result:
  "Your [artifact type] is ready:
   Title:    [artifact title]
   Notebook: [notebook title]"

Offer Google Docs export (for briefing_doc, faq, study_guide, blog_post only):
  "Would you like me to export this to Google Docs?"

If accepted:
- notebooklm-mcp:export_artifact
  - artifact_id: [artifact UUID]
  - export_type: docs
  - notebook_id: [notebook UUID]
  - title: [Notebook short name] - [Artifact Type] - YYYY.MM.DD
- Report the Google Docs URL on completion

---

## PHASE 5 -- OFFER FOLLOW-UP

"Would you like me to:
  - Generate a different artifact type from this notebook?
  - Query this notebook directly (chat)?
  - Add more sources to this notebook?"

---

## TECHNICAL NOTES

- Audio and mind_map artifacts cannot be exported to Google Docs
- Studio generation can take several minutes for large notebooks
- This skill is READ-ONLY: never update notebook title, index, or sources
- If studio_create fails, check that the notebook has at least 1 source loaded
- Export requires the Google Docs MCP to be connected
- nlm login may be required at the start of each Claude Desktop session

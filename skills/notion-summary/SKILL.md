---
name: notion-summary
description: "When asked to summarise a financial announcement (usually an RNS), you summarise the text from the Notion Page and post it to a Notion \"Summary (item)\" field on that page."
---

## Skill: notion-announcement-summary

**Trigger:** User asks to summarise a financial/corporate announcement and post it to Notion.
**Purpose:** Read an RNS or similar announcement, produce a structured summary (<=200 words), and post it to the Notion "Summary (item)" property field with correct formatting.

### Rules

- Summary must be <=200 words
- Sections: Financial Highlights, Financial Position, Operations, Key Developments (adapt headings to suit the announcement type)
- Each section heading must be bold
- Each bullet point must be on its own line
- Use Shift+Enter for line breaks within the Notion text property field
- Never use pipe separators (|)
- Never put all content on a single line

### Workflow (browser control)

1. Use `get_page_text` to read the full announcement
2. Compose the summary internally before typing anything
3. Click the Summary (item) field to activate it
4. For each section:
   a. Press Ctrl+B -> type heading -> press Ctrl+B (bold toggled inline)
   b. Press Shift+Enter
   c. Type bullet: * [content] -> press Shift+Enter
   d. Repeat for all bullets in section
5. Click outside the field to save
6. Take a screenshot to verify formatting
7. Confirm task complete

### Quality Checks

- Headings are bold and on their own lines
- Bullets are on separate lines
- No pipe separators
- Word count <=200

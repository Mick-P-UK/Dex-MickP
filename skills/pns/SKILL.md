---
name: pns
trigger: /pns
description: Post Notion Summary. When invoked on a Notion page containing an announcement, article, or report, reads the page content, generates a concise structured summary (max 200 words), and posts it into the Summary (item) property field. Adapts section headings to content type (financial results, trading updates, general articles). Use on any Notion database page with a Summary (item) text property.
---

# Skill: /pns -- Post Notion Summary

## Purpose
Read a Notion page, generate a structured summary of no more than 200 words, and post it into the **Summary (item)** property field near the top of the page.

---

## Step-by-Step Instructions

### Step 1 -- Read the page content
Use `get_page_text` on the current Notion tab to extract the full text.
- Set `max_chars` to at least 99999 to capture the full content.

### Step 2 -- Generate the summary
Write a summary of no more than 200 words. Structure it with bold section headings and bullet points. Choose 4-5 logical sections based on content type:

- **Financial results:** Financial Highlights, Divisional Performance, Shareholder Returns, Guidance & Targets, Strategic Progress
- **Trading updates:** Financial Highlights, Trading Performance, Regional/Channel Breakdown, Outlook
- **General articles/notes:** Key Points, Background, Implications, Next Steps

Each heading should have 2-3 concise, data-rich bullet points.

Format:
```
**Section Heading**
- Bullet point one
- Bullet point two
**Next Section**
- Bullet point one
- Bullet point two
```

Keep all points tight and decision-relevant for an investor or researcher.

### Step 3 -- Locate the Summary (item) field
Take a screenshot to confirm page layout. Use `find` to locate the Summary (item) field in the properties panel near the top of the page.

**CRITICAL:** Click the **value side** of the field (the area to the right of the "Summary (item)" label, where it shows "Empty" or existing content) -- NOT the label itself. Clicking the label opens a context menu (rename, edit, delete) instead of the input box.

### Step 4 -- Open and activate the field
Click the value area to open the text input box. Click inside to place the cursor.

If the field already contains content: use `Ctrl+A` then `Delete` to clear it before typing.

### Step 5 -- Type the summary using Shift+Enter for line breaks

**CRITICAL: Never press plain Enter/Return inside a Notion property field.** Plain Enter saves and closes the field immediately, cutting off remaining content. Always use `Shift+Enter` for all line breaks.

Typing sequence for each section:
1. Type `**Section Heading**`
2. Press `Shift+Enter`
3. Type `- Bullet point`
4. Press `Shift+Enter`
5. Repeat for each bullet, then start the next section heading

Bold markdown (`**text**`) is auto-converted by Notion as you type.

### Step 6 -- Save by clicking outside
Once all content is typed, click outside the field -- ideally in the left sidebar or a neutral area. Do NOT click on the page title or body text. The field saves automatically when focus moves away.

### Step 7 -- Verify
Take a screenshot to confirm the summary is correctly saved. Check:
- Bold headings are rendering in bold
- All bullet points are visible
- Content is not truncated
- Full summary is present (not just the first line)

If the field appears to show only the first line, click into it to expand -- Notion's inline display may truncate long property values, but the full content should be stored correctly.

---

## Key Technical Notes

| Rule | Detail |
|------|--------|
| Shift+Enter is essential | Plain Enter closes the field and saves only what has been typed so far |
| Click the value, not the label | Clicking the label opens a property options menu |
| Bold text | Typing `**text**` in a Notion rich-text field auto-converts to bold |
| Clear existing content | Use Ctrl+A then Delete before retyping if field already has content |
| Save cleanly | Click the left navigation sidebar to dismiss the editing popup |
| Truncated display | Normal Notion behaviour -- full content is stored, click field to see it all |

---

## Adaptability
This skill works on any Notion database page with a **Summary (item)** text property. Always adapt section headings to suit the content type. Prioritise decision-relevant information for an investor or researcher. Keep summaries to 200 words or fewer.

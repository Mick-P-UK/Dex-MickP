---
title: Notion Announcement Summary (Summary item field)
code: SUM-01
category: SUM
ahk: none
version: 1.0
date_created: 2026.07.29
date_updated: 2026.07.29
status: active
operational: true
tags: [prompt, notion, summary, rns, announcement, formatting, bullets, diy-investors]
---

# Notion Announcement Summary (Summary item field)

## Prompt

Please create a concise summary (no more than 200 words) from this announcement and post it in the Summary (item) field near the top of this Notion page. Format requirements: Use Ctrl+B to toggle bold on/off inline as you type each heading - do not go back to apply bold afterwards. Press Shift+Enter after each heading and each bullet point to create line breaks within the field. Do NOT use pipe separators (|) or put everything on one line. Each item beneath a section heading must begin with a round bullet character (Unicode U+2022) followed by a single space. Section headings themselves do not get a bullet. Example (where [U+2022] is the literal round bullet character): [U+2022] Revenue $155m (+65% YoY). Sections: Financial Highlights, Financial Position, Operations, Key Developments (or headings appropriate to the announcement). Workflow: Click the Summary (item) field -> type the heading with bold toggled on -> Shift+Enter -> toggle bold off -> type bullet points with Shift+Enter between each -> repeat for each section -> click outside to save -> confirm formatting looks correct.

## Notes

- Purpose: generate a tight (<=200 word) structured summary of a company announcement (usually an RNS) and post it directly into the Notion "Summary (item)" field.
- ASCII-store convention: the prompt names the bullet as "Unicode U+2022" and shows the example marker as "[U+2022]". When actually typed into Notion, that means the literal round bullet character followed by a space. This keeps the vault file ASCII-clean per Mick's zero-tolerance rule while preserving the exact formatting instruction.
- Arrows in the workflow step are written as "->" (ASCII) and stand for the original single-arrow flow markers.
- Related: overlaps with the /pns skill (Post Notion Summary) and the notion-summary skill. This note is the plain dictated-prompt version for manual/hand-driven use.

## Changelog

- v1.0 - created 2026.07.29 (dictated by Mick; stored fully-ASCII with the bullet described as U+2022, at Mick's direction)

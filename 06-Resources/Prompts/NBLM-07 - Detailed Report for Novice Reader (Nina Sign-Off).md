---
title: Detailed Report for Novice Reader (Nina Sign-Off)
code: NBLM-07
category: NBLM
ahk: ::nb8#
version: 1.0
date_created: 2026.07.29
date_updated: 2026.07.29
status: active
operational: true
tags: [prompt, notebooklm, detailed-report, novice, nina, sign-off, technical-terms, calculations, appendix, uk-english]
---

# Detailed Report for Novice Reader (Nina Sign-Off)

## Prompt

Using the selected sources, please provide a Detailed Report - giving a detailed and balanced view in response to the {{User Query}}. Please include an Executive Summary, Index, Tabulated Analysis figures and a conclusion. IMPORTANT: 1) Use UK English & Spelling. 2) Please include an appendix with your full calculations (if financial figures and/or calculations are involved). 3) Add an Appendix with any technical terms fully explained. 4) Assume the reader is a "novice". Sign off as "Nina, Mick's AI Research Assistant" add the current date & time (London).

## Notes

- Purpose: general-purpose NotebookLM report prompt for a non-specialist audience. Sits alongside NBLM-05 and NBLM-06 as the "novice reader" variant of the same family.
- Placeholder: {{User Query}} is NotebookLM's own variable - leave it as written.
- AHK shortcode reserved as ::nb8# but NOT yet added to the AutoHotkey script (Mick to add).
- ::nb7# is deliberately NOT a gap. Mick has a prompt assigned to it that has not yet been passed to Cedric (2026.07.29 - he was mid webinar preparation). Do not reassign ::nb7# and do not renumber this entry. When Mick supplies it, file it as NBLM-08 with ahk ::nb7#, and note that from here on the CAT-NN code and the AHK number no longer run in step.
- Differences from NBLM-06 (General Analysis - Nina Sign-Off):
  * calls for a "Detailed Report" rather than an "Analysis Report"
  * calculations appendix is conditional ("if financial figures and/or calculations are involved") rather than mandatory
  * adds the explicit instruction to assume a novice reader
  * no charts request and no risk warning
  * sign-off date/time is "London" rather than "London [BST]", so it stays correct year round
- Differences from NBLM-05 (General Analysis - No Sign-Off): NBLM-05 has no sign-off and no novice-reader instruction.

## Changelog

- v1.0 - created 2026.07.29 (supplied by Mick; AHK ::nb8# reserved, pending addition to the AHK script)

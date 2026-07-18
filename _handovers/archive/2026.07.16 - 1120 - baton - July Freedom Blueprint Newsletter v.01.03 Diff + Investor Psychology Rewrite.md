---
title: Baton Handover -- July Freedom Blueprint Newsletter v.01.03 Diff + Investor Psychology Rewrite
date: 2026-07-16
time: late morning (London)
topic: July 2026 Freedom Blueprint Newsletter
thread: Diffed Mick's edited v.01.03 Word draft against the working TXT, applied all changes, added a new Investor Psychology article Mick drafted via Descript, rewrote that article in Mick's voice, session paused mid-project to resume this evening
status: handover
author: Cedric (PAIDA)
generated-by: AI
---

# Baton Handover -- July Freedom Blueprint Newsletter v.01.03 (2026-07-16, late morning)

Topic: July 2026 Freedom Blueprint Newsletter (Mick's-Writing-System vault - no separate Dex topic note; tracked via that vault's own auto-memory system, see project_july_newsletter.md)

## Thread character

Session opened in the Mick's-Writing-System vault (not Dex). Mick uploaded a revised .docx (v.01.03) of the July newsletter he had been editing directly in Word, including a new "Investor Psychology" section he had drafted via Descript's AI tool - he flagged upfront that the Descript article was not in his voice and asked for it to be rewritten. No docx-to-text skill exists yet in this vault (see project_docx_to_html_skill memory, still parked), so Cedric used python-docx directly (confirmed installed) to extract the .docx paragraph text and diff it against the last working TXT draft (v.01.02). Applied every substantive change Mick had made in Word, then rewrote the Investor Psychology article from scratch using voice-dna-mick.json and the diy-newsletter skill, keeping the same subheading structure but replacing the generic AI content with Mick's first-person register, British understatement, and concrete grounding (2008 crash, Great Depression, Buffett buy-the-dip framing). Mid-session, Mick flagged two new "Yr2" portfolio images added to the Newsletter-Images folder the previous day; Cedric asked whether to add Year 2 portfolio sections to Page 3, and Mick said leave them out for this edition. Verified the finished draft was 100% ASCII-clean via a Python scan (mandatory rule in this vault). Session then paused at Mick's request, to resume this evening.

## Decisions made

- Yr2 portfolio images (UK Active 10_Yr2_16288.05_GBP, US Active 10_Yr2_18361.54_USD, both added 15th July) will NOT be added to the July edition - Page 3 stays with just the two Year 1 portfolios (UK Active 10, US Active 10), matching the structure already established in v.01.01/v.01.02.
- The Investor Psychology article Mick drafted via Descript is superseded, not kept in the live draft - Cedric's rewrite in Mick's voice is now the Page 4 content. The original AI-generated text is preserved only in version history (noted inline in the TXT file) in case Mick wants to compare or recover any specific line.
- Newsletter has grown from a 4-page to a 5-page edition this month (Page 4 = new Investor Psychology article, wrap-up pushed to Page 5) - same pattern as the content-heavy June edition, which also ran longer than the typical 4-pager. Not treated as a problem, just noted.

## Files changed this thread

All in `C:\Vaults\Mick's-Writing-System\knowledge\drafts\` unless noted.

- [CREATE] `2026.07.16 - Freedom Blueprint July_v.01.03_TXT.txt` - full working draft, all of Mick's v.01.03 edits applied (signature date, feature headline tweak, GBP/USD symbol-to-text swaps, purchase-date clarifier, new UK-vs-US comparison paragraph, ACM Research exit gain + cash balance, curly-apostrophe ASCII cleanup) plus the rewritten Investor Psychology article as new Page 4. Verified zero non-ASCII characters via a Python scan.
- [SOURCE, unchanged] `2026.07.15 - Freedom Blueprint July_v.01.03_DRAFT_Mick.docx` - Mick's Word version this thread worked from.
- [UPDATE] Writing System auto-memory: `project_july_newsletter.md` - rewritten to reflect the 5-page state, what's done, and what's still needed from Mick.

## Open questions / unfinished

- **Page 5 wrap-up still a placeholder** - closing remarks not yet drafted (needs Mick's tone/summary input, same as prior months).
- **Inner Circle webinar date** - draft still carries "Wednesday 8th July 2026" as a placeholder, which has almost certainly already passed by publish date. Needs a real date/time from Mick.
- **Boot Camp / upcoming events** - nothing drafted yet for the wrap-up; needs Mick's input on what to include.
- **No docx-to-text skill exists yet** - this thread again worked around that gap with an inline python-docx script rather than a reusable tool. The planned `project_docx_to_html_skill` build (still parked, "to be built in a fresh session") would also solve the docx-diffing problem this thread needed - worth considering scoping it to cover both directions (docx->html AND docx->text-for-diffing) when that build finally happens.
- **v.01.03 DRAFT_Mick.docx had no new/replaced images** - confirmed via the docx's image relationships (9 images total, consistent with the existing header/footer/feature/2x portfolio/2x transactions set); the two new Yr2 images living in the Newsletter-Images folder were added separately, not embedded in the docx Mick sent.

## Next-thread pickup

- Opener phrase: "Cedric, resume from LATEST handover" (or just "let's pick the newsletter back up" - Mick knows this is a same-day pause, not a multi-day gap).
- First action: draft Page 5 wrap-up. Will need from Mick: (1) closing remarks tone/summary for the month, (2) confirmed next Inner Circle webinar date/time (8th July placeholder is stale), (3) any Boot Camp or upcoming events to mention.
- Once Page 5 is drafted, the newsletter is ready for Mick's full read-through and word-count check (currently running long at ~1,450 words across 5 pages vs the usual ~1,050 target - flag this to Mick rather than silently trimming, since the extra length is the Investor Psychology article he explicitly wanted).
- After text is approved: produce the .docx via python-docx (heading colours per SKILL.md: navy #1F3864 section headings, dark red #C00000 portfolio headings) and the HTML version for WordPress, per the standard two-track workflow.

## Content Studio logged

No Content Studio artefacts this thread - this was Writing System newsletter production work, not Dex/PAIDA infrastructure or content-idea work.

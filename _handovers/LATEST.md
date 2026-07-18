---
title: Baton Handover -- July Freedom Blueprint Newsletter v.01.04 Content-Complete + New 5-Page Template + Layout SOP
date: 2026-07-17
time: afternoon/evening (London)
topic: July 2026 Freedom Blueprint Newsletter
thread: Closed out the last open content gaps on the July newsletter (video link, webinar dates, closing remarks, feedback CTA link), built the .docx via python-docx, and - at Mick's request while he read a printout - built a reusable 5-page Word template and captured his own layout edits (horizontal-rule section dividers instead of page breaks) into the newsletter SOP and memory for good
status: handover
author: Cedric (PAIDA)
generated-by: AI
---

# Baton Handover -- July Freedom Blueprint Newsletter v.01.04 (2026-07-17, afternoon/evening)

Topic: July 2026 Freedom Blueprint Newsletter (Mick's-Writing-System vault - no separate Dex topic note; tracked via that vault's own auto-memory system, see project_july_newsletter.md and the new project_newsletter_5page_template.md)

## Thread character

Continued directly from the 2026-07-16 handover (Page 5 still a placeholder). Mick supplied, in sequence: a video thumbnail image + Vimeo link for the Investor Psychology article, two webinar dates (AI for Investing monthly webinar and Inner Circle webinar), and asked Cedric to draft closing remarks and drop the Boot Camp/events placeholder (nothing to report this edition). Cedric closed all of these out, verified ASCII compliance, and versioned the result as v.01.04 (TXT + a Cedric-built DOCX via python-docx, following the diy-newsletter skill's heading-colour rules).

Mick then said he'd print the DOCX and read it carefully during the day, being out until evening - and asked Cedric to use the wait productively by building a reusable 5-page Word template (the July edition grew from the usual 4 pages to 5 because of the added Investor Psychology article), to sit alongside the existing 4-page master template without overwriting it. Cedric built this by extracting the header/footer images from the original template and reassembling a fresh 5-page structure with placeholder text, matching the skill's navy/red heading-colour convention.

Before evening, Mick returned having made his own layout edit directly in Word, saved as `..._v.01.04_DOCX_Mick.docx` (his naming, an underscore short of "_Mick" the first time, self-corrected). Cedric diffed this against the original to find Mick had replaced every manual page break with a thin horizontal-rule divider (bottom paragraph border) at each section boundary, letting the document paginate naturally rather than forcing hard breaks - and asked Cedric to capture this as a standing SOP rule, not just a one-off edit. Cedric extracted the exact border spec from Mick's XML, rebuilt the 5-page template to match it, and wrote it into both the diy-newsletter skill and the newsletter-style feedback memory.

Finally, Mick asked for the feedback CTA ("Just send us a message HERE!") to carry a real hyperlink to the site's contact page, and confirmed this is standard for every newsletter, not July-specific. Cedric added it as an actual OOXML hyperlink (not just the bold/blue styling Mick's own edit already had) to both DOCX versions and the 5-page template, and documented it as a permanent fixed element in the skill (alongside the header/footer images) and in memory.

## Decisions made

- July v.01.04 is content-complete across all 5 pages: Intro, Mick's Musings/feature article, Portfolio Updates (UK + US, both shown in full), Investor Psychology article (with video thumbnail hyperlinked to Vimeo), and Wrap-Up (draft closing remarks + two webinar dates, Boot Camp placeholder removed entirely rather than left empty).
- A second master Word template now exists for 5-page/content-heavy editions, alongside the untouched original 4-page master. Use the 5-page one whenever a month has a second full feature article that won't fit the standard 4-page structure; confirm with Mick if it's ambiguous which size an edition needs.
- **New standing layout rule**: never use `doc.add_page_break()` between newsletter sections again. Use a bottom-paragraph-border horizontal rule instead (`w:pBdr` / `w:bottom` - single, sz 6, space 1, colour auto), applied to the last paragraph of each section, so the document flows continuously and paginates naturally in Word. This applies to all future .docx production, not just the 5-page template.
- **New standing content rule**: the feedback CTA "HERE!" is always a real hyperlink to https://diy-investors.com/contact-us-2/ in every newsletter .docx Cedric produces - confirmed by Mick as standard, not edition-specific.
- Mick's own `_v.01.04_DOCX_Mick.docx` is now the reference layout copy (his hands-on edit, not just a read-through markup) - treat it as the layout baseline; the TXT (v.01.04) remains the text-content baseline until Mick says otherwise.

## Files changed this thread

All in `C:\Vaults\Mick's-Writing-System\` unless noted.

- [CREATE] `knowledge\drafts\2026.07.17 - Freedom Blueprint July_v.01.04_TXT.txt` - Page 4 video link + Page 5 wrap-up (closing remarks, both webinar dates, feedback CTA link note) completed; Boot Camp placeholder removed.
- [CREATE, then UPDATE] `knowledge\drafts\2026.07.17 - Freedom Blueprint July_v.01.04_DOCX.docx` - full Cedric-built .docx via python-docx (navy #1F3864 / red #C00000 heading colours, all portfolio/transaction/feature images embedded, video thumbnail hyperlinked to Vimeo, provenance footer on every page per the vault-wide DOCX rule); later updated to add the real "HERE!" hyperlink.
- [Mick's own edit, then UPDATE] `knowledge\drafts\2026.07.17 - Freedom Blueprint July_v.01.04_DOCX_Mick.docx` - Mick's manual layout pass (horizontal-rule dividers replacing all page breaks); Cedric added the real "HERE!" hyperlink on top of Mick's edit without disturbing anything else.
- [CREATE, then rebuilt twice] `0.0 - Inbox\Newsletter-Images\2026.07.17-Freedom-Blueprint_Template_v1.00_5Page.docx` - new reusable 5-page master template (placeholder/generic content, same structure as the July edition); rebuilt once to apply the horizontal-rule-divider convention (0 page breaks, 8 dividers, matching Mick's spec exactly), rebuilt again to add the real feedback-CTA hyperlink.
- [UPDATE] `.claude\skills\diy-newsletter\SKILL.md` - overview line now notes 4-page vs 5-page editions; "Word Template Location" section documents both templates and when to use each; new "Layout: section dividers, not hard page breaks" subsection with the exact XML spec; feedback-CTA hyperlink documented as a fixed/permanent element; new "July 2026" entry under Cycle Learnings.
- [UPDATE] Writing System auto-memory: `project_july_newsletter.md` (rewritten for v.01.04 content-complete state + Mick's own layout edit), `feedback_newsletter_style.md` (added the divider-convention and feedback-CTA-link formatting standards), `MEMORY.md` (index updated).
- [CREATE] Writing System auto-memory: `project_newsletter_5page_template.md` - new project memory documenting the 5-page template, its structure, and its layout convention.

## Open questions / unfinished

- **Mick's final sign-off on v.01.04 still pending** - he was reading a printout during the day and may return with further content edits (most likely to the draft closing remarks, which were explicitly flagged as "for Mick to tweak").
- **Track 2 (HTML/WordPress) not started** - per the standard two-track workflow, this happens once the DOCX content is fully finalised. Not yet begun this thread.
- **Which DOCX is canonical going forward is slightly split**: Mick's `_DOCX_Mick.docx` carries his layout edit; Cedric's `_DOCX.docx` (no suffix) carries the same content built independently. Both now have the real feedback hyperlink applied. Worth clarifying with Mick whether he wants Cedric to standardise on editing his `_Mick` copy directly from now on, or keep producing a separate Cedric-built copy each time.
- **4-page master template is untouched** (per the do-not-overwrite rule) - only the new 5-page template reflects the divider convention. If Mick ever wants the 4-page master itself updated to match (e.g. if a future 4-page edition should also use dividers instead of page breaks), that would need an explicit ask, since the skill flags it as "do not overwrite."

## Next-thread pickup

- Opener phrase: "Cedric, resume from LATEST handover" (or "let's finish the newsletter" - same-day continuation, Mick is expected back this evening).
- First action: check whether Mick has any further edits from his read-through (especially the closing remarks). Once confirmed, the newsletter is ready to move into Track 2 (HTML production for WordPress) per the standard workflow.
- If Mick asks about the new 5-page template or the divider/hyperlink SOP changes, they're fully documented in the diy-newsletter skill and in the two memory files noted above - no need to re-derive.

## Content Studio logged

No Content Studio artefacts this thread - this was Writing System newsletter production and SOP/template work, not Dex/PAIDA infrastructure work.

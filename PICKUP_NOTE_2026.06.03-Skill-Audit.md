# PICKUP NOTE - Skill Dual-Write Audit
**Date:** 2026.06.03
**Author:** Cedric (Claude Desktop)
**Status:** PAUSED - resume after tonight's webinar
**Reason for pause:** Mick finalising webinar prep; no bandwidth for decisions today.

---

## ONE-LINE SUMMARY
A full audit of all skills across the 3 locations found heavy drift. 3 fixes are
done; the canonical model turns out to be ALREADY DOCUMENTED in memory (Dex + mirror);
a few items still need Mick's judgement. Full report: "2026.06.03 - Skill Dual-Write Audit.md".

---

## WHAT TRIGGERED THIS
While adding a "Click here for Report" CTA to a Coeur Mining (CDE) report image,
Cedric noticed the image-cta-overlay skill in the web mirror was STALE (old v1)
versus the correct v2.2 in the vault. Pushing v2.2 to the mirror raised the
question: have OTHER skills drifted too? Answer: yes, a lot.

---

## THE 3 LOCATIONS
1. MIRROR  = /mnt/skills/user/                                 (21 skills, web-only, no auto backup)
2. PRIMARY = C:\Vaults\Mick's Vault\.claude\skills\            (20 skills)
3. DEX     = C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\  (28 skills)

Of 12 skills that live in 2+ places, only 2 are byte-identical.

---

## IMPORTANT: THE CANONICAL MODEL IS ALREADY DECIDED (found in CEDRIC_MEMORY.md)
The "Mandatory Skill Deployment Protocol" in CEDRIC_MEMORY.md states the canonical
pair is:
  - Vault master: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\<skill>\  (DEX)
  - MCP mirror:   /mnt/skills/user/<skill>\
And SKILLS_REGISTRY.md (Dex vault root) is the declared source of truth for the mapping.

So "which vault is canonical" is NOT actually an open question - it is DEX + mirror.
The 2026.05.30 memory entry confirms portfolio-post-creator, benchmark-fetcher,
wordpress-image-uploader and wordpress-post-publisher were MIGRATED into Dex + mirror,
with the PRIMARY copies "left in place (not deleted)" - i.e. the PRIMARY copies are
explicitly LEGACY STRAYS, not canonical.

CAVEAT: in practice PRIMARY is still acting as the live source for at least annie and
image-cta-overlay (their correct/newest copies live in PRIMARY, not Dex). So the tidy
"everything canonical lives in Dex" model is not fully realised on disk yet. Honest
status: the model is decided (Dex + mirror); migration onto it is only partial.

---

## DONE THIS SESSION (no action needed)
1. image-cta-overlay: Mirror <- PRIMARY v2.2. VERIFIED MATCH (md5 6f5e4c5f).
2. annie: Mirror <- PRIMARY. VERIFIED MATCH (md5 9f133960).
   - Fixed a FUNCTIONAL BUG: mirror used dead tool names (list_gcal_events,
     find_free_time). Now uses Google Calendar:gcal_list_events etc. annie would
     have failed if loaded from the web mirror before this fix.
3. pdf-to-pptx-converter: Mirror <- DEX v1.1. VERIFIED MATCH (md5 fff2a7a3).

NOTE: all 3 fixes wrote to the MIRROR only (Claude container), NOT the Windows vault,
so they are NOT captured by any Dex git commit, and the mirror is not version-controlled.
If the mirror resets, these fixes are lost again. (See the mirror-scope concern below.)

---

## CRITICAL CONCERN: THE MIRROR MAY BE PROJECT-SCOPED OR RESETTING
On 2026.05.30 the four end-of-month skills were dual-written to Dex + mirror and
"verified byte-identical". Today, NONE of those four (portfolio-post-creator,
wordpress-post-publisher, benchmark-fetcher, wordpress-image-uploader) are present in
the mirror visible from THIS (Cedric) project.

Two possible explanations - needs clarifying before trusting the mirror:
  (a) The mirror is PER-PROJECT (the 2026.05.30 work was done in the Poster Pete project,
      so those skills are in Pete's mirror, not Cedric's). OR
  (b) The mirror RESET and lost them.
Either way this is the central fragility: the mirror is not a reliable store, and
"dual-write to mirror" does not guarantee the skill is there later. Same risk as the
15 mirror-only skills having no backup.

---

## REMAINING WORK (post-webinar)

### A. Re-establish canonical Dex+mirror for the four migrated skills
- DEX has the newest: portfolio-post-creator v2.3, wordpress-post-publisher v1.2
  (both gained 2026.05.30 tag rules), benchmark-fetcher v1.0, wordpress-image-uploader v1.0.
- Mirror copies are MISSING - recreate them from Dex (if mirror is the right scope here).
- PRIMARY copies are stale legacy (portfolio v2.2, wordpress v1.1) - delete or freeze
  as read-only backup, per Mick.

### B. Decide whether annie + image-cta-overlay should move to Dex (canonical)
They currently live canonically in PRIMARY. Under the documented model they "should"
be in Dex + mirror. Either migrate them to Dex, or formally record PRIMARY as a second
sanctioned master for these. Mick's call.

### C. Forked / no-clear-winner skills - need a manual pick
1. session-start (PRIMARY vs DEX) - GENUINE FORK.
   PRIMARY: v1.1, proper YAML frontmatter, dated 2026-03-12.
   DEX: no frontmatter, STILL USES THE OLD tool_search probe for environment detection,
   which CONTRADICTS the current protocol (Filesystem:list_allowed_directories).
   Pick PRIMARY's approach; the Dex detection method is out of date - do NOT keep it.
2. ai4inv-webinar-processor (MIRROR vs DEX) - parallel edits, no versions, mostly
   formatting (em dash vs ASCII). Quick manual pick.
3. notion-summary (MIRROR vs DEX) - different elaboration (21 vs 40 lines), no versions.
   ALSO clarify the namespace overlap with "notion-summary-generator" (mirror-only).

### D. Backup policy for the 15 mirror-only skills
cc1136-to-xero, content-extraction, diy-ai-logo-placement, ii-to-xero, key-takeaways,
linkedin-post, lse-news-checker, motion-design-prompt, natwest-to-xero,
notion-summary-generator, portfolio-risers-fallers, researcher-agent, title-generator,
twitter-thread, us-news-checker.
No disk backup anywhere. Decide whether to back these up to Dex. (Matches the parked
"14 online-only skills" item; count is now 15.)

---

## NON-ISSUES (verified, ignore)
- benchmark-fetcher (PRIMARY vs DEX): differ ONLY on the self-referential "Location (vault):"
  line - SUPPOSED to differ. Content identical.
- wordpress-image-uploader (PRIMARY vs DEX): same - only the Location line differs.
- yt-weekly-stats-v2 (MIRROR vs DEX): differ ONLY by em dash vs ASCII "--". Cosmetic.
- yt-play-button-overlay (PRIMARY vs DEX): identical.

---

## SKILLS ONLY IN ONE LOCATION (for completeness)
- PRIMARY-only (12, mostly Desktop/Obsidian skills, probably fine to not mirror):
  batch-approval-processor, empty-note-detector, epic-ticker-enricher, my-view-notion-writer,
  obsidian-frontmatter, sensitivity-scanner, sharescope-login, sharescope-logout,
  sharescope-screenshot, vault-file-mover, webinar-radar-extractor, youtube-research.
- DEX-only (18, confirm intentional):
  batch-process-webinars, logo-masking, micks-stocknote, micks-view-query, nina-to-notion,
  notebooklm-add-content, notebooklm-chat, notebooklm-notebook-setup, notebooklm-studio-output,
  paypal-to-xero, pns, process-webinar, sharescope-financials, sharescope-nlm-research,
  sharescope-start, thumbnail-play-button, week-plan-print, yt-inbox-sweeper.

---

## SUGGESTED ORDER OF WORK WHEN WE RESUME
1. Read SKILLS_REGISTRY.md (Dex root) - it is the declared source of truth and may already
   resolve several of the questions below.
2. Clarify the mirror scope question (per-project vs reset). This decides whether the
   mirror can be trusted as half of the dual-write pair at all.
3. Re-establish the four migrated skills in the mirror from Dex; retire PRIMARY strays.
4. Decide annie + image-cta-overlay home (migrate to Dex, or sanction PRIMARY).
5. Resolve session-start (drop old tool_search method), ai4inv-webinar-processor, notion-summary.
6. Decide backup policy for the 15 mirror-only skills.

---

## REFERENCE
- Full report: /mnt/user-data/outputs/2026.06.03 - Skill Dual-Write Audit.md (Mick downloaded)
- This pickup note: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\PICKUP_NOTE_2026.06.03-Skill-Audit.md
- Source of truth to consult first: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\SKILLS_REGISTRY.md
- Resume phrase: "Cedric, I'm back. Let's pick up the skill dual-write audit from the pickup note."

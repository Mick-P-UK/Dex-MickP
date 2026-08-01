# CEDRIC MEMORY
**Last Updated:** 2026.08.01 (Sat, Claude Code, afternoon 16:16) - END-OF-MONTH PORTFOLIO ROUTINE BUILT (capture done; posting started). This is the UPSTREAM capture that feeds the pre-existing End-of-Month Portfolio Posting routine (Poster Pete). NEW skill eom-portfolio-capture + SOP - End-of-Month ShareScope Capture (v1.0). ONE ShareScope login captures, for the month just ended: 4 Active 10 portfolios (current-holdings screenshot + month-scoped transactions image) + ASX (FTSE All-Share) and SP500 (S&P 500) 12-month charts at 1200x675 AND 1920x1080 (16:9 JPEG, period VERIFIED). Scripts in 04-Projects/2026.04.04-ShareScope-Automation: eom_capture_full.py (orchestrator; args YYYY.MM.DD, --commit to file into live folders, --headless for unattended), crop_transactions.py (OCR month-crop of the Cash statement), format_holdings.py (wrapper over skills/portfolio-formatter/annotate_portfolio.py), eom_capture_example.py (shared helpers). KEY MECHANICS: the four Active 10 portfolios are NOT pinned quick-buttons - select from the top-toolbar "Portfolios" dropdown, exact labels "0 - 0 - 2026 - Active 10 - UK / UK (Yr2) / US / US (Yr2)"; index charts via SEARCH (ASX=FTSE All-Share, GSPC=S&P 500), NOT the "FTSE All"/"US 500" top buttons (those open constituent LISTS); 12-month period is set AND verified; transactions have NO native date filter so are an OCR crop (scroll .trans-view-scroll-div to the bottom first for long Yr2 statements; OCR on a 3x-upscaled copy). HOLDINGS FORMAT (matches Mick's posts): trim to Total + grey frame + top-right box (red title "UK Active 10: 31st July 2026" + blue gain line) + bottom label box + BLUE underline under Cash + RED under Total (both BELOW the value). Percentages are TRUNCATED not rounded. annotate_portfolio.py patched: Windows Arial font + Windows Tesseract path + pound sign in gain line + blue Cash underline. Total OCR can MISREAD (UK Yr2 read 216182 not 16182.41; US 9310 not 9301.37) so TOTALS are passed verified. All 11 July images committed to the live DIY - Portfolios + Indices folders. POSTING (eom_post_drafts.py, Poster Pete WP app-password): UK Active 10 draft post 15585 created and matched to the June reference post. BENCHMARK BUG: Yahoo ^FTAS is STALE (last close 17 July) - use ShareScope's month-end (ASX 5836.47); benchmark-fetcher needs fixing. Registered in SKILLS_REGISTRY + _SOPs/INDEX (entry 8 capture, entry 9 the previously-unindexed posting SOP) + ShareScope-data-cmd-Reference. OPEN: verify UK draft; create the other 3 drafts (US Active 10 MID_YR1; UK Yr2 + US Yr2 MID_YR2 - US Yr2 has NO July transactions so gets a text line, not an image); log Meet Cedric; fix benchmark-fetcher; then wrap capture+posting into ONE overarching routine (Mick: it is a routine/SOP chaining skills, not one mega-skill) + optional headless Task Scheduler run in the early hours of the 1st. LESSON (Mick): match the PREVIOUS posts, do not reinvent formatting. Full detail: _handovers/LATEST.md.
**Last Updated:** 2026.08.01 (Sat, Claude Code, morning 10:56) - PORTICO-WE-PORTFOLIOS AUTOMATION BUILT (weekend PP1/PP2 snapshot + Slack post): two new skills + one SOP. (1) portico-snapshot - lifts the hardened sharescope_portico.py capture + annotate_portico.py formatter into a proper skill (capture PP1/PP2 -> house-style images -> portico_history.json week-on-week store); standalone, any day. (2) PPfolios-to-Slack - new slack_post_portico.py posts the finished images to #portico-portfolio-1 (C01H7ST4BDK) + #portico-portfolio-2 (C04GZAAPT9U) AS Mick via a Slack USER token (SLACK_USER_TOKEN=xoxp-, chat:write+files:write user scopes, app 'PPfolios Poster' in Portico Plaza) now in C:\Users\pavey\.env; converts PNG->standard-named JPG, drafts caption from a new phraseology reference + week-on-week delta, posts ONLY on Mick's go-ahead (real channels gated behind --yes; tested end-to-end to the private #cedric-private C0BMFLPKTHS). Both skills dual-written vault + C:\Users\pavey\.claude\skills (hash-verified); skills/README.md updated. (3) SOP - Portico-WE-portfolios.md (v1.0) in 06-Resources/SOPs + INDEX.md entry 7. Bases PP1 29,331.39 / PP2 50,000; percentages truncated 2dp. CAPTION RULE (Mick): images posted FIRST, video AFTER, so the #micks-diary pointer is forward-looking by default ('will shortly be available'). Meet Cedric brain dump logged (Notion 3afdb32a...). LIVE RUN DONE 11:42 BST - PP1 (70,044.43, down ~2,708 w-o-w) and PP2 (64,697.27, down ~622) posted to their member channels AS Mick with timed sign-offs. THREE FIXES the first live run surfaced (all permanent): (1) ensure_transactions_view() clicks data-cmd=ViewTransactions before selecting a portfolio (Mick's diagnosis - both PPs had failed 'selection not confirmed'); (2) annotate_portico.py font() now finds Arial on Windows (it was falling back to PIL's tiny default and IGNORING all label sizes - the cause of the wrong-looking labels); (3) pytesseract pointed at the Windows Tesseract install. TWO STANDING RULES: sign-off must carry the posting TIME before the date; any new ShareScope data-cmd goes into ShareScope-data-cmd-Reference.md the same session. NEXT: build the #micks-diary video-creation skill (Mick is making this week's video manually as the reference example). Full detail: _handovers/LATEST.md.
**Last Updated:** 2026.07.31 (Fri, Cowork-cloud, evening 18:55) - DITTY BOX YE 30.11.2025 JADE PACK COMPLETED AND ZIPPED. Found the missing 'outstanding items' list - it was never a chat message, it had been written to the checklist spreadsheet in the Z - For Jade folder on 26 July (LESSON: look for the artefact, not the thread). J11 had already been done by Mick but a modified-date sweep missed it because copies carry the SOURCE timestamp - in that folder compare J-refs, never dates. Mick posted the last manual journals and reprinted the three Xero reports; Cedric then cross-tied the pack: TB balances 266,352.67, loss 4,895.59 agrees to Current Year Earnings, net assets -198,998.29 agrees to capital and reserves, CC-1136 2,294.37 ties to J20, prior year 1,786.33 ties to J19, PayPal 234.38 ties to J18. THREE QUERIES RAISED: salaries 1,300 in the P&L against a single 500 payslip; J09/J09A dated 28 May 2026 rather than the year end; J19/J20 naming. DECISIONS: payroll evidence is NOT sent to Jade (payroll runs through Xero and she has access) - J24/J25 withdrawn, standing rule, do not rebuild next year; the checklist goes INSIDE the zip as J00 so Jade opens onto an index; withdrawn items are moved to a named subfolder and marked 'Not sent', never deleted. Pack = 25 items + J00, 9.8 MB, zipped and in the Z - For Jade folder with the covering letter in .md and .docx (modelled on the 26 June 2025 original). DB-Accounts-CW Session 14 committed AND pushed (2907a24). NEXT YEAR: take J09/J09A AT the year end date; the Balance Sheet is J23, not J33. OUTSTANDING: send the pack to Jade (only the e-mail is left); Hambledon Group pack not started. GAP FOUND: sundown-wrap exists in the vault skills folder but NOT in the Cowork skill store, so it had to be read from the vault by hand - same dual-deploy failure as image-cta-overlay this morning. A full skills-folder-vs-store sweep is warranted. Full detail: _daily/2026.07.31 - Sundown.md.
**Last Updated:** 2026.07.31 (Fri, Cowork-cloud, early afternoon 13:57) - CTA THUMBNAIL BAND STYLE AGREED + image-cta-overlay v2.0. Added a diagonal CTA to the 29 July webinar title-slide thumbnail ("Click HERE for PowerPoint PDF."). Plain bright green text read as a watermark, so on Mick's suggestion the text was put on a narrow angled rectangular band. Two variants offered (light grey vs charcoal); MICK CHOSE LIGHT GREY and asked for it to be stored as the standing option. HOUSE PRESET: light grey band (224,224,224 at alpha 240), mid-grey 3px border, bright green text (0,255,0) with a MANDATORY 3px dark outline (without it the green mushes on grey), soft drop shadow, corner-to-corner angle, 64px font on a 1366x769 thumbnail. Applies to diy-investors.ai monthly webinar thumbnails and any dark blue .ai Webinar slide; plain red text stays the fallback elsewhere. DISCOVERY: image-cta-overlay had NEVER been in the vault - it existed only in the Cowork skill store, so the dual-deploy rule had silently never been applied to it. Now written to skills/image-cta-overlay/SKILL.md (v2.0) and registered in SKILLS_REGISTRY.md + skills/README.md for the first time. OUTSTANDING: Cowork skill store still runs v1.0 until Mick uploads the delivered image-cta-overlay.skill via Settings > Capabilities; /mnt/skills/user/ mirror still pending; git commit rides the next daily-commit run (no git route from Cowork cloud this session - no folder mounted for device_bash). Full detail: _handovers/LATEST.md.
**Last Updated:** 2026.07.30 (Thu, Claude Code, evening 19:00) - EDV CORRECTION + NOTEBOOK CLEANUP: Ron's report had used STALE 30 April ShareScope figures (April CSVs left in the notebook); corrected to current 30 July figures and regenerated DOCX/PDF. NOT a currency error - ShareScope CSVs are USD. EDV notebook trimmed 97->43 (removed 24 stale April CSVs + 31 duplicates); April CSVs archived to the EDV base-data folder first. Two standing rules baked in (clear prior CSVs before Ron; archive-not-delete) in memory notebook-hygiene-per-company + SOP STEP 3.5. Logged an important next step: build a Ron OUTPUT-CHECKER (memory project_ron_output_checker). Full detail: _handovers/LATEST.md.
**Last Updated:** 2026.07.30 (Thu, Claude Code, morning 09:15) - EDV H1 2026 RESULTS: downloaded EDV Q2/H1 2026 results (5 PDFs) to the EDV Documents folder; added them plus 6 ShareScope CSVs (as text) and the 12-month chart to the EXISTING EDV NotebookLM notebook 57014b58 (renamed EDV - Endeavour Mining_Updated:2026.07.30, now 96 sources); Ron wrote the H1 2026 analysis (BUY into weakness), saved to 06-Resources/Research-Log/Research/EDV/2026.07.30 - EDV - Endeavour Mining - AI - Financial Analysis_v2.md; also built a formatted DOCX + PDF in the EDV folder. NEW RULE: on NBLM auth death, try a HEADED browser with stored Google creds BEFORE escalating to Mick (it auto-logged-in hands-free today). Full detail: _handovers/LATEST.md.
**Last Updated:** 2026.07.29 (Wed, Cowork-cloud, mid-afternoon 15:39) - PROMPT LIBRARY: third prompt added, NBLM-07 "Detailed Report for Novice Reader (Nina Sign-Off)". Supplied by Mick as a NotebookLM prompt while he was mid 29 July webinar preparation. Filed to all THREE places per the established workflow: source note 06-Resources/Prompts/NBLM-07 - Detailed Report for Novice Reader (Nina Sign-Off).md, operational C:\Vaults\Cowork\PROMPT_LIBRARY.md (INDEX row + PROMPTS block), and 00-Index.md regenerated (2 to 3 notes). Both files verified zero non-ASCII bytes. KEY STANDING FACT: AHK shortcode ::nb8# is RESERVED for NBLM-07 but NOT yet added to the AutoHotkey script (Mick to add). ::nb7# is NOT a free gap - Mick has a prompt already assigned to it that he has not yet passed to Cedric; do NOT reassign ::nb7# and do NOT renumber NBLM-07. When that prompt arrives it becomes NBLM-08 with ahk ::nb7#, so from here the CAT-NN code numbers and the AHK shortcode numbers deliberately no longer run in step (harmless - the CAT-NN code is the link key, the shortcode is only a typing trigger). OBSERVATION for Mick: existing NBLM-06 signs off with "London [BST]" which is wrong every winter; NBLM-07 says just "London" and is correct year round - candidate one-line fix to NBLM-06. Full detail: _handovers/LATEST.md.
**Last Updated:** 2026.07.29 (Wed, Claude Code, mid-afternoon) - GGP Q4/FY26 QUARTERLY ANALYSIS orchestrated (Nina notebook + Ron) end-to-end + new PROVISIONAL SOP. Added the 29 July GGP June-2026 Quarterly Activities Report (RNS) to the Greatland Resources notebook (7473143f, source ef481528); Ron authored an updated FY26 analysis bolting Q4 onto the prior quarters PLUS a 30-item calculations appendix. KEY: turnover is REPORTED not estimated (FY26 net revenue A$2,271m = gold 2,034 + copper 219); profitability built from real cost lines (site EBITDA ~A$1.42-1.45bn, EBIT ~A$1.28-1.30bn) with statutory NPAT deliberately left as a flagged GAP pending the audited FY26 accounts (~Sept 2026). Sourced REAL Apr-Jun 2026 commodity/FX data (gold Q2 avg ~US$4,513/oz, copper LME ~US$13,600/t, AUD/USD ~0.709) - saved to Claude Code auto-memory commodity-prices-q2-cy2026 for reuse; realisation cross-check confirms unhedged gold (~102% of spot) and copper sold net of TC/RC (~84% of LME). Compared vs the 6 July Nina view (production estimates within 0.5%, her chart-read prices within ~1.4%). Deliverables: vault markdown in NotebookLM-Queries + formatted DOCX + PDF in the GGP research folder (provenance footer, ASCII). NEW PROVISIONAL SOP - Quarterly Production Update (v0.9, awaiting Mick's review) at 06-Resources/SOPs + registered as entry 6 in C:\Vaults\_SOPs\INDEX.md; standalone quarterly-production-update skill to be built LATER against a live quarterly (Mick's decision). Full detail: _handovers/LATEST.md.
**Last Updated:** 2026.07.29 (Wed, Claude Code, afternoon) - GGP NOTEBOOK MARKER + two NotebookLM rules hardened. Pre-webinar check: NotebookLM (now Gemini Notebook) auth had failed at Token fetch; fixed hands-off via the Playwright cookie re-export from the CLI browser_profile (login attempt first wasted 2-3 min - see rule change). On the GGP - Greatland Gold notebook (7473143f, latest, updated 2026.07.06): queried it, wrote a dated point-in-time analysis-snapshot MARKER (as at 2026-07-06) covering thesis/assets/financials/catalysts/risks/valuation, added it as a text SOURCE inside the notebook (source fda4b9c9) AND saved a vault copy to NotebookLM-Queries\2026.07.06 - GGP Greatland Resources - Analysis Snapshot Marker.md, so future analysis can be diffed against it. RENAMED that notebook to "Greatland Resources_Updated:2026.07.29" (Mick flagged I first dropped the _Updated: convention suffix). TWO new MANDATORY rules added to C:\Users\pavey\.claude\_rules.md: (1) "NotebookLM auth - re-export cookies FIRST (post-rebrand)" - on ANY notebooklm auth failure go straight to the Playwright re-export, do NOT try `notebooklm login` first (it hangs post-rebrand); (2) "NotebookLM notebook naming convention" - every rename must carry `_Updated:YYYY.MM.DD` with today's date. Auto-memory notebooklm-login-detection-rebrand-fix.md + MEMORY.md index updated to match. PARKED (Mick's call): re-pointing sharescope_nlm_researcher.py preflight_auth_check() and Ron's agent-def "Auth fallback" at the re-export-first approach. Mick prepping for tonight's AI for Investing webinar with a backup plan. Full detail: _handovers/LATEST.md.
**Last Updated:** 2026.07.29 (Wed, Claude Code, midday) - PROMPT LIBRARY activated + first two prompts migrated. The 06-Resources/Prompts folder (dormant at 0 notes since 30 June 2026) is now live. Added SUM-01 (Notion Announcement Summary - posts a <=200-word structured RNS summary into the Notion Summary (item) field) and SUM-02 (Video Section Summary - timestamped bullet summary of an edited video, <=7 sections, <130 words). Each prompt lives in THREE synced places: source note in 06-Resources/Prompts/ (code-first filename, template frontmatter), the operational file C:\Vaults\Cowork\PROMPT_LIBRARY.md (INDEX row + PROMPTS block - what AutoHotkey and the demos read), and the generated catalogue 06-Resources/Prompts/00-Index.md. Codes are CAT-NN; categories NBLM/INV/SUM/CON/ANL/COM/WEB/GEN. SUM-02 was first filed as WEB-01 then recategorised to SUM at Mick's request. STANDING DECISION (2026.07.29): store prompts FULLY ASCII per the global rule - describe any required non-ASCII glyph in words (bullet as 'Unicode U+2022', arrows as '->', em dash as ' - '); de-mangle mojibake in pasted prompts first. SUM-01 overlaps the /pns skill (left standalone at Mick's request, cross-referenced). New auto-memory prompt-library-workflow.md written. NEW TASK ^task-20260729-001 (P1, Medium): bulk-migrate the many remaining prompts in a dedicated block. Full detail: _handovers/LATEST.md.
**Last Updated:** 2026.07.28 (Tue, Cowork-cloud, morning-midday) - AI4INV CORE MODEL INFOGRAPHIC built and themed + NEW SKILL pptx-editable-graphics. Built the concentric three-piece jigsaw infographic (Data / Storage / Wiki inside a gold binding ring inside an AI / User / PLACEHOLDER actor ring) for the 29 July AI for Investing webinar. Delivered flat PNG first, which was WRONG - Mick needs native editable shapes so he can drag pieces apart for build animations, recolour and retype live. Rebuilt as 16 native PowerPoint objects, then re-skinned to the .ai Webinar house palette read straight out of the live deck v1.03. NEW STANDING RULE now in memory: PowerPoint infographics are ALWAYS fully editable native shapes, never a flat image, unless explicitly asked otherwise. NEW SKILL skills/pptx-editable-graphics (SKILL.md + ppt_shapes.py + extract_theme.py + qa_render.py + references/themes.md + worked example), registered in SKILLS_REGISTRY.md and skills/README.md, tested end to end from a clean directory. KEY TECHNICAL FINDING: Mick's decks carry the STOCK Office 2007 colour scheme in ppt/theme/theme1.xml while the real branding lives in literal srgbClr values on the slides - always read the slide census, never the theme part. Also decided AGAINST using Claude Design for slide branding (it is a UI/design-system tool; the deck itself stays the single source of truth). OPEN: /mnt skill mirror sync; Inner Circle + Portico Plaza theme extraction (tasks 20260728-001/002, medium). Full detail: _handovers/LATEST.md
**Last Updated:** 2026.07.27 (Mon, Claude Code, afternoon-evening) - JUNE 2026 WEBINAR PROCESSED end-to-end + new SOP + skill fix (after restoring NotebookLM auth - see the line below). Ran the ai4inv-webinar-processor pipeline for the June edition (held 1 July 2026, postponed due to Mick's illness): uploaded the 57MB m4a to the "DIY.ai - Monthly Webinars" notebook (d3d6216b, audio source df09ec5a), generated a source-scoped 10-section user guide (`ask -s`), built the branded Word guide into the webinar Recordings folder, refreshed the index source (854bbadd) + Source Index note (4bc66b71) + index.md note + a new per-edition summary note, and renamed the notebook _Updated:2026.07.27. Phase B: generated the whiteboard past-tense explainer Video Overview "June 2026 Webinar Recap" (artifact 57c313ce) via `generate video --format explainer --style whiteboard --prompt-file`, reusing the prompt from Mick's Vault "0.0 - Inbox/2026.06.28 - NBLM Video Prompt (Webinar Summary).md" (May->June); downloaded the 35MB mp4 to Recordings as "...Recap_Unedited.mp4" through the authenticated browser profile (plain curl hits a Google sign-in). NEW "SOP - AI4Inv Monthly Webinar Processing.md" (v1.0) in 06-Resources/SOPs + registered as entry 5 in C:\Vaults\_SOPs\INDEX.md; UPDATED the ai4inv-webinar-processor SKILL.md to this CLI's real syntax (source add + `source wait`, NOT `--wait`; `source delete -y`, NOT `source remove --confirm`; no `note update` - delete + `note create --content -` stdin; `rename` title positional; `ask -s` scoping; Windows docx `require('docx')`+cwd not /tmp; Phase B video) + added the edition-vs-held-date rule. KEY: the EDITION month can differ from the file date (June edition held 1 July; two webinars fall in July - the 1 Jul June-edition and a separate 29 Jul edition). PENDING: /mnt skill mirror sync (Claude Code cannot reach /mnt); INDEX.md at C:\Vaults\_SOPs still has no git backup. Full detail: _handovers/LATEST.md.
**Last Updated:** 2026.07.27 (Mon, Claude Code, early afternoon) - NOTEBOOKLM CLI AUTH RESTORED + root cause of the login hang found (cross-surface note, applies in Claude Code / Desktop / Cowork / web). SYMPTOM: `notebooklm auth check --test` passed on cookies but FAILED at "Token fetch" (redirect to accounts.google.com); `notebooklm login` opened its Chromium and Mick was fully signed in and could see every notebook, but login detection NEVER fired - the window just sat until the 5-minute timeout (happened twice that morning). ROOT CAUSE: Google rebranded NotebookLM to "Gemini Notebook" at notebook.google.com; the CLI (notebooklm-py 0.7.3) waits to detect a signed-in state on the OLD notebooklm.google.com page, which no longer loads, so detection cannot complete and never writes storage_state.json. The Google session itself was fine - only the CLI's capture step is broken. FIX THAT WORKED (does NOT need Mick to re-login): the CLI persistent profile at C:\Users\pavey\.notebooklm\profiles\default\browser_profile already held a valid login; re-export its live cookies into storage_state.json with a tiny Playwright script (launch_persistent_context headless on that user-data-dir, goto https://notebooklm.google.com, verify it did NOT redirect to accounts.google.com, then ctx.storage_state(path=storage_state.json)); back up the old file first (storage_state.json.bak-reexport). Token fetch then passed (29 cookies) and `notebooklm list` worked. DEAD ENDS - do not waste time on them: `notebooklm login --browser-cookies chrome` needs rookiepy (a Rust extension with no prebuilt wheel for Python 3.14, which is the version notebooklm runs under here - the build fails with no cargo); browser_cookie3 installs fine but the CLI's --browser-cookies path does not use it. GOTCHA: two `notebooklm login` runs at once - the second dies exit 2 ("Opening in existing browser session"); stop the stuck task and kill any chrome.exe whose command line contains that browser_profile path before retrying. This SUPERSEDES the _rules.md "notebooklm login self-heals hands-off" assumption post-rebrand: go straight to the re-export. Also saved as a Claude Code auto-memory (notebooklm-login-detection-rebrand-fix). Longer-term proper fix: check for a newer notebooklm-py that understands the Gemini Notebook rebrand. Full detail: _handovers/LATEST.md (next wrap).
**Last Updated:** 2026.07.26 (Sun, Cowork-cloud, late afternoon) - PORTICO MEMBER REPORT project started. New Dex project: 04-Projects/2026.07.26 - Portico Portfolios - Performance Update (July 2026). Read ALL 8 Gemini Notebook Studio reports (NotebookLM renamed - now notebook.google.com; cloud Cowork CAN reach it via Chrome browser + JS extraction, CLI not needed for Studio artefacts). Member-attraction report outlined and approved: title 'How GBP 50,000 Became GBP 138,000 - The Portico Story', subtitle 'Beating the Market by Three to One'. MICK'S RULES captured: AI angle kept LIGHT (AI only used ~2 years, track record built on technique not technology); Portico Plaza = copies of real transactions within 24h, education NOT recommendations (Mick not FCA registered); members cherry-pick techniques to suit their own style; stop losses 'generally' - Mick admits holding too long sometimes. Ch1 Executive Summary APPROVED v0.2 (.md + .docx in project folder; doubles as promo video script). Ch2-4 drafted v0.1 awaiting Mick's review over next day or two. Key audited facts: GBP 50k net invested -> GBP 138,071.80 (25.07.2026), +176.14%, CAGR 16.94% vs All-Share 5.35% price-only (dividends caveat drafted into Ch3 for Mick's decision; FTSE CAGR recomputes 5.33); 17 of 160 stocks doubled (1 in 9); Nanosynth 345.3% in 36 days. NEXT: Mick reviews Ch2-4 one at a time, then Ch5-7; Ch10 needs Inner Circle / Portico Plaza tier offer details from Mick. Voice source: Mick's-Writing-System context/core/voice-dna-mick.json. Full detail: _handovers/LATEST.md.
**Last Updated:** 2026.07.26 (Sun, Cowork-cloud, early afternoon) - RESUMED from LATEST handover (Ditty Box accountant pack) and closed the three infrastructure loose ends. (1) SOP REGISTERED: SOP - Ditty Box Ltd Year End Accounts added to C:\Vaults\_SOPs\INDEX.md as entry 4 (v0.9 DRAFT, status caveat + [CONFIRM] warning included) - the mandatory final step is now done; this session's Filesystem allowlist covered C:\Vaults so the previous block was gone. (2) FOOTER MIRROR: found the Spreadsheet Print Footer rule ALREADY present in C:\Users\pavey\.claude\_rules.md - no action needed, pending item closed. (3) GIT COMMITTED: vault committed from the Cowork device VM via the C:\Vaults mount - commits 5c4b1ef (27 files, the whole accountant-pack session) + e265930 (changelog). CRITICAL TECHNIQUE for next time: git through the VM mount shows EVERY file as modified (CRLF/LF phantom diffs) - always run git with -c core.autocrlf=true from the VM or a commit would rewrite line endings vault-wide; also the mount CANNOT delete files, so git leaves its own .lock files behind (index.lock/HEAD.lock) - move them into _to_delete/ to unblock (a stale ORIG_HEAD.lock from 11 Jul was also cleared). PUSH still blocked from the VM (no SSH route to github, port 22 forbidden) - the two commits ride the next daily-commit push or a manual push by Mick. _to_delete/ in the vault root holds the moved lock files for Mick to bin. STILL OPEN: five pack items (J11, J19-J23) on Mick, SOP's 7 questions, paypal-to-xero promotion decision, baton-wrap bulletproofing amendment. Full detail: _handovers/LATEST.md.
**Last Updated:** 2026.07.26 (Sun, Cowork-cloud, morning-midday) - DITTY BOX YEAR-END ACCOUNTANT PACK built + packaged as a skill + SOP written. Assembled the YE 30.11.2025 pack for Jade: derived the manifest from last year's pack (the J-numbered FILENAMES in 01_YE 30.11.2024\Z - For Jade_YE_30.11.2024\For sending 2 Jade are the real record - the checklist xlsx in that folder was only ever filled to line 1), mapped J01-J25 against 400+ files across ~30 sub-folders of 001_YE 30.11.2025, copied 21 items with device_bash cp -p on Mick's own disk, MD5-verified every copy, confirmed all 408 originals still in place. 5 items OUTSTANDING and only Mick can make them: J11 ii portfolio at 30.11.2024, J19+J20 Halifax CC-1136 opening/closing balance grabs, J21+J22+J23 Xero Trial Balance / P&L-with-codes / Balance Sheet prints. J24+J25 (payslip, PAYE setup) added as new items at Mick's choice; he declined Manual Journals, Amazon schedule and Dir Loan docs as extras. KEY INSIGHT for next year: filenames carry the PRODUCTION date not the period covered, so the YE 30.11.2025 opening-balance statement is a file named 2026.05.27 covering 30.11.2024 - match on period, never on prefix. NEW STANDING RULE: Mick's spreadsheet print footer `(&Z&F - Printed: &D at &T)` = `(&[Path]&[File] - Printed: &[Date] at &[Time])`, LEFT section, EVERY worksheet, odd+even+first variants, brackets ARE literal - added to CLAUDE.md USER_EXTENSIONS (survives /dex-update) and to cross-surface preferences; MIRROR STILL PENDING at C:\Users\pavey\.claude\_rules.md (out of session scope). NEW SKILL info-for-accountant (vault skills/ + .skill file delivered): SKILL.md + reference/manifest.md (J01-J25 with search hints) + scripts/build_checklist.py; designed to DERIVE the manifest from the prior year's pack each year rather than hardcode, so it self-updates; knows the 2024 pack's defects (a J33 that should be J23, a truncated duplicate J04) and will not copy them forward; /mnt/skills/user mirror NOT possible from Cowork cloud. REGISTRY FIX: SKILLS_REGISTRY.md was stale since 2026-07-19 and had NEVER listed any of the six accounts skills - all six now registered; discovered paypal-to-xero is VAULT-ONLY (its four siblings are Cowork-visible), flagged not fixed. NEW SOP: 06-Resources/SOPs/SOP - Ditty Box Ltd Year End Accounts.md, v0.9 DRAFT - none existed; the whole year-end process lived only inside SKILL.md files, executable but not readable. Reverse-engineered from the six skills and two years of working folders; steps 1/2/6 solid, reconciliation step is inference; 7 [CONFIRM] flags and 7 open questions at section 12 pending Mick's walkthrough before v1.0/active. BLOCKED: the SOP could not be registered in C:\Vaults\_SOPs\INDEX.md (outside this session's Filesystem allowlist); the folder-access dialog failed because the desktop window was unavailable. Also PENDING: git commit/push (no shell access to the vault from Cowork cloud). Full detail: _handovers/LATEST.md.
**Last Updated:** 2026.07.25 (Sat, Cowork-cloud, afternoon-evening) - Portico ShareScope capture HARDENED by driving ShareScope live via the Playwright MCP on mick-pc25, plus baton-system recovery, plus PP1/PP2 weekend images delivered. ROOT CAUSES of the long PP1-wrong/PP2-right bug (all now in ShareScope-data-cmd-Reference.md 'View-state verification'): (1) 'Current holdings' (data-cmd ViewCurrentOnly) is a TOGGLE current<->full, NOT a set, and each portfolio REMEMBERS its own state - an unconditional click flipped PP1 to full and PP2 to current; (2) the button 'active' class is useless (sits on BOTH tabs) - the reliable signal is which grid caption is actually PAINTED ('List of current holdings' vs 'List of holdings'); (3) the view must be read only AFTER the list finishes loading (PP1's long list ~3s in a fresh context; reading mid-load catches a lingering caption). FIXES in sharescope_portico.py (compile+ASCII clean, in vault): select_portfolio verified+retrying (match 'PPx (UK)' EXCLUDING the 'Port:' CurPort indicator, confirm against the panel header, raise on fail - validated live); ensure_current_holdings toggle-aware (only toggle when the SETTLED view is full) + network-idle settle + caption-painted verify + stable re-check; capture_panel re-verifies right before the screenshot. CAVEAT/OPEN: on a SLOW load the caption did not paint within retries and PP1 still captured full (18:39 run, verified by eye); PP2 reliable. Next fix: load-independent signal - detect CLOSED positions (Shares=0 rows, only in the full view; grid rows are DOM div.list-row in div.list-content-fixed) OR auto-retry on the run's error flag. DELIVERED today: PP1 + PP2 finished house-style weekend images to portico/outputs/ (PP2 from the 18:40 clean run; PP1 from a verified earlier live current-holdings capture cropped+formatted, since the run's PP1 was full; both verified by eye; PP1 total 72,752.54 +148.03%, PP2 65,319.26 +30.63%). BATON SYSTEM: recovered stale LATEST.md, wrote post-mortem + hardening spec (freshness guard, archive-first/verify-after, run vault SKILL.md directly when the Cowork registry omits it) - STILL PENDING: amend skills/baton-wrap/SKILL.md + Mick uploads to Cowork+web. LEARNINGS: drive the real UI early (5 blind reruns taught less than 1 live session); verify the SETTLED rendered result, not a click or momentary signal; know control semantics (toggle != switch, state remembered per context); when DOM and pixels disagree the pixels win; fail loud. NOTE: clearing the automation browser's localStorage while probing reset THAT browser's ShareScope layout only (Mick's normal ShareScope + the script's fresh context both verified intact). Full detail: _handovers/LATEST.md.
**Last Updated:** 2026.07.23 (Thu, Claude Code, late afternoon) - ShareScope pre-webinar hardening. Closed the three outstanding ShareScope items ahead of next week's AI for Investing webinar, then added three fixes. (1) WATCHER RESTART: old pid 2328 long dead (recycled to svchost); a fresh watcher was already on current code; restarted cleanly regardless (final pid 27076, registered in Windows startup, live NLM auth verified). (2) JSE TIDY: removed the erroneous chart image source 2a9c622c from JSE notebook cfd84684 (18->17 sources, remaining all legit) and deleted the 4 superseded local JSE debug PNGs (kept the canonical 17:30 that the report chart_source points at). (3) END-TO-END TEST PASS on USAS (Americas Gold and Silver Corp, NYSE American/TSX, USD): enriched the EXISTING USAS notebook b8835808 (kept Mick's 2 prelim sources), the watcher ran CSV->chart->NLM prep->next_action, and Ron produced a clean v2 report (verified 0 non-ASCII bytes, 0 HTML entities, chart embedded, market hand-corrected to US/USD; verdict HOLD / Speculative Buy on a hold of 3.50 dollars). Then at Mick's request: NO-FLASH FIX - the flashing black boxes were the notebooklm CLI console windows (NOT the browser); added creationflags=CREATE_NO_WINDOW to all 5 notebooklm/subprocess call sites (run_nlm in sharescope_nlm_researcher.py + nlm_notebook_manager.py, the live auth check in notebooklm_auth_monitor.py, and 2 watcher orchestrator calls) - committed aef1165. HEADLESS: set true then REVERSED to false - Mick WANTS the ShareScope browser VISIBLE for the webinar demo; visibility and the flash fix are independent (SHARESCOPE_HEADLESS=false in C:\Users\pavey\.env only, gitignored, not committed). SINGLE-SESSION BOOKEND RESTORED: the pipeline was logging in TWICE (CSVs via sharescope_orchestrator, chart via sharescope_chart_orchestrator); the original bookend runner sharescope_session.py still existed but the watcher bypassed it. Created a thin wrapper sharescope_session_orchestrator.py around run_sharescope_session(financials+chart) and re-wired the watcher to ONE run_session() call (old orchestrators kept as fallback). Validated LIVE via a full watcher test on USAS - watcher log shows exactly ONE login and ONE logout, all 6 CSVs + chart captured inside, 25s; run_complete logins=1/logouts=1 (committed 368f84a: watcher + new orchestrator + sharescope_session.py which was previously untracked). Mid-session the NBLM "auth-lie" appeared and self-healed hands-off (notebooklm login -> "Already logged in."). OPEN: US-stock MARKET MIS-CLASSIFICATION (US stocks tagged market:"UK" - task chip task_d0889bb3, webinar-relevant; Cedric offered to fix, Mick chose to wrap so STILL OPEN); ShareScope repo STILL has no remote (both commits local only); untracked pipeline files (sharescope_chart.py etc.) + a stray corrupted-name ZPHR file (repo hygiene, fold into backup task); pre-existing harmless logout "NoneType ... stop" warning + empty session_*.log (both cosmetic). Full detail: _handovers/LATEST.md.
**Last Updated:** 2026.07.23 (Thu, Claude Code, afternoon) - CREI retro CLOSED + Ron/SOP auth self-heal alignment shipped + pad-slide-numbers skill built. REMINDER (backup gap): the Cowork vault C:\Vaults\Cowork\ is NOT a git repo, so the CANONICAL ShareScope SOP (3-SKILL-sharescope-nlm-research.md) and everything else under C:\Vaults\Cowork have NO off-machine backup at all - resolve as part of the C:\Vaults backup strategy decision (task_c3efead7), alongside the dedicated ~/.claude repo and the ShareScope-Automation private remote. CREI retro: all five findings resolved - verdict drift (baked "lead with stable price levels + chart date, treat the single BUY/HOLD/SELL word as secondary" into Ron's template); auth-canary lie + balance-sheet transport timeout (both verified fixed in sharescope_nlm_researcher.py from the morning); P&L HTML-entity leak (NOT a bug - Ron's markdown + template are clean, was a Notion-render artifact, spot-check next push); Ron subagent-type now registers. Auth self-heal wording aligned across all four byte-identical ron.md copies (hash 8afcc13) + the canonical ShareScope SOP (Cowork, 4 spots) + both vault SKILL.md mirrors: auth failure now tries hands-off `notebooklm login` FIRST, escalating to Mick only if the browser-profile session is dead. Committed + pushed Dex-MickP 658fe25 (2 ron.md tracked copies + 2 SKILL.md mirrors; surgical - unrelated working-tree files left alone). Earlier today: built + shipped the pad-slide-numbers skill (zero-pads exported slide filenames Slide1.PNG -> Slide01.PNG; auto-width, idempotent, collision-safe; dual-written vault skills/ + ~/.claude/skills, committed 0dc5dad; /mnt/skills/user mirror still pending a Desktop/Cowork session). LATEST.md updated to mark the retro closed. Full detail: _handovers/LATEST.md.
**Last Updated:** 2026.07.23 (Thu, Claude Code, early morning ~07:00) - Config-loading fixes + NBLM auth self-heal + off-machine backups. Session ran in the C:\Vaults working directory (Claude Code). Diagnosed the class of "config that loads in claude.ai but not Claude Code": a C:\Vaults-rooted session auto-loads ONLY user-level ~/.claude (CLAUDE.md + @_rules.md) and the working-dir-root C:\Vaults\CLAUDE.md - NOT nested-vault .claude/ folders (memory claude-code-config-loading-mick-vaults). Fixed the intermittent greeting: vault Dex-MickP\CLAUDE.md block now CANONICAL + version-stamped v2.0, a MIRROR added to ~/.claude/_rules.md (PowerShell London-time check vs the vault's Python) so it loads every Claude Code session, CEDRIC_MEMORY London Time Protocol slimmed to a pointer to stop drift (Mick committed as f56af67, pushed). Ron sub-agent had the SAME root cause - ron.md only in the two nested vault .claude/agents/ folders, so subagent_type ron never registered in a C:\Vaults session; fixed by copying the byte-identical canonical (all 3 copies MD5-verified) to user-level ~/.claude/agents/ron.md (registers next session; restart pending for this one). CREI housekeeping: deleted stray untagged/error balance_sheet source 50761844 from notebook 53fd542b (6 [PIPE] sources intact); added a 3-attempt/5s-backoff transport-timeout retry loop around ADD_SOURCE in sharescope_nlm_researcher.py (py_compile OK, 0 non-ASCII; ShareScope repo commit ba053d1, LOCAL ONLY). BONUS best fix: Mick's experiment firing notebooklm login from Cedric's shell revealed it self-heals hands-off ("Already logged in.") when the CLI's persistent Chromium profile is still valid - baked into preflight_auth_check() (auto-login + re-verify before halting) AND a new _rules.md rule, so Mick is only asked to log in when the browser-profile session is actually dead. Backups: ~/.claude had NO version control - snapshotted the 5 core config files (CLAUDE.md, .CLAUDE.md, abbreviations.md, _rules.md, agents/ron.md) into Dex-MickP\System\claude-config-backup\ (secret-scanned clean), committed 622b562 and PUSHED (interim SNAPSHOT, goes stale on edit); dedicated ~/.claude repo raised as an URGENT task (~2026-07-26). ShareScope-Automation is a separate nested repo (branch post-webinar-dev) with NO remote - URGENT task raised to add a private GitHub remote (~2026-07-26). Confirmed Cedric CAN run git directly in Claude Code on Mick's PC (old "cannot" note was Cowork/Desktop-era). Meet Cedric episode "The Case of the Missing Good Morning" drafted to 00-Inbox + created in Notion Content Studio (3a6db32a9b0a81c2bf53cb6ee7241f59, Draft). Two learnings saved to the Claude Code memory system (claude-code-config-loading-mick-vaults; verify-git-state-before-committing) + new MEMORY.md index. OPEN: CREI retro (item 1) not done - 3 of 5 findings remain (verdict drift; P&L HTML-entity leak; Ron restart); align Ron agent-def + SOP auth step to the self-heal. Full detail: _handovers/LATEST.md.
**Last Updated:** 2026.07.22 (Wed, Claude Code, midday) - CREI research end-to-end + Ron chart-embed rule baked in + Obsidian URI fix (strip .md) baked into pipeline + NEW SOP INDEX created at C:\Vaults\_SOPs\INDEX.md (vault-neutral) + new global rule "consult SOP index FIRST on any operational request" added to _rules.md. Session ran in Mick's-Writing-System vault. Started with a CREI (Custodian Property Income REIT) research request - I initially misfired on skill selection (loaded `sharescope-nlm-upload` when the request needed the full `sharescope-nlm-research` pipeline). Mick corrected: "you developed exactly that automatically a couple of days ago". Discovered the SOP v2.0 at C:\Vaults\Cowork\ShareScope-Project-Setup\3-SKILL-sharescope-nlm-research.md via the prior handover, then ran the pipeline properly: Cedric ran both ShareScope scripts directly via PowerShell (orchestrator 18.7s -> 6/6 CSVs; chart 17.6s -> 12-month PNG at 1200x675), fired Nina in background (~5min, notebook 53fd542b-e797-48cb-a6bc-7c0d0b4d74ef created, 6 CSVs + 10 news sources), spawned Ron via `subagent_type: "ron"` with 7-line per-run prompt, Ron used 8 tool uses in 8min, returned BUY-rated report with full TA. Report saved as v2 at 06-Resources\Research-Log\Research\CREI\2026.07.22 - CREI - Custodian REIT - AI - Financial Analysis_v2.md; Notion Research Database entry created https://app.notion.com/p/3a5db32a9b0a816db613ff7abda17cb1 with Cedric's Report tag + relations to the existing Custodian Property REIT ticker page. Mid-run Mick asked me to make sure Ron embeds the 12-month chart PNG at the top of the Technical Analysis section (not leave it to Mick to hand-embed) - sent a live nudge to Ron via SendMessage (successful embed) AND baked the rule permanently into ron.md in BOTH vaults (mandatory embed via Obsidian wikilink `![[filename.png]]` filename-only + italic caption line) AND saved feedback memory `feedback_ron_embed_chart.md`. Post-report Mick reported the Obsidian link in my output wasn't clicking - investigated, both `%20`-encoded and raw-spaces variants worked via Win+R, but the .md extension was the blocker. FIXED `_make_obsidian_uri()` in sharescope_nlm_researcher.py to strip .md before URL-encoding (comment references today's diagnosis); compile-verified. Saved feedback memory `feedback_obsidian_uri_format.md`. Mick then raised the deeper question: I hadn't found the ShareScope SOP automatically at session start - proposed adding a rule to CLAUDE.md pointing at an SOP index. Discussed: made it generic (any operational request, not just stock-research), triggered by task-shape (produce/publish/run/analyse etc.) not by user naming an SOP (I initially wrote the rule as "when the user says there's an SOP" - Mick correctly called out the circularity: if I don't check the index I can't know an SOP exists). Built the fix: `_rules.md` gets a new section "SOP index - consult FIRST on any operational request" that fires on task shape and reads the index before any other tool call. INDEX FIRST created at C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\_SOPs\INDEX.md, then MOVED (per Mick's follow-up architectural point) to C:\Vaults\_SOPs\INDEX.md - vault-neutral parent-folder location, doesn't privilege any one vault, matches that SOPs cross vault boundaries. Old Dex-scoped location deleted, `_rules.md` path updated. Index seeded with the two active SOPs (ShareScope + Ron pipeline; Freedom Blueprint newsletter v2.0) plus a "planned but not built" section for the docx-to-html skill, Writing-System GitHub backup, and the newly-open C:\Vaults backup strategy question. Backup decision explicitly spawned as its own task chip (task_c3efead7) - options being weighed: (1) one meta-repo, (2) per-vault repos + standalone _SOPs repo, (3) hybrid; Cedric recommendation option 2 or 3. Related still-open items to bundle with that decision: ShareScope-Automation private remote (open since 2026-07-11), Writing-System GitHub backup (planned, memory `project_github_writing_system`). Ron's earlier report had one `&amp;` HTML entity in "P&amp;L Analysis" - fixed to `P&L` before writing to vault. All today's vault edits (report, CEDRIC_MEMORY.md, baton archive, LATEST.md, Ron agent def, `_rules.md` at ~/.claude, new C:\Vaults\_SOPs\INDEX.md) ride the 9pm sweep for Dex-MickP; the ron.md edit in the Writing-System vault, feedback memories, and new C:\Vaults-level index are NOT covered by any current git backup (all part of the deferred backup decision). Watcher pid restart from the 2026-07-21 handover is STILL not done - process still runs the pre-SOP-v2.0 code; not blocking today's manual-triggered CREI run but the voice-triggered path remains untested against the new code. All CREI-day-artefacts confirmed: notebook, CSVs, chart PNG, Nina populated, Ron v2 report, Notion entry, chart embed rendering (per SendMessage nudge). Verdict on the day: infrastructure change (SOP index + rule) is arguably more valuable than the CREI report itself - it prevents the exact skill-misfire that started the session from ever happening again. Full detail: _handovers/LATEST.md.
**Last Updated:** 2026.07.21 (Tue, Claude Code, day-close) - ShareScope Pipeline v2 SHIPPED. Two threads today. Morning/afternoon thread (baton 14:35) codified SOP v2.0 for the ShareScope + NBLM + Ron pipeline as the new source of truth at C:\Vaults\Cowork\ShareScope-Project-Setup\3-SKILL-sharescope-nlm-research.md (~330 lines, includes Appendix A mandatory report template and Appendix B changelog). Fixed `_make_obsidian_uri()` in sharescope_nlm_researcher.py to emit `vault=Dex-MickP&file=<url-encoded-relative-path>` (the working format on Windows) with a fallback to `path=` if the report sits outside the vault root. Investigated the yesterday-flagged "Ron sub-agent NBLM CLI auth quirk" and found it was a MISDIAGNOSIS - the real cause is genuine Google session invalidation which the notebooklm_auth_status.json cache CANNOT see (the cache measures cookie EXPIRY not VALIDITY, and the auth monitor's live check runs only every 6 hours, so the cache can lie for up to 6 hours after Google invalidates). Fix when it happens: `notebooklm login` in a browser (needs Mick). Defined Ron as a PERMANENT named agent: `.claude/agents/ron.md` written in BOTH vaults (Mick's-Dex-2nd-Brain\Dex-MickP\.claude\agents\ and Mick's-Writing-System\.claude\agents\) so Ron is available as `subagent_type: "ron"` from any Claude Code session started in either vault. Full identity, mandatory report template, UK/US market conventions, hard rules (UK English + ASCII only, sign off as Ron), auth fallback. Harness picked him up live without a restart. Ran a full ENQ end-to-end validation using every new fix in one go: Cedric-runs-both-scripts (orchestrator + chart), Nina prepped notebook, Ron spawned via subagent_type: "ron" with a MINIMAL 7-line prompt (vs the ~60-line inline prompt via general-purpose the previous day), Ron ran in 9 min using only 10 tool uses (vs 26 yesterday), returned comprehensive report with proper multi-indicator TA. Saved as ENQ v2 dated 2026.07.21 with proper frontmatter and working Obsidian link. Afternoon/evening thread (baton 18:39) - Mick asked to work through the entire five-item next-action list from the 14:35 baton in one pass, then commit immediately. Delivered all five: (1) preflight_auth_check() helper added to sharescope_nlm_researcher.py + wired before Step 0 (halts pipeline with clear "run `notebooklm login`" message if the canary fails - closes the up-to-6-hour cache-lie window), (2) module-level `SKIP_LEGACY_V1_REPORT = True` constant + refactored run_nlm_research() tail so Nina's ask + save block is conditional, with the notebook title-rename step moved outside so it always runs (Ron needs the fresh "_Updated_YYYY.MM.DD" title), (3) fixed page.press('Control+Shift+L') -> page.keyboard.press('Control+Shift+L') in sharescope_logout.py line 77 (silences the "Logout failed: Page.press() missing 1 required positional argument: 'key'" cosmetic warning), (4) added run_chart_orchestrator() helper to sharescope_watcher.py, wired chart step in as Step 2b, added result["next_action"] on run_complete payload with three explicit forks (documented that the watcher CANNOT invoke Ron - named sub-agents only exist inside a Claude Code session - so it stops at "notebook + chart ready" and hands off), (5) backfilled TWO Notion Research Database entries (title convention `YYYY.MM.DD - [Company Name] ([TICKER]): Ron's Analysis`, `Cedric's Report` Tag, EPIC + Company/Source Name relations, userDefined:URL as obsidian:// deep link back to vault): JSE Ron v2 https://app.notion.com/p/3a4db32a9b0a819ea59bcfe96b25d28a and ENQ Ron v2 https://app.notion.com/p/3a4db32a9b0a81afa78ece40d501d945. Data source id ac552ce5-2ceb-4ffb-a502-7d5da6c67cf8. IMMEDIATE COMMIT (Mick's request, not waiting for 9pm sweep): ShareScope repo `post-webinar-dev` 42f2fd5 (3 files, +916/-151, LOCAL ONLY - no remote, ShareScope-Automation still needs its own private repo per the July personal-backup open item) covering the three script edits only. Dex-MickP repo `main` 4ca4235 (19 files, +978/-62), pushed clean 9ade3da..4ca4235 origin/main, includes Ron's agent definition, both today's baton archives (14:35 + 18:39), ENQ v2 + v1 safety-net + JSE v2 docx, LATEST.md, Companies/ENQ profile bump, _index.md ENQ bump, plus ambient daily gmail-sweep intake. Working tree clean end-of-day. OPEN: RESTART the ShareScope watcher (pid 2328) so the SOP v2.0 code takes effect (running process still has old code loaded); the voice-triggered watcher path is now Ron-aware in code but end-to-end validation on a real voice trigger is still pending; the ShareScope repo private remote is still an open task. Full detail: _handovers/LATEST.md. Also 2026.07.20 work (Ron pattern restored + chart 12m fix + JSE report v2, baton 17:40 archived) is captured in yesterday's LATEST.md archive rather than a memory entry (yesterday's edits rode the 9pm sweep as normal).
**Last Updated:** 2026.07.19 (Sun, Claude Code, late afternoon) - July newsletter PUBLISHED live end-to-end + newsletter-wp-publisher skill built + Newsletter SOP v2.0 rebuilt (md/txt/docx). Session ran in Mick's-Writing-System vault, continuing directly from the 2026.07.18 17:01 handover (v.01.07 FINAL, still carrying placeholder image/PDF/cross-link URLs). Mick asked whether the whole WordPress publish step could be automated via Poster Pete instead of him uploading images and swapping URLs by hand; confirmed the wordpress-image-uploader and wordpress-post-publisher skills (Dex vault) work identically from Claude Code (direct .env/disk access, no Filesystem MCP needed despite their "Claude Desktop only" note being stale). Located all 6 local images + the final PDF (one image, the Investor Psychology video thumbnail, had never been saved standalone - extracted from the FINAL docx via PowerShell ZipFile.ExtractToDirectory, identified visually, saved properly). Uploaded all 7 files to the diy-investors.com media library and pushed the resolved HTML onto Mick's existing draft (post 15514, content-only update, status left as draft) - Mick then previewed and published it himself, and sent the member email. Mick asked to turn this into a proper reusable skill, future-proofed for a possible second newsletter on diy-investors.ai: built newsletter-wp-publisher (Dex-MickP\skills\newsletter-wp-publisher, SKILL.md + scripts/publish_newsletter.py) - manifest-driven (not folder-scanned, unlike the portfolio skill, because newsletter filenames aren't convention-locked enough), multi-site aware via a SITE_KEYS table, supports both update-existing-draft and create-new-draft modes, always hardcodes status=draft, aborts before writing/pushing if any placeholder is left unresolved. Confirmed WP_DIY_AI_URL/USER/APP_PASSWORD already exist in .env from the portfolio-posting work, so diy-investors.ai is wired but explicitly flagged UNTESTED. Registered in SKILLS_REGISTRY.md; wired into diy-newsletter SKILL.md as new workflow step 10a plus two Cycle Learnings entries; resolved the previously-open "Cedric cannot verify live WordPress posts" issue note (partially - REST API read now works, visual browser rendering still doesn't). Finally, rebuilt the newsletter SOP from scratch as a checklist (Mick had started one in April 2026, v1.0 docx, fixed at 4 pages with publishing fully manual - found via a parked June pickup note asking for exactly this): new v2.0 at Mick's-Writing-System\0.0 - Inbox\, produced in three formats (.md source of truth, .txt for reading, .docx with mandatory provenance footer) covering all 8 phases including the new publishing automation. Writing System auto-memory updated: project_july_newsletter.md (PUBLISHED section added), new project_newsletter_wp_publisher_skill.md, new project_newsletter_sop.md, MEMORY.md index. Full detail: _handovers/LATEST.md.
**Last Updated:** 2026.07.16 (Thu, Claude Code, late morning) - July Freedom Blueprint Newsletter v.01.03 diff applied + Investor Psychology article rewritten in Mick's voice. Session ran in Mick's-Writing-System vault, not Dex. Mick uploaded his edited v.01.03 .docx (worked directly in Word) including a brand new "Investor Psychology (can you handle a downturn)?" section he had drafted via Descript's AI tool - flagged upfront as not being in his voice. No docx-to-text skill exists yet (project_docx_to_html_skill still parked), so used python-docx directly (confirmed installed) to extract paragraph text from the .docx and diff it against the last working TXT (v.01.02). Applied every substantive change: signature date, feature headline tweak ("Burnham's In" -> "Burnham's (almost) In"), GBP/USD symbol-to-text swaps per the vault's ASCII rule, a purchase-date clarifier on the Goldplat gain, a new UK-vs-US portfolio comparison paragraph (cleaned a curly apostrophe that had crept in), the ACM Research exit's overall gain + resulting cash balance, and removed a resolved internal editorial note. Rewrote the Investor Psychology article from scratch using voice-dna-mick.json + the diy-newsletter skill: kept the same five subheadings (Illusion of Rationality, Loss Aversion and Panic Selling, Myth of Quick Recoveries, Building Resilience, Automation and Perspective Shift) but replaced the generic AI content with Mick's first-person register, British understatement, and concrete grounding (2008 crash, Great Depression, Buffett buy-the-dip framing) - now Page 4, wrap-up pushed to Page 5. Mid-session Mick flagged two new "Yr2" portfolio images added to Newsletter-Images the previous day; asked whether to add Year 2 portfolio sections to Page 3 - Mick said leave them out, Page 3 stays with just the two Year 1 portfolios. Verified the finished draft 100% ASCII-clean via a Python scan. Newsletter has grown from 4 to 5 pages this month (~1,450 words drafted so far vs the usual ~1,050 target) - same pattern as the content-heavy June edition. Session paused at Mick's request (baton-wrap) to resume this evening; Page 5 wrap-up (closing remarks, webinar date - the 8th July placeholder is stale, Boot Camp/events) is the only piece still outstanding. New draft: knowledge/drafts/2026.07.16 - Freedom Blueprint July_v.01.03_TXT.txt. Writing System auto-memory project_july_newsletter.md rewritten to match. Full detail: _handovers/LATEST.md.
**Last Updated:** 2026.07.12 (Sun, Claude Code, evening) - Cold-start continuity verified (all five notebooklm-* skills carry via yesterday's symlinks; @_rules.md import loads the NotebookLM/NBLM auto-lookup rule in-context) + notebooklm-add-content SKILL.md 0.7.3 syntax fixed + Fourthwall PDF lead magnet recommendation delivered. Item 1 (Windows-doctor GitHub issue) already done by Mick manually before session. Item 2 ran deeper than pickup note flagged: three separate 0.7.3 breakages in notebooklm-add-content - `--confirm` wrong (should be `-y`), `source remove` doesn't exist in 0.7.3 (`source delete`), AND `notebook rename/create/delete` command group was FLATTENED to top-level (`notebooklm rename` etc). Six edits total to the vault-library SKILL.md; grep of all four notebooklm-* skills now shows zero legacy syntax. Item 3 executed as Option C hybrid: created notebook "PDF Lead Magnet - DIY Investors_Updated:2026.07.12" (id a80a1222-0fba-423f-98f7-785c294d3372), added seed brief anchoring the ICP + business profile + brand frameworks, kicked off NotebookLM Deep sweep (132 sources: seed brief + auto-generated Deep research report titled "The Strategic Architecture of High-Converting Financial Lead Magnets" + 130 URL sources + final index text source; IMPORT_RESEARCH RPC timed out at 30s but CLI detected sources landed and treated as success - benign, worth adding to notebooklm-cli-custom Gotchas next session). Queried notebook for 5 candidate topic+format combinations; pressure-tested against ICP verbatim language ("Got my fingers burnt", "I missed that one", "make money not lose money", "beat the market") + brand constraints (Portico Investing, Three Pillars, DYOR, no certainty/guaranteed, transparency about wins AND losses). WINNING recommendation: "The DIY Investor's Stock Score Sheet - A Three Pillars Buy Test" - interactive PDF scoring worksheet, reader inputs a ticker + scores against Fundamental/Technical/News-Flow, gets Go/Wait/Avoid, back page channels to Silver Inner Circle ("Inner Circle is where I run this filter systematically across the entire UK market every year for you"). RUNNERS-UP: Portfolio Health Check (existing-portfolio segment) + Autopsy of a Trade (as Day-4 nurture email content). REJECTED: Portico Playbook (wrong altitude for cold Bronze) + Contrarian Hype Checklist (Awareness-tier low quality). Vault report: Dex-MickP\00-Inbox\2026.07.12 - Fourthwall - PDF Lead Magnet Topic Recommendation.md. Dual-save studio note in notebook (id 8a719769); placeholder deleted; final dual index (studio note id a30ec070 + text source id 46acf5c7) both titled "Index_Updated:2026.07.12 - 17.32". Key research quantitative benchmarks retained in the report: CVR by format Interactive Quiz 40.1% low-quality > Calculators 25-32% HIGH-quality > Webinars 27.4% > Benchmark Reports 24.6% > Checklists 23.2% > Static Ebooks 19% > Newsletters 6.25%; email-only opt-in (1 field 13.4% vs 8+ fields 2.4%); Day 0/2/4/7/10 nurture drives 20-30% download-to-call vs 2% for send-and-hope; interactive/endowment assets 2-3x uplift over static. Auto-memory project_fourthwall_pdf_lead_magnet.md written + MEMORY.md index updated. Cowork mirror /mnt/skills/user/notebooklm-add-content/SKILL.md now three fixes behind - sync next Cowork session. Notion connector authorized mid-session but not exercised (no Content Studio artefact from this thread). Vault + skill edits ride tonight's 9pm daily_git_commit.py sweep.
**Last Updated:** 2026.07.12 (Sun, Claude Code, afternoon) - NotebookLM CLI infrastructure + Fourthwall research. NEW GLOBAL custom skill C:\Users\pavey\.claude\skills\notebooklm-cli-custom (9 sections: ask --save-as-note shortcut, PowerShell escaping recipe for `notebooklm note create` with long content, dual-save pattern vault+notebook, ASCII cleanup, tag capitalisation, gotchas incl. today's auth quirk and the Windows doctor Profile-Dir false positive). Four vault-library notebooklm-* skills (setup, add-content, chat, studio-output) SYMLINKED into the global Claude Code root - Mick ran an elevated PowerShell mklink script; verified live in-session, no restart needed; source of truth stays at Dex-MickP\skills\. NEW rules file C:\Users\pavey\.claude\_rules.md linked from global CLAUDE.md via `@_rules.md` import (CLAUDE.md v1.3 -> v1.4, changelog row added). First rule seeded: NotebookLM/NBLM auto-lookup ("consult notebooklm-* skills before any tool call"). UPGRADED notebooklm-py 0.3.4 -> 0.7.3 via `python -m pip install --upgrade notebooklm-py` + `notebooklm skill install`; auto-migration preserved 29 auth cookies; today's 0.3.4 "ask endpoint says auth expired while status endpoint works and on-disk cookies are valid" false positive is FIXED by v0.4.0/v0.5.0 auth reliability fixes (re-tested clean). `notebooklm doctor` reports Profile-Dir 0o777-vs-0o700 as a warning on Windows - cosmetic false positive (Get-Acl confirmed folder locked to owner + SYSTEM + Administrators only, no world-writable ACE); GitHub issue drafted for the maintainer at teng-lin/notebooklm-py, browser tab opened for Mick to paste-submit. Fourthwall notebook interrogated twice: (1) tier replication - mirror Bronze/Silver/Gold unchanged; Mick's addendum clarifies annual-only members with Feb 2027 renewal window make the notebook's mid-cycle-churn concern a non-issue (switch-over IS the renewal); (2) 8-section PDF sales playbook - 2GB digital-product limit, 5% flat / 0% on Pro, VAT handled by Fourthwall, YouTube shelf rejects digital items (Trojan Horse physical proxy workaround), free-PDF lead magnet, educational-not-advice framing for DIY-investing. Both filed to Dex-MickP\00-Inbox with the Fourthwall tag; PDF playbook also posted BACK as a note in the Fourthwall NotebookLM studio panel via the escaping recipe. Level-2 end-to-end test of notebooklm-chat also ran clean (fees query -> NotebookLM-Queries). TWO MEET CEDRIC episodes drafted to Notion Micks Content Studio (both Meet Cedric / Video / Draft / YouTube-Public): "When the Job Moves House (Why Cedric Sometimes Has to Work Inside Claude Code)" and "Two Doors, Two Toolkits (Why Cowork and Claude Code Don't Share Every Skill)". Auto-memory: project_notebooklm_cli_custom_skill.md and project_fourthwall_migration.md written. Wider context: Anthropic Cowork cloud move (7 July 2026) is why the whole session ran in Claude Code - Cowork's cloud shell cannot reach a locally installed CLI.
**Last Updated:** 2026.07.11 (Sat, Cowork, evening 4) - Git commit DONE + fixed daily_git_commit.py. Today's whole session was committed and pushed: manual commit 5e10b38 (505 files, main 5e2f08f..5e10b38 on github.com/Mick-P-UK/Dex-MickP). Mick ran it in PowerShell on his machine because the Cowork sandbox has NO SSH key (push must come from his PC; sandbox can commit but not push). ROOT ISSUE found + FIXED: daily_git_commit.py built the commit message inline as git commit -m "<...>", so a large file list (503 files) exceeded the Windows ~8191-char command-line limit ("The command line is too long") - the first manual attempt failed there, and tonight's 9pm sweep would have failed the same way. Patched the script to write the message to a temp file and use git commit -F (no length limit) with try/finally cleanup; also capped the config/docs file lists to 10 like the code list. Backup: daily_git_commit.py.bak-2026-07-11. Verified: py_compile OK, ASCII-clean, and an 8932-char message commits fine via -F in a throwaway repo. The patch itself is uncommitted and rides tonight's 9pm sweep, which now runs the fixed script. Workaround used for the failed manual commit: files were already staged, so `git commit -m "<short msg>"` then `git push` succeeded (pre-commit ASCII hook passed).
**Last Updated:** 2026.07.11 (Sat, Cowork, evening 3) - Vault ASCII cleanup DONE + built the non-ascii-sweep skill. (1) Full non-ASCII sweep of the whole vault: typography corruption (smart quotes, em/en dashes, ellipsis, nbsp, bullets, arrows, box-drawing) fixed everywhere; then per Mick's choices currency->ASCII (GBP/EUR/c), status glyphs->tags ([x]/[ ]/[!]/^/v), decorative emoji + ShareScope private-use glyphs + broken U+FFFD dropped, accents transliterated to base, and 9 wrong-encoding cp1252 files (incl 4 Writing System letters/newsletters) re-saved as UTF-8. 413 files changed; verification = ZERO non-ASCII in any decodable text file. Root cause was the Mac-seeded DEX templates (now cleaned, so new notes start clean). Report: System/Debug_Logs/2026.07.11 - Vault ASCII Cleanup Report.md. Left alone: 6 undecodable junk/binary files (Word/ShareScope temp, 2 corrupt .md.v3-backup, a log), the credential pickle, and .obsidian config. (2) Built skills/non-ascii-sweep (modes scan/safe/full). Its script ascii_sweep.py is PURE ASCII by design - all special chars via chr() code points - so the sweep can never corrupt its own mapping tables; auto-detects the vault root; writes dated reports to System/Debug_Logs. (3) Scheduled task non-ascii-sweep-weekly: Saturday ~10am London, SAFE mode only (typography auto-fix + report meaningful for review; never full unattended). GOTCHA: the Write/Edit tools truncated the large .py at ~285 lines AND did not sync to the bash mount - wrote the final script via bash heredoc; PREFER heredoc for large script files in this vault. Caveat to flag: accents were transliterated vault-wide (e.g. any names in 08-People) - can restore specific names from git if wanted. Git: all of today rides the 9pm sweep unless Mick asks to commit now.
**Last Updated:** 2026.07.11 (Sat, Cowork, evening 2) - New project set up: 04-Projects/2026.07.11 - Hermes-Claude-Obsidian, paired with a NotebookLM notebook (id fa003870-78c0-45f4-9df1-c815958f88f7, title "Hermes + Claude + Obsidian_Updated:2026.07.11", created by Mick via the notebooklm CLI). Purpose: investigate the Hermes Agent (Nous Research open-source personal AI assistant framework - persistent memory, self-written skills, scheduler, multi-channel gateway) as a possible route to assist the MCSB build. Registered in the project index (04-Projects/README.md, new Active Projects section) and cross-linked from the in-vault MCSB project note (2026.05.11-MCSB-Webinar-Voice, new Section 10). Drafted a Meet Cedric episode in the project folder (even-handed investigate-not-convert angle). Grounding source is the 00-Inbox Hermes guide note ("Hermes - A Guide for DIY Investors", from a claude.ai web session, tied to the 29 Jul 2026 AI-4-Investing webinar). Mick then asked to add that guide as a source into the notebook via notebooklm.google.com. Project name uses hyphens (Hermes-Claude-Obsidian) to stay ASCII-clean. Vault edits ride the 9pm sweep.
**Last Updated:** 2026.07.11 (Sat, Cowork, evening) - Session-start CONTINUITY FIX + MCSB reconciliation prep. Root problem: this morning's work was invisible at session start because the wrap flushed CEDRIC_MEMORY.md but APPENDED at the file bottom while the top Last Updated stack (what start reads) still showed 07.10. Fixed both ends: baton-wrap step 3 + sundown-wrap step 7 now PREPEND a Last Updated line + Recent session block at the top (never append); session-start now reads _handovers/LATEST.md FIRST then the memory top, trusting LATEST if it is newer (Dex CLAUDE.md edited; master C:\Users\pavey\.claude\CLAUDE.md appended via PowerShell, backup .bak-2026-07-11). Orphaned entry tidied to top. Committed 5e2f08f. Also: brain-dump note + two backlog tasks (^task-20260711-001 ShareScope private repo; ^task-20260711-002 MCSB PRD v0.3 reconciliation); found the canonical MCSB PRD v0.3 lives OUTSIDE the vaults in the PAIDA Master folder (Documents\0.0 - AI Projects\0 - PAIDA - Mick 2nd Brain\PAIDA Master - Second Brain\04-Projects\2026.05.09 - MCSB\), confirmed v0.3 is the latest, made a PDF; lifted the 13 May Phase 1 implementation pickup note into 00-Inbox. PROGRESS.md exists there (updated 07.07) + three 07.10 Cowork-cloud notes. OQ2 (fold PAIDA Master into Dex) now ripe. Vault edits ride the 9pm sweep.
**Last Updated:** 2026.07.11 (Sat, Cowork, afternoon) - Personal Content Backup executed. Reversed the two-repo plan: Dex-MickP is now ONE PRIVATE everything-repo (never published; a scrubbed DEMO repo is derived only if a structure is shared). First full backup pushed to GitHub (7e02ee7, 291 files). Fixed the silently-failing nightly auto-push by switching origin to SSH (dedicated ed25519 key dex-mickp-autocommit on Mick-P-UK). .gitignore slimmed to secrets + machine junk; pre-commit ASCII hook rescoped to work-mcp inputs only so creative content keeps its typography. Still open: ShareScope-Automation needs its own private repo (backed up nowhere); point Cowork default folder at Dex-MickP. NOTE: this entry was originally appended at the FILE BOTTOM by the wrap and has been moved to the top; the two wrap skills are now fixed to prepend so it will not recur.
**Last Updated:** 2026.07.10 (Fri, Claude Code CLI, evening) - ASCII cleanup closed out. Fixed the
PATH UiPath analysis file that was held back from the 2026.07.10 GitHub commit by the pre-commit
ASCII hook: found ONE offending character (em dash U+2014, used twice in the "Overall Summary"
section - "repurchases-deploying" / "authorization-will"), swapped both for spaced ASCII hyphens,
verified zero non-ASCII bytes remain, committed both the cleaned research file and the SOP note
that documented the fix, pushed clean (10b5a83..2312d47 main -> main). CORRECTION: Mick confirmed
the June end-of-month portfolio posting run was NOT actually outstanding - he checked the WordPress
drafts on 2026.07.09 and published all four with that day's date. The "held for Desktop" item
carried in memory since 2026.07.09 is now CLOSED; drafts must have existed from an earlier
(unlogged) build step and only the manual review+publish was pending.
**Last Updated:** 2026.07.09 (Thu, Cowork) - SOP session. Reminded Mick how the end-of-month portfolios reach diy-investors.com: orchestrator portfolio-post-creator -> benchmark-fetcher + wordpress-image-uploader -> wordpress-post-publisher; posts created as DRAFTS only, Mick reviews the wp-admin edit URL and publishes. Confirmed the routine CANNOT run from Cowork: it needs Poster Pete's WP creds in C:\Users\pavey\.env, and Cowork cannot mount the home folder (reserved as internal session storage) nor read the file directly (WP API itself IS reachable from the sandbox, HTTP 200 - only the credential read is blocked). So the June run (month-end 30 Jun 2026, post date 9 Jul, all four portfolios) was HELD for Claude Desktop at Mick's choice. Started an SOP LIBRARY at 06-Resources\SOPs\ - first entry "SOP - End-of-Month Portfolio Posting.md" (YAML tag SOP, ASCII-clean, grounded in the four skills). Mick wants SOPs for all recurring workflows and flagged SOP-creation itself as a Meet Cedric topic.
**Last Updated:** 2026.07.05 (Sun, Cowork, afternoon 2) - Schema harmonisation + two new standing rules. (1) Harmonised gmail-self-notes note YAML with the vault _templates: author (was By), date_created (was created), url (lowercase, was Reference Link), added empty Category/status/topics placeholders, body now uses ## Summary / ## Key Takeaways / ## Notes. Updated build_vault_note.py in BOTH the vault AND the read-only mirror (reached the mirror by calling request_cowork_directory on its backing folder - see rule below). Fixed the 6 _templates (By->author, Reference Link->url, dropped the quoted "date_created:" key which had a colon baked into the property name). Updated Inbox.base ordering (created->date_created). MIGRATED all 70 existing 00-Inbox notes: frontmatter harmonised + key-order normalised to FM_ORDER; body headings applied only to youtube/attachment notes; plain text notes and ## Related blocks left intact. Fixed 3 non-ASCII files (00-Index Template.md em dash; Ideas/README.md + Meetings/README.md dashes/arrows/box-drawing tree). (2) NEW MANDATORY RULE in CLAUDE.md: ALWAYS request file/folder access (request_cowork_directory) BEFORE reporting a file/folder as unavailable / read-only / needs-a-restart. Root cause: I wrongly reported the skill mirror as un-syncable when a single folder request fixed it instantly. (3) NEW behaviour: whenever I find a non-ASCII file, flag it AND offer to fix it (do not just mention it). DONE (after reboot): the new mandatory rule is now also in the master global config C:\Users\pavey\.claude\CLAUDE.md (Mick appended it via PowerShell; backup CLAUDE.md.bak-20260705). Rule now lives in all three CLAUDE homes + this memory.
**Last Updated:** 2026.07.05 (Sun, Cowork, afternoon) - gmail-self-notes taken live-ish. Created two Obsidian Bases (root _All-Notes.base + 00-Inbox/Inbox.base). Resolved YouTube overlap (vault wins; yt-inbox-sweeper retired for YT); migrated 44 old Sheet rows to 00-Inbox/YouTube-Queue and archived the Sheet ([ARCHIVED 2026.07.05]). Ran a representative 48h test sweep (all pathways pass: youtube/text/attachment, xref + two-way links, MCSB authorship). Two skill fixes: YouTube title from email SUBJECT not web_fetch oEmbed (provenance-blocked), and youtube notes -> 00-Inbox/YouTube-Queue. Scheduled gmail-self-notes-sweep daily ~06:20 (self-contained prompt; processed-log seeded last_run 13:07). Added MCSB-Filed Gmail label (Label_534, light grey) + archive-out-of-inbox on success (never delete/mark read); search excludes -label:MCSB-Filed as 2nd dedupe. OPEN: backfill ~35 remaining 48h emails; re-sync installed .skill + mirror (M) with today's changes; click Run now to pre-approve tools; bookmark the base.
**Last Updated:** 2026.07.05 (Sun, Cowork) - Built + installed TWO Gmail self-note skills. cedric-note-fetcher (on-demand: fetch a self-sent attachment to outputs). gmail-self-notes (scheduled vault ingestion: body text + attachment + YouTube link each become Obsidian notes in 00-Inbox, with a shared xref datetime key and two-way related wikilinks; attachment author MCSB when built with Cedric else Mick; YouTube notes carry url + add-to-nblm + summary:pending). Attachment bridge: Gmail cannot download attachments, so browser Add-to-Drive then Google Drive connector (decode+validate). Created two Obsidian Bases (_All-Notes.base at vault root: Everything + Notes-only; 00-Inbox/Inbox.base: 5 views). OPEN: gmail-self-notes YouTube branch OVERLAPS existing yt-inbox-sweeper (Sheet-based, daily 06:30) - reconcile before scheduling. Skills backed up to vault (V) + installed (P); mirror (M) pending.
**Last Updated:** 2026.07.04 (Sat, Cowork) - Big ax-trees-automation session (Session 18). Built ax-mapper (generic AX-tree UI mapper: engine + per-app adapters) in the vault; converged the ShareScope mapper onto it (live proof passed, bespoke scripts archived+deleted); extended the map to v1.5 (news categories + Design; full portfolio download flow PP1/PP2). Split ShareScope into TWO adapters (stock + portfolio). New Key Convention saved: always give Mick commands in PowerShell, baby steps (he is not a coder).
**Last Updated:** 2026.07.02 (Thu late morning, Claude Desktop) - ShareScope chart shape + .env fixes. (1) CHART now exports true 16:9: sharescope_chart.py ticks the bitmap dialog's Custom option and sets 1200x675 - CONFIRMED exactly 1200x675 on HDD (right proportions for docx + 16:9 slides). (2) LOGIN failed after Mick rotated the ShareScope password because the script read the WRONG .env (a stale old Vault copy); repointed sharescope_login.py to C:\Users\pavey\.env (the single canonical creds file), added load_dotenv(override=True) + path logging - CONFIRMED working. (3) Credential SWEEP: repointed wordpress-post-publisher + wordpress-image-uploader to C:\Users\pavey\.env. (4) Added a top-level CREDENTIALS SINGLE-SOURCE rule to the master CLAUDE.md (v1.3) and reconciled all lower-level CLAUDE.md files to point at it; verified Poster Pete/WP creds are safely in the canonical .env before Mick deletes the redundant Vault copy. Detail in the 2026.07.02 session block below.
**Prior update:** 2026.07.01 (Wed early evening, Claude Desktop) - Built the ShareScope CHART + REPORT automation. NEW: sharescope-get-chart (v1.0, native 12-month PNG export), sharescope_session.py session runner (ONE login, many tickers/tasks, ONE logout - confirmed on HDD: chart + 6 CSVs in 26s), and sharescope-report (v0.1, chart embedded in the branded DIY template - proven on a Hardide brief). Selectors confirmed + logged. Produced a webinar crib sheet + a Meet Cedric episode (Content Studio, Draft). URGENT open item: strip the ShareScope password from PLAIN TEXT in sharescope-financials SKILL.md. NOTE: .env SHARESCOPE_HEADLESS is currently FALSE for tonight's live demo - flip back to true after. Full detail: 04-Projects\2026.07.01-ShareScope-Chart-Export\BUILD_LOG.md.
**Earlier update:** 2026.06.30 (Tue evening, Cowork) - Set up the PROMPT LIBRARY single-source-of-truth in Dex (new 06-Resources\Prompts\: README, _Prompt-Template schema, 00-Index, Prompts.base). Schema aligned 1:1 with PROMPT_LIBRARY.md via shared `code` key. Also FIXED Git: pushed a 7-commit backlog to GitHub and edited daily_git_commit.py so it self-heals (pushes whenever local is ahead, even on no-change days) and logs to _git-commit.log; enabled Task Scheduler history. STILL TO DO: migrate 141 prompt .md files from Mick's Vault (pilot batch agreed). Full detail: PICKUP_NOTE_2026.06.30-Prompt-Library-Migration.md (Dex root).
**Older update:** 2026.06.03 (Wed late morning) - Skill dual-write AUDIT across all three locations (Mirror /mnt/skills/user, PRIMARY C:\Vaults\Mick's Vault\.claude\skills, DEX skills). Heavy drift found: of 12 skills in 2+ places only 2 byte-identical. Fixed 3 in the mirror (image-cta-overlay v2.2; annie - fixed DEAD tool names; pdf-to-pptx-converter v1.1). Rest PAUSED for after tonight's webinar. FULL DETAIL + remaining work in PICKUP_NOTE_2026.06.03-Skill-Audit.md (Dex root). Key realisation: canonical model is ALREADY documented (Dex + mirror) but migration onto it is only partial, AND the four 2026.05.30-migrated skills are now MISSING from this project's mirror (mirror may be project-scoped or resetting).
**Environment:** Cowork-cloud (this session; device bridge to C:\Vaults + live ShareScope via Playwright MCP on mick-pc25). (Prior sessions: Claude Code CLI, Cowork, Claude Desktop.)

---

## Recent session: 2026.08.01 (Saturday, Claude Code, morning) - Portico-WE-portfolios automation (PP1/PP2 snapshot + Slack post)

- GOAL: automate Mick's Saturday routine of posting PP1 and PP2 portfolio snapshots to their Slack channels. Built as two standalone skills + one chaining SOP (kept separate so a snapshot can be taken any day and a post run without re-capture).
- portico-snapshot skill: wraps the existing hardened sharescope_portico.py (capture + CSV export + current-holdings filter) and annotate_portico.py (house-style formatter). Output: finished PNGs in portico/outputs + a portico_history.json week-on-week update. Slack-agnostic. Known caveat carried forward: capture can grab the full holdings list on a slow page load (PP1 most at risk) - re-run/verify.
- PPfolios-to-Slack skill + new script portico/slack_post_portico.py: posts a finished image AS Mick using a Slack USER token. Slack flow: files.getUploadURLExternal -> byte upload -> files.completeUploadExternal with initial_comment=caption. Converts PNG->JPG named 'YYYY.MM.DD - PPn_{total}GBP_Up by {gain}GBP_Up by {pc}pc.jpg'. Channels PP1=C01H7ST4BDK (public), PP2=C04GZAAPT9U (private).
- SLACK APP SETUP (Mick did, Cedric guided): 'PPfolios Poster' app in Portico Plaza, created From a manifest, USER token scopes chat:write + files:write ONLY (deliberately no im:write / channel-create - least privilege). 'Create and Install' threw 'Something went wrong' repeatedly; FIX = the app had already been created, so install it from the OAuth & Permissions page instead of re-clicking. Token saved as SLACK_USER_TOKEN in C:\Users\pavey\.env (single source).
- SAFETY: real member channels require --yes; --channel <id> overrides the target (used for testing); the seatbelt only guards the two live channels. The read/search Slack MCP connector was used to find channel IDs and verify posts. auth.test confirmed posting identity = mickp @ Portico Plaza. End-to-end TEST post landed correctly in the private #cedric-private (C0BMFLPKTHS): posted as Mick, image attached, <#C01HC8AD7V0|micks-diary> rendered as a link.
- Phraseology library: portico/PPfolios-Slack-Phraseology-Reference.md captures Mick's caption voice. CAPTION TIMING RULE (Mick, this session): images posted first, video after -> the pointer is forward-looking by default ('The video, with my commentary, will shortly be available on #micks-diary').
- Draft-and-confirm is a HARD rule: Cedric drafts captions, Mick approves, then post. Never auto-post to member channels.
- Deployed: both skills dual-written (vault skills/ + C:\Users\pavey\.claude\skills, SHA256-verified), skills/README.md updated, SOP - Portico-WE-portfolios.md (v1.0) written to 06-Resources/SOPs, indexed as Active SOP 7 in C:\Vaults\_SOPs\INDEX.md.
- Meet Cedric brain dump logged to Notion Content Studio (3afdb32a9b0a8122b59bcbe0e93aa99e): 'Teaching Cedric to Post My Weekend Portfolios to Slack (as Me)'.
- LIVE RUN DONE (11:42 BST): both posted AS Mick. Three fixes the run surfaced are permanent - ViewTransactions-first (ensure_transactions_view), annotate font() finds Arial on Windows, pytesseract points at the Windows Tesseract. Timed sign-offs; portico_history.json updated (2026-08-01). git committed + pushed this session.
- OPEN / NEXT: (1) build the #micks-diary VIDEO-CREATION skill - Mick is making this week's video MANUALLY as the reference example; (2) capture slow-load robustness (PP1 full-list risk); (3) fully unattended weekend schedule not decided.

## Recent session: 2026.07.30 (Thursday, Claude Code, evening) - EDV report correction + notebook hygiene

- Mick spotted Ron's ShareScope consensus looked wrong (he suspected a missing AUD/USD conversion). ROOT CAUSE was STALE data: Ron's "ShareScope Est." column had the 30 April forecast (revenue $8,020.6m) because the April ShareScope CSVs were still in the EDV notebook when he queried it. The CSVs are USD (verified: CSV H1 2025 turnover 2,050.0 = company-reported $2,050m); only per-share extras (FCF-per-share, Graham number) are GBp. No conversion was missing.
- Corrected the report .md to current 30 July figures (revenue 7,533.6, PBT 3,572.9, EPS 5.68, div 1.925, FCF 2,880.2, net cash 1,361.3), recomputed variances, added a correction note; regenerated DOCX + PDF (Mick had the DOCX open in Word - lock; he closed it and I overwrote). With correct data, ShareScope EPS/dividend reconcile with Ron; only revenue/FCF stay high (imply ~+78% growth).
- Cleaned the EDV notebook 97->43 sources (removed 24 stale April ShareScope CSVs + 31 duplicate copies); archived the 6 April CSVs to the EDV base-data folder first (2026.04.30 - EDV_ShareScope_*.csv).
- NBLM auth died twice mid-session; both healed hands-free via the headed browser on stored Google creds (new rule confirmed working).
- Baked in two standing rules (memory notebook-hygiene-per-company; SOP STEP 3.5 in canonical + vault mirror): clear the prior run's ShareScope CSVs before Ron queries, and archive-not-delete anything removed from a company notebook.
- Logged Mick's requested next step: a Ron OUTPUT-CHECKER (auto-verify stale-source / currency / arithmetic before a report is accepted) - memory project_ron_output_checker, _SOPs/INDEX.md planned section. See [[EDV H1 2026 Results Research]].


## Recent session: 2026.07.30 (Thursday, Claude Code, morning) - EDV H1 2026 Results Research

- Mick asked to download all EDV Q2/H1 2026 results-day assets and file them. Pulled 5 PDFs (News Release, Presentation, MD&A, Financial Statements, Mine Statistics) from the endeavourmining.com results page (verified the real S3 links via the in-app browser DOM, not the WebFetch summariser) into the EDV Documents folder. The 6th listed item (Webcast) is a media-server stream, not a file; no call transcript posted yet.
- Ran the full ShareScope + NotebookLM + Ron pipeline (SOP #1). Existing EDV notebook found (id 57014b58-830f-43bd-9c80-273bb64c1f71) so ADDED rather than created. Loaded today's 5 result PDFs + 6 ShareScope CSVs + 12-month chart (12 new sources, all verified ready). Renamed with _Updated:2026.07.30. Notebook now holds 96 sources (April run left duplicate news/RNS - offered a cleanup, not yet done).
- GOTCHA confirmed: NotebookLM rejects raw .csv file uploads (status error). Fix: upload ShareScope data as TEXT (copy csv to .txt, add --type file) - processes cleanly. The CLI --title now works for file uploads in this version (was previously ignored).
- NBLM AUTH: session was genuinely dead (headless re-export redirected to accounts.google.com). NEW hands-free fix: launched a HEADED persistent-context browser on the profile - Google auto-signed-in from stored creds, Mick typed nothing. Captured storage_state, auth healed. Rule updated in _rules.md and memory notebooklm-login-detection-rebrand-fix.md: try the headed browser BEFORE escalating.
- Ron's verdict: BUY into weakness / HOLD until it reclaims GBP 40. Key catch: ShareScope FY2026 consensus (revenue $8.0bn, EPS 712c) is unreliable - cannot reconcile with H1 actuals + guidance; Ron anchored on H1 actuals instead. Cedric's caveat: Ron's ~$1.92/sh FY dividend looks high vs the company's $300m FY-2026 minimum (~$1.24/sh base). H1 figures spot-checked against the News Release PDF and tie out.
- Deliverables in the EDV folder: 2026.07.30 - EDV_H1 2026 Results_Ron Analysis_Formatted.docx and _Formatted_PDF.pdf (docx-js build, PDF via Word COM; chart embedded, provenance footer, ASCII clean).
- OPEN: (1) log a Notion research entry for EDV; (2) prune duplicate sources in the EDV notebook; (3) optional DOCX/PDF layout tweaks. See [[EDV H1 2026 Results Research]].


## Recent session: 2026.07.29 (Wednesday, Cowork-cloud, mid-afternoon) - Prompt library: NBLM-07 added, ::nb7# reserved by Mick

- Mick supplied one new NotebookLM prompt for the library and said the AHK shortcode
  would be ::nb8# when he gets round to adding it to AutoHotkey. He was busy with
  29 July webinar preparation throughout, so this was a quick drop-and-file.
- Filed as NBLM-07 "Detailed Report for Novice Reader (Nina Sign-Off)" across the
  three-place workflow (source note, PROMPT_LIBRARY.md, 00-Index.md). Fully ASCII,
  verified zero non-ASCII bytes in both written files.
- Cedric initially recorded ::nb7# as an unused gap and queried it. Mick corrected:
  ::nb7# IS assigned to a prompt he has not yet passed over. Both files were then
  amended to flag ::nb7# as reserved-and-pending rather than free.
- STANDING INSTRUCTION: when Mick supplies the ::nb7# prompt, file it as NBLM-08
  with ahk ::nb7#. Do not reassign ::nb7#, do not renumber NBLM-07. Code numbers and
  shortcode numbers stop running in step from here by design.
- Noted but NOT actioned: NBLM-06 signs off "London [BST]", which is incorrect from
  late October to late March. NBLM-07 uses plain "London". Mick has not yet said
  whether to amend NBLM-06.
- Also still open from the 1208 thread: the bulk prompt-library migration
  (^task-20260729-001), 141 files, untouched.

---

## Recent session: 2026.07.29 (Wednesday, Claude Code, mid-afternoon) - GGP Q4/FY26 quarterly analysis (Nina + Ron) + provisional SOP

Mick asked Cedric to orchestrate (Nina in NotebookLM + Ron) an updated Greatland Resources (GGP) analysis after the 29 July 2026 June-quarter Quarterly Activities Report (Greatland FY ends 30 June). Flow: verified NotebookLM auth healthy (no re-export needed); confirmed the notebook "Greatland Resources_Updated:2026.07.29" (7473143f); extracted the RNS text with pymupdf (poppler/pdftoppm is NOT installed so the Read tool cannot render PDF pages); added the RNS as source ef481528; sourced REAL Apr-Jun 2026 gold/copper/AUD-USD data via web (no assumptions - Nina's earlier prices were visual chart reads); spawned Ron (subagent_type ron) with a full real-data pack. Ron wrote the report + a 30-calc appendix, then Cedric built a formatted DOCX (python-docx, house style + provenance footer) and a PDF (Word COM via PowerShell - no LibreOffice installed; `notebooklm source add --wait` flag does not exist in this CLI build, poll `source list` instead).

Key outcome: turnover is now REPORTED not estimated (FY26 net revenue A$2,271m); profitability built from real cost lines (EBITDA ~A$1.4bn) with statutory NPAT flagged as a GAP pending the audited accounts (~Sept 2026). Old-vs-new: Nina's 6 July production estimates were within 0.5% and her chart-read commodity prices within ~1.4% of the now-real data.

Files: [CREATE] NotebookLM-Queries/2026.07.29 - GGP Greatland Resources - Q4 n FY26 Updated Analysis.md (Ron report + appendix); [CREATE] GGP research folder DOCX + PDF (_Formatted / _Formatted_PDF); [CREATE] auto-memory commodity-prices-q2-cy2026.md + MEMORY.md index line; [CREATE] 06-Resources/SOPs/SOP - Quarterly Production Update.md (v0.9 PROVISIONAL); [UPDATE] C:\Vaults\_SOPs\INDEX.md (new entry 6, flagged provisional).

Decisions: build the quarterly-update routine as a SOP FIRST (skill later, against a live quarterly) and as a NEW standalone skill (not an extension of sharescope-nlm-research). SOP marked PROVISIONAL awaiting Mick's review - six open questions at its section 10. Old GGP notebooks (68ceea40, a942a497) left as-is at Mick's request. Mick was busy with 29 July webinar prep throughout.

## Recent session: 2026.07.29 (Wednesday, Claude Code, afternoon) - GGP notebook analysis marker + two NotebookLM rules hardened

- Mick asked, pre-webinar, whether Cedric could still reach the notebooks in NotebookLM (rebranded by Google to Gemini Notebook) and whether a Greatland Resources (GGP) notebook existed. Auth had lapsed - `notebooklm auth check --test` failed at Token fetch.
- Self-healed WITHOUT bothering Mick: killed the hung `notebooklm login` (it timed out to background after 120s - the known post-rebrand detection hang), then ran the Playwright cookie re-export from C:\Users\pavey\.notebooklm\profiles\default\browser_profile into storage_state.json. Landed on notebook.google.com (session live), Token fetch then passed.
- Found FOUR Greatland notebooks. The current/latest is "GGP - Greatland Gold_Updated_2026.07.06" (id 7473143f). Note the company itself rebranded Greatland Gold -> Greatland Resources, hence duplicate-ish names.
- Queried that notebook and wrote a concise point-in-time ANALYSIS SNAPSHOT MARKER as at 2026-07-06 (thesis: Newmont Telfer+Havieron buy, hub-and-spoke; assets Telfer/Havieron/O'Callaghans/regional; A$1,289m cash debt-free; ASX listing done, WA EPA approval outstanding; ~GBP 4.87bn cap, Citi/Macquarie Neutral). Purpose: a fixed baseline to diff future analysis against.
- Added the marker as a text SOURCE inside the notebook (source id fda4b9c9) at Mick's request, AND saved a vault copy: NotebookLM-Queries\2026.07.06 - GGP Greatland Resources - Analysis Snapshot Marker.md (ASCII-clean; GBP not the pound glyph).
- RENAMED the notebook to "Greatland Resources" - but first dropped the convention suffix; Mick corrected, so final title is "Greatland Resources_Updated:2026.07.29".
- Added TWO mandatory rules to _rules.md: (1) NotebookLM auth = re-export cookies FIRST post-rebrand, never `notebooklm login` first (it hangs 2-3 min); (2) NotebookLM notebook naming = every rename carries `_Updated:YYYY.MM.DD`. Updated auto-memory notebooklm-login-detection-rebrand-fix.md + MEMORY.md to match.
- Flagged a demo risk: three similarly-named Greatland notebooks now exist (offered to archive-rename the older two "GGP - Greatland Resources" 68ceea40 and "Greatland Resources_Updated: 2026.01.14" a942a497 - Mick has not yet decided).
- PARKED for later (Mick's call): align sharescope_nlm_researcher.py preflight_auth_check() and Ron's agent-def "Auth fallback" to the re-export-first approach.

## Recent session: 2026.07.29 (Wednesday, Claude Code, midday) - Prompt Library activated + first two prompts migrated

- Mick asked to add prompts into his prompt library. Found the library has two layers: development source notes in Dex-MickP\06-Resources\Prompts\ (one markdown note per prompt, YAML frontmatter per _Prompt-Template.md) and the lean operational file C:\Vaults\Cowork\PROMPT_LIBRARY.md (INDEX table + PROMPTS section) that AutoHotkey hotstrings and the investing demos read. A generated catalogue 00-Index.md sits alongside the source notes.
- Added SUM-02 first (Video Section Summary - Timestamped Bullets): a short bullet summary (<130 words) of an edited video with timestamped section markers, no more than 7 sections. Initially filed as WEB-01, then Mick asked to recategorise to SUM, so it became SUM-02 (he reserved SUM-01 for a prompt he was about to give).
- Added SUM-01 (Notion Announcement Summary - Summary item field): generates a <=200-word structured summary of an announcement (usually an RNS) and posts it into the Notion "Summary (item)" field with bold headings and bulleted items. The pasted prompt arrived as UTF-8 mojibake; de-mangled it back to the intended characters (em dash, round bullet, arrows) first.
- STANDING DECISION on special characters: Mick chose "fully ASCII" storage. The prompt names the required bullet as "Unicode U+2022" and shows the example marker as "[U+2022]" rather than embedding the glyph; arrows written "->", em dash " - ". Keeps the vault ASCII-clean per the global zero-tolerance rule while preserving the prompt's exact formatting instruction.
- SUM-01 overlaps the existing /pns skill (Post Notion Summary) and the notion-summary skill. Mick's call: leave SUM-01 as a standalone library prompt for now (cross-referenced to /pns in the note); he will review whether to fold it into /pns later. Did NOT modify /pns.
- Updated all three files for each prompt (source note, PROMPT_LIBRARY.md, 00-Index.md). The Prompts folder had been at 0 notes since 30 June 2026 (migration pending); it is now live with 2 notes.
- Wrote a new Claude Code auto-memory prompt-library-workflow.md (the 3-place sync, CAT-NN codes, category vocabulary, ASCII-glyph convention, backlog) + MEMORY.md index pointer.
- Logged a Medium-priority task ^task-20260729-001 in 03-Tasks/Tasks.md (P1): bulk-migrate the many remaining prompts in a dedicated block, with the full workflow captured in the task body so it can be picked up cold.

## Recent session: 2026.07.28 (Tuesday, Cowork-cloud, morning-midday) - AI4Inv Core Model infographic and pptx-editable-graphics skill

- Mick asked for an infographic for the 29 July AI for Investing webinar: a three-piece interlocking jigsaw circle (Data biggest, then Storage, then Wiki), a wide ring around it holding text, and an outer ring split into AI / User / a third segment left as a placeholder. 16:9 for a PowerPoint slide.
- FIRST DELIVERY WAS WRONG. Built it as an SVG rendered to a transparent PNG and dropped on a slide. Mick came back: he wants the PowerPoint output FULLY EDITABLE so he can move parts, change colours and change annotations. Rebuilt entirely as native shapes.
- NEW STANDING RULE, saved to memory at Mick's request: for infographics, PowerPoint output is ALWAYS fully editable native shapes (freeforms, autoshapes, real text boxes), never a flat PNG, unless he explicitly asks for an image.
- Final structure: 3 freeform jigsaw pieces, 1 Donut autoshape for the binding ring, 3 Block Arc autoshapes for the outer ring, 9 text boxes, all individually named for the Selection Pane.
- Mick then asked two good questions: should infographic building be a skill, and should Claude Design be used for branding. ANSWERS: yes to a narrowly scoped TECHNIQUE skill (not a picture catalogue); NO to Claude Design for this - it is a product/UI design-system tool, and using it would create a second source of truth for brand colours that would drift from the .potx/.pptx packs. The deck stays the single source of truth.
- Caught a real problem: the graphic was on a white background with near-black title while the .ai Webinar pack is a dark frame. Extracted the actual palette from the live deck (2026.07.27 - AI-4-Inv_Webinar_for_29th July 2026__v1.03.pptx) and re-skinned it.
- KEY TECHNICAL FINDING: the deck's ppt/theme/theme1.xml carries the STOCK Office 2007 scheme (4F81BD / C0504D / 9BBB59). The REAL branding is in literal srgbClr values on the slides: navy 0B1E3B / 13294F, brand gold DBA43A, panel EDF1F2 with C4CED3 border, green 2E7D32, blue 2E4ED1, salmon E39B92, slate 9AA6AD family, Calibri. ALWAYS census the slides, never trust the theme part.
- SECOND FINDING: despite being the "dark tech" pack, .ai Webinar content sits on a LIGHT panel inside the dark frame. Mick's light-theme preference holds inside it. Do not build dark-background graphics for this pack.
- NEW SKILL: skills/pptx-editable-graphics. SKILL.md, scripts/ppt_shapes.py (helper library), scripts/extract_theme.py, scripts/qa_render.py, references/themes.md, examples/build_jigsaw_ring.py. Registered in SKILLS_REGISTRY.md and skills/README.md. Tested end to end from a clean directory - the example reproduces the delivered slide exactly.
- GOTCHAS BAKED INTO THE SKILL (each one cost time today): python-pptx's <p:style> effectRef idx="2" re-injects drop shadows even after shadow.inherit=False, so zero lnRef/fillRef/effectRef; Block Arc adj1/adj2 are 60000ths of a degree measured CLOCKWISE from three o'clock; donut adj3 is a fraction of shape WIDTH not radius; python-pptx normalises adjustments by 100000 which is wrong for angles so write the <a:gd> elements directly; curved text is not editable so rotate normal text boxes to the tangent instead.
- NOTED FOR MICK: slide 4 of deck v1.03 still contains the OLD light-theme shapes he pasted in earlier - they need deleting and replacing with the themed version.
- Deliverables all committed to C:\Users\pavey\Documents\0.0 - AI Projects\2026.07.29 - AI-4-Inv Webnr\.
- CAVEAT: only the vault master copy of the new skill was written. The /mnt/skills/user/ mirror lives in the ephemeral cloud sandbox, so the usual dual-deploy byte-identical verification has NOT happened - needs a mirror sync from a Desktop session.

---

## Recent session: 2026.07.27 (Monday, Claude Code, afternoon-evening) - NotebookLM auth fix + June webinar processing + SOP

- Started as a connectivity check. NotebookLM CLI auth failed at "Token fetch" while cookies looked fine. ROOT CAUSE: Google's "Gemini Notebook" rebrand (notebook.google.com) breaks the CLI's `notebooklm login` sign-in detection - it hangs to the 5-minute timeout even though Mick is fully signed in and can see his notebooks. FIX (no re-login needed): re-export live cookies from the CLI persistent browser profile (C:\Users\pavey\.notebooklm\profiles\default\browser_profile) into storage_state.json with a small Playwright script. Token fetch then passed (29 cookies). Saved cross-surface here + Claude Code auto-memory `notebooklm-login-detection-rebrand-fix`. This supersedes the old "notebooklm login self-heals" assumption post-rebrand.
- Ran the full ai4inv-webinar-processor pipeline on the JUNE 2026 edition (held 1 July 2026): notebook DIY.ai - Monthly Webinars d3d6216b; audio source df09ec5a; source-scoped user guide via `ask -s`; branded Word guide built via node/docx from a Windows-path work dir; index source 854bbadd + Source Index note 4bc66b71 + index.md note + new per-edition summary note; notebook renamed _Updated:2026.07.27.
- Phase B: whiteboard past-tense explainer Video Overview "June 2026 Webinar Recap" (artifact 57c313ce) via `generate video --format explainer --style whiteboard --prompt-file`; reused Mick's saved webinar-summary video prompt (May->June). Downloaded the 35MB mp4 to the webinar Recordings folder as "...Recap_Unedited.mp4" through the authenticated browser profile.
- Built "SOP - AI4Inv Monthly Webinar Processing.md" (v1.0, 06-Resources/SOPs) and registered it as entry 5 in C:\Vaults\_SOPs\INDEX.md. Updated the skill SKILL.md with the corrected CLI syntax and the new Phase B video step. Deliverables (docx + mp4) live in the webinar Recordings folder, not the vault.
- CAVEATS: /mnt skill mirror sync pending (Claude Code cannot reach /mnt); C:\Vaults\_SOPs\INDEX.md still has no git backup (open backup-strategy decision); the member Word guide uses the DIY branded footer, not the internal provenance footer (deliberate - no local paths in a members' document).


## Recent session: 2026.07.26 (Sunday, Cowork-cloud, late afternoon) - Portico Member Report

- NEW PROJECT: Dex-MickP/04-Projects/2026.07.26 - Portico Portfolios - Performance Update (July 2026)/ - member-attraction report rewriting the Gemini Notebook Portico analysis in Mick's voice.
- Gemini Notebook (renamed NotebookLM, notebook.google.com) notebook 'Portico-Portfolios_Performance_Updated:2026.07.26' fully read from cloud Cowork via Chrome: 18 sources, 8 Studio reports extracted with JS innerText chunking (span click -> source viewer -> slice between 'Source guide' and Chat markers).
- Title confirmed by Mick: How GBP 50,000 Became GBP 138,000 - The Portico Story / Beating the Market by Three to One.
- Ch1 approved v0.2 after two Mick corrections (stop-loss honesty; accurate Plaza description). Ch2-4 drafted v0.1. Checklist file tracks status.
- All arithmetic verified in Python (figures reconcile; FTSE CAGR 5.35 notebook vs 5.33 recomputed - flagged).
- Obsidian YAML frontmatter required on all project MD files (Mick instruction).
- Outputs destination: the project folder itself (Mick instruction).


## Recent session: 2026.07.26 (Sunday, Cowork-cloud, morning-midday) - Ditty Box year-end accountant pack, info-for-accountant skill, spreadsheet footer rule, and the first accounts SOP

Mick opened with an annual chore: copy the supporting evidence out of the Ditty Box
year folders into the "For Jade" folder for the accountants. He gave last year's path
as the template and asked for a plan and checklist FIRST (he said so mid-turn, and it
is now a standing preference).

What the reconnaissance found, and what next year depends on:

- The AUTHORITATIVE record of what the accountants want is the J-numbered FILENAMES in
  the prior year's "For sending 2 Jade" folder. The checklist xlsx sitting in that
  folder was only ever filled in as far as line 1 and is misleading.
- Filenames carry the date the file was PRODUCED, not the period covered. The
  YE 30.11.2025 opening-balance statement is named 2026.05.27 and covers 30.11.2024.
  Match on period, never on prefix. This is the single easiest thing to get wrong.
- Year folder prefixes are inconsistent (01_YE 30.11.2024 vs 001_YE 30.11.2025).

Delivered: 21 of 26 items copied into Z - For Jade_YE_30.11.2025\For sending 2 Jade,
named J<nn> - <original filename>, every copy MD5-matched to its source, all 408
originals verified still in place (copies only - Mick was explicit). Checklist xlsx
built, green/amber, saved to the Jade folder and sent to him; he printed it.

Five gaps remain and all five need Mick: the ii portfolio at 30.11.2024 (J11), both
Halifax CC-1136 balance screenshots (J19, J20), and the three Xero prints - Trial
Balance, P&L with codes, Balance Sheet (J21, J22, J23). He is working through them and
will come back for the zip.

He then asked for three follow-ons, each of which turned up something worth keeping:

1. STANDARD SPREADSHEET FOOTER. `(&Z&F - Printed: &D at &T)` on the left, every
   worksheet, all three footer variants, brackets literal. Now in CLAUDE.md's
   USER_EXTENSIONS block and in cross-surface preferences. Verified it survives the
   LibreOffice recalc round trip, which can strip header/footer settings.
2. PACKAGE IT AS A SKILL. Built info-for-accountant. The argument made to Mick, and
   the design principle: the copying is ten lines of shell; the VALUE is the manifest
   and the gap report. So the skill derives its manifest from the prior year's pack
   rather than hardcoding filenames, proposes a mapping for approval before touching
   anything, and refuses to guess between candidates.
3. REGISTRY AND SOP. Found skills/README.md missing five accounts skills and
   SKILLS_REGISTRY.md missing all six and stale since 19 July - both fixed. Found NO
   SOP for preparing the accounts existed at all; the entire process lived inside
   SKILL.md files, executable but unreadable. Wrote one, deliberately as v0.9 DRAFT
   with seven [CONFIRM] flags, because steps 1/2/6 are evidenced but the
   reconciliation step is inference and should not be presented as fact.

Open at handover: register the SOP in C:\Vaults\_SOPs\INDEX.md (blocked - outside the
Filesystem allowlist, and the folder-access dialog could not be shown because the
desktop window was unavailable); mirror the footer rule into
C:\Users\pavey\.claude\_rules.md; git commit and push (no vault shell from Cowork
cloud); answer the SOP's seven open questions; decide whether paypal-to-xero should be
promoted to a Cowork skill.

## Recent session: 2026.07.25 (Saturday, Cowork-cloud, afternoon-evening) - Portico ShareScope capture hardened by driving ShareScope live + baton-system recovery + PP1/PP2 weekend images delivered

Ran in Cowork-cloud via the Filesystem bridge to C:\Vaults, with live ShareScope automation through the Playwright MCP on mick-pc25 (logged in with the .env creds). Two arcs. ARC 1 (baton recovery): found LATEST.md stale (held the 07.23 baton) because today's earlier Portico work had been parked only in a project PICKUP_POINT; backed up LATEST.md byte-for-byte to _handovers/_backups/, wrote a post-mortem + bulletproofing spec (_handovers/2026.07.25 - Baton-Wrap Post-Mortem and Bulletproofing Spec.md), reconciled LATEST.md. ARC 2 (Portico capture, the bulk): PP1 kept capturing the full 'List of holdings' view instead of current holdings across FIVE reruns. The cause was only found by DRIVING ShareScope live: ViewCurrentOnly is a TOGGLE not a set, each portfolio remembers its own state, the button 'active' class is on both tabs, and the view must be read after the list finishes loading. Rewrote select_portfolio (verified+retrying; excludes the CurPort 'Port:' indicator; confirms via the panel header 'Transactions for Portfolio: ... PPx (UK)') and ensure_current_holdings (toggle-aware, network-idle settle, caption-painted verify, stable re-check) + a capture_panel pre-screenshot guard; added a 'View-state verification' section to ShareScope-data-cmd-Reference.md. Validated selection and the toggle branch live. CAVEAT: a slow-load run (18:39) still captured PP1 full (caption not painted in time); PP2 reliable. Recommended next fix: a load-independent signal (detect Shares=0 closed rows, present only in the full view; grid rows are DOM div.list-row in div.list-content-fixed) or auto-retry on the error flag. Delivered both finished weekend images to portico/outputs/ (PP2 from the 18:40 clean run; PP1 from a verified earlier live current-holdings capture cropped+formatted, data identical Saturday-close; both verified by eye). Learnings: drive the real UI early; verify the settled rendered result; know control semantics; pixels are ground truth; fail loud. Housekeeping: clearing the automation browser's localStorage mid-probe reset only THAT browser's ShareScope layout (Mick's normal ShareScope + the script's fresh context both intact). Full detail: _handovers/LATEST.md.

## Recent session: 2026.07.21 (Tuesday, Claude Code, day-close) - ShareScope Pipeline v2 SHIPPED (SOP codified, Ron permanent agent, ENQ end-to-end validated, five follow-up items done, immediate commit)

Two threads today, both closed. Full day of ShareScope + NBLM + Ron pipeline work.

**Thread 1 (baton 14:35) - SOP v2.0 codification + Ron permanent + ENQ end-to-end:**

- SOP v2.0 IS THE NEW SOURCE OF TRUTH for the ShareScope + NBLM + Ron pipeline.
  File: `C:\Vaults\Cowork\ShareScope-Project-Setup\3-SKILL-sharescope-nlm-research.md`.
  Approximately 330 lines. Includes new three-actor architecture section
  (Cedric orchestrates, Nina fetches, Ron analyses), Cedric-runs-both-scripts
  directly (interactive), mandatory 12-month chart PNG as Step 2b, Ron sub-agent
  spawn via `subagent_type: "ron"` as Step 4, tag format
  `[TICKER, Financial-Analysis, ShareScope-Research, Ron]`, Obsidian URI format
  `vault=Dex-MickP&file=<url-encoded-relative-path>` on Windows. Appendix A is
  the mandatory report template Cedric passes Ron; Appendix B is the v1.0/v2.0
  changelog. Nina's legacy v1-report path is documented as retained-but-ignored
  (safety-net fallback).

- `_make_obsidian_uri()` in sharescope_nlm_researcher.py FIXED to emit the
  reliable Windows format. Falls back to `path=<absolute>` if the report sits
  outside the vault root. Proven live end of the ENQ run.

- The "Ron sub-agent NBLM CLI auth quirk" from the 20 July session was a
  MISDIAGNOSIS. The real cause is genuine Google session invalidation which the
  `notebooklm_auth_status.json` cache CANNOT see. The cache measures cookie
  EXPIRY, not cookie VALIDITY; the auth monitor's live check runs only every
  6 hours; so the cache can lie for up to 6 hours after Google invalidates a
  session. Fix when it happens: `notebooklm login` in a browser (needs Mick).

- Ron is a PERMANENT NAMED AGENT. Definition file:
  `.claude/agents/ron.md` written in BOTH vaults (Dex-MickP + Mick's-Writing-
  System). YAML frontmatter (name/description/model) + markdown body. Contains
  Ron's full identity, notebook + chart access instructions, mandatory report
  template, market conventions (UK vs US), hard rules (UK English, ASCII only,
  sign off as Ron), auth fallback, output contract. Available as
  `subagent_type: "ron"` from any Claude Code session in either vault. Harness
  picked him up live in-session without a Claude Code restart. Cedric now
  passes only 7 lines of per-run detail on each spawn (vs ~60-line inline
  prompt via general-purpose the day before). Ron used 10 tool uses on ENQ
  today vs 26 on JSE yesterday. That is the whole point of a named agent.

- ENQ end-to-end validation ran clean. Fresh 6 CSVs, corrected 12-month chart
  PNG, notebook prepped (6 CSVs uploaded + 10 news items + title auto-renamed
  to "ENQ - Enquest_Updated_2026.07.21"), Ron spawned, Ron authored the v2
  report with full multi-indicator TA (support 25/22/20/18p; resistance 27/28p;
  MA stack; OBV/RSI/MACD/AccDist/ADX). BUY (special situation) driven by
  Malaysia PSC transformation and Magnus balance-sheet fix. Cleaned Ron's
  output (`&amp;` -> `&`, GBP substitution, no ASCII violations), added v2
  frontmatter (analyst: Ron, chart_source recorded, tags including ENQ + Ron),
  saved as
  `06-Resources/Research-Log/Research/ENQ/2026.07.21 - ENQ - Enquest - AI - Financial Analysis_v2.md`.

**Thread 2 (baton 18:39) - five follow-up items + immediate git commit:**

Direct pickup from Thread 1's next-action list. Mick greenlit the whole list
and asked for an immediate commit rather than letting today's work ride the
9pm daily sweep.

1. **Auth-canary preflight** - added `preflight_auth_check()` helper to
   sharescope_nlm_researcher.py (co-located with `run_nlm()`). Runs
   `notebooklm auth check --test` (live token fetch against Google). Wired
   into `run_nlm_research()` immediately before Step 0. Halts on failure with
   a clear "run `notebooklm login`" message. Closes the up-to-6-hour cache-
   lie window that the auth monitor cannot see.

2. **Skip Nina's legacy v1** - added module-level
   `SKIP_LEGACY_V1_REPORT = True` (with docstring explaining SOP v2.0
   rationale) and refactored the tail of `run_nlm_research()` so the Nina ask
   + save block is inside `if not SKIP_LEGACY_V1_REPORT:`. Extracted the
   notebook title-rename step (Step 5) OUTSIDE the conditional so it always
   runs. Flip the flag to False to bring Nina's v1 back as a safety-net.

3. **Logout Page.press bug** - line 77 of sharescope_logout.py:
   `page.press('Control+Shift+L')` -> `page.keyboard.press('Control+Shift+L')`.
   The old form required a selector as its first argument and threw the
   "missing 1 required positional argument: 'key'" cosmetic warning on every
   single run.

4. **Watcher on the Ron pipeline** - top-of-file docstring rewritten to SOP
   v2.0. Added `run_chart_orchestrator(ticker)` helper mirroring the existing
   `run_orchestrator(ticker)` pattern (subprocess to
   sharescope_chart_orchestrator.py, 180s timeout, reads
   `chart_result_{TICKER}.json`). Wired in as Step 2b after CSV export. Added
   `result["next_action"]` field on run_complete payload with three explicit
   forks: nlm_ok + chart_ok ("spawn Ron via subagent_type"), nlm_ok only
   (fundamentals-only fallback), and nlm_failed. Documented explicitly that
   the watcher CANNOT invoke Ron itself (named sub-agents only exist inside
   a Claude Code session), so it stops at "notebook + chart ready" and hands
   off via the next_action field. Test on the next voice trigger.

5. **Notion Research Database backfill** - two entries created in Research
   Database (main items), data source id
   `ac552ce5-2ceb-4ffb-a502-7d5da6c67cf8`. Title convention:
   `YYYY.MM.DD - [Company Name] ([TICKER]): Ron's Analysis`. Tag:
   `Cedric's Report` (existing tag, kept for consistency). EPIC and
   Company/Source Name relations point at the ticker collection
   `2f3b567d-5dd5-4a64-ae9b-a33df0ee53e5` (JSE ticker page id
   `170c3f50cea64b06a5ec7bc78b47bb36`; ENQ ticker page id
   `17b9a7b1ecc04d338a6c61272d735ada`). `userDefined:URL` on each entry is
   the working obsidian:// deep link back to the vault v2 file. Icon: chart
   (matches historical entries).
   - JSE: https://app.notion.com/p/3a4db32a9b0a819ea59bcfe96b25d28a
   - ENQ: https://app.notion.com/p/3a4db32a9b0a81afa78ece40d501d945

All three edited scripts pass py_compile.

**Immediate commits (Mick's request):**

- ShareScope-Automation is a NESTED PRIVATE GIT REPO under 04-Projects/,
  gitignored from the Dex-MickP repo (line 46 of .gitignore). Branch
  `post-webinar-dev`. NO REMOTE - the "ShareScope-Automation needs its own
  private repo" open item from the July personal-backup work is still open.
  Committed `42f2fd5` with ONLY the three script edits from this session
  (`sharescope_nlm_researcher.py`, `sharescope_logout.py`,
  `sharescope_watcher.py`). Pre-existing local mods to sharescope_login /
  orchestrator / research_log.py + docs from prior sessions were left
  deliberately untouched. Local only, nothing pushed.

- Dex-MickP repo `main`, origin `git@github.com:Mick-P-UK/Dex-MickP.git`.
  Used `git add -A` (matches daily_git_commit.py pattern). 19 files, +978/-62.
  Includes: `.claude/agents/ron.md`, both today's baton archives
  (14:35 + 18:39), ENQ v2 + Nina v1 safety-net, JSE v2 docx, LATEST.md,
  Companies/ENQ profile bump, `_index.md` ENQ bump, plus 9 ambient
  YouTube-Queue markdowns and one NBLM prompt note from the daily
  gmail-self-notes sweep. Commit `4ca4235`, pushed clean
  (`9ade3da..4ca4235 main -> main`). Working tree clean end-of-day.

- The 07:38 automated daily commit had already run this morning (Committed
  20 change(s) then Push succeeded, per `_git-commit.log`). Tonight's 9pm
  sweep will be a near no-op because everything's already up.

**Standing open items to carry forward:**

- **RESTART the ShareScope watcher** (pid 2328, `nlm_auth_status: ok`,
  started 07:34 today). The running process still has the OLD code loaded -
  any voice-triggered research fires the old flow. HIGH PRIORITY before the
  next voice trigger. `taskkill /pid 2328 /f` then relaunch via
  `start_watcher.bat` (or its equivalent).
- End-to-end validation of the Ron-aware watcher path (chart Step 2b +
  `next_action` signal) needs a real voice trigger since the changes landed.
- ShareScope repo remains without a remote. Today's `42f2fd5` is local only.
- Broken JSE chart PNGs (three in `downloads/JSE/` from the 20 July debug
  loop, plus one uploaded as source `2a9c622c-7f55-42b4-836f-6b4a484b26ce`
  in the JSE NBLM notebook). Next JSE pipeline run selectively clears the
  notebook side; local PNGs need manual tidy.
- MCSB PRD v0.3 reconciliation (task `^task-20260711-002`) still open.

Full detail: `_handovers/LATEST.md` (currently the 18:39 baton).

---

## Recent session: 2026.07.19 (Sunday, Claude Code, late afternoon) - July newsletter published end-to-end + newsletter-wp-publisher skill + Newsletter SOP v2.0

- CONTEXT: direct continuation of the 2026.07.18 17:01 baton handover. July Freedom
  Blueprint was FINAL (v.01.07) but the WordPress HTML still carried placeholder image,
  PDF, and cross-link URLs pending Mick's manual upload.
- AUTOMATED THE PUBLISH STEP: Mick asked if the whole WordPress publish could be done by
  Cedric instead of him doing it by hand. Confirmed the existing wordpress-image-uploader
  and wordpress-post-publisher skills (built for the portfolio-posting pipeline) work
  identically from Claude Code - their "Claude Desktop only" note is stale, Claude Code
  has direct .env/disk access, no Filesystem MCP required. Verified all three WP
  credential keys present in .env before touching anything live.
- RAN THE JULY PUBLISH: located the 6 local newsletter images + final PDF (one image,
  the Investor Psychology video thumbnail, only existed embedded inside the final DOCX -
  extracted via PowerShell ZipFile.ExtractToDirectory, identified visually among the 8
  embedded images, saved properly into Newsletter-Images). Uploaded all 7 files to the
  diy-investors.com media library via Poster Pete's Application Password, replaced every
  YOUR_MEDIA_URL/YOUR_PDF_URL/YOUR_MAY_POST_URL placeholder with the real returned URL,
  pushed a content-only update onto Mick's existing draft (post 15514) - status left as
  draft throughout. Mick then previewed and published it live himself, and sent the
  member email.
- BUILT newsletter-wp-publisher SKILL (Dex-MickP\skills\newsletter-wp-publisher): Mick
  asked for this to become a proper reusable skill rather than a one-off script, and
  asked - with nothing concrete planned - whether it could extend to a possible future
  second newsletter on diy-investors.ai. Built as manifest-driven (deliberately NOT
  folder-scanned like the portfolio skill, because newsletter filenames aren't
  convention-locked enough to auto-detect safely), multi-site aware via a SITE_KEYS
  table, supporting both `update` (existing draft, content-only) and `create` (brand new
  draft, untested in practice yet) modes. Status is always hardcoded to draft in both
  modes. Aborts before writing the HTML file or touching the post if any placeholder
  is left unresolved. Confirmed WP_DIY_AI_URL/USER/APP_PASSWORD already exist in .env
  (left over from the portfolio-posting skills) and the skill's site table already
  supports diy-investors-ai - flagged explicitly as wired but UNTESTED until a real AI
  for Investing newsletter run happens.
- REGISTRY + SKILL DOCS: added newsletter-wp-publisher to SKILLS_REGISTRY.md; added
  workflow step 10a and two Cycle Learnings entries to the diy-newsletter skill
  (Mick's-Writing-System vault); resolved (partially) the long-open "Cedric cannot
  verify live WordPress posts" issue note - REST API read-back now works, but visual
  browser rendering of the member-gated site still doesn't, so Mick's own preview
  check before publishing remains the final gate.
- REBUILT THE NEWSLETTER SOP TO v2.0: Mick flagged a draft SOP had been started in
  April 2026 (v1.0 docx, found alongside a parked June 2026 pickup note that had
  scoped almost exactly what was needed) but never finished and was now stale (fixed
  at 4 pages, WordPress publishing documented as fully manual, missing every rule
  added since - provenance footer draft/final split, version-bump-on-handback,
  widow/orphan check, section-dividers-not-page-breaks). Rebuilt as an 8-phase
  checklist at Mick's-Writing-System\0.0 - Inbox\2026.07.19 - Freedom Blueprint
  Newsletter SOP v2.0, produced in three formats on request: .md (source of truth),
  .txt (plain read-through copy), .docx (formatted with the mandatory provenance
  footer, since it's a working vault document not customer-facing final output).
  Old v1.0 docx left in place for historical reference, not deleted.
- MEMORY: Writing System auto-memory updated - project_july_newsletter.md (new
  PUBLISHED section), new project_newsletter_wp_publisher_skill.md, new
  project_newsletter_sop.md, MEMORY.md index entries for all three.

---

## Recent session: 2026.07.12 (Sunday, Claude Code, afternoon) - NotebookLM CLI infrastructure + Fourthwall research

- WHY THIS SESSION HAD TO BE CLAUDE CODE, not Cowork: post-7-July, Cowork runs in a cloud sandbox that cannot reach the locally installed `notebooklm` CLI on Mick's PC. Claude Code's shell runs on the PC, so the CLI is reachable. Direct follow-on to the 2026.07.10 "The Day Cowork Moved to the Cloud" episode.
- CREATED a GLOBAL custom skill `notebooklm-cli-custom` at C:\Users\pavey\.claude\skills\ (available to every Claude Code session on this PC). Nine sections: preflight; the correct `ask --save-as-note` single-step save; the PowerShell escaping recipe for `notebooklm note create` with long content (proven live: ~20 KB Fourthwall PDF report posted successfully after the wrong-first-attempt taught us the escape trick); the dual-save pattern (vault + notebook studio); ASCII cleanup table tied to CLAUDE.md's rule; tag-case check against existing vault tags; gotchas (including two added later this session: the ask/status auth-expired false positive on 0.3.4, and the Windows doctor Profile-Dir false positive on 0.7.3).
- FOUR vault-library `notebooklm-*` skills brought into Claude Code's view via SYMLINKS (not copies). Elevated PowerShell script generated for Mick; he ran it; all four verified live in the session without restart. Source of truth stays at Dex-MickP\skills\notebooklm-* (registered in SKILLS_REGISTRY.md, mirrored to /mnt/skills/user/ for Cowork). Same underlying files, two doors.
- NEW C:\Users\pavey\.claude\_rules.md - separate file so behavioural rules can be iterated without touching foundational CLAUDE.md. Wired in via an `@_rules.md` import line under the header of the master CLAUDE.md (bumped v1.3 -> v1.4, changelog row added). First rule seeded: "on any user mention of NotebookLM / Notebook LM / notebooklm / NBLM, before any tool call, consult the notebooklm-* skills available." Direct consequence of today's session where the four existing vault-library skills were initially invisible to Claude Code.
- UPGRADED notebooklm-py 0.3.4 -> 0.7.3. Mick ran `python -m pip install --upgrade notebooklm-py` + `notebooklm skill install`. Auto-migration preserved auth (29 cookies, storage_state.json intact). Rationale documented from the GitHub release notes for 0.4/0.5/0.6/0.7 minor bumps: no breaking changes affecting Mick's CLI usage; substantial auth-reliability and Windows-console fixes. Post-upgrade retest of the earlier failing `notebooklm ask` was a clean success first attempt, so today's 0.3.4 "ask says auth expired but status works" false positive is fixed.
- `notebooklm doctor` on 0.7.3 warns "Profile Dir permissions: 0o777, expected: 0o700" on Windows. Get-Acl on the folder shows Owner (MICK_PC25\pavey) + NT AUTHORITY\SYSTEM + BUILTIN\Administrators only; NO BUILTIN\Users / Authenticated Users / Everyone. Cosmetic false positive - Python's `os.stat` synthesises POSIX bits on Windows that do not reflect the real ACLs. Documented in the custom skill's Gotchas. GitHub issue drafted for teng-lin/notebooklm-py; browser tab opened at issues/new for Mick to paste-submit. Do NOT run `notebooklm doctor --fix` blindly on this warning.
- FOURTHWALL research (via the notebooklm-chat pattern - answered via the CLI then saved to the vault): (1) TIER REPLICATION - the notebook confirmed mirroring all three tiers (Bronze free / Silver Inner Circle / Gold Plaza) into Fourthwall unchanged; native support for 0-priced free tier; Merchant of Record; 5% flat fee. Mick's addendum on the vault note captured the critical simplification: his members are ALL annual with the Feb 2027 renewal window, so the notebook's mid-cycle-churn campaign concern does NOT apply here - the platform switch simply IS the renewal. (2) PDF SALES - 8-section report from the Fourthwall notebook: 2 GB file upload limit; 5% flat / 0% on Pro; VAT handled by Fourthwall; YouTube Merch Shelf rejects digital items (workaround = "Trojan Horse" physical proxy product); free-PDF lead magnet as top-of-funnel into Bronze; framing note for DIY-investing = first-person "how I built my portfolio" not "how you will make X%". Both reports filed to Dex-MickP\00-Inbox with the Fourthwall tag. PDF sales report also posted BACK as a note in the Fourthwall NotebookLM studio panel (dual-save pattern's first real test).
- Level 2 END-TO-END TEST of the notebooklm-chat vault-library skill - ran the whole pattern from ask -> Cedric-format -> Write to Dex-MickP\NotebookLM-Queries. Query: "flat transaction fee for digital products"; answer: "5% flat, 0% on Pro"; ran clean after the CLI upgrade. Proves the symlinks work end-to-end.
- TWO MEET CEDRIC EPISODES drafted to Notion Micks Content Studio (both Project=Meet Cedric, Format=Video, Status=Draft, Audience=YouTube/Public): "When the Job Moves House (Why Cedric Sometimes Has to Work Inside Claude Code)" - the routing story; "Two Doors, Two Toolkits (Why Cowork and Claude Code Don't Share Every Skill)" - the different-skill-locations story with the room/toolkit metaphor.
- AUTO-MEMORY (Writing System project): `project_notebooklm_cli_custom_skill.md` and `project_fourthwall_migration.md` written; `MEMORY.md` index updated with both entries.
- OPEN: (1) GitHub issue for the Doctor Windows false positive is DRAFTED but not submitted - Mick pastes into the open browser tab; (2) pre-existing bug in the vault-library `notebooklm-add-content` SKILL.md references `--confirm` on `source remove` and `note delete` (should be `-y / --yes`), small edit deferred; (3) Fourthwall PDF topic research (choosing a specific lead-magnet subject for DIY investors) is a planned separate task Mick flagged; (4) `notebooklm-cli-custom` trigger phrases untested across a session boundary - cold-start proof is next session.

---

## Recent session: 2026.07.11 (Saturday, Cowork, evening) - Hermes project, full vault ASCII cleanup, non-ascii-sweep skill, git fix

- NEW project 04-Projects/2026.07.11 - Hermes-Claude-Obsidian (index note carries the NotebookLM
  id/url/title in YAML), paired with the notebook Mick made via the notebooklm CLI (id
  fa003870-78c0-45f4-9df1-c815958f88f7). Registered in the project index (04-Projects/README.md
  Active Projects) and cross-linked from the in-vault MCSB note (2026.05.11-MCSB-Webinar-Voice, new
  Section 10). Drafted a Meet Cedric episode (investigate Hermes Agent as a route to help the MCSB
  build). Added the Hermes guide as a source into the notebook via notebooklm.google.com (Copied text).
- FULL vault ASCII cleanup: typography corruption fixed everywhere; then per Mick's choices currency
  -> ASCII (GBP/EUR/c), status glyphs -> tags, decorative emoji + ShareScope PUA glyphs + broken
  U+FFFD dropped, accents transliterated, 9 cp1252 files re-decoded (incl 4 Writing System pieces).
  413 files; verification = ZERO non-ASCII in any decodable text file. Root cause: Mac-seeded DEX
  templates (now cleaned). Report: System/Debug_Logs/2026.07.11 - Vault ASCII Cleanup Report.md.
  Left alone: 6 undecodable junk/binary files + credential pickle + .obsidian. CAVEAT: accents were
  transliterated vault-wide (e.g. any 08-People names) - restorable from git if wanted.
- Built skills/non-ascii-sweep (scan/safe/full). ascii_sweep.py is PURE ASCII by design (chr code
  points) so it can never corrupt its own maps; auto-detects the vault root; writes dated reports.
  Scheduled non-ascii-sweep-weekly Sat ~10am London, SAFE mode only. Registered in SKILLS_REGISTRY
  (Section 1a + Section 5). GOTCHA: Write/Edit truncated the large .py at ~285 lines and did not sync
  to the bash mount - wrote the final script via bash heredoc; PREFER heredoc for large script files.
- Fixed daily_git_commit.py: it built the message inline (git commit -m), so 503 files exceeded the
  Windows ~8191-char command-line limit ("command line too long"); patched to git commit -F tempfile
  and capped the config/docs lists. Backup .bak-2026-07-11. Would also have failed tonight's 9pm sweep.
- Git: today's main body committed + pushed by Mick from PowerShell (5e10b38, 505 files, to
  github.com/Mick-P-UK/Dex-MickP). Sandbox has NO SSH key so pushes must come from his PC. Later edits
  (script patch, registry, this wrap) ride the 9pm sweep (now the fixed script) or a manual push.

---

## Recent session: 2026.07.11 (Saturday, Cowork, evening 2) - Hermes-Claude-Obsidian project + NotebookLM

- Mick created a NotebookLM notebook (via the notebooklm Windows CLI, which he runs
  himself - I cannot type into a Windows terminal from Cowork). Title "Hermes + Claude +
  Obsidian_Updated:2026.07.11"; id fa003870-78c0-45f4-9df1-c815958f88f7.
- Set up the matching project in the vault: 04-Projects/2026.07.11 - Hermes-Claude-Obsidian/
  with an index note carrying the notebook id/url/title in YAML frontmatter. Date-first per
  our naming rule; name hyphenated (Hermes-Claude-Obsidian) to stay strictly ASCII.
- Registered it in the PROJECT index (04-Projects/README.md - added an Active Projects
  section) rather than a vault-level index, at Mick's steer.
- Cross-linked it FROM the in-vault MCSB project note (2026.05.11 - Cedric Webinar Voice
  Integration and MCSB Knowledge Bridge) via a new "Section 10 - Related Explorations", so
  the MCSB thread does not lose sight of it. NOTE: the canonical MCSB PRD/PROGRESS still
  live OUTSIDE the vaults in the PAIDA Master folder; the webinar-voice note is the closest
  in-vault MCSB anchor.
- Drafted a Meet Cedric episode in the project folder ("Could an Open-Source Assistant Help
  Build Our Shared Brain?") - investigate-not-convert framing, weighs Hermes's memory/skills/
  scheduler upside against skill-poisoning / infrastructure-not-app risk.
- Purpose of the whole thread: assess whether Hermes Agent shortcuts or informs the MCSB
  build. Grounding doc is the 00-Inbox Hermes guide (prepared for the 29 Jul 2026 webinar).
- Mick then asked to add that Hermes guide as a source into the notebook via
  notebooklm.google.com (browser route, not the CLI).

---

## Recent session: 2026.07.11 (Saturday, Cowork, evening) - Session-start continuity fix + MCSB prep

- Mick asked "where were we"; the morning's Personal Content Backup work was missing from the
  top of memory. Diagnosed: the 14:05 baton flushed CEDRIC_MEMORY.md but APPENDED the block at
  the file bottom while the top Last Updated stack still read 07.10, so a top-down session-start
  missed it. Not a "memory never written" bug - a "written in the wrong place" bug.
- Fixed BOTH ends. Write side: baton-wrap step 3 + sundown-wrap step 7 now carry an explicit
  PLACEMENT rule to PREPEND a new Last Updated line (under the heading) + a new Recent session
  block (after the first ---), never append to the bottom. Read side: session-start now reads
  _handovers/LATEST.md FIRST, then the memory top, and trusts LATEST if it is newer. Applied to
  the Dex CLAUDE.md (edited here) and the master C:\Users\pavey\.claude\CLAUDE.md (appended by
  Mick via PowerShell; backup CLAUDE.md.bak-2026-07-11).
- Tidied the orphaned 07.11 entry to the top; committed the whole fix (5e2f08f) over SSH.
- Brain dump captured to 00-Inbox; two tasks added to 03-Tasks/Tasks.md: ^task-20260711-001
  (give ShareScope-Automation its own private repo - unbacked-up) and ^task-20260711-002
  (reconcile MCSB PRD v0.3 with recent work + update PROGRESS.md and the Notion Build Tracker).
- MCSB PRD located: it lives OUTSIDE the vaults, in the PAIDA Master folder at
  C:\Users\pavey\Documents\0.0 - AI Projects\0 - PAIDA - Mick 2nd Brain\PAIDA Master - Second
  Brain\04-Projects\2026.05.09 - MCSB\2026.05.13-MCSB-PRD_V0.3.docx. Confirmed v0.3 is latest
  (v0.2.1 was an earlier draft). Converted it to PDF next to the docx. That folder also holds a
  maintained PROGRESS.md (updated 07.07) and three 07.10 Cowork-cloud/GitHub impact notes.
- Lifted the 13 May Phase 1 implementation pickup note into 00-Inbox (ASCII-normalised). It
  flags OQ2 "fold PAIDA Master into Dex?" - deferred then, ripe now given the PRD sits outside.
- Git: this afternoon/evening vault edits (brain dump, tasks, pickup note, this wrap) left for
  the 9pm sweep at Mick's choice. PDF sits in the PAIDA Master folder (not a git repo).

---

## Recent session: 2026.07.11 (Saturday, Cowork, afternoon) - Personal Content Backup executed

- Decision reversed: NO separate personal repo. Dex-MickP is now ONE PRIVATE repo holding
  everything, never published; a scrubbed DEMO repo would be derived if structure is shared.
- .gitignore rewritten: ignore only machine junk + secrets (.env, .mcp.json,
  System/.credentials/, tokens, pickles, *.log except _changelog/). All PARA content now tracked.
- Pre-commit ASCII hook rescoped to work-mcp inputs only (03-Tasks, 02-Week_Priorities,
  01-Quarter_Goals, 00-Inbox/Meetings, 05-Areas/People). Creative content backs up with typography.
- Fixed a corrupted Week_Priorities.md (injected python fragment) + 4 other in-scope files.
- First full backup committed + pushed (7e02ee7, 291 files). Repo current with GitHub.
- Auto-push FIXED: nightly daily_git_commit.py always pushed but GCM/wincredman failed headlessly.
  Switched origin to SSH (dedicated ed25519 key on Mick-P-UK). Verified push works (commit 1ca585c).
- Still open: ShareScope-Automation own private repo (unbacked-up); minor cruft tidy; point
  Cowork default folder at Dex-MickP.
- Handover baton: _handovers/archive/2026.07.11 - 1404 - baton - Personal Content Backup.md.

---

## Recent session: 2026.07.10 (Friday, Claude Code CLI, evening) - PATH file ASCII cleanup closed out

- Picked up the SOP note left from 2026.07.10: "2026.07.10 - NOTE - Clean the PATH UiPath File
  for ASCII (Local)_v1.0.md" flagged that the PATH (UiPath Inc.) financial analysis file was held
  back from the same-day GitHub commit because the Dex-MickP pre-commit hook blocks non-ASCII bytes.
- Read the file, grepped for non-ASCII bytes: found exactly ONE offending character used twice, an
  em dash (U+2014) in the "Overall Summary and Recommendation" section - "share repurchases-
  deploying a fresh $500 million authorization-will help put a floor under the stock price."
  Replaced both instances with spaced ASCII hyphens; meaning unchanged.
- Re-grepped: zero non-ASCII bytes remain. Confirmed both the research file and the SOP note were
  untracked (first commit, not edits of an existing tracked file).
- Committed both files together (2312d47) with the pre-commit hook reporting "UTF-8 check passed (2
  .md file(s) clean)", then pushed to origin main (10b5a83..2312d47).
- OUTSTANDING (carried forward, unchanged): the held June end-of-month portfolio posting run (month-
  end 30 Jun, post date 9 Jul, all four portfolios) still needs to be run from Claude Desktop -
  Cowork cannot reach the WordPress credentials in C:\Users\pavey\.env. Also still open: the second
  SOP on "which environment runs what" (Desktop vs Cowork vs claude.ai), offered but not yet built.

---

## Recent session: 2026.07.09 (Thursday, Cowork) - SOP library started

- Mick asked how the end-of-month portfolios get posted to diy-investors.com. Walked him through
  the four-skill chain: portfolio-post-creator (orchestrator) -> benchmark-fetcher +
  wordpress-image-uploader -> wordpress-post-publisher. Posts are created as DRAFTS only; Mick
  reviews the wp-admin edit URL and publishes. Four portfolios (UK/US Active 10, Yr1 + Yr2).
- CONSTRAINT confirmed: the routine cannot run from Cowork because Poster Pete's WP creds live in
  C:\Users\pavey\.env and Cowork cannot mount the home folder (reserved as internal session
  storage) nor read the file directly. The WP API itself IS reachable from the sandbox (HTTP 200);
  only the credential read is blocked.
- June run (month-end 30 Jun 2026, post date 9 Jul, all four portfolios) HELD for Claude Desktop at
  Mick's choice. Re-issue there: "Run the end-of-month portfolio posts for 30 June, all four
  portfolios, post date 9 July."
- Started an SOP LIBRARY at 06-Resources\SOPs\. First entry: "SOP - End-of-Month Portfolio
  Posting.md" (YAML tag SOP; ASCII-clean; grounded in the four skills). Mick wants SOPs for all
  recurring workflows; flagged SOP-creation itself as a Meet Cedric topic. Offered a second SOP on
  "which environment runs what" (Desktop vs Cowork vs claude.ai) - pending.

---

## Recent session: 2026.07.04 (Saturday, Cowork) - ax-mapper + ShareScope map v1.5

- Imported an overnight claude.ai conversation + attachments (Playwright agent CLI proposal) into
  the ax-trees-automation project.
- Built ax-mapper in the Dex vault (skills/ax-mapper/): a GENERIC, read-only accessibility-tree UI
  mapper. Engine is app-agnostic; each app is a small adapter. Offline suite 18/18. Reusable for ANY
  Playwright-drivable web app - copy adapter-template.js to add one.
- CONVERGED the ShareScope mapper onto ax-mapper. 3-test live proof passed (179 controls, exact parity
  with master v1.4). Bespoke Node scripts archived (with sha256 manifest) then deleted.
- Extended the map to v1.5: news category selection (All/Share/List/RNS/Hot/Latest) + List design
  dialog; and the full PORTFOLIO download flow - selector -> pick portfolio -> holdings/transactions
  -> Sharing -> Export holdings/transactions -> Export options dialog (Holdings / latest / Transactions).
- TWO ShareScope adapters now: sharescope.adapter.example.js (stock; searches a ticker) and
  sharescope-portfolio.adapter.js (portfolio; NO stock search - the correct flow, Mick's steer).
- Key gotchas (in the master map): portfolio toolbar hidden in the single-stock Financials view;
  run the browser wide or rightmost toolbar buttons overflow; print-to-PDF is a Chrome/OS dialog and
  is NOT automatable (use CSV export).
- Meet Cedric episode drafted: meet-cedric/2026.07.04-teaching-cedric-to-read-any-app.md (TODO: post
  the brain dump to Notion Content Studio when the Notion connector is authorised).
- PENDING (Desktop): mirror skills/ax-mapper to /mnt/skills/user (dual-write rule - could not be done
  from Cowork). Git: project committed via git-save.bat; vault syncs its own way.
- Full detail: ax-trees-automation/session-logs/2026-07-04-session18.md and SESSION19-PICKUP.md.

---

## Recent session: 2026.07.02 (Thursday late morning, Claude Desktop) - ShareScope 16:9 chart + .env consolidation

Continuation of the ShareScope automation WIP. Two fixes plus a credential-path sweep.

### 1. Chart now exports true 16:9 (docx + PowerPoint ready)
- Problem: the chart PNG came out near-square (~631x560) because the export took the default
  on-screen size.
- First attempt (reverted): widening the browser viewport before capture. Mick then spotted
  the real lever - the "Save chart as PNG (bitmap)" dialog has a Custom size option.
- Fix (sharescope_chart.py): the save step now ticks Custom and sets CHART_PNG_WIDTH x
  CHART_PNG_HEIGHT (1200 x 675) then clicks OK. Diagnostic logging added for the dialog fields.
- CONFIRMED: HDD chart came out exactly 1200 x 675 (aspect 1.778 = 16:9). Tunable via the two
  constants at the top of sharescope_chart.py.

### 2. Login .env fix (password rotation exposed a two-.env problem)
- Mick rotated the ShareScope password and thought he had updated the .env, but login kept
  failing "invalid password". Cause: the script read C:\Vaults\Mick's Vault\.env which still
  held the OLD password. Mick's real/canonical creds file is C:\Users\pavey\.env (the same file
  MCSB tokens + ax-trees already use). The Vault copy was a stale second file.
- Fix (sharescope_login.py): primary env_path repointed to C:\Users\pavey\.env; old Vault path
  dropped as primary. Added load_dotenv(env_path, override=True) so the .env always beats any
  stale OS env var, plus a "Reading credentials from: <path>" log line so the file in use is
  never ambiguous. CONFIRMED working - login clean, chart saved.

### 3. Credential-path SWEEP (repoint scripts off the old Vault .env)
- Canonical creds file is now C:\Users\pavey\.env for everything.
- Repointed to C:\Users\pavey\.env:
    - skills\wordpress-post-publisher\SKILL.md (2 refs: Credentials note + load_env code)
    - skills\wordpress-image-uploader\SKILL.md (1 ref: load_env default)
- Checked, NO change needed:
    - benchmark-fetcher (uses Yahoo Finance + a local xlsx, no .env)
    - portfolio-post-creator (delegates creds to the two WP skills, no .env of its own)
    - sharescope_login.py (already repointed in fix 2)
- NOTE: mirror copies (/mnt/skills/user/) NOT updated - vault is source of truth; mirror sync
  is part of the deferred 2026.06.03 skill audit and is unreliable anyway.

### 4. Credentials SINGLE-SOURCE rule added at the top level + all CLAUDE.md files reconciled
- Root cause of the recurring stray/stale .env problem: no top-level rule saying WHERE the one
  .env lives, so copies keep appearing (a project-subfolder copy on 2026-05-03; today's stale
  Vault copy). Fix = one authoritative rule at the highest level, everything else points to it.
- MASTER config C:\Users\pavey\.claude\CLAUDE.md bumped to v1.3 (changelog updated) with a new
  CRITICAL RULE: "Credentials - Single Source". In brief: ALL local script/skill credentials,
  keys and tokens live in ONE file only, C:\Users\pavey\.env; never create another .env; never
  hardcode; read with load_dotenv(override=True); FAIL (do not fall back) if a key is missing.
  Scoped to LOCAL contexts (claude.ai Web / Cowork sandbox have no local disk - secrets there
  arrive via connectors, not this file).
- Condensed copy added to CEDRIC_MEMORY.md Key Conventions (loaded every session).
- Reconciled every older/duplicate .env mention to POINT AT the master rule (stops drift):
    - C:\Users\pavey\.claude\.CLAUDE.md               -> converted to a pointer
    - C:\Vaults\Cowork\CLAUDE.md                      -> pointer (old block had em dashes)
    - C:\Vaults\Cowork\ax-trees-automation\CLAUDE.md  -> pointer (kept its placeholder-.env note)
    - C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\CLAUDE.md -> reframed its generic "Security & API
      Keys" section. That section was inherited from the Dex template and actually taught the
      OPPOSITE habit (create a per-project gitignored .env); now it defers to the single-source rule.

### 5. Verified Poster Pete / WordPress creds are safe BEFORE deleting the old .env
- Mick spotted Poster Pete (WordPress user 'posterpete', Editor) credentials in the redundant
  Vault .env and asked whether a routine would break when he deletes them.
- Traced: the only Poster Pete users are the wordpress-post-publisher + wordpress-image-uploader
  skills (called by the monthly portfolio-post-creator routine). BOTH were repointed to
  C:\Users\pavey\.env in the sweep (fix 3).
- CONFIRMED the WP keys are present in C:\Users\pavey\.env (WP_DIY_INVESTORS_URL/USER/APP_PASSWORD
  and WP_DIY_AI_URL/USER/APP_PASSWORD). So deleting the old Vault copy is SAFE - the monthly
  WordPress posting routine will still find its credentials. Values not recorded here.
- Note: WP_DIY_AI_APP_PASSWORD is still a placeholder (posting to diy-investors.ai was never
  wired up) - pre-existing, unaffected by the move.

### Endgame for Mick
- Once satisfied, DELETE / empty the ShareScope + WP credentials from the redundant
  C:\Vaults\Mick's Vault\.env so there is genuinely one source. Any straggler script still
  pointing there will then fail loudly with "missing credentials" - which flushes it out
  safely. Mick to locate any such stragglers (news checkers etc. - not confirmed to use .env).

### Still open (carried forward)
- Flip .env SHARESCOPE_HEADLESS back to true (currently false from the demo/testing).
- Fold the 6 financial CSVs into sharescope-report as tables (v0.2).
- Fix the harmless sharescope_logout.py cleanup warnings (project-wide, non-blocking).
- COWORK: test whether Cowork can run the local Playwright automation; bundle skill scripts.
- ASCII clean-up of the Cowork + Dex CLAUDE.md rulebooks (legacy em dashes + mangled tick marks) - logged as a non-urgent memory task 2026.07.02.

### Resume phrase
"Cedric, I'm back. Let's pick up the ShareScope work - report financials tables next."

---

## Recent session: 2026.07.01 (Wednesday early evening, Claude Desktop) - ShareScope chart + report automation

Started from "find the old ShareScope work"; ended with a working single-session automation
that captures a chart, pulls financials, and folds the chart into a branded report. Built on
the existing 04-Projects\2026.04.04-ShareScope-Automation modules (login/search/export/logout/
utils reused UNCHANGED - only new orchestration + a chart module were added).

### Built this session
- sharescope-get-chart skill (v1.0): native 12-month "Save chart as PNG (bitmap)" export for
  any ticker. Files: sharescope_chart.py + sharescope_chart_orchestrator.py.
- sharescope_session.py (SESSION RUNNER): one login, many tickers/tasks, one logout. The
  standard multi-task entry point; report skills import run_sharescope_session(). Confirmed
  on HDD: chart + 6 financial CSVs in a single 26s session.
- sharescope-report skill (v0.1): embeds the chart into DIY_Investors_Report_Template.docx.
  Proven with a real Hardide (HDD) Stock Research Brief - chart embedded, branding intact.

### Selectors confirmed live (2026.07.01)
- Chart view button: button[data-cmd="ViewChart"] (name "Chart" matches TWO elements).
- 12-month period control: labelled "1 year".
- Save item: "Save chart as PNG (bitmap)..." (a scaling dialog appears - click OK).

### Deliverables
- 2026.07.01 - HDD - Stock Research Brief.docx (sample report with embedded chart).
- 2026.07.01 - ShareScope Demo - Webinar Crib Sheet (pdf + docx) - six-step live runsheet.
- Meet Cedric episode in Content Studio (Draft, Video):
  https://app.notion.com/p/390db32a9b0a81b0a74dfab05fe44686
- Build record + pickup + episode pack: 04-Projects\2026.07.01-ShareScope-Chart-Export\
  (BUILD_LOG.md is the primary handoff doc).

### RESOLVED 2026.07.02
- DONE: Stripped the ShareScope username + password from PLAIN TEXT in
  skills\sharescope-financials\SKILL.md - replaced with <your-sharescope-username> /
  <your-sharescope-password> placeholders pointing at the .env only. Swept the other
  four sharescope skills and reference files - no other copies of those credentials.
  Mick to rotate the exposed ShareScope password and update C:\Vaults\Mick's Vault\.env.

### Other open items (post-webinar)
- Fold the 6 financial CSVs into the report as summary tables (sharescope-report v0.2).
- COWORK GOAL: (a) TEST whether Cowork can execute the local headless Playwright automation
  before assuming it (Test, Don't Trust); (b) bundle each skill's scripts into its own folder
  so they are self-contained/portable rather than pointing at the April project.
- Fix the harmless sharescope_logout.py cleanup warnings (project-wide, non-blocking).
- Dual-write the new SKILL.md files to the /mnt/skills/user mirror.

### Note for next session
- .env SHARESCOPE_HEADLESS is currently FALSE (set for tonight's live webinar demo so the
  browser is visible). Flip back to true for hands-off runs after the webinar.

### Resume phrase
"Cedric, I'm back. Let's pick up the ShareScope report automation - financials tables next."

---

## Recent session: 2026.06.30 (Tuesday evening, Cowork) - Prompt Library single-source-of-truth + Git fix

Mick asked where to store his prompt markdown notes (currently a dumping ground in Mick's
Vault) so they live in ONE place and are GitHub-backed. Agreed model: MOVE (not copy) them
into Dex-MickP\06-Resources\Prompts\ as the human-friendly SOURCE; keep PROMPT_LIBRARY.md
(C:\Vaults\Cowork) as the single OPERATIONAL file AHK + demos read.

### Built this session (scaffolding only - 141-file migration NOT started)
- 06-Resources\Prompts\README.md, _Prompt-Template.md, 00-Index.md, Prompts.base.
- Frontmatter schema aligned 1:1 with PROMPT_LIBRARY.md, linked by a shared `code` (CAT-NN).
  Fields: title, code, category (NBLM INV SUM CON ANL COM WEB GEN), ahk, version,
  date_created, date_updated, status, operational, tags (always starts with `prompt`).

### Git automation detour (now fixed)
- Repo had 7 local commits never pushed to GitHub. Pushed them (now in sync).
- Cause = holiday 12-24 June (PC off) + a logic gap (daily script skipped the push on
  no-change days) + scheduled push failing on commit days.
- Edited daily_git_commit.py: pushes whenever local is ahead (self-heals backlog), logs to
  _git-commit.log. Verified py_compile on Mick's PC. Enabled Task Scheduler history.
- LESSON: do NOT run git from the Cowork sandbox on this mount - it left a stale
  .git\index.lock that the sandbox could not remove (Mick deleted it on Windows). Sandbox
  also reads half-synced (truncated) copies of files on the cloud drive - trust the host
  Read tool, not bash, for file integrity on C:\Vaults.

### Still open (the actual job)
- Migrate 141 prompt .md files from Mick's Vault (131 in 0.0 - Inbox, 9 in Projects, 1
  template). Pilot ONE group first (NBLM or Perplexity), normalise frontmatter, dedupe
  near-identicals (flag before deleting), regenerate 00-Index.md, confirm Base in Obsidian.
- READ TO RESUME: PICKUP_NOTE_2026.06.30-Prompt-Library-Migration.md (Dex root).

---

## Recent session: 2026.06.03 (Wednesday late morning) - Skill dual-write audit (PAUSED for webinar)

Started with a routine task (add red "Click here for Report" CTA to a Coeur Mining CDE
report image via image-cta-overlay). Noticed the mirror copy of image-cta-overlay was a
STALE v1 (fixed 52px font, overflow bug) vs the correct v2.2 in PRIMARY. Synced it, then
ran a FULL audit of every skill across the three locations.

### Locations and headline
- MIRROR  /mnt/skills/user/                                 21 skills
- PRIMARY C:\Vaults\Mick's Vault\.claude\skills\            20 skills
- DEX     C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\  28 skills
Of the 12 skills that live in 2+ locations, only 2 were byte-identical
(yt-play-button-overlay; image-cta-overlay after today's fix).

### Fixed and VERIFIED this session (mirror writes only)
- image-cta-overlay: Mirror <- PRIMARY v2.2 (md5 6f5e4c5f).
- annie: Mirror <- PRIMARY (md5 9f133960). Fixed a FUNCTIONAL BUG - mirror used dead
  tool names (list_gcal_events, find_free_time); now Google Calendar:gcal_list_events etc.
- pdf-to-pptx-converter: Mirror <- DEX v1.1 (md5 fff2a7a3).
WARNING: these are mirror-only writes, not version-controlled. If the mirror resets they
are lost again.

### Important reconciliation with existing memory
- The "Mandatory Skill Deployment Protocol" already mandates DEX (master) + mirror, and
  SKILLS_REGISTRY.md is the declared source of truth. So the canonical model is NOT an
  open question - it is Dex + mirror.
- BUT in practice PRIMARY is still the live source for annie + image-cta-overlay, so the
  model is only partially realised on disk.
- The four skills migrated to Dex+mirror on 2026.05.30 are NOT in this project's mirror
  now. Either the mirror is project-scoped (that work was in the Poster Pete project) or
  it reset. This must be clarified before the mirror can be trusted as half the pair.

### Still open (deferred to after tonight's webinar)
- Re-establish the four migrated skills in the mirror from Dex; retire stale PRIMARY strays.
- Decide annie + image-cta-overlay home (migrate to Dex, or sanction PRIMARY as 2nd master).
- session-start FORK: PRIMARY v1.1 (correct) vs DEX (no frontmatter, OLD tool_search probe
  for env detection - contradicts the current Filesystem:list_allowed_directories protocol).
  Drop the Dex method.
- ai4inv-webinar-processor and notion-summary: parallel edits, manual pick needed.
- notion-summary vs notion-summary-generator namespace overlap to clarify.
- 15 mirror-only skills have NO disk backup anywhere - backup policy decision.

### Deliverables written
- Pickup note (comprehensive): PICKUP_NOTE_2026.06.03-Skill-Audit.md (Dex root) - READ THIS to resume.
- Full report: /mnt/user-data/outputs/2026.06.03 - Skill Dual-Write Audit.md (Mick downloaded).

### Resume phrase
"Cedric, I'm back. Let's pick up the skill dual-write audit from the pickup note."

---

## Recent session: 2026.06.01 (Monday) - AI report template library extended + Aptos font rule

Set up a reusable reference for sector-wide screening reports and locked in a font standard.
- New template type: `06-Resources/AI_Report_Templates/Sector_Screen_Report/` created
  alongside the existing `Research_Brief/`. Purpose: multi-company sector screens / rankings
  (landscape), distinct from the single-company portrait Research Brief.
- Worked example saved there by Mick: `PM_Miners_Quarterly_Growth_Consolidated.docx` - US
  Precious Metal Miners (63-stock ShareScope universe) quarterly growth report. 5 tables
  (OCF Top 10, turnover Top 10, full 23-name ranking, performance overlay, valuation overlay)
  + 3 matplotlib quadrant charts (turnover vs YTD price; turnover vs forecast PE; turnover
  vs PSR). 12 pages, landscape, Aptos 12pt.
- `Sector_Screen_Report/README.md` written: structure, house style (hex codes), methodology
  (sequential QoQ turnover, de-cumulation, SEC-XBRL-plus-web-research for foreign filers,
  state-exclusions-never-estimate), and build approach (docx-js + matplotlib).
- `AI_Report_Templates/CHANGELOG.md` updated with a 2026-06-01 entry.
- New standing style rule recorded: all .docx default to Aptos 12pt body (see Key Conventions).
- Key analytical finding from the example worth recalling: sequential turnover growth had
  near-zero correlation with YTD share-price performance (Pearson r approx 0.02) - the
  turnover ranking is an operational-momentum / candidate-generation tool, not a price-timing
  signal. The dual-metric names (Coeur, Kinross, Agnico) screened most internally consistent.

---

## Recent session: 2026.05.30 (Saturday) - End-of-month skills migrated to Dex vault

Migrated the four DIY Investors end-of-month portfolio skills from the Poster Pete
(C-Pete) claude.ai project into the Dex vault + mirror:
- Skills: portfolio-post-creator v2.2, benchmark-fetcher v1.0,
  wordpress-image-uploader v1.0, wordpress-post-publisher v1.1.
- Dual-registered V + M (verified byte-identical). In-file path headers fixed to Dex paths.
- Registry updated: CLAUDE.md, skills/README.md, SKILLS_REGISTRY.md (Section 1b -> 1a,
  portfolio-post-creator v2.0 -> v2.2, Pending Action #1 closed).
- Credentials: .env stays single-source in C:\Vaults\Mick's Vault\.env (Mick's decision -
  not duplicated to Dex, avoids drift when passwords change). WordPress skills point there.
- Originals left in C:\Vaults\Mick's Vault\.claude\skills\ for now (not deleted).
- CHANGELOG.md left as a pure Cedric Server CODE / SemVer log (Mick's decision 2026-05-30); this housekeeping recorded in this memory, the session log, and SKILLS_REGISTRY.
Full detail: System/session_log.md (2026-05-30 entry).
[2026.06.03 note: portfolio-post-creator is now v2.3 and wordpress-post-publisher v1.2 in
Dex (2026.05.30 tag rules); and these four are not visible in this project's mirror - see
the 2026.06.03 audit entry above.]

---

## Top of Mind - 2026.05.17 (Sunday)

### MCSB (Mick and Cedric Shared Brain) -- PHASE 1 IN PROGRESS
**Status:** Phases 1.1, 1.2, 1.3a-1.3g all COMPLETE and PROD-confirmed. Server at v0.4.0. Phase 1.3 (Cedric Server v0.1 series) is now FULLY COMPLETE. Phase 1 first publish to GitHub also done (16 files in milestone commit 2026-05-17 14:35 London). Next: Phase 1.4 (mostly done already, just needs ratification) + Phase 1.5 (MCP wrapper v0.1).
**PRD v0.3:** `PAIDA Master - Second Brain/04-Projects/2026.05.09 - MCSB/2026.05.13-MCSB-PRD_V0.3.docx` (includes D26)
**Pickup note:** `2026.05.17-MCSB-Phase1-Session5-Pickup-Note.md` in same folder -- READ THIS to resume
**Resume phrase:** "Cedric, I'm back. Session 6 -- let's confirm the autonomous tick fired since Session 5, then move to Phase 1.5 (MCP wrapper v0.1)."

**Build Tracker (Notion):** https://www.notion.so/b2462f490c7448cf8af9b51e91f1d159
**PROGRESS.md:** PAIDA Master - Second Brain/04-Projects/2026.05.09 - MCSB/PROGRESS.md
**Rule:** Both trackers updated together at end of every session / context refresh.

**Completed this session (2026.05.17 Session 5 -- afternoon):**
- cedric_server.py rewritten to v0.4.0 (22,017 -> 34,244 bytes): embedded the hourly worker as a FastAPI background scheduler task. Closes Phase 1.3g and seals the Cedric Server v0.1 series.
- APScheduler (AsyncIOScheduler) drives an hourly tick from inside the server, replacing the Windows Task Scheduler dependency.
- threading.Lock around each tick: non-blocking acquire so a slow tick can never overlap with the next; second call is recorded as status=skipped rather than queued.
- New endpoints (both PC-only via require_pc_token):
    GET  /worker/status   -- enabled / scheduler_started / lock_held / next_run / counts / last_run / last_skip / last_error
    POST /worker/run_now  -- manual trigger; optional ?dry_run=true override
- /health enriched with a worker block (next_run, lock_held, counts, last_run_summary).
- Clean @app.on_event("shutdown") hook so Ctrl+C exits the scheduler cleanly.
- Worker shim added (cedric_worker.py +1,401 bytes): run_worker_pipeline(dry_run, verbose) -- CLI-independent entry point. main() is now a 4-line CLI wrapper around it; CLI behaviour unchanged.
- Env vars: CEDRIC_WORKER_ENABLED / CEDRIC_WORKER_INTERVAL_MIN / CEDRIC_WORKER_DRY_RUN (sensible defaults).
- Sandbox tests: 25/25 paths green.
- PROD walkthrough (13:43-14:35 London on Mick's PC): every endpoint proven, scheduler started with first auto-tick scheduled, dry-run and real-run ticks both fired through, MCSB Phase 1 published to GitHub for the first time (16 files in milestone commit).
- Mid-walk hygiene: __pycache__/ added to .gitignore (line 94, confirmed by git check-ignore).
- Bug arc: stale .git/index.lock from old Task Scheduler racing first real tick. Recovered by Admin PowerShell + lock removal. Saved as the new "scheduler handover" feedback memory (always disable old driver BEFORE first real tick).
- Tooling note: Edit-tool apostrophe truncation hit again (Python this time). Memory broadened beyond JS to all languages. Used /tmp Python scripts as the apostrophe-safe alternative.

**Token env-var contract (locked Session 3):**
- MCSB_PC_TOKEN: full access including private + /search_all
- MCSB_MOBILE_TOKEN: restricted, no private, no /search_all
- Both live in C:\Users\pavey\.env -- NEVER copy elsewhere
- Mint with: `python generate_tokens.py` (helper in vault root)

**Pre-flight for next session: NONE.**
Server v0.4.0 is prod-installed and running with embedded scheduler. apscheduler dep installed. Old Windows Task Scheduler "Cedric Hourly Worker" job is DISABLED (still present, will be DELETED in Session 6 after one observation cycle). __pycache__/ now properly excluded from git. Phase 1 is on GitHub.

**Important: SECURITY ROTATION pending.**
The two tokens minted Session 3 were pasted into chat during the
walkthrough. Practical risk = zero today (server is 127.0.0.1 only),
but BEFORE the Cloudflare tunnel goes up, Mick must:
  cd C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP
  python generate_tokens.py
and swap the new tokens into .env. Flag this when tunnel work begins.

**Outstanding / Deferred:**
- Session 6 priorities: (1) confirm autonomous tick fired (tick_count > 3 with trigger=scheduler somewhere), (2) DELETE the disabled "Cedric Hourly Worker" Task Scheduler job via Admin PowerShell.
- Minor patch: surface git push failures as error_count++ rather than swallowing as pushed=False.
- Lifespan refactor (cedric_server uses deprecated @app.on_event; FastAPI 0.110+ prefers lifespan context manager). ~5 min, low priority.
- Windows service install for Cedric Server (still foreground dev mode).
- Token rotation before Cloudflare tunnel work.

**Meet Cedric episode arc:**
- Episode A: The 46-page PRD review (Content Studio logged 2026.05.13)
- Episode B: Building the Build Tracker (Content Studio logged 2026.05.13)
- Episode C: Building the Foundation -- vault restructure + hourly worker (Content Studio logged 2026.05.14)
- Episode D: The Server Awakens -- first endpoint live + final PRD decision logged (Content Studio logged 2026.05.15)
- Episode E: First Capture -- /memory/note plus two-tier bearer auth (Content Studio logged 2026.05.15 Session 3)
- Episode F: Cedric Catches His Own Bug -- 1.3d /agents/reload sandbox save (Content Studio logged 2026.05.17 Session 4). Bonus B-segment: PowerShell apostrophe quoting gotcha hit during PROD walkthrough.
- Episode G: Cedric Catches Phase 1 Crashing Lock-File Bug -- 1.3g handover race condition (Content Studio logged 2026.05.17 Session 5). Hero arc: deploying embedded scheduler raced the old Task Scheduler over .git/index.lock; teaches "disable old driver BEFORE first real tick". Bonus: milestone first publish of MCSB Phase 1 to GitHub.

### Subscription audit follow-ups (from 12 May afternoon session)
- Cancel Codia AI before 21 May (USD 20/month)
- Verify usage / decide on Synthesia (GBP 201.60/yr renews 25 Nov), Ideogram ($180/yr renews 2 Sep), Text Blaze ($35.88/yr renews 18 Aug)
- Cancel Alex McFarland "AI Writing Systems" Substack before 18 May (GBP 16/month - not actually cancelled despite earlier belief)
- Investigate hosting subs: Network Solutions (expired service notice 18 Apr), Bluehost, 123-reg, iPage
- ChatGPT Plus cancelled today, paid through to ~9 June - use it during the paid window
- Otter.ai Pro retained (Zoom auto-join workflow justifies it)
- OpenAI API billing plan cancelled 16 April (confirmed via platform.openai.com screenshot)

---

## SKILLS - SOURCE OF TRUTH

For any question about what skills exist, where they live, who built them, or how to invoke them, the canonical reference is:

  C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\SKILLS_REGISTRY.md

This file lists every skill across vault, mirror, plugin marketplace, scheduled tasks, and claude.ai PAIDA Projects (Pete, Cedric, Poppy). Update on every skill create / rename / version-bump / deprecate. See its Section 7 for maintenance rules.

[2026.06.03: A full audit found the on-disk reality has drifted from this registry's
intent - see the 2026.06.03 session entry and PICKUP_NOTE_2026.06.03-Skill-Audit.md.
Re-reconcile SKILLS_REGISTRY.md against all three locations when the audit resumes.]

---

## Session Log - 2026.05.17 Afternoon (MCSB Phase 1 Session 5 - 1.3g CLOSED, Phase 1.3 SERIES COMPLETE)

### What we did
- Built Cedric Server v0.4.0 (cedric_server.py 22,017 -> 34,244 bytes): embedded the hourly worker as a FastAPI background scheduler task. Closes Phase 1.3g and seals the Cedric Server v0.1 series.
- APScheduler (AsyncIOScheduler) drives an hourly tick from inside the server. threading.Lock guards re-entry (skipped, never queued). Two new PC-only endpoints: GET /worker/status, POST /worker/run_now. /health enriched with a worker block. Clean shutdown hook.
- Worker shim added: cedric_worker.run_worker_pipeline() is the CLI-independent entry point; main() is now a thin CLI wrapper. CLI behaviour unchanged.
- Env-var config: CEDRIC_WORKER_ENABLED / CEDRIC_WORKER_INTERVAL_MIN / CEDRIC_WORKER_DRY_RUN.
- Sandbox tests: 25/25 paths green (auth matrices on both new endpoints, dry-run tick, lock contention, regression on /memory/note and /agents/reload).

### PROD walkthrough (13:43-14:35 London, on Mick's PC)
- pip install apscheduler -> 3.11.2 clean.
- Server v0.4.0 booted with the new "embedded worker scheduler started (every 60 min, dry_run=False)" message.
- /health returned v0.4.0 + worker block populated + next_run 14:43:51.
- Auth matrix proven on both new endpoints (401/403/200).
- Dry-run tick completed -> tick_count=1, last_run populated.
- Mid-walk: noticed __pycache__/ untracked. Added to .gitignore via Add-Content. Line 94 confirmed by git check-ignore. Status dropped from 17 to 16 files.
- Real-run tick attempt 1: completed but pushed=False. Window A revealed "fatal: Unable to create '.git/index.lock': File exists." -- old Task Scheduler had raced our test (still enabled).
- Disabled Task Scheduler via Admin PowerShell (user mode denied). Removed lock file. Retry -> pushed=True, 14:35:09-14:35:12 (3 sec).
- MCSB Phase 1 published to GitHub for the first time (16 files in milestone commit).
- Final /worker/status: tick_count=3, last_run.git_pushed=true.

### Design decisions logged this session
- DEC-S5-01: APScheduler chosen over hand-rolled asyncio loop. Reason: scales cleanly when Phase 5 adds /briefing/today and Phase 6 adds theme-mining cadence; tiny dep; battle-tested.
- DEC-S5-02: First tick offset by WORKER_INTERVAL_MIN (no boot tick). Matches prior Task Scheduler behaviour and keeps the startup hook cheap.

### Lesson saved as feedback memory
- Scheduler handover rule: when moving a scheduled job from one driver to another, ALWAYS disable the old driver BEFORE the first real-run tick of the new one. The dry-run path won't catch this because it skips git add. (Saved as feedback_scheduler_handover.md in Cedric's auto-memory.)

### Files changed in vault this session
- cedric_server.py (v0.3.0 -> v0.4.0)
- cedric_worker.py (+ run_worker_pipeline shim, 16,451 bytes)
- CHANGELOG.md (v0.4.0 entry added at top, D25 format)
- .gitignore (+ __pycache__/ exclusion at line 94)
- PAIDA Master/04-Projects/2026.05.09 - MCSB/PROGRESS.md (Session 5 entry, 1.3g [x], header date/status)
- PAIDA Master/04-Projects/2026.05.09 - MCSB/2026.05.17-MCSB-Phase1-Session5-Pickup-Note.md (new)
- GitHub remote: first push of MCSB Phase 1 (16 files in milestone commit).

### Notion Content Studio
- New page: "2026.05.17 - Cedric Catches Phase 1 Crashing Lock-File Bug". Project: Meet Cedric. Format: Video. Status: Brain Dump. Hero arc + teachable rule + first-publish-to-GitHub bonus.

### Outstanding / next session
- Confirm autonomous tick fired (check tick_count > 3 with a trigger=scheduler entry in history).
- DELETE the disabled "Cedric Hourly Worker" Task Scheduler job via Admin PowerShell.
- Minor: surface git push failures as error_count++ rather than swallowing as pushed=False.
- Lifespan refactor (deprecated @app.on_event -> FastAPI 0.110+ lifespan context manager).
- Still deferred: Windows service install, token rotation before Cloudflare tunnel work.

### Resume phrase
"Cedric, I'm back. Session 6 -- let's confirm the autonomous tick fired since Session 5, then move to Phase 1.5 (MCP wrapper v0.1)."

---

## Session Log - 2026.05.17 Morning (MCSB Phase 1 Session 4 - 1.3d and 1.3e CLOSED)

### What we did
- Reviewed PROGRESS.md and the relevant PRD sections (Appendix B for the /agents/reload spec, sections 8.6 + 11.2 for agents.md and the hourly worker, section 20 for the phased plan).
- Built Cedric Server v0.3.0 (cedric_server.py 12,967 -> 22,017 bytes).
  - GET /agents/reload endpoint per PRD Appendix B, PC-token only (mobile token returns 403).
  - require_pc_token FastAPI dependency -- closes off 1.3e and provides a reusable PC-only auth tier for later /search_all and /briefing/today.
  - agents.md loader: parses frontmatter version, counts top-level rule blocks, hashes content for drift detection.
  - @app.on_event("startup") hook loads agents.md once on boot and writes a baseline snapshot.
  - Snapshot system: writes a versioned copy to agents.md-history/ on every content change, with filenames including seconds and a 6-char content hash so same-minute reloads do not collide. Auto-appends to agents.md-history/CHANGELOG.md (newest first).
  - Drift detection: when content changes but the frontmatter version does NOT, response sets content_drift: true and the CHANGELOG entry is tagged "(content drift -- version not bumped)".
  - /health enriched with an agents block (version, rules_loaded, loaded_at, snapshot_count).
- Sandbox tests: 18/18 paths green.
- Real bug caught by the sandbox: snapshot filenames using minute-level timestamps collided when two reloads happened in the same minute. Fixed by adding seconds + 6-char hash. Sandbox proved 6 rapid reloads now produce 6 unique files. This is the Meet Cedric Episode F hero arc.

### PROD walkthrough (10:48-11:05 London, on Mick's PC)
- Stumble at Step 2: unquoted vault path triggered PowerShell continuation prompt because of the apostrophe in "Mick's-Dex-2nd-Brain". Recovered with Ctrl+C + retry with the path in double quotes. New feedback memory saved so this never recurs.
- /health: confirmed v0.3.0, agents v1.0, 3 rules, baseline snapshot_count 1, both tokens configured.
- /agents/reload with PC token -> 200 + correct PRD-spec JSON, snapshot_written false (idempotent -- no content change since startup).
- /agents/reload with mobile token -> 403, detail "PC token required for this endpoint." 1.3e PROVEN in PROD.
- Cedric appended a 3-line test comment to agents.md (no version bump). Mick hit reload -> content_drift: true, snapshot_written: true, agents_version still 1.0. Two real snapshot files now in agents.md-history/. CHANGELOG auto-entry appeared at the top with the drift marker. Cedric reverted agents.md silently to its 1822-byte baseline.
- Server stopped cleanly with Ctrl+C and Y.

### Files changed in vault this session
- cedric_server.py (v0.2.0 -> v0.3.0)
- CHANGELOG.md (v0.3.0 entry added at top, D25 format)
- agents.md-history/CHANGELOG.md (2 new auto-entries: server-startup + manual-reload with drift marker)
- agents.md-history/agents-v1.0-2026.05.17T104843-c40c6f.md (baseline snapshot, retained as PROD evidence)
- agents.md-history/agents-v1.0-2026.05.17T105856-08a5a2.md (drift-edit snapshot, retained as PROD evidence)
- PAIDA Master/04-Projects/2026.05.09 - MCSB/PROGRESS.md (Session 4 entry, 1.3d [x], 1.3e [x], header date/status)
- PAIDA Master/04-Projects/2026.05.09 - MCSB/2026.05.17-MCSB-Phase1-Session4-Pickup-Note.md (new)

### Notion Content Studio
- New page: "2026.05.17 - Cedric Catches His Own Bug (1.3d Sandbox Save)". Project: Meet Cedric. Format: Video. Status: Brain Dump. Includes PROD success postscript and the apostrophe B-segment angle.

### Outstanding / next session
- Phase 1.3g: embed cedric_worker.py as a FastAPI background scheduler task inside the server (replaces the Windows Task Scheduler dependency). After 1.3g, the Cedric Server v0.1 series is fully complete.
- Then Phase 1.4 (agents.md framework finalisation), 1.5 (MCP wrapper v0.1), 1.6 (mobile sync), 1.7 (CLAUDE.md core + fragments + assembly script), 1.8 (private-content audit).
- Still deferred: Windows service install, token rotation before Cloudflare tunnel work.

### Resume phrase
"Cedric, I'm back. Let's continue Phase 1 -- ready for 1.3g (embed cedric_worker.py as a background scheduler task inside the server)."

---

## Session Log - 2026.05.13 Afternoon (MCSB PRD Review + v0.3 Production)

### MCSB PRD v0.3 approved. 46-page editorial review completed. Phase 1 ready.
**Session time:** ~16:00-17:30 BST (Wednesday afternoon, Cowork mode)
**Surfaces used:** Cowork, python-docx via bash sandbox

### What was done
- Picked up PRD v0.2.2_1 (Mick uploaded docx, 957 paragraphs)
- Worked through all 46 pages of Mick's markup in page-by-page passes
- Produced four intermediate versions: V0.2.2_2 (p.30), V0.2.2_3 (pp.31-36), V0.2.2_4 (pp.37-46)
- Key content changes: channel URLs added, website tier subfolders (Inner-Circle/Plaza, Free/Silver), Newsletters plural with subfolders, Events folder, Portico course, Case-Studies, CRM Address field, ax-trees global skills note, OQ6/7/12/14 resolved, D24-D25 added
- Produced PRD v0.3 (1,136 paragraphs): version bumped, Appendix A (folder schema ~80 lines) and Appendix B (API reference ~90 lines) written from scratch, Document History updated
- Phase 1 pickup note written: 2026.05.13-MCSB-Phase1-Pickup-Note.md
- Cedric memory (project_mcsb.md) updated to reflect Phase 1 ready status
- Two Meet Cedric episode brain dumps logged to Notion Content Studio
- Notion MCSB Build Tracker discussion begun; Option 3 agreed (Notion + PROGRESS.md)

### Decisions made this session
- D24: Notion bridge-not-migrate (Research DB, Companies Covered, Memory Vault stay in Notion)
- D25: Cedric Server CHANGELOG.md required
- OQ6 resolved: Backblaze B2 accepted
- OQ7 resolved: Obsidian Core Daily Notes; blank note deletion by hourly worker
- OQ12 resolved: agents.md-history/ + CHANGELOG.md
- OQ14 resolved: Notion permanent coexistence confirmed

### Outstanding / next session
- Create MCSB Build Tracker Notion database
- Create vault PROGRESS.md template
- Then: Phase 1 build (next separate session)

---

## Session Log - 2026.05.12 Evening (GitHub Backup Pipeline Diagnosis + Fix)

### Backup pipeline broken for 14 days. Diagnosed, fixed, push verified.
**Session time:** ~18:25-19:10 BST (Tuesday evening, Cowork mode)
**Trigger:** Mick asked "are the git commits actually being pushed to GitHub? Are our backups secure?"
**Answer (initially): NO - last commit was 28 April 2026, 14 days ago.**

### What was wrong
1. Stale `.git/index.lock` left over from a crashed git process c.28 April.
   Every subsequent `git add` since had been failing instantly with
   "Unable to create index.lock: File exists". The daily script silently
   bailed on this for two weeks.
2. Once Mick removed the lock, the pre-commit hook then correctly blocked
   the commit due to 21 .md files containing Unicode typographic chars
   (em dashes, smart quotes, ellipsis, box-drawing chars). Hook reads
   bytes not chars so its "Euro sign" / "Right double quote" labels are
   misleading - actual chars were U+2014 em dash, U+201C/D smart quotes,
   U+2013 en dash, U+2019 smart apostrophe, U+2500-251C box drawing.

### What was done
- Mick: removed `.git/index.lock` and `.git/objects/maintenance.lock`
- Cedric: wrote Python script to UTF-8-normalise 21 files in place
  (70 chars replaced total, verified clean afterwards)
- Mick: re-ran `python daily_git_commit.py` from vault root
- Result: commit cbf6b82 landed (100 files, 10,622 ins, 973 del)
  Push verified - local HEAD matches `ls-remote` HEAD on GitHub

### Outstanding (captured in pickup note)
1. **Problem 1b - root cause hunt**: how did Unicode typographic chars get
   past the "ASCII only" guardrails into 20 AI-research files and 1
   Poppy pickup note? Suspect: the skill/workflow producing AI Financial
   Analysis reports writes straight to disk without ASCII normalisation.
   Three hardening options documented.
2. **Problem 2 - ShareScope-Automation has no GitHub remote**: separate
   git repo at 04-Projects/2026.04.04-ShareScope-Automation/ has 2 local
   commits, 15 dirty files, NO remote configured. Not backed up anywhere.
   Decision needed from Mick.
3. **Problem 3 - verify Windows Scheduled Task still firing**: even though
   today's commit went through manually, the recurring task may have
   stopped firing. Check Task Scheduler history once Problem 1b is closed.
4. **Housekeeping**: small empty file `.cedric_write_test_2026_05_12.tmp`
   in vault root accidentally caught in tonight's commit (Cedric created
   it for a write-permissions test). `git rm` it tomorrow.
5. **Suggestion**: promote tonight's one-off fix script to a permanent
   vault tool at `tools/fix_typographic_chars.py`.

### Pickup note location
  C:\Vaults\Cowork\2026.05.12 - GitHub Backup Diagnosis - Pickup Note.md

### Lesson for Cedric (relevant to memory)
- ALWAYS investigate stale .git lockfile warnings rather than dismissing
  them as permissions quirks. In the first pass tonight Cedric saw the
  "unable to unlink index.lock" warning from his own `git fetch` and
  misread it as a Linux-mount artefact. It was actually the smoking gun.
  Test, Don't Trust - same principle as the dual-write rule.

---

## Session Log - 2026.05.10 Late-PM (YouTube Script v2 - Edits Applied)

### v2 drafted with 5 edits. All verified, change-highlighted DOCX delivered. Mick reviewing.
**Session time:** ~16:25-17:00 BST (Sunday late afternoon)
**Project:** YouTube content for diy-investors.com channel (@DIY-Investors)
**Status:** v2 complete. Mick has change-highlighted DOCX for second read-through.

**What we did:**
- Picked up cleanly from RESUMPTION-PICKUP-NOTE.md per "Path A" (verbal edits from Mick)
- Five edits requested: 1) COMEX inventory line in Section 4; 2-4) GUIA/INCRA/FUNAI acronym
  expansions in Section 5; 5) sanity check on copper guidance figure in Section 6
- Fact-checked the copper figure via web search across SIX independent sources
  (Coeur press release, MINING.com, SME Mining Engineering, Investing.com, Mugglehead,
  Resource World): 50-65 million pounds is correct. New Afton contributes all of it
  and is fundamentally a copper-gold mine, not a precious metals mine.
- Fact-checked the COMEX silver inventory claim: registered stocks below 100m oz, multi-source
  confirmed including ZeroHedge 1 May 2026. Edit on safe ground.
- Mick chose Option A on the copper clarifier: keep figure, add aside in [ASIDE] brackets
  noting New Afton is a copper-gold mine.
- v2-draft.md written via single Filesystem write (full overwrite, ASCII only)
- v2 DOCX built with v2 changes highlighted in YELLOW for easy comparison vs v1 read-through
- Validation hit a docx-js quirk: highlightCs element fails strict OOXML schema
  (Word opens fine but validator blocks). Fix: post-process the .docx zip, regex-strip
  all <w:highlightCs/> elements, repackage. PASS after fix.
- Final v2 DOCX delivered via /mnt/user-data/outputs/

**CRITICAL LESSON LEARNED THIS SESSION (Mick caught it):**
Cedric stated "copper is measured in pounds (a much smaller unit than ounces)" when
verifying the copper figure. THIS IS WRONG. There are 16 ounces in 1 pound, so a pound
is LARGER than an ounce, not smaller. Mick caught this immediately with "When I went to
School, there were 16oz to 1 pound - so ounces are smaller than pounds!"

The actual reasoning that justifies the figure: 50-65m lbs of copper IS large by weight
(~800m-1bn avoirdupois ounces equivalent), BUT this is correct because New Afton is a
copper-gold mine. By DOLLAR VALUE the mix is balanced: gold ~$3.6bn, silver ~$1.6bn,
copper ~$0.26bn at current prices. So copper is the SMALLEST revenue stream despite being
the largest by weight.

PATTERN TO REMEMBER: when cross-source verification confirms a figure, STOP THERE. Do
not add hand-wavy unit-conversion reasoning post-hoc. The cross-source check is the
verification, not the unit comparison. Adding spurious reasoning to "explain" a verified
figure is how unforced errors creep in.

**Files now on disk:**
- v1 markdown source (preserved): scripts/v1-draft.md
- v1 DOCX (Mick's name): scripts/2026.05.10 - Gold_SRB_n_CDE_YT-Script_v1-draft.docx
- v2 markdown source: scripts/v2-draft.md
- v2 DOCX (suggested filename): 2026.05.10 - Gold_SRB_n_CDE_YT-Script_v2-draft.docx

**Edits applied (all verified):**
1. Section 4: COMEX silver inventory line added after ETF buying point.
   Verified: registered stocks below 100m oz, multi-source confirmed.
2. Section 5: GUIA expanded to "Brazilian environmental installation licence"
3. Section 5: INCRA expanded to "National Institute for Colonisation and Agrarian Reform"
4. Section 5: FUNAI expanded to "National Foundation for Indigenous Peoples"
5. Section 6: copper figure (50-65m lbs) verified across 6 sources. KEPT.
   "New Afton is a copper-gold mine" clarifier added in [ASIDE] brackets per Mick's request.

**Word count v2:** 2,065 spoken words (~14.8 min at 140 wpm).
v1 was 2,004 -> v2 added ~60 words via acronym expansions and COMEX line.

**Validation:** ASCII PASS, voice-guard PASS, all 6 edit checks PASS, DOCX validator PASS
(after highlightCs strip).

**Patterns / lessons logged:**
- DOCX build with change-highlighting: docx-js TextRun supports `highlight: "yellow"`.
  But docx-js emits a non-standard <w:highlightCs/> alongside <w:highlight/> which
  fails strict OOXML schema validation. FIX: post-process the .docx zip, regex-strip
  all <w:highlightCs[^/]*/> elements, repackage. Word opens both versions fine; the
  strip is for validator compliance only.
- Verbal-edit pickup pattern (Path A from RESUMPTION-PICKUP-NOTE) worked well: read v1
  source, apply edits in memory, write v2 to scripts folder, regenerate DOCX with
  highlight-on-changes, present.
- When Mick queries a number that "feels wrong", do a real fact check (web search +
  cross-source) before answering. Don't rely on memory or hand-wave reasoning.
- "Side-note aside" device: use [ASIDE - text] brackets for camera cues that flag
  on-camera commentary distinct from stage directions in [square brackets]. Working
  pattern for this video; could be a voice-DNA addition if Mick uses it again.

**Outstanding (for next session):**
1. Mick reads through v2 DOCX, tracking the yellow-highlighted changes
2. Decision: ship as v1-final, or v3 with more edits
3. If shipping: lock title, regenerate clean DOCX without highlights, update Notion
   Micks Content Studio entry from "In Review" to "Ready"
   (entry id: 35cdb32a-9b0a-8127-b9e9-ed66cb9b2c33)
4. Charts handoff to editor (both JPGs originally at /mnt/user-data/uploads/, may need
   re-uploading or copying into the project folder for permanence)

**Notion update status:**
- Micks Content Studio entry already exists at "In Review" status from earlier today
  (id: 35cdb32a-9b0a-8127-b9e9-ed66cb9b2c33). Did NOT update this session - status
  still accurately reflects state (v2 produced, awaiting Mick's read-through).
- Will move to "Ready" when v2 (or v3) is signed off.

---

## Session Log - 2026.05.10 PM (YouTube Script v1 Drafted - SRB + CDE)

### Script v1 written, voice-DNA validated, DOCX delivered. Mick reviewing offline.
**Session time:** ~11:55-12:25 BST (Sunday afternoon, picked up after morning context refresh)
**Project:** YouTube content for diy-investors.com channel (@DIY-Investors)
**Status:** v1 complete. Mick has DOCX for printed read-through. v2 awaits his edits + title sign-off.
**Outcome:** v2 produced same day - see late-PM entry above.

**What we did:**
- Picked up cleanly from the morning pickup note in fresh context
- Read PICKUP-NOTE-for-fresh-context.md and voice-dna-mick.json end-to-end before drafting
- Sanity-checked the central-thesis numbers in Python: Q1 2026 vs 2025 actual gap is 52.2%
  ("roughly 50%" in the script stays honest); EDV gap is 61%; Q1 drawdown 26.8%
- Drafted v1 in one Filesystem write (full overwrite, ASCII only)
- Validated post-write: ASCII compliance PASS (no em dashes, smart quotes, ellipsis);
  voice-guard pass (no banned guru-speak); spoken word count 2,004 -> ~13-14 min at 140 wpm
- Flagged the length overrun to Mick (target was 8-12 min). Mick chose to keep the depth.
- Built print-friendly DOCX via docx-js + skill: A4, Arial 12pt, 1.5x line spacing,
  section dividers, blue sub-block labels, header + page-of-total-pages footer,
  appendix with title options + pre-record checklist
- Validated DOCX (90 paragraphs, all checks PASS)
- Delivered both files to /mnt/user-data/outputs/ for download
- Mick saved DOCX to vault scripts folder under his preferred filename convention

**Files now on disk:**
- Markdown source (Cedric's authoritative draft):
  C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\05-Areas\YouTube_System\diy-investors.com\YT-Longform\2026-05-10 - Gold Miners Q1 Realised Price Story (SRB+CDE)\scripts\v1-draft.md
- DOCX (Mick's read-through copy):
  C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\05-Areas\YouTube_System\diy-investors.com\YT-Longform\2026-05-10 - Gold Miners Q1 Realised Price Story (SRB+CDE)\scripts\2026.05.10 - Gold_SRB_n_CDE_YT-Script_v1-draft.docx

**Title options put to Mick (still awaiting choice as of late-PM):**
1. Gold's Pulled Back - But Miners Just Banked Record Q1 Prices. Two I'm Watching. (working)
2. Gold Hit $5,602 - But the Miners Are Still Cheap. Two I'm Watching.
3. Spot Gold Says Correction. Miner Earnings Say Re-rating. Two Stocks On My Radar.
4. The Q1 Gold Story Retail Is Missing - SRB and CDE.

**Lessons / patterns logged:**
- Filesystem MCP write_file is text-only -- binary DOCX must go via /mnt/user-data/outputs/
  with present_files. Always tell Mick to download and drop into the vault himself.
- str_replace is Claude-side only. For vault edits, always read full file -> modify in
  memory -> Filesystem:write_file with complete content. (Confirmed again, was already
  in Key Conventions.)
- DOCX skill at /mnt/skills/public/docx/SKILL.md works cleanly with docx-js. Print-friendly
  recipe to remember: A4, Arial 12pt, 1.5x spacing (line: 360), section divider rules
  (paragraph border-bottom), italic-grey stage directions, blue H2 for sub-blocks.
- Voice-DNA validation in Python after writing is now the standard QA step for any
  long-form Mick-voice content. ASCII check + word count + banned-phrase check.

**Notion update status (from PM session):**
- Micks Content Studio entry created during PM session shutdown.
- Entry id: 35cdb32a-9b0a-8127-b9e9-ed66cb9b2c33
- Status: "In Review"
- URL: https://www.notion.so/35cdb32a9b0a8127b9e9ed66cb9b2c33

---

## Session Log - 2026.05.10 AM (YouTube Video Brief: Gold Miners Q1 Realised Price - SRB + CDE)

### YouTube longform video brief built. Pickup note ready for fresh-context script drafting.
**Session time:** ~10:30-12:30 BST (Sunday morning)
**Project:** YouTube content for diy-investors.com channel (@DIY-Investors)
**Status:** Brief complete, voice DNA loaded, pickup note saved. Script draft NOT yet written
(picked up in afternoon session above).

**What we did:**
- Mick asked for two-phase research: trending YouTube investing topics + match against vault content
- Phase 1 vault research: read CEDRIC_MEMORY, YouTube_System config, voice DNA, ICP profile, channel YAML
- Phase 2 web research: ranked top 10 trending investing topics (gold/miner re-rating made the list)
- Confirmed last YouTube upload was Feb 2026 silver shortage; Sep 2025 video on AI miner research already proven on channel
- Mick chose: gold miners lagging the metal price, mixing UK + US listings
- Iterated structure: started with 4 stocks (SRB, EDV, CDE, WPM), Mick pivoted to 2-stock approach
- Final structure: SRB (UK, BUY 80.7% discount, with honest Coringa permit risk Jan 2027) + CDE (US/NYSE, room to run on 2026F multiples 8.9x P/E, 4.5x EV/EBITDA)

**Two charts uploaded by Mick (both saved at /mnt/user-data/uploads/):**
- 2026_04_08_-_GGP_-_Gold_n_Silver_Prices_Q1_2026-Estimated.jpg (Q1 monthly averages table)
- 2026_04_20_-_Gold_TradEcon__1yr_Chart_4805_1_USD_per_oz_JPG.jpg (1-year price arc)

**Central thesis identified:**
The Q1 2026 realised price disconnect. Spot gold "correcting" 10% from Jan ATH of $5,602, but
miners booking Q1 2026 sales received average ~$4,870/oz - roughly 50% higher than 2025 average
of ~$3,200/oz. EDV's Q1 confirmed it: realised $4,842 vs $3,000 guidance assumption. Q1 reports
landing now will show a re-rating retail hasn't priced in.

**Agreed video parameters:**
- Title direction: "Gold Hit $5,589 - But the Miners Are Still Cheap" (revised in PM session for 2-stock format)
- Two charts to feature in Section 1 as the visual hook
- Elliott Wave: GENERIC framing only ("corrective wave then continuation"), no specific count
- Inner Circle webinar coverage: soft mention, not hard CTA
- Charts attribution: "my research" without specifying source
- Tone: honest, down-to-earth, AI gets you to analysis quicker but you still own the call

**Voice DNA loaded fully (voice-dna-mick.json):**
- 12 patterns to deploy: personal attribution, humility markers, audience specificity (DIY-Investors capitalised),
  conversational transitions, softer technical language, hedging on predictions/conviction on principles,
  Cedric+Annie as named collaborators, British English throughout, data-first, temporal precision,
  self-aware concept references, full risk warning + DYOR signature

**Project folder created:**
C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\05-Areas\YouTube_System\diy-investors.com\YT-Longform\2026-05-10 - Gold Miners Q1 Realised Price Story (SRB+CDE)\
+ scripts/ subfolder

**Pickup note saved (CRITICAL for next session - now CONSUMED in PM session):**
2026-05-10 - Gold Miners Q1 Realised Price Story (SRB+CDE)\PICKUP-NOTE-for-fresh-context.md
Contains: full brief, both charts described, complete SRB + CDE financial data, script structure
section by section, voice DNA patterns, file writing requirements, frontmatter template.

**Mick's reason for context refresh:**
Context was filling up after extensive research and brief iteration. Smart move to clear before
the heaviest task (script writing). Pickup note designed so fresh Cedric has zero context loss.
PATTERN VALIDATED: PM session picked up cleanly with no information lost.

**Session intelligence to carry forward:**
- Channel ID UCaWdEBBHiV6P0i7X5fDCY0A (@DIY-Investors)
- Sister site diy-investors.ai active with Cedric/Nina AI content
- Notion Research Database ID: ac552ce5-2ceb-4ffb-a502-7d5da6c67cf8
- Notion Micks Content Studio DB ID: a1983c632eb84e15b365a6e3e310ff96
- SRB Notion: 353db32a-9b0a-8198-9801-cbb03e443ecf (Nina BUY 1 May 2026)
- CDE Notion: 34fdb32a-9b0a-8143-8cd0-e2e399711789 (Cedric Analysis 27 Apr 2026)
- EDV Notion: 351db32a-9b0a-8112-862e-cfe359ba4b6c (Nina 29 Apr 2026)
- 19 companies tracked in Research Log _index.md as of session

---

## Session Log - 2026.05.03 (ax-trees-automation: Sessions 6-7 - NotebookLM Bridge)

### notebooklm-bridge.js built and first live test passed. Two bugs found and fixed.
**Session time:** Sessions 6 and 7 -- 2026-05-03 afternoon
**Project:** ax-trees-automation
**Session logs:** C:\Vaults\Cowork\ax-trees-automation\session-logs\2026-05-03-session6.md
                 C:\Vaults\Cowork\ax-trees-automation\session-logs\2026-05-03-session7.md

**Session 6: notebooklm-bridge.js built**
- Decision 3 confirmed: do NOT rewrite Python NLM pipeline in JS -- bridge to it via child_process
- Python script: sharescope_nlm_researcher.py (handles Layers 2-5: notebook check/create,
  CSV upload, news search, Nina analysis, report save to vault)
- notebooklm-bridge.js written: spawns Python, streams output through Spinner, extracts JSON result
- Three supporting fixes: CSV filename suffixes, sharescope-search now returns companyName,
  sharescope-get-metrics passes companyName through to bridge
- Terminal Spinner class added (mirrors Python Spinner: rotating frames + alternating messages)
- notebookLM CLI: unofficial but working. Authenticate via: notebookLM login (once per session)
- Token stored at: C:\Users\pavey\.notebooklm\storage_state.json

**Session 7: Live test SQZ + bug fixes**
- First live test: pipeline ran end-to-end, report saved to vault. Two issues found.
- BUG 1 FIXED: extractJsonResult returned null (bridge reported success:false despite Python success)
  Root cause: Python prints Obsidian deep-link block AFTER JSON dict; stdout.slice(idx) included
  trailing ==== content, breaking JSON.parse. Fix: brace-depth counting to find matching }.
- ENHANCEMENT: flagNewsWarning() added. If IMPORT_RESEARCH fails (news search non-fatal timeout),
  bridge prepends Obsidian [!WARNING] callout to saved .md report so readers know news is absent.
- IMPORT_RESEARCH RPC: timed out 6x in first test (~4 min delay). Non-fatal. Google service issue.
  Monitor across runs. Not something we control in our code.

**JS file write rule (CRITICAL - confirmed again this session):**
  Edit tool ALWAYS truncates JS files at apostrophes in string literals.
  ALWAYS use bash heredoc: cat > filepath << 'ENDOFFILE' ... ENDOFFILE

**ax-trees-automation task status (as of 2026-05-03 Session 7):**
- [x] Layer 1: ShareScope data collection -- COMPLETE
- [T] Layers 2-5: notebooklm-bridge.js -- TESTED (retest needed to confirm extractJsonResult fix)
- [ ] Top-level orchestrator / run-research.bat -- NOT STARTED
- [ ] Portfolio-screenshots mini-project -- NOT STARTED
- [ ] Sharescope-stock-filter mini-project -- NOT STARTED

**Session 8 first task:**
  Run retest command (see SESSION8-PICKUP.md). If success:true confirmed, mark [x] COMPLETE.
  Then run full --run-layer1 end-to-end test.

**Mandatory reads at Session 8 start:**
  1. session-logs/SESSION8-PICKUP.md
  2. PIPELINE-PROGRESS.md
  3. skills/SKILLS-INDEX.md

---

## Session Log - 2026.05.03 (ax-trees-automation: Sessions 3-5 Complete, Layer 1 Done)

### ax-trees-automation Layer 1 (ShareScope Data Collection) FULLY COMPLETE
**Session time:** All-day sessions 3, 4, 5 -- 2026-05-03
**Project:** ax-trees-automation
**Session logs:** C:\Vaults\Cowork\ax-trees-automation\session-logs\2026-05-03-session5.md

**Session 3: AX tree master + project reorganisation**
- sharescope-ax-tree-master.md v1.2 created with all confirmed selectors
- Project folder structure cleaned up and standardised

**Session 4: Login/logout/screenshot skills**
- skills/sharescope-login.js -- [x] COMPLETE
- skills/sharescope-logout.js -- [x] COMPLETE (Options menu selector discovered and confirmed)
- skills/sharescope-screenshot.js -- [x] COMPLETE
- Logout discovery: must use #cogwheel-menu-main button[title="Options menu"] (not .first())

**Session 5: Search/export/metrics skills + live tests + infrastructure**
- .env restored to correct location C:\Users\pavey\.env (had been placed in project subfolder)
- .env protection rule added to THREE CLAUDE.md levels:
    C:\Users\pavey\.claude\CLAUDE.md (global -- Mick created in Cursor)
    C:\Vaults\Cowork\CLAUDE.md (vault level)
    C:\Vaults\Cowork\ax-trees-automation\CLAUDE.md (project level)
- skills/sharescope-search.js -- [x] COMPLETE
- skills/sharescope-export-financials.js -- [x] COMPLETE
- skills/sharescope-get-metrics.js -- [x] COMPLETE (orchestrator: login->search->export->logout)
- Live test GGP (Greatland Resources): PASS (selector bugs found and fixed)
- Live test SQZ (Serica Energy): PASS (clean run, all 6 tabs, logout confirmed)
- Auto-test policy added to CLAUDE.md: always test before reporting, never ask permission
- PIPELINE-PROGRESS.md created: master view of all 5 pipeline layers
- PROGRESS-TEMPLATE.md created: standard for all mini-projects
- PROGRESS.md standard locked: [ ] NOT STARTED | [~] WIP | [B] BUILT | [T] TESTED | [x] COMPLETE
- Dex vault mounted this session (request_cowork_directory): CEDRIC_MEMORY.md now writable directly
- Folder access rule added to CLAUDE.md (see Key Conventions below)

**ax-trees-automation task status (as of 2026-05-03 Session 5):**
- [x] Layer 1: ShareScope data collection -- COMPLETE (all 6 skills, both live tests)
- [ ] Layer 2: NotebookLM check/create -- SESSION 6 NEXT
- [ ] Layer 3: NotebookLM upload CSVs -- NOT STARTED
- [ ] Layer 4: NotebookLM run research -- NOT STARTED
- [ ] Layer 5: Research report format/return -- NOT STARTED

**Session 6 trigger:** "Cedric, please pick up the ax-trees-automation project for Session 6."
**First task Session 6:** Create mini-projects/notebooklm-check/ folder and PROGRESS.md.
  Key question: does NotebookLM have an API, or does it require browser automation?

**Mandatory reads at Session 6 start:**
  1. ax-trees-automation/CLAUDE.md
  2. PIPELINE-PROGRESS.md
  3. skills/SKILLS-INDEX.md
  4. sharescope/sharescope-ax-tree-master.md (v1.2)

**Key confirmed selectors (live-tested 2026-05-03):**
- Search results: #find-share-dlg-results > div.find-dlg-row > span.find-dlg-row-tidm
- Tab buttons: data-cmd attributes ONLY (role/name selectors are ambiguous)
- Forecasts tab: data-cmd="ShowBrokers" (NOT ShowForecasts -- different sub-toggle)
- Logout: #cogwheel-menu-main button[title="Options menu"] then #logout2

---

## Session Log - 2026.05.02 Evening (ax-trees-automation: Rebuild + PRD + Notion + Pickup)

### ax-trees-automation: folder rebuilt in Cowork vault. PRD v1.0 written. Session 3 ready.
**Session time:** ~19:00-20:30 BST
**Project:** ax-trees-automation

**Context:**
Mick asked to pick up the ax-trees-automation project. Previous session's files
(folder structure, session log) were found in a temporary session workspace, not
persisted to the Cowork vault. Full session transcript was recovered via session history.
All work was rebuilt cleanly this session.

**NOTE on 2026.05.01 Evening entry below:**
That entry records Tasks 2 and 3 as complete (PRD written, migration survey done, Python
pipeline discovered, SS-01 staged). Those outputs were written to a temporary workspace
and are not accessible in the Cowork vault. They may or may not exist in a session archive.
This session rebuilt Task 1 and wrote a fresh PRD (Task 2). Task 3 is still to be done.

**Completed this session:**
- Rebuilt full v7 folder structure into C:\Vaults\Cowork\ax-trees-automation\ (36 files, 23 dirs)
- Wrote PRD.md v1.0 (14 sections: purpose, platforms, skills architecture, mini-projects model,
  output standards, anti-bot approach, tech stack, full folder tree, plugin roadmap, migration plan)
- Updated Notion Meet Cedric / ShareScope hub (corrected SS-02, added SS-03 stub)
- Wrote full session log with Session 3 pickup instructions
- Updated CEDRIC_MEMORY.md (this update)

**ax-trees-automation current task status (as of 2026-05-02 Session 2 -- superseded by 2026-05-03 entry above):**
1. [x] Build v7 folder structure -- COMPLETE
2. [x] Write PRD.md -- COMPLETE (v1.1)
3. [x] Explore existing ShareScope project + plan migration -- COMPLETE (Session 3)
4. [x] Set up Meet Cedric / ShareScope series in Notion -- COMPLETE
5. [x] Layer 1: ShareScope skills built and tested -- COMPLETE (Sessions 4-5)

**See 2026-05-03 session log above for full Session 6 pickup details.**

**Key file locations (all in C:\Vaults\Cowork\ax-trees-automation\):**
- PRD.md -- full project requirements document
- CLAUDE.md -- global rules for all sessions
- skills/SKILLS-INDEX.md -- master skill catalogue
- mini-projects/MINI-PROJECTS-MASTER.md -- all project status
- session-logs/2026-05-01-session.md -- full session history + Session 3 pickup instructions

**Session 3 pickup:**
Say: "Cedric, pick up the ax-trees-automation project for Session 3."
Task 3: explore C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\
and plan the migration into ax-trees-automation.

**Notion series hub:** https://app.notion.com/p/353db32a9b0a81018396c00fb2378db4

---

## Critical Learning Requirement (Active)

**CODING GUIDANCE MANDATE (2026.04.04):**
Mick is a relative newbie to coding. For ALL coding-related tasks:
- Always provide step-by-step instructions with exact directory paths
- Always show exactly what to type in command prompts
- Always specify file locations and directory names
- Explain what each command does
- Provide clear "before you start" setup instructions
- This requirement remains active until Mick explicitly requests we change it after gaining experience

This applies to ALL .MD files, CLAUDE.MD, and CHANGELOG.md updates.

---

## Key Conventions (Never Forget)
- **Commands = PowerShell + baby steps (Mick is NOT a coder):** ALWAYS give terminal commands in PowerShell syntax (his default shell), never Command Prompt / cmd.exe. Use `cd "path"` (no `/d`), set variables with `$env:NAME = "value"` (not `set NAME=value`), and quote comma-separated arg values (e.g. `--only "a,b"`). Always double-quote vault paths (apostrophe in "Mick's-Dex-2nd-Brain" breaks unquoted). Feed steps ONE small copy-paste block at a time, wait for the result, then give the next; explain each step in plain English and assume NO shell/coding knowledge. (Added 2026.07.04 after a cmd-style `cd /d` command failed in his PowerShell window.)
- **Credentials single source (MANDATORY):** All LOCAL script/skill credentials, API keys and tokens live ONLY in C:\Users\pavey\.env. Never create another .env (no project-subfolder or vault copies), never hardcode secrets in any skill/script/doc/CLAUDE.md, read with load_dotenv(override=True), and FAIL clearly if a key is missing (never fall back to another location). Local contexts only - in claude.ai Web / Cowork sandbox there is no local disk, so secrets arrive via connectors. Full rule in the master C:\Users\pavey\.claude\CLAUDE.md (v1.3, 2026.07.02). (Added 2026.07.02 after a stale second .env caused silent login failures.)
- **Folder access:** If Cedric needs a folder not currently mounted (e.g. Dex vault, a project subfolder), use request_cowork_directory to prompt Mick for access BEFORE attempting any file operations. Never assume access -- always request it. This is the standard pattern for all sessions.
- YYYY.MM.DD prefix: ALL project folders, files, Notion titles, SOURCE titles in NotebookLM
- Notebook titles in NotebookLM: NO date prefix
- Index titles in NotebookLM: Index_Updated:YYYY.MM.DD - HH.MM (dots, no colons)
- ASCII only in vault file writes
- Transactions: month-scoped, non-strikethrough rows only
- No featured image on portfolio posts
- Real image dimensions always from WordPress media_details API
- Yr2 benchmark: always uses 1 Jan of CURRENT year as start point
- **Filesystem MCP write_file OVERWRITES -- never use for partial updates. Always read full file, modify in memory, write complete content back. (Learned 2026.04.29.)**
- **Filesystem MCP write_file is text-only -- binary deliverables (DOCX, PDF, PPTX, XLSX, images) MUST be staged via /mnt/user-data/outputs/ and shared with present_files. Confirmed 2026.05.10. (Note: there is no Claude-to-user binary-copy tool, so Cedric cannot place a binary file straight into the vault - Mick downloads and drops it in. Reconfirmed 2026.06.01.)**
- **AI report templates live at C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\06-Resources\AI_Report_Templates. Two report types so far: (1) Research_Brief/ - single-company portrait stock brief (DIY_Investors_Report_Template.docx); (2) Sector_Screen_Report/ - multi-company landscape sector screen / ranking, with a worked example (PM_Miners_Quarterly_Growth_Consolidated.docx) and a README documenting structure, house style and methodology. Each report type has its own README.md; the folder has a top-level README.md and CHANGELOG.md. Check here before building any new report so style stays consistent. (Added 2026.06.01.)**
- **DOCX font default: always Aptos 12pt for body text, headings scaled proportionally, unless Mick specifies otherwise. For wide tables, keep cell text at a size that fits the page rather than forcing 12pt (do not let columns wrap); small-print caveat notes may be one point smaller than body. This is also stored as a cross-project memory edit. (Locked 2026.06.01, superseding the earlier Arial 12pt print-DOCX recipe.)**
- **NEVER add hand-wavy unit-conversion or "common sense" reasoning to back up a verified figure.** Cross-source verification IS the verification. Adding spurious post-hoc reasoning is how unforced errors creep in. (Learned 2026.05.10 - the "pounds smaller than ounces" gaffe; Mick caught it. There are 16 oz in 1 lb, so a pound is LARGER than an ounce.)
- **DOCX with change-highlighting:** docx-js TextRun supports `highlight: "yellow"`, but emits a non-standard `<w:highlightCs/>` element that fails strict OOXML schema validation. After build, post-process the .docx zip to regex-strip all `<w:highlightCs[^/]*/>` elements before delivery. Word opens both versions fine; the strip is for validator compliance only.
- **Skill dual-write integrity (2026.06.03):** A full audit found the mirror /mnt/skills/user/ drifts from the vault and is not reliably populated per project. NEVER trust the mirror as authoritative; treat the vault as source of truth and verify (md5, normalised for CRLF) after any mirror write. When fixing a skill, confirm which of the three locations (Mirror, PRIMARY .claude/skills, DEX skills) is canonical FIRST - see PICKUP_NOTE_2026.06.03-Skill-Audit.md.

---

## London Time Protocol (MANDATORY)
Pointer only - not a separate definition. The greeting / London-time rule is
CANONICAL in the USER_EXTENSIONS "Time-Based Greeting v2.0" block of
Dex-MickP\CLAUDE.md, and mirrored for Claude Code in
C:\Users\pavey\.claude\_rules.md. Follow that rule; do not keep a third copy
here. (Slimmed 2026.07.23 to stop drift.)

---

## Mandatory Skill Deployment Protocol
EVERY skill MUST be deployed to BOTH locations. No exceptions.
- Vault master: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\<skill-name>\
- MCP mirror:   /mnt/skills/user/<skill-name>/
Verify both copies match after deployment.
/mnt/skills/user/ IS writable from bash_tool in Claude Desktop (confirmed).
In claude.ai Web: vault writes via Filesystem MCP work; /mnt/skills/user/ is read-only.
[2026.06.03 audit caveat: this protocol is the INTENT, but on-disk reality has drifted -
some skills' newest copy lives in PRIMARY (Mick's Vault\.claude\skills) not DEX, and the
mirror does not always retain skills across projects/resets. Reconcile when the audit resumes.]

---

## NOTE: Earlier session log entries (pre-2026.05.10) preserved in git history.
This memory file was streamlined on 2026.05.10 to keep recent sessions front-of-mind.
For older session details (NotebookLM skill suite, ShareScope build, Poppy planning, etc.),
see git log on this file or the per-project session-logs/ folders.

---

## STANDING RULE: ShareScope automation uses data-cmd (2026.07.25)
All ShareScope browser automation MUST drive the UI via ShareScope's stable
`data-cmd` command attributes (paired with a :visible filter to avoid hidden
responsive duplicates), NOT button text / role / position. If a needed control
is not yet mapped, map it first (dump page HTML, find data-cmd), add it to the
master reference, then use it. Master reference (keep it the single source of
truth): 04-Projects/2026.04.04-ShareScope-Automation/ShareScope-data-cmd-Reference.md
(financials-panel selectors: ShareScope-Export-Accessibility-Reference.md).

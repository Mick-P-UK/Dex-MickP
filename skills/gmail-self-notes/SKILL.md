---
name: gmail-self-notes
description: >-
  Scheduled and on-demand ingestion of the notes Mick emails to himself into his
  Obsidian vault inbox. Each self-sent email is decomposed into separate markdown
  notes: the body text (author Mick), any attachment converted to markdown (author
  MCSB when built with Cedric, else Mick), and any YouTube link captured as a
  resource note with the URL in YAML frontmatter. Use this skill whenever Mick asks
  to "sweep my Gmail notes", "pull my self-notes into the vault", "ingest last
  night's emails", "get my emailed thoughts into the second brain", "process my
  YouTube links", "run the gmail-self-notes sweep", or for the scheduled morning
  run. For a one-off "just download that attachment to a file" request use the
  cedric-note-fetcher skill instead; this skill is the vault-ingestion pipeline.
license: Proprietary - Mick Pavey / DIY Investors internal use.
---

# gmail-self-notes

## Purpose

Mick captures thoughts, documents and useful YouTube videos by emailing them to
himself (often addressed to Cedric). This skill sweeps those self-sent emails and
files them into the vault inbox as clean Obsidian markdown notes, so they become
part of the shared second brain. It runs as a scheduled morning task and on demand.

## What it produces (three note types)

Each email is decomposed into its parts. One email can create several notes.

1. Text note - the body text of the email.
   - author: Mick, type: note.
2. Attachment note - each attachment, converted to markdown.
   - author: MCSB if the document was built with Cedric (content mentions Cedric or
     PAIDA), otherwise Mick. type: attachment.
   - The original binary is kept in the inbox `attachments/` subfolder and linked.
   - A docx is NOT auto-generated; regenerate one on demand only (see below).
3. YouTube / resource note - each YouTube link.
   - author: Mick, type: youtube. The video URL goes in a `url:` frontmatter field,
     the channel in `channel:`, the video title is the note title, and Mick's
     annotation goes in the body. If he wrote an "add to NBLM" directive, set
     `action: add-to-nblm` and `nblm_topic:`. A `summary: pending` flag and a
     "## Summary (pending)" section are added for on-demand filling later.

Every note derived from the same email also carries a shared `xref:` datetime key
(YYYY.MM.DD-HH-mm-ss, from the Gmail sent time in London) and two-way `related:`
wikilinks to its sibling(s), so the body text and its attachment (or link) stay
connected - pick up either and the other is one click away.

## Prerequisites

- Gmail connector (search_threads, get_thread) - find emails, read body + attachment list.
- Google Drive connector (search_files, download_file_content) - download attachment bytes.
- Claude in Chrome MCP - to "Add to Drive" from the email (attachment path only).
- Vault filesystem access - to write into the inbox folder.
- pandoc - to convert docx/pdf attachments to markdown.
- web_fetch - to read the YouTube oEmbed title (no API key needed).

If a prerequisite is missing, say which and continue with the parts you can do
(text and YouTube notes need neither Chrome nor Drive).

## CONFIG (inbox path set; still verify the folder exists at runtime)

  INBOX_PATH = C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\00-Inbox   # confirmed by Mick
  ATTACH_SUBDIR = attachments
  YT_SUBDIR = YouTube-Queue   # youtube notes go in <INBOX_PATH>\YouTube-Queue to keep
        # the inbox root tidy; the Inbox Base still catches them via file.inFolder.
  PROCESSED_LOG = <INBOX_PATH>\.gmail-self-notes-processed.json
        # stores last_run (ISO) + the set of processed thread/artifact ids
  SEARCH_WINDOW = after:<last_run date>   # catch-up since last successful run;
        # fall back to newer_than:2d on the very first run. Never a fixed 24h.

Do NOT write notes if INBOX_PATH does not exist - stop and report, so nothing lands
in the wrong place.

## Procedure

### 1. Establish the run window
Verify current London time in code (BST vs GMT) so "overnight" is correct. For the
scheduled run use SEARCH_WINDOW; for a manual catch-up use the range Mick gives.

### 2. Find self-sent notes
Gmail search_threads, e.g.:
  from:me to:me -label:MCSB-Filed newer_than:1d
  Cedric -label:MCSB-Filed newer_than:1d
Always add  -label:MCSB-Filed  to the search: it is the second, independent dedupe
alongside the processed log (see the labelling step below).
Collect candidate threads. For each, read the processed log and SKIP any
gmail_thread already fully ingested (per-artifact keys below make this precise).

### 3. Read each email
get_thread FULL_CONTENT. Take `plaintextBody`, the `attachments` array
(filename + mimeType), the subject and the sent date.

### 4. Classify and build notes
For each email:

  a. Clean body = plaintextBody with the signature block stripped (the helper does
     this). Keep a copy for annotation use.

  b. YouTube links: run
       python scripts/extract_youtube.py --text <body.txt>
     For each returned video:
       - Title: take it from the email SUBJECT, which is always of the form
         Watch "<title>" on YouTube - strip the `Watch "` prefix and `" on YouTube`
         suffix. Do NOT use web_fetch on the oembed URL: self-sent URLs are not in
         the web_fetch provenance set and it will refuse. Channel is optional - read
         it from the video page via Claude in Chrome if wanted, else leave blank.
       - Write a note:
           python scripts/build_vault_note.py --inbox "<INBOX_PATH>\YouTube-Queue" \
             --title "<video title>" --type youtube --author Mick \
             --date "<email_date>" \
             --fm "url=<canonical>" --fm "channel=<author_name>" \
             --fm "gmail_thread=<threadId>" --fm "tags=[inbox, youtube]" \
             [--fm "action=add-to-nblm" --fm "nblm_topic=<topic>"] \
             --body-text "<annotation>" \
             --append "Source: <canonical>" --summary-pending
       - The annotation (body with URLs removed) carries Mick's note text.

  c. Attachments: for each attachment, fetch the bytes using the SAME pipeline as
     cedric-note-fetcher:
       - In Chrome, open  https://mail.google.com/mail/u/0/#all/<threadId>  and click
         "Add to Drive" for the attachment (wait for the loading splash; re-screenshot
         and click at the control's current position; confirm "Added to My Drive").
       - Drive search_files to find it, download_file_content to get base64.
       - Decode + validate:
           python scripts/decode_attachment.py --from-json <result.json> \
             --out "<INBOX_PATH>/attachments/<filename>"
         (Never hand-paste base64; if the result was auto-saved to a tool-result
         file, decode from that. Validate; retry on failure.)
       - Convert to markdown:
           pandoc "<INBOX_PATH>/attachments/<filename>" -t markdown -o <conv.md>
         (For PDFs use pandoc or the pdf skill; for images/spreadsheets, skip the
         markdown conversion and just keep the original, noting it in a stub note.)
       - Write the note (author auto-detected):
           python scripts/build_vault_note.py --inbox "<INBOX_PATH>" \
             --title "<document title>" --type attachment --detect-author \
             --date "<email_date>" --fm "gmail_thread=<threadId>" \
             --fm "attachment=<filename>" --fm "tags=[inbox, attachment]" \
             --md-file <conv.md>

  d. Body text note: create a text note from the clean body ONLY when the body is
     more than just a URL/annotation already captured in (b) and there is no
     attachment whose covering message it duplicates. Rule of thumb:
       - Pure text email  -> one text note.
       - Email with attachment -> one text note (the covering message) + attachment note(s).
       - Pure YouTube link email -> YouTube note only (annotation lives there).
     Command:
       python scripts/build_vault_note.py --inbox "<INBOX_PATH>" \
         --title "<subject>" --type note --author Mick --date "<email_date>" \
         --fm "gmail_thread=<threadId>" --fm "tags=[inbox, self-note]" \
         --body-file <body.txt>

  e. Cross-link siblings: after building ALL notes for this email, pass their file
     paths to the linker so each gets two-way `related:` wikilinks (and a "## Related"
     section). Skip if the email produced only one note.
       python scripts/link_siblings.py "<note1>" "<note2>" ["<note3>" ...]

  Always pass  --fm "xref=<YYYY.MM.DD-HH-mm-ss>"  and  --fm "email_date=<iso>"  to
  every build_vault_note.py call above, using the Gmail sent time converted to
  Europe/London. The xref is the shared "same email" key; link_siblings adds the
  clickable two-way links on top.

### 5. Record and report
- Append each produced artifact to PROCESSED_LOG keyed by gmail_thread with a list
  of artifact ids (video_id, attachment filename, or "body"). Use this to dedupe.
- Log creates to Mick's changelog per his global rules.
- Report: per email, which notes were written (paths), and flag anything skipped or
  needing attention (e.g. an attachment that would not validate).

## Author rule
- Text notes and YouTube notes: author Mick (his thoughts / his curation).
- Attachment notes: author MCSB when the document was built with Cedric (the helper
  detects "Cedric"/"PAIDA" in the content with --detect-author), otherwise Mick.
  MCSB = "Mick and Cedric Second Brain".

## Signature and ASCII
- Strip Mick's standard signature block ("With Best Wishes From..."/website lines).
- All vault files are ASCII only (smart quotes, dashes and ellipses are converted;
  other non-ASCII is dropped). The helper enforces this.

## Naming
- Filename: "YYYY.MM.DD - Title.md" (dots, date first), matching Mick's convention.
- Collisions get " (2)", " (3)" suffixes automatically.

## Docx on demand
Markdown is the canonical vault format. If Mick later asks for an attachment as a
Word document, rebuild it from the markdown note with the docx skill - do not
produce docx during the sweep.

## Dedupe and scheduling (catch-up on wake)
This skill writes to a LOCAL Obsidian vault and drives Chrome on Mick's machine, so
it only runs when the computer is on and the Claude Desktop app is open. It cannot
run while the machine is off. Design it to be timing-independent:

- Window = "since last successful run", NOT a fixed 24h. Store last_run in
  PROCESSED_LOG and search Gmail with  after:<last_run date>  (fall back to
  newer_than:2d on the very first run). However late it runs, it captures everything
  since it last succeeded - a machine off for days loses nothing.
- Idempotent via PROCESSED_LOG: re-running never re-creates an existing artifact, so
  overlapping windows and manual re-runs are safe.
- Schedule a daily run at ~06:45 London (cron "45 6 * * *", local time) as the
  nominal time. CONFIRMED behaviour: scheduled tasks run while the Claude Desktop app
  is open, and if the app was closed when the task was due it runs on next launch.
  That is the catch-up-on-wake mechanism; combined with the since-last-run window a
  single launch run clears any multi-day backlog. Mick can also trigger it any time
  by asking to "sweep my notes" just after switching on.
- Each scheduled run starts fresh with no memory of prior sessions, so the task
  prompt must be self-contained: tell it to run the gmail-self-notes skill, name the
  inbox path, and restate the since-last-run + idempotency rules.
- Attachments additionally need Chrome signed in to Gmail. If it is not, still ingest
  the text and YouTube notes and mark the attachments pending; a later run completes
  them (they stay unprocessed in PROCESSED_LOG until done).
- After ALL notes for an email are filed successfully, mark the source thread:
  apply the Gmail label "MCSB-Filed" (labelId Label_534, light grey) with label_thread,
  then archive it by removing the INBOX label with unlabel_thread (removes it from the
  inbox; it stays in All Mail and under MCSB-Filed). NEVER delete. Only label+archive
  AFTER the notes are written, so a failure never loses an unfiled email.
- The MCSB-Filed label is the visible confirmation AND a second dedupe: the search
  excludes -label:MCSB-Filed, so even if the processed log is lost nothing double-files.
- Do not mark emails read. Write the new last_run timestamp + processed ids to
  PROCESSED_LOG on successful completion (belt-and-braces with the label).

## Reliability
- Text and YouTube notes never need Chrome/Drive, so they always succeed; do them
  first. Attachments use the browser+Drive hop and are validated before filing.
- If Chrome is not signed in, still ingest text and YouTube notes and report the
  attachments as pending.

## Helpers
- scripts/extract_youtube.py   - parse YouTube URLs + NBLM directive from body text.
- scripts/build_vault_note.py  - write an Obsidian note (frontmatter, author, ASCII,
                                 signature strip, dated filename).
- scripts/decode_attachment.py - decode + validate a Drive base64 attachment.
- scripts/link_siblings.py     - inject two-way related wikilinks across an email's notes.

## Edge cases
- Multiple videos or attachments in one email: one note each; dedupe by id.
- No inbox folder / wrong path: stop and report (never dump elsewhere).
- oEmbed fails for a video (private/deleted): still write the note using the raw URL
  as the title and note that the title could not be fetched.

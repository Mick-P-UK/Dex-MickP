---
name: cedric-note-fetcher
description: >-
  Retrieves notes and their attachments that Mick has emailed to himself (usually
  addressed to Cedric) and saves the attachment as a real file in the outputs folder.
  Use this skill whenever Mick asks to "download the note I emailed myself", "grab
  last night's note", "get the attachment from my Gmail", "fetch the Cedric note",
  "download the note or notes I made", "pull the attachment off that email", or any
  request to turn a self-sent email attachment (docx, pdf, xlsx, pptx, image, etc.)
  into a downloaded file. Works around the fact that the Gmail connector can read
  emails but cannot download attachments: it saves the attachment to Google Drive via
  the browser, then pulls it down through the Google Drive connector. Always use this
  skill for self-emailed note attachments rather than doing it ad hoc.
license: Proprietary - Mick Pavey / DIY Investors internal use.
---

# Cedric Note Fetcher

## Purpose

Mick captures ideas late at night by emailing himself a note, often addressed to
"Cedric", frequently with a Word/PDF/Excel attachment. He does not want to touch
Gmail manually to get those attachments onto his machine.

The Gmail connector can search and read these emails but has NO tool to download an
attachment's bytes. This skill bridges that gap with a proven three-hop pipeline:

  Gmail (find the email) -> browser "Add to Drive" (save attachment to Drive)
  -> Google Drive connector (download the bytes) -> outputs folder.

## Prerequisites

- Gmail connector (search_threads, get_thread) - to find the note and see attachments.
- Claude in Chrome MCP - to open the message and click "Add to Drive".
  Mick must be signed in to Gmail in Chrome.
- Google Drive connector (search_files, download_file_content, read_file_content) -
  to pull the file down.

If any of these is missing, tell Mick which one and stop.

## When To Use

Trigger on requests like: "download the note(s) I emailed myself", "get last night's
Cedric note", "fetch the attachment from that email", "grab the note I made",
"pull the docx off my Gmail". If Mick only wants the text of the note (no attachment),
the Gmail body is enough - you do not need the Drive hop.

## Procedure

### Step 1 - Find the note(s)

Verify the current London time with code first (per Mick's time protocol) so any
"last night" / "this morning" window is correct (BST vs GMT).

Search Gmail with search_threads. Good default queries (widen or narrow as needed):

  Cedric after:YYYY/MM/DD before:YYYY/MM/DD
  Cedric has:attachment newer_than:3d
  from:me to:me has:attachment newer_than:2d

Notes are usually SENT and INBOX (Mick emails himself). If Mick gives a time window
(e.g. "between 10.30pm and midnight"), use it to pick the right thread(s). If more
than one candidate matches and it is ambiguous, list the subjects and ask which.

### Step 2 - Confirm the attachment

For each chosen thread, call get_thread with messageFormat FULL_CONTENT. Read the
`attachments` array: note each `filename` and `mimeType`. If there is no attachment,
tell Mick the note is text-only and give him the body - stop here.

### Step 3 - Save the attachment to Drive (browser)

Load the Chrome tools (ToolSearch: tabs_context_mcp, navigate, computer, find), then:

1. tabs_context_mcp with createIfEmpty true.
2. navigate to:  https://mail.google.com/mail/u/0/#all/<threadId>
3. Gmail often shows a loading splash first. Wait ~3s, screenshot, and retry the
   screenshot if the renderer is briefly busy.
4. Locate the attachment card near the bottom of the email. Hover over it if the
   "Add to Drive" control is not already visible, then click "Add to Drive".
   (The layout can reflow after load - re-screenshot and click the control at its
   CURRENT coordinates rather than trusting an earlier position.)
5. Confirm the toast reads "Added to My Drive". If there are several attachments,
   add each one.

"Add to Drive" is a benign, reversible action (it copies into Mick's own Drive) and
is the whole point of this skill, so it does not need separate permission. Do NOT
click any web links inside the email body.

### Step 4 - Download the bytes (Drive connector)

1. Drive search_files to locate the just-added file, e.g.:
     title contains '<name-without-extension>' and mimeType = '<the mimeType>'
   Sort/scan for the most recent createdTime that matches. Grab its `id`.
2. Call download_file_content with that fileId. The bytes come back base64 in the
   `.content` field.
3. Decode RELIABLY (see the reliability rules below), writing the real binary to the
   outputs folder under the original filename.

### Step 5 - Validate, deliver, log

- Validate the decoded file (the helper does this): Office files (docx/xlsx/pptx)
  must open as a valid zip; PDFs must start with %PDF; images must have the right
  magic bytes. If validation FAILS, do not ship it - see reliability rules.
- Move the final file(s) to the outputs folder and present them with present_files.
- Give Mick a one-line summary (filename, source email, date). Add a "Sources" link
  to the Gmail thread and the Drive file.
- Log the fetch to the changelog per Mick's global rules.

## Reliability Rules (the one fragile step)

The base64 -> binary decode is the only place this can go wrong. Follow these:

- NEVER hand-type or paste the base64 into a bash heredoc. Transcribing thousands of
  characters by hand corrupts the file (this has bitten us before).
- Preferred: if the download_file_content result was large enough to be auto-saved to
  a tool-results file, read THAT file directly in bash, extract `.content` with jq,
  and pipe through `base64 -d`. No transcription, fully reliable.
- If the result came back inline, write the exact `.content` string to a single
  file with the Write tool in ONE operation (do not stream it through bash), then run
  the helper script to decode and validate.
- ALWAYS validate after decoding. If validation fails, re-download once and retry.
- Fallback for TEXT-BASED documents only (docx): if the binary keeps failing
  validation, use Drive read_file_content to pull the clean text and rebuild a fresh,
  valid .docx with the docx skill. Tell Mick it is a faithful rebuild, not the exact
  original bytes. Do NOT use this fallback for PDFs/images (fidelity is lost).

## Decoding With The Helper

`scripts/decode_attachment.py` does the decode + validation:

  # from a tool-results JSON file that contains {"content": "<base64>", ...}
  python scripts/decode_attachment.py --from-json /path/to/tool-result.txt --out "/outputs/<filename>"

  # from a raw base64 text file you wrote with the Write tool
  python scripts/decode_attachment.py --from-b64 /path/to/attach.b64 --out "/outputs/<filename>"

It exits non-zero and prints FAIL if the decoded file does not validate for its
extension, so you can branch on the result.

## Conventions (Mick's house rules)

- UK English throughout (organise, colour, behaviour).
- ASCII only in any vault/text files this skill writes - no smart quotes, em dashes,
  or ellipses.
- Keep the original attachment filename unless Mick asks otherwise.
- Do not delete the Drive copy afterwards (deletion is out of scope; leave it).

## Edge Cases

- No attachment: hand over the note body text; skip the Drive hop.
- Multiple notes / multiple attachments: process each; present them together.
- Chrome not signed in or extension not connected: say so and stop.
- File not found in Drive after "Added to My Drive": re-search with a looser title
  match and a recent createdTime filter before giving up.

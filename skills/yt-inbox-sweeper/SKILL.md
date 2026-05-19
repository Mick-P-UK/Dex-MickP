---
name: yt-inbox-sweeper
description: Sweeps Mick's Gmail for self-sent emails containing YouTube links, extracts the URL plus his hint phrase, enriches with video metadata and Cedric's commentary, appends a row to the YouTube Queue Google Sheet, and archives the email with a YT-Processed label. Use this skill whenever Mick asks to "run the YT sweep", "process my YouTube self-emails", "clear my inbox of YouTube links", or any request to triage YouTube links he has emailed to himself. Also runs daily on a schedule at 06:30 London time.
---

# YouTube Inbox Sweeper

## Purpose
Mick has a habit of forwarding interesting YouTube videos to his own email address (mickp.dbox@gmail.com) with a short hint phrase indicating his thinking - e.g. "Cowork for diy?", "For webinar?", "SMALL BUSINESS", "Explore using linear for project management". This skill triages those self-emails into a structured Google Sheet so the inbox stays clean and the links remain searchable.

## Output destination
- Google Sheet: "YouTube Queue - Email Sweep"
  - Sheet ID: 1bXirFpcyp8XDoYMB5LcNxQm0ztJoRb6lheHln1md-Fo
  - URL: https://docs.google.com/spreadsheets/d/1bXirFpcyp8XDoYMB5LcNxQm0ztJoRb6lheHln1md-Fo
- Containing folder: "email-sweep-results"
  - Folder ID: 1UVxW-I22TgpEydgw-mLT68N648ib5Xog
- Parent folder: "0 - AI - Cowork" (1mfb82toinDXfo1ZjKTaEBPUh83dTmRE3)

## Sheet schema (columns A to K)
1. Date Sent (YYYY-MM-DD HH:MM, London time)
2. URL (clean YouTube URL, no tracking parameters)
3. Video Title (from YouTube metadata)
4. Channel (from YouTube metadata)
5. Duration (HH:MM:SS)
6. Your Tag (Mick's hint phrase, normalised - first line of email body or subject)
7. Cedric's Take (one or two sentences on likely relevance, based on tag + title + channel)
8. Status (one of: New, Reviewed, Actioned, Archived)
9. Watched? (Yes / No / Partial - left blank by skill, Mick fills in)
10. Your Notes (free text - left blank by skill, Mick fills in)
11. Source Email ID (Gmail message ID for traceability)

## Workflow

### Step 1: Search Gmail
Run the following Gmail searches in parallel:
- `from:me to:me has:link youtube.com after:[YYYY/MM/DD]` where the date is the last successful run date (or 7 days ago on first run)
- Also include: `from:mickp.dbox@gmail.com to:mickp.dbox@gmail.com (youtube.com OR youtu.be) after:[YYYY/MM/DD]`

Exclude any thread already carrying the label "YT-Processed" or "YT-Skip".

Max 50 threads per run.

### Step 2: Extract per thread
For each matching email:
- Get the full message body (FULL_CONTENT)
- Extract YouTube URL(s) using regex matching both `youtube.com/watch?v=` and `youtu.be/` forms; strip query parameters except `v` and `t`
- Identify Mick's hint phrase: use the email subject line if it is custom (not just "Watch..." from YouTube share); otherwise look at the first non-URL line of the plaintext body. Common patterns include short questions ("Cowork for diy?"), tags in caps ("SMALL BUSINESS"), or short directive phrases ("Explore using linear for project management"). If none found, leave Your Tag blank.
- Capture the message ID and the sent date

### Step 3: Enrich with YouTube metadata
For each URL:
- Fetch the YouTube page (web_fetch) and extract title, channel, duration from the page metadata
- If fetch fails, record "Unknown" for missing fields and proceed - never block the whole sweep on one bad URL

### Step 4: Generate Cedric's Take
For each row, write a one or two sentence note that:
- Connects Mick's hint phrase to the video title/channel
- Flags potential relevance to known projects: AI-4-Inv webinar, DIY Investors site, Cowork demos, Claude Code workflows, portfolio research, MCP/connector building, plugin development
- Notes if the content looks evergreen vs. time-sensitive
- Is honest if the connection is unclear ("No obvious link to current projects - watch and decide")

Use UK English. ASCII only - no em dashes, smart quotes, or ellipsis.

### Step 5: Append to Google Sheet
- Use the Drive/Sheets MCP to append one row per video to the sheet
- Status column defaults to "New"
- Watched? and Your Notes left blank

### Step 6: Label and archive in Gmail
- Apply Gmail label "YT-Processed" to each processed thread (create the label if it does not exist)
- Remove the INBOX label (archive the message)
- Do NOT delete

### Step 7: Report back
Produce a concise summary:
- Number of emails processed
- Number of unique URLs added
- Any URLs that failed enrichment
- Direct link to the sheet for review

## Safety nets
- If Mick labels a thread "YT-Skip" before the sweep runs, ignore it entirely (do not process, do not archive)
- If a URL is already present in the sheet (dedup on URL column), skip it but still archive the email
- If the sweep finds zero new emails, report that and exit cleanly

## Schedule
Runs daily at 06:30 London time via scheduled task "yt-inbox-sweeper-daily" - completes before the 06:45 morning briefing so the YouTube inbox is triaged before the briefing fires.

## Manual invocation
Triggers include:
- "run the YT sweep"
- "process my YouTube self-emails"  
- "clear the YouTube backlog"
- "sweep my inbox for YouTube"
- Any request mentioning YouTube links in self-emails

## Future extensions (not yet implemented)
- Expand scope to non-YouTube links (articles, RNS, Substack)
- Auto-tag against a controlled vocabulary (Project / Watch Later / Reference / Pass-along)
- Generate a weekly digest of unwatched items
- Cross-reference against the AI4Inv webinar planning notes

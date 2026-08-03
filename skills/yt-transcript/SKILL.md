---
name: yt-transcript
description: >
  Fetches the transcript of a YouTube video and files it in the vault as a note that
  follows Mick's Obsidian "Source Template" (Summary / Key Takeaways / Notes/Transcript),
  with Cedric writing the Summary and Key Takeaways from the transcript. Use this skill
  whenever Mick says "get the transcript of [video]", "transcribe this YouTube video",
  "grab the transcript", "make a transcript note", "process my YouTube inbox", "transcribe
  the videos I emailed myself", or pastes a YouTube link and asks for a transcript /
  summary / key takeaways. Mick emails himself YouTube links most days, so this is a
  near-daily tool. Works from a URL/ID or by scanning the 00-Inbox self-notes.
---

# yt-transcript

Turns a YouTube video into a clean, ASCII, Source-Template note in the vault. Built
2026.08.02 with Mick after doing three of these by hand (Nick Milo, Wanderloots, Artem
Zhutov) proved the workflow.

## What it produces

A note in `06-Resources/Transcripts` named
`YYYY.MM.DD - Transcript - <Author> - <Title>.md`, matching the Source Template exactly:

```
---
date_created: YYYY.MM.DD
Category:
tags: [YT]
Reference Link: <youtube url>
Channel: <youtube channel - auto>
By: <author/presenter - Cedric fills>
status:
---
## Summary

<Cedric writes this from the transcript>

## Key Takeaways

<Cedric writes this from the transcript>

## Notes/Transcript

<one provenance line, then the cleaned transcript>
```

- `tags: [YT]` is added automatically (Mick's convention for YouTube sources).
- `Reference Link` = the video URL.
- `Channel` and `By` are DELIBERATELY separate fields. `Channel` is the YouTube channel,
  auto-filled from oembed (reliable, always present). `By` is the PERSON who presents -
  which may equal the channel (Artem Zhutov), be a sub-brand of it (channel Wanderloots ->
  By Callum), be one of several contributors on a large channel, or be unknown. The script
  auto-fills `Channel` and leaves `By` blank; Cedric fills `By` with the person's name (a
  YAML list if several, left blank if genuinely not identifiable - never guessed).
- Transcript is cleaned to plain ASCII (smart quotes/dashes/ellipsis mapped, [music] and
  ">>" caption markers stripped, timestamps removed) and broken into paragraphs.

## FIRST: work out which runtime you are in

The engine fetches captions over the network and writes into the Windows vault. Neither of
those is possible in every runtime, so establish where you are BEFORE reaching for the
script. Verified 2026.08.02: YouTube returns `IpBlocked` for caption requests from
datacentre IPs, and the Cowork device bridge (`device_bash`) has no network access at all.
The fetch only succeeds from Mick's own home IP.

| Runtime | How to tell | Path to use |
|---------|-------------|-------------|
| A - Claude Code on the PC, or Cowork running "On your computer" | A shell can see `C:\Vaults` directly | Path A (script) - full function |
| B - Cowork in the cloud | Vault reachable only via Filesystem MCP or the device bridge; `mcp__claude-in-chrome__*` available | Path B (browser capture) |
| C - claude.ai web | No vault, no shell | Path C (deliver the note as a file) |

Do NOT run the script in Runtime B or C. It will fail on `IpBlocked` and waste a cycle.

In all three paths the division of labour is the same: the MECHANICAL part is fetch + clean
+ lay out the note; the JUDGEMENT part is Cedric writing the Summary and Key Takeaways and
filling `By`. Never leave the placeholders in a finished note, and keep everything ASCII.

## Path A - script (Runtime A only)

1. Run the engine:

   ```
   VAULT="C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP"
   # one or more links / 11-char ids:
   python "$VAULT/skills/yt-transcript/scripts/yt_transcript.py" --url "https://youtu.be/VIDEOID"
   # or process the freshly-emailed self-notes in the inbox root:
   python "$VAULT/skills/yt-transcript/scripts/yt_transcript.py" --scan-inbox
   ```

2. For EACH note the script writes: open it, read the `## Notes/Transcript` section, and
   replace the two `_pending - Cedric to write from the transcript_` placeholders with:
   - `## Summary` - a tight paragraph (what the video is and its through-line).
   - `## Key Takeaways` - a scannable bullet list of the concrete, reusable points.
3. Fill `By:` with the human author/presenter (the script leaves it blank and fills
   `Channel` instead). E.g. for the "Linking Your Thinking with Nick Milo" channel, set
   `By: Nick Milo`; for the "Wanderloots" channel, `By: Callum`. Use a YAML list if there
   are several presenters, and leave `By` blank rather than guessing if it is not clear.
   The filename uses the author when known - rename it to match if you set `By`.
4. Keep everything ASCII (vault rule). The script guarantees the transcript is ASCII; your
   Summary/Key Takeaways must be too - straight quotes, hyphens, no ellipsis glyph.
5. Report to Mick with clickable links to the finished notes.

## Path B - browser capture (Cowork in the cloud)

The script cannot fetch here, but Mick's own browser can. Use Claude in Chrome, which runs
on his machine and therefore his IP.

1. Invoke the `claude-in-chrome` skill first, then load the browser tools with ONE
   ToolSearch call (`tabs_context_mcp`, `tabs_create_mcp`, `navigate`, `computer`,
   `get_page_text`).
2. Open the video, expand the description, click "Show transcript", and pull the transcript
   panel text with `get_page_text`.
3. Get `Channel` and `Title` from oembed - that endpoint is NOT IP-blocked and works fine
   from the cloud container:
   `https://www.youtube.com/oembed?url=<video url>&format=json`
4. Clean the captured text to the same standard the script applies: map smart quotes,
   dashes and ellipsis to ASCII, drop any remaining non-ASCII, strip `[music]`-style markers
   and `>>` speaker arrows, remove timestamps, and re-paragraph it.
   Reuse the `REPL` / `ascii_only` logic in `scripts/yt_transcript.py` - do not reinvent it.
5. Check `06-Resources/Transcripts` for the video id before writing (same dedupe rule as
   the script - the id sits in the provenance line of every note).
6. Write the note into the vault with the Filesystem MCP (`Filesystem__write_file`) at
   `06-Resources/Transcripts/YYYY.MM.DD - Transcript - <Author> - <Title>.md`, in the exact
   Source Template shape shown above, with the Summary and Key Takeaways written in.

## Path C - deliver as a file (claude.ai web)

No vault and no network here. Do not pretend otherwise - say so in one line rather than
failing silently.

1. Ask Mick to paste the transcript (YouTube's "Show transcript" panel, or the Obsidian Web
   Clipper YouTube template) along with the video URL.
2. Clean it to ASCII by the same rules, build the full Source Template note including the
   Summary and Key Takeaways, and set `Channel` and `By` from what Mick supplies.
3. Deliver it as a `.md` file named
   `YYYY.MM.DD - Transcript - <Author> - <Title>.md` for Mick to drop into
   `06-Resources/Transcripts`. Do not paste a long transcript into the chat body.

## Modes and flags

- `--url URL [URL ...]` - one or more YouTube links or 11-char ids.
- `--scan-inbox` - scan the `00-Inbox` ROOT for YouTube self-notes (this is where the
  gmail-self-notes sweep files fresh links) and process any not already transcribed.
- `--include-queue` - with `--scan-inbox`, also sweep the `00-Inbox/YouTube-Queue` backlog
  (recursive). WARNING: that backlog is large (200+ videos as of 2026.08.02) - only use
  this deliberately, and prefer `--dry-run` first.
- `--dry-run` - list what would be processed, with dedupe status, and write nothing. Always
  worth running before a `--scan-inbox --include-queue`.
- `--force` - re-transcribe even if a note for that video id already exists.
- `--out-dir DIR` / `--root DIR` - override the output folder / vault root.

## Dedupe

Before writing, the script checks `06-Resources/Transcripts` for the video id (it appears
in the provenance line of every note). If found, it skips - so re-running `--scan-inbox` is
safe and idempotent.

## Dependency

`youtube-transcript-api` (pip, no API key). Installed permanently on Mick's PC 2026.08.02.
If a fresh machine is missing it: `python -m pip install youtube-transcript-api`.

## Gotchas

- Only works on videos that have captions (auto or manual). No captions -> the script
  reports the failure and moves on.
- oembed returns the CHANNEL name as author; for `By` Cedric should use the person's name.
- YouTube can rate-limit caption fetches from some networks (this hit Mick's tablet, not
  his PC). If it fails on the PC, retry, or fall back to the Obsidian Web Clipper YouTube
  template (open "Show transcript" first).
- `IpBlocked` is NOT a transient error to retry - it means the runtime is not on Mick's home
  IP. Stop and switch to Path B or Path C. Verified 2026.08.02 from a Cowork cloud container.
- The oembed lookup for Channel/Title works from anywhere; only the CAPTION fetch is blocked.
  So even in Path B and C the metadata half can still be automated.
- The script is written in pure ASCII on purpose so it can never introduce non-ASCII into
  the vault it writes to.

## Provenance

- Created: 2026.08.02 (Claude Code, Windows), built with Mick.
- Author: Cedric (PAIDA).
- Engine: scripts/yt_transcript.py (modes: --url, --scan-inbox; dedupe; --dry-run).
- Output: 06-Resources/Transcripts, Source-Template format.
- v1.1, 2026.08.02 (Cowork session): added the runtime table and Paths A/B/C after testing
  the engine from a cloud container and getting `IpBlocked` from YouTube. Packaged as a
  .skill bundle for account-level install so the skill is available in claude.ai web and
  Cowork as well as Claude Code. Lives-In codes now V + A (account skill).

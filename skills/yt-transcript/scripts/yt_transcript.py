#!/usr/bin/env python3
"""
yt_transcript.py - fetch a YouTube transcript and write it into a vault note that
follows Mick's Obsidian "Source Template" (Summary / Key Takeaways / Notes/Transcript).

The script does the MECHANICAL part only: fetch the captions, clean them to plain
ASCII, paragraph them, and write a note with the Summary and Key Takeaways left as
placeholders. Cedric (the agent running the skill) then reads the transcript and
writes the Summary and Key Takeaways in - that part needs a language model, not code.

Modes:
  --url URL [URL ...]   one or more YouTube links or 11-char video ids
  --scan-inbox          scan 00-Inbox for YouTube self-notes not yet transcribed

Notes are written to 06-Resources/Transcripts by default (--out-dir to override).
Requires: youtube-transcript-api (pip install youtube-transcript-api). No API key.

Written in pure ASCII on purpose (vault rule): any special char is a code point.
"""
import sys, os, re, glob, argparse, urllib.request, json
from datetime import datetime

TRANSCRIPTS_REL = os.path.join("06-Resources", "Transcripts")
INBOX_REL = "00-Inbox"

# smart-punctuation -> ASCII; anything else non-ASCII is dropped
REPL = {0x2018:"'",0x2019:"'",0x201A:"'",0x201B:"'",0x201C:'"',0x201D:'"',0x201E:'"',
        0x2013:"-",0x2014:"-",0x2015:"-",0x2012:"-",0x2010:"-",0x2011:"-",0x2212:"-",
        0x2026:"...",0x00A0:" ",0x2022:"-",0x00B7:"-"}

def ascii_only(s):
    return "".join(REPL.get(ord(c), c if ord(c) < 128 else "") for c in s)

def find_root(override):
    if override:
        return override
    here = os.path.abspath(os.path.dirname(__file__))
    while True:
        if os.path.exists(os.path.join(here, "CEDRIC_MEMORY.md")):
            return here
        parent = os.path.dirname(here)
        if parent == here:
            break
        here = parent
    # fallback to the known Windows path
    cand = r"C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP"
    return cand if os.path.isdir(cand) else None

def parse_video_id(s):
    s = s.strip()
    m = re.search(r"(?:v=|youtu\.be/|/shorts/|/embed/|/live/)([A-Za-z0-9_-]{11})", s)
    if m:
        return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", s):
        return s
    return None

def oembed(vid):
    title = author = None
    try:
        u = "https://www.youtube.com/oembed?url=https://youtu.be/%s&format=json" % vid
        with urllib.request.urlopen(u, timeout=25) as r:
            meta = json.load(r)
        title = meta.get("title"); author = meta.get("author_name")
    except Exception as e:
        print("  oembed failed for %s: %r" % (vid, e))
    return title, author

def get_segments(vid):
    from youtube_transcript_api import YouTubeTranscriptApi
    langs = ["en", "en-GB", "en-US"]
    try:
        api = YouTubeTranscriptApi()
        if hasattr(api, "fetch"):
            fetched = api.fetch(vid, languages=langs)
            return [s.text for s in fetched]
    except Exception as e:
        print("  (new-API note: %r)" % e)
    return [d["text"] for d in YouTubeTranscriptApi.get_transcript(vid, languages=langs)]

def clean_and_paragraph(texts):
    t = " ".join(x.replace("\n", " ") for x in texts)
    t = re.sub(r"\[(?:music|applause|laughter|inaudible|silence)\]", " ", t, flags=re.I)
    t = re.sub(r"(?:\s*>>\s*)+", " ", t)
    t = ascii_only(t)
    t = re.sub(r"\s+", " ", t).strip()
    sentences = re.split(r"(?<=[.!?])\s+", t)
    paras, buf = [], []
    for s in sentences:
        buf.append(s)
        if len(buf) >= 5:
            paras.append(" ".join(buf)); buf = []
    if buf:
        paras.append(" ".join(buf))
    return "\n\n".join(paras), len(t.split())

def sanitize_filename(s):
    s = ascii_only(s)
    s = re.sub(r'[\\/:*?"<>|]', "", s)      # illegal on Windows / Obsidian
    s = re.sub(r"\s+", " ", s).strip()
    return s[:90].rstrip(" .")

def already_done(out_dir, vid):
    if not os.path.isdir(out_dir):
        return False
    for fp in glob.glob(os.path.join(out_dir, "*.md")):
        try:
            if vid in open(fp, encoding="utf-8").read():
                return True
        except Exception:
            pass
    return False

def build_note(vid, url, title, channel, body, wc, date_str, source_note):
    channel = ascii_only(channel or "")
    title = ascii_only(title or vid)
    rel = ""
    if source_note:
        rel = " Related: [[%s]]" % ascii_only(source_note)
    prov = ("_Transcript of %s | channel: %s | video id: %s | approx %d words | "
            "captured %s, auto-captions cleaned to plain text, timestamps removed.%s_"
            % (url, channel or "unknown", vid, wc, date_str, rel))
    lines = []
    lines.append("---")
    lines.append("date_created: %s" % date_str)
    lines.append("Category:")
    lines.append("tags: [YT]")
    lines.append("Reference Link: %s" % url)
    lines.append("Channel: %s" % channel)   # auto from oembed - the YouTube channel
    lines.append("By:")                      # the PERSON/author - Cedric fills (may differ
                                             # from channel, may be a list, may stay blank)
    lines.append("status:")
    lines.append("---")
    lines.append("## Summary")
    lines.append("")
    lines.append("_pending - Cedric to write from the transcript_")
    lines.append("")
    lines.append("## Key Takeaways")
    lines.append("")
    lines.append("_pending - Cedric to write from the transcript_")
    lines.append("")
    lines.append("## Notes/Transcript")
    lines.append("")
    lines.append(prov)
    lines.append("")
    lines.append(body)
    lines.append("")
    return "\n".join(lines)

def process(vid, url, root, out_dir, date_str, source_note=None, force=False):
    if not force and already_done(out_dir, vid):
        print("SKIP (already transcribed): %s" % vid)
        return None
    title, author = oembed(vid)
    try:
        texts = get_segments(vid)
    except Exception as e:
        print("FAIL %s - no transcript: %r" % (vid, e))
        return None
    body, wc = clean_and_paragraph(texts)
    note = build_note(vid, url, title, author, body, wc, date_str, source_note)
    fname = "%s - Transcript - %s - %s.md" % (
        date_str, sanitize_filename(author or "Unknown"), sanitize_filename(title or vid))
    dest = os.path.join(out_dir, fname)
    bad = [ord(c) for c in note if ord(c) > 127]
    if bad:
        print("WARN non-ASCII slipped through:", bad[:5])
    open(dest, "w", encoding="utf-8", newline="").write(note)
    print("WROTE: %s  (%d words)" % (dest, wc))
    return dest

def scan_inbox(root, recursive=False):
    inbox = os.path.join(root, INBOX_REL)
    # Default: inbox ROOT only (where the gmail-self-notes sweep files fresh notes).
    # The YouTube-Queue subfolder is a separate backlog - opt in with --include-queue.
    pattern = os.path.join(inbox, "**", "*.md") if recursive else os.path.join(inbox, "*.md")
    found = []  # (vid, url, source_note_basename)
    seen = set()
    for fp in glob.glob(pattern, recursive=recursive):
        try:
            txt = open(fp, encoding="utf-8").read()
        except Exception:
            continue
        base = os.path.splitext(os.path.basename(fp))[0]
        for m in re.finditer(r"https?://[^\s\"'\)]*(?:youtube\.com|youtu\.be)[^\s\"'\)]*", txt):
            url = m.group(0)
            vid = parse_video_id(url)
            if vid and vid not in seen:
                seen.add(vid)
                found.append((vid, "https://www.youtube.com/watch?v=%s" % vid, base))
    return found

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", nargs="+", default=[])
    ap.add_argument("--scan-inbox", action="store_true")
    ap.add_argument("--include-queue", action="store_true",
                    help="with --scan-inbox, also scan the 00-Inbox/YouTube-Queue backlog (recursive)")
    ap.add_argument("--root", default=None)
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true",
                    help="list what would be processed (and dedupe status), write nothing")
    a = ap.parse_args()

    root = find_root(a.root)
    if not root:
        print("ERROR: cannot locate Dex-MickP vault. Pass --root."); sys.exit(2)
    out_dir = a.out_dir or os.path.join(root, TRANSCRIPTS_REL)
    os.makedirs(out_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y.%m.%d")

    jobs = []  # (vid, url, source_note)
    for u in a.url:
        vid = parse_video_id(u)
        if not vid:
            print("Could not parse a video id from: %s" % u); continue
        jobs.append((vid, "https://www.youtube.com/watch?v=%s" % vid, None))
    if a.scan_inbox:
        inbox_jobs = scan_inbox(root, recursive=a.include_queue)
        scope = "00-Inbox + YouTube-Queue" if a.include_queue else "00-Inbox root only"
        print("Inbox scan (%s) found %d unique YouTube video(s)." % (scope, len(inbox_jobs)))
        jobs.extend(inbox_jobs)

    if not jobs:
        print("Nothing to do. Use --url <link> or --scan-inbox."); return

    if a.dry_run:
        print("\nDRY RUN - would process %d video(s):" % len(jobs))
        for vid, url, src in jobs:
            state = "already transcribed (skip)" if already_done(out_dir, vid) else "NEW"
            print("  [%s] %s  %s" % (state, vid, ("from " + src) if src else url))
        return

    written = []
    for vid, url, src in jobs:
        dest = process(vid, url, root, out_dir, date_str, source_note=src, force=a.force)
        if dest:
            written.append(dest)
    print("\nDONE. %d note(s) written to %s" % (len(written), out_dir))
    for d in written:
        print(" -", os.path.basename(d))
    if written:
        print("\nNEXT: Cedric reads each note and fills the Summary and Key Takeaways,"
              " and sets 'By' to the human author name if oembed gave the channel.")

if __name__ == "__main__":
    main()

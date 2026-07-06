#!/usr/bin/env python3
# Scan a self-sent email body for YouTube links and any "add to NBLM" directive.
#
# Prints a JSON object on stdout with these keys:
#   videos      - list of objects, each with: raw, video_id, canonical, oembed
#   nblm        - true if an "add to NBLM" / NotebookLM directive was found
#   nblm_topic  - the topic text after the directive (may be empty)
#   annotation  - the email body with signature and bare YouTube URLs removed
#
# The skill fetches each video's title from the "oembed" URL (via web_fetch),
# then calls build_vault_note.py to write the inbox note. Tracking params
# (si, is, t, feature, pp, ...) are dropped so the stored URL is clean.
#
# ASCII only. UK English. No network access in this script - parsing only.

import argparse
import json
import re
import sys

# Each pattern captures the 11-char video id in group 1. The trailing [^\s]*
# swallows any tracking query so the whole URL token is removed from the annotation.
YT_PATTERNS = [
    r"(?:https?://)?(?:www\.|m\.)?youtube\.com/watch\?[^\s]*?\bv=([A-Za-z0-9_-]{11})[^\s]*",
    r"(?:https?://)?(?:www\.|m\.)?youtube\.com/shorts/([A-Za-z0-9_-]{11})[^\s]*",
    r"(?:https?://)?(?:www\.|m\.)?youtube\.com/live/([A-Za-z0-9_-]{11})[^\s]*",
    r"(?:https?://)?(?:www\.)?youtu\.be/([A-Za-z0-9_-]{11})[^\s]*",
    r"(?:https?://)?(?:www\.|m\.)?youtube\.com/embed/([A-Za-z0-9_-]{11})[^\s]*",
]

SIG_MARKERS = [
    "with best wishes",
    "author of",
    "picking winning shares",
    "website (1)",
    "website (2)",
    "www.diy-investors",
]

# "add to nblm re X", "nblm for X", "notebook lm: X", etc.
NBLM_RE = re.compile(
    r"\b(?:add\s+to\s+)?(?:nblm|notebook\s?lm)\b\s*(?:re|for|about|:|-)?\s*([^\n]*)",
    re.IGNORECASE,
)

STRIP_CHARS = " .-:"


def strip_signature(text):
    out = []
    for ln in text.splitlines():
        low = ln.strip().lower()
        if any(low.startswith(m) or (m in low and len(low) < 80) for m in SIG_MARKERS):
            break
        out.append(ln.rstrip())
    return "\n".join(out).strip()


def find_videos(text):
    seen = {}
    for pat in YT_PATTERNS:
        for m in re.finditer(pat, text):
            vid = m.group(1)
            if vid in seen:
                continue
            seen[vid] = {
                "raw": m.group(0),
                "video_id": vid,
                "canonical": "https://www.youtube.com/watch?v=" + vid,
                "oembed": "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=" + vid + "&format=json",
            }
    return list(seen.values())


def find_nblm(text):
    m = NBLM_RE.search(text)
    if not m:
        return False, ""
    topic = m.group(1).strip(STRIP_CHARS)
    if topic.lower().startswith("http") or len(topic) > 120:
        topic = ""
    return True, topic


def make_annotation(text, videos):
    ann = strip_signature(text)
    for v in videos:
        ann = ann.replace(v["raw"], "").strip()
    ann = re.sub(r"\n{3,}", "\n\n", ann).strip()
    return ann


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True, help="file containing the email body")
    args = ap.parse_args()
    try:
        text = open(args.text, encoding="utf-8", errors="replace").read()
    except OSError as exc:
        print(json.dumps({"error": str(exc)}))
        return 3
    videos = find_videos(text)
    nblm, topic = find_nblm(text)
    out = {
        "videos": videos,
        "nblm": nblm,
        "nblm_topic": topic,
        "annotation": make_annotation(text, videos),
    }
    print(json.dumps(out, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# Build an Obsidian markdown note for Mick's vault inbox from a self-sent Gmail item.
#
# Note types produced by the gmail-self-notes skill:
#   text       - the body text of a self-sent note (author usually Mick)
#   attachment - an attachment already converted to markdown (author Mick or MCSB)
#   youtube    - a captured YouTube link (author Mick; url in frontmatter)
#
# Schema harmonised 2026-07-05 with the vault _templates:
#   - author (not By), date_created (not created), url (lowercase) for the link.
#   - Category / status / topics placeholders always emitted (empty) for later use.
#   - Body adopts the template headings: ## Summary / ## Key Takeaways / ## Notes.
#
# Responsibilities:
#   - Strip Mick's standard signature block from raw email body text.
#   - Enforce ASCII-only output (vault house rule): map smart quotes/dashes, drop rest.
#   - Write YAML frontmatter with an author field (and any extra fields you pass).
#   - Name the file "YYYY.MM.DD - Title.md" (vault convention), de-duplicating.
#
# Content source (choose one): --body-file / --md-file / --body-text / none.
# Extra frontmatter: repeat --fm KEY=VALUE (url, channel, xref, action, nblm_topic,
#   summary, gmail_thread, email_date, tags, ...). VALUE is written verbatim, so pass
#   YAML lists like --fm tags="[inbox, youtube]" as-is.
# --detect-author overrides --author: MCSB if content mentions Cedric/PAIDA, else Mick.
# Body extras: --heading, --append (repeatable), --summary-pending.
#
# ASCII only. UK English.

import argparse
import datetime as dt
import os
import re
import sys

SIG_MARKERS = [
    "with best wishes from",
    "with best wishes",
    'author of "picking winning shares"',
    "picking winning shares",
    "website (1)",
    "website (2)",
    "www.diy-investors",
]

ASCII_MAP = {
    "'": "'", "'": "'", "'": "'", "'": "'",
    """: '"', """: '"', """: '"',
    "-": "-", "-": "-", "-": "-", "-": "-",
    "...": "...", " ": " ", "-": "-", "-": "-",
    "GBP": "GBP ", "EUR": "EUR ", "(TM)": "(TM)", "(R)": "(R)",
    "->": "->", "<-": "<-",
}

# Known frontmatter key order; unknown keys are appended alphabetically after these.
# xref = shared "same email" datetime key (YYYY.MM.DD-HH-mm-ss).
# related = two-way sibling wikilinks, injected post-build by link_siblings.py.
# Category / status / topics = placeholders shared with the vault _templates schema.
FM_ORDER = ["title", "author", "type", "url", "channel", "source",
            "date_created", "email_date", "gmail_thread", "xref", "action",
            "nblm_topic", "summary", "Category", "status", "topics",
            "tags", "related"]

# Emitted even when empty, so the property exists for later use / Base columns.
PLACEHOLDER_KEYS = {"Category", "status", "topics"}


def to_ascii(s):
    for k, v in ASCII_MAP.items():
        s = s.replace(k, v)
    return s.encode("ascii", "ignore").decode("ascii")


def strip_signature(text):
    out = []
    for ln in text.splitlines():
        low = ln.strip().lower()
        if any(low.startswith(m) or (m in low and len(low) < 80) for m in SIG_MARKERS):
            break
        out.append(ln.rstrip())
    while out and not out[-1].strip():
        out.pop()
    while out and not out[0].strip():
        out.pop(0)
    return "\n".join(out)


def slugify_title(t):
    t = to_ascii(t).strip()
    t = re.sub(r'[\\/:*?"<>|#^\[\]]+', " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:120] if t else "untitled"


def parse_date(s):
    if not s:
        return dt.date.today()
    s = s.strip().replace("Z", "+00:00")
    try:
        return dt.datetime.fromisoformat(s).date()
    except ValueError:
        m = re.match(r"(\d{4})[-/.](\d{2})[-/.](\d{2})", s)
        if m:
            return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return dt.date.today()


def unique_path(inbox, base):
    path = os.path.join(inbox, base + ".md")
    n = 2
    while os.path.exists(path):
        path = os.path.join(inbox, "%s (%d).md" % (base, n))
        n += 1
    return path


def build_frontmatter(fields):
    keys = [k for k in FM_ORDER if k in fields]
    keys += sorted(k for k in fields if k not in FM_ORDER)
    lines = ["---"]
    for k in keys:
        v = fields[k]
        if v is None or v == "":
            if k in PLACEHOLDER_KEYS:
                lines.append("%s:" % k)
            continue
        lines.append("%s: %s" % (k, v))
    lines.append("---")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Build an Obsidian vault note from a self-sent Gmail item.")
    ap.add_argument("--inbox", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--author", default="Mick")
    ap.add_argument("--type", default="note")
    ap.add_argument("--date", default="")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--body-file")
    src.add_argument("--md-file")
    src.add_argument("--body-text")
    ap.add_argument("--fm", action="append", default=[], metavar="KEY=VALUE")
    ap.add_argument("--detect-author", action="store_true")
    ap.add_argument("--heading")
    ap.add_argument("--append", action="append", default=[])
    ap.add_argument("--summary-pending", action="store_true")
    args = ap.parse_args()

    if not os.path.isdir(args.inbox):
        print("INPUT ERROR: inbox folder does not exist: %s" % args.inbox)
        return 3

    body = ""
    try:
        if args.body_file:
            body = strip_signature(open(args.body_file, encoding="utf-8", errors="replace").read())
        elif args.md_file:
            body = open(args.md_file, encoding="utf-8", errors="replace").read()
        elif args.body_text:
            body = strip_signature(args.body_text)
    except OSError as exc:
        print("INPUT ERROR: %s" % exc)
        return 3
    body = to_ascii(body).strip()

    author = args.author
    if args.detect_author:
        probe = (body + " " + args.title).lower()
        author = "MCSB" if ("cedric" in probe or "paida" in probe) else "Mick"

    fields = {
        "title": to_ascii(args.title).strip(),
        "author": author,
        "type": args.type,
        "source": "gmail-self-note",
        "date_created": dt.date.today().isoformat(),
        "Category": "",
        "status": "",
        "topics": "",
    }
    for pair in args.fm:
        if "=" not in pair:
            print("INPUT ERROR: --fm needs KEY=VALUE, got: %s" % pair)
            return 3
        k, v = pair.split("=", 1)
        fields[k.strip()] = to_ascii(v).strip()
    if args.summary_pending and "summary" not in fields:
        fields["summary"] = "pending"

    # Body adopts the vault template headings: Summary / Key Takeaways / Notes.
    notes_parts = []
    if args.heading:
        notes_parts.append("# " + to_ascii(args.heading).strip())
    if body:
        notes_parts.append(body)
    for extra in args.append:
        notes_parts.append(to_ascii(extra).strip())
    notes_block = "## Notes"
    joined = "\n\n".join(p for p in notes_parts if p)
    if joined:
        notes_block += "\n\n" + joined

    summary_block = "## Summary"
    if args.summary_pending:
        summary_block += "\n\n> To be filled on demand."

    body_out = "\n\n".join([summary_block, "## Key Takeaways", notes_block])

    prefix = parse_date(args.date).strftime("%Y.%m.%d")
    base = "%s - %s" % (prefix, slugify_title(args.title))
    os.makedirs(args.inbox, exist_ok=True)
    path = unique_path(args.inbox, base)

    content = build_frontmatter(fields) + "\n\n" + body_out + "\n"
    content = to_ascii(content)
    with open(path, "w", encoding="ascii", errors="ignore", newline="\n") as fh:
        fh.write(content)

    print("WROTE: %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())

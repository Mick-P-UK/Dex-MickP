#!/usr/bin/env python3
# Inject two-way "related" wikilinks into a set of vault notes that came from the
# same self-sent email (they share an xref). Pass 2+ note paths. Each note gets:
#   - a frontmatter  related:  YAML list of the OTHER notes as quoted wikilinks
#   - a "## Related" body section with the same wikilinks
# Idempotent: any existing related: block and "## Related" section are replaced,
# so re-running (or a later top-up) is safe.
#
# ASCII only. UK English.

import argparse
import os
import sys


def wikilink(path):
    return '"[[' + os.path.splitext(os.path.basename(path))[0] + ']]"'


def split_note(text):
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return lines[1:i], lines[i + 1:]
    return None, lines


def strip_related_fm(fm_lines):
    out = []
    skipping = False
    for ln in fm_lines:
        if ln.startswith("related:"):
            skipping = True
            continue
        if skipping:
            # continuation lines of a YAML list are indented ("  - ...")
            if ln.startswith(" ") or ln.startswith("\t"):
                continue
            skipping = False
        out.append(ln)
    return out


def strip_related_section(body_lines):
    out = []
    skipping = False
    for ln in body_lines:
        if ln.strip().lower() == "## related":
            skipping = True
            continue
        if skipping:
            # stop skipping at the next heading
            if ln.startswith("#"):
                skipping = False
                out.append(ln)
            # otherwise drop the old related lines
            continue
        out.append(ln)
    return out


def insert_related_fm(fm_lines, links):
    # place related just before 'created:' if present, else at end
    block = ["related:"] + ["  - " + l for l in links]
    idx = None
    for i, ln in enumerate(fm_lines):
        if ln.startswith("created:"):
            idx = i
            break
    if idx is None:
        return fm_lines + block
    return fm_lines[:idx] + block + fm_lines[idx:]


def rebuild(text, links):
    fm_lines, body_lines = split_note(text)
    section = ["", "## Related", ""] + ["- " + l.strip('"') for l in links] + [""]
    if fm_lines is None:
        # no frontmatter - just manage the body section
        body_lines = strip_related_section(body_lines)
        return "\n".join(body_lines).rstrip() + "\n" + "\n".join(section) + "\n"
    fm_lines = strip_related_fm(fm_lines)
    fm_lines = insert_related_fm(fm_lines, links)
    body_lines = strip_related_section(body_lines)
    body = "\n".join(body_lines).rstrip()
    out = ["---"] + fm_lines + ["---", "", body] + section
    return "\n".join(out).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+", help="2+ note paths sharing an xref")
    args = ap.parse_args()
    paths = [p for p in args.paths if os.path.isfile(p)]
    if len(paths) < 2:
        print("Nothing to link (need 2+ existing notes).")
        return 0
    for target in paths:
        others = [wikilink(p) for p in paths if p != target]
        with open(target, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        new = rebuild(text, others)
        new = new.encode("ascii", "ignore").decode("ascii")
        with open(target, "w", encoding="ascii", errors="ignore", newline="\n") as fh:
            fh.write(new)
        print("LINKED: %s -> %d sibling(s)" % (os.path.basename(target), len(others)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

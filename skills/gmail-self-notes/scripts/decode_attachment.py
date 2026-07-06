#!/usr/bin/env python3
"""
Decode a base64 attachment (from the Google Drive download_file_content connector)
into a real binary file, then validate it for its extension.

Two input modes:
  --from-json PATH   PATH is a JSON file (e.g. an auto-saved tool-result) that
                     contains a top-level "content" field holding the base64 string.
  --from-b64  PATH   PATH is a plain text file containing only the base64 string.

Usage:
  python decode_attachment.py --from-json tool-result.txt --out "/outputs/note.docx"
  python decode_attachment.py --from-b64  attach.b64      --out "/outputs/note.pdf"

Exit codes:
  0  decoded and validated OK
  2  decoded but validation FAILED (do not ship the file; retry or fall back)
  3  usage / input error (could not read or decode the base64)

ASCII only. UK English.
"""

import argparse
import base64
import json
import os
import sys
import zipfile


def load_b64_from_json(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        raw = fh.read().strip()
    # The file may be pure JSON, or JSON with surrounding noise. Try strict first.
    try:
        obj = json.loads(raw)
        if isinstance(obj, dict) and "content" in obj:
            return obj["content"]
    except json.JSONDecodeError:
        pass
    # Fallback: pull the value of the first "content":"..." pair by hand.
    marker = '"content"'
    i = raw.find(marker)
    if i == -1:
        raise ValueError('No "content" field found in JSON input.')
    j = raw.find('"', i + len(marker))
    if j == -1:
        raise ValueError('Malformed "content" field.')
    j += 1
    k = raw.find('"', j)
    if k == -1:
        raise ValueError('Unterminated "content" value.')
    return raw[j:k]


def load_b64_from_text(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read().strip()


def validate(path):
    """Return (ok, message) for the decoded file based on its extension."""
    ext = os.path.splitext(path)[1].lower()
    zip_exts = {".docx", ".xlsx", ".pptx", ".dotx", ".xlsm", ".potx"}
    try:
        with open(path, "rb") as fh:
            head = fh.read(8)
    except OSError as exc:
        return False, "cannot reopen decoded file: %s" % exc

    if ext in zip_exts:
        if not zipfile.is_zipfile(path):
            return False, "not a valid Office (zip) file"
        try:
            with zipfile.ZipFile(path) as z:
                bad = z.testzip()
                if bad is not None:
                    return False, "corrupt zip entry: %s" % bad
                n = len(z.namelist())
            return True, "valid Office file, %d entries" % n
        except zipfile.BadZipFile:
            return False, "bad zip structure"

    if ext == ".pdf":
        if head[:4] == b"%PDF":
            return True, "valid PDF header"
        return False, "missing %PDF header"

    if ext in {".png"}:
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            return True, "valid PNG header"
        return False, "missing PNG header"

    if ext in {".jpg", ".jpeg"}:
        if head[:3] == b"\xff\xd8\xff":
            return True, "valid JPEG header"
        return False, "missing JPEG header"

    # Unknown/text type: accept as long as some bytes were written.
    size = os.path.getsize(path)
    if size > 0:
        return True, "%d bytes written (no format check for %s)" % (size, ext or "no-ext")
    return False, "empty file"


def main():
    ap = argparse.ArgumentParser(description="Decode + validate a base64 attachment.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--from-json", metavar="PATH", help="JSON file with a 'content' base64 field")
    src.add_argument("--from-b64", metavar="PATH", help="text file with only the base64 string")
    ap.add_argument("--out", required=True, metavar="PATH", help="output file path (keep the real extension)")
    args = ap.parse_args()

    try:
        b64 = load_b64_from_json(args.from_json) if args.from_json else load_b64_from_text(args.from_b64)
    except (OSError, ValueError) as exc:
        print("INPUT ERROR: %s" % exc)
        return 3

    b64 = "".join(b64.split())  # strip any whitespace/newlines
    try:
        data = base64.b64decode(b64, validate=True)
    except (base64.binascii.Error, ValueError) as exc:
        print("DECODE ERROR: base64 did not decode cleanly (%s). Re-download; do not hand-paste." % exc)
        return 3

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "wb") as fh:
        fh.write(data)

    ok, msg = validate(args.out)
    if ok:
        print("OK: %s (%d bytes) - %s" % (args.out, len(data), msg))
        return 0
    print("FAIL: %s - %s. Retry the download or use the docx text-rebuild fallback." % (args.out, msg))
    return 2


if __name__ == "__main__":
    sys.exit(main())

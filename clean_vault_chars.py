#!/usr/bin/env python3
"""
Clean Windows-1252 non-ASCII bytes from vault .md files.
Targets exactly the characters flagged by the pre-commit hook.
Run from: C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\
"""

import os

FILES = [
    r"C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\CHANGELOG.md",
    r"C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\CLAUDE.md",
    r"C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\ai4inv-webinar-processor\SKILL.md",
]

# Multi-byte patterns first (order matters - do these before single-byte)
MULTI_BYTE = [
    (b'\x80\x94', b' --'),
    (b'\x80\x93', b' --'),
    (b'\x80\x92', b"'"),
    (b'\x80\x99', b'(TM)'),
]

# Single-byte patterns
SINGLE_BYTE = [
    (b'\x80', b''),
    (b'\x85', b'...'),
    (b'\x91', b"'"),
    (b'\x92', b"'"),
    (b'\x93', b'"'),
    (b'\x94', b'"'),
    (b'\x95', b'-'),
    (b'\x96', b'-'),
    (b'\x97', b'-'),
    (b'\x99', b'(TM)'),
    (b'\xa0', b' '),
]

BANNED_BYTES = set([b[0] for b, _ in MULTI_BYTE] + [b[0] for b, _ in SINGLE_BYTE])

def clean_bytes(data):
    for bad, good in MULTI_BYTE:
        data = data.replace(bad, good)
    for bad, good in SINGLE_BYTE:
        data = data.replace(bad, good)
    return data

def find_remaining(data):
    return [(i, b) for i, b in enumerate(data) if b in BANNED_BYTES]

total_cleaned = 0
for filepath in FILES:
    fname = os.path.basename(filepath)
    try:
        with open(filepath, 'rb') as f:
            original = f.read()

        cleaned = clean_bytes(original)

        if cleaned == original:
            print(f"[OK]    {fname} - no changes needed")
            continue

        remaining = find_remaining(cleaned)
        if remaining:
            print(f"[WARN]  {fname} - {len(remaining)} issues remain after cleaning:")
            for pos, byte in remaining[:5]:
                print(f"          pos {pos}: 0x{byte:02X}")
            continue

        with open(filepath, 'wb') as f:
            f.write(cleaned)

        print(f"[FIXED] {fname} - cleaned successfully")
        total_cleaned += 1

    except FileNotFoundError:
        print(f"[MISS]  {fname} - file not found at {filepath}")
    except Exception as e:
        print(f"[ERR]   {fname} - {e}")

print()
print(f"Done. {total_cleaned} file(s) cleaned.")
if total_cleaned > 0:
    print("Next step: python daily_git_commit.py")

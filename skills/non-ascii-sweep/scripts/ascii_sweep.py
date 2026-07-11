#!/usr/bin/env python3
"""
ascii_sweep.py - Non-ASCII sweep for the Dex-MickP vault.

Modes:
  scan  - report only, change nothing (default).
  safe  - auto-fix ONLY typography corruption (curly quotes, dashes, ellipsis,
          non-breaking spaces, bullets, arrows, box-drawing). Report any remaining
          meaningful non-ASCII (currency, emoji, accents) for manual review. Never
          transliterates aggressively. This is the mode the weekly schedule uses.
  full  - the complete pass: typography PLUS currency->ASCII, status glyphs->tags,
          drop decorative emoji + private-use glyphs + broken U+FFFD, transliterate
          accented letters to base, and re-decode wrong-encoding (cp1252) text files.
          On-demand only, with Mick's go-ahead.

Usage:
  python3 ascii_sweep.py --mode safe
  python3 ascii_sweep.py --mode scan --root "/path/to/Dex-MickP"
  python3 ascii_sweep.py --mode full --no-report

NOTE: this file is written in PURE ASCII on purpose. Every special character is
referenced by its Unicode code point (chr(...)) so the sweep can never corrupt its
own mapping tables when it cleans the vault that contains it.
"""
import os, sys, glob, argparse, collections, unicodedata
from datetime import datetime, timezone, timedelta

SKIP_DIRS = {'.git', 'node_modules', '__pycache__', '.obsidian', '.venv', 'venv',
             'site-packages', '.pytest_cache', '.mypy_cache', 'dist', 'build'}
BIN_EXT = {'.png','.jpg','.jpeg','.gif','.pdf','.docx','.pptx','.xlsx','.xls','.zip',
           '.ico','.pyc','.woff','.woff2','.ttf','.otf','.mp3','.mp4','.mov','.svg',
           '.webp','.gz','.pack','.idx','.db','.sqlite','.pickle','.pkl','.p12',
           '.pem','.key','.heic','.wav','.m4a','.eot','.bin'}

_TYPO_CP = [
 (0x2018,"'"),(0x2019,"'"),(0x201A,"'"),(0x201B,"'"),
 (0x201C,'"'),(0x201D,'"'),(0x201E,'"'),(0x201F,'"'),
 (0x2013,'-'),(0x2014,'-'),(0x2015,'-'),(0x2012,'-'),(0x2010,'-'),(0x2011,'-'),(0x2212,'-'),
 (0x2026,'...'),
 (0x00A0,' '),(0x2007,' '),(0x2008,' '),(0x2009,' '),(0x200A,' '),
 (0x2002,' '),(0x2003,' '),(0x2004,' '),(0x2005,' '),(0x2006,' '),(0x202F,' '),(0x205F,' '),
 (0x2022,'-'),(0x00B7,'-'),(0x2023,'-'),(0x2043,'-'),(0x2027,'-'),
 (0x2192,'->'),(0x2190,'<-'),(0x2191,'^'),(0x2193,'v'),(0x2194,'<->'),
 (0x21D2,'=>'),(0x21D0,'<='),
 (0x2032,"'"),(0x2033,'"'),
 (0x200B,''),(0xFEFF,''),(0x00AD,''),(0x200E,''),(0x200F,''),(0x200C,''),(0x200D,''),
 (0x00B4,"'"),
]
TYPO = {chr(cp): rep for cp, rep in _TYPO_CP}

def box_map(o):
    if o in (0x2500,0x2501,0x2504,0x2505,0x2508,0x2509,0x254C,0x254D,0x2574,0x2576,0x2578,0x257A):
        return '-'
    if o in (0x2502,0x2503,0x2506,0x2507,0x250A,0x250B,0x254E,0x254F,0x2575,0x2577,0x2579,0x257B):
        return '|'
    if 0x2500 <= o <= 0x257F:
        return '+'
    if 0x2580 <= o <= 0x259F:
        return '#'
    return None

_FULL_CP = [
 (0x00A3,'GBP'),(0x20AC,'EUR'),(0x00A2,'c'),(0x00A5,'JPY'),(0x20B9,'INR'),
 (0x00A4,''),(0x20A9,'KRW'),
 (0x2122,'(TM)'),(0x00A9,'(c)'),(0x00AE,'(R)'),(0x00B0,' deg'),(0x00B1,'+/-'),
 (0x00D7,'x'),(0x00F7,'/'),(0x2248,'~'),(0x2264,'<='),(0x2265,'>='),(0x2260,'!='),
 (0x2261,'=='),(0x221A,'sqrt'),(0x221E,'inf'),(0x00B5,'u'),(0x00A7,'section'),
 (0x00B6,'para'),(0x2030,' per mille'),(0x2020,'+'),(0x2021,'++'),
 (0x2039,'<'),(0x203A,'>'),(0x00AB,'<<'),(0x00BB,'>>'),
 (0x00BC,'1/4'),(0x00BD,'1/2'),(0x00BE,'3/4'),(0x2044,'/'),
 (0x2211,'sum'),(0x220F,'prod'),
 (0x2705,'[x]'),(0x2714,'[x]'),(0x2713,'[x]'),(0x2611,'[x]'),(0x25A0,'[x]'),(0x25FC,'[x]'),(0x2612,'[x]'),
 (0x274C,'[ ]'),(0x2717,'[ ]'),(0x2718,'[ ]'),(0x2610,'[ ]'),(0x25A1,'[ ]'),
 (0x25B2,'^'),(0x25B3,'^'),(0x25B4,'^'),(0x25B8,'>'),(0x25B6,'>'),(0x25BA,'>'),(0x25B7,'^'),
 (0x25C0,'<'),(0x25C4,'<'),(0x25C1,'<'),
 (0x25BC,'v'),(0x25BD,'v'),(0x25BE,'v'),(0x25BF,'v'),
 (0x25CF,'*'),(0x25CB,'o'),(0x25E6,'o'),(0x25C6,'*'),(0x25C7,'*'),(0x25AA,'-'),(0x25AB,'-'),
 (0x2605,'*'),(0x2606,'*'),(0x2B50,'*'),
 (0x26A0,'[!]'),(0x2757,'[!]'),(0x2755,'[!]'),(0x2753,'[?]'),(0x2139,'[i]'),
 (0x23F3,'[~]'),(0x23F8,'[||]'),(0x23F9,'[stop]'),(0x23FA,'[rec]'),
 (0x2B06,'^'),(0x2B07,'v'),(0x2B05,'<-'),(0x27A1,'->'),
 (0x2795,'+'),(0x2796,'-'),(0x2716,'x'),(0x2733,'*'),(0x2734,'*'),
 (0x1F534,'[red]'),(0x1F7E2,'[green]'),(0x1F7E1,'[amber]'),(0x1F535,'[blue]'),
 (0x1F7E0,'[orange]'),(0x1F7E3,'[purple]'),(0x1F7E4,'[brown]'),
 (0x26AB,'[black]'),(0x26AA,'[white]'),
]
FULL_EXTRA = {chr(cp): rep for cp, rep in _FULL_CP}

DROP_RANGES = [
 (0xE000,0xF8FF),(0xFE00,0xFE0F),(0x1F000,0x1FAFF),(0x1F1E6,0x1F1FF),
 (0x2600,0x27BF),(0x2B00,0x2BFF),(0x2300,0x23FF),(0x2460,0x24FF),
 (0x25A0,0x25FF),(0x1F900,0x1F9FF),
]

def in_drop(o):
    if o == 0xFFFD or o == 0x20E3:
        return True
    for a, b in DROP_RANGES:
        if a <= o <= b:
            return True
    return False

def clean_typo(t):
    out = []
    for ch in t:
        o = ord(ch)
        if o < 128:
            out.append(ch); continue
        if ch in TYPO:
            out.append(TYPO[ch]); continue
        bm = box_map(o)
        if bm is not None:
            out.append(bm); continue
        out.append(ch)
    return ''.join(out)

def clean_full(t):
    out = []
    for ch in t:
        o = ord(ch)
        if o < 128:
            out.append(ch); continue
        if ch in TYPO:
            out.append(TYPO[ch]); continue
        bm = box_map(o)
        if bm is not None:
            out.append(bm); continue
        if ch in FULL_EXTRA:
            out.append(FULL_EXTRA[ch]); continue
        if in_drop(o):
            continue
        dec = unicodedata.normalize('NFKD', ch)
        out.append(''.join(c for c in dec if ord(c) < 128))
    s = ''.join(out)
    return ''.join(c for c in s if ord(c) < 128)

CURR = {0x00A3, 0x20AC, 0x00A2, 0x00A5, 0x20B9}
def bucket(ch):
    o = ord(ch)
    if o in CURR: return 'currency'
    if 0xE000 <= o <= 0xF8FF: return 'private-use glyphs'
    if o == 0xFFFD: return 'broken (U+FFFD)'
    if (0x1F000 <= o) or (0x2600 <= o <= 0x27BF) or (0x25A0 <= o <= 0x25FF) or (0x2B00 <= o <= 0x2BFF):
        return 'emoji/status/shapes'
    if 0xC0 <= o <= 0x24F: return 'accented letters'
    return 'other symbols'

def london_now():
    u = datetime.now(timezone.utc)
    bst = 4 <= u.month <= 10
    return u.astimezone(timezone(timedelta(hours=1 if bst else 0)))

def detect_root(override):
    if override:
        return override
    for pat in ('/sessions/*/mnt/*/Dex-MickP', '/mnt/*/Dex-MickP', '*/Dex-MickP'):
        hits = [h for h in glob.glob(pat) if os.path.isdir(h)]
        if hits:
            return hits[0]
    here = os.path.abspath(os.path.dirname(__file__))
    while here != '/':
        if os.path.exists(os.path.join(here, 'CEDRIC_MEMORY.md')):
            return here
        here = os.path.dirname(here)
    return None

def iter_files(root):
    for dp, dn, fns in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for fn in fns:
            if os.path.splitext(fn)[1].lower() in BIN_EXT:
                continue
            yield os.path.join(dp, fn)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', choices=['scan', 'safe', 'full'], default='scan')
    ap.add_argument('--root', default=None)
    ap.add_argument('--no-report', action='store_true')
    a = ap.parse_args()

    root = detect_root(a.root)
    if not root:
        print('ERROR: could not locate the Dex-MickP vault. Pass --root.'); sys.exit(2)

    modified = 0; recoded = []; skipped_bin = []; errors = []; undecodable = []
    remaining = collections.Counter(); remaining_files = collections.Counter()

    for fp in iter_files(root):
        rel = os.path.relpath(fp, root)
        try:
            raw = open(fp, 'rb').read()
        except Exception as e:
            errors.append((rel, str(e))); continue
        used_cp1252 = False
        try:
            t = raw.decode('utf-8')
        except UnicodeDecodeError:
            if a.mode != 'full':
                undecodable.append(rel); continue
            try:
                t = raw.decode('cp1252')
            except Exception:
                undecodable.append(rel); continue
            printable = sum(1 for c in t if c in '\n\t' or 32 <= ord(c) < 127 or ord(c) >= 160)
            if not t or printable / len(t) < 0.90:
                skipped_bin.append(rel); continue
            used_cp1252 = True

        if a.mode == 'scan':
            newt = t
        elif a.mode == 'safe':
            newt = clean_typo(t)
        else:
            newt = clean_full(t)

        if a.mode != 'scan' and (newt != t or used_cp1252):
            try:
                open(fp, 'w', encoding='utf-8', newline='').write(newt)
                modified += 1
                if used_cp1252:
                    recoded.append(rel)
            except Exception as e:
                errors.append((rel, str(e))); continue

        for ch in newt:
            if ord(ch) >= 128:
                remaining[bucket(ch)] += 1
                remaining_files[rel] += 1

    now = london_now()
    L = []
    L.append("# Non-ASCII Sweep Report (%s mode) - %s London" % (a.mode, now.strftime('%Y.%m.%d %H:%M')))
    L.append("")
    L.append("Vault root: %s" % root)
    L.append("Mode: %s" % a.mode)
    if a.mode != 'scan':
        L.append("Files modified: %d" % modified)
        if recoded:
            L.append("Wrong-encoding text files re-decoded (cp1252 -> UTF-8): %d" % len(recoded))
    L.append("")
    total_rem = sum(remaining.values())
    if a.mode == 'full':
        L.append("Non-ASCII remaining after full clean: %d (target 0)" % total_rem)
    elif a.mode == 'safe':
        L.append("Meaningful non-ASCII remaining for review (not auto-changed): %d" % total_rem)
    else:
        L.append("Total non-ASCII found: %d" % total_rem)
    L.append("")
    if remaining:
        L.append("## By category")
        for k, c in remaining.most_common():
            L.append("- %d : %s" % (c, k))
        L.append("")
        L.append("## Top files")
        for f, c in remaining_files.most_common(25):
            L.append("- %d : %s" % (c, f))
        L.append("")
    if recoded:
        L.append("## Wrong-encoding text files re-decoded")
        for f in recoded:
            L.append("- %s" % f)
        L.append("")
    if undecodable:
        L.append("## Files that cannot be decoded as text (left untouched)")
        for f in undecodable:
            L.append("- %s" % f)
        L.append("")
    if skipped_bin:
        L.append("## Skipped as binary/non-text during full pass")
        for f in skipped_bin:
            L.append("- %s" % f)
        L.append("")
    if errors:
        L.append("## Errors")
        for f, e in errors[:30]:
            L.append("- %s - %s" % (f, e))
        L.append("")
    report = "\n".join(L) + "\n"

    if not a.no_report:
        rdir = os.path.join(root, 'System', 'Debug_Logs')
        os.makedirs(rdir, exist_ok=True)
        rpath = os.path.join(rdir, "%s - Non-ASCII Sweep (%s).md" % (now.strftime('%Y.%m.%d'), a.mode))
        open(rpath, 'w', encoding='utf-8', newline='').write(report)
        print("Report written:", os.path.relpath(rpath, root))

    print("[non-ascii-sweep] mode=%s modified=%d remaining_nonascii=%d undecodable=%d errors=%d"
          % (a.mode, modified, total_rem, len(undecodable), len(errors)))
    if remaining:
        print("  categories: " + ", ".join("%s=%d" % (k, c) for k, c in remaining.most_common()))

if __name__ == '__main__':
    main()

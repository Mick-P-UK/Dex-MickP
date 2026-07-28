"""Read the real palette, fonts and chrome geometry out of a target .pptx.

Usage:
    python extract_theme.py "path/to/deck.pptx" [--slide N]

Why this exists: Mick's decks routinely carry the stock Office 2007 colour
scheme in ppt/theme/theme1.xml while the actual branding lives in literal
srgbClr values on the slides. Reading only the theme part gives you 4F81BD and
a wrong answer. This prints both, plus the layout geometry of a representative
content slide so a new graphic can sit on the same chrome.
"""
import argparse
import collections
import os
import re
import shutil
import sys
import tempfile
import zipfile

HEX = r'([0-9A-Fa-f]{6})'


def unpack(pptx_path):
    tmp = tempfile.mkdtemp(prefix="pptx_theme_")
    zipfile.ZipFile(pptx_path).extractall(tmp)
    return tmp


def theme_part(root):
    x = open(os.path.join(root, "ppt", "theme", "theme1.xml"),
             encoding="utf-8").read()
    print("THEME PART (ppt/theme/theme1.xml)")
    m = re.search(r"<a:clrScheme.*?</a:clrScheme>", x, re.S)
    if m:
        for g in re.finditer(
                r'<a:(\w+)>\s*<a:(?:srgbClr val="%s"|sysClr[^>]*lastClr="%s")' % (HEX, HEX),
                m.group(0)):
            print("   %-10s #%s" % (g.group(1), g.group(2) or g.group(3)))
    f = re.search(r"<a:fontScheme.*?</a:fontScheme>", x, re.S)
    if f:
        for g in re.finditer(r'<a:(major|minor)Font>\s*<a:latin typeface="([^"]*)"',
                             f.group(0)):
            print("   %-10s %s" % (g.group(1) + "Font", g.group(2)))
    print("   (if this looks like stock Office - 4F81BD/C0504D/9BBB59 - ignore it")
    print("    and use the slide census below)")


def slide_files(root):
    d = os.path.join(root, "ppt", "slides")
    fs = [f for f in os.listdir(d) if re.match(r"slide\d+\.xml$", f)]
    return sorted(fs, key=lambda f: int(re.search(r"\d+", f).group()))


def census(root):
    counts, per_slide = collections.Counter(), {}
    for f in slide_files(root):
        x = open(os.path.join(root, "ppt", "slides", f), encoding="utf-8").read()
        hits = re.findall(r'srgbClr val="%s"' % HEX, x)
        per_slide[f] = collections.Counter(h.upper() for h in hits)
        counts.update(h.upper() for h in hits)
    print("\nLITERAL COLOUR CENSUS ACROSS ALL SLIDES (this is the real palette)")
    for k, v in counts.most_common(20):
        print("   #%s  x%d" % (k, v))
    return per_slide


def pick_representative(per_slide):
    """The slide using the most distinct brand colours is usually the fullest
    example of the house content layout."""
    best, score = None, -1
    for f, c in per_slide.items():
        distinct = len([k for k in c if k not in ("FFFFFF", "000000")])
        if distinct > score:
            best, score = f, distinct
    return best


def chrome(root, slide_file):
    x = open(os.path.join(root, "ppt", "slides", slide_file), encoding="utf-8").read()
    print("\nCHROME GEOMETRY from %s (inches: x, y, w, h)" % slide_file)
    for m in re.finditer(r"<p:sp>.*?</p:sp>", x, re.S):
        s = m.group(0)
        geom = re.search(r'prstGeom prst="(\w+)"', s)
        if not geom:
            continue
        name = re.search(r'name="([^"]*)"', s)
        off = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"/>'
                        r'<a:ext cx="(\d+)" cy="(\d+)"', s)
        fills = re.findall(r'<a:solidFill><a:srgbClr val="%s"' % HEX, s)
        ln = re.search(r'<a:ln w="(\d+)"[^>]*>\s*<a:solidFill><a:srgbClr val="%s"' % HEX, s)
        box = tuple(round(int(v) / 914400.0, 2) for v in off.groups()) if off else None
        print("   %-12s %-18s %-28s fills=%s line=%s"
              % ((name.group(1) if name else "")[:12], geom.group(1), str(box),
                 ["#" + f for f in fills[:3]],
                 ("%.2fpt #%s" % (int(ln.group(1)) / 12700.0, ln.group(2))) if ln else None))
    print("\n   Text colours on that slide are the fills on shapes named Text*.")
    print("   Copy the panel/bar/badge rectangles to reproduce the house chrome.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx")
    ap.add_argument("--slide", type=int, default=None,
                    help="1-based slide number to read chrome from")
    a = ap.parse_args()
    if not os.path.exists(a.pptx):
        sys.exit("not found: %s" % a.pptx)

    root = unpack(a.pptx)
    try:
        theme_part(root)
        per_slide = census(root)
        target = ("slide%d.xml" % a.slide) if a.slide else pick_representative(per_slide)
        chrome(root, target)
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    main()

"""Validate a .pptx, render it to JPEGs and print the paths for inspection.

Usage:
    python qa_render.py "output.pptx" [--dpi 130] [--first 1] [--last 5]

Always look at the images. The first render of a new graphic nearly always has
one real defect - overflow, an overlap, or something sitting outside its panel.
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys

SKILL_CANDIDATES = [
    "/root/.claude/skills/pptx/scripts/office",
    "/mnt/skills/public/pptx/scripts/office",
    os.path.expanduser("~/.claude/skills/pptx/scripts/office"),
]


def find_office_scripts():
    for d in SKILL_CANDIDATES:
        if os.path.isdir(d):
            return d
    return None


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx")
    ap.add_argument("--dpi", type=int, default=130)
    ap.add_argument("--first", type=int, default=1)
    ap.add_argument("--last", type=int, default=0)
    a = ap.parse_args()

    if not os.path.exists(a.pptx):
        sys.exit("not found: %s" % a.pptx)

    work = os.path.dirname(os.path.abspath(a.pptx)) or "."
    stem = os.path.splitext(os.path.basename(a.pptx))[0]
    office = find_office_scripts()

    # 1. package validation
    if office and os.path.exists(os.path.join(office, "validate.py")):
        r = run([sys.executable, os.path.join(office, "validate.py"), a.pptx])
        print(r.stdout.strip() or r.stderr.strip())
    else:
        print("validate.py not found - skipping package validation")

    # 2. pptx -> pdf
    soffice = os.path.join(office, "soffice.py") if office else None
    if soffice and os.path.exists(soffice):
        cmd = [sys.executable, soffice, "--headless", "--convert-to", "pdf", a.pptx]
    else:
        cmd = ["soffice", "--headless", "--convert-to", "pdf", a.pptx]
    r = run(cmd, cwd=work, timeout=600)
    pdf = os.path.join(work, stem + ".pdf")
    if not os.path.exists(pdf):
        sys.exit("PDF conversion failed:\n" + (r.stderr or r.stdout))

    # 3. pdf -> jpegs
    prefix = os.path.join(work, "qa_" + stem.replace(" ", "_")[:30])
    for old in glob.glob(prefix + "-*.jpg"):
        os.remove(old)
    pt = ["pdftoppm", "-jpeg", "-r", str(a.dpi), "-f", str(a.first)]
    if a.last:
        pt += ["-l", str(a.last)]
    pt += [pdf, prefix]
    r = run(pt)
    imgs = sorted(glob.glob(prefix + "-*.jpg"))
    if not imgs:
        sys.exit("no images produced:\n" + (r.stderr or r.stdout))

    print("\nRENDERED - open these and look at them:")
    for i in imgs:
        print("  " + os.path.abspath(i))
    print("\nCheck for: text overflowing its box or its panel, shapes outside the "
          "content area, overlaps, unwanted drop shadows (see the effectRef "
          "gotcha in SKILL.md), low-contrast label text, uneven margins.")


if __name__ == "__main__":
    main()

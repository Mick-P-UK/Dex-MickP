#!/usr/bin/env python3
"""
pad_slide_numbers.py - Zero-pad trailing numbers in filenames so they sort naturally.

Problem this solves: exported slide sets are named Slide1.PNG ... Slide52.PNG.
When sorted alphabetically, Slide1, Slide10, Slide11 ... come before Slide2,
which is out of sequence. Padding the single-digit numbers (Slide1 -> Slide01)
makes every file sort in true numeric order.

Design:
- Auto-detects the pad width from the HIGHEST number present, per name group.
  52 slides   -> width 2 (Slide01 ... Slide52)
  120 slides  -> width 3 (Slide001 ... Slide120)
  Never shortens an already-wider number.
- Idempotent: files already padded correctly are skipped. Safe to run twice.
- Collision-safe: renames via unique temp names (two-phase), and aborts with a
  clear message if a target name already exists as an unrelated file.
- Groups by (prefix, extension), so a folder can hold more than one series and
  each is padded to its own width independently.
- Only the TRAILING digits of the name stem are treated as the number, so a
  dated prefix like "2026.07.22 - Deck - Slide1.PNG" pads only the "1".

Usage:
    python pad_slide_numbers.py "<folder>"                 # rename in place
    python pad_slide_numbers.py "<folder>" --dry-run       # preview only
    python pad_slide_numbers.py "<folder>" --prefix Slide  # only that series

Exit codes: 0 = success (including nothing-to-do), 1 = error / collision abort.
"""

import argparse
import os
import re
import sys

STEM_NUMBER_RE = re.compile(r"^(?P<prefix>.*?)(?P<num>\d+)$")


def scan(folder, prefix_filter=None):
    """Return {(prefix, ext): [(name, num_str, num_int), ...]} for numbered files."""
    groups = {}
    for name in os.listdir(folder):
        full = os.path.join(folder, name)
        if not os.path.isfile(full):
            continue
        stem, ext = os.path.splitext(name)
        m = STEM_NUMBER_RE.match(stem)
        if not m:
            continue  # no trailing number -> leave alone (covers, notes, etc.)
        prefix = m.group("prefix")
        num_str = m.group("num")
        if prefix_filter is not None and prefix.lower() != prefix_filter.lower():
            continue
        groups.setdefault((prefix, ext), []).append((name, num_str, int(num_str)))
    return groups


def plan_renames(groups):
    """Build a list of (old_name, new_name) that actually change. Width is the
    larger of (digits needed for the max number) and (longest existing literal),
    so we pad up but never strip an already-wider number."""
    plan = []
    for (prefix, ext), files in groups.items():
        max_num = max(n for _, _, n in files)
        width = max(len(str(max_num)), max(len(s) for _, s, _ in files))
        for name, num_str, num_int in files:
            new_num = str(num_int).zfill(width)
            if new_num == num_str:
                continue  # already correct
            plan.append((name, prefix + new_num + ext))
    return plan


def find_collisions(folder, plan):
    """A target collides if it already exists on disk and is NOT one of the files
    we are about to move away."""
    sources = {old for old, _ in plan}
    collisions = []
    for old, new in plan:
        dest = os.path.join(folder, new)
        if os.path.exists(dest) and new not in sources:
            collisions.append((old, new))
    return collisions


def apply_renames(folder, plan):
    """Two-phase rename through unique temp names to avoid any intermediate clash."""
    temps = []
    for i, (old, new) in enumerate(plan):
        tmp = os.path.join(folder, "__pad_tmp_%d__%s" % (i, new))
        os.rename(os.path.join(folder, old), tmp)
        temps.append((tmp, os.path.join(folder, new)))
    for tmp, final in temps:
        os.rename(tmp, final)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Zero-pad trailing numbers in filenames.")
    ap.add_argument("folder", help="Folder containing the files to renumber.")
    ap.add_argument("--prefix", default=None,
                    help="Only process files whose name-stem prefix matches this "
                         "(e.g. 'Slide'). Default: every numbered series in the folder.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Show what would change without renaming anything.")
    args = ap.parse_args(argv)

    folder = args.folder
    if not os.path.isdir(folder):
        print("ERROR: not a folder: %s" % folder)
        return 1

    groups = scan(folder, args.prefix)
    if not groups:
        print("No numbered files found in: %s" % folder)
        if args.prefix:
            print("(prefix filter was: %s)" % args.prefix)
        return 0

    plan = plan_renames(groups)
    if not plan:
        total = sum(len(v) for v in groups.values())
        print("Nothing to do - all %d numbered file(s) are already padded correctly."
              % total)
        return 0

    collisions = find_collisions(folder, plan)
    if collisions:
        print("ABORTED - target name(s) already exist as different files:")
        for old, new in collisions:
            print("  %s -> %s  (target already exists)" % (old, new))
        print("Resolve the clashes and re-run. Nothing was changed.")
        return 1

    for old, new in plan:
        print("%s -> %s" % (old, new))

    if args.dry_run:
        print("\nDRY RUN - %d file(s) would be renamed. Nothing changed." % len(plan))
        return 0

    apply_renames(folder, plan)
    print("\nDone - renamed %d file(s)." % len(plan))
    return 0


if __name__ == "__main__":
    sys.exit(main())

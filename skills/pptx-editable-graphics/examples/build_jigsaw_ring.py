"""Worked example: concentric three-piece jigsaw, binding ring, outer actor ring.

Built for the AI for Investing webinar, 29 July 2026. Every element is a native
editable PowerPoint shape. Use this as the pattern for any new concentric or
segmented diagram: define a palette dict at the top, lay out radii in inches,
build outermost first so the stacking order comes out right, then add labels.

    python build_jigsaw_ring.py

Adjust PALETTE by running scripts/extract_theme.py against the target deck.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "scripts"))

from ppt_shapes import (deck, rect, donut, block_arc, freeform, textbox,   # noqa: E402
                        polar, ring_rotation, jigsaw_piece, SLIDE_16x9)

# ------------------------------------------------- palette (.ai Webinar) -----
P = {
    "backdrop": "0B1E3B", "gold": "DBA43A", "badge_l": "E39B92",
    "panel": "EDF1F2", "panel_line": "C4CED3", "title": "13294F",
    "data": "13294F", "storage": "B4544A", "wiki": "2E7D32",
    "ring": "DBA43A", "ring_txt": "0B1E3B",
    "out1": "3F4E57", "out2": "55646D", "out3": "6B7A83",
    "white": "FFFFFF",
}

SLIDE_TITLE = "Building a DIY-Investing System (Mick's Suggestion)..."
BADGE_L, BADGE_R = "diy-investors.ai", '"AI for Investing"  (29th July 2026)'
RING_LABEL = "RING LABEL - EDIT ME"

# --------------------------------------------------------------- geometry ----
W, H = SLIDE_16x9
CX, CY = W / 2, 4.48
R_OUT_OUT = 2.52
S = R_OUT_OUT / 2.80                      # one scale factor keeps proportions
R_JIG, R_RING_IN, R_RING_OUT, R_OUT_IN = 1.42 * S, 1.52 * S, 2.14 * S, 2.24 * S

# label, start angle, end angle (maths convention, counter-clockwise), colour, pt
# DATA is deliberately the largest span - ask Mick whether size means volume or
# importance before fixing these.
PIECES = [("DATA", 15.0, 185.0, P["data"], 27),
          ("STORAGE", 185.0, 290.0, P["storage"], 18),
          ("WIKI", 290.0, 375.0, P["wiki"], 18)]
OUTER = [("AI", 90.0, P["out1"]), ("USER", 210.0, P["out2"]),
         ("PLACEHOLDER", 330.0, P["out3"])]
OUTER_SPAN = 115.0                        # 120 less a 5 degree gap

prs, slide = deck(W, H)

# --- house chrome, so the graphic can be judged in context -------------------
rect(slide, 0, 0, W, H, P["backdrop"], P["gold"], 1.5, name="Backdrop")
rect(slide, 0, 0, W, 0.55, P["backdrop"], P["backdrop"], 1.0, name="Top bar")
rect(slide, 0.20, 0.09, 2.95, 0.38, P["backdrop"], P["gold"], 1.0,
     name="Badge left", rounded=True)
rect(slide, 9.35, 0.09, 3.78, 0.38, P["backdrop"], P["gold"], 1.0,
     name="Badge right", rounded=True)
rect(slide, 0.18, 0.66, 12.97, 6.72, P["panel"], P["panel_line"], 1.0,
     name="Content panel", rounded=True)

textbox(slide, BADGE_L, 1.675, 0.28, 2.8, 0.30, 13, P["badge_l"],
        italic=True, name="Badge text left")
textbox(slide, BADGE_R, 11.24, 0.28, 3.6, 0.30, 11, P["white"],
        bold=False, name="Badge text right")
textbox(slide, SLIDE_TITLE, W / 2, 1.28, 12.33, 0.60, 27, P["title"],
        name="Slide title")

# --- outermost first so stacking order comes out right -----------------------
for lbl, theta, colour in OUTER:
    block_arc(slide, CX, CY, R_OUT_IN, R_OUT_OUT, theta, OUTER_SPAN, colour,
              name="Outer ring - %s" % lbl)

donut(slide, CX, CY, R_RING_IN, R_RING_OUT, P["ring"], name="Binding ring")

for lbl, a0, a1, colour, _sz in PIECES:
    freeform(slide, jigsaw_piece(CX, CY, a0, a1, R_JIG), colour,
             P["panel"], 2.25, name="Jigsaw piece - %s" % lbl)

# --- labels last so they sit on top ------------------------------------------
for lbl, a0, a1, _c, size in PIECES:
    x, y = polar(CX, CY, a0 + ((a1 - a0) % 360.0) / 2, 0.58 * R_JIG)
    textbox(slide, lbl, x, y, 1.8, 0.40, size, P["white"],
            name="Label - %s" % lbl, spacing=1.2)

for theta, tag in ((90.0, "top"), (270.0, "bottom")):
    x, y = polar(CX, CY, theta, (R_RING_IN + R_RING_OUT) / 2)
    textbox(slide, RING_LABEL, x, y, 2.1, 0.28, 11, P["ring_txt"],
            name="Ring label %s" % tag, spacing=1.0)

for lbl, theta, _c in OUTER:
    x, y = polar(CX, CY, theta, (R_OUT_IN + R_OUT_OUT) / 2)
    textbox(slide, lbl, x, y, 2.4, 0.32, 15, P["white"],
            rot=ring_rotation(theta), name="Label - %s" % lbl, spacing=1.5)

slide.notes_slide.notes_text_frame.text = (
    "Every element is a native editable PowerPoint shape. To reuse in the live "
    "deck, select the ring, jigsaw and label shapes only (not the chrome) and "
    "paste onto the existing slide. Group each shape with its label before "
    "animating or dragging."
)

out = "2026.07.29 - AI4Inv Core Model Infographic (themed).pptx"
prs.save(out)
print("wrote", out)

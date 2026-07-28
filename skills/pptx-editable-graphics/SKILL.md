---
name: pptx-editable-graphics
description: Builds diagrams and infographics for PowerPoint as fully editable native shapes (freeforms, autoshapes, real text boxes) instead of flat images, and skins them to the correct DIY-Investing house theme by reading the palette straight out of the target deck. Use this skill whenever Mick asks for an infographic, diagram, concept graphic, process flow, cycle, jigsaw, venn, funnel, ring or "picture that explains X" that will end up on a slide. Also triggers on "make that editable", "rebuild the graphic as shapes", "match the deck theme", "brand this diagram", "put it in the .ai Webinar style", or any complaint that a supplied graphic cannot be edited or does not match the slide pack. Do NOT use for photographs, screenshots, charts of real data (use the chart tools) or for building whole decks (use the pptx skill).
---

# PowerPoint Editable Graphics Skill

Mick's standing rule: **any diagram destined for a slide must arrive as native
PowerPoint shapes, never as a PNG**. He needs to drag pieces apart for build
animations, recolour to suit the pack, and retype labels live. A flattened image
fails all three.

This skill is a technique library, not a picture catalogue. It does not know what
diagram to draw - Mick says that. It knows how to draw whatever he says in a way
that stays editable and on-brand.

## The two rules that matter

1. **Editable, always.** Every element is a `p:sp` - freeform, preset autoshape or
   text box. No `addImage`, no rasterising, no SVG import.
2. **Theme comes from the target deck, not from memory.** Read the actual palette
   out of the .pptx Mick is going to paste into. Never guess brand colours and never
   maintain a second copy of them somewhere else.

## Workflow

### Step 1 - Ask before drawing
Infographics are badly underspecified by nature. Before writing any code, confirm:
- What the shapes represent and their relative sizes (does "biggest" mean volume or
  importance? Ask - it changes the design and the message).
- Any labels Mick has not supplied yet - offer a visible placeholder such as
  `PLACEHOLDER` or `RING LABEL - EDIT ME` rather than inventing wording.
- **Which deck it is going into.** This is the question that gets forgotten and it
  is the one that causes a rebuild.

### Step 2 - Extract the theme from the target deck
```
python scripts/extract_theme.py "path/to/live_deck.pptx"
```
Prints the theme colour scheme and fonts, the most-used literal colours across all
slides, and the chrome geometry (top bar, badges, content panel, title block) of the
most representative content slide. Feed those hex values straight into the palette
dict of the build script.

Do NOT stop at `ppt/theme/theme1.xml`. Mick's decks routinely carry the stock Office
2007 scheme in the theme part while the real branding lives in literal `srgbClr`
values on the slides themselves. The script reports both; trust the slide census.

Known house themes already captured are in `references/themes.md`. Re-extract anyway
if the deck has moved on - the reference file is a convenience, the deck is the truth.

### Step 3 - Build
Copy `examples/build_jigsaw_ring.py` as a starting point and import the helpers:

```python
from ppt_shapes import (deck, style, textbox, set_adj, block_arc, donut,
                        freeform, polar, ring_rotation, annulus_sector)
```

Work in inches with a maths-convention polar helper and convert at the last moment.
It keeps the geometry readable and stops sign errors.

### Step 4 - QA (not optional)
```
python scripts/qa_render.py "output.pptx"
```
Validates the package, converts to PDF, renders to JPEG and prints the paths. Look
at the image. The first render nearly always has one real defect.

## Gotchas that have already cost time

These are the specific traps. Every one of them has bitten.

**Theme style refs re-inject drop shadows.** `python-pptx`'s `add_shape` writes a
`<p:style>` block with `effectRef idx="2"`. Setting `shape.shadow.inherit = False`
adds an empty `<a:effectLst/>` but LibreOffice (and some PowerPoint versions) still
honour the style ref, so every shape renders with a shadow. Fix: set `lnRef`,
`fillRef` and `effectRef` idx to `0`. `style()` in the helper library does this.

**Block Arc angles are not maths angles.** OOXML `blockArc` `adj1`/`adj2` are in
60000ths of a degree, measured **clockwise from three o'clock**, and the arc is drawn
clockwise from adj1 to adj2. To place a segment centred on maths angle `theta`
spanning `span`:
```
adj1 = (-(theta + span/2)) % 360 * 60000
adj2 = (-(theta - span/2)) % 360 * 60000
adj3 = (r_out - r_in) / r_out * 100000      # thickness, fraction of radius
```
`adj3` on `donut` is a fraction of the shape **width**, not the radius. Different
denominator, easy to get wrong.

**python-pptx normalises adjustments wrongly for angles.** `shape.adjustments[n]`
divides by 100000, which is right for ratios and wrong for angles. Write the `<a:gd>`
elements directly - `set_adj()` does.

**Curved text is not editable.** WordArt text-on-a-path cannot be produced by
python-pptx and would not be editable anyway. Instead use a normal text box and
rotate it to the tangent. For a label at maths angle `theta` on a ring:
```
rotation = (90 - theta) if sin(theta) >= 0 else (270 - theta)
```
Upper half reads with "up" pointing outward, lower half with "up" pointing inward.
Both come out upright to the viewer. `ring_rotation()` in the helper library.

**Horizontal text does not fit in a ring.** A label at ring mid-radius `r` has only
about `2 * sqrt(r_out^2 - r^2)` of horizontal room. Check it before choosing a font
size, or rotate the box per above.

**Freeform vertex count.** Roughly one vertex per 2 degrees of arc and about 28 for
a knob gives a smooth curve without producing a shape that is miserable to edit.

**Interlocking jigsaw boundaries.** Define the boundary path once as a function of
angle with the knob always bulging toward increasing angle, then have each piece
traverse its start boundary outward and its end boundary reversed. Every piece
automatically gets exactly one tab and one matching socket, and neighbours always
mesh. Do not try to draw tabs and sockets separately.

**Labels do not follow shapes.** Text boxes are separate objects. Tell Mick to group
each shape with its label (Ctrl+G) before he animates or drags anything.

**Name every shape.** Set `cNvPr/@name` to something meaningful. Mick works in the
Selection Pane and "Freeform 7" is useless to him.

## Output conventions

- File naming `YYYY.MM.DD - Title.pptx`, dots, date first, no exception.
- 16:9 unless told otherwise (13.333 x 7.5 inches).
- Deliver the graphic on a slide that reproduces the target deck's chrome, so Mick
  can see it in context. He can copy just the graphic shapes across.
- Save to `/mnt/user-data/outputs/`, deliver with the file tool, and also write it
  into the project folder the deck lives in.
- Log the create/update to the changelog.
- If Mick also wants a PNG, produce it **in addition to** the editable version,
  never instead of it.

## Files

| Path | What it is |
|---|---|
| `scripts/ppt_shapes.py` | Helper library - deck setup, style/shadow fix, freeforms, block arcs, donuts, rotated text, polar maths |
| `scripts/extract_theme.py` | Reads palette, fonts and chrome geometry out of a target .pptx |
| `scripts/qa_render.py` | Validate, convert to PDF, render JPEGs for visual inspection |
| `references/themes.md` | House themes already captured (.ai Webinar and others as they are done) |
| `examples/build_jigsaw_ring.py` | Worked example - concentric three-piece jigsaw with binding ring and outer actor ring |

## Dependencies
`python-pptx`, `Pillow`, LibreOffice (via the pptx skill's `scripts/office/soffice.py`),
`pdftoppm`. The pptx skill's `validate.py` is used by `qa_render.py` when present.

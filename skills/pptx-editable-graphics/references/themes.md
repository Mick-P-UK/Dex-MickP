# House themes for slide graphics

Captured by running `scripts/extract_theme.py` against the live deck. Treat this
file as a convenience only. The deck is always the source of truth - re-extract
before building, because Mick revises the packs.

Note: all three packs carry the STOCK Office 2007 colour scheme in
`ppt/theme/theme1.xml` (4F81BD / C0504D / 9BBB59). Ignore it. The branding is in
literal srgbClr values on the slides.

---

## .ai Webinar (AI for Investing, diy-investors.ai)

Extracted 2026.07.28 from
`2026.07.27 - AI-4-Inv_Webinar_for_29th July 2026__v1.03.pptx` (slide 16 pattern).

Dark navy surround, gold brand furniture, light content panel. Despite being the
"dark tech" pack, the CONTENT sits on a light panel - Mick's standing preference
for light themes holds inside the dark frame. Do not build a dark-background
graphic for this pack.

### Palette

| Role | Hex |
|---|---|
| Backdrop / top bar navy | `0B1E3B` |
| Panel title navy | `13294F` |
| Brand gold (badges, borders, accents) | `DBA43A` |
| Left badge text (salmon) | `E39B92` |
| Content panel fill | `EDF1F2` |
| Content panel border | `C4CED3` |
| Card fill / card border | `FFFFFF` / `DCE3E7` |
| Body text | `1A1A1A` |
| House green (positive, recommended) | `2E7D32` |
| Green card fill | `EAF3EC` |
| House blue (headers) | `2E4ED1` |
| Slate family | `9AA6AD`, `C4CED3`, `DCE3E7` |
| Font | Calibri throughout |

### Derived tones for graphics
Not in the deck, but derived from it and used on the Core Model infographic so
the graphic reads as part of the pack:

| Role | Hex | Derivation |
|---|---|---|
| Rose / warm piece | `B4544A` | `E39B92` darkened for white text |
| Outer ring dark | `3F4E57` | `9AA6AD` family, darkened |
| Outer ring mid | `55646D` | " |
| Outer ring light | `6B7A83` | " (white bold text is ~4:1 here - do not go lighter) |

### Chrome geometry (inches: x, y, w, h)

| Element | Shape | Box | Fill / line |
|---|---|---|---|
| Top bar | rect | 0, 0, 13.33, 0.55 | `0B1E3B` |
| Left badge | roundRect | 0.20, 0.09, 2.95, 0.38 | `0B1E3B` fill, `DBA43A` 1pt line, text `E39B92` bold italic 13pt |
| Right badge | roundRect | 9.35, 0.09, 3.78, 0.38 | `0B1E3B` fill, `DBA43A` 1pt line, text white 11pt |
| Content panel | roundRect | 0.18, 0.66, 12.97, 6.72 | `EDF1F2` fill, `C4CED3` 1pt line |
| Panel title | text | 0.50, 0.86, 12.33, 0.85 | `13294F`, bold, centred, 27-30pt |
| Content card | roundRect | varies | `FFFFFF` fill, `DCE3E7` 1pt line |
| Card header bar | roundRect | varies | `0B1E3B` fill, white bold text |
| Highlight card | roundRect | varies | `EAF3EC` fill, `2E7D32` 1.25pt line |

Usable area for a centred circular graphic under the title: roughly y 1.95 to
7.05, so a maximum outer radius of about 2.5 inches centred at (6.667, 4.48).

---

## Inner Circle (data / charts, print-friendly)

Not yet extracted. TODO task-20260728-001 in 03-Tasks/Tasks.md, medium priority.
Run `extract_theme.py` against the current Inner Circle deck before building
anything for it, and record the result here in the same depth as the .ai Webinar
section above.

## Portico Plaza (webinars)

Not yet extracted. TODO task-20260728-002 in 03-Tasks/Tasks.md, medium priority.
Same instruction as above.

## Boot Camp (educational, print-friendly)

Deferred. Mick's decision 2026.07.28: Boot Camp is an annual event, so capturing
its theme waits until next year. Do not raise it as an outstanding item before
then.

---

Reminder: Inner Circle, Portico Plaza and Boot Camp all belong to DIY Investing
(diy-investors.com), a separate business line from AI for Investing
(diy-investors.ai). Do not mix the packs.

Both outstanding packs are print-friendly, so expect lighter backgrounds than
the .ai Webinar pack. Check the contrast of any white label text before reusing
the .ai Webinar approach wholesale.

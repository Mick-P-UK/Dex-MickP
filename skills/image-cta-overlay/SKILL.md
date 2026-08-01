---
name: image-cta-overlay
description: Add a diagonal "Click here for Report" (or custom) call-to-action text overlay to an image thumbnail, either as plain text or on an angled coloured band. Use this skill whenever Mick asks to add a CTA, overlay text, "click here" label, or watermark-style text diagonally across an image - e.g. for webinar recordings, report thumbnails, YouTube cards, or any image that needs a clickable-looking overlay. Triggers include "add click here text", "overlay text on image", "add CTA to thumbnail", "add diagonal text to image", "add a banner/band CTA", "make it look clickable", or any request to stamp text across a thumbnail image.
version: 2.0
updated: 2026.07.31
---

# Image CTA Overlay Skill

Adds a diagonal call-to-action overlay to an image thumbnail. Built for DIY Investors
thumbnails - report covers, webinar cards, YouTube covers - but works on any image.

Two styles are available:

1. **Plain text** (original default) - text with a drop shadow, no background.
2. **Banded** (house style for dark slides) - the text sits on a narrow angled
   rectangular band. Reads as a button/sticker rather than a watermark.

## Choosing the style

| Situation | Style |
|-----------|-------|
| diy-investors.ai MONTHLY WEBINAR thumbnail | **Banded, light grey band + bright green text** (Mick's confirmed house style) |
| Any slide with a DARK BLUE / dark tech background (.ai Webinar template) | **Banded, light grey band + bright green text** |
| Light or busy background, quick watermark | Plain text, red |
| Anything else / unsure | Ask, but default to plain text red |

### House CTA preset (dark blue webinar slides)
- Band fill: light grey `(224, 224, 224)`, alpha `240`
- Band border: mid grey `(90, 90, 90)`, 3px
- Text: bright green `(0, 255, 0)` with a 3px dark outline `(20, 20, 20)`
  (the outline is REQUIRED - bright green on light grey is low contrast without it)
- Soft black drop shadow behind the whole band (offset +6px, Gaussian blur radius 7)
- Angle: corner-to-corner, `atan2(height, width)`
- Font size 64 on a 1366x769 thumbnail

A charcoal band `(55, 55, 55)` with a light border was trialled as an alternative.
Mick chose light grey. Keep charcoal only as an explicit override.

## Default behaviour (plain style)
- Text: **"Click here for Report"** (override if user specifies different text)
- Colour: **Red** `(220, 0, 0)`
- Angle: **Natural diagonal** - `atan2(height, width)`, spans corner to corner at any aspect ratio
- Font size: **52px** - scale up for large images
- Shadow: black semi-transparent, offset `(+2, +2)`
- Output: PNG at `/mnt/user-data/outputs/YYYY.MM.DD - [original_stem]_CTA.png`

## Input
- One image file (JPG or PNG) - uploaded directly or at a path under the uploads folder
- Optional overrides: custom text, font size, text colour, band on/off, band colour

## Steps

### 1. Locate the image
Check the uploads folder for the file. Use the most recently uploaded image if not specified.

### 2. Run the overlay script

```python
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os
from datetime import date

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]

def _load_font(size):
    for fp in FONT_CANDIDATES:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()

def add_cta_overlay(
    input_path,
    output_path,
    text="Click here for Report",
    font_size=52,
    text_colour=(220, 0, 0),
    shadow_colour=(0, 0, 0, 180),
    # --- band options ---
    band=False,                      # True = draw the angled rectangle behind the text
    band_colour=(224, 224, 224),     # light grey house preset
    band_alpha=240,                  # 255 = solid; ~180 lets the slide ghost through
    band_border=(90, 90, 90),
    text_outline=(20, 20, 20),       # keeps bright green legible on light grey
    outline_width=3,
    pad_x=48,
    pad_y=26,
):
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size
    font = _load_font(font_size)

    dummy = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bbox = dummy.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    angle = math.degrees(math.atan2(h, w))   # corner-to-corner

    if not band:
        pad = 20
        layer = Image.new("RGBA", (text_w + pad * 2, text_h + pad * 2), (255, 255, 255, 0))
        d = ImageDraw.Draw(layer)
        d.text((pad + 2, pad + 2), text, font=font, fill=shadow_colour)
        d.text((pad, pad), text, font=font, fill=(*text_colour, 255))
    else:
        bw, bh = text_w + pad_x * 2, text_h + pad_y * 2
        margin = 30                                    # room for shadow and rotation
        layer = Image.new("RGBA", (bw + margin * 2, bh + margin * 2), (0, 0, 0, 0))

        # soft drop shadow behind the whole band
        sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rectangle(
            [margin + 6, margin + 6, margin + bw + 6, margin + bh + 6], fill=(0, 0, 0, 140)
        )
        layer = Image.alpha_composite(layer, sh.filter(ImageFilter.GaussianBlur(7)))

        d = ImageDraw.Draw(layer)
        d.rectangle(
            [margin, margin, margin + bw, margin + bh],
            fill=(*band_colour, band_alpha),
            outline=(*band_border, 255),
            width=3,
        )
        d.text(
            (margin + pad_x - bbox[0], margin + pad_y - bbox[1]),
            text, font=font, fill=(*text_colour, 255),
            stroke_width=outline_width, stroke_fill=(*text_outline, 255),
        )

    rotated = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    rw, rh = rotated.size
    img.paste(rotated, ((w - rw) // 2, (h - rh) // 2), rotated)
    img.convert("RGB").save(output_path, "PNG")
    return output_path


# House preset - one-liner for the monthly webinar thumbnail
def add_webinar_cta(input_path, output_path, text="Click HERE for PowerPoint PDF.",
                    font_size=64):
    return add_cta_overlay(
        input_path, output_path, text=text, font_size=font_size,
        text_colour=(0, 255, 0), band=True,
        band_colour=(224, 224, 224), band_alpha=240,
    )
```

### 3. Name the output file
```
/mnt/user-data/outputs/YYYY.MM.DD - [original_stem]_CTA.png
```
Date computed with `datetime.date.today()` - never hardcoded.

### 4. Present the file
Deliver the PNG to Mick immediately so he can download it.

### 5. Check the result before delivering
Open the output and look at it. The band WILL cover part of the slide. If it hides
the title line, the date, or the presenter credit, say so and offer:
- smaller font (approx 52) with the band shifted down-left across the photo and empty space
- `band_alpha` around 180 so the title ghosts through
- keep as is if the hidden text is not important

## Font size guidance
| Image width | Plain text | Banded |
|-------------|-----------|--------|
| < 500px     | 36        | 32     |
| 500-900px   | 52        | 48     |
| 900-1500px  | 72        | 64     |
| > 1500px    | 96+       | 84+    |

Banded sizes run slightly smaller because the band adds visual weight.

## Common overrides
- Monthly webinar PDF link: `add_webinar_cta(..., text="Click HERE for PowerPoint PDF.")`
- Webinar recording: `text="Watch Recording"`
- YouTube card: `text="Watch on YouTube"`, font_size 72 plain / 64 banded
- Report link: plain defaults
- Custom colour: `text_colour=(R, G, B)`
- Charcoal band variant: `band_colour=(55, 55, 55)`, `band_border=(200, 200, 200)`,
  `text_outline=(0, 0, 0)`

## Standing rules
- UK English in all commentary
- ASCII only in any file written to the vault
- Use `--break-system-packages` with pip if Pillow needs installing
- Always output PNG regardless of input format (avoids JPEG artefacts on text)
- Never hardcode dates - compute with `datetime.date.today()`
- Plain-style shadow offset is always `(+2, +2)`

## Learning log
| Date       | Learning |
|------------|----------|
| 2026.04.23 | Skill created from live session. Image 745x557px; 52px font at 36.8deg worked well. Shadow alpha 180 legible over both light header and dark body. |
| 2026.07.31 | Banded style added (v2.0). 1366x769 webinar thumbnail, dark blue .ai Webinar background, 29.4deg diagonal. Plain bright green text read as a watermark; the band made it read as a button. Mick compared light grey vs charcoal and chose LIGHT GREY as the standing option for monthly webinar thumbnails and any dark blue slide. Bright green on light grey needs the 3px dark text outline or the letters mush. 64px font, band padding 48x26. NOTE: this skill had never been written to the vault before today - it existed only in the Cowork skill store. |

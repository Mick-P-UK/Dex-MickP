---
name: yt-play-button-overlay
description: Adds a play button overlay to the centre (or a corner) of any image thumbnail, in one of three selectable styles - YouTube (dark disc, red ring, white arrow), Clean (white disc, black arrow, for warm or busy centres where a red ring would not stand out), or Minimal (dark disc, white arrow, no ring). Use this skill whenever Mick uploads an image and asks for a play button, video symbol, "make it look clickable", or circle-with-triangle overlay - for YouTube thumbnails, the DIY Investors newsletter, WordPress posts, or any content that should indicate a video link. Handles JPG and PNG input. Always use this skill rather than writing ad-hoc image code.
---

# Play Button Overlay Skill

Adds a professional play button to an image so it reads as a clickable video link.
Consolidated 2026.07.08 from the two earlier skills (thumbnail-play-button and the
original yt-play-button-overlay), which had drifted apart. This is now the single
canonical play-button skill.

## Styles

Pick the style with the `style` argument. If Mick does not specify one, choose sensibly:
default to `youtube`, but switch to `clean` when the centre of the image is a warm,
mid-toned or busy colour (orange, brown, red, tan) where a red ring would not stand out.

| style | Look | Best for |
|-------|------|----------|
| youtube | Dark semi-transparent disc, red ring, white arrow | Classic YouTube thumbnails on darker or high-contrast backgrounds |
| clean | White disc, thin grey ring, black arrow, soft drop shadow | Warm or busy centres (orange/brown/red) where a red ring would vanish. High contrast, very clear. |
| minimal | Dark semi-transparent disc, white arrow, no ring | Understated, non-branded video hint |

## Inputs

- One uploaded image (JPG or PNG) at `/mnt/user-data/uploads/`
- Optional: `style` (youtube / clean / minimal), `size` (small / medium / large),
  `position` (centre / bottom-right), `fmt` (png / jpg)

## Defaults

- style: youtube (auto-switch to clean for warm/busy centres - see above)
- size: medium (radius = 13.5 percent of the shorter image side)
- position: centre
- fmt: png (crisp edges on the ring and arrow; use jpg only if a JPG is specifically needed)

---

## Workflow

### Step 1 - Confirm the image
Check the uploaded image is at `/mnt/user-data/uploads/`. If none is present, ask Mick to upload one.

### Step 2 - Run the implementation
Use this exact implementation. It supersamples at 4x then downsamples with LANCZOS for
smooth, anti-aliased edges. Do not rewrite from scratch.

```python
from PIL import Image, ImageDraw
from datetime import datetime, timezone, timedelta
import os

STYLES = {
    "youtube": {"disc": (0, 0, 0, 160),     "ring": (255, 0, 0, 230), "ring_w": 0.08, "arrow": (255, 255, 255, 240), "shadow": False},
    "clean":   {"disc": (255, 255, 255, 235),"ring": (90, 90, 90, 200), "ring_w": 0.03, "arrow": (15, 15, 15, 255),   "shadow": True},
    "minimal": {"disc": (0, 0, 0, 160),     "ring": None,              "ring_w": 0.0,  "arrow": (255, 255, 255, 235), "shadow": False},
}
SIZES = {"small": 0.09, "medium": 0.135, "large": 0.18}
SS = 4  # supersample factor

def add_play_button(input_path, style="youtube", size="medium",
                    position="centre", fmt="png", output_filename=None):
    st = STYLES[style]
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size

    R = int(min(w, h) * SIZES[size])
    if position == "bottom-right":
        cx, cy = int(w * 0.78), int(h * 0.72)
    else:  # centre
        cx, cy = w // 2, h // 2

    # Supersampled transparent layer
    layer = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    CX, CY, RR = cx * SS, cy * SS, R * SS

    # Optional soft drop shadow (offset dark disc)
    if st["shadow"]:
        off = int(RR * 0.05)
        d.ellipse([CX - RR + off, CY - RR + off, CX + RR + off, CY + RR + off], fill=(0, 0, 0, 90))

    # Disc
    d.ellipse([CX - RR, CY - RR, CX + RR, CY + RR], fill=st["disc"])

    # Ring (optional)
    if st["ring"] is not None and st["ring_w"] > 0:
        rw = max(1, int(RR * st["ring_w"]))
        d.ellipse([CX - RR, CY - RR, CX + RR, CY + RR], outline=st["ring"], width=rw)

    # Play triangle, nudged right so it looks optically centred
    tri = RR * 0.55
    nudge = int(RR * 0.10)
    pts = [
        (CX - tri * 0.75 + nudge, CY - tri),
        (CX - tri * 0.75 + nudge, CY + tri),
        (CX + tri + nudge,        CY),
    ]
    d.polygon(pts, fill=st["arrow"])

    # Downsample and composite
    layer = layer.resize((w, h), Image.LANCZOS)
    out = Image.alpha_composite(img, layer).convert("RGB")

    # Dated filename (London time)
    if output_filename is None:
        utc = datetime.now(timezone.utc)
        bst = 4 <= utc.month <= 10
        london = utc.astimezone(timezone(timedelta(hours=1 if bst else 0)))
        date_str = london.strftime("%Y.%m.%d")
        base = os.path.splitext(os.path.basename(input_path))[0]
        ext = "png" if fmt == "png" else "jpg"
        output_filename = f"{date_str} - {base}-Play.{ext}"

    out_path = f"/mnt/user-data/outputs/{output_filename}"
    if fmt == "png":
        out.save(out_path, "PNG")
    else:
        out.save(out_path, quality=95)
    return out_path
```

### Step 3 - Present the file
Call `present_files` with the returned path so Mick can download it. One-line confirmation.

---

## Variations quick reference

| Mick asks for | Argument |
|---|---|
| Standard YouTube thumbnail | style="youtube" (default) |
| Clear button on an orange/brown/busy image | style="clean" |
| Subtle / understated | style="minimal" |
| Smaller / larger button | size="small" / size="large" |
| Corner instead of centre | position="bottom-right" |
| JPG output | fmt="jpg" |

## Standing rules
- Pillow must be available: `pip install Pillow --break-system-packages`
- Output PNG by default (best edge quality); JPG only when specifically required
- Never hardcode dates - compute London time as above
- Triangle is always nudged right for optical centring

## Notes and learning log
| Date | Note |
|------|------|
| 2026.02.26 | Original thumbnail-play-button created (YouTube style, red ring). |
| 2026.04.16 | Original yt-play-button-overlay created (dark disc, white arrow). First use: RPI newsletter thumbnail. |
| 2026.07.08 | Consolidated both into this single skill. Added supersampled anti-aliasing, selectable styles (youtube / clean / minimal), size and position options. Clean style validated live on a warm-toned 1690x870 thumbnail (white disc, black arrow) - approved by Mick. thumbnail-play-button moved to _deprecated. |

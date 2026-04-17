---
name: yt-play-button-overlay
description: Adds a YouTube-style play button (semi-transparent dark circle with white triangle) to the centre of a thumbnail image. Use this skill whenever Mick uploads a YouTube thumbnail and asks for a play button, video symbol, or circle-with-triangle overlay to be added -- for example when preparing thumbnails for the DIY Investors newsletter. Handles JPG and PNG input, outputs a high-quality JPG. Always use this skill rather than writing ad-hoc image processing code.
---

# YouTube Play Button Overlay Skill

**Purpose:** Add a centred YouTube-style play button to a thumbnail image. Used whenever a newsletter or other content requires a thumbnail to visually indicate it is a video link.

---

## What This Skill Does

1. Loads the uploaded thumbnail (JPG or PNG)
2. Draws a semi-transparent dark circle in the centre
3. Draws a white triangle (play icon) inside the circle, slightly right-offset for visual balance
4. Saves the result as a high-quality JPG
5. Moves the output to `/mnt/user-data/outputs/` with a `YYYY.MM.DD -` prefixed filename
6. Presents the file to Mick using `present_files`

---

## Standard Parameters

These defaults produce a clean, professional result and should be used unless Mick requests a variation:

| Parameter | Default | Notes |
|-----------|---------|-------|
| Circle radius | 1/6 of shorter image dimension | Scales correctly for any thumbnail size |
| Circle fill | `(0, 0, 0, 160)` | Semi-transparent black (alpha 160/255) |
| Triangle fill | `(255, 255, 255, 230)` | Near-opaque white |
| Triangle right-offset | 12% of circle radius | Corrects visual centering of play icon |
| Triangle size | 50% of circle radius | Proportional to circle |
| Output quality | 95 | High quality JPEG |

---

## Python Implementation

Always use this exact implementation. Do not rewrite from scratch.

```python
from PIL import Image, ImageDraw
from datetime import datetime, timezone, timedelta
import os

def add_play_button(input_path, output_filename=None):
    # Load image
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size

    # Overlay layer
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Dimensions
    cx, cy = w // 2, h // 2
    circle_r = min(w, h) // 6

    # Circle
    draw.ellipse(
        [cx - circle_r, cy - circle_r, cx + circle_r, cy + circle_r],
        fill=(0, 0, 0, 160)
    )

    # Triangle (right-offset for visual balance)
    t_offset = circle_r * 0.12
    t_size = circle_r * 0.5
    points = [
        (cx - t_size * 0.6 + t_offset, cy - t_size),
        (cx - t_size * 0.6 + t_offset, cy + t_size),
        (cx + t_size * 0.9 + t_offset, cy),
    ]
    draw.polygon(points, fill=(255, 255, 255, 230))

    # Composite and save
    result = Image.alpha_composite(img, overlay).convert("RGB")

    if output_filename is None:
        # Generate dated filename
        utc_now = datetime.now(timezone.utc)
        bst_active = 4 <= utc_now.month <= 10
        offset = timedelta(hours=1) if bst_active else timedelta(hours=0)
        london_now = utc_now.astimezone(timezone(offset))
        date_str = london_now.strftime("%Y.%m.%d")
        base = os.path.splitext(os.path.basename(input_path))[0]
        output_filename = f"{date_str} - {base}-Play.jpg"

    out_path = f"/mnt/user-data/outputs/{output_filename}"
    result.save(out_path, quality=95)
    return out_path
```

---

## Execution Steps

1. **Identify the uploaded image path** -- check `/mnt/user-data/uploads/` for the thumbnail file
2. **Run the Python implementation** using `bash_tool` with a heredoc
3. **Confirm output saved** to `/mnt/user-data/outputs/` with correct `YYYY.MM.DD -` prefix
4. **Call `present_files`** with the output path so Mick can download it
5. **Brief confirmation** -- one sentence, e.g. "Play button added and centred -- here's your newsletter-ready thumbnail."

---

## Output Naming Convention

`YYYY.MM.DD - [original-filename]-Play.jpg`

Example: `2026.04.16 - RPI-YT-Video-Thumbnail-Play.jpg`

---

## Notes & Learning Log

| Date | Note |
|------|------|
| 2026.04.16 | Skill created. First use: RPI video thumbnail for DIY Investors newsletter. Default parameters validated -- result approved by Mick. |

---

## Edge Cases

- **PNG input**: Convert to RGBA before compositing, then save as RGB JPEG -- handled by default implementation
- **Very small images**: Circle radius scales automatically via `min(w, h) // 6` -- no special handling needed
- **Already has play button**: Not detectable programmatically -- Mick will not upload duplicates, but if uncertain, ask before processing
- **Custom size requested**: Adjust `circle_r` multiplier (e.g. `// 5` for larger, `// 8` for smaller)

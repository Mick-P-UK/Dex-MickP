---
name: thumbnail-play-button
description: Add a YouTube-style play button overlay to any image thumbnail. Use this skill whenever the user uploads an image and wants to make it look like a clickable video link - for newsletters, websites, WordPress posts, or any document where a thumbnail should indicate a video. Triggers include "add a play button", "make this look clickable", "add a video overlay", "YouTube style", or any request to overlay a play button on a thumbnail image.
---

# Thumbnail Play Button Skill

Adds a professional YouTube-style play button overlay to an image, making it suitable for use as a clickable video thumbnail in newsletters, websites, or documents.

## Output

A new JPG image with:
- Semi-transparent dark circle centred on the image
- Red outline ring (YouTube style)
- White triangular play arrow

## Inputs

- One uploaded image (JPG or PNG)
- Optionally: size preference (small / medium / large), position (centre / bottom-right)

## Defaults

- Size: medium (13% of image height as radius)
- Position: centre
- Style: YouTube (dark circle, red outline, white arrow)

---

## Workflow

### Step 1 - Confirm the image

Check the uploaded image is accessible at `/mnt/user-data/uploads/`. If no image is present, ask the user to upload one.

### Step 2 - Run the overlay script

```python
from PIL import Image, ImageDraw

img = Image.open("/mnt/user-data/uploads/[FILENAME]").convert("RGBA")
w, h = img.size

overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Size control: adjust multiplier for small (0.09), medium (0.13), large (0.18)
radius = int(h * 0.13)
cx, cy = w // 2, h // 2  # centre position

# Dark semi-transparent circle background
draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius], fill=(0, 0, 0, 160))

# Red YouTube-style outline ring
stroke = int(radius * 0.08)
draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius], outline=(255, 0, 0, 230), width=stroke)

# White play triangle (offset slightly right for optical balance)
tri_size = int(radius * 0.55)
tx = cx + int(radius * 0.1)
ty = cy
triangle = [
    (tx - int(tri_size * 0.5), ty - int(tri_size * 0.85)),
    (tx - int(tri_size * 0.5), ty + int(tri_size * 0.85)),
    (tx + int(tri_size * 0.9), ty)
]
draw.polygon(triangle, fill=(255, 255, 255, 240))

result = Image.alpha_composite(img, overlay).convert("RGB")
result.save("/mnt/user-data/outputs/[OUTPUT_FILENAME].jpg", quality=95)
```

### Step 3 - Name the output file

Follow Mick's YYYY.MM.DD naming convention:
`YYYY.MM.DD_[descriptive-name]_PlayBtn.jpg`

### Step 4 - Present the file

Use `present_files` to share the result with the user.

---

## Variations

| User request | Change to make |
|---|---|
| Smaller button | radius multiplier: 0.09 |
| Larger button | radius multiplier: 0.18 |
| Subtle / understated | Reduce circle fill alpha from 160 to 100, outline alpha from 230 to 150 |
| Bottom-right position | cx = int(w * 0.78), cy = int(h * 0.72) |
| White outline instead of red | outline=(255, 255, 255, 230) |

---

## Notes

- Pillow must be available: `pip install Pillow --break-system-packages`
- Works on any standard JPG or PNG image
- Output is always JPG at 95% quality
- Typical use: newsletter YouTube thumbnails, WordPress post images, webinar landing pages
- Created: 2026.02.26 from proven workflow (DIY Investors Newsletter session)

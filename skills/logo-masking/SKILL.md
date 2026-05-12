# Logo Masking Skill

Remove watermarks, branding logos, or copyright marks from PNG and JPG images by
painting a colour-matched rectangle over the target area. Designed primarily for
NotebookLM infographics but works on any image with a logo in a fixed corner.

## Trigger Phrases

Use this skill when Mick says any of the following:
- "mask the logo", "remove the NotebookLM logo", "remove the branding"
- "clean up this slide", "strip the watermark"
- "logo masking", "run logo-masking"
- "mask the bottom-right corner"
- Uploads a PNG or JPG and asks to remove any visible branding/logo

## What This Skill Does

1. Opens the source image (PNG or JPG)
2. Auto-samples the background colour near the logo (eyedropper approach)
3. Paints a colour-matched rectangle over the logo area - invisible seam
4. Saves the cleaned image with a new filename (removes "_Unformatted" / "_Unedited",
   or appends "_clean" if no such suffix exists)
5. Verifies the result by displaying the output image

## Key Design Decisions (Do Not Change Without Testing)

- **Mask size**: 380px wide x 70px tall - covers full NotebookLM logo at 2752x1536
- **Sample point**: 300px left of right edge, 30px from bottom - reliably lands on
  background, not on the logo itself
- **Colour consistency check**: samples 4 nearby pixels to confirm background is uniform
- **Output format**: same as input (PNG stays PNG, JPG stays JPG)
- **Logo position**: bottom-right corner (default) - adjustable via parameters below

## Workflow

### Step 1 - Identify the source file

Ask Mick for the full file path if not already provided.
Accepted formats: .png, .jpg, .jpeg

### Step 2 - Determine output filename

Apply this naming logic (in order):
1. If filename contains "_Unformatted" -> remove it
2. If filename contains "_Unedited" -> remove it
3. Otherwise -> append "_clean" before the extension

Examples:
- "2026.04.29 - AI-Leverage_Unformatted.png" -> "2026.04.29 - AI-Leverage.png"
- "2026.04.29 - Infographic_01_Unedited.png" -> "2026.04.29 - Infographic_01.png"
- "slide_deck.png" -> "slide_deck_clean.png"

Save to the same folder as the source file.

### Step 3 - Run the masking script

Use this exact Python template in bash:

```python
from PIL import Image, ImageDraw
import os

src = "/path/to/source/image.png"
dst = "/path/to/output/image.png"

img = Image.open(src).convert("RGB")
W, H = img.size
print(f"Image size: {W}x{H}")

# --- Sample background colour ---
sample_x = W - 300
sample_y = H - 30
r, g, b = img.getpixel((sample_x, sample_y))
print(f"Sampled colour: R={r} G={g} B={b}  #{r:02x}{g:02x}{b:02x}")

# Nearby consistency check
for ox, oy in [(-60, 0), (0, -15), (60, 0), (0, -30)]:
    px = img.getpixel((sample_x + ox, sample_y + oy))
    print(f"  nearby: {px}  #{px[0]:02x}{px[1]:02x}{px[2]:02x}")

# --- Apply mask ---
bg_color = (r, g, b)
draw = ImageDraw.Draw(img)
draw.rectangle([W - 380, H - 70, W, H], fill=bg_color)

img.save(dst)
print(f"Saved: {dst}")
```

**Path translation for bash** (Cowork mounted paths):
- Map the Windows path to its /sessions/awesome-busy-meitner/mnt/ equivalent
- The Infographics folder mounts as: /sessions/awesome-busy-meitner/mnt/Infographics/
- AI_Report_Templates mounts as: /sessions/awesome-busy-meitner/mnt/AI_Report_Templates/

### Step 4 - Verify

Use the Read tool on the Windows output path to display the cleaned image inline.
Confirm the logo area is invisible (no visible seam or colour mismatch).

### Step 5 - Report to Mick

State:
- Output filename and location
- Sampled background colour (hex)
- Whether the mask was clean (verified visually)

---

## Adjusting for Different Logo Positions

If the logo is NOT in the bottom-right corner, adjust the sample point and rectangle:

| Position    | Sample point              | Rectangle                          |
|-------------|---------------------------|------------------------------------|
| Bottom-right (default) | (W-300, H-30) | [W-380, H-70, W, H]   |
| Bottom-left | (300, H-30)               | [0, H-70, 380, H]                  |
| Top-right   | (W-300, 30)               | [W-380, 0, W, 70]                  |
| Top-left    | (300, 30)                 | [0, 0, 380, 70]                    |

If the background is not uniform (e.g. logo sits on patterned area), expand
the sample to an average of a 10x10 pixel block:

```python
region = img.crop((sample_x - 5, sample_y - 5, sample_x + 5, sample_y + 5))
avg = region.resize((1, 1), Image.LANCZOS).getpixel((0, 0))
bg_color = avg[:3]
```

---

## Batch Processing

If Mick provides multiple files in the same folder, process them in a loop:

```python
import os
from PIL import Image, ImageDraw

folder = "/sessions/awesome-busy-meitner/mnt/Infographics/"
files = [f for f in os.listdir(folder)
         if f.lower().endswith(('.png', '.jpg', '.jpeg'))
         and ('Unformatted' in f or 'Unedited' in f)]

for fname in files:
    src = os.path.join(folder, fname)
    dst = src.replace('_Unformatted', '').replace('_Unedited', '')
    img = Image.open(src).convert("RGB")
    W, H = img.size
    r, g, b = img.getpixel((W - 300, H - 30))
    draw = ImageDraw.Draw(img)
    draw.rectangle([W - 380, H - 70, W, H], fill=(r, g, b))
    img.save(dst)
    print(f"Done: {os.path.basename(dst)}  bg=#{r:02x}{g:02x}{b:02x}")
```

---

## Requirements

- Python 3 with Pillow (pre-installed in Cowork bash sandbox)
- Source image must be accessible via a mounted Cowork folder
- If folder not yet mounted, use request_cowork_directory first

---

## Verified Specifications

- Tested on NotebookLM infographics at 2752x1536 resolution
- Works on both PNG and JPG inputs
- Background colour sampling is reliable for uniform/near-uniform backgrounds
- Mask size (380x70px) covers the full NotebookLM logo with margin to spare
- Zero visible seam on light backgrounds (white, grey, cream, pastel)

## Status

Version: 1.0
Status: Production Ready
Tested: 2026.04.29 on 2x NotebookLM infographics (2752x1536 PNG)
Quality: Seamless - no visible mask edge on either test image

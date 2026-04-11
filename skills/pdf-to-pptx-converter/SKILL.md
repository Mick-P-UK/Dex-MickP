---
name: pdf-to-pptx-converter
description: Convert PDF slide decks (like NotebookLM PDF slide deck presentations) into branded PowerPoint presentations with DIY Investors branding and automatic logo masking.
---

# PDF to PPTX Converter

Convert PDF slide decks (like NotebookLM presentations) into branded PowerPoint presentations with DIY Investors branding and automatic logo masking.

## When to use

Use this skill for ANY request involving:
- "Convert this PDF to PowerPoint"
- "Turn this PDF slide deck into a presentation"
- "Make a PowerPoint from this PDF"
- User uploads a PDF that appears to be a slide deck
- Any mention of converting PDFs to PPTX with branding

## What this skill does

This skill transforms PDF slide decks into professional PowerPoint presentations by:

1. **Extracting PDF pages** as high-quality images (200 DPI)
2. **Adding DIY Investors branding** - compact header with logo and event banner
3. **Stretching images** to fill slides edge-to-edge (no white borders)
4. **Masking unwanted logos** (like NotebookLM) with invisible, colour-matched rectangles
5. **Detecting background colours** by sampling the EXACT bottom-right corner of each slide image
6. **Avoiding text collision** to ensure slide content remains visible

## Instructions

### Step 1: Copy the conversion script to Claude's working directory

The script is stored persistently in the vault. Copy it before running:

```bash
cp "C:/Vaults/Mick's-Dex-2nd-Brain/Dex-MickP/skills/pdf-to-pptx-converter/pdf_to_pptx.py" /home/claude/pdf_to_pptx.py
```

If the vault path is not accessible (e.g. running in claude.ai Web without Filesystem MCP), recreate the script
from the embedded source in this SKILL.md (see bottom of file).

### Step 2: Execute the conversion

```bash
python3 /home/claude/pdf_to_pptx.py \
  "<input_pdf_path>" \
  "/mnt/user-data/outputs/<output_filename>.pptx" \
  "<logo_path>"
```

**Parameters:**
- `input_pdf_path` - Full path to the uploaded PDF (usually in `/mnt/user-data/uploads/`)
- `output_filename` - Use format: `YYYY.MM.DD_-_Title_-_Template.pptx`
- `logo_path` - Path to DIY Investors logo JPG (project file or outputs folder)

**Logo path options (in priority order):**
1. `/mnt/project/DIYLogo_290_x_58px_for_Report_Covers_JPG.jpg` (project file - preferred)
2. `/mnt/user-data/outputs/diy-investors-logo.jpg` (if copied there previously)
3. Copy from project first: `cp /mnt/project/DIYLogo_290_x_58px_for_Report_Covers_JPG.jpg /home/claude/logo.jpg`

### Step 3: Present the result

After conversion completes, use `present_files` to share the PowerPoint:

```python
present_files(["/mnt/user-data/outputs/<output_filename>.pptx"])
```

## Verified specifications

The following specifications have been tested and verified:

**Branding Header:**
- Height: 0.34 inches (compact)
- Logo: 1.2" x 0.24" (left side, top-left corner)
- Banner: Red (RGB 192, 57, 43) from logo right edge to slide right edge
- Banner text: White, bold, 11pt, centred

**Image Processing:**
- PDF extraction: 200 DPI for quality
- Border cropping: Removes 20px borders on all sides
- Slide filling: 100% width and height, edge-to-edge, no white gaps
- Output format: PNG, optimised

**Masking Rectangle (NotebookLM Logo) - CRITICAL SETTINGS:**
- Width: 1.20 inches (covers last 12% of slide width)
- Height: 0.17 inches (tall enough to cover logo, short enough to avoid text)
- Position: Anchored to absolute bottom-right corner (no margins)
- Coverage area: 8.80" to 10.00" horizontally, 5.46" to 5.625" vertically
- **Colour matching: Sampled from a 60x20 pixel patch at the EXACT bottom-right corner of each slide image**
  - This is the region where the NotebookLM watermark appears
  - Sampling is done AFTER border cropping, on the final image
  - Each slide is sampled independently (background colour varies per slide)
  - Average RGB across the patch is used for seamless colour matching
- Shadow: Disabled (critical for invisibility)
- Border: None (critical for invisibility)

**Verification Results:**
- 100% NotebookLM logo coverage on all slides
- Perfect background colour matching - invisible masking
- No white borders - edge-to-edge fill
- Production ready

## Colour sampling - technical detail

The colour sampling function works as follows:

```python
def sample_bottom_right_color(img):
    w, h = img.size
    # Sample 60x20 pixel patch from absolute bottom-right corner
    x0 = max(0, w - 60)
    y0 = max(0, h - 20)
    patch = img.crop((x0, y0, w, h))
    # Average all pixel RGB values
    pixels = list(patch.getdata())
    r = sum(p[0] for p in pixels) // len(pixels)
    g = sum(p[1] for p in pixels) // len(pixels)
    b = sum(p[2] for p in pixels) // len(pixels)
    return RGBColor(r, g, b)
```

This function is called on each slide AFTER border cropping, ensuring the sample
is from the correct region regardless of the PDF's original dimensions.

## Important notes

**DO NOT modify these optimised values without testing:**
- Masking rectangle dimensions (1.20" x 0.17") are the result of iterative testing
- Header height (0.34") is balanced for visibility and content space
- Colour sampling from bottom-right corner (60x20px patch) is correct and must not be changed to sample from elsewhere

**Requirements:**
- Python packages required: PyMuPDF (fitz), python-pptx, Pillow (all pre-installed in Claude environment)
- Input PDF should be a slide deck (16:9 aspect ratio recommended)

## Configurable parameters (edit in script)

To adapt for different event branding, edit these constants at the top of `pdf_to_pptx.py`:

```python
BANNER_COLOR = RGBColor(192, 57, 43)   # Red for Boot Camp; change for other templates
BANNER_TEXT  = "DIY-Investors 'Boot Camp' (17th January 2026)"  # Update date/event name
```

For Inner Circle or Plaza webinars, update BANNER_COLOR and BANNER_TEXT accordingly before running.

## Example workflow

```
User: "Convert this PDF to PowerPoint using BC2026 template"

Step 1: Copy script
cp "C:/Vaults/Mick's-Dex-2nd-Brain/Dex-MickP/skills/pdf-to-pptx-converter/pdf_to_pptx.py" /home/claude/pdf_to_pptx.py

Step 2: Run conversion
python3 /home/claude/pdf_to_pptx.py \
  "/mnt/user-data/uploads/presentation.pdf" \
  "/mnt/user-data/outputs/2026.04.06_-_Presentation_-_Boot_Camp.pptx" \
  "/mnt/project/DIYLogo_290_x_58px_for_Report_Covers_JPG.jpg"

Step 3: Present result
present_files(["/mnt/user-data/outputs/2026.04.06_-_Presentation_-_Boot_Camp.pptx"])
```

## Performance

- Processing speed: ~1 second per slide
- Typical 15-slide PDF: 15-20 seconds total
- Output file size: 8-15 MB (embedded high-quality images)

## Future enhancements

- Support for Plaza/Inner Circle dark theme (purple header)
- Configurable event dates via command-line parameter
- Batch processing multiple PDFs
- Template selection menu (BC2026 / Plaza / Inner Circle)

## Status

**Version:** 1.1
**Status:** Production Ready
**Script location:** C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\pdf-to-pptx-converter\pdf_to_pptx.py
**Last updated:** 2026-04-06
**Key fix in v1.1:** Colour sampling explicitly confirmed as bottom-right corner; script saved persistently to vault

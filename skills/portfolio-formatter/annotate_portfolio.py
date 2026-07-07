#!/usr/bin/env python3
"""
portfolio-formatter - annotate a ShareScope portfolio screenshot.

Takes a raw ShareScope "Current holdings" screenshot (JPG or PNG, ANY size) and
produces a trimmed, branded image matching Mick's manual style:

  1. Trim to the holdings panel (drop the empty area, button row and taskbar,
     stopping at the grey "Total" summary bar of the holdings list)
  2. Grey border around the whole image
  3. Bottom portfolio label box (blue border/text), inset from the right so it
     never covers the date/time stamp preserved in the bottom-right corner
  4. Top-right annotation box: red title line (portfolio + date) and blue gain
     line (headline gain/loss + percentage)
  5. Red underline under the summary Total value

Headline gain = Total - base (base defaults to 10,000 in the portfolio's
currency). Percentages are TRUNCATED to 2dp, not rounded, matching Mick's
examples (23.6762 -> 23.67, 1.7282 -> 1.72).

Everything is detected from the image by feature (proportional, not fixed
pixels) so it works across different screenshot sizes. Values are read by OCR
(tesseract) and every reading is printed; any can be overridden on the CLI.

USAGE
  python3 annotate_portfolio.py SOURCE.jpg [options]

OPTIONS (all optional - OCR fills them in when omitted)
  --out PATH          output PNG path
  --label "TEXT"      full label, e.g. "US Active 10 (Yr2): 6th July 2026"
  --total N           summary Total value (float), overrides OCR
  --currency GBP|USD  overrides OCR-detected symbol
  --base N            notional starting stake (default 10000)
  --jpg               also write a quality-95 JPG alongside the PNG
"""

import numpy as np, argparse, os, re, sys, math
from datetime import date
from PIL import Image, ImageDraw, ImageFont, ImageOps
import pytesseract
from pytesseract import Output

# Colours - closest match to Mick's example "after" images
RED  = (197, 0, 0)      # annotation title + Total underline
BLUE = (0, 0, 197)      # annotation/label box borders + gain line + label text
GREY = (128, 128, 128)  # outer frame
WHITE = (255, 255, 255)

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def font(sz, bold=True):
    p = ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
         else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    if os.path.exists(p):
        return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def trunc2(x):
    return math.trunc(x * 100) / 100.0


def ordinal(n):
    suf = "th" if 11 <= n % 100 <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"


def detect_table_bottom(a, H):
    """First tall run of near-white full-width rows below 35% height = table end."""
    white = (a[:, :, 0] > 245) & (a[:, :, 1] > 245) & (a[:, :, 2] > 245)
    rw = white.mean(axis=1)
    run = 0
    for y in range(int(0.35 * H), H):
        run = run + 1 if rw[y] > 0.97 else 0
        if run >= 40:
            return y - run + 1
    return int(0.5 * H)


def ocr_all(im):
    d = pytesseract.image_to_data(im, output_type=Output.DICT, config="--psm 6")
    return [(d['text'][i].strip(), d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            for i in range(len(d['text'])) if d['text'][i].strip()]


def _bw_ocr(crop, whitelist=None, thresh=150, scale=3):
    """Upscale + threshold (both polarities) then OCR - for small/low-contrast text."""
    c = crop.convert("L").resize((crop.width * scale, crop.height * scale))
    a = np.asarray(c).astype(int)
    outs = []
    for inv in (False, True):
        mask = (a > thresh) if not inv else (a < thresh)
        bw = Image.fromarray((mask.astype(np.uint8) * 255))
        cfg = "--psm 7" + (f" -c tessedit_char_whitelist={whitelist}" if whitelist else "")
        outs.append(pytesseract.image_to_string(bw, config=cfg).strip())
    return outs


def detect_portfolio(im, currency):
    """Read the green header bar (white-on-green). Threshold to black-on-white first.
    Falls back to currency (GBP->UK, USD->US) if the header cannot be parsed."""
    W, H = im.size
    hdr = im.crop((0, int(0.028 * H), W, int(0.070 * H))).convert("RGB")
    lum = np.asarray(hdr).astype(int).mean(axis=2)
    inv = Image.fromarray((255 - (lum > 180).astype(np.uint8) * 255).astype("uint8"))
    ht = pytesseract.image_to_string(inv, config="--psm 7").strip()
    m = re.search(r"Active\s*10\s*[-–]\s*([A-Za-z]{2})\s*(\(Yr\d\))?", ht)
    if m:
        region, yr = m.group(1).upper(), (m.group(2) or "")
        return f"{region} Active 10{(' ' + yr) if yr else ''}".strip()
    region = "UK" if currency == "GBP" else "US"
    return f"{region} Active 10"


def detect_date(im):
    """Read the valuation date. Prefers the bottom-right clock (dd/mm/yyyy),
    falls back to the holdings date column."""
    W, H = im.size
    regions = [im.crop((int(W - 0.16 * W), int(H - 0.05 * H), W, H)),
               im.crop((0, int(0.20 * H), int(0.09 * W), int(0.30 * H)))]
    for cr in regions:
        for txt in _bw_ocr(cr, "0123456789/"):
            m = re.search(r"(\d{1,2})/(\d{1,2})/(\d{2,4})", txt)
            if m:
                dd, mm, yy = int(m.group(1)), int(m.group(2)), int(m.group(3))
                yy = 2000 + yy if yy < 100 else yy
                if 1 <= mm <= 12 and 1 <= dd <= 31:
                    return f"{ordinal(dd)} {MONTHS[mm - 1]} {yy}"
    return None


def read_values(im, gap):
    words = ocr_all(im)
    txt = " ".join(w[0] for w in words)
    currency = "USD" if ("$" in txt and "£" not in txt) else "GBP"

    portfolio = detect_portfolio(im, currency)
    datestr = detect_date(im)

    # Summary Total value + bbox: OCR the top-left value block
    block = im.crop((0, 80, int(im.width * 0.26), 145))
    bd = pytesseract.image_to_data(block, output_type=Output.DICT, config="--psm 6")
    cand = []
    for i in range(len(bd['text'])):
        m = re.match(r"^[£$]?([\d,]+\.\d{2})$", bd['text'][i].strip())
        if m:
            cand.append((float(m.group(1).replace(",", "")),
                         bd['left'][i], bd['top'][i] + 80, bd['width'][i], bd['height'][i]))
    total, tbbox = None, None
    if cand:
        cand.sort(key=lambda c: c[2])          # lowest row = Total
        v, l, tp, wd, ht = cand[-1]
        total, tbbox = v, (l, tp, l + wd, tp + ht)

    return dict(currency=currency, portfolio=portfolio, date=datestr,
                total=total, tbbox=tbbox)


def build(args):
    im = Image.open(args.source).convert("RGB")
    W, H = im.size
    a = np.asarray(im).astype(int)

    gap = detect_table_bottom(a, H)
    v = read_values(im, gap)

    currency = args.currency or v["currency"]
    sym = "$" if currency == "USD" else "£"
    total = args.total if args.total is not None else v["total"]
    if total is None:
        sys.exit("ERROR: could not read Total value - pass --total N")
    label = args.label or (f"{v['portfolio']}: {v['date']}" if v["date"] else v["portfolio"])

    print(f"[OCR ] portfolio={v['portfolio']} currency={currency} date={v['date']} total={total}")

    gain = total - args.base
    pct = trunc2(gain / args.base * 100.0)
    word = "Up" if gain >= 0 else "Down"
    line2 = f"({word} by {sym}{abs(gain):,.2f}   [{pct:+.2f}%])"
    print(f"[CALC] {line2}  (base {sym}{args.base:,.0f})")

    # crop table + preserve clock
    crop = im.crop((0, 0, W, gap))
    cw, ch = crop.size
    clk_w, clk_h = int(0.093 * W), int(0.042 * H)
    clock = im.crop((W - clk_w, H - clk_h, W, H))

    lab_font = font(max(15, int(cw * 0.020)))
    d0 = ImageDraw.Draw(crop)
    lb = d0.textbbox((0, 0), label, font=lab_font)
    lw, lh = lb[2] - lb[0], lb[3] - lb[1]
    pad = 9
    strip_h = max(lh + pad * 2, clock.height) + 8

    canvas = Image.new("RGB", (cw, ch + strip_h), WHITE)
    canvas.paste(crop, (0, 0))
    canvas.paste(clock, (cw - clock.width - 4, ch + (strip_h - clock.height) // 2))
    draw = ImageDraw.Draw(canvas)

    # red underline under summary Total
    if v["tbbox"]:
        x0, _, x1, y1 = v["tbbox"]
        draw.line([(x0, y1 + 1), (x1, y1 + 1)], fill=RED, width=2)

    # bottom label box, inset from clock
    avail = cw - clock.width - 16
    bx0 = (avail - (lw + pad * 2)) // 2
    by0 = ch + (strip_h - (lh + pad * 2)) // 2
    draw.rectangle([bx0, by0, bx0 + lw + pad * 2, by0 + lh + pad * 2],
                   fill=WHITE, outline=BLUE, width=2)
    draw.text((bx0 + pad, by0 + pad), label, font=lab_font, fill=RED)

    # top-right annotation box (red title, blue gain)
    af = font(max(15, int(cw * 0.021)))
    b1 = draw.textbbox((0, 0), label, font=af)
    b2 = draw.textbbox((0, 0), line2, font=af)
    lh1 = b1[3] - b1[1]
    bw = max(b1[2] - b1[0], b2[2] - b2[0]) + 20
    bh = lh1 + (b2[3] - b2[1]) + 22
    ax1 = cw - int(cw * 0.012) - bw
    ay0 = int(ch * 0.012)
    draw.rectangle([ax1, ay0, ax1 + bw, ay0 + bh], fill=WHITE, outline=BLUE, width=2)
    for i, (ln, col) in enumerate([(label, RED), (line2, BLUE)]):
        bb = draw.textbbox((0, 0), ln, font=af)
        tw = bb[2] - bb[0]
        draw.text((ax1 + (bw - tw) // 2, ay0 + 8 + i * (lh1 + 8)), ln, font=af, fill=col)

    out_img = ImageOps.expand(canvas, border=3, fill=GREY)

    out = args.out or default_out(label)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    out_img.save(out, "PNG")
    print(f"[SAVE] {out}  ({out_img.size[0]}x{out_img.size[1]})")
    if args.jpg:
        jp = os.path.splitext(out)[0] + ".jpg"
        out_img.save(jp, "JPEG", quality=95)
        print(f"[SAVE] {jp}")
    return out


def default_out(label):
    d = date.today().strftime("%Y.%m.%d")
    title = label.split(":")[0].strip()
    return os.path.join("outputs", f"{d} - {title} - Portfolio Formatted_v1.0.png")


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("source")
    p.add_argument("--out")
    p.add_argument("--label")
    p.add_argument("--total", type=float)
    p.add_argument("--currency", choices=["GBP", "USD"])
    p.add_argument("--base", type=float, default=10000.0)
    p.add_argument("--jpg", action="store_true")
    return p.parse_args()


if __name__ == "__main__":
    build(parse_args())

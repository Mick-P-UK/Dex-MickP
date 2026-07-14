#!/usr/bin/env python3
"""
build_schedule.py - amazon-orders skill (Ditty Box Ltd YE accounts)

Turns the per-order Amazon items CSV chunks (produced by
export_amazon_items_csv with start_index) into a landscape, one-row-per-item
review schedule for a financial year, with the REAL payment card on every row.

The chunk pulls themselves are done by Cedric interactively via the
amazon-orders MCP (see SKILL.md). This script does the deterministic part:
  1. Combines all chunk CSVs in a folder.
  2. Dedupes item rows on (Order ID, ASIN, Item Total).
  3. Filters to the FY window (1 Dec prior year .. 30 Nov FY year).
  4. Reconciles Order IDs against an optional master order list (JSON).
  5. Classifies business vs personal from the real card (default 1136).
  6. Builds the landscape per-item XLSX (green=business, plain=personal, pink=cancelled).
  7. Prints a verification report and warns if pulls did not page back far enough.

ASCII only. UK English. XLSX written to a temp file then moved (Cowork
Windows-mount null-padding workaround).
"""

import argparse, csv, glob, json, os, sys, tempfile, shutil
from collections import OrderedDict
from datetime import date

POUND = "\u00a3"
FMT = POUND + "#,##0.00"

CARDTYPE_DEFAULT = {
    "1136": "Halifax Clarity (Business)",
    "8155": "Personal Mastercard",
    "0343": "Personal Mastercard",
    "5039": "Personal Mastercard",
}


def money(s):
    return float((s or "0").replace(POUND, "").replace(",", "").strip() or 0)


def to_date(s):
    y, m, d = s.split("-")
    return date(int(y), int(m), int(d))


def load_chunks(chunks_dir, pattern):
    files = sorted(glob.glob(os.path.join(chunks_dir, pattern)))
    if not files:
        sys.exit("ERROR: no chunk files matched %s in %s" % (pattern, chunks_dir))
    rows = []
    for f in files:
        with open(f, encoding="utf-8-sig", newline="") as fh:
            rows.extend(list(csv.DictReader(fh)))
    return rows, files


def build(args):
    fy_start = date(args.fy_year - 1, 12, 1)
    fy_end = date(args.fy_year, 11, 30)

    rows, files = load_chunks(args.chunks_dir, args.chunks_glob)
    all_dates = sorted(x["Order Date"] for x in rows if x.get("Order Date"))
    oldest = to_date(all_dates[0]) if all_dates else None

    seen = set(); items = []
    for x in rows:
        od = x.get("Order Date", "")
        if not od or not (fy_start <= to_date(od) <= fy_end):
            continue
        key = (x["Order ID"], x["ASIN"], x["Item Total"])
        if key in seen:
            continue
        seen.add(key); items.append(x)

    byorder = OrderedDict()
    for x in sorted(items, key=lambda r: (r["Order Date"], r["Order ID"])):
        byorder.setdefault(x["Order ID"], []).append(x)

    master = {}; cancelled_ids = []
    if args.master and os.path.exists(args.master):
        mlist = json.load(open(args.master, encoding="utf-8"))
        master = {m["oid"]: m for m in mlist}
        cancelled_ids = [m["oid"] for m in mlist if "cancel" in str(m.get("status", "")).lower()]
    if args.cancelled:
        cancelled_ids = [c.strip() for c in args.cancelled.split(",") if c.strip()]

    # Flag only where the item lines tie to NEITHER the order subtotal NOR the
    # order total (>2p). A gap between subtotal and total is just shipping /
    # promotion / part gift-card and is normal - not flagged.
    recon_flag = {}
    for oid, its in byorder.items():
        isum = sum(money(x["Item Total"]) for x in its)
        sub = money(its[0].get("Order Subtotal", ""))
        tot = money(its[0]["Order Total"])
        recon_flag[oid] = abs(isum - sub) > 0.02 and abs(isum - tot) > 0.02

    print("amazon-orders build_schedule.py")
    print("FY window: %s .. %s" % (fy_start, fy_end))
    print("Chunk files read: %d" % len(files))
    print("Oldest order date pulled: %s" % (oldest or "n/a"))
    if oldest and oldest > fy_start:
        print("*** WARNING: oldest pulled date (%s) is AFTER FY start (%s)." % (oldest, fy_start))
        print("    Not paged back far enough - pull more chunks at a higher start_index")
        print("    until the oldest date is on/before %s." % fy_start)

    delivered = len(byorder)
    biz = [o for o, its in byorder.items() if its[0]["Card Last 4"].strip() == args.business_card]
    pers = [o for o in byorder if o not in biz]
    biz_total = sum(money(byorder[o][0]["Order Total"]) for o in biz)
    pers_total = sum(money(byorder[o][0]["Order Total"]) for o in pers)

    print("\nDelivered orders in FY window: %d  (item rows: %d)" % (delivered, len(items)))
    print("  Business (card %s): %d orders, GBP %.2f" % (args.business_card, len(biz), biz_total))
    print("  Personal (other cards): %d orders, GBP %.2f" % (len(pers), pers_total))

    missing = []
    if master:
        want = set(master) - set(cancelled_ids)
        missing = sorted(want - set(byorder))
        print("\nReconciliation vs master (%d orders, %d cancelled):" % (len(master), len(cancelled_ids)))
        print("  Delivered captured: %d / %d" % (delivered, len(want)))
        if missing:
            print("  *** MISSING %d delivered order(s) - pull an overlapping chunk:" % len(missing))
            for mid in missing:
                m = master.get(mid, {})
                print("      %s  %s  GBP %s" % (m.get("date", "?"), mid, m.get("amt", "?")))
        else:
            print("  All delivered orders captured. Zero gaps.")

    if any(recon_flag.values()):
        n = sum(1 for v in recon_flag.values() if v)
        print("\n%d order(s) flagged: item-sum != order total (promotion / part gift-card / postage)." % n)
        print("Order Total (amount charged) is authoritative; flagged in Notes column.")

    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

    wb = Workbook(); ws = wb.active; ws.title = "FY %d-%d Amazon Items" % (args.fy_year - 1, args.fy_year)
    hdr_fill = PatternFill("solid", fgColor="1F3864"); hdr_font = Font(bold=True, color="FFFFFF", size=10)
    green = PatternFill("solid", fgColor="C6EFCE"); pink = PatternFill("solid", fgColor="F8CBAD")
    thin = Side(style="thin", color="BFBFBF"); border = Border(left=thin, right=thin, top=thin, bottom=thin)
    wrap = Alignment(wrap_text=True, vertical="top"); topal = Alignment(vertical="top")
    rightal = Alignment(horizontal="right", vertical="top")

    title = ("Ditty Box Ltd - Amazon.co.uk Orders - FY 1 Dec %d to 30 Nov %d - Per-Item Schedule"
             % (args.fy_year - 1, args.fy_year))
    ws.merge_cells("A1:O1"); c = ws["A1"]; c.value = title; c.font = Font(bold=True, size=13, color="1F3864")
    ws.merge_cells("A2:O2")
    ws["A2"].value = ("Real payment card per order from Amazon invoice. Card %s = business card (green). "
                      "Other cards = personal. Cancelled orders at foot (pink). Prepared by Cedric %s."
                      % (args.business_card, args.date_today))
    ws["A2"].font = Font(italic=True, size=9, color="808080"); ws["A2"].alignment = Alignment(wrap_text=True)
    ws.row_dimensions[2].height = 28

    cols = ["Order Date", "Order ID", "Card Last4", "Card Type", "Biz / Personal", "Item (product)",
            "ASIN", "Qty", "Unit Price", "Item Total", "Order Total", "Status", "Ship-to",
            "Xero Code (Mick)", "Notes"]
    hr = 4
    for i, h in enumerate(cols, 1):
        cell = ws.cell(hr, i, h); cell.fill = hdr_fill; cell.font = hdr_font; cell.border = border
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    ws.freeze_panes = "A5"

    cardtype = dict(CARDTYPE_DEFAULT)
    cardtype.setdefault(args.business_card, "Business card (%s)" % args.business_card)

    r = hr + 1
    for oid, its in byorder.items():
        card = its[0]["Card Last 4"].strip()
        is_biz = card == args.business_card
        for j, x in enumerate(its):
            first = (j == 0)
            row = [x["Order Date"] if first else "",
                   oid if first else "",
                   card if first else "",
                   cardtype.get(card, "Personal card") if first else "",
                   ("Business" if is_biz else "Personal") if first else "",
                   x["Product Name"], x["ASIN"], int(x["Quantity"] or 1),
                   money(x["Unit Price"]), money(x["Item Total"]),
                   money(x["Order Total"]) if first else "",
                   x["Order Status"] if first else "",
                   x["Recipient"] if first else "", "",
                   ("CHECK item-sum vs order total" if (first and recon_flag.get(oid)) else "")]
            for i, v in enumerate(row, 1):
                cell = ws.cell(r, i, v); cell.border = border
                if i in (9, 10, 11):
                    cell.number_format = FMT; cell.alignment = rightal
                elif i == 6:
                    cell.alignment = wrap
                elif i == 8:
                    cell.alignment = Alignment(horizontal="center", vertical="top")
                else:
                    cell.alignment = topal
                if is_biz:
                    cell.fill = green
            ws.row_dimensions[r].height = 30
            r += 1

    for oid in cancelled_ids:
        m = master.get(oid, {})
        row = [m.get("date", ""), oid, "", "", "Cancelled",
               "(order cancelled - no card charge, no items shipped)", "", "", "", "",
               0.0, "Cancelled", m.get("ship", ""), "", "Exclude from Xero"]
        for i, v in enumerate(row, 1):
            cell = ws.cell(r, i, v); cell.border = border; cell.fill = pink
            if i in (9, 10, 11):
                cell.number_format = FMT; cell.alignment = rightal
            elif i == 6:
                cell.alignment = wrap
            else:
                cell.alignment = topal
        r += 1

    r += 1
    ws.cell(r, 5, "SUMMARY").font = Font(bold=True, size=11, color="1F3864"); r += 1

    def putrow(label, val, fill=None):
        nonlocal r
        ws.cell(r, 5, label).font = Font(bold=True)
        cell = ws.cell(r, 11, val); cell.number_format = FMT; cell.font = Font(bold=True); cell.alignment = rightal
        if fill:
            for cc in range(5, 12):
                ws.cell(r, cc).fill = fill
        r += 1

    putrow("Business - card %s (%d orders)" % (args.business_card, len(biz)), round(biz_total, 2), fill=green)
    putrow("Personal - other cards (%d orders)" % len(pers), round(pers_total, 2))
    if cancelled_ids:
        putrow("Cancelled (%d orders)" % len(cancelled_ids), 0.0, fill=pink)
    putrow("TOTAL delivered FY orders (%d)" % delivered, round(biz_total + pers_total, 2))

    widths = {"A": 11, "B": 20, "C": 9, "D": 22, "E": 13, "F": 52, "G": 13, "H": 6,
              "I": 11, "J": 11, "K": 12, "L": 11, "M": 20, "N": 14, "O": 26}
    for col, w in widths.items():
        ws.column_dimensions[col].width = w
    ws.page_setup.orientation = "landscape"; ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True

    out_name = "%s - Amazon Orders FY %d-%d Per-Item Schedule.xlsx" % (args.date_today, args.fy_year - 1, args.fy_year)
    out_path = os.path.join(args.output_dir, out_name)
    os.makedirs(args.output_dir, exist_ok=True)
    tf = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx"); tf.close()
    wb.save(tf.name); shutil.move(tf.name, out_path)
    print("\nWrote: %s" % out_path)

    if missing:
        print("EXIT 2: reconciliation incomplete (missing delivered orders).")
        return 2
    return 0


def main():
    ap = argparse.ArgumentParser(description="Build the Amazon FY per-item schedule XLSX.")
    ap.add_argument("--chunks-dir", required=True)
    ap.add_argument("--chunks-glob", default="_chunk_*.csv")
    ap.add_argument("--fy-year", type=int, required=True, help="FY end year, e.g. 2025 for YE 30 Nov 2025")
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--date-today", required=True, help="YYYY.MM.DD for the filename")
    ap.add_argument("--business-card", default="1136")
    ap.add_argument("--master", default=None)
    ap.add_argument("--cancelled", default=None)
    args = ap.parse_args()
    sys.exit(build(args))


if __name__ == "__main__":
    main()

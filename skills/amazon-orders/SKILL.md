---
name: amazon-orders
description: >
  Builds a full landscape, one-row-per-item schedule of every Ditty Box Ltd
  Amazon.co.uk order for a financial year, with the REAL payment card on each
  order, and reconciles it against the year's order list so nothing is missed.
  Use this skill whenever Mick asks to "do the Amazon orders", "build the
  Amazon schedule", "process the Amazon orders for the year", "list all my
  Amazon orders with the card", "do the Amazon per-item schedule", "run the
  amazon-orders skill", or any request to turn the year's Amazon purchases into
  a business-vs-personal review schedule for Xero coding. Classifies business
  by the real card (Halifax 1136), not by cross-match. Always use this skill
  rather than pulling and parsing the orders by hand. Also use it when Mick asks
  to "reconcile Amazon to the credit card", "tie the Amazon orders to the 1136
  statement", or "prove the Amazon spend" - pass the card's Xero-import CSV via
  --statement-csv and the skill emits the reconciliation as a second output.
  NOTE: this skill produces a REVIEW SCHEDULE (XLSX) for Mick to assign Xero
  codes - it does NOT produce a Xero import CSV (Amazon spend lands in Xero via
  the card accounts: Halifax 1136 for business, personal cards separately).
---

# Amazon Orders - Year End Per-Item Schedule

Pulls every Amazon.co.uk order for a Ditty Box Ltd financial year (1 Dec to
30 Nov) with the real payment card and full item detail, reconciles the order
list so nothing is missed, and builds a landscape review schedule: one row per
item, business (Halifax 1136) rows in green, personal in plain, cancelled in
pink.

Amazon removed its native order-history CSV in March 2023, so the data is
pulled via the locally installed amazon-order-history MCP (browser automation).

## When to use

Once a year during the Ditty Box Ltd annual accounts cycle, to turn the year's
Amazon purchases into a schedule Mick can code to Xero. Also fine for an
interim spot-check.

## What this skill does NOT do

- Does NOT produce a Xero import CSV. Amazon purchases reach Xero through the
  card accounts (Halifax 1136 for business, personal cards for personal spend),
  not as a separate Amazon feed. This schedule is a review/coding aid.
- Does NOT assign Xero account codes. Mick fills the "Xero Code (Mick)" column
  on the green rows.
- Does NOT create anything in Xero. The official Xero connector is read-only
  (reporting tools only) - it cannot create a bill, spend-money or draft.
- Does NOT need the Halifax 1136 cross-match any more. The real card is now on
  every order, so business is read straight off the card (this replaces the old
  cross-match method in the 2026.05.29 SOP).

## Prerequisites

1. The amazon-order-history MCP installed and authenticated for region uk
   (v0.3.1 or later - the version with the start_index parameter).
   Auth persists in C:\Users\pavey\.amazon-order-history-mcp\browser-data\.
2. Python 3 with openpyxl (pip install openpyxl --break-system-packages).
3. Optional but recommended: a master order list JSON for reconciliation (see
   "Reconciliation" below). If none exists yet, the skill still runs - it just
   cannot prove completeness, so page back generously.

## Inputs each year

- FY end year, e.g. 2025 for YE 30 Nov 2025 (FY window = 1 Dec 2024..30 Nov 2025).
- Date today in YYYY.MM.DD form (for the filename).
- Business card last 4 (default 1136).

## Step 1 - Verify authentication

Call check_amazon_auth_status region uk. Expect authenticated: true,
username "Hello, M.A.Pavey". If not, a browser window opens - Mick logs in,
then re-check.

## Step 2 - Pull the year in chunks (real card + items)

Call export_amazon_items_csv in chunks of 20 using start_index, writing each
chunk to the year's workings folder. The items export returns the real
"Card Last 4" and "Payment Method" on every row.

  export_amazon_items_csv region=uk year=<FYyear-1> start_index=0  max_orders=20  (December)
  export_amazon_items_csv region=uk year=<FYyear>   start_index=0  max_orders=20
  export_amazon_items_csv region=uk year=<FYyear>   start_index=20 max_orders=20
  export_amazon_items_csv region=uk year=<FYyear>   start_index=40 max_orders=20
  ... keep going: 60, 80, 100, ...

CRITICAL PAGING RULE: keep adding chunks for the FY year until the OLDEST date
in the newest chunk is on or before 1 Dec of the prior year. A year with more
than ~100 orders needs start_index beyond 80 (FY 2024-25 needed 100 to reach
2 Jan 2025 - five chunks was NOT enough). The build script prints a WARNING if
the oldest pulled date is after the FY start - if you see it, pull more.

Name chunks so the script's default glob finds them, e.g.
_chunk_2024_si0.csv, _chunk_2025_si0.csv, _chunk_2025_si20.csv, ...

Keep pulls SEQUENTIAL. Parallel per-order calls fail ("permission stream
closed"). A timed-out large batch writes no file - that is why chunks are 20.

## Step 3 - Build the schedule (script)

Run scripts/build_schedule.py. It combines the chunks, dedupes item rows,
keeps the FY window, reconciles against the master, classifies by the real
card, and writes the landscape XLSX.

```bash
python3 /path/to/skills/amazon-orders/scripts/build_schedule.py \
  --chunks-dir "C:/Vaults/DB-Accounts-CW/YE_2025.11.30/workings" \
  --fy-year 2025 \
  --output-dir "C:/Vaults/DB-Accounts-CW/YE_2025.11.30/workings" \
  --date-today 2026.07.13 \
  --business-card 1136 \
  --master "C:/Vaults/DB-Accounts-CW/YE_2025.11.30/workings/_master_orders.json" \
  --statement-csv "C:/Vaults/DB-Accounts-CW/YE_2025.11.30/workings/2026.05.28 - D.Box_HX-CC-1136_Xero-import_YE_2025_DRAFT.csv"
```

--business-card defaults to 1136. --master, --cancelled and --statement-csv are
optional; omit --statement-csv and the skill runs standalone (schedule only).
The script writes the XLSX via a temp file then moves it (Cowork Windows-mount
null-padding workaround) and exits non-zero if any master order is missing.

## The chunk CSV format (background)

export_amazon_items_csv writes a 32-column, one-row-per-item CSV with a UTF-8
BOM. Key columns the script uses: Order ID, Order Date (YYYY-MM-DD), ASIN,
Product Name, Quantity, Unit Price, Item Total, Order Subtotal, Order Total,
Order Status, Recipient, Payment Method, Card Last 4.

## Classification

Business = Card Last 4 equals the business card (default 1136, the Halifax
Clarity credit card). Every other card (personal Mastercards, e.g. 8155 / 0343
/ 5039) = Personal. No Halifax statement cross-match needed. This is the whole
point of pulling the real card: business spend on 1136 can no longer hide in
the personal pile.

## Gift cards - why "Charged to Card" exists

An order can be part- or fully-settled from an Amazon gift card balance. Amazon
still shows a card number against it, but the gift-funded part NEVER reaches the
card statement. Counting the order value as card spend therefore overstates the
year.

Detection: Payment Method contains "Gift Card" (e.g. "Amazon Gift CardMaster").
For those orders the amount that actually hit the card is Amazon's
Order Grand Total (0.00 when the gift card covered it all); for every other
order Grand Total mirrors Order Total.

The schedule therefore carries TWO money columns per order:
  Order Total     - the value of the order (what Amazon billed for the goods)
  Charged to Card - what actually reached the card, and so what appears on the
                    card statement. Sum THIS to agree to the statement.
Gift-card rows are filled amber and carry a plain-English note. Do not claim a
gift-card-funded amount via the card. Worth a query: was the gift card company
or personal funds?

FY 2024-25 had two: one full (GBP 13.00 order, GBP 0.00 charged, card 1136) and
one partial (GBP 40.82 order, GBP 33.82 charged, card 5039). The partial is why
a simple "Grand Total == 0" test is NOT sufficient - test the Payment Method.

## Reconciliation to the card statement (optional, --statement-csv)

Pass the business card's Xero-import CSV (the output of the cc1136-to-xero
skill) and the skill writes a second XLSX proving every Amazon charge on the
card ties to an Amazon order or is a non-order item.

  --statement-csv "<path to>/YYYY.MM.DD - D.Box_HX-CC-1136_Xero-import_YE_YYYY*.csv"
  --match-window 14      (days after the order date to look for the charge)

Method - and note what it deliberately does NOT do. It does NOT hard-code
subscription amounts. It matches ORDERS to CHARGES on the amount that actually
reached the card (not the order value), allowing -2..+match-window days because
Amazon charges when it ships. It then tries combinations, because Amazon batches
several orders into one card charge (FY 2024-25: GBP 42.79 on 22 Dec = two 21 Dec
orders, GBP 25.00 + GBP 17.79). WHATEVER CHARGES ARE LEFT OVER ARE the non-order
items - subscriptions, Prime, etc. Deriving them this way means an Amazon price
change cannot silently break the reconciliation.

Sections in the output: orders matched to a charge (green); orders settled by
gift card, no charge expected (amber); orders with NO matching charge (red -
usually shipped/charged after the year end, check the next statement); charges
with no matching order (subscriptions / membership - already in Xero via the
card import, just code them); and a CONTROL block that must tie to 0.00.

## Reconciliation (master order list)

The master JSON is a list of objects, one per FY order, with at least:
  { "oid": "204-xxxxxxx-xxxxxxx", "date": "2025-01-02", "amt": 22.13,
    "status": "Delivered", "ship": "Mr Michael A Pavey" }
Orders whose status contains "cancel" are treated as cancelled: they are listed
separately at the foot (pink) and are NOT expected in the items export
(cancelled orders are skipped by Amazon's export - they have no card charge).
The script reports any delivered master order not captured and exits 2 so the
gap is impossible to miss - pull an overlapping chunk to fill it, then re-run.

If there is no master yet, build one from a fast order-summary export
(export_amazon_orders_csv, both calendar years) filtered to the FY window, or
skip --master and rely on the paging rule plus the oldest-date warning.

## Output

In the year's workings folder:
  `YYYY.MM.DD - Amazon Orders FY YYYY-YYYY Per-Item Schedule.xlsx`   (always)
  `YYYY.MM.DD - Amazon vs Card NNNN Reconciliation FY YYYY-YYYY.xlsx` (only with
                                                              --statement-csv)

Landscape, one row per item. Columns: Order Date, Order ID, Card Last4, Card
Type, Biz/Personal, Line, Item (wrapped, wide), ASIN, Qty, Unit Price, Item
Total, Order Total, Charged to Card, Status, Ship-to, Xero Code (Mick), Notes.

IMPORT-READY SHAPE (Mick's requirement, 2026.07.14): the order-level fields
repeat on EVERY item line so each row stands alone. The two money-per-order
columns (Order Total, Charged to Card) are the exception - they appear ONCE per
order, on its first line, so the columns can be summed without double-counting a
multi-item order. Sum the Order Total column, never the Item Total column, to
agree the year. A "Line" column ("1 of 2") plus a heavier rule above each new
order makes multi-item orders obvious now that the Order ID repeats.

Every sheet carries the standing footer rule (Mick, 2026.07.14): the file path
and print date/time on the left of the footer -
"(&[Path]&[File] - Printed: &[Date] at &[Time])" - so any printout traces back to
its source file. This applies to ALL Excel Cedric produces, not just this skill.

Green = business card, amber = gift-card funded, plain = personal, pink =
cancelled. Summary block at the foot shows order value AND charged to card:
business, personal, cancelled, total delivered, and the gift-card amount that
never reached a card.

A "CHECK item-sum vs order total" note appears only where the item lines tie to
NEITHER the order subtotal NOR the order total (a plain subtotal-to-total gap is
just shipping / promotion / postage and is normal, so it is not flagged). These
Notes cells are filled LIGHT RED so they jump out (Mick's request 2026.07.14).
Gift-card orders show the gift-card note instead - the gift card explains the
gap, so it is not a "something is wrong" flag.

## Verification the script prints

- FY window and number of chunk files read.
- Oldest order date pulled, with a WARNING if it is after the FY start.
- Delivered order count and item-row count.
- Business vs personal split: orders, order value AND charged to card.
- Any gift-card orders, with order value vs charged.
- Reconciliation vs master: captured / expected, and any missing orders.
- Count of orders flagged for the item-sum check.
- With --statement-csv: charges matched / not matched, gift-card orders, orders
  with no charge, and a CONTROL line that must read "(TIES)".

## Known gotchas

1. Paging: five chunks (si 0-80) is not always enough. Page until the oldest
   date is on/before the FY start. Trust the WARNING line.
2. Cancelled orders are skipped by the items export - they must come from the
   master and are listed separately. They carry no card charge.
3. Sequential pulls only - parallel calls fail; large batches time out and
   write nothing. Keep max_orders at 20.
4. get_amazon_order_details is unreliable for the card (empty) and hangs on
   include_transactions - do not use it for this; use the bulk items export.
5. UTF-8 BOM on every chunk - the script reads with utf-8-sig.
6. Cowork null-padding on Windows-mounted writes - script writes XLSX to a
   temp file then moves it.
7. The date-range filter (start_date/end_date) on the MCP is dead - use year +
   start_index only, and filter to the FY window in the script.
8. GIFT CARDS: never assume the order value hit the card. Test Payment Method
   for "Gift Card" and take Order Grand Total. A partial gift card (order 40.82,
   charged 33.82) will defeat a "Grand Total == 0" test.
9. Amazon batches orders into one card charge - the reconciliation must try
   combinations, not just 1:1 matching.
10. If Excel has the output open, the save fails with PermissionError - write to
   a new filename or ask Mick to close it.
11. NEVER let a cell's text start with "=". openpyxl types it as a FORMULA, and
   Excel then shows "Removed Records: Formula from /xl/worksheets/sheet1.xml
   part" and repairs (deletes) it. Bit us 2026.07.14 with a control label
   "= Total Amazon charges...". The script now calls no_formulas(ws) before
   every save, which forces any formula-typed cell back to text. Keep that
   guard, and check openpyxl data_type == "f" if the repair dialog ever
   reappears.

## If the script fails

The logic is fully documented above (combine, dedupe on Order ID+ASIN+Item
Total, filter the FY window, classify by Card Last 4, reconcile vs master,
build the landscape XLSX). Cedric can reproduce it directly from this SKILL.md.

## After the run

Tell Mick:
1. Delivered order count and the business/personal split (orders and GBP).
2. The reconciliation result (captured vs expected; clean = zero gaps).
3. Any orders the real card reclassified from personal to business (the leak
   this skill exists to catch).
4. Any item-sum CHECK flags, and any gift-card orders (these change what can be
   claimed via the card).
5. With --statement-csv: whether the reconciliation TIES, and list any charges
   with no matching order (they still need coding in Xero).
Then remind him to fill Xero codes on the green rows and to git commit.

## Validation history

- Built and validated 2026.07.13 (Session 11) against FY 1 Dec 2024 - 30 Nov
  2025. Script output reproduced the hand-built schedule exactly: 95 delivered
  orders (24 business on card 1136 = GBP 2,013.80; 71 personal = GBP 1,977.58),
  3 cancelled, zero gaps vs the 98-order master. The real card caught 8 business
  orders that a prior cross-match sheet had mislabelled personal.
- 2026.07.14 (Session 12): import-ready shape (order fields repeat per line,
  Line column, single Order Total), light-red CHECK flags, gift-card detection
  and the Charged to Card column, and the optional --statement-csv
  reconciliation folded in as a second output (Mick's decision: keep it in this
  skill rather than a separate one - shared inputs, no drift; same call he made
  folding the stock PDF into schwab-to-xero in Session 10).
  IMPORTANT CORRECTION from that day: business ORDER VALUE is GBP 2,013.80 but
  business CHARGED TO CARD is GBP 2,000.80 - the GBP 13.00 difference is one
  order settled entirely from an Amazon gift card. GBP 2,000.80 is what ties to
  the 1136 statement. Reconciliation TIED to 0.00: 22 charges / 23 orders =
  GBP 2,000.80 matched, 13 leftover charges = GBP 208.88 (12 monthly subs +
  Prime), 1 gift-card order, 0 unmatched either way.

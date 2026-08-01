---
title: SOP - Portico-WE-portfolios (weekend PP1 + PP2 snapshot and Slack post)
version: 1.0
created: 2026-08-01
owner: Mick (built with Cedric)
status: active
purpose: The weekend routine that captures the two Portico portfolios (PP1, PP2) from ShareScope, formats them into Mick's house-style snapshot images, and posts them to their Slack channels as Mick with an approved caption. Chains the portico-snapshot and PPfolios-to-Slack skills.
---

# SOP - Portico-WE-portfolios

Mick's Saturday-morning routine: show the two Portico portfolios to the members by
posting a branded snapshot image of each to its Slack channel, then (separately) post
a video with commentary to #micks-diary.

This SOP chains two standalone skills, kept separate on purpose:
1. `portico-snapshot` - capture + format PP1 and PP2 (runnable any day).
2. `PPfolios-to-Slack` - publish the finished images to Slack (runnable independently).

## Trigger phrases

"do the weekend Portico post", "run Portico-WE-portfolios", "do the PP1 and PP2
weekend snapshots and post them", "weekend Portico routine", "let's do the Portico
weekend post".

## Key facts (do not get these wrong)

- Portfolios: PP1 -> #portico-portfolio-1 (C01H7ST4BDK, public);
  PP2 -> #portico-portfolio-2 (C04GZAAPT9U, private).
- Base capital: PP1 = 29,331.39 (carrying value); PP2 = 50,000.00 (nominal).
  Gain = Total - base. Percentage TRUNCATED to 2dp, never rounded.
- Posts go out AS Mick (Slack user token), PP1 FIRST then PP2 (PP2 refers back to PP1).
- The video/commentary goes to #micks-diary (C01HC8AD7V0) SEPARATELY. Mick posts the
  IMAGES FIRST and makes the video AFTERWARDS, so the caption points FORWARD by default
  ("will shortly be available on #micks-diary"), not "is contained in the video on...".
- Label/caption date is the actual Saturday, not necessarily today.

## Standing rule - publishing is Mick's call

These are live member channels. Cedric ALWAYS drafts the captions, shows Mick the
images + captions + figures + target channels, and posts ONLY on Mick's explicit
go-ahead. The poster script also gates the two real channels behind a `--yes` flag.
Never auto-post.

## The routine

### 1. CAPTURE (Mick runs, on his PC) - via portico-snapshot skill

```
cd "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation"
python sharescope_portico.py
```

Expect `holdings=OK transactions=OK snapshot=OK` for both, plus a
`filtered to N current holdings` line each. If the summary flags
`current-holdings view NOT confirmed` (the known slow-load caveat, PP1 most at risk),
re-run or verify the raw PNG by eye before formatting.

### 2. RECONCILE + FORMAT (Cedric) - portico-snapshot skill

Read each portfolio's Total from `portico\downloads\YYYY.MM.DD - PPx - Holdings.csv`,
cross-check the raw PNG by eye, then run `annotate_portico.py --stamp` per portfolio
to produce the finished images in `portico\outputs\`
(`YYYY.MM.DD - PPn - Portico Weekend Snapshot.png`). Append the week's figures + the
week-on-week deltas to `portico\portico_history.json`.

### 3. DRAFT CAPTIONS (Cedric) - PPfolios-to-Slack skill

Draft both captions using
`portico\PPfolios-Slack-Phraseology-Reference.md`. PP1 first (usually greets), PP2
second (refers back). Movement comment from the week-on-week delta. Forward-looking
#micks-diary pointer by default (see Key facts). Save to `caption_pp1.txt` /
`caption_pp2.txt`. Show Mick and get approval.

### 4. POST (Cedric, on Mick's go-ahead) - PPfolios-to-Slack skill

```
cd "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\portico"

python slack_post_portico.py --portfolio PP1 --image "outputs/YYYY.MM.DD - PP1 - Portico Weekend Snapshot.png" --total <PP1_total> --base 29331.39 --caption-file caption_pp1.txt --yes
python slack_post_portico.py --portfolio PP2 --image "outputs/YYYY.MM.DD - PP2 - Portico Weekend Snapshot.png" --total <PP2_total> --base 50000 --caption-file caption_pp2.txt --yes
```

Confirm the permalinks; optionally read each channel back to verify.

### 5. VIDEO (Mick, separately)

Mick creates and posts the commentary video to #micks-diary afterwards. NOT part of
this SOP yet - a dedicated video-creation skill is planned (Mick, 2026-08-01).

## Testing safely

Rehearse against the private `#cedric-private` channel (C0BMFLPKTHS) with
`--channel C0BMFLPKTHS` (no `--yes` needed - the seatbelt only guards PP1/PP2).

## Prerequisites

- ShareScope creds and `SLACK_USER_TOKEN` (xoxp-, chat:write+files:write user scopes,
  "PPfolios Poster" app) both in the single canonical `C:\Users\pavey\.env`.
- Python with requests, Pillow, python-dotenv (capture also needs Playwright; the
  formatter needs Tesseract/pytesseract).

## Open items / not yet built

- Slow-load robustness on capture (PP1 can occasionally grab the full holdings list) -
  add a grid 0-share signal or auto-retry on the error flag. See the portico-snapshot
  skill and PICKUP_POINT_2026.07.25_Portico.md.
- Fully unattended weekend SCHEDULE (Windows Task Scheduler capture + Cedric formats/
  posts). Approach still to be confirmed with Mick; until then this is a Mick-triggered
  routine.
- Video-creation skill for the #micks-diary commentary (next build).

## Related

- Skills: `skills\portico-snapshot\SKILL.md`, `skills\PPfolios-to-Slack\SKILL.md`
- Scripts: `...\portico\sharescope_portico.py`, `...\portico\annotate_portico.py`,
  `...\portico\slack_post_portico.py`
- Phraseology: `...\portico\PPfolios-Slack-Phraseology-Reference.md`
- Week store: `...\portico\portico_history.json`
- Index entry: `C:\Vaults\_SOPs\INDEX.md` (Active SOP #7)

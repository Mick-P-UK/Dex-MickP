---
name: PPfolios-to-Slack
description: Posts the finished Portico PP1 and PP2 snapshot images to their Slack channels (#portico-portfolio-1 and #portico-portfolio-2), AS Mick, each with an approved caption in his house style. Standalone - runnable independently of capture. Use this skill whenever Mick says "post the PP1 and PP2 snapshots to Slack", "post the Portico snapshots", "PPfolios to Slack", "put the portfolio snapshots on Slack", "post PP1 and PP2", or any request to publish the weekend Portico snapshot images to Slack. Always drafts the caption for Mick and posts ONLY on his explicit go-ahead - never auto-posts. For the full weekend routine (capture then post), follow the Portico-WE-portfolios SOP.
version: 1.0
created: 2026-08-01
owner: Mick (built with Cedric)
---

# PPfolios-to-Slack

Publish the two finished Portico snapshot images to their Slack channels, posted AS
Mick (user token), each with a short caption written in his weekend house style. This
is the second half of the weekend routine; the first half (capture + format) is the
`portico-snapshot` skill. Kept separate so a snapshot can be captured without posting,
or a post re-run without re-capturing.

## Hard rule - draft, then post only on Mick's go-ahead

These are LIVE member channels. Publishing is Mick's call every time. ALWAYS:
1. Draft the caption (below), show it to Mick with the target channel and figures.
2. Post ONLY after Mick's explicit approval.
3. The poster script enforces this too: posting to a real PP1/PP2 channel requires
   the `--yes` flag; without it the script prints a dry preview and posts nothing.

Never auto-post. Never post without showing the draft first.

## Prerequisites

- `SLACK_USER_TOKEN` in the single canonical `C:\Users\pavey\.env` - a Slack USER
  token (`xoxp-`) with `chat:write` and `files:write` USER scopes, from the
  "PPfolios Poster" app in the Portico Plaza workspace. A user token is required so
  posts appear AS Mick, not as a bot. Verify any time with:
  `python -c "import requests,os; from dotenv import dotenv_values;
   t=dotenv_values(r'C:\Users\pavey\.env')['SLACK_USER_TOKEN'];
   print(requests.post('https://slack.com/api/auth.test',headers={'Authorization':f'Bearer {t}'}).json())"`
  (expect ok=True, user=mickp, team=Portico Plaza).
- Python with `requests`, `Pillow`, `python-dotenv` (all confirmed present on Mick's PC).
- Finished snapshot PNGs from `portico-snapshot`, in
  `04-Projects\2026.04.04-ShareScope-Automation\portico\outputs\`.
- The reconciled Total for each portfolio (drives the JPG name and the caption figure).

## Channels (do not guess these)

- PP1 -> #portico-portfolio-1  (C01H7ST4BDK, public)
- PP2 -> #portico-portfolio-2  (C04GZAAPT9U, private)
- Commentary/video channel referenced in captions: #micks-diary (C01HC8AD7V0).
  Mick posts the video there SEPARATELY; this skill only links to it.

## The script

`04-Projects\2026.04.04-ShareScope-Automation\portico\slack_post_portico.py`

It: loads the token, converts the finished PNG to Mick's standard-named JPG
(`YYYY.MM.DD - PPn_{total}GBP_Up by {gain}GBP_Up by {pc}pc.jpg`, percentages
truncated to 2dp), then uploads + posts it to the channel with the caption as the
message (Slack files.getUploadURLExternal -> byte upload -> completeUploadExternal
with initial_comment). Gain/percentage are computed from `--total` and `--base`.

Base capital: PP1 = 29331.39, PP2 = 50000.

## Workflow

### Step 1 - Draft the caption (Cedric)

Use the phraseology reference so it reads as genuinely Mick:
`04-Projects\2026.04.04-ShareScope-Automation\portico\PPfolios-Slack-Phraseology-Reference.md`

Caption skeleton:
`[greeting - PP1 usually greets] + [here-is line: "Here's PPn today (Saturday Nth Month YYYY)"]
 + [one-line week-on-week movement comment] + [pointer to <#C01HC8AD7V0|micks-diary>]
 + [sign-off: "Mick (HH.MMBST, Nth Month YYYY)"]`

SIGN-OFF TIME IS MANDATORY (Mick, 2026-08-01): the sign-off must carry the POSTING TIME
before the date - "Mick (HH.MMBST, Nth Month YYYY)" - stamped with the ACTUAL London
time at the moment of posting (BST late Mar - late Oct, else GMT), so it accurately
records when the post went out. Never drop the time.

- PP1 is drafted and posted FIRST; PP2 SECOND and refers back ("And here's PP2 today...").
- The movement comment ("increased slightly", "down slightly", "up a smidgeon",
  "bounced back") comes from the week-on-week delta in `portico_history.json`
  (this week's total vs last week's). Match Mick's understated tone; do not invent
  figures. If unsure which way to phrase it, ask Mick.
- VIDEO TIMING (default): Mick posts the IMAGES FIRST and makes the video AFTERWARDS,
  so the pointer must be FORWARD-LOOKING by default - the video does not exist yet.
  Default: "The video, with my commentary, will shortly be available on
  <#C01HC8AD7V0|micks-diary>." Only use the past/present form ("is contained in the
  video on ...") when Mick has already posted the video before the images.
- Write the finished channel-mention form `<#C01HC8AD7V0|micks-diary>` in the caption
  so Slack renders it as a link (confirmed working).
- Keep it ASCII; write pound values as GBP inside vault-stored drafts, but the LIVE
  Slack caption may use the pound sign (Slack is not the vault). If in doubt, GBP is safe.

Save each caption to a small UTF-8 file (avoids PowerShell quoting pain), e.g.
`portico\caption_pp1.txt` and `portico\caption_pp2.txt`.

### Step 2 - Show Mick the drafts and get the go-ahead

Present both drafted captions, the two images, the totals, and the target channels.
Wait for explicit approval. Adjust wording if Mick asks.

### Step 3 - Post (Cedric, on approval)

PP1 first, then PP2:

```
cd "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\04-Projects\2026.04.04-ShareScope-Automation\portico"

python slack_post_portico.py --portfolio PP1 ^
  --image "outputs/YYYY.MM.DD - PP1 - Portico Weekend Snapshot.png" ^
  --total <PP1_total> --base 29331.39 ^
  --caption-file caption_pp1.txt --yes

python slack_post_portico.py --portfolio PP2 ^
  --image "outputs/YYYY.MM.DD - PP2 - Portico Weekend Snapshot.png" ^
  --total <PP2_total> --base 50000 ^
  --caption-file caption_pp2.txt --yes
```

The script prints the post permalink for each. Optionally confirm with a channel read.

### Testing without publishing

To rehearse safely, post to the private `#cedric-private` channel (C0BMFLPKTHS)
instead of a member channel, using `--channel C0BMFLPKTHS` (no `--yes` needed - the
`--yes` gate applies only to the real PP1/PP2 channels):

```
python slack_post_portico.py --portfolio PP2 --image "outputs/...PP2....png" ^
  --total <total> --base 50000 --caption-file caption_pp2.txt --channel C0BMFLPKTHS
```

## Gotchas / notes

- User token ONLY - a bot token would post as an app, not as Mick. The app has only
  `chat:write` + `files:write` user scopes; it deliberately CANNOT open DMs
  (`im:write`), create channels, or read history. That is fine - it only posts.
- `--yes` is the seatbelt for the two live channels. `--channel <id>` overrides the
  target (used for the test channel); the seatbelt only triggers for PP1/PP2 ids.
- The posted JPG is written alongside the source PNG in `outputs\` and kept as the
  record of what went out.
- The commentary VIDEO in #micks-diary is Mick's separate manual step - this skill
  only links to it, never posts it.
- If `auth.test` fails ("invalid_auth"/"token_expired"), the token in `.env` needs
  refreshing: reinstall the "PPfolios Poster" app and copy the new User OAuth Token.

## Where this sits

`portico-snapshot` (capture + format) -> **PPfolios-to-Slack** (publish). The weekend
routine that chains them is the `Portico-WE-portfolios` SOP.

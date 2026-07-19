# SKILL: newsletter-wp-publisher
**Version:** 1.0
**Created:** 2026.07.19
**Location (vault):** C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\newsletter-wp-publisher\SKILL.md
**Author:** Cedric (PAIDA)

---

## Purpose

Take a finished newsletter HTML file (built in the Mick's-Writing-System vault by the
`diy-newsletter` skill, still carrying `YOUR_MEDIA_URL/...`, `YOUR_PDF_URL` and any
cross-link placeholders) and publish it end-to-end to WordPress: upload every image and
the PDF to the media library, swap the placeholders for real URLs, and push the result
to a post - either updating an existing draft or creating a brand new one.

This closes the loop that previously ended with "Mick uploads the images and swaps the
URLs himself." Built 2026.07.19 after successfully running the full pipeline by hand on
the July 2026 Freedom Blueprint newsletter (post 15514, diy-investors.com).

This skill handles WordPress media/post mechanics only. It has no knowledge of newsletter
content, voice, or layout - that is `diy-newsletter`'s job.

---

## Multi-Site Support

| Site ID | URL | .env key (URL) | .env key (user) | .env key (password) | Status |
|---------|-----|----------------|-----------------|---------------------|--------|
| `diy-investors-com` | https://diy-investors.com | WP_DIY_INVESTORS_URL | WP_DIY_INVESTORS_USER | WP_DIY_INVESTORS_APP_PASSWORD | LIVE - proven 2026.07.19 (July newsletter, post 15514) |
| `diy-investors-ai` | https://diy-investors.ai | WP_DIY_AI_URL | WP_DIY_AI_USER | WP_DIY_AI_APP_PASSWORD | Credentials confirmed present in .env (checked 2026.07.19) but UNTESTED - no AI for Investing newsletter has been built or pushed yet. Test with a private/throwaway draft the first time before trusting it for a real edition. |

To publish to a new site in future, add its three keys to `C:\Users\pavey\.env` and a
row to `SITE_KEYS` in `scripts/publish_newsletter.py` - the rest of the pipeline (upload,
placeholder replace, create/update) is already site-agnostic and needs no other changes.

Credentials are read fresh from `.env` on every run. Never hard-code credentials in this
skill, the script, or any manifest file.

---

## Two Modes

### `update` - push new content into an existing draft (used for July 2026)

Use this when Mick has already created the WordPress draft post himself (typically by
pasting the HTML in), and you are only swapping placeholder URLs for real ones.

- Only the `content` field is touched. Title, status, category, tags are left exactly as
  they are - never assume, never overwrite.
- Before doing anything, the script GETs the existing post and prints its current title
  and status so a stale or wrong `post_id` is caught immediately, not after upload.

### `create` - build a brand new draft from scratch

Use this once Mick is ready to skip the manual "paste the HTML into a new post" step too
(this is the natural next step Mick flagged on 2026.07.19 - not yet exercised in
practice as of this version).

- Status is always hardcoded to `draft` - this skill NEVER auto-publishes, in either mode.
- Requires `title` and (usually) `category_slug` in the manifest. `tags` and `post_date`
  are optional.

---

## Manifest Schema

The script takes one JSON manifest per run. Cedric builds this by hand each edition
(see "Finding the local media files" below) - there is no folder-scanning magic here,
because newsletter image filenames are far less convention-locked than the portfolio
screenshots `wordpress-image-uploader` handles.

```json
{
  "target_site": "diy-investors-com",
  "mode": "update",
  "post_id": 15514,
  "html_path": "C:\\Vaults\\Mick's-Writing-System\\knowledge\\drafts\\2026.07.18 - Freedom Blueprint July_HTML.html",
  "media": [
    {
      "placeholder": "YOUR_MEDIA_URL/jul-2026-uk-economy-scorecard-burnham-backdrop.png",
      "local_path": "C:\\Vaults\\Mick's-Writing-System\\0.0 - Inbox\\Newsletter-Images\\2026.07.14 - UK Economy Scorecard (Burnham Backdrop)_July-Newsletter.png",
      "wp_filename": "2026.07.14-UK-Economy-Scorecard-Burnham-Backdrop.png"
    }
  ],
  "pdf": {
    "placeholder": "YOUR_PDF_URL",
    "local_path": "C:\\Vaults\\Mick's-Writing-System\\knowledge\\drafts\\2026.07.18 - Freedom Blueprint July_v.01.07_FINAL_PDF.pdf",
    "wp_filename": "2026.07.18-Freedom-Blueprint-July_v.01.07_FINAL.pdf"
  },
  "extra_replacements": {
    "YOUR_MAY_POST_URL": "https://diy-investors.com/wp-content/uploads/2026/05/2026.05.16-May-Newsletter_v.01.06_FINAL_PDF.pdf"
  }
}
```

For `mode: create`, add:

```json
{
  "title": "The Freedom Blueprint (August '26 Edition)",
  "category_slug": "freedom-blueprint",
  "tags": [],
  "post_date": "2026-08-15"
}
```

`placeholder` for a media item is the FULL string as it appears in the HTML (i.e.
`YOUR_MEDIA_URL/<token>`, not just the token) - this makes the manifest a literal
find-and-replace map with no token-parsing logic needed in the script.

---

## Workflow

1. Confirm the target site's three credential keys exist in `.env`. Abort with a clear
   error naming the missing keys if not - never fall back to another site's credentials.
2. `mode: update` only - GET the existing post, print its current title + status to Mick
   before touching anything.
3. Upload every file in `media` and (if present) `pdf` to `/wp-json/wp/v2/media` via the
   target site's Poster Pete Application Password. Real `source_url` returned by
   WordPress replaces the matching `placeholder` string in the HTML - never construct the
   URL manually.
4. Apply `extra_replacements` (cross-links to earlier editions, etc.).
5. Safety check: scan the resulting HTML for `YOUR_MEDIA_URL`, `YOUR_PDF_URL`, or any
   `extra_replacements` key still present. If anything is unresolved, ABORT before writing
   the file or touching the post - never publish a page with a dead placeholder link.
6. Write the updated HTML back to `html_path` in place (this is the same file the
   `diy-newsletter` skill produced - keeps the vault's local master in sync with what
   went live).
7. `mode: update` - POST `{"content": html}` only to `/wp-json/wp/v2/posts/<post_id>`.
   `mode: create` - POST a full new draft (title/content/status=draft/categories/tags/date)
   to `/wp-json/wp/v2/posts`.
8. Report back: post ID, status, wp-admin edit URL, and public preview link. Mick reviews
   and publishes himself - this skill never flips status to `publish`.

---

## Finding the Local Media Files (manual/semi-automated - do this before writing the manifest)

Newsletter images live in `C:\Vaults\Mick's-Writing-System\0.0 - Inbox\Newsletter-Images\`
and the finished PDF lives in `C:\Vaults\Mick's-Writing-System\knowledge\drafts\`, both
named with the `YYYY.MM.DD - ...` vault convention, but there is no single reliable regex
across all six-plus image slots the way there is for portfolio screenshots. Locate each
file with Glob against the placeholder's subject matter (scorecard, UK/US portfolio,
UK/US transactions, video thumbnail) before building the manifest, and always confirm
with `Test-Path` (or equivalent) that every path in the manifest resolves before running
the script - a mid-run failure after some uploads have already gone live is avoidable
with a five-second pre-flight check.

### Gotcha: a placeholder image may not exist as a standalone file (2026.07.19)

The July edition's Investor Psychology video thumbnail was never saved as its own file -
it only existed embedded inside the final DOCX. To recover it:

```powershell
$docx = "path\to\FINAL.docx"
$dest = "$env:TEMP\claude\docx_media_extract"
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory($docx, $dest)
# Images land in $dest\word\media\image1.png, image2.png, ... in insertion order.
# Use the Read tool on each candidate to identify which is which by eye, then copy
# the right one into Newsletter-Images with a proper YYYY.MM.DD-prefixed filename
# before referencing it in the manifest.
```

Check for this before assuming a manifest entry is missing/broken.

---

## Security Rules (non-negotiable - same as wordpress-post-publisher / wordpress-image-uploader)

1. **ALWAYS draft on create** - hardcoded, never overridden by manifest input.
2. **NEVER touch status on update** - the update path only ever sends `content`.
3. **NEVER hard-code credentials** anywhere in this skill, script, or a manifest file.
4. **Read `.env` fresh** every run - do not cache credentials between sessions.
5. **Abort rather than guess** - missing credential keys, an unreachable post_id, or any
   unresolved placeholder all stop the run before anything is written or pushed.
6. **Revocation:** if credentials are compromised, Mick revokes the Application Password
   from WP admin > Users > Poster Pete > Application Passwords; this skill then fails
   cleanly until new credentials are added to `.env`.

---

## Reusability / Relationship to Other Skills

- Distinct from `wordpress-image-uploader`, which is portfolio-screenshot-specific
  (folder + filename detection logic keyed to the four portfolio IDs). Newsletter media
  doesn't fit that convention closely enough to reuse it directly - this skill has its
  own generic "any local file -> WP media" uploader instead.
- The `update` post-mechanics (partial `content`-only POST) is new - `wordpress-post-publisher`
  v1.2 only documented `create`. Consider folding `update_post` into
  `wordpress-post-publisher` itself in a future pass so both skills share one
  implementation rather than two near-identical `requests.post` calls; not done yet
  because the two skills' create/update needs diverged just enough (content-agnostic
  post objects vs. a fixed newsletter manifest) that merging them felt premature after
  a single real run. Revisit once a second `create`-mode newsletter run has happened.

---

## Style Rules & Learnings

### 2026.07.19 - Manifest-driven, not folder-scanned (standing rule)
Newsletter image discovery is NOT automated the way portfolio screenshots are. Cedric
builds the manifest by hand each edition using Glob + visual confirmation (Read tool on
image files). This was a deliberate choice, not a shortcut: portfolio filenames follow a
tight, documented regex (see `wordpress-image-uploader`); newsletter filenames do not,
and forcing a brittle auto-detector would risk silently uploading the wrong screenshot.

### 2026.07.19 - Pre-flight existence check before any live call (standing rule)
Always verify every `local_path` in the manifest resolves (e.g. `Test-Path` in
PowerShell) before invoking the script. Uploads already sent to WordPress before a
later failure are not automatically rolled back.

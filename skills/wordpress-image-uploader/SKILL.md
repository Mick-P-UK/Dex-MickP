# SKILL: wordpress-image-uploader
**Version:** 1.0
**Created:** 2026.03.30
**Location (vault):** C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\wordpress-image-uploader\SKILL.md
**Location (mirror):** /mnt/skills/user/wordpress-image-uploader/SKILL.md
**Author:** Cedric (PAIDA)

---

## Purpose

Find portfolio screenshot images on Mick's PC and upload them to the WordPress media library on either diy-investors.com or diy-investors.ai.

Returns real media IDs, source URLs, and pixel dimensions for use in post HTML. No placeholder values are ever returned - only real data from the WordPress API.

This skill is called by `portfolio-post-creator` before HTML assembly. It has no knowledge of post content or WordPress post creation.

---

## Inputs

| Parameter | Type | Description |
|-----------|------|-------------|
| `portfolio_id` | string | One of: `uk-active-10`, `uk-active-10-yr2`, `us-active-10`, `us-active-10-yr2` |
| `year` | int | e.g. `2026` |
| `month` | int | e.g. `3` for March |
| `target_site` | string | `diy-investors-com` or `diy-investors-ai` |

---

## Portfolio Folder Paths

| Portfolio ID | Folder Path |
|-------------|-------------|
| `uk-active-10` | `C:\Users\pavey\Documents\0.2 - Areas (n)\02 - DIY - Investors\DIY - Portfolios\2026_UK_Active 10` |
| `uk-active-10-yr2` | `C:\Users\pavey\Documents\0.2 - Areas (n)\02 - DIY - Investors\DIY - Portfolios\2026_UK Active 10_Yr2` |
| `us-active-10` | `C:\Users\pavey\Documents\0.2 - Areas (n)\02 - DIY - Investors\DIY - Portfolios\2026_US_Active 10` |
| `us-active-10-yr2` | `C:\Users\pavey\Documents\0.2 - Areas (n)\02 - DIY - Investors\DIY - Portfolios\2026_US Active 10_Yr2` |

---

## Step 1: Find Images on Mick's PC

Use `Filesystem:list_directory` on the portfolio folder, then run the detection logic below in Python via `bash_tool`.

```python
import os, calendar
from datetime import datetime

def find_month_end_image(folder_listing, year, month):
    """
    folder_listing: list of filenames in the portfolio folder (from Filesystem:list_directory)
    Returns the matching month-end filename, or raises with a clear message.
    """
    last_day = calendar.monthrange(year, month)[1]
    date_prefix = f"{year}.{month:02d}.{last_day:02d}"

    exclude_keywords = [
        'newsletter', 'transactions', 'webnr', 'webinar',
        'after buying', 'after selling', 'purchases', 'adding',
        'initial', 'eighth', 'ninth', 'tenth', 'purchase'
    ]

    candidates = []
    for filename in folder_listing:
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        if not filename.startswith(date_prefix):
            continue
        name_lower = filename.lower()
        if any(kw in name_lower for kw in exclude_keywords):
            continue
        candidates.append(filename)

    if len(candidates) == 1:
        return candidates[0]
    elif len(candidates) == 0:
        raise FileNotFoundError(
            f"No month-end image found for {date_prefix}.\n"
            f"Expected a file starting with '{date_prefix}' that is not a "
            f"Newsletter, Transactions, or Webinar image."
        )
    else:
        # Try to narrow by inclusion keywords
        for filename in candidates:
            name_lower = filename.lower()
            if any(kw in name_lower for kw in ['month end', 'month-end', 'after 1', 'after 2']):
                return filename
        raise ValueError(
            f"Multiple month-end image candidates found for {date_prefix}:\n"
            + "\n".join(f"  - {f}" for f in candidates)
            + "\nPlease confirm which file to use."
        )


def find_transactions_image(folder_listing, year, month):
    """
    Returns the transactions filename, or None if no transactions file exists.
    Prefers files dated on the last day of the month.
    """
    month_name = datetime(year, month, 1).strftime('%B').lower()
    last_day = calendar.monthrange(year, month)[1]
    date_prefix = f"{year}.{month:02d}.{last_day:02d}"

    candidates = []
    for filename in folder_listing:
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        name_lower = filename.lower()
        if 'transaction' in name_lower and str(year) in filename:
            if month_name in name_lower or f"{month:02d}" in filename:
                candidates.append(filename)

    if not candidates:
        return None

    # Prefer month-end dated file
    for f in candidates:
        if f.startswith(date_prefix):
            return f

    return candidates[0]
```

### Known Naming Quirks

- UK Yr1: `Month End` (space) or `Month-End` (hyphen) - inconsistent
- UK Yr2: `After NNmths` (e.g. `After 13mths`) - no 'Month End' phrase
- US Yr1: `Month End` for most months; `Up by X.XXpc since 1st Jan` for January
- US Yr2: `month-end` (lowercase hyphen) for most months; `Up NN.NNpc_since 1st Jan` for January
- File extensions: mix of `.jpg` and `.JPG` - always compare case-insensitively

---

## Step 2: Copy Files to Claude's Computer

Once filenames are identified, copy them from Mick's PC to Claude's environment:

```python
# Use Filesystem:copy_file_user_to_claude for each file
# main_image_path = full path on Mick's PC (folder_path + "\\" + filename)
# transactions_image_path = full path on Mick's PC (or None)
```

---

## Step 3: Upload to WordPress Media Library

Read credentials from `.env`:

```python
def load_env(env_path=r"C:\Vaults\Mick's Vault\.env"):
    env = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env[key.strip()] = value.strip()
    return env
```

Site configuration:

| Site ID | URL key | User key | Password key |
|---------|---------|----------|-------------|
| `diy-investors-com` | `WP_DIY_INVESTORS_URL` | `WP_DIY_INVESTORS_USER` | `WP_DIY_INVESTORS_APP_PASSWORD` |
| `diy-investors-ai` | `WP_DIY_AI_URL` | `WP_DIY_AI_USER` | `WP_DIY_AI_APP_PASSWORD` |

Upload function:

```python
import requests, base64, mimetypes

def upload_image(site_url, user, app_password, local_path, filename):
    """
    Upload a single image to the WordPress media library.
    local_path: path on Claude's computer (after copy_file_user_to_claude)
    filename: desired filename on WordPress (use YYYY.MM.DD naming convention)
    Returns dict with media_id, source_url, width, height.
    ALWAYS reads real dimensions from media_details - never returns hardcoded values.
    """
    token = base64.b64encode(
        f"{user}:{app_password.replace(' ', '')}".encode()
    ).decode()

    mime_type, _ = mimetypes.guess_type(local_path)
    if not mime_type:
        mime_type = 'image/jpeg'

    headers = {
        'Authorization': f'Basic {token}',
        'Content-Disposition': f'attachment; filename="{filename}"',
        'Content-Type': mime_type,
    }

    with open(local_path, 'rb') as f:
        image_data = f.read()

    response = requests.post(
        f"{site_url}/wp-json/wp/v2/media",
        headers=headers,
        data=image_data,
        timeout=60
    )

    if response.status_code == 201:
        media = response.json()
        # ALWAYS use real dimensions from media_details
        # Never fall back to hardcoded defaults - raise instead
        media_details = media.get('media_details', {})
        width = media_details.get('width')
        height = media_details.get('height')
        if not width or not height:
            raise ValueError(
                f"WordPress did not return dimensions for {filename}. "
                f"media_details content: {media_details}"
            )
        return {
            'success': True,
            'media_id': media['id'],
            'source_url': media['source_url'],
            'width': width,
            'height': height,
            'alt_text': filename.replace('-', ' ').replace('_', ' ').rsplit('.', 1)[0]
        }
    else:
        return {
            'success': False,
            'status_code': response.status_code,
            'error': response.text,
            'filename': filename
        }
```

---

## Step 4: Output

Return a structured result to the calling skill:

```json
{
  "main_image": {
    "media_id": 15082,
    "source_url": "https://diy-investors.com/wp-content/uploads/2026/03/2026.03.31-UK-Active-10_11500-GBP_Month-End.jpg",
    "width": 1366,
    "height": 768,
    "alt_text": "2026.03.31 UK Active 10 11500 GBP Month End",
    "filename": "2026.03.31-UK-Active-10_11500-GBP_Month-End.jpg"
  },
  "transactions_image": {
    "media_id": 15083,
    "source_url": "https://diy-investors.com/wp-content/uploads/2026/03/2026.03.31-UK-Active-10_Transactions_March-2026.jpg",
    "width": 1366,
    "height": 220,
    "alt_text": "2026.03.31 UK Active 10 Transactions March 2026",
    "filename": "2026.03.31-UK-Active-10_Transactions_March-2026.jpg"
  }
}
```

If no transactions image exists, `transactions_image` is `null`.

---

## Error Handling

### Image not found on PC

```
Could not find the month-end image for [Portfolio] [Month YYYY].
Looked in: [folder path]
Expected: a file starting with '[YYYY.MM.DD]' that is not a Newsletter, Transactions, or Webinar image.
Files found with that date prefix:
  [list any files found with that prefix]
Please check the folder and confirm the filename.
```

### Upload failed

```
Image upload failed:
- File: [filename]
- HTTP Status: [code]
- Error: [message]
Action: Check Poster Pete role has 'upload_files' capability in WP Admin > Users.
```

### Dimensions not returned

```
WordPress accepted the upload but did not return image dimensions for [filename].
This should not happen. Check the WP media library to confirm the file uploaded correctly,
then provide the dimensions manually so the post HTML can be completed.
```

---

## Security Rules

- NEVER hard-code credentials
- Read .env fresh on every run
- NEVER log credential values to output, changelog, or memory
- This skill only functions in Claude Desktop (Filesystem MCP required to read .env)

---

## Style Rules & Learnings

### 2026.03.14 - Always use real dimensions (standing rule)
Never use hardcoded placeholder dimensions in img tags. WordPress will stretch or blur images
with incorrect dimensions. Always use `media_details.width` and `media_details.height` from
the API response. If these are absent, raise an error rather than fall back to defaults.

### 2026.03.14 - No featured image (standing rule)
This skill uploads images to the media library only. It does NOT set featured images.
Portfolio post images are embedded directly in the post body HTML. Setting a featured image
causes duplicates and incorrect positioning.

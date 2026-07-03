# SKILL: wordpress-post-publisher
**Version:** 1.2
**Created:** 2026.03.12
**Updated:** 2026.05.30 (v1.2 - tags field added to payload for portfolio post tagging)
**Prior update:** 2026.03.30 (v1.1 - image upload removed, delegated to wordpress-image-uploader skill)
**Location (vault):** C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\skills\wordpress-post-publisher\SKILL.md
**Location (mirror):** /mnt/skills/user/wordpress-post-publisher/SKILL.md
**Author:** Cedric (PAIDA)

---

## Purpose

Push fully-formed post objects to WordPress as drafts via the REST API. Generic and reusable - works for any content type (portfolio posts, company analysis, investing techniques, newsletters, etc.).

This skill handles ALL WordPress interaction. It has no knowledge of post content, house styles, or calculation rules.

---

## Site Configuration

| Site ID | URL | .env key (URL) | .env key (user) | .env key (password) |
|---------|-----|----------------|-----------------|---------------------|
| `diy-investors-com` | https://diy-investors.com | WP_DIY_INVESTORS_URL | WP_DIY_INVESTORS_USER | WP_DIY_INVESTORS_APP_PASSWORD |
| `diy-investors-ai` | https://diy-investors.ai | WP_DIY_AI_URL | WP_DIY_AI_USER | WP_DIY_AI_APP_PASSWORD |

---

## Credentials

Read from `.env` file at: `C:\Users\pavey\.env`

**NEVER hard-code credentials in this skill or in any script.**

Reading credentials via Filesystem MCP (Claude Desktop only):

```python
import os
from pathlib import Path

def load_env(env_path):
    env = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env[key.strip()] = value.strip()
    return env

env_path = r"C:\Users\pavey\.env"
credentials = load_env(env_path)
```

**Important:** This skill only functions in Claude Desktop (Filesystem MCP required to read .env). In claude.ai Web, the post object can be generated but not published.

---

## WordPress REST API

**Endpoint:** `POST /wp-json/wp/v2/posts`

**Authentication:** HTTP Basic Auth using Application Password.
Format: `username:application_password` encoded as Base64.

WordPress Application Password format: `xxxx xxxx xxxx xxxx xxxx xxxx`
Remove spaces when constructing the Basic Auth string.

```python
import requests
import base64
import json

def publish_draft(site_id, post_object, credentials):
    """
    Push a post object to WordPress as a draft.
    Returns the draft URL on success.
    """
    # Select site credentials
    if site_id == 'diy-investors-com':
        url = credentials['WP_DIY_INVESTORS_URL']
        user = credentials['WP_DIY_INVESTORS_USER']
        password = credentials['WP_DIY_INVESTORS_APP_PASSWORD'].replace(' ', '')
    elif site_id == 'diy-investors-ai':
        url = credentials['WP_DIY_AI_URL']
        user = credentials['WP_DIY_AI_USER']
        password = credentials['WP_DIY_AI_APP_PASSWORD'].replace(' ', '')
    else:
        raise ValueError(f"Unknown site_id: {site_id}")

    # Build auth header
    token = base64.b64encode(f"{user}:{password}".encode()).decode()
    headers = {
        'Authorization': f'Basic {token}',
        'Content-Type': 'application/json'
    }

    # Build WP post payload
    payload = {
        'title': post_object['title'],
        'content': post_object['html_body'],
        'status': 'draft',  # ALWAYS draft - never publish automatically
        'categories': [],   # Category by slug resolved below
        'tags': post_object.get('tags', []),  # Tag IDs passed directly (not resolved by slug)
        'date': (post_object['post_date'] + 'T12:00:00') if post_object.get('post_date') and len(post_object.get('post_date','')) == 10 else post_object.get('post_date', None)
    }

    # Resolve category slug to ID
    category_slug = post_object.get('category_slug')
    if category_slug:
        cat_response = requests.get(
            f"{url}/wp-json/wp/v2/categories",
            params={'slug': category_slug},
            headers=headers
        )
        categories = cat_response.json()
        if categories:
            payload['categories'] = [categories[0]['id']]

    # Create the draft post
    response = requests.post(
        f"{url}/wp-json/wp/v2/posts",
        headers=headers,
        data=json.dumps(payload)
    )

    if response.status_code == 201:
        result = response.json()
        return {
            'success': True,
            'draft_id': result['id'],
            'draft_url': result['link'],
            'edit_url': f"{url}/wp-admin/post.php?post={result['id']}&action=edit"
        }
    else:
        return {
            'success': False,
            'status_code': response.status_code,
            'error': response.text
        }
```

---

## Input Format

Accepts a structured post object from any content-creator skill:

```json
{
  "portfolio_id": "uk-active-10",
  "title": "Active 10 (UK) - 31st January 2026",
  "html_body": "[full HTML content]",
  "category_slug": "uk-active-10",
  "tags": [513],
  "target_site": "diy-investors-com",
  "expected_main_filename": "2026.01.31-UK-Active-10_10957.84-GBP_Month-End.jpg",
  "expected_transactions_filename": "2026.01.31-UK-Active-10_Transactions_January-2026.jpg",
  "post_date": "2026-02-27",
  "status": "draft"
}
```

Only `title`, `html_body`, `category_slug`, `target_site` are required. All other fields are informational. `tags` accepts an array of WordPress tag IDs (integers).

---

## Output

On success, return to Mick:

```
Draft created successfully:
- Title: [post title]
- Site: [site URL]
- Edit URL: [wp-admin edit link]
- Expected main image: [filename]
- Expected transactions image: [filename if applicable]

Next steps:
1. Open the edit URL above in your browser
2. Check the post preview looks correct
3. Publish when ready
```

On failure, return:
```
Draft creation failed:
- Site: [site URL]
- HTTP Status: [code]
- Error: [message]
- Action: Check credentials in .env file and verify Poster Pete account is active
```

---

## Image Upload

Image uploading is handled by the `wordpress-image-uploader` skill. This skill (publisher) receives post objects with image URLs and media IDs already resolved - it does not upload images.

Do NOT call WP media API from this skill. Always expect `html_body` to already contain real `source_url` values and real media IDs from the uploader.

**No featured image:** Never set `featured_media` on any post. Portfolio images are embedded in the post body only.

---

## Security Rules (non-negotiable)

1. **ALWAYS post as draft** - `status: 'draft'` is hardcoded. Never change to `publish` without explicit Mick instruction per-post.
2. **NEVER store credentials** in this skill file, in chat, or in any generated script file.
3. **NEVER log credentials** to any output, changelog, or memory.
4. **Read .env fresh** each run - do not cache credentials between sessions.
5. **Application Password only** - never use Mick's main admin password.
6. **Revocation:** If credentials are compromised, Mick revokes the Application Password from WP admin > Users > Poster Pete > Application Passwords. This skill then fails cleanly until new credentials are added to .env.

---

## Reusability

This skill is content-agnostic. It can publish posts generated by any skill or written directly in chat, provided they conform to the input format above. Current and planned callers:

- `portfolio-post-creator` (active from 2026.03.12)
- `company-post-creator` (planned)
- `technique-post-creator` (planned)
- Ad-hoc posts written directly in chat (always available)

To use for an ad-hoc post, simply provide:
```
Publish this to [diy-investors-com / diy-investors-ai]:
Title: [post title]
Category: [category slug]
Content: [HTML or plain text]
```

---

## Error Handling

| Error | Likely cause | Action |
|-------|-------------|--------|
| 401 Unauthorized | Wrong credentials or App Password revoked | Check .env, verify Pete's account in WP admin |
| 404 Not Found | Wrong site URL or REST API disabled | Verify URL in .env, check WP REST API is enabled in Hostinger |
| 403 Forbidden | Pete's Editor role insufficient | Check Pete's role in WP admin > Users |
| 422 Unprocessable | Malformed post payload | Check category slug exists on target site |
| Connection error | Site unreachable | Check Hostinger status, verify URL |

---

## Style Rules & Learnings

### 2026.05.30 - Portfolio tags must be applied at publish time (standing rule)
- Every portfolio post must include the `tags` array in the post payload. The four portfolio tag IDs on diy-investors.com are: UK Active 10 = 513, UK Active 10 (Yr2) = 890, US Active 10 = 512, US Active 10 (Yr2) = 891. Tags are passed as integer IDs directly (not resolved by slug). The `tags` field is now included in the standard payload. Never omit tags from portfolio posts.

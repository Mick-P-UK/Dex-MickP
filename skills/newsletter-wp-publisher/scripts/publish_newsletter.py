"""
newsletter-wp-publisher: upload newsletter media to WordPress and push the
finished HTML to a post (create a new draft, or update an existing one).

Usage:
    python publish_newsletter.py <manifest.json>

See SKILL.md for the manifest schema and worked examples.
"""

import base64
import json
import mimetypes
import sys

import requests

ENV_PATH = r"C:\Users\pavey\.env"

SITE_KEYS = {
    "diy-investors-com": ("WP_DIY_INVESTORS_URL", "WP_DIY_INVESTORS_USER", "WP_DIY_INVESTORS_APP_PASSWORD"),
    "diy-investors-ai": ("WP_DIY_AI_URL", "WP_DIY_AI_USER", "WP_DIY_AI_APP_PASSWORD"),
}


def load_env(path):
    env = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def get_site_credentials(env, target_site):
    if target_site not in SITE_KEYS:
        raise ValueError(f"Unknown target_site '{target_site}'. Known sites: {list(SITE_KEYS)}")
    url_key, user_key, pass_key = SITE_KEYS[target_site]
    missing = [k for k in (url_key, user_key, pass_key) if k not in env]
    if missing:
        raise ValueError(
            f"Missing .env keys for '{target_site}': {missing}. "
            f"Cannot proceed - never fall back to a different site's credentials."
        )
    return env[url_key].rstrip("/"), env[user_key], env[pass_key]


def auth_header(user, app_password):
    token = base64.b64encode(f"{user}:{app_password.replace(' ', '')}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def upload_media(site_url, user, app_password, local_path, wp_filename):
    mime_type, _ = mimetypes.guess_type(local_path)
    if not mime_type:
        mime_type = "application/octet-stream"

    headers = dict(auth_header(user, app_password))
    headers["Content-Disposition"] = f'attachment; filename="{wp_filename}"'
    headers["Content-Type"] = mime_type

    with open(local_path, "rb") as f:
        data = f.read()

    resp = requests.post(f"{site_url}/wp-json/wp/v2/media", headers=headers, data=data, timeout=90)
    if resp.status_code != 201:
        raise RuntimeError(f"Upload failed for {wp_filename}: {resp.status_code} {resp.text[:500]}")
    return resp.json()


def resolve_category_id(site_url, headers_json, category_slug):
    resp = requests.get(
        f"{site_url}/wp-json/wp/v2/categories", params={"slug": category_slug}, headers=headers_json, timeout=30
    )
    resp.raise_for_status()
    categories = resp.json()
    if not categories:
        raise ValueError(f"Category slug '{category_slug}' not found on target site.")
    return categories[0]["id"]


def main():
    if len(sys.argv) != 2:
        print("Usage: python publish_newsletter.py <manifest.json>")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        manifest = json.load(f)

    env = load_env(ENV_PATH)
    site_url, user, app_password = get_site_credentials(env, manifest["target_site"])
    headers_json = dict(auth_header(user, app_password))
    headers_json["Content-Type"] = "application/json"

    mode = manifest["mode"]
    if mode not in ("create", "update"):
        raise ValueError("manifest['mode'] must be 'create' or 'update'")

    # --- Pre-flight: confirm existing post state before touching anything (update mode) ---
    if mode == "update":
        post_id = manifest["post_id"]
        get_resp = requests.get(
            f"{site_url}/wp-json/wp/v2/posts/{post_id}",
            headers=headers_json,
            params={"context": "edit"},
            timeout=30,
        )
        if get_resp.status_code != 200:
            print(f"FAILED to read post {post_id}: {get_resp.status_code} {get_resp.text[:500]}")
            sys.exit(1)
        existing = get_resp.json()
        print(f"Existing post status: {existing.get('status')}")
        print(f"Existing post title:  {existing.get('title', {}).get('rendered')}")

    # --- Upload media, build placeholder -> real URL map ---
    html_path = manifest["html_path"]
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    print("\nUploading media...")
    for item in manifest.get("media", []):
        result = upload_media(site_url, user, app_password, item["local_path"], item["wp_filename"])
        html = html.replace(item["placeholder"], result["source_url"])
        print(f"  OK: {item['wp_filename']} -> {result['source_url']}")

    pdf_item = manifest.get("pdf")
    if pdf_item:
        result = upload_media(site_url, user, app_password, pdf_item["local_path"], pdf_item["wp_filename"])
        html = html.replace(pdf_item["placeholder"], result["source_url"])
        print(f"  OK: {pdf_item['wp_filename']} -> {result['source_url']}")

    for placeholder, real_value in manifest.get("extra_replacements", {}).items():
        html = html.replace(placeholder, real_value)

    # --- Safety check: never push content with a stale placeholder still in it ---
    unresolved = [tok for tok in ("YOUR_MEDIA_URL", "YOUR_PDF_URL") if tok in html]
    unresolved += [
        ph
        for ph in manifest.get("extra_replacements", {})
        if ph in html
    ]
    if unresolved:
        print(f"\nABORTING: unresolved placeholders remain: {unresolved}")
        print("HTML file NOT modified, post NOT touched. Fix the manifest and re-run.")
        sys.exit(1)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\nLocal HTML file updated in place: {html_path}")

    # --- Create or update the post ---
    if mode == "update":
        post_id = manifest["post_id"]
        update_resp = requests.post(
            f"{site_url}/wp-json/wp/v2/posts/{post_id}",
            headers=headers_json,
            json={"content": html},
            timeout=60,
        )
        if update_resp.status_code != 200:
            print(f"\nFAILED to update post {post_id}: {update_resp.status_code} {update_resp.text[:1000]}")
            sys.exit(1)
        result = update_resp.json()
        print("\nPost updated successfully (status untouched):")
    else:
        payload = {
            "title": manifest["title"],
            "content": html,
            "status": "draft",  # ALWAYS draft on create - never publish automatically
        }
        if manifest.get("category_slug"):
            payload["categories"] = [resolve_category_id(site_url, headers_json, manifest["category_slug"])]
        if manifest.get("tags"):
            payload["tags"] = manifest["tags"]
        if manifest.get("post_date"):
            payload["date"] = manifest["post_date"] + "T12:00:00"

        create_resp = requests.post(
            f"{site_url}/wp-json/wp/v2/posts", headers=headers_json, json=payload, timeout=60
        )
        if create_resp.status_code != 201:
            print(f"\nFAILED to create post: {create_resp.status_code} {create_resp.text[:1000]}")
            sys.exit(1)
        result = create_resp.json()
        print("\nDraft created successfully:")

    print(f"  Status:     {result.get('status')}")
    print(f"  Post ID:    {result.get('id')}")
    print(f"  Edit URL:   {site_url}/wp-admin/post.php?post={result.get('id')}&action=edit")
    print(f"  Preview:    {result.get('link')}")


if __name__ == "__main__":
    main()

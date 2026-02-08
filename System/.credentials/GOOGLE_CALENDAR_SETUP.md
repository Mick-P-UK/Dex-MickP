# Google Calendar API Setup Guide

This guide walks you through setting up Google Calendar API access for Dex.

## Prerequisites

- Google account with Google Calendar
- Python packages (install if needed):
  ```bash
  pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
  ```

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name (e.g., "Dex Calendar Integration")
4. Click "Create"

## Step 2: Enable Google Calendar API

1. In your new project, go to **APIs & Services** → **Library**
2. Search for "Google Calendar API"
3. Click on it, then click "Enable"

## Step 3: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in app name (e.g., "Dex Calendar")
   - Add your email as developer contact
   - Skip optional fields, click "Save and Continue"
   - On Scopes page, click "Save and Continue"
   - On Test users page, add your Google email, then "Save and Continue"
4. Back on Create OAuth client ID page:
   - Application type: **Desktop app**
   - Name: "Dex Calendar Client"
   - Click "Create"
5. Click "Download JSON" to download your credentials
6. Save the downloaded file as:
   ```
   System/.credentials/google_calendar_credentials.json
   ```

## Step 4: First-Time Authentication

1. The first time the calendar MCP runs, it will:
   - Open your web browser automatically
   - Ask you to sign in to Google
   - Request permission to access your calendar
   - Display a warning "Google hasn't verified this app" (click "Advanced" → "Go to [app name]")
2. Grant the permissions
3. The authentication token will be saved to:
   ```
   System/.credentials/google_calendar_token.pickle
   ```
4. Future uses won't require browser authentication (token auto-refreshes)

## Step 5: Test the Integration

After setup, test by running:

```bash
# List your calendars
calendar_list_calendars

# Get today's events
calendar_get_today
```

## Troubleshooting

### "Credentials not found" error

Make sure the file is saved exactly as:
```
System/.credentials/google_calendar_credentials.json
```

### "Access denied" or "403 error"

1. Check that Google Calendar API is enabled in Cloud Console
2. Verify you're signed in with the correct Google account
3. Try deleting `google_calendar_token.pickle` and re-authenticating

### "Google hasn't verified this app" warning

This is normal for personal projects. Click:
1. "Advanced"
2. "Go to [your app name] (unsafe)"
3. The app is safe - you created it yourself!

### Rate limits

Google Calendar API has these limits:
- 1,000,000 queries per day (plenty for personal use)
- 10 queries per second per user

## Security Notes

**Keep these files private:**
- `google_calendar_credentials.json` - Contains OAuth client secret
- `google_calendar_token.pickle` - Contains access token

**Never commit these to git!** They're already in `.gitignore`.

## Revoking Access

To revoke Dex's access to your calendar:
1. Go to [Google Account Permissions](https://myaccount.google.com/permissions)
2. Find "Dex Calendar" (or your app name)
3. Click "Remove Access"
4. Delete `google_calendar_token.pickle` from System/.credentials/

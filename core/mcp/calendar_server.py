#!/usr/bin/env python3
"""
Google Calendar MCP Server for Dex

Provides read/write access to Google Calendar via Google Calendar API.
Works on all platforms (Windows, macOS, Linux).

Tools:
- calendar_list_calendars: List all available calendars
- calendar_get_events: Get events for a date range
- calendar_get_today: Quick access to today's meetings
- calendar_create_event: Create a new event
- calendar_search_events: Search events by title
- calendar_delete_event: Delete an event
- calendar_get_next_event: Get the next upcoming event
- calendar_get_events_with_attendees: Get events with full attendee details
"""

import os
import json
import logging
import yaml
from pathlib import Path
from datetime import datetime, date, timedelta, timezone
from typing import Optional
import pickle

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# Google Calendar imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_CALENDAR_AVAILABLE = True
except ImportError:
    GOOGLE_CALENDAR_AVAILABLE = False
    logging.warning("Google Calendar API libraries not installed. Run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")

# Vault paths
VAULT_PATH = Path(os.environ.get('VAULT_PATH', Path.cwd()))
PEOPLE_DIR = VAULT_PATH / "05-Areas" / "People"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Credentials paths
CREDENTIALS_DIR = VAULT_PATH / "System" / ".credentials"
CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
TOKEN_FILE = CREDENTIALS_DIR / "google_calendar_token.pickle"
CLIENT_SECRET_FILE = CREDENTIALS_DIR / "google_calendar_credentials.json"

# User profile path
USER_PROFILE_PATH = VAULT_PATH / "System" / "user-profile.yaml"


def get_default_work_calendar() -> str:
    """Get the configured work calendar from user-profile.yaml.

    Returns the work_calendar if configured, otherwise tries work_email,
    otherwise falls back to 'primary'.
    """
    try:
        if USER_PROFILE_PATH.exists():
            with open(USER_PROFILE_PATH, 'r') as f:
                profile = yaml.safe_load(f)

            # Try calendar.work_calendar first
            if profile.get('calendar', {}).get('work_calendar'):
                return profile['calendar']['work_calendar']

            # Fall back to work_email
            if profile.get('work_email'):
                return profile['work_email']

            # Try constructing from email_domain
            if profile.get('name') and profile.get('email_domain'):
                name = profile['name'].lower().replace(' ', '.')
                domain = profile['email_domain']
                return f"{name}@{domain}"
    except Exception as e:
        logger.warning(f"Could not read work calendar from profile: {e}")

    return "primary"  # Fallback to primary Google calendar


# Cache the default calendar
DEFAULT_WORK_CALENDAR = get_default_work_calendar()
logger.info(f"Default work calendar: {DEFAULT_WORK_CALENDAR}")


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder for handling date/datetime objects"""
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


def get_google_calendar_service():
    """Authenticate and return Google Calendar API service.

    Uses OAuth 2.0 with token caching. On first run, opens browser for auth.
    """
    if not GOOGLE_CALENDAR_AVAILABLE:
        raise RuntimeError("Google Calendar API libraries not installed")

    if not CLIENT_SECRET_FILE.exists():
        raise FileNotFoundError(
            f"Google Calendar credentials not found at: {CLIENT_SECRET_FILE}\n\n"
            "Setup instructions:\n"
            "1. Go to https://console.cloud.google.com/\n"
            "2. Create a new project or select existing\n"
            "3. Enable Google Calendar API\n"
            "4. Create OAuth 2.0 credentials (Desktop app)\n"
            "5. Download credentials JSON\n"
            "6. Save as: {CLIENT_SECRET_FILE}"
        )

    creds = None

    # Load cached token if exists
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for future use
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def format_event(event: dict) -> dict:
    """Format Google Calendar event to match Dex calendar format."""
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))

    # Check if all-day event
    all_day = 'date' in event['start']

    # Parse dates
    if all_day:
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
    else:
        start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))

    return {
        'id': event['id'],
        'title': event.get('summary', '(No title)'),
        'start': start_dt.isoformat(),
        'end': end_dt.isoformat(),
        'all_day': all_day,
        'location': event.get('location', ''),
        'description': event.get('description', ''),
        'attendees': [
            {
                'name': att.get('displayName', att.get('email', 'Unknown')),
                'email': att.get('email', ''),
                'status': att.get('responseStatus', 'needsAction')
            }
            for att in event.get('attendees', [])
        ]
    }


def find_calendar_id(service, calendar_name: str) -> Optional[str]:
    """Find calendar ID by name or email. Returns None if not found."""
    if calendar_name == 'primary':
        return 'primary'

    try:
        calendar_list = service.calendarList().list().execute()
        for calendar in calendar_list.get('items', []):
            if (calendar.get('summary', '').lower() == calendar_name.lower() or
                calendar.get('id', '').lower() == calendar_name.lower()):
                return calendar['id']
    except HttpError as e:
        logger.error(f"Error finding calendar: {e}")

    return None


def normalize_name_for_filename(name: str) -> str:
    """Convert a name to a filename-safe format."""
    import re
    safe_name = re.sub(r'[^\w\s-]', '', name)
    safe_name = re.sub(r'\s+', '_', safe_name.strip())
    return safe_name


def find_person_page(name: str, email: str) -> Optional[Path]:
    """Find an existing person page by name or email."""
    name_variations = [
        normalize_name_for_filename(name),
        normalize_name_for_filename(email.split('@')[0].replace('.', ' ').replace('_', ' ').title()) if '@' in email else None
    ]
    name_variations = [n for n in name_variations if n]

    for folder in ['Internal', 'External']:
        folder_path = PEOPLE_DIR / folder
        if folder_path.exists():
            for file in folder_path.glob('*.md'):
                file_stem_lower = file.stem.lower().replace('_', ' ').replace('-', ' ')

                for name_var in name_variations:
                    name_var_lower = name_var.lower().replace('_', ' ')
                    if name_var_lower in file_stem_lower or file_stem_lower in name_var_lower:
                        return file

                    name_parts = name_var_lower.split()
                    if len(name_parts) >= 2:
                        if name_parts[0] in file_stem_lower and name_parts[-1] in file_stem_lower:
                            return file

                try:
                    content = file.read_text()
                    if email.lower() in content.lower():
                        return file
                except:
                    pass
    return None


# Initialize MCP server
app = Server("dex-calendar-mcp")


@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List all available calendar tools"""
    return [
        types.Tool(
            name="calendar_list_calendars",
            description="List all calendars available in Google Calendar",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        types.Tool(
            name="calendar_get_events",
            description="Get events from a specific calendar for a date range",
            inputSchema={
                "type": "object",
                "properties": {
                    "calendar_name": {
                        "type": "string",
                        "description": "Name of the calendar (e.g., 'Work' or 'user@example.com')"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format (defaults to today)"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date in YYYY-MM-DD format (defaults to start_date + 1 day)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of events to return (default: 50)",
                        "default": 50
                    }
                },
                "required": []
            }
        ),
        types.Tool(
            name="calendar_get_today",
            description="Quick access to today's events from a calendar",
            inputSchema={
                "type": "object",
                "properties": {
                    "calendar_name": {
                        "type": "string",
                        "description": "Calendar name (optional, defaults to your work calendar)"
                    }
                },
                "required": []
            }
        ),
        types.Tool(
            name="calendar_create_event",
            description="Create a new calendar event",
            inputSchema={
                "type": "object",
                "properties": {
                    "calendar_name": {
                        "type": "string",
                        "description": "Name of the calendar to add the event to"
                    },
                    "title": {
                        "type": "string",
                        "description": "Event title/summary"
                    },
                    "start_datetime": {
                        "type": "string",
                        "description": "Start datetime in 'YYYY-MM-DD HH:MM' format"
                    },
                    "duration_minutes": {
                        "type": "integer",
                        "description": "Duration in minutes (default: 30)",
                        "default": 30
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional event description/notes"
                    },
                    "location": {
                        "type": "string",
                        "description": "Optional event location"
                    }
                },
                "required": ["title", "start_datetime"]
            }
        ),
        types.Tool(
            name="calendar_search_events",
            description="Search for events by title across a calendar",
            inputSchema={
                "type": "object",
                "properties": {
                    "calendar_name": {
                        "type": "string",
                        "description": "Name of the calendar to search"
                    },
                    "query": {
                        "type": "string",
                        "description": "Search term to match against event titles"
                    },
                    "days_back": {
                        "type": "integer",
                        "description": "How many days back to search (default: 30)",
                        "default": 30
                    },
                    "days_forward": {
                        "type": "integer",
                        "description": "How many days forward to search (default: 30)",
                        "default": 30
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="calendar_delete_event",
            description="Delete a calendar event by its ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "calendar_name": {
                        "type": "string",
                        "description": "Name of the calendar containing the event"
                    },
                    "event_id": {
                        "type": "string",
                        "description": "Event ID (returned by other calendar tools)"
                    }
                },
                "required": ["event_id"]
            }
        ),
        types.Tool(
            name="calendar_get_next_event",
            description="Get the next upcoming event from a calendar",
            inputSchema={
                "type": "object",
                "properties": {
                    "calendar_name": {
                        "type": "string",
                        "description": "Calendar name (optional, defaults to your work calendar)"
                    }
                },
                "required": []
            }
        ),
        types.Tool(
            name="calendar_get_events_with_attendees",
            description="Get events with full attendee details (name, email, status)",
            inputSchema={
                "type": "object",
                "properties": {
                    "calendar_name": {
                        "type": "string",
                        "description": "Name of the calendar"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format (defaults to today)"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date in YYYY-MM-DD format (defaults to start_date + 1 day)"
                    }
                },
                "required": []
            }
        )
    ]


@app.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls"""

    arguments = arguments or {}

    try:
        service = get_google_calendar_service()
    except Exception as e:
        error_msg = f"Failed to connect to Google Calendar: {str(e)}"
        return [types.TextContent(type="text", text=json.dumps({
            "success": False,
            "error": error_msg
        }, indent=2))]

    if name == "calendar_list_calendars":
        try:
            calendar_list = service.calendarList().list().execute()
            calendars = [
                {
                    "title": cal.get('summary', ''),
                    "id": cal['id'],
                    "primary": cal.get('primary', False),
                    "access_role": cal.get('accessRole', '')
                }
                for cal in calendar_list.get('items', [])
            ]

            result = {
                "success": True,
                "calendars": [cal["title"] for cal in calendars],
                "count": len(calendars),
                "details": calendars
            }
        except HttpError as e:
            result = {"success": False, "error": str(e)}

        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "calendar_get_events":
        calendar_name = arguments.get("calendar_name", DEFAULT_WORK_CALENDAR)
        start_date = arguments.get("start_date", datetime.now().strftime("%Y-%m-%d"))

        start_dt = datetime.strptime(start_date, "%Y-%m-%d")

        if "end_date" in arguments:
            end_dt = datetime.strptime(arguments["end_date"], "%Y-%m-%d")
        else:
            end_dt = start_dt + timedelta(days=1)

        # Convert to RFC3339 format with timezone
        time_min = start_dt.replace(tzinfo=timezone.utc).isoformat()
        time_max = end_dt.replace(tzinfo=timezone.utc).isoformat()

        calendar_id = find_calendar_id(service, calendar_name) or calendar_name
        limit = arguments.get("limit", 50)

        try:
            events_result = service.events().list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                maxResults=limit,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = [format_event(e) for e in events_result.get('items', [])]

            result = {
                "success": True,
                "calendar": calendar_name,
                "date_range": f"{start_date} to {end_dt.strftime('%Y-%m-%d')}",
                "events": events,
                "count": len(events)
            }
        except HttpError as e:
            result = {"success": False, "error": str(e)}

        return [types.TextContent(type="text", text=json.dumps(result, indent=2, cls=DateTimeEncoder))]

    elif name == "calendar_get_today":
        calendar_name = arguments.get("calendar_name", DEFAULT_WORK_CALENDAR)
        today = datetime.now().strftime("%Y-%m-%d")

        arguments = {"calendar_name": calendar_name, "start_date": today}
        return await handle_call_tool("calendar_get_events", arguments)

    elif name == "calendar_create_event":
        calendar_name = arguments.get("calendar_name", DEFAULT_WORK_CALENDAR)
        title = arguments["title"]
        start_str = arguments["start_datetime"]
        duration = arguments.get("duration_minutes", 30)
        description = arguments.get("description", "")
        location = arguments.get("location", "")

        try:
            start_dt = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
            end_dt = start_dt + timedelta(minutes=duration)
        except ValueError:
            return [types.TextContent(type="text", text=json.dumps({
                "success": False,
                "error": f"Invalid datetime format. Use 'YYYY-MM-DD HH:MM', got: {start_str}"
            }, indent=2))]

        calendar_id = find_calendar_id(service, calendar_name) or calendar_name

        event = {
            'summary': title,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_dt.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_dt.isoformat(),
                'timeZone': 'UTC',
            },
        }

        try:
            created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
            result = {
                "success": True,
                "message": f"Event created: {created_event.get('htmlLink')}",
                "event": {
                    "id": created_event['id'],
                    "title": title,
                    "calendar": calendar_name,
                    "start": start_str,
                    "duration_minutes": duration
                }
            }
        except HttpError as e:
            result = {"success": False, "error": str(e)}

        return [types.TextContent(type="text", text=json.dumps(result, indent=2, cls=DateTimeEncoder))]

    elif name == "calendar_search_events":
        calendar_name = arguments.get("calendar_name", DEFAULT_WORK_CALENDAR)
        query = arguments["query"]
        days_back = arguments.get("days_back", 30)
        days_forward = arguments.get("days_forward", 30)

        start_dt = datetime.now() - timedelta(days=days_back)
        end_dt = datetime.now() + timedelta(days=days_forward)

        time_min = start_dt.replace(tzinfo=timezone.utc).isoformat()
        time_max = end_dt.replace(tzinfo=timezone.utc).isoformat()

        calendar_id = find_calendar_id(service, calendar_name) or calendar_name

        try:
            events_result = service.events().list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                q=query,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = [format_event(e) for e in events_result.get('items', [])]

            result = {
                "success": True,
                "query": query,
                "calendar": calendar_name,
                "events": events,
                "count": len(events)
            }
        except HttpError as e:
            result = {"success": False, "error": str(e)}

        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "calendar_delete_event":
        calendar_name = arguments.get("calendar_name", DEFAULT_WORK_CALENDAR)
        event_id = arguments["event_id"]

        calendar_id = find_calendar_id(service, calendar_name) or calendar_name

        try:
            service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
            result = {
                "success": True,
                "message": f"Event deleted: {event_id}"
            }
        except HttpError as e:
            result = {"success": False, "error": str(e)}

        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "calendar_get_next_event":
        calendar_name = arguments.get("calendar_name", DEFAULT_WORK_CALENDAR)

        now = datetime.now(timezone.utc).isoformat()
        calendar_id = find_calendar_id(service, calendar_name) or calendar_name

        try:
            events_result = service.events().list(
                calendarId=calendar_id,
                timeMin=now,
                maxResults=1,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            items = events_result.get('items', [])
            if not items:
                result = {
                    "success": True,
                    "message": "No upcoming events found",
                    "next_event": None
                }
            else:
                result = {
                    "success": True,
                    "next_event": format_event(items[0])
                }
        except HttpError as e:
            result = {"success": False, "error": str(e)}

        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "calendar_get_events_with_attendees":
        calendar_name = arguments.get("calendar_name", DEFAULT_WORK_CALENDAR)
        start_date = arguments.get("start_date", datetime.now().strftime("%Y-%m-%d"))

        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        if "end_date" in arguments:
            end_dt = datetime.strptime(arguments["end_date"], "%Y-%m-%d")
        else:
            end_dt = start_dt + timedelta(days=1)

        time_min = start_dt.replace(tzinfo=timezone.utc).isoformat()
        time_max = end_dt.replace(tzinfo=timezone.utc).isoformat()

        calendar_id = find_calendar_id(service, calendar_name) or calendar_name

        try:
            events_result = service.events().list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                maxResults=50,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = [format_event(e) for e in events_result.get('items', [])]

            # Enhance attendees with person page links
            for event in events:
                if "attendees" in event:
                    for att in event["attendees"]:
                        person_page = find_person_page(att.get('name', ''), att.get('email', ''))
                        att['has_person_page'] = person_page is not None
                        if person_page:
                            att['person_page'] = str(person_page.relative_to(VAULT_PATH))

            result = {
                "success": True,
                "calendar": calendar_name,
                "date_range": f"{start_date} to {end_dt.strftime('%Y-%m-%d')}",
                "events": events,
                "count": len(events)
            }
        except HttpError as e:
            result = {"success": False, "error": str(e)}

        return [types.TextContent(type="text", text=json.dumps(result, indent=2, cls=DateTimeEncoder))]

    else:
        return [types.TextContent(type="text", text=json.dumps({
            "error": f"Unknown tool: {name}"
        }, indent=2))]


async def _main():
    """Async main entry point for the MCP server"""
    logger.info("Starting Dex Calendar MCP Server")
    logger.info("Using Google Calendar API")

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="dex-calendar-mcp",
                server_version="2.0.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def main():
    """Sync entry point for console script"""
    import asyncio
    asyncio.run(_main())


if __name__ == "__main__":
    main()

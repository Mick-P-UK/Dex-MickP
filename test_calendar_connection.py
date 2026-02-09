#!/usr/bin/env python3
"""Test Google Calendar connection"""
import sys
from pathlib import Path

# Add the MCP directory to path
sys.path.insert(0, str(Path('core/mcp')))

try:
    from calendar_server import get_google_calendar_service
    
    print("Testing Google Calendar connection...")
    print(f"Credentials file: System/.credentials/google_calendar_credentials.json")
    
    service = get_google_calendar_service()
    print("✓ Successfully authenticated!")
    
    # List calendars
    calendar_list = service.calendarList().list().execute()
    calendars = calendar_list.get('items', [])
    
    print(f"\n✓ Found {len(calendars)} calendar(s):")
    for cal in calendars[:5]:
        name = cal.get('summary', 'Unknown')
        primary = " (PRIMARY)" if cal.get('primary') else ""
        print(f"  - {name}{primary}")
    
    # Get this week's events
    from datetime import datetime, timedelta
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=7)
    
    print(f"\nFetching events for this week ({start_of_week.strftime('%Y-%m-%d')} to {end_of_week.strftime('%Y-%m-%d')})...")
    
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_of_week.isoformat() + 'Z',
        timeMax=end_of_week.isoformat() + 'Z',
        maxResults=20,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    print(f"✓ Found {len(events)} event(s) this week")
    
    if events:
        print("\nUpcoming events:")
        for event in events[:5]:
            start = event['start'].get('dateTime', event['start'].get('date'))
            title = event.get('summary', '(No title)')
            print(f"  - {start[:10]} {start[11:16] if 'T' in start else ''} {title}")
    
    print("\n✅ Calendar connection is working!")
    
except FileNotFoundError as e:
    print(f"❌ Error: {e}")
    print("\nThe credentials file might be missing or in the wrong location.")
except Exception as e:
    print(f"❌ Error connecting to calendar: {e}")
    import traceback
    traceback.print_exc()

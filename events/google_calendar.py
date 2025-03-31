from datetime import timedelta
import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load credentials
SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDS_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')

def get_calendar_service():
    creds = service_account.Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    return build('calendar', 'v3', credentials=creds)

def add_event_to_google_calendar(event):
    """Sync event to Google Calendar."""
    service = get_calendar_service()
    
    event_body = {
        'summary': event.title,
        'description': event.description,
        'start': {'dateTime': event.date_time.isoformat(), 'timeZone': 'UTC'},
        'end': {'dateTime': (event.date_time + timedelta(hours=2)).isoformat(), 'timeZone': 'UTC'},
        'location': event.location,
    }

    created_event = service.events().insert(calendarId='primary', body=event_body).execute()
    return created_event.get('htmlLink')

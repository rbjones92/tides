# Robert Jones
# 10.4.22
# google calendar API connection


from pprint import pprint
import datetime
import os.path
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

NOW = datetime.datetime.utcnow().isoformat() + "Z"
CLIENT_SECRET_FILE = 'C:/Users/Robert.Jones/OneDrive - Central Coast Energy Services, Inc/Documents/Python_Projects/tides/gCal_API/client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly','https://www.googleapis.com/auth/calendar.events.readonly','https://www.googleapis.com/auth/calendar.events'] 

all_events = []


def main():

    ### Establish credentials and grab token #### 
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json',SCOPES)
    if not creds or not creds.valid:
        # Causes an error...
        '''
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
        '''
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE,SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json','w') as token:
            token.write(creds.to_json())

    service = build('calendar','v3',credentials=creds)

    return service

def list_events(service):

    ### LIST ALL EVENTS ### 

    # Find events
    events = service.events().list(calendarId='primary', timeMin = NOW, singleEvents=True, orderBy ='startTime').execute()
    # Append to list
    all_events.append(events)
    # Print
    pprint(all_events)


def create_event(service):
    ### CREATE AN EVENT ###
    colors = service.colors().get().execute()

    event_request_body = {
        'start' : {
            'dateTime': NOW,
        },
        'end': {
            'dateTime': NOW,
        },
        'summary': 'Testing Testicles',
        'description': 'testy testicles',
        'colorId': 5,
        'status': 'confirmed',
        'visibility':'public',
        'location':'Scrotumville'
    }

    response = service.events().insert(
        calendarId = 'robertbjones92@gmail.com',
        body = event_request_body
    ).execute()


if __name__ == '__main__':
    main()


### LIST EVENTS ### 
# list_events(main())
        
### CREATE EVENT ###
create_event(main())


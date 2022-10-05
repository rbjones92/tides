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


def connect():

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

    ### ADD TIDES EVENTS TO GOOGLE CALENDAR###

    import pandas as pd
    df = pd.read_csv('C:/Users/Robert.Jones/OneDrive - Central Coast Energy Services, Inc/Documents/Python_Projects/tides/transformed.csv/tide_transformed.csv')

    df_dates = df[df.columns[1]]
    df_ft = df[df.columns[2]]
    df_time = df[df.columns[3]]
    date_list = df_dates.values.tolist()
    ft_list = df_ft.values.tolist()
    time_list = df_time.values.tolist()

    colors = service.colors().get().execute()

    for j in range(len(date_list)):

        date_list[j] = datetime.datetime(int(date_list[j][0:4]),int(date_list[j][5:7]),int(date_list[j][8:]),int(time_list[j][0:2]),int(time_list[j][3:5])).isoformat()
        print(date_list[j])

    for i in range(len(date_list)):

        event_request_body = {
            'start' : {
                'dateTime': date_list[i],
                'timeZone': 'PST'
            },
            'end': {
                'dateTime': date_list[i],
                'timeZone': 'PST'
            },
            'summary': 'Beach Ebike Day',
            'description': f'tide at {ft_list[i]} feet',
            'colorId': 5,
            'status': 'confirmed',
            'visibility':'public',
            'location':'Moss Landing, CA'
        }

        response = service.events().insert(
            calendarId = 'robertbjones92@gmail.com',
            body = event_request_body
        ).execute()




### LIST EVENTS ### 
# list_events(connect())
        
### CREATE EVENT ###
# create_event(connect())


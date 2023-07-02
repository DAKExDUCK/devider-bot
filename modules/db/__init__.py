import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class DB:
    spreadsheet_id = '1CLxMwz2rr1pVh-xNn0L_sEUTYUUMJNtS8gfMRZkS5yo'
    range_name = 'A2:G'
    creds = None
    service = None

    def init():
        if os.path.exists('token.json'):
            DB.creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if not DB.creds or not DB.creds.valid:
            if DB.creds and DB.creds.expired and DB.creds.refresh_token:
                DB.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                DB.creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(DB.creds.to_json())

        DB.service = build('sheets', 'v4', credentials=DB.creds)

    def get_values(range=None):
        if range is None:
            range = DB.range_name

        return DB.service.spreadsheets().values().get(
            spreadsheetId=DB.spreadsheet_id, range=range
        ).execute().get('values', [])
    
    def insert_new(tg_id:str, tg_tag:str, name:str, city:str, mail:str, phone:str, group:int):
        values = [[ tg_id, tg_tag, name, city, mail, phone, group ]]
        body = {
            'values': values
        }
        result = DB.service.spreadsheets().values().append(
            spreadsheetId=DB.spreadsheet_id, range=DB.range_name,
            valueInputOption="USER_ENTERED", body=body).execute()
        return result
    
    def exists(tg_id):
        values = DB.get_values()
        return str(tg_id) in [ str(val[0]) for val in values ]

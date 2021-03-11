import os
import threading
from pathlib import Path
from django.utils import timezone
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def insert_into_spreadsheet(email) -> None:
    def _insert():
        scope = ['https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            os.path.join(Path(__file__).resolve().parent.parent, 'client_secret.json'), scope)
        client = gspread.authorize(creds)
        sheet = client.open("testing-api").sheet1
        sheet.insert_row([timezone.now().strftime('%m/%d/%Y %H:%M:%S'), email])

    x = threading.Thread(target=_insert)
    x.start()

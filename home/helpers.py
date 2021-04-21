import os
from pathlib import Path
from django.utils import timezone
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def insert_into_spreadsheet(email) -> None:
    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        os.path.join(Path(__file__).resolve().parent.parent, 'google-credentials.json'), scope)
    client = gspread.authorize(creds)
    sheet = client.open("Join Interniac (Responses)").sheet1
    if not _email_exists(email, sheet):
        sheet.append_row([timezone.now().strftime('%m/%d/%Y %H:%M:%S'), email])


def _email_exists(email, sheet) -> bool:
    email_list = sheet.col_values(2)

    for i in email_list:
        if i == email:
            return True

    return False

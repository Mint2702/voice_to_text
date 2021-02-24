import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from settings import settings


CREDS_PATH = settings.creds_path
TOKEN_PATH = settings.token_path

SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]


class Drive:
    def __init__(self):
        self.refresh_token()
        self.drive_service = build("drive", "v3", credentials=creds)
        self.dowload()

    def refresh_token(self):
        self.creds = None
        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH, "rb") as token:
                self.creds = pickle.load(token)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open(TOKEN_PATH, "wb") as token:
                pickle.dump(self.creds, token)

    def dowload(self):
        results = (
            service.files()
            .list(pageSize=10, fields="nextPageToken, files(id, name)")
            .execute()
        )
        items = results.get("files", [])

        if not items:
            print("No files found.")
        else:
            print("Files:")
            for item in items:
                print(u"{0} ({1})".format(item["name"], item["id"]))


test = Drive()

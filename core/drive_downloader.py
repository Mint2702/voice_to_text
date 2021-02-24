import os
import pickle
from io import FileIO
from loguru import logger

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from settings import settings


CREDS_PATH = settings.creds_path
TOKEN_PATH = settings.token_path

SCOPES = "https://www.googleapis.com/auth/drive"


class Drive:
    def __init__(self):
        self.refresh_token()
        self.service = build("drive", "v3", credentials=self.creds)
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
        file_id = "1ayGVdccCmS4BvQK5YL7l8mfd4PVrPEvd"
        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO("video.mp4", "wb")
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            logger.info("Download %d%%." % int(status.progress() * 100))

    def list_files(self):
        results = (
            self.service.files()
            .list(pageSize=10, fields="nextPageToken, files(id, name, mimeType)")
            .execute()
        )
        logger.info(results)


test = Drive()

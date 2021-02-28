import requests
from datetime import datetime, timedelta
import os

from sound_text_class import SoundToText
from drive_downloader import Drive
from youtube_downloader import Youtube


class EruditeRecords:
    def __init__(self):
        self.fromdate = f"{self.set_dates()} 9:00:00"
        self.todate = f"{self.set_dates()} 21:00:00"
        self.offline_rooms = {}
        records = self.get_all_records_per_day()
        self.drive = Drive()
        self.youtube = Youtube()
        self.convert_rooms(records)

    def set_dates(self) -> str:
        today = datetime.today().date() - timedelta(days=1)
        return today

    def get_all_records_per_day(self) -> list:
        params = {"fromdate": self.fromdate, "todate": self.todate}
        r = requests.get("https://nvr.miem.hse.ru/api/erudite/records", params=params)
        return r.json()

    def convert_rooms(self, records: list):
        for record in records:
            if record["type"] == "Offline":
                room_name = record["room_name"]
                start_time = record["start_time"]
                start_time = start_time[:10]
                if not self.check_if_offline(room_name, record["type"], start_time):
                    continue
                room_times = self.offline_rooms.get(room_name)
                if room_times is None:
                    self.offline_rooms[room_name] = [start_time]
                room_times.append(start_time)
                id = self.get_file_id(record["url"])
                self.drive.download(id)
                self.video = self.drive.file_name
            else:
                self.youtube.download(record["url"])
                self.video = self.youtube.file_name
            convertion = SoundToText(self.video)
            key_words = convertion.get_counter()
            record.update({"keywords": key_words})
            self.delete()

    def check_if_new(self, name: str, start_time: str) -> bool:
        start_time = start_time[:10]
        room_times = self.offline_rooms.get(name)
        if room_times is None or room_times.count(start_time) == 0:
            return True
        return False

    def get_file_id(self, url: str) -> str:
        id = url[32:]
        id = id[: len(id) - 8]
        return id

    def delete(self):
        os.remove(self.video)


check = EruditeRecords()

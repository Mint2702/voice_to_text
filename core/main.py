import requests
from datetime import datetime, timedelta

from sound_text_class import SoundToText


class EruditeRecords:
    def __init__(self):
        self.fromdate = f"{self.set_dates()} 9:00:00"
        self.todate = f"{self.set_dates()} 21:00:00"
        self.offline_rooms = []
        records = self.get_all_records_per_day()
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
            room_name = record["room_name"]
            if self.check_if_offline(room_name, record["type"]):
                continue
            self.offline_rooms.append(room_name)

    def check_if_offline(self, name: str, type: str) -> bool:
        if self.offline_rooms.count(name) == 0 and type == "Offline":
            return False
        return True


check = EruditeRecords()

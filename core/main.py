import requests
import os
from loguru import logger

from sound_text_class import SoundToText
from drive_downloader import Drive
from youtube_downloader import Youtube
from erudite_api import Erudite


class EruditeRecords:
    def __init__(self) -> None:
        self.drive = Drive()
        self.youtube = Youtube()
        self.erudite = Erudite()

    def get_all_records_per_day(self) -> list or None:
        return self.erudite.get_all_records_per_day()

    def filter_records(self, records: list) -> list:
        zoom_and_offline = []
        jitsi = []
        for record in records:
            if (
                record["type"] == "Offline"
                and not self.check_for_dublicate(zoom_and_offline, record)
            ) or record["type"] == "Zoom":
                zoom_and_offline.append(record)
            elif record["type"] == "Jitsi":
                jitsi.append(record)

        return zoom_and_offline, jitsi

    def check_for_dublicate(self, records: list, record: dict) -> bool:
        start_time = record["start_time"]
        start_time = start_time[:5]
        for record_offline in records:
            if (
                record_offline["room_name"] == record["room_name"]
                and record_offline["start_time"][:5] == start_time
            ):
                return True
        return False

    def convert_offline_zoom(self, records: list) -> None:
        for record in records:
            self.download_offline_zoom(record)
            key_words = self.convert()
            self.erudite.patch_record(key_words, record["id"])

    def convert_jitsi(self, records: list) -> None:
        for record in records:
            self.download_jitsi(record)
            key_words = self.convert()
            self.erudite.patch_record(key_words, record["id"])

    def download_jitsi(self, record: dict) -> None:
        self.youtube.download(record["url"])
        logger.info(f"Video - {self.youtube.vid.title} downloaded")
        self.video = self.youtube.file_name
        self.video = self.video[:-4]

    def download_offline_zoom(self, record: dict) -> None:
        id = self.get_file_id(record["url"])
        self.drive.download(id)
        self.video = self.drive.file_name
        self.video = self.video[:-4]

    def convert(self) -> list:
        convertion = SoundToText(self.video)
        key_words = convertion.get_list()
        del convertion
        self.delete()
        return key_words

    def get_file_id(self, url: str) -> str:
        id = url[32:]
        id = id[: len(id) - 8]
        return id

    def delete(self) -> None:
        os.remove(f"{self.video}.mp4")


@logger.catch
def main() -> None:
    conv = EruditeRecords()
    records = conv.get_all_records_per_day()
    offline_zoom, jitsi = conv.filter_records(records)
    # conv.convert_offline_zoom(offline_zoom)
    conv.convert_jitsi(jitsi)


if __name__ == "__main__":
    main()

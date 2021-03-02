import os
from loguru import logger

from sound_text_class import SoundToText
from drive_downloader import Drive
from youtube_downloader import Youtube
from erudite_api import Erudite


def convert_offline_zoom(records: list) -> None:
    for record in records:
        video_name = download_offline_zoom(record)
        key_words = convert(video_name)
        erudite.patch_record(key_words, record["id"])


def convert_jitsi(records: list) -> None:
    for record in records:
        video_name = download_jitsi(record)
        if video_name:
            key_words = convert(video_name)
            erudite.patch_record(key_words, record["id"])


def download_jitsi(record: dict) -> bool or str:
    status = youtube.download(record["url"])
    if status:
        logger.info(f"Video - {youtube.vid} downloaded")
        video_name = youtube.file_name
        video_name = video_name[:-4]
        return video_name
    return False


def download_offline_zoom(record: dict) -> str:
    id = get_file_id(record["url"])
    drive.download(id)
    video_name = drive.file_name
    video_name = video_name[:-4]
    return video_name


def convert(video_name: str) -> list:
    convertion = SoundToText(video_name)
    convertion.convert_video_to_text()
    key_words = convertion.get_list()
    del convertion
    delete(video_name)
    return key_words


def get_file_id(url: str) -> str:
    id = url[32:]
    id = id[: len(id) - 8]
    return id


def delete(video_name: str = "video") -> None:
    os.remove(f"{video_name}.mp4")


@logger.catch
def main() -> None:
    global drive, youtube, erudite
    drive = Drive()
    youtube = Youtube()
    erudite = Erudite()

    records = erudite.get_all_records_per_day()
    offline_zoom, jitsi = erudite.filter_records(records)
    print(jitsi)

    # convert_offline_zoom(offline_zoom)
    convert_jitsi(jitsi)


if __name__ == "__main__":
    main()

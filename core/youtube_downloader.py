from os import rename
from pytube import YouTube
from loguru import logger


class Youtube:
    @staticmethod
    def download(url: str, name: str = "video.mp4") -> str:
        """ Downloads video from youtube and reames it """

        if not name.endswith(".mp4"):
            raise Exception("Invalid file format")

        try:
            vid = YouTube(url).streams.first().download()
            logger.info("Downloading video")
            rename(vid, name)
        except Exception:
            logger.error("Error while downloading video from Youtube")
            return None, name

        return vid, name

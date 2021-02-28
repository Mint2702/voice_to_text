from os import rename
from pytube import YouTube, exceptions
from loguru import logger


class Youtube:
    def __init__(self):
        pass

    def download(self, url: str, name: str = "video.mp4") -> str:
        """ Downloads video from youtube and reames it """

        name = self.check_repair_name(name)
        self.file_name = name
        try:
            vid = YouTube(url).streams.first().download()
            rename(vid, name)
        except exceptions.VideoUnavailable:
            logger.error("Video not found in YouTube")

        return name

    def check_repair_name(self, name: str) -> str:
        """ Checks if name ends with .mp4, ads it if not """

        if not name.endswith(".mp4"):
            name += ".mp4"

        return name


# test = Youtube()
# name = test.download("https://www.youtube.com/watcsdvsh?v=HjPRvcxbxcbGpYVL_s", "new")

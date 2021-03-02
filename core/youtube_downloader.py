from os import rename
from pytube import YouTube, exceptions
from loguru import logger


class Youtube:
    def __init__(self):
        pass

    def download(self, url: str, name: str = "video.mp4") -> bool:
        """ Downloads video from youtube and reames it """

        name = self.check_repair_name(name)
        self.file_name = name
        try:
            self.vid = YouTube(url).streams.first().download()
            logger.info("Downloading video")
            rename(self.vid, name)
        except:
            logger.error("Error while downloading video from Youtube")
            return False

        return True

    def check_repair_name(self, name: str) -> str:
        """ Checks if name ends with .mp4, ads it if not """

        if not name.endswith(".mp4"):
            name += ".mp4"

        return name


# test = Youtube()
# name = test.download("https://www.youtube.com/watch?v=jcsL6xefiRc", "name")

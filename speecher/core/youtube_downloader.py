import pafy
from loguru import logger
import subprocess
import os


class Youtube:
    @staticmethod
    def download(url: str, name: str = "video.mp4") -> str:
        """ Downloads video from youtube and reames it """

        if not name.endswith(".mp4"):
            raise Exception("Invalid file format")

        try:
            vid = pafy.new(url, basic=True, gdata=False)
            duration_hour = int(vid.duration[:2])
            duration_minutes = int(vid.duration[3:5])
            if duration_hour > 0 or duration_minutes > 10:
                stream = vid.getbest()
                print(stream.mediatype)
                vid_title = f"{vid.title}.mp4"
                logger.info("Downloading video")
                stream.download(quiet=True, filepath=f"core/video.m3u8")
                subprocess.call("ls")
                subprocess.call(
                    f"ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -i core/video.m3u8 -c copy -bsf:a aac_adtstoasc core/video.mp4",
                    shell=True,
                )
                os.remove("video.m3u8")
                return vid_title, name
            else:
                logger.warning(f"Video {vid.title} is too short")
                return None, name
        except Exception as err:
            logger.error(f"Error while downloading video from YouTube - {err}")
            return None, name

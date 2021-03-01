from pydub import AudioSegment
import math
import speech_recognition as speech_recog
import subprocess
import os
from loguru import logger
from collections import Counter

from settings import settings


class SoundToText:
    COMMON = settings.common_words.split("\n")
    SOUND_WAV = "sound.wav"
    SOUND_AAC = "sound.aac"

    def __init__(self, name: str, lang: str = "ru-RU") -> None:
        self.text = ""
        self.video_to_sound(name)
        names_list = self.split()
        self.convert(names_list, lang)
        self.text = self.text.split(" ")
        self.clear_words()
        print(self.get_counter())

    def __del__(self) -> None:
        try:
            os.remove(self.SOUND_WAV)
            os.remove(self.SOUND_AAC)
        except:
            pass

    def split(self) -> list:
        """ Splits video by 1-minute length pieces """

        split_wav = SplitAudio(self.SOUND_WAV)
        return split_wav.multiple_split()

    def convert(self, names: list, lang: str = "ru-RU") -> None:
        """ Converts sound from every file given into a list of words, deletes converted .wav file """

        for name in names:
            logger.info(f"Converting {name} into text...")
            sample_audio = speech_recog.AudioFile(name)

            r = speech_recog.Recognizer()
            with sample_audio as source:
                audio_content = r.record(source)

            try:
                responce = r.recognize_google(audio_content, language=lang)
                self.text += f"{responce} "
            except speech_recog.UnknownValueError:
                pass
            os.remove(name)

    def clear_words(self) -> None:
        for word in self.text:
            if self.COMMON.count(word) != 0:
                while True:
                    try:
                        self.text.remove(word)
                    except:
                        break

    def get_counter(self) -> Counter:
        return Counter(self.text)

    def get_list(self) -> list:
        return self.text

    def video_to_sound(self, name: str) -> None:
        subprocess.call(
            f"ffmpeg -i {name}.mp4 -c:a copy -vn {self.SOUND_AAC}", shell=True
        )
        subprocess.call(f"ffmpeg -i {self.SOUND_AAC} {self.SOUND_WAV}", shell=True)


class SplitAudio:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.audio = AudioSegment.from_wav(self.filename)

    def get_duration_minutes(self) -> int:
        return self.audio.duration_seconds / 60

    def single_split(self, from_min: int, to_min: int, split_filename: str) -> None:
        """ Cuts a piece from an audio by given minutes """

        t1 = from_min * 60 * 1000
        t2 = to_min * 60 * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(split_filename, format="wav")

    def multiple_split(self, min_per_split: int = 1) -> list:
        """ Cuts a =n audio in fragments of the given length """

        total_mins = math.ceil(self.get_duration_minutes())
        names = []
        for i in range(0, total_mins, min_per_split):
            split_name = self.filename + "_" + str(i)
            names.append(split_name)
            self.single_split(i, i + min_per_split, split_name)
            logger.info(f" Video {i} cut from {self.filename}")
            if i == total_mins - min_per_split:
                logger.info("All splited successfully")

        return names


# test = SoundToText("videoLiza")

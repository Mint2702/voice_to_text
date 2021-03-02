from pydub import AudioSegment
import math
import speech_recognition as speech_recog
import subprocess
import os
from loguru import logger
from collections import Counter
import re


class SoundToText:
    SOUND_WAV = "sound.wav"
    SOUND_AAC = "sound.aac"

    def __init__(self, name: str = "video", lang: str = "ru-RU") -> None:
        self.taboo = re.split(",|\n", self.read_file())
        self.text = ""
        self.name = name
        self.lang = lang

    def __del__(self) -> None:
        try:
            os.remove(self.SOUND_WAV)
            os.remove(self.SOUND_AAC)
        except:
            pass

    def read_file(self) -> list:
        f = open("taboo.txt", "r")
        return f.read()

    def convert_video_to_text(self) -> None:
        self.video_to_sound(self.name)
        names_list = self.split()
        self.convert_audio_to_text(names_list, self.lang)
        self.text = self.text.split(" ")
        self.clear_words()
        logger.info(f"Words found - {self.get_counter()}")

    def video_to_sound(self, name: str) -> None:
        subprocess.call(f"ffmpeg -i {name}.mp4 -c:a copy -vn {self.SOUND_AAC}", shell=True)
        subprocess.call(f"ffmpeg -i {self.SOUND_AAC} {self.SOUND_WAV}", shell=True)

    def split(self) -> list:
        """ Splits video by 1-minute length pieces """

        split_wav = SplitAudio(self.SOUND_WAV)
        return split_wav.multiple_split()

    def convert_audio_to_text(self, names: list, lang: str = "ru-RU") -> None:
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
        print(self.taboo)
        for word in self.text:
            if word.lower() in self.taboo or len(word) < 2:
                self.text = list(filter((word).__ne__, self.text))

    def get_counter(self) -> Counter:
        return Counter(self.text)

    def get_set(self) -> list:
        return set(self.text)


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


# test = SoundToText("videoL")
# test.convert_video_to_text()

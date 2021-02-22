from pydub import AudioSegment
import math
import speech_recognition as speech_recog
import subprocess
import os
from loguru import logger


class SoundToText:
    def __init__(self, name: str):
        self.common_words = ""
        self.text = ""
        self.file_name = "sound.wav"
        subprocess.call(f"ffmpeg -i {name}.mp4 -c:a copy -vn sound.aac", shell=True)
        subprocess.call(f"ffmpeg -i sound.aac {self.file_name}", shell=True)
        names_list = self.split()
        self.convert(names_list)
        self.parce_text()
        self.clear_words()
        print(self.text)

    def __del__(self):
        os.remove(self.file_name)
        os.remove("sound.aac")

    def split(self) -> list:
        split_wav = SplitAudio(self.file_name)
        return split_wav.multiple_split(min_per_split=1)

    def convert(self, names: list):
        for name in names:
            logger.info(f"Converting {name} into text...")
            sample_audio = speech_recog.AudioFile(name)

            r = speech_recog.Recognizer()
            with sample_audio as source:
                # r.adjust_for_ambient_noise(source)  -  Noise clearence, sometimes decreases the accuracy of the convertion
                audio_content = r.record(source)

            try:
                responce = r.recognize_google(audio_content, language="ru-RU")
                self.text += f"{responce} "
            except speech_recog.UnknownValueError:
                pass
            os.remove(name)

    def parce_text(self):
        self.text = self.text.split(" ")

    def clear_words(self):
        for word in self.text:
            if len(word) < 3:
                self.text.remove(word)


class SplitAudio:
    def __init__(self, filename: str):
        self.filename = filename
        self.audio = AudioSegment.from_wav(self.filename)

    def get_duration(self) -> int:
        return self.audio.duration_seconds

    def single_split(self, from_min: int, to_min: int, split_filename: str):
        t1 = from_min * 60 * 1000
        t2 = to_min * 60 * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(split_filename, format="wav")

    def multiple_split(self, min_per_split: int) -> list:
        total_mins = math.ceil(self.get_duration() / 60)
        names = []
        for i in range(0, total_mins, min_per_split):
            split_fn = str(i) + "_" + self.filename
            names.append(split_fn)
            self.single_split(i, i + min_per_split, split_fn)
            logger.info(str(i) + " Done")
            if i == total_mins - min_per_split:
                logger.info("All splited successfully")

        return names


test = SoundToText("video")

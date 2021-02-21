from pydub import AudioSegment
import math


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
            print(str(i) + " Done")
            if i == total_mins - min_per_split:
                print("All splited successfully")

        return names

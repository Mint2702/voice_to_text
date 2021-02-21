import speech_recognition as speech_recog
import time
import subprocess

from sep import SplitAudio


subprocess.call(["ffmpeg", "-i", "au.m4a", "au.wav"])


file_init = "au2.wav"
split_wav = SplitAudio(file_init)
names = split_wav.multiple_split(min_per_split=1)

for name in names:
    print(name)
    sample_audio = speech_recog.AudioFile(name)

    r = speech_recog.Recognizer()
    with sample_audio as source:
        r.adjust_for_ambient_noise(source)
        audio_content = r.record(source)

    print(r.recognize_google(audio_content, language="ru-RU"))
    time.sleep(2)

#!/usr/bin/env python3
import speech_recognition as sr
import os

# Suppress ALSA warnings
# os.environ['ALSA_PCM_CARD'] = 'default'
# os.environ['ALSA_MIXER_CARD'] = 'default'

# Redirect stderr to suppress ALSA lib errors (optional)
# Uncomment the next two lines if you want to completely hide ALSA errors
devnull = os.open(os.devnull, os.O_WRONLY)
os.dup2(devnull, 2)

r = sr.Recognizer()


def convert_speech_to_text() -> str:
    """Convert speech to text using the default microphone."""
    with sr.Microphone() as source:
        audio_data = r.record(source, duration=5)
        print("Recognizing...")
        try:
            text = r.recognize_google(audio_data)
        except sr.UnknownValueError:
            print("Didn't receive any audio input.")
            text = ""
    return text

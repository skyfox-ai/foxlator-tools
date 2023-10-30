
import logging
import speech_recognition as sr  # type: ignore
from stt_test.stt_providers.ISTTBase import ISSTBase


class Sphinx(ISSTBase):

    MODEL_SIZES = []

    def _init_values(self):
        pass

    def _before_all(self, model_size: str):
        pass

    def _audio_to_text(self, recognizer: sr.Recognizer, audio: sr.AudioData) -> str:
        return recognizer.recognize_sphinx(audio)  # type: ignore

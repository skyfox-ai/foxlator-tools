
import speech_recognition as sr  # type: ignore
from stt_test.stt_providers.ISTTBase import ISSTBase


class Sphinx(ISSTBase):

    MODEL_SIZES = []

    def _before_all(self, model_size: str):
        pass

    def _audio_to_text(self, audio: sr.AudioData) -> str:
        return self._recognizer.recognize_sphinx(audio)  # type: ignore

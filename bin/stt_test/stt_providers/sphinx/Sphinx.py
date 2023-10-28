
import speech_recognition as sr  # type: ignore
from stt_providers.ISTTBase import ISSTBase


class Sphinx(ISSTBase):

    def _prepare_model(self):
        # TODO: TO IMPLMENT
        pass

    def _audio_to_text(self, recognizer: sr.Recognizer, audio: sr.AudioData) -> str:
        return recognizer.recognize_sphinx(audio)  # type: ignore

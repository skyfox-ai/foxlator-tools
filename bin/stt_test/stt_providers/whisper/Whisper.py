
import speech_recognition as sr  # type: ignore
from stt_test.stt_providers.ISTTBase import ISSTBase


class Whisper(ISSTBase):

    def _prepare_model(self):
        # TODO: TO IMPLMENT
        pass

    def _audio_to_text(self, recognizer: sr.Recognizer, audio: sr.AudioData) -> str:
        # TODO: TEST IT
        return recognizer.recognize_whisper(audio)  # type: ignore

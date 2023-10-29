
import speech_recognition as sr  # type: ignore
import ast
from stt_test.stt_providers.ISTTBase import ISSTBase


class Vosk(ISSTBase):

    def _prepare_model(self):
        # TODO: TO IMPLMENT
        pass

    def _audio_to_text(self, recognizer: sr.Recognizer, audio: sr.AudioData) -> str:
        return ast.literal_eval(
            recognizer.recognize_vosk(audio))['text']  # type: ignore


import logging
import speech_recognition as sr  # type: ignore
from stt_test.stt_providers.ISTTBase import ISSTBase


class Sphinx(ISSTBase):

    MODELS = []

    def _prepare_model(self, model_size: str):
        logging.info(
            'Models selection is not supported in Sphinx. Skipping...')

    def _audio_to_text(self, recognizer: sr.Recognizer, audio: sr.AudioData) -> str:
        return recognizer.recognize_sphinx(audio)  # type: ignore

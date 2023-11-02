
import logging
from pathlib import Path
import speech_recognition as sr  # type: ignore
import ast
from stt_test.utils.files import download_and_extract, prepare_dir
from stt_test.stt_providers.ISTTBase import ISSTBase
import os
import shutil
from vosk import Model  # type: ignore


class Vosk(ISSTBase):

    MODEL_SIZES = ['small', 'medium', 'big', 'large']
    MODEL_PATH = Path(os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'model'))

    def _download_model_and_extract(self, model_size: str):
        match model_size:
            case 'small':
                url = 'https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip'
            case 'medium':
                url = 'https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip'
            case 'big':
                url = 'https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip'
            case 'large':
                url = 'https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip'
            case _:
                raise Exception('Not supported model size')
        prepare_dir(Vosk.MODEL_PATH)
        logging.info(f"Downloading {model_size} model for Vosk\n")
        download_and_extract(url, Vosk.MODEL_PATH)

    def _prepare_model_dir(self):
        source_dir = next((d for d in Vosk.MODEL_PATH.iterdir()
                           if d.is_dir() and d.name.startswith("vosk")), None)
        if not source_dir:
            raise Exception("Model dir not found")
        file_names = os.listdir(source_dir)
        for file in file_names:
            shutil.move(os.path.join(source_dir, file), Vosk.MODEL_PATH)
        shutil.rmtree(source_dir, ignore_errors=True)

    def _before_all(self, model_size: str):
        self._download_model_and_extract(model_size)
        self._prepare_model_dir()
        model = Model(str(Vosk.MODEL_PATH))
        setattr(self._recognizer, 'vosk_model', model)

    def _audio_to_text(self, audio: sr.AudioData) -> str:
        return ast.literal_eval(self._recognizer.recognize_vosk(audio))[  # type: ignore
            'text']

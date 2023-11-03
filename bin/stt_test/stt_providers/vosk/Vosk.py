
import logging
from pathlib import Path
import speech_recognition as sr  # type: ignore
import ast
from stt_test.utils.file_utils import download_and_extract, prepare_dir
from stt_test.stt_providers.ISTTBase import ISTT
import os
import shutil
from vosk import Model, KaldiRecognizer  # type: ignore


class Vosk(ISTT):

    MODEL_SIZES = ['small', 'medium', 'big', 'large']
    MODEL_PATH = Path(os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'model'))
    _model: KaldiRecognizer

    def _download_model_and_extract(self, model_size: str):
        base_url = 'https://alphacephei.com/vosk/models/'
        models_urls = {
            'small': base_url + 'vosk-model-small-en-us-0.15.zip',
            'medium': base_url + 'vosk-model-en-us-0.22-lgraph.zip',
            'big': base_url + 'vosk-model-en-us-0.22.zip',
            'large': base_url + 'vosk-model-en-us-0.42-gigaspeech.zip',
        }
        url = models_urls.get(model_size)
        if not url:
            raise Exception('Not supported model size')
        prepare_dir(Vosk.MODEL_PATH)
        logging.info("Downloading %s model for Vosk\n", model_size)
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

    def _prepare_model(self, model_size: str):
        self._download_model_and_extract(model_size)
        self._prepare_model_dir()
        self._model = KaldiRecognizer(Model(str(Vosk.MODEL_PATH)), 16000)

    def _audio_to_text(self, audio: sr.AudioData, language: str | None = None) -> str:
        self._model.AcceptWaveform(  # type: ignore
            audio.get_raw_data(convert_rate=16000, convert_width=2))  # type: ignore
        results: str = str(self._model.FinalResult())  # type: ignore
        return ast.literal_eval(results)['text']


import logging
import speech_recognition as sr  # type: ignore
import ast
from stt_test.utils.files import download_and_extract, prepare_dir
from stt_test.stt_providers.ISTTBase import ISSTBase
import os
import shutil


class Vosk(ISSTBase):

    MODELS = ['small', 'medium', 'big', 'large']

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

    def _prepare_model(self, model_size: str):
        self._download_model_and_extract(model_size)
        source_dir = next((d for d in Vosk.MODEL_PATH.iterdir()
                           if d.is_dir() and d.name.startswith("vosk")), None)
        if not source_dir:
            raise Exception("Model dir not found")
        file_names = os.listdir(source_dir)
        for file in file_names:
            shutil.move(os.path.join(source_dir, file), Vosk.MODEL_PATH)
        shutil.rmtree(source_dir, ignore_errors=True)

    def _audio_to_text(self, recognizer: sr.Recognizer, audio: sr.AudioData) -> str:
        from vosk import Model, KaldiRecognizer  # type: ignore

        assert isinstance(audio, sr.AudioData)
        self.vosk_model = Model(Vosk.MODEL_PATH)
        rec = KaldiRecognizer(self.vosk_model, 16000)

        rec.AcceptWaveform(audio.get_raw_data(  # type: ignore
            convert_rate=16000, convert_width=2))
        return ast.literal_eval(rec.FinalResult())['text']  # type: ignore

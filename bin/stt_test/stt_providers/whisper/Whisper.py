
from typing import Dict  # type: ignore
import speech_recognition as sr  # type: ignore
from stt_test.stt_providers.ISTTBase import ISSTBase
import whisper as whisper_provider  # type: ignore
import numpy as np
from numpy.typing import NDArray
import soundfile as sf  # type: ignore
import torch
import io


class Whisper(ISSTBase):

    MODEL_SIZES = ['tiny', 'base', 'small', 'medium', 'large']
    _model: whisper_provider.Whisper

    def _set_model(self, model_size: str):
        if model_size not in Whisper.MODEL_SIZES:
            raise Exception('Not supported model size')
        self._model = whisper_provider.load_model(model_size)

    def _convert_audio(self, audio: sr.AudioData) -> NDArray[np.float32]:
        wav_bytes = audio.get_wav_data(convert_rate=16000)  # type: ignore
        wav_stream = io.BytesIO(wav_bytes)
        audio_array = sf.read(wav_stream)[0]  # type: ignore
        return audio_array.astype(np.float32)  # type: ignore

    def _before_all(self, model_size: str):
        self._set_model(model_size)

    def _audio_to_text(self, audio: sr.AudioData, language: str | None = None) -> str:
        result: Dict[str, str] = self._model.transcribe(  # type: ignore
            self._convert_audio(audio),
            language=language,
            task=None,
            fp16=torch.cuda.is_available(),
        )  # type: ignore
        return str(result['text'])

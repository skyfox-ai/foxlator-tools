
import speech_recognition as sr  # type: ignore
from stt_test.stt_providers.ISTTBase import ISSTBase
import whisper as whisper_provider  # type: ignore


class Whisper(ISSTBase):

    MODEL_SIZES = ['tiny', 'base', 'small', 'medium', 'large']

    def __init__(self) -> None:
        super().__init__()

    def _before_all(self,  model_size: str):
        if model_size not in Whisper.MODEL_SIZES:
            raise Exception('Not supported model size')
        model = whisper_provider.load_model(model_size)
        setattr(self._recognizer, "whisper_model", {model_size: model})

    def _audio_to_text(self, audio: sr.AudioData) -> str:
        return self._recognizer.recognize_whisper(  # type: ignore
            audio)

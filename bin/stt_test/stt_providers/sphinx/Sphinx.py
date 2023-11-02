
# type: ignore
import speech_recognition as sr
from stt_test.stt_providers.ISTTBase import ISSTBase
from pocketsphinx import pocketsphinx, Jsgf, FsgModel
import os
import site


class Sphinx(ISSTBase):

    MODEL_SIZES = []
    _model: pocketsphinx.Decoder

    def _prepare_model(self, model_size, language: str = 'en-US'):
        language_directory = os.path.join(
            os.path.realpath(site.getsitepackages()[0]), "speech_recognition", "pocketsphinx-data", language)
        acoustic_parameters_directory = os.path.join(
            language_directory, "acoustic-model")
        language_model_file = os.path.join(
            language_directory, "language-model.lm.bin")
        phoneme_dictionary_file = os.path.join(
            language_directory, "pronounciation-dictionary.dict")

        config = pocketsphinx.Decoder.default_config()
        config.set_string("-hmm", acoustic_parameters_directory)
        config.set_string("-lm", language_model_file)
        config.set_string("-dict", phoneme_dictionary_file)
        config.set_string("-logfn", os.devnull)
        self._model = pocketsphinx.Decoder(config)

    def _before_all(self, model_size: str, language: str = 'en-US'):
        self._prepare_model(model_size, language)

    def _audio_to_text(self, audio: sr.AudioData, language: str | None = None) -> str:
        raw_data = audio.get_raw_data(convert_rate=16000, convert_width=2)
        self._model.start_utt()
        self._model.process_raw(raw_data, False, True)
        self._model.end_utt()
        hypothesis = self._model.hyp()
        return hypothesis.hypstr if hypothesis else ""

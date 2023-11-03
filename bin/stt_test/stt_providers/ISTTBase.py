import json
import logging
from typing import List, Literal, Protocol, TypedDict
import speech_recognition as sr  # type: ignore
import time
from stt_test.utils.SentenceChecker import SentenceChecker
from stt_test.utils.test_data import get_audio_with_transcription


class STTResult(TypedDict):
    stt_trans: str
    trans: str
    similarity: float
    execution_time: float


class ISTT(Protocol):

    MODEL_SIZES: List[str]
    _sc: SentenceChecker
    _recognizer: sr.Recognizer

    def _init(self, model_size: str):
        self._sc = SentenceChecker()
        self._recognizer = sr.Recognizer()
        self._prepare_model(model_size)

    def _prepare_model(self, model_size: str):
        """Method for preparing models"""
        ...

    def _audio_to_text(self, audio: sr.AudioData, language: str) -> str:
        """Methods that runs STT on a single audio"""
        ...

    def _save_results(self, data: List[STTResult], model_size: str):
        with open(f'report_{self.__class__.__name__}_{model_size}.json', 'w') as fp:
            json.dump(data, fp)

    def run_analysis(self, file: str, trans: str, language: str):
        with sr.AudioFile(file) as source:
            audio = self._recognizer.record(source)  # type: ignore
        try:
            start_time = time.time()
            stt_trans = self._audio_to_text(audio, language)
            execution_time = time.time() - start_time
            similarity = self._sc.check_similarity(stt_trans, trans)
            return STTResult(stt_trans=stt_trans, trans=trans, similarity=similarity,
                             execution_time=execution_time)
        except sr.UnknownValueError as e:
            raise Exception(f'Error while analysing {file}.\n{e}\nSkiping ...')

    def run(self, audio_type: Literal['clean', 'other'], samples_num: int, model_size: str, language: str):
        self._init(model_size)
        all_results: List[STTResult] = []
        audio_with_trans = get_audio_with_transcription(audio_type)
        samples_num = samples_num if samples_num else len(audio_with_trans)
        for i, file_trans in enumerate(audio_with_trans.items()):
            file, trans = file_trans
            if len(all_results) == samples_num:
                break
            analysis = self.run_analysis(file, trans, language)
            logging.info(
                "[%d/%d] Similarity: %s\tTime: %s", i, samples_num, analysis['similarity'], analysis['execution_time'])
            all_results.append(analysis)
        self._save_results(all_results, model_size)

import logging
from pathlib import Path
from typing import List, Literal, Protocol, TypedDict
import speech_recognition as sr  # type: ignore
import time
from pathlib import Path
from os import path
from stt_test.utils.SentenceChecker import SentenceChecker
from stt_test.utils.test_data import get_audio_with_transcription


class STTResult(TypedDict):
    stt_trans: str
    trans: str
    similarity: float
    execution_time: float


class ISSTBase(Protocol):

    MODELS: List[str]
    MODEL_PATH = Path(path.join(path.dirname(
        path.realpath(__file__)), 'model'))

    def _prepare_model(self, model_size: str):
        """Method for preparing models"""
        ...

    def _audio_to_text(self, recognizer: sr.Recognizer, audio: sr.AudioData) -> str:
        """Methods that runs STT on a single audio"""
        ...

    def _save_results(self, data: List[STTResult]):
        # TODO: IMPLEMENT IT
        pass

    def run_analysis(self, audio_type: Literal['clean', 'other'], samples_num: int, model: str):
        self._prepare_model(model)
        recognizer = sr.Recognizer()
        sc = SentenceChecker()
        all_results: List[STTResult] = []
        for i, file_trans in enumerate(get_audio_with_transcription(audio_type).items()):
            file, trans = file_trans
            if len(all_results) == samples_num:
                break
            with sr.AudioFile(file) as source:
                audio = recognizer.record(source)  # type: ignore
            try:
                start_time = time.time()
                stt_trans = self._audio_to_text(recognizer, audio)
                execution_time = time.time() - start_time
                similarity = sc.check_similarity(stt_trans, trans)
                logging.info(
                    f"[{i}/{samples_num}] Similarity: {similarity}\tTime: {execution_time}")
                all_results.append(
                    STTResult(stt_trans=stt_trans, trans=trans, similarity=similarity,
                              execution_time=execution_time)
                )
            except sr.UnknownValueError:
                logging.error(f"Error while analysing {file}. Skiping ...")
        self._save_results(all_results)

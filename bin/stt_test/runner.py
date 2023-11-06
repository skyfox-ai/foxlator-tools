import argparse
import logging
import os
import speech_recognition as sr  # type: ignore
from stt_test.utils.SentenceChecker import SentenceChecker

from .report import create_general_report
from .stt_providers.ISTTBase import ISTT
from .utils.test_data import download_test_audio
from .stt_providers.sphinx.Sphinx import Sphinx
from .stt_providers.vosk.Vosk import Vosk
from .stt_providers.whisper.Whisper import Whisper


def _get_stt_provider(provider_name: str) -> ISTT:
    match provider_name:
        case Sphinx.__name__:
            return Sphinx()
        case Vosk.__name__:
            return Vosk()
        case Whisper.__name__:
            return Whisper()
        case _:
            logging.error("Incorrect provider delivered: %s", provider_name)
            exit()


def _run_single_stt(args: argparse.Namespace, report_dir: str):
    provider = _get_stt_provider(args.provider)
    model: str = args.model if "model" in args else ''
    provider.run(audio_type=args.audio_type, samples_num=args.samples_num,
                 model_size=model, language=args.lang, report_dir=report_dir)


def _run_all(args: argparse.Namespace, report_dir: str):
    recognizer = sr.Recognizer()
    sentence_checker = SentenceChecker()
    for provider in [Sphinx(), Vosk(), Whisper()]:
        if not provider.MODEL_SIZES:
            provider.run(audio_type=args.audio_type, samples_num=args.samples_num, model_size='',
                         language=args.lang, report_dir=report_dir, recognizer=recognizer, sentence_checker=sentence_checker)
            del provider._model  # type: ignore
        for model_size in provider.MODEL_SIZES:
            provider.run(audio_type=args.audio_type, samples_num=args.samples_num, model_size=model_size,
                         language=args.lang, report_dir=report_dir, recognizer=recognizer, sentence_checker=sentence_checker)
            del provider._model  # type: ignore


def run_stt_test(args: argparse.Namespace):
    if args.redownload_samples:
        download_test_audio(args.audio_type)
    report_dir = os.path.join(os.getcwd(), args.report_dir)
    if args.provider:
        if args.provider == "ALL":
            _run_all(args, report_dir)
        else:
            _run_single_stt(args, report_dir)
    if args.create_general_report:
        create_general_report(report_dir)

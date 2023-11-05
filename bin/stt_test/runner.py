import argparse
import logging
import os

from .report import create_general_report
from .stt_providers.ISTTBase import ISTT
from .utils.test_data import download_test_audio
from .stt_providers.sphinx.Sphinx import Sphinx
from .stt_providers.vosk.Vosk import Vosk
from .stt_providers.whisper.Whisper import Whisper


def get_stt_provider(provider_name: str) -> ISTT:
    match(provider_name):
        case Sphinx.__name__:
            return Sphinx()
        case Vosk.__name__:
            return Vosk()
        case Whisper.__name__:
            return Whisper()
        case _:
            logging.error("Incorrect provider delivered: %s", provider_name)
            exit()


def run_stt_test(args: argparse.Namespace):
    if args.redownload_samples:
        download_test_audio(args.audio_type)
    report_dir = os.path.join(os.getcwd(), args.report_dir)
    if args.provider:
        provider = get_stt_provider(args.provider)
        model = args.model if "model" in args else ''
        provider.run(args.audio_type, args.samples_num,
                     model, args.lang, report_dir)
    if args.create_general_report:
        create_general_report(report_dir)
    print(args)

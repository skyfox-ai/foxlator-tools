import argparse
import logging

from .utils.test_data import download_test_audio


def get_stt_provider(provider_name: str):
    match provider_name:
        case "sphinx":
            pass
        case "vosk":
            pass
        case "whisper":
            pass
        case _:
            logging.error(
                "Provider not found. Use --help to get available STT providers")


def run_stt_test(args: argparse.Namespace):
    if args.redownload_samples:
        download_test_audio(args.audio_type)
    if args.provider:
        get_stt_provider(args.provider)

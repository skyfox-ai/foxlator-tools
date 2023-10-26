import argparse

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
            print("Provider not found. Use --help to get available STT providers")


def stt_runner(args: argparse.Namespace):
    if args.redownload_samples:
        download_test_audio(args.audio_type)
    if args.provider:
        get_stt_provider(args.provider)

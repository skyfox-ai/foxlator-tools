import argparse
import logging
from .stt_providers.ISTTBase import ISSTBase


from .utils.test_data import download_test_audio


def get_stt_provider(provider_name: str) -> ISSTBase:
    try:
        return globals()[provider_name]
    except KeyError:
        logging.error(
            "Provider not found. Use --help to get available STT providers")
    except Exception as e:
        logging.error(e)
    finally:
        exit()


def run_stt_test(args: argparse.Namespace):
    if args.redownload_samples:
        download_test_audio(args.audio_type)
    if args.provider:
        provider = get_stt_provider(args.provider)
        provider.run_analysis(args.audio_type, args.samples_num)
    print(args)

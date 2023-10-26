import argparse


def get_stt_provider(provider_name: str):
    match provider_name:
        case _:
            pass


def run_stt_test(args: argparse.Namespace):
    if not args.provider:
        return print("No STT provider was selected. Use --help to see the available options")

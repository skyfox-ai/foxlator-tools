import argparse

from stt_test.stt_providers.whisper.Whisper import Whisper

parser = argparse.ArgumentParser(description="Whisper STT")

parser.add_argument("--model", type=str, choices=Whisper.MODEL_SIZES,
                    help=f"model size (default: {Whisper.MODEL_SIZES[1]})", default='base')

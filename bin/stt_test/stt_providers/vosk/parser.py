import argparse

from stt_test.stt_providers.vosk.Vosk import Vosk

parser = argparse.ArgumentParser(description="Vosk STT")

parser.add_argument("--model", type=str, choices=Vosk.MODEL_SIZES,
                    help=f"model size (default: {Vosk.MODEL_SIZES[1]})", default=f'{Vosk.MODEL_SIZES[1]}')

import argparse

from stt_test.stt_providers.vosk.Vosk import Vosk

parser = argparse.ArgumentParser(description="Vosk STT")

parser.add_argument("--model", type=str, choices=Vosk.MODELS,
                    help=f"model size (default: {Vosk.MODELS[1]})", default=f'{Vosk.MODELS[1]}')

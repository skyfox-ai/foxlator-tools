import argparse

parser = argparse.ArgumentParser(description="Whisper STT")

parser.add_argument("--model", type=str, choices=['tiny', 'base', 'small', 'medium', 'large'],
                    help="model size (default: base)", default='base')

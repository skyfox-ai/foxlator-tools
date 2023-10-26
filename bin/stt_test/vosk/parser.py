import argparse

parser = argparse.ArgumentParser(description="Vosk STT")

parser.add_argument("--model", type=str, choices=['small', 'medium', 'big', 'large'],
                    help="model size (default: medium)", default='medium')

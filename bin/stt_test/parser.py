import argparse
import pathlib
import os
from .stt_providers.sphinx.parser import parser as sphinx_parser
from .stt_providers.vosk.parser import parser as vosk_parser
from .stt_providers.whisper.parser import parser as whisper_parser


parser = argparse.ArgumentParser()

parser.add_argument("--lang",
                    type=str,
                    default='en',
                    help="Language in audio files (default: en). Currently only 'en' language is supported")

parser.add_argument("--samples-num",
                    type=int,
                    help="Number of audio files to be analyzed")

parser.add_argument("--raport-dest",
                    type=pathlib.Path,
                    help="Folder to which the report is to be generated",
                    default=os.getcwd())

parser.add_argument("--redownload-samples",
                    action="store_true",
                    help="If set then the audio test files will be downloaded again")

parser.add_argument("--audio-type",
                    type=str,
                    choices=['clean', 'other'],
                    default='clean',
                    help="Audio type based on https://www.openslr.org/12")


subparsers = parser.add_subparsers(dest='provider')
subparsers.add_parser(
    'sphinx', parents=[sphinx_parser], add_help=False, help="Analyze sphinx STT"
)
subparsers.add_parser(
    'vosk', parents=[vosk_parser], add_help=False, help="Analyze vosk STT"
)
subparsers.add_parser(
    'whisper', parents=[whisper_parser], add_help=False, help="Analyze whisper STT"
)

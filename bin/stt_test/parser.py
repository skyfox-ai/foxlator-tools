import argparse
import pathlib
import os
from .sphinx.parser import parser as sphinx_parser
from .vosk.parser import parser as vosk_parser
from .whisper.parser import parser as whisper_parser


parser = argparse.ArgumentParser()

parser.add_argument("--lang",
                    type=str,
                    help="Language in audio files (default: en). Currently only 'en' language is supported",
                    default='en')

parser.add_argument("--samples_num",
                    type=int,
                    help="Number of audio files to be analyzed")

parser.add_argument("--raport_dest",
                    type=pathlib.Path,
                    help="Folder to which the report is to be generated",
                    default=os.getcwd())

parser.add_argument("--audio_type",
                    type=str,
                    choices=['clean', 'other'],
                    help="Audio type based on https://www.openslr.org/12", default='clean')


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

import argparse
import pathlib

from .stt_providers.sphinx.Sphinx import Sphinx
from .stt_providers.vosk.Vosk import Vosk
from .stt_providers.whisper.Whisper import Whisper
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

parser.add_argument("--report-dir",
                    type=pathlib.Path,
                    help="Folder that should contain reports")

parser.add_argument("--redownload-samples",
                    action="store_true",
                    help="If set then the audio test files will be downloaded again")

parser.add_argument("--audio-type",
                    type=str,
                    choices=['clean', 'other'],
                    default='clean',
                    help="Audio type based on https://www.openslr.org/12")

parser.add_argument("--create-general-report",
                    action="store_true",
                    help="Create general raport from all STT reports")


subparsers = parser.add_subparsers(dest='provider', metavar="")
subparsers.add_parser(
    Sphinx.__name__, parents=[sphinx_parser], add_help=False, help="Analyze sphinx STT"
)
subparsers.add_parser(
    Vosk.__name__, parents=[vosk_parser], add_help=False, help="Analyze vosk STT"
)
subparsers.add_parser(
    Whisper.__name__, parents=[whisper_parser], add_help=False, help="Analyze whisper STT"
)
subparsers.add_parser(
    "ALL", add_help=False, help="Runs all STT analysis"
)

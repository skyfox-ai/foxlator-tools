#!/usr/bin/env python3.10

import argparse
import subprocess
import logging
from enum import Enum

import foxlator_lib as fll

from stt_test.parser import parser as stt_parser


def parse_description() -> str:
    interpreter = subprocess.run(
        ['which', 'python3.10'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    return f"""foxlator-tools is a help tool that includes useful features for foxlator, 
        backend library version: {fll.utils.get_version()}, interpreter used: '{interpreter}'"""


class Commands(Enum):
    test_stt = 'test-stt'


parser = argparse.ArgumentParser(
    description=parse_description()
)

parser.add_argument('--loglevel',
                    default='INFO',
                    type=str,
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                    help='Provide logging level (default: INFO)')
subparsers = parser.add_subparsers(dest='subparser_name')
subparsers.add_parser(
    Commands.test_stt.value,
    parents=[stt_parser],
    add_help=False,
    help="Tool for analyzing different STTs"
)

args = parser.parse_args()
logging.basicConfig(level=args.loglevel)

match args.subparser_name:
    case Commands.test_stt.value:
        from stt_test.runner import stt_runner
        stt_runner(args)
    case _:
        pass

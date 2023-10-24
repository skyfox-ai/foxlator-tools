import argparse
from enum import Enum
from stt_test.parser import parser as stt_parser


class Commands(Enum):
    test_stt = 'test-stt'


parser = argparse.ArgumentParser(
    description="foxltor-tools is a help tool that includes useful features for foxlator"
)

subparsers = parser.add_subparsers(dest='subparser_name')
subparsers.add_parser(
    Commands.test_stt.value,
    parents=[stt_parser],
    add_help=False,
    help="Tool for analyzing different STTs"
)

args = parser.parse_args()

match args.subparser_name:
    case Commands.test_stt.value:
        from stt_test.runner import run_stt_test
        run_stt_test(args)
    case _:
        pass

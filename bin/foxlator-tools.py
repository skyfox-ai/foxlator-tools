#!/usr/bin/env python3.10

import argparse
import subprocess
import logging
import requests

from enum import Enum

import foxlator_lib as fll

from stt_test.parser import parser as stt_parser


fll_version = fll.utils.get_version()


def get_latest_release_version() -> str:
    endpoint = 'https://pypi.org/pypi/foxlator-lib/json'
    response = requests.get(url=endpoint)
    return list(response.json()['releases'].keys())[-1]


def parse_description() -> str:
    interpreter = subprocess.run(
        ['which', 'python3.10'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    return f"""foxlator-tools is a help tool that includes useful features for foxlator, 
        backend library version: {fll_version}, interpreter used: '{interpreter}'"""


def check_version():
    pypi_version = get_latest_release_version()
    if (pypi_version != fll_version):
        logging.warning(
            "The newest foxlator-lib version (%s) is not installed, consider updating it", pypi_version)


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

check_version()

args = parser.parse_args()
logging.basicConfig(level=args.loglevel)

match args.subparser_name:
    case Commands.test_stt.value:
        from stt_test.runner import run_stt_test
        run_stt_test(args)
    case _:
        pass

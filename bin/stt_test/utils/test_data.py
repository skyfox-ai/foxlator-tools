
from os import path, listdir
from pathlib import Path
from typing import Dict, Literal
import logging

from stt_test.utils.file_utils import download_and_extract, prepare_dir

AUDIO_DIR = Path(path.join(path.dirname(
    path.realpath(__file__)), 'test_audio'))


def download_test_audio(type: Literal["clean", "other"]):
    prepare_dir(AUDIO_DIR)
    url = f'https://www.openslr.org/resources/12/dev-{type}.tar.gz'
    logging.info('Downloading audio files\n')
    download_and_extract(url, AUDIO_DIR)


def get_audio_with_transcription(type: Literal["clean", "other"]) -> Dict[str, str]:
    all_speakers_path = path.join(AUDIO_DIR, 'LibriSpeech', f'dev-{type}')
    if not all([path.exists(AUDIO_DIR), path.isdir(AUDIO_DIR), path.exists(all_speakers_path)]):
        logging.warning('%s not found. Auto-download starts...', AUDIO_DIR)
        download_test_audio(type)
    audo_files: Dict[str, str] = {}
    logging.info(
        'Mapping the transcription of the recording and the path to it...')
    for speaker_id in listdir(all_speakers_path):
        speaker_path = path.join(all_speakers_path, speaker_id)
        for chapter_id in listdir(speaker_path):
            chapter_path = path.join(speaker_path, chapter_id)
            with open(path.join(chapter_path, f"{speaker_id}-{chapter_id}.trans.txt"), 'r') as f:
                trans_file = f.readlines()
            for line in trans_file:
                audio_file_name, transcription = line.split(" ", 1)
                filepath = f"{path.join(chapter_path, audio_file_name)}.flac"
                audo_files[filepath] = transcription
    logging.info('Mapping has finished')
    return audo_files

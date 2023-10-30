
from os import remove
from pathlib import Path
import wget  # type: ignore
import shutil
import tarfile
import logging
import zipfile


def prepare_dir(path: Path):
    logging.info(f"test_audio dir preparation...")
    shutil.rmtree(path, ignore_errors=True)
    path.mkdir()


def download_and_extract(url: str, extract_dir: Path):
    package: str = str(wget.download(url))  # type: ignore
    if url.endswith('.zip'):
        with zipfile.ZipFile(package, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
    else:
        with tarfile.open(package, "r:gz") as tar:
            tar.extractall(path=extract_dir)
    logging.info(f'\nFile downloaded and extracted to {extract_dir}')
    remove(package)

import spacy
import logging
import sys
import os


class SentenceChecker:

    def __init__(self, model_name: str = "en_core_web_lg") -> None:
        self.nlp = self._get_spacy_nlp(model_name)

    def _get_spacy_nlp(self, model_name: str):
        if spacy.util.is_package(model_name):
            return spacy.load(model_name)
        self._download_model(model_name)
        return spacy.load(model_name)

    def _download_model(self, model_name: str):
        status = os.system(f"{sys.executable} -m spacy download {model_name}")
        if status != 0:
            raise Exception(
                "Error while downloading the sentence checker model")
        logging.info(f"Download completed")

    def check_similarity(self, sentence_1: str, sentence_2: str):
        return self.nlp(sentence_1.lower()).similarity(self.nlp(sentence_2.lower()))

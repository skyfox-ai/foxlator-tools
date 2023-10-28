import spacy
import subprocess
import logging


class SentenceChecker:

    def __init__(self, model_name: str = "en_core_web_lg") -> None:
        self.nlp = self._get_spacy_nlp(model_name)

    def _get_spacy_nlp(self, model_name: str):
        try:
            return spacy.load(model_name)
        except OSError:
            logging.info("Spacy model not found. Downloading...")
            try:
                self._download_model(model_name)
                return spacy.load(model_name)
            except subprocess.CalledProcessError:
                raise Exception(
                    "Error while downloading the model. Check the connection and try again")

    def _download_model(self, model_name: str):
        subprocess.run(
            f"python -m spacy download {model_name}", shell=True, check=True)
        logging.info(f"Download completed")

    def check_similarity(self, sentence_1: str, sentence_2: str):
        return self.nlp(sentence_1.lower()).similarity(self.nlp(sentence_2.lower()))

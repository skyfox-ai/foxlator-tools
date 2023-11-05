from sentence_transformers import SentenceTransformer  # type: ignore
from sentence_transformers import SentenceTransformer, util  # type: ignore


class SentenceChecker:

    def __init__(self, model_name: str = "paraphrase-multilingual-mpnet-base-v2") -> None:
        self.model = SentenceTransformer(model_name)

    def check_similarity(self, sentence_1: str, sentence_2: str) -> float:
        sentence_embeddings = self.model.encode(  # type: ignore
            [sentence_1, sentence_2])
        result = util.pytorch_cos_sim(
            sentence_embeddings[0], sentence_embeddings[1])
        return float(result.numpy()[0][0])

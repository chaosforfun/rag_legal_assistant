from typing import List

from sentence_transformers import SentenceTransformer

from .config import EMBED_MODEL_NAME

class EmbeddingModel:
    def __init__(self, model_name: str = EMBED_MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts, show_progress_bar=False).tolist()

from typing import List

from .embedding import EmbeddingModel
from .vector_store import VectorStore

class Retriever:
    def __init__(self, embed_model: EmbeddingModel, vector_store: VectorStore):
        self.embed_model = embed_model
        self.vector_store = vector_store

    def retrieve(self, query: str, k: int = 3) -> List[str]:
        query_emb = self.embed_model.embed([query])[0]
        results = self.vector_store.search(query_emb, k=k)
        return [text for text, _ in results]

from typing import List

from .retriever import Retriever
from .llm import LLMClient

class RAGPipeline:
    def __init__(self, retriever: Retriever, llm: LLMClient, top_k: int = 3):
        self.retriever = retriever
        self.llm = llm
        self.top_k = top_k

    def run(self, question: str) -> str:
        contexts = self.retriever.retrieve(question, k=self.top_k)
        answer = self.llm.generate(question, contexts)
        return answer

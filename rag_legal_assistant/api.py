from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .config import VECTOR_DIM
from .embedding import EmbeddingModel
from .vector_store import VectorStore
from .retriever import Retriever
from .llm import LLMClient
from .rag_pipeline import RAGPipeline

app = FastAPI(title="法规RAG助手")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

embedding_model = EmbeddingModel()
vector_store = VectorStore(dim=VECTOR_DIM)
retriever = Retriever(embedding_model, vector_store)
llm_client = LLMClient()
rag_pipeline = RAGPipeline(retriever, llm_client)

@app.post("/query")
def query_rag(req: QueryRequest):
    answer = rag_pipeline.run(req.question)
    return {"answer": answer}

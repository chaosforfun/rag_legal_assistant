from typing import List, Tuple

import numpy as np
import faiss
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import DATABASE_URL, VECTOR_DIM

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)

class Vector(Base):
    __tablename__ = "vectors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    doc_id = Column(Integer, nullable=False)
    dim = Column(Integer, default=VECTOR_DIM)
    values = Column(Text, nullable=False)

class VectorStore:
    def __init__(self, dim: int = VECTOR_DIM):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.store: List[str] = []

    def _deserialize(self, vec_text: str) -> List[float]:
        return [float(v) for v in vec_text.split(",") if v]

    def _serialize(self, vectors: List[List[float]]) -> List[str]:
        return [",".join(str(v) for v in vec) for vec in vectors]

    def add(self, embeddings: List[List[float]], texts: List[str]):
        vecs = np.array(embeddings).astype("float32")
        self.index.add(vecs)
        self.store.extend(texts)
        serialized = self._serialize(embeddings)

        session = self.Session()
        try:
            for text, vec in zip(texts, serialized):
                doc = Document(content=text)
                session.add(doc)
                session.flush()
                session.add(Vector(doc_id=doc.id, values=vec))
            session.commit()
        finally:
            session.close()

    def load_from_db(self):
        session = self.Session()
        try:
            vectors = session.query(Vector).all()
            docs = session.query(Document).all()
            doc_map = {doc.id: doc.content for doc in docs}
            if not vectors:
                return
            
            # 过滤出维度匹配的向量
            valid_embeddings = []
            valid_texts = []
            for v in vectors:
                emb = self._deserialize(v.values)
                if len(emb) == self.dim:
                    valid_embeddings.append(emb)
                    valid_texts.append(doc_map.get(v.doc_id, ""))
            
            if not valid_embeddings:
                return
                
            vecs = np.array(valid_embeddings).astype("float32")
            self.index.add(vecs)
            self.store = valid_texts
        finally:
            session.close()

    def search(self, query_emb: List[float], k: int = 3) -> List[Tuple[str, float]]:
        if self.index.ntotal == 0:
            self.load_from_db()
        query = np.array([query_emb]).astype("float32")
        distances, indices = self.index.search(query, k)
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx == -1 or idx >= len(self.store):
                continue
            results.append((self.store[idx], float(dist)))
        return results

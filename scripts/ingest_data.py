from pathlib import Path

from rag_legal_assistant.data_loader import load_documents
from rag_legal_assistant.embedding import EmbeddingModel
from rag_legal_assistant.vector_store import VectorStore

DATA_DIR = Path(__file__).resolve().parent.parent / "data/documents"


def main():
    docs = load_documents(str(DATA_DIR))
    if not docs:
        print("No documents found.")
        return

    embed_model = EmbeddingModel()
    vector_store = VectorStore(dim=768)

    texts = [d["text"] for d in docs]
    embeddings = embed_model.embed(texts)
    # 逐条添加文档到向量数据库
    # 因为 add 方法现在只支持单条数据插入
    for embedding, text in zip(embeddings, texts):
        vector_store.add(embedding, text)
    print(f"Indexed {len(texts)} documents.")


if __name__ == "__main__":
    main()

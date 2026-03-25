from pathlib import Path

from rag_legal_assistant.data_loader import load_legal_documents
from rag_legal_assistant.embedding import EmbeddingModel
from rag_legal_assistant.vector_store import VectorStore

DATA_DIR = Path(__file__).resolve().parent.parent / "data/legal"

def main():
    docs = load_legal_documents(str(DATA_DIR))
    if not docs:
        print("No documents found.")
        return

    embed_model = EmbeddingModel()
    vector_store = VectorStore(dim=768)

    texts = [d["text"] for d in docs]
    embeddings = embed_model.embed(texts)
    vector_store.add(embeddings, texts)
    print(f"Indexed {len(texts)} documents.")

if __name__ == "__main__":
    main()

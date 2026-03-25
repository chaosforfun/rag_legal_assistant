import os
from pathlib import Path
from typing import List

def load_legal_documents(data_dir: str) -> List[dict]:
    docs = []
    for root, _, files in os.walk(data_dir):
        for fname in files:
            if fname.lower().endswith((".txt", ".md")):
                path = Path(root) / fname
                text = path.read_text(encoding="utf-8", errors="ignore")
                docs.append({"path": str(path), "text": text})
    return docs

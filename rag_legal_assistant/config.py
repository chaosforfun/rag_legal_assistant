import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = os.getenv("LEGAL_DATA_DIR", str(BASE_DIR / "data/legal"))
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://rag:rag@localhost:5432/rag")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
EMBED_MODEL_NAME = os.getenv("EMBED_MODEL_NAME", "sentence-transformers/all-mpnet-base-v2")
VECTOR_DIM = int(os.getenv("VECTOR_DIM", "768"))

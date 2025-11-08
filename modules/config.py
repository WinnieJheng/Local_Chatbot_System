import os
from langchain_community.llms import Ollama

# 預設改成連 Docker 服務名稱 "ollama"
BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
LLM_MODEL = "gemma3:4b"
EMBED_MODEL = "nomic-embed-text"

VECTOR_DIR = "vectorDB"
PDF_DIR = "pdfFiles"
os.makedirs(VECTOR_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

llm = Ollama(model=LLM_MODEL, base_url=BASE_URL)

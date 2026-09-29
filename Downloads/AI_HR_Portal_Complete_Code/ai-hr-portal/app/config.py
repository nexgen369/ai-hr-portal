import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
    azure_openai_api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    azure_openai_api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")
    chat_deployment: str = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "hr-chat")
    embedding_deployment: str = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "hr-embedding")
    search_endpoint: str = os.getenv("AZURE_SEARCH_ENDPOINT", "").rstrip("/")
    search_key: str = os.getenv("AZURE_SEARCH_KEY", "")
    search_index: str = os.getenv("AZURE_SEARCH_INDEX", "hr-policy-index")
    top_k: int = int(os.getenv("RAG_TOP_K", "4"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "900"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "120"))

settings = Settings()

def validate_runtime_config(require_search=True):
    missing = []
    if not settings.azure_openai_endpoint: missing.append("AZURE_OPENAI_ENDPOINT")
    if not settings.azure_openai_api_key: missing.append("AZURE_OPENAI_API_KEY")
    if require_search:
        if not settings.search_endpoint: missing.append("AZURE_SEARCH_ENDPOINT")
        if not settings.search_key: missing.append("AZURE_SEARCH_KEY")
    if missing:
        raise RuntimeError("Missing environment variables: " + ", ".join(missing))

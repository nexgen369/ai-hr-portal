from openai import AzureOpenAI
from .config import settings, validate_runtime_config

def client():
    validate_runtime_config(require_search=False)
    return AzureOpenAI(
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
        api_version=settings.azure_openai_api_version,
    )

def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    response = client().embeddings.create(model=settings.embedding_deployment, input=texts)
    return [item.embedding for item in response.data]

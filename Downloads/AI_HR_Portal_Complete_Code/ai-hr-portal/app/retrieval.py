from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from .config import settings, validate_runtime_config

def search_client():
    validate_runtime_config()
    return SearchClient(
        endpoint=settings.search_endpoint,
        index_name=settings.search_index,
        credential=AzureKeyCredential(settings.search_key),
    )

def retrieve(question_vector: list[float], top_k: int | None = None) -> list[dict]:
    results = search_client().search(
        search_text=None,
        vector_queries=[VectorizedQuery(
            vector=question_vector,
            k_nearest_neighbors=top_k or settings.top_k,
            fields="contentVector",
        )],
        top=top_k or settings.top_k,
        select=["id", "content", "source", "chunk"],
    )
    return [
        {
            "content": row.get("content", ""),
            "source": row.get("source", "unknown"),
            "chunk": row.get("chunk", 0),
            "score": row.get("@search.score"),
        }
        for row in results
    ]

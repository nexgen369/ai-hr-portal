import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SearchField, SearchFieldDataType, SimpleField,
    SearchableField, VectorSearch, HnswAlgorithmConfiguration,
    VectorSearchProfile, SearchField,
)
from app.config import settings, validate_runtime_config

def main():
    validate_runtime_config()
    # Embedding dimension must match the deployed embedding model.
    dimensions = int(os.getenv("EMBEDDING_DIMENSIONS", "1536"))
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SearchableField(name="source", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="chunk", type=SearchFieldDataType.Int32, filterable=True),
        SearchField(
            name="contentVector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=dimensions,
            vector_search_profile_name="hr-vector-profile",
        ),
    ]
    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="hr-hnsw")],
        profiles=[VectorSearchProfile(name="hr-vector-profile", algorithm_configuration_name="hr-hnsw")],
    )
    client = SearchIndexClient(settings.search_endpoint, AzureKeyCredential(settings.search_key))
    client.create_or_update_index(SearchIndex(name=settings.search_index, fields=fields, vector_search=vector_search))
    print(f"Index ready: {settings.search_index}")

if __name__ == "__main__":
    main()

import hashlib
from pathlib import Path
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from app.config import settings, validate_runtime_config
from app.embeddings import embed_texts

def chunks(text: str, size: int, overlap: int):
    if overlap >= size:
        raise ValueError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE")
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        part = text[start:end].strip()
        if part:
            yield part
        if end == len(text):
            break
        start = end - overlap

def main():
    validate_runtime_config()
    source_path = Path(__file__).resolve().parents[1] / "data" / "hr-policy.txt"
    text = source_path.read_text(encoding="utf-8")
    parts = list(chunks(text, settings.chunk_size, settings.chunk_overlap))
    vectors = embed_texts(parts)
    docs = []
    for i, (part, vector) in enumerate(zip(parts, vectors)):
        stable_id = hashlib.sha1(f"{source_path.name}:{i}:{part}".encode()).hexdigest()
        docs.append({"id": stable_id, "content": part, "source": source_path.name, "chunk": i, "contentVector": vector})
    client = SearchClient(settings.search_endpoint, settings.search_index, AzureKeyCredential(settings.search_key))
    for start in range(0, len(docs), 100):
        result = client.upload_documents(docs[start:start+100])
        failed = [r for r in result if not r.succeeded]
        if failed:
            raise RuntimeError(f"{len(failed)} documents failed to upload")
    print(f"Ingested {len(docs)} chunks from {source_path.name}")

if __name__ == "__main__":
    main()

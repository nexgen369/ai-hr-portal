# AI HR Portal — Azure RAG demo

A sample FastAPI application that answers HR-policy questions using Azure OpenAI and Azure AI Search.

## Prerequisites
- Python 3.11+
- Azure OpenAI resource with chat and embedding deployments
- Azure AI Search service
- Azure AI Search index configured using `scripts/create_index.py`

## Local setup (Windows PowerShell)
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```
Edit `.env` with your resource endpoints, keys, deployment names and embedding dimension. Never commit `.env`.

## Setup and run
```powershell
python -m scripts.create_index
python -m scripts.ingest
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000. API docs: http://127.0.0.1:8000/docs

## Tests
```powershell
pytest -q
```

## Important
- `data/hr-policy.txt` is fictional demo content. Replace it with approved, access-controlled policy material.
- Confirm the embedding deployment's vector dimensions and set `EMBEDDING_DIMENSIONS` accordingly.
- Terraform files provide a starter layout; several Azure resources are intentionally placeholders and are not a complete production deployment.
- Add authentication/authorization before exposing this app to employees. Do not expose API keys to browser code.
- This demo does not guarantee that model answers are always correct; validate citations and answers with HR.

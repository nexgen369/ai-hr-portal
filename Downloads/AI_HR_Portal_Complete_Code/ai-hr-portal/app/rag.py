from openai import AzureOpenAI
from .config import settings, validate_runtime_config
from .embeddings import embed_texts
from .retrieval import retrieve

SYSTEM_PROMPT = """You are an HR policy assistant. Answer using only the supplied policy context.
If the context does not contain the answer, say you could not find the information in the available HR policy documents
and suggest contacting HR. Do not invent benefits, dates, eligibility, or policy rules.
Cite supporting source filenames in a Sources section."""

def answer_question(question: str) -> dict:
    question = question.strip()
    if not question:
        raise ValueError("Question cannot be empty.")
    validate_runtime_config()
    vector = embed_texts([question])[0]
    passages = retrieve(vector)
    if not passages:
        return {"answer": "I could not find relevant information in the available HR policy documents. Please contact HR.", "sources": []}

    context = "\n\n".join(
        f"[Source: {p['source']} | chunk {p['chunk']}]\n{p['content']}"
        for p in passages
    )
    client = AzureOpenAI(
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
        api_version=settings.azure_openai_api_version,
    )
    completion = client.chat.completions.create(
        model=settings.chat_deployment,
        temperature=0.1,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Policy context:\n{context}\n\nEmployee question: {question}"},
        ],
    )
    return {
        "answer": completion.choices[0].message.content or "",
        "sources": sorted({p["source"] for p in passages}),
        "retrieved_chunks": passages,
    }

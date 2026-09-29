# Workflow

1. Prepare approved HR policy documents.
2. Create the Azure AI Search index with a vector field whose dimensions match the embedding deployment.
3. Run ingestion to chunk policy text, create embeddings, and upload records.
4. Start the FastAPI application.
5. Employee submits a question.
6. The app embeds the question, retrieves relevant policy chunks, and sends grounded context to the chat deployment.
7. The app returns the response and source filenames.
8. Evaluate retrieval quality, groundedness, access control, and refusal behavior before production.

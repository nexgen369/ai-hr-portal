# Azure architecture

Employee/browser -> FastAPI application -> Azure OpenAI embeddings -> Azure AI Search vector retrieval -> retrieved HR-policy passages -> Azure OpenAI chat deployment -> answer with source filenames.

Production controls to evaluate: Microsoft Entra ID authentication, managed identity, Key Vault, private endpoints/network restrictions, Azure Monitor/Application Insights, data retention, and role-based access. Mark a component deployed only after validating it in the Azure subscription.

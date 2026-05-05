# [Vertex AI RAG Engine billing](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-engine-billing.md.txt)

The [VPC-SC security controls](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/security-controls) and
CMEK are supported by Agent Platform RAG Engine. Data residency and AXT security controls aren't
supported.

This page describes the Vertex AI RAG Engine pricing and billing based
on the Vertex AI RAG Engine components you use, such as models,
reranking, and vector storage.

For more information, see the [Vertex AI RAG Engine
overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/%7Brag-overview) page.

## Pricing and billing

This table explains how billing works when you use the RAG components.

| **Component** | **How billing works with Vertex AI RAG Engine** |
|---|---|
| [Data ingestion](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/use-data-ingestion) | Vertex AI RAG Engine supports ingesting data from different data sources. For example, uploading local files, Cloud Storage, and Google Drive. Accessing files in these data sources from Vertex AI RAG Engine is free, but these data sources might charge for data transfer. For example, data egress costs. |
| [Data transformation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/fine-tune-rag-transformations) (file parsing) | - **Default parser**: Free. - **[LLM Parser](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/llm-parser)**: Vertex AI RAG Engine uses the LLM model that you specified to parse your file, and you will see and pay LLM model costs directly from your project. - **[Document AI layout parser](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/layout-parser-integration)**: Vertex AI RAG Engine uses the Document AI layout parser that you specified to process your file, and you will see and pay for the use of the Document AI layout parser directly from your project. |
| [Data transformation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/fine-tune-rag-transformations) (file chunking) | Supports fixed-size chunking, which is free. |
| [Embedding generation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/use-embedding-models) | Vertex AI RAG Engine orchestrates the embedding generation using the embedding model that you specified, and your project is billed for the costs associated with that model. For more pricing information, see [Cost of building and deploying AI models in Gemini Enterprise Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/pricing). |
| Data indexing and retrieval | > [!NOTE] > **Note:** The Vertex AI RAG Engine uses Spanner as a backend for its data indexing and retrieval operations. Using Spanner results in associated billing charges. For more information, see [Spanner pricing](https://docs.cloud.google.com/spanner/pricing). <br /> RAG Engine supports two categories of vector databases for vector search: - RAG-managed database - Bring-Your-Own vector database A RAG-managed database has two purposes: - A RAG-managed database stores RAG resources, such as RAG corpora and RAG files. File contents are excluded. - Upon your choice, embedding indexing and retrieval for vector search. A RAG-managed database uses a Spanner instance as the backend. For each of your projects, Vertex AI RAG Engine provisions a customer-specific Google Cloud project and manages RAG-managed resources that are stored in Vertex AI RAG Engine, so that your data is physically isolated. If you choose the `RagManagedDB` Basic tier or Scaled tier, Vertex AI RAG Engine provisions a Spanner Enterprise edition instance in the corresponding project: - **Basic tier**: 100 processing units with backup - **Scaled tier**: Starting at 1 node (1,000 processing units) and autoscaling up to 10 nodes with backup If any RAG corpus in your project chooses to use a RAG-managed database for the vector search, you will be charged for the RAG-managed Spanner instance. Vertex AI RAG Engine surfaces Spanner costs from your corresponding RAG-managed project to your Google Cloud project, so that you can see and pay Spanner instance costs. For more pricing details on Spanner, see [Spanner pricing](https://docs.cloud.google.com/spanner/pricing). |
| [Reranking for Vertex AI RAG Engine](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-engine/retrieval-and-ranking) | The following ranking tools are supported post retrieval: - **LLM Reranker**: Vertex AI RAG Engine uses the LLM model that you specified to rerank the retrieval results, and you will see and pay LLM model costs directly from your project. - **Vertex AI Search ranking API** : Vertex AI RAG Engine uses the Vertex AI Search ranking API to rerank the retrieval results, and you will see and pay for the [Ranking API](https://docs.cloud.google.com/generative-ai-app-builder/pricing#ranking_api_pricing) directly from your project. |

## Delete Vertex AI RAG Engine

The following code samples demonstrate how to delete a
Vertex AI RAG Engine for the Google Cloud console, Python, and REST:

- Version 1 (v1) API
  [parameters](https://docs.cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations/updateRagEngineConfig)
  and [code
  samples](https://docs.cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations/updateRagEngineConfig).

- v1beta1 API
  [parameters](https://docs.cloud.google.com/vertex-ai/docs/reference/rest/v1beta1/projects.locations/updateRagEngineConfig)
  and [code
  samples](https://docs.cloud.google.com/vertex-ai/docs/reference/rest/v1beta1/projects.locations/updateRagEngineConfig).

## What's next

- To learn how to use the Vertex AI SDK to run
  Vertex AI RAG Engine tasks, see [RAG quickstart for
  Python](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-quickstart).

- To learn about grounding, see [Grounding
  overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/gemini-enterprise-agent-platform/models/grounding/overview).

- To learn more about the responses from RAG, see [Retrieval and Generation
  Output of
  Vertex AI RAG Engine](https://docs.cloud.google.com/vertex-ai/docs/model-reference/rag-output-explained).

- To learn about the RAG architecture:

  - [Infrastructure for a RAG-capable generative AI application using
    Agent Platform and
    Vector Search](https://docs.cloud.google.com/architecture/gen-ai-rag-vertex-ai-vector-search)

  - [Infrastructure for a RAG-capable generative AI application using
    Agent Platform and
    AlloyDB for PostgreSQL](https://docs.cloud.google.com/architecture/rag-capable-gen-ai-app-using-vertex-ai).
# [Vector database choices in Gemini Enterprise Agent Platform RAG Engine](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/vector-db-choices.md.txt)

The [VPC-SC security controls](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/security-controls) and
CMEK are supported by Agent Platform RAG Engine. Data residency and AXT security controls aren't
supported.
The Gemini Enterprise Agent Platform RAG Engine-managed Spanner instance
is used as a vector database and is GA with billing enabled. For more
information, see [Gemini Enterprise Agent Platform RAG Engine
billing](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-engine-billing).

This page introduces the vector databases supported on Gemini Enterprise Agent Platform RAG Engine.
You can also see how to connect a vector database (vector store) to your RAG
corpus.

Vector databases play a crucial role in enabling retrieval for RAG applications.
Vector databases offer a specialized way to store and query vector embeddings,
which are mathematical representations of text or other data that capture
semantic meaning and relationships. Vector embeddings allow RAG systems to
quickly and accurately find the most relevant information within a vast
knowledge base, even when dealing with complex or nuanced queries. When combined
with an embedding model, vector databases can help overcome the limitations of
LLMs, and provide more accurate, relevant, and comprehensive responses.

## Supported vector databases

When creating a RAG corpus, Gemini Enterprise Agent Platform RAG Engine offers the
enterprise-ready `RagManagedDb` as the default vector database, which requires
no additional provisioning or managing. `RagManagedDb` offers both KNN and ANN
search options and allows switching to a basic tier for some quick prototyping
and experimentation. To learn more about choosing a retrieval strategy on
`RagManagedDb` or for updating the tier, see [Use `RagManagedDb` with
RAG](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/use-ragmanageddb-with-rag). For Gemini Enterprise Agent Platform RAG Engine to
automatically create and manage the vector database for you, see [REST Resource:
projects.locations.ragCorpora](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/rest/v1/projects.locations.ragCorpora).

In addition to the default `RagManagedDb`, Gemini Enterprise Agent Platform RAG Engine
lets you provision and use your vector database within your RAG corpus. In this
case, you are responsible for the lifecycle and scalability of your vector
database.

## Compare vector database options

This table lists your choices of vector databases that are supported within
Gemini Enterprise Agent Platform RAG Engine and provides links to pages that explain how
to use the vector databases within your RAG corpus.

| Vector database | Benefits | Best for | Disadvantages | Supported distance metrics | Search type | Launch stage |
|---|---|---|---|---|---|---|
| [`RagManagedDb`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/use-ragmanageddb-with-rag) (default) is a regionally-distributed scalable database service that offers very high consistency and high availability and can be used for a vector search. easy simple fast quick | - No setup required. - Good for enterprise-scale and small-scale use cases. - Very high consistency. - High availability. - Low latency. - Excellent for transactional workloads. - CMEK enabled. | - Generating high-volume documents. - Building enterprise-scale RAG. - Developing a quick proof of concept. - Providing low provisioning and maintenance overhead. - Using with chat bots. - Building RAG applications. | - For optimal recall, the ANN feature requires that the index be rebuilt after major changes to your data. | `cosine` | KNN (default) and ANN | Generally available |
| [Vector Search](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/use-vertexai-vector-search) is the vector database service within Agent Platform that's optimized for machine-learning tasks. | - Integrates with other Google Cloud services. - Scalability and reliability are supported by Google Cloud infrastructure. - Uses pay-as-you-go pricing. | - Generating high-volume documents. - Building enterprise-scale RAG. - Managing vector database infrastructure. - Existing Google Cloud customers or anyone looking to use multiple Google Cloud services. | - Updates aren't reflected immediately. - Vendor lock-in with Google Cloud. - Could be more expensive depending on your use cases. | `cosine` `dot-product` | ANN | Generally available |
| [Vertex AI Feature Store](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/use-feature-store-with-rag) is a managed service for organizing, storing, and serving machine-learning features. | - Integrates with Gemini Enterprise Agent Platform and other Google Cloud services. - Scalability and reliability are supported by Google Cloud infrastructure. - Leverages existing BigQuery infrastructure. | - Generating high-volume documents. - Building enterprise-scale RAG. - Managing vector database infrastructure. - Existing Google Cloud customers or customers looking to use multiple Google Cloud services. | - Changes are only available in the online store after a manual synchronization is performed. - Vendor lock-in with Google Cloud. | `cosine` `dot-product` `L2 squared` | ANN | Preview |
| [Weaviate](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/use-weaviate-db) is an open-source vector database that's flexible and modular. | - Supports various data types and offers built-in graph capabilities. - Provides open source and a vibrant community. - Highly flexible and customizable. - Supports diverse data types and modules for different modalities, such as text and images. - Can choose among Cloud providers, such as Google Cloud, AWS, and Azure. | - Generating high-volume documents. - Building enterprise-scale RAG. - Managing vector database infrastructure. - Existing Weaviate customers. | - Updates aren't reflected immediately. - Can be more complex to set up and manage. - Performance can vary depending on the configuration. | `cosine` `dot-product` `L2 squared` `hamming` `manhattan` | ANN + Hybrid search support | Preview |
| [Pinecone](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/use-pinecone) is a fully-managed cloud-native vector database designed for a high-performance similarity search. | - Get started quickly. - Excellent scalability and performance. - Focus on vector search with advanced features like filtering and a metadata search. - Can choose among Cloud providers, such as Google Cloud, AWS, and Azure. | - Generating high-volume documents. - Building enterprise-scale RAG. - Managing vector database infrastructure. - Existing Pinecone customers. | - Updates aren't reflected immediately. - Can be more expensive than other options. - Quotas and limits restrict scale and performance. - Limited control over the underlying infrastructure. | `cosine` `euclidean` `dot-product` | ANN | Generally available |

## What's next

- To create a RAG corpus, see [Method: ragCorpora.create](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/rest/v1/projects.locations.ragCorpora/create)

- To list RAG corpus, see [Method: ragCorpora.list](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/rest/v1/projects.locations.ragCorpora/list)
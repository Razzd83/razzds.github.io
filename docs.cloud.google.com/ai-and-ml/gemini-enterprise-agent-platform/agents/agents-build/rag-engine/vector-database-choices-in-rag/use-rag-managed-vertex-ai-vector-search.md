# [Use Vector Search 2.0 with RAG](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/use-rag-managed-vertex-ai-vector-search.md.txt)

> [!WARNING]
> **Preview**
>
> Some of the RAG features are Preview offerings, subject to the "Pre-GA Offerings Terms"
> of the [Google Cloud Service Specific
> Terms](https://cloud.google.com/terms/service-terms). Pre-GA products and features are available "as-is" and may have limited support, and
> changes to Pre-GA products and features may not be compatible with other Pre-GA versions. For
> more information, see the [launch stage descriptions](https://cloud.google.com/products#product-launch-stages).
>
> By using the Gemini API on Gemini Enterprise Agent Platform, you agree to the Generative AI Preview
> [terms and conditions](https://cloud.google.com/trustedtester/aitos)(Preview
> Terms).
>
> <br />
>
The [VPC-SC security controls](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/security-controls) and
CMEK are supported by Agent Platform RAG Engine. Data residency and AXT security controls aren't
supported.
RAG Engine corpora that are backed by Vector Search 2.0 are
available only in `us-central1`. To use it, your project must be
added to the allowlist for Vertex AI RAG Engine in
`us-central1`. For users with new projects, you can contact
`vertex-ai-rag-engine-support@google.com` to onboard to
`us-central1`.

This page shows you how Vertex AI RAG Engine uses [Gemini Enterprise Agent Platform
Vector Search 2.0](https://docs.cloud.google.com/vertex-ai/docs/vector-search-2/overview), which is
a Google Cloud product that serves as a comprehensive storage and retrieval
system to store and manage vector representations of your documents. The
Gemini Enterprise Agent Platform Vector Search 2.0 is then used to retrieve relevant
documents based on the document's semantic similarity to a given query.

RAG will manage the Vector Search 2.0 collections for you and you will
have full access to the Vector Search 2.0 collections in your project.

## Choosing a RAG backend

When using Vertex AI RAG Engine, you can choose between different
backend storage options for your RAG corpora. The following table summarizes the
key differences:

| Backend Option | Underlying Technology | Management by RAG Engine | Data Visibility in Project | CMEK Support |
|---|---|---|---|---|
| `RagManagedVertexVectorSearch` | Gemini Enterprise Agent Platform Vector Search 2.0 | Fully managed by Google. | Visible in your Google Cloud project | No |
| `VertexVectorSearch` | Gemini Enterprise Agent Platform Vector Search 1.0 | User is expected to set up, manage, and clean up the Vector Search 1.0 instance. | Visible in your Google Cloud project | No |
| `RagManagedDb` | Spanner | Fully managed by Google. | Not directly visible in your project | Yes |

Choose `RagManagedVertexVectorSearch` for the latest features, automated
management, and transparency into your Vector Search 2.0 data. If CMEK
support is a strict requirement, consider `RagManagedDb`, keeping in mind the
lack of direct visibility into the backend database.

## Enable Vector Search API

To use RAG Managed Gemini Enterprise Agent Platform Vector Search, you need to first
enable the [Vector Search
API](https://console.developers.google.com/apis/api/vectorsearch.googleapis.com/).

### Create a RAG corpus with `RagManagedVertexVectorSearch`

This code samples demonstrates how to create a RAG corpus using
`RagManagedVertexVectorSearch`.

### Python

    from vertexai.preview import rag
    import https://docs.cloud.google.com/python/docs/reference/vertexai/latest

    PROJECT_ID = YOUR_PROJECT_ID
    LOCATION = YOUR_RAG_ENGINE_LOCATION
    DISPLAY_NAME = YOUR_RAG_CORPUS_DISPLAY_NAME

    # Initialize Agent Platform API once per session
    https://docs.cloud.google.com/python/docs/reference/vertexai/latest.init(project=PROJECT_ID, location=LOCATION)

    vector_db = rag.RagManagedVertexVectorSearch()
    rag_corpus = rag.create_corpus(
        display_name=DISPLAY_NAME, backend_config=rag.RagVectorDbConfig(vector_db=vector_db))

### REST

Replace the following variables:

- **<var translate="no">PROJECT_ID</var>**: Your project ID.
- **<var translate="no">LOCATION</var>**: The region to process the request.
- **<var translate="no">CORPUS_DISPLAY_NAME</var>**: The display name of the RAG corpus.

    PROJECT_ID=PROJECT_ID
    LOCATION=LOCATION
    CORPUS_DISPLAY_NAME=CORPUS_DISPLAY_NAME

    curl -X POST \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    https://${LOCATION}-aiplatform.googleapis.com/v1beta1/projects/${PROJECT_ID}/locations/${LOCATION}/ragCorpora \
    -d '{
          "display_name" : '\""${CORPUS_DISPLAY_NAME}"\"',
          "vector_db_config": {
            "rag_managed_vertex_vector_search": {}
          }
        }'

### Importing your data into `RagManagedVertexVectorSearch`

You can use either the `ImportRagFiles` API or the `UploadRagFile` API to import
your data into the `RagManagedVertexVectorSearch`.

To upload your local file into your RAG corpus, see [Upload a RAG
file](https://docs.cloud.google.com/vertex-ai/docs/reference/rest/v1beta1/projects.locations.ragCorpora.ragFiles/upload). To
import data into your RAG corpus, see the following code sample that
demonstrates how to import from Cloud Storage. To learn about the supported
data sources, see [Data sources supported for
RAG](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/use-data-ingestion#supported-data-sources).

### Python

    from vertexai.preview import rag
    import https://docs.cloud.google.com/python/docs/reference/vertexai/latest

    PROJECT_ID = YOUR_PROJECT_ID
    LOCATION = YOUR_RAG_ENGINE_LOCATION
    CORPUS_ID = YOUR_CORPUS_ID
    PATHS = ["gs://my_bucket/my_files_dir"]

    # Initialize Agent Platform API once per session
    https://docs.cloud.google.com/python/docs/reference/vertexai/latest.init(project=PROJECT_ID, location=LOCATION)

    corpus_name = f"projects/{PROJECT_ID}/locations/{LOCATION}/ragCorpora/{CORPUS_ID}"
    # This is a non blocking call.
    response = await rag.import_files_async(
        corpus_name=corpus_name,
        paths=PATHS,
    )

    # Wait for the import to complete.
    await response.https://docs.cloud.google.com/python/docs/reference/vertexai/latest/vertexai._genai.types.CheckQueryJobResultDict.html#vertexai__genai_types_CheckQueryJobResultDict_result()

### REST

    GCS_URI=GCS_URI

    curl -X POST \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    https://${LOCATION}-aiplatform.googleapis.com/v1beta1/projects/${PROJECT_ID}/locations/${LOCATION}/ragCorpora/${CORPUS_ID}/ragFiles:import \
    -d '{
      "import_rag_files_config": {
        "gcs_source": {
          "uris": '\""${GCS_URI}"\"',
          },
      }
    }'

## What's next

- To import files and folders from Google Drive or Cloud Storage, see
  [Import RAG files
  example](https://docs.cloud.google.com/vertex-ai/docs/reference/rest/v1beta1/projects.locations.ragCorpora.ragFiles/import).

- To list RAG files, see [List RAG files
  example](https://docs.cloud.google.com/vertex-ai/docs/reference/rest/v1beta1/projects.locations.ragCorpora.ragFiles/list).

- To use a reranker for retrieval, see [Reranking for Gemini Enterprise Agent Platform RAG
  Engine](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/retrieval-and-ranking)
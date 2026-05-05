# [Use Vertex AI RAG Engine in Gemini Live API](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/use-rag-in-multimodal-live.md.txt)

> [!WARNING]
> **Experimental**
>
> Some of the RAG features are Experimental offerings, subject to the "Pre-GA Offerings Terms"
> of the [Google Cloud Service Specific
> Terms](https://cloud.google.com/terms/service-terms). Pre-GA products and features are available "as-is" and may have limited support, and
> changes to Pre-GA products and features may not be compatible with other Pre-GA versions. For
> more information, see the [launch stage descriptions](https://cloud.google.com/products#product-launch-stages).
>
The [VPC-SC security controls](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/security-controls) and
CMEK are supported by Agent Platform RAG Engine. Data residency and AXT security controls aren't
supported.

Retrieval-augmented generation (RAG) is a technique that's used to retrieve and
provide relevant information to LLMs to generate verifiable responses. The
information can include fresh information, a topic and context, or ground truth.

This page shows you how to use Vertex AI RAG Engine with the
[Gemini Live API](https://docs.cloud.google.com/vertex-ai/docs/live-api/tools#use-rag-with-live-api), which
lets you specify and retrieve information from the RAG corpus.

## Prerequisites

The following prerequisites must be completed before you can use
Vertex AI RAG Engine with the multimodal Live API:

1. Enable the RAG API in Agent Platform.

2. [Create the RAG Corpus
   example](https://docs.cloud.google.com/vertex-ai/docs/reference/rest/v1beta1/projects.locations.ragCorpora/create).

3. To upload files to the RAG Corpus, see [Import RAG files example
   API](https://docs.cloud.google.com/vertex-ai/docs/reference/rest/v1beta1/projects.locations.ragCorpora.ragFiles/import).

## Set up

You can use Vertex AI RAG Engine with the Live API by specifying
Vertex AI RAG Engine as a tool. The following code sample
demonstrates how to specify Vertex AI RAG Engine as a tool:

Replace the following variables:

- **<var translate="no">YOUR_PROJECT_ID</var>**: The ID of your Google Cloud project.
- **<var translate="no">YOUR_CORPUS_ID</var>**: The ID of your corpus.
- **<var translate="no">YOUR_LOCATION</var>**: The region to process the request.

    PROJECT_ID = "YOUR_PROJECT_ID"
    RAG_CORPUS_ID = "YOUR_CORPUS_ID"
    LOCATION = "YOUR_LOCATION"

    TOOLS = {
      "retrieval": {
        "vertex_rag_store": {
            "rag_resources": {
            "rag_corpus": "projects/${PROJECT_ID}/locations/${LOCATION}/ragCorpora/${RAG_CORPUS_ID}"
          }
        }
      }
    }

## Use `Websocket` for real-time communication

To enable real-time communication between a client and a server, you must use a
`Websocket`. These code samples demonstrate how to use a `Websocket` using the
Python API and the Python SDK.

### Python API

    CONFIG = {"response_modalities": ["TEXT"], "speech_config": { "language_code": "en-US" }}
    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {bearer_token[0]}",
    }
    HOST= "${LOCATION}-aiplatform.googleapis.com"
    SERVICE_URL = f"wss://{HOST}/ws/google.cloud.aiplatform.v1beta1.LlmBidiService/BidiGenerateContent"
    MODEL="gemini-2.0-flash-exp"

    # Connect to the server
    async with connect(SERVICE_URL, additional_headers=headers) as ws:
      # Setup the session
      await ws.send(
    json.dumps(
              {
                  "setup": {
                      "model": MODEL,
                      "generation_config": CONFIG,
                      # Setup RAG as a retrieval tool
                      "tools": TOOLS,
                  }
              }
          )
      )

      # Receive setup response
      raw_response = await ws.recv(decode=False)
      setup_response = json.loads(raw_response.decode("ascii"))

      # Send text message
      text_input = "What are popular LLMs?"
      display(Markdown(f"**Input:** {text_input}"))

      msg = {
          "client_content": {
              "turns": [{"role": "user", "parts": [{"text": text_input}]}],
              "turn_complete": True,
          }
      }

      await ws.send(json.dumps(msg))

      responses = []

      # Receive chunks of server response
      async for raw_response in ws:
          response = json.loads(raw_response.decode())
          server_content = response.pop("serverContent", None)
          if server_content is None:
              break

          model_turn = server_content.pop("modelTurn", None)
          if model_turn is not None:
              parts = model_turn.pop("parts", None)
              if parts is not None:
                  display(Markdown(f"**parts >** {parts}"))
                  responses.append(parts[0]["text"])

          # End of turn
          turn_complete = server_content.pop("turnComplete", None)
          if turn_complete:
              grounding_metadata = server_content.pop("groundingMetadata", None)
              if grounding_metadata is not None:
                grounding_chunks = grounding_metadata.pop("groundingChunks", None)
                if grounding_chunks is not None:
                  for chunk in grounding_chunks:
                    display(Markdown(f"**grounding_chunk >** {chunk}"))
              break

      # Print the server response
      display(Markdown(f"**Response >** {''.join(responses)}"))

### Python SDK

To learn how to install the generative AI SDK, see [Install a
library](https://ai.google.dev/gemini-api/docs/libraries#install):

    from google import genai
    from google.genai import types
    from google.genai.types import (Content, LiveConnectConfig, HttpOptions, Modality, Part,)
    from IPython import display

    MODEL="gemini-2.0-flash-exp"

    client = genai.Client(
      vertexai=True,
      project=PROJECT_ID,
      location=LOCATION
    )

    async with client.aio.live.connect(
      model=MODEL,
      config=LiveConnectConfig(response_modalities=[Modality.TEXT],
                                tools=TOOLS),
    ) as session:
      text_input = "\'What are core LLM techniques?\'"
      print("> ", text_input, "\n")
      await session.send_client_content(
          turns=Content(role="user", parts=[Part(text=text_input)])
      )

      async for message in session.receive()
          if message.text:
              display.display(display.Markdown(message.text))
              continue

## Use Vertex AI RAG Engine as the context store

You can use Vertex AI RAG Engine as the context store for
Gemini Live API to store session context to form and retrieve past
contexts that are related to your conversation and enrich the current context
for model generation. You can also take advantage of this feature to share
contexts across your different Live API sessions.

Vertex AI RAG Engine supports storing and indexing the following
forms of data from session contexts:

- Text
- Audio speech

### Create a MemoryCorpus type corpus

To store and index conversation texts from the session context, you must create
a RAG corpus of the `MemoryCorpus` type. You must also specify an LLM parser in
your memory corpus configuration that's used to parse session contexts stored
from the Live API to build memory for indexing.

This code sample demonstrates how to create a corpus. However, first replace the
variables with values.

    # Currently supports Google first-party embedding models
    EMBEDDING_MODEL = YOUR_EMBEDDING_MODEL  # Such as "publishers/google/models/text-embedding-005"
    MEMORY_CORPUS_DISPLAY_NAME = YOUR_MEMORY_CORPUS_DISPLAY_NAME
    LLM_PARSER_MODEL_NAME = YOUR_LLM_PARSER_MODEL_NAME  # Such as "projects/{project_id}/locations/{location}/publishers/google/models/gemini-2.5-pro-preview-05-06"

    memory_corpus = rag.create_corpus(
       display_name=MEMORY_CORPUS_DISPLAY_NAME,
       corpus_type_config=rag.RagCorpusTypeConfig(
           corpus_type_config=rag.MemoryCorpus(
               llm_parser=rag.LlmParserConfig(
                   model_name=LLM_PARSER_MODEL_NAME,
               )
           )
       ),
       backend_config=rag.RagVectorDbConfig(
           rag_embedding_model_config=rag.RagEmbeddingModelConfig(
               vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
                   publisher_model=EMBEDDING_MODEL
               )
           )
       ),
    )

### Specify your memory corpus to store contexts

When using your memory corpus with the Live API, you must specify the memory
corpus as a retrieval tool and then set `store_context` to `true` to allow the
Live API to store the session contexts.

This code sample demonstrates how to specify your memory corpus to store
contexts. However, first replace the variables with values.

    from google import genai
    from google.genai import types
    from google.genai.types import (Content, LiveConnectConfig, HttpOptions, Modality, Part)
    from IPython import display

    PROJECT_ID=YOUR_PROJECT_ID
    LOCATION=YOUR_LOCATION
    TEXT_INPUT=YOUR_TEXT_INPUT
    MODEL_NAME=YOUR_MODEL_NAME  # Such as "gemini-2.0-flash-exp"

    client = genai.Client(
       vertexai=True,
       project=PROJECT_ID,
       location=LOCATION,
    )

    memory_store=types.VertexRagStore(
       rag_resources=[
           types.VertexRagStoreRagResource(
               rag_corpus=memory_corpus.name
           )
       ],
       store_context=True
    )

    async with client.aio.live.connect(
       model=MODEL_NAME,
       config=LiveConnectConfig(response_modalities=[Modality.TEXT],
                                tools=[types.Tool(
                                    retrieval=types.Retrieval(
                                        vertex_rag_store=memory_store))]),
    ) as session:
       text_input=TEXT_INPUT
       await session.send_client_content(
           turns=Content(role="user", parts=[Part(text=text_input)])
       )

       async for message in session.receive():
           if message.text:
               display.display(display.Markdown(message.text))
               continue

## What's next

- To learn more about Vertex AI RAG Engine, see
  [Vertex AI RAG Engine overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview).

- To learn more about the RAG API, see [Vertex AI RAG Engine
  API](https://docs.cloud.google.com/vertex-ai/docs/reference/rest/v1beta1).

- To manage your RAG corpora, see [Corpus
  management](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/manage-your-rag-corpus#corpus-management).

- To manage your RAG files, see [File
  management](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/manage-your-rag-corpus#file-management).

- To learn how to use the Vertex AI SDK to run
  Vertex AI RAG Engine tasks, see [RAG quickstart for
  Python](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-quickstart).
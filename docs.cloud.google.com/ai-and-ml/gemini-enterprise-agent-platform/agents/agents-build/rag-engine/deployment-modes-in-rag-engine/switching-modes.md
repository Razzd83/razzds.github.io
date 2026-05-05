# [Switching between modes](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/switching-modes.md.txt)

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

Deployment modes are a project-level configuration. Switching between the two modes doesn't move or delete your data from the other mode. You can use the `UpdateRagEngineConfig` API to switch between the Serverless and Spanner deployment modes. You can also use this API to set the tier on your Spanner deployment mode or to unprovision your Spanner mode to stop billing. You can use the `GetRagEngineConfig` API to read your current deployment mode information.

## Switching to Serverless mode

The following code samples demonstrate how to switch your `RagEngineConfig` to Serverless mode:

### Console

1. In the Google Cloud console, go to the **RAG Engine** page.

   [Go to RAG Engine](https://console.cloud.google.com/agent-platform/rag/corpus)
2. Select the region in which your RAG Engine is running.
3. Click the **Switch to Serverless** option. It might not be visible if you're on Serverless mode. You can verify your current mode from the mode label at the top right section of the page.

### REST

    PROJECT_ID: Your project ID.
    LOCATION: The region to process the request.

    curl -X PATCH \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    https://LOCATION-aiplatform.googleapis.com/v1beta1/projects/PROJECT_ID/locations/LOCATION/ragEngineConfig -d "{'ragManagedDbConfig': {'serverless': {}}}"

### Python

    from vertexai.preview import rag
    import https://docs.cloud.google.com/python/docs/reference/vertexai/latest

    PROJECT_ID = YOUR_PROJECT_ID
    LOCATION = YOUR_RAG_ENGINE_LOCATION

    # Initialize Agent Platform API once per session
    https://docs.cloud.google.com/python/docs/reference/vertexai/latest.init(project=PROJECT_ID, location=LOCATION)

    rag_engine_config_name=f"projects/{PROJECT_ID}/locations/{LOCATION}/ragEngineConfig"

    new_rag_engine_config = rag.RagEngineConfig(
        name=rag_engine_config_name,
        rag_managed_db_config=rag.RagManagedDbConfig(mode=rag.Serverless()),
    )

    updated_rag_engine_config = rag.rag_data.update_rag_engine_config(
        rag_engine_config=new_rag_engine_config
    )

    print(updated_rag_engine_config)

## Switching to Spanner mode

The following code samples demonstrate how to switch your `RagEngineConfig` to Spanner mode. If you've previously used Spanner mode, and have chosen a tier, you don't need to provide it explicitly while switching. If not, refer to the lower code examples on how to switch to Spanner mode while providing a tier.

### Console

1. In the Google Cloud console, go to the **RAG Engine** page.

   [Go to RAG Engine](https://console.cloud.google.com/agent-platform/rag/corpus)
2. Select the region in which your RAG Engine is running.
3. Click the **Switch to Spanner** option. It might not be visible if you're on Spanner mode. You can verify your current mode from the mode label.

### REST

    PROJECT_ID: Your project ID.
    LOCATION: The region to process the request.

    curl -X PATCH \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    https://LOCATION-aiplatform.googleapis.com/v1beta1/projects/PROJECT_ID/locations/LOCATION/ragEngineConfig -d "{'ragManagedDbConfig': {'spanner': {}}}"

### Python

    from vertexai.preview import rag
    import https://docs.cloud.google.com/python/docs/reference/vertexai/latest

    PROJECT_ID = YOUR_PROJECT_ID
    LOCATION = YOUR_RAG_ENGINE_LOCATION

    # Initialize Agent Platform API once per session
    https://docs.cloud.google.com/python/docs/reference/vertexai/latest.init(project=PROJECT_ID, location=LOCATION)

    rag_engine_config_name=f"projects/{PROJECT_ID}/locations/{LOCATION}/ragEngineConfig"

    new_rag_engine_config = rag.RagEngineConfig(
        name=rag_engine_config_name,
        rag_managed_db_config=rag.RagManagedDbConfig(mode=rag.Spanner()),
    )

    updated_rag_engine_config = rag.rag_data.update_rag_engine_config(
        rag_engine_config=new_rag_engine_config
    )

    print(updated_rag_engine_config)

## Read your current RagEngineConfig

The following code samples demonstrate how to read your `RagEngineConfig` to see what mode and tier is chosen:

### REST

    PROJECT_ID: Your project ID.
    LOCATION: The region to process the request.

    curl -X GET \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    https://LOCATION-aiplatform.googleapis.com/v1beta1/projects/PROJECT_ID/locations/LOCATION/ragEngineConfig

### Python

    from vertexai.preview import rag
    import https://docs.cloud.google.com/python/docs/reference/vertexai/latest

    PROJECT_ID = YOUR_PROJECT_ID
    LOCATION = YOUR_RAG_ENGINE_LOCATION

    # Initialize Agent Platform API once per session
    https://docs.cloud.google.com/python/docs/reference/vertexai/latest.init(project=PROJECT_ID, location=LOCATION)

    rag_engine_config = rag.rag_data.get_rag_engine_config(
        name=f"projects/{PROJECT_ID}/locations/{LOCATION}/ragEngineConfig"
    )

    print(rag_engine_config)

## Update the tier on Spanner mode

The following code samples demonstrate how to update the tier on Spanner mode:

### Update your RagEngineConfig to Spanner mode Scaled tier

The following code samples demonstrate how to set the `RagEngineConfig` to the Spanner mode with Scaled tier:

##### Console

1. In the Google Cloud console, go to the **RAG Engine** page.

   [Go to RAG Engine](https://console.cloud.google.com/agent-platform/rag/corpus)
2. Select the region in which your RAG Engine is running.
3. Click the **Switch to Spanner** option, if not already on Spanner mode.
4. Click **Configure RAG Engine** . The **Configure RAG Engine** pane appears.
5. Select the tier with which you want to run your RAG Engine.
6. Click **Save**.

##### REST

    PROJECT_ID: Your project ID.
    LOCATION: The region to process the request.

    curl -X PATCH \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    https://LOCATION-aiplatform.googleapis.com/v1beta1/projects/PROJECT_ID/locations/LOCATION/ragEngineConfig -d "{'ragManagedDbConfig': {'spanner': {'scaled': {}}}}"

##### Python

    from vertexai.preview import rag
    import https://docs.cloud.google.com/python/docs/reference/vertexai/latest

    PROJECT_ID = YOUR_PROJECT_ID
    LOCATION = YOUR_RAG_ENGINE_LOCATION

    # Initialize Agent Platform API once per session
    https://docs.cloud.google.com/python/docs/reference/vertexai/latest.init(project=PROJECT_ID, location=LOCATION)

    rag_engine_config_name=f"projects/{PROJECT_ID}/locations/{LOCATION}/ragEngineConfig"

    new_rag_engine_config = rag.RagEngineConfig(
        name=rag_engine_config_name,
        rag_managed_db_config=rag.RagManagedDbConfig(mode=rag.Spanner(tier=rag.Scaled())),
    )

    updated_rag_engine_config = rag.rag_data.update_rag_engine_config(
        rag_engine_config=new_rag_engine_config
    )

    print(updated_rag_engine_config)

### Update your RagEngineConfig to Spanner mode with Basic tier

The following code samples demonstrate how to set the `RagEngineConfig` to the Spanner mode with Basic tier:

##### Console

1. In the Google Cloud console, go to the **RAG Engine** page.

   [Go to RAG Engine](https://console.cloud.google.com/agent-platform/rag/corpus)
2. Select the region in which your RAG Engine is running.
3. Click the **Switch to Spanner** option, if not already on Spanner mode.
4. Click **Configure RAG Engine** . The **Configure RAG Engine** pane appears.
5. Select the tier that you want to run your RAG Engine.
6. Click **Save**.

##### REST

    PROJECT_ID: Your project ID.
    LOCATION: The region to process the request.

    curl -X PATCH \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    https://LOCATION-aiplatform.googleapis.com/v1beta1/projects/PROJECT_ID/locations/LOCATION/ragEngineConfig -d "{'ragManagedDbConfig': {'spanner': {'basic': {}}}}"

##### Python

    from vertexai.preview import rag
    import https://docs.cloud.google.com/python/docs/reference/vertexai/latest

    PROJECT_ID = YOUR_PROJECT_ID
    LOCATION = YOUR_RAG_ENGINE_LOCATION

    # Initialize Agent Platform API once per session
    https://docs.cloud.google.com/python/docs/reference/vertexai/latest.init(project=PROJECT_ID, location=LOCATION)

    rag_engine_config_name=f"projects/{PROJECT_ID}/locations/{LOCATION}/ragEngineConfig"

    new_rag_engine_config = rag.RagEngineConfig(
        name=rag_engine_config_name,
        rag_managed_db_config=rag.RagManagedDbConfig(mode=rag.Spanner(tier=rag.Basic())),
    )

    updated_rag_engine_config = rag.rag_data.update_rag_engine_config(
        rag_engine_config=new_rag_engine_config
    )

    print(updated_rag_engine_config)

### Update your RagEngineConfig to Unprovisioned tier

The following code samples demonstrate how to set the `RagEngineConfig` to the Spanner mode with Unprovisioned tier. This will permanently delete all the data from your Spanner deployment mode and halt billing expenses arising from it.

##### Console

1. In the Google Cloud console, go to the **RAG Engine** page.

   [Go to RAG Engine](https://console.cloud.google.com/agent-platform/rag/corpus)
2. Select the region in which your RAG Engine is running.
3. Click the **Switch to Spanner** option, if not already on Spanner mode.
4. Click **Delete RAG Engine**. A confirmation dialog appears.
5. Verify that you're about to delete your data in RAG Engine by entering **delete**.
6. Click **Confirm**.
7. Click **Save**.

##### REST

    PROJECT_ID: Your project ID.
    LOCATION: The region to process the request.

    curl -X PATCH \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    https://LOCATION-aiplatform.googleapis.com/v1beta1/projects/PROJECT_ID/locations/LOCATION/ragEngineConfig -d "{'ragManagedDbConfig': {'spanner': {'unprovisioned': {}}}}"

##### Python

    from vertexai.preview import rag
    import https://docs.cloud.google.com/python/docs/reference/vertexai/latest

    PROJECT_ID = YOUR_PROJECT_ID
    LOCATION = YOUR_RAG_ENGINE_LOCATION

    # Initialize Agent Platform API once per session
    https://docs.cloud.google.com/python/docs/reference/vertexai/latest.init(project=PROJECT_ID, location=LOCATION)

    rag_engine_config_name=f"projects/{PROJECT_ID}/locations/{LOCATION}/ragEngineConfig"

    new_rag_engine_config = rag.RagEngineConfig(
        name=rag_engine_config_name,
        rag_managed_db_config=rag.RagManagedDbConfig(mode=rag.Spanner(tier=rag.Unprovisioned())),
    )

    updated_rag_engine_config = rag.rag_data.update_rag_engine_config(
        rag_engine_config=new_rag_engine_config
    )

    print(updated_rag_engine_config)
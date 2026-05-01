# [Authenticate using an agent's own authority](https://docs.cloud.google.com/iam/docs/auth-agent-own-identity.md.txt)

Agents can access Google Cloud APIs and other resources by using their own
authority. We recommend this method for agents that are hosted on Google Cloud
to interact with other Google Cloud services.

When an agent acts on its own authority, it uses its primary [SPIFFE identity](https://docs.cloud.google.com/iam/docs/agent-identity-overview#spiffe-identity)
to request Google Cloud access tokens.

> [!NOTE]
> **Note:** If you want your agent to access Google Cloud services on behalf of an end user, [Authenticate to services using 3-legged OAuth auth provider](https://docs.cloud.google.com/iam/docs/auth-with-3lo).

## Before you begin

1. [Verify that you have chosen the correct authentication method](https://docs.cloud.google.com/iam/docs/agent-identity-overview#auth-models).
2. [Create and deploy an agent](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/quickstart-adk) with Agent Identity enabled.
3. [Verify that you have the roles required to complete
   this task](https://docs.cloud.google.com/iam/docs/auth-agent-own-identity#req-roles).

### Required roles


To get the permissions that
you need to grant an agent access to Google Cloud services,

ask your administrator to grant you the
following IAM roles on the target resource:

- To grant access to an agent:
  - [Project IAM Admin](https://docs.cloud.google.com/iam/docs/roles-permissions/resourcemanager#resourcemanager.projectIamAdmin) (`roles/resourcemanager.projectIamAdmin`)
  - [Security Admin](https://docs.cloud.google.com/iam/docs/roles-permissions/iam#iam.securityAdmin) (`roles/iam.securityAdmin`)
- Recommended roles for the agent identity:
  - [Agent Context Editor](https://docs.cloud.google.com/iam/docs/roles-permissions/aiplatform#aiplatform.agentContextEditor) (`roles/aiplatform.agentContextEditor`)
  - [Agent Default Access](https://docs.cloud.google.com/iam/docs/roles-permissions/aiplatform#aiplatform.agentDefaultAccess) (`roles/aiplatform.agentDefaultAccess`)
  - [Vertex AI User](https://docs.cloud.google.com/iam/docs/roles-permissions/aiplatform#aiplatform.user) (`roles/aiplatform.user`)
  - [Service Usage Consumer](https://docs.cloud.google.com/iam/docs/roles-permissions/serviceusage#serviceusage.serviceUsageConsumer) (`roles/serviceusage.serviceUsageConsumer`)
  - [Browser](https://docs.cloud.google.com/iam/docs/roles-permissions/browser#browser) (`roles/browser`)
  - [Storage Object Viewer](https://docs.cloud.google.com/iam/docs/roles-permissions/storage#storage.objectViewer) (`roles/storage.objectViewer`)


For more information about granting roles, see [Manage access to projects, folders, and organizations](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access).


You might also be able to get
the required permissions through [custom
roles](https://docs.cloud.google.com/iam/docs/creating-custom-roles) or other [predefined
roles](https://docs.cloud.google.com/iam/docs/roles-overview#predefined).

## Grant access to agents

To let your agent access a Google Cloud service, you must grant the
agent's identity the required roles on the target resource.

In IAM allow policies, agent identities use
[*principal identifiers*](https://docs.cloud.google.com/iam/docs/principal-identifiers).

To grant an agent access to a resource, use the Google Cloud console or the
gcloud CLI.

### Console

1. In the Google Cloud console, go to the **IAM** page for the resource that you want to grant access to.
   - For a project, go to the **IAM** page:

     [Go to the IAM page](https://console.cloud.google.com/iam-admin/iam)
   - For other resources, go to the page for that resource and click the **Permissions** or **IAM** tab.
2. Click **Grant Access**.
3. In the **New principals** field, enter the principal identifier that matches the level of access you want to grant:
   - **A single agent** : `principal://agents.global.org-ORGANIZATION_ID.system.id.goog/resources/aiplatform/projects/PROJECT_NUMBER/locations/LOCATION/reasoningEngines/ENGINE_ID`
   - **All agents in a project** : `principalSet://agents.global.org-ORGANIZATION_ID.system.id.goog/attribute.platformContainer/aiplatform/projects/PROJECT_NUMBER`
   - **All agents in an organization** : `principalSet://agents.global.org-ORGANIZATION_ID.system.id.goog/*`
4. In the **Select a role** field, search for and select the role that you want to grant.
5. Click **Save**.

### Google Cloud CLI

To grant an agent access to a resource, run the following command:

```bash
gcloud SERVICE add-iam-policy-binding RESOURCE_NAME \
    --member="PRINCIPAL_IDENTIFIER" \
    --role="`ROLE`"
```

Replace the following:

- <var translate="no">SERVICE</var>: The Google Cloud service (for example, `storage` or `bigquery`).
- <var translate="no">RESOURCE_NAME</var>: The name of the resource (for example, the bucket name or dataset ID).
- <var translate="no">PRINCIPAL_IDENTIFIER</var>: The principal identifier that matches the level of access that you want to grant:
  - **A single agent** : `principal://agents.global.org-ORGANIZATION_ID.system.id.goog/resources/aiplatform/projects/PROJECT_NUMBER/locations/LOCATION/reasoningEngines/ENGINE_ID`
  - **All agents in a project** : `principalSet://agents.global.org-ORGANIZATION_ID.system.id.goog/attribute.platformContainer/aiplatform/projects/PROJECT_NUMBER`
  - **All agents in an organization** : `principalSet://agents.global.org-ORGANIZATION_ID.system.id.goog/*`
- <var translate="no">ORGANIZATION_ID</var>: Your Google Cloud organization ID.
- <var translate="no">PROJECT_NUMBER</var>: Your Google Cloud project number.
- <var translate="no">LOCATION</var>: The location of your agent (for example, `us-central1`). (Required only for single agent access.)
- <var translate="no">ENGINE_ID</var>: The ID of your reasoning engine. (Required only for single agent access.)
- <var translate="no">ROLE</var>: The IAM role that you want to grant.

## Reference the agent identity in your code

The Google Cloud client libraries automatically use Agent Identity when your
agent is deployed to a supported Google Cloud environment.

The following Python snippet shows how to manually use Agent Identity
credentials to call the Cloud Vision API using the Agent Development Kit (ADK).

    from google.cloud import vision
    from google.auth import default
    from google.adk.tools import tool

    @tool
    def analyze_image_from_gcs(gcs_uri: str) -> dict:
        # Application default credentials automatically retrieve the
        # Agent Identity token from the metadata server.
        agent_identity_credentials, project_id = default()

        client = vision.https://docs.cloud.google.com/python/docs/reference/vision/latest/google.cloud.vision_v1.services.image_annotator.ImageAnnotatorClient.html(
            credentials=agent_identity_credentials,
            project=project_id
        )

        # Prepare the image object with the Cloud Storage URI.
        image = vision.https://docs.cloud.google.com/python/docs/reference/vision/latest/google.cloud.vision_v1.types.Image.html()
        image.source.image_uri = gcs_uri

        # Perform label detection on the image.
        response = client.label_detection(image=image)

        # Check for any errors returned by the API.
        if response.error.message:
            return {"status": "failure", "error_message": response.error.message}

        labels = response.label_annotations
        return {"status": "success", "labels": [label.description for label in labels]}

## Optional: Opt out of Context-Aware Access

A default Google-managed Context-Aware Access policy helps to secure Agent Identity credentials. Beyond the Agent Gateway, the policy enforces Demonstrable Proof of Possession (DPoP) by authenticating the agent's access token. The policy also enforces that mTLS is used to access the Agent Gateway. This ensures that certificate-bound tokens can only be used from their intended, trusted runtime environment (for example, a Cloud Run container). This security baseline makes stolen credentials unreplayable, helping to protect against credential theft and account takeover (ATO).

In rare cases, such as specific token-sharing requirements among agents, if
you need to inject the token directly in the header, or if your agent can't
authenticate with a [401 UNAUTHENTICATED error](https://docs.cloud.google.com/iam/docs/troubleshoot-auth-manager#401-error), you
can opt out of the default Context-Aware Access policy. Opting out removes the
protection of token binding, making these short-lived access tokens vulnerable
to theft or replay attacks. Therefore, opting out **isn't recommended**.

To opt out, set the following environment variable
when you deploy your agent:

```python
config={
  "env_vars": {
    "GOOGLE_API_PREVENT_AGENT_TOKEN_SHARING_FOR_GCP_SERVICES": False,
  }
}
```

## Deploy the agent

When you deploy your agent to Google Cloud, ensure that Agent Identity is
enabled.
If you're deploying to Agent Runtime, use the `identity_type=AGENT_IDENTITY`
flag:

    import https://docs.cloud.google.com/python/docs/reference/vertexai/latest
    from vertexai import https://docs.cloud.google.com/python/docs/reference/vertexai/latest/vertexai._genai.types.html
    from vertexai.agent_engines import https://docs.cloud.google.com/python/docs/reference/vertexai/latest/vertexai.preview.reasoning_engines.AdkApp.html

    # Initialize the Vertex AI client with v1beta1 API for Agent Identity support
    client = https://docs.cloud.google.com/python/docs/reference/vertexai/latest.Client(
        project="PROJECT_ID",
        location="LOCATION",
        http_options=dict(api_version="v1beta1")
    )

    # Use the proper wrapper class for your Agent Framework (e.g., AdkApp)
    app = AdkApp(agent=agent)

    # Deploy the agent with Agent Identity enabled
    remote_app = client.https://docs.cloud.google.com/python/docs/reference/vertexai/latest/vertexai._genai.agent_engines.html.create(
        agent=app,
        config={
            "identity_type": https://docs.cloud.google.com/python/docs/reference/vertexai/latest/vertexai._genai.types.html.https://docs.cloud.google.com/python/docs/reference/vertexai/latest/vertexai._genai.types.IdentityType.html.https://docs.cloud.google.com/python/docs/reference/vertexai/latest/vertexai._genai.types.IdentityType.html#vertexai__genai_types_IdentityType_AGENT_IDENTITY,
            "requirements": ["google-cloud-aiplatform[agent_engines,adk]"],
        },
    )

## What's next

- [Authenticate using 2-legged OAuth with auth manager](https://docs.cloud.google.com/iam/docs/auth-with-2lo)
- [Authenticate using 3-legged OAuth with auth manager](https://docs.cloud.google.com/iam/docs/auth-with-3lo)
- [Authenticate using API key with auth manager](https://docs.cloud.google.com/iam/docs/auth-with-api-key)
- [Manage Agent Identity auth providers](https://docs.cloud.google.com/iam/docs/manage-auth-providers)
- [Troubleshoot Agent Identity auth manager](https://docs.cloud.google.com/iam/docs/troubleshoot-auth-manager)
- [Agent Identity overview](https://docs.cloud.google.com/iam/docs/agent-identity-overview)
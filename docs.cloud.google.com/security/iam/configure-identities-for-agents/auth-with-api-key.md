# [Authenticate using API key with auth manager](https://docs.cloud.google.com/iam/docs/auth-with-api-key.md.txt)

> [!WARNING]
>
> **Preview**
>
>
> This feature is
>
> subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
> [Service Specific
> Terms](https://docs.cloud.google.com/terms/service-terms#1).
>
> Pre-GA features are available "as is" and might have limited support.
>
> For more information, see the
> [launch stage descriptions](https://cloud.google.com/products/#product-launch-stages).

To let your agents authenticate to external tools like Google Maps or Weather
APIs, configure outbound authentication using API key auth providers in
Agent Identity auth manager.

API key auth providers manage your cryptographic keys for you. This capability
removes the need to hardcode keys in your agent's code or manage them manually.

## API key workflow

API key auth providers use the agent's identity and don't require user consent.
Google takes measures to help secure the API key during storage. When you use the Agent Development Kit (ADK),
it automatically retrieves and injects the API key into the tool invocation
headers.

## Before you begin

1. [Verify that you have chosen the correct authentication method](https://docs.cloud.google.com/iam/docs/agent-identity-overview#auth-models).
2.


   Enable the Agent Identity Connector API.


   **Roles required to enable APIs**


   To enable APIs, you need the Service Usage Admin IAM
   role (`roles/serviceusage.serviceUsageAdmin`), which
   contains the `serviceusage.services.enable` permission. [Learn how to grant
   roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access).

   [Enable the API](https://console.cloud.google.com/flows/enableapi?apiid=iamconnectors.googleapis.com)

   <br />

3. [Create and deploy an agent](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/quickstart-adk).

4. Obtain the **API key** from the third-party service that you want to
   connect to.

5. [Verify that you have the roles required to complete
   this task](https://docs.cloud.google.com/iam/docs/auth-with-api-key#req-roles).

### Required roles


To get the permissions that
you need to create and use an API key auth provider,

ask your administrator to grant you the
following IAM roles on the project:

- To create auth providers:
  - [IAM Connector Admin](https://docs.cloud.google.com/iam/docs/roles-permissions/iamconnectors#iamconnectors.admin) (`roles/iamconnectors.admin`)
  - [IAM Connector Editor](https://docs.cloud.google.com/iam/docs/roles-permissions/iamconnectors#iamconnectors.editor) (`roles/iamconnectors.editor`)
- To use auth providers:
  - [IAM Connector User](https://docs.cloud.google.com/iam/docs/roles-permissions/iamconnectors#iamconnectors.user) (`roles/iamconnectors.user`)
  - [Agent Default Access](https://docs.cloud.google.com/iam/docs/roles-permissions/aiplatform#aiplatform.agentDefaultAccess) (`roles/aiplatform.agentDefaultAccess`)
  - [Agent Context Editor](https://docs.cloud.google.com/iam/docs/roles-permissions/aiplatform#aiplatform.agentContextEditor) (`roles/aiplatform.agentContextEditor`)
  - [Vertex AI User](https://docs.cloud.google.com/iam/docs/roles-permissions/aiplatform#aiplatform.user) (`roles/aiplatform.user`)
  - [Service Usage Consumer](https://docs.cloud.google.com/iam/docs/roles-permissions/serviceusage#serviceusage.serviceUsageConsumer) (`roles/serviceusage.serviceUsageConsumer`)


For more information about granting roles, see [Manage access to projects, folders, and organizations](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access).


These predefined roles contain

the permissions required to create and use an API key auth provider. To see the exact permissions that are
required, expand the **Required permissions** section:


#### Required permissions

The following permissions are required to create and use an API key auth provider:

- To create auth providers: `` `iamconnectors.connectors.create` ``
- To use auth providers:
  - `` `iamconnectors.connectors.retrieveCredentials` ``
  - `` `aiplatform.endpoints.predict` ``
  - `` `aiplatform.sessions.create` ``


You might also be able to get
these permissions
with [custom roles](https://docs.cloud.google.com/iam/docs/creating-custom-roles) or
other [predefined roles](https://docs.cloud.google.com/iam/docs/roles-overview#predefined).

## Create an API key auth provider

Create an auth provider to define the configuration and credentials for third-party applications.

To create an API key auth provider, use the Google Cloud console or the Google Cloud CLI.

### Console

1. In the Google Cloud console, go to the **Agent Registry** page.

   [Go to Agent Registry](https://console.cloud.google.com/agent-platform/agent-registry/)
2. Click the name of the agent that you want to create an auth provider for.
3. Click **Identity**.
4. In the **Auth Providers** section, click **Add auth provider**.
5. In the **Add auth provider** pane, enter a name and description.

   The name can contain only lowercase letters, numbers, or hyphens, cannot end with a hyphen, and must start with a lowercase letter.
6. From the **OAuth Type** list, select **API key** .
7. Click **Create and continue**.
8. To grant your agent identity permission to use the auth provider, click **Grant access** .

   This automatically assigns the **Connector User**
   (`roles/iamconnectors.user`) role to the agent identity on the
   auth provider resource.
9. In the **Auth provider credentials** section, enter the **API key**.
10. Click **Add provider config**.

The newly created auth provider appears in the **Auth Providers** list.

### Google Cloud CLI

1. Create the auth provider:

       gcloud alpha agent-identity connectors create AUTH_PROVIDER_NAME \
           --location="`LOCATION`" \
           --api-key="`API_KEY`"

2. To grant your agent identity permission to use auth providers, update the
   IAM allow policy for either the project or the specific auth
   provider, and grant the **Connector User** (`roles/iamconnectors.user`)
   role to the agent principal.

   Agent Identity is based on the industry-standard **SPIFFE** ID format. In
   IAM allow policies, agent identities are referred to using
   **principal identifiers**.

   ### Project-level (gcloud)

   Granting the role at the project level allows the agent to use any auth
   provider in that project.
   - To grant a single agent access to auth providers in a project, run the
     following command:

         gcloud projects add-iam-policy-binding PROJECT_ID \
             --role='roles/iamconnectors.user' \
             --member="principal://agents.global.org-`ORGANIZATION_ID`.system.id.goog/resources/aiplatform/projects/`PROJECT_NUMBER`/locations/`LOCATION`/reasoningEngines/`ENGINE_ID`"

   - To grant all agents in a project access to auth providers, run the
     following command:

         gcloud projects add-iam-policy-binding PROJECT_ID \
             --role='roles/iamconnectors.user' \
             --member="principalSet://agents.global.org-`ORGANIZATION_ID`.system.id.goog/attribute.platformContainer/aiplatform/projects/`PROJECT_NUMBER`"

   ### Connector-level (curl)

   To grant a single agent access to a specific auth provider, use the
   `setIamPolicy` API. This command overwrites any existing
   allow policy on the resource.

   ```bash
   curl -X POST \
       -H "Authorization: Bearer $(gcloud auth print-access-token)" \
       -H "Content-Type: application/json" \
       -d '{
     "policy": {
       "bindings": [
         {
           "role": "roles/iamconnectors.user",
           "members": ["principal://agents.global.org-`ORGANIZATION_ID`.system.id.goog/resources/aiplatform/projects/`PROJECT_NUMBER`/locations/`LOCATION`/reasoningEngines/`ENGINE_ID`"]
         }
       ]
     }
   }' \
       "https://iamconnectors.googleapis.com/v1alpha/projects/`PROJECT_ID`/locations/`LOCATION`/connectors/`AUTH_PROVIDER_NAME`:setIamPolicy"
   ```

   Replace the following:
   - `PROJECT_ID`: Your Google Cloud project ID.
   - `AUTH_PROVIDER_NAME`: The name of the auth provider.
   - `ORGANIZATION_ID`: Your Google Cloud organization ID.
   - `PROJECT_NUMBER`: Your Google Cloud project number.
   - `LOCATION`: The location for your agent (for example, `us-central1`).
   - `ENGINE_ID`: The ID of your reasoning engine.

## Authenticate in your agent code

To authenticate your agent, you can use the ADK.

### ADK

Reference the auth provider in your agent's code using the MCP toolset in the
ADK.

```python
from google.adk.agents.llm_agent import LlmAgent
from google.adk.auth.credential_manager import CredentialManager
from google.adk.integrations.agent_identity import GcpAuthProvider, GcpAuthProviderScheme
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.auth.auth_tool import AuthConfig

# Register the Google Cloud auth provider so the CredentialManager can use it.
CredentialManager.register_auth_provider(GcpAuthProvider())

# Create the Google Cloud auth provider scheme using the auth provider's full resource name.
auth_scheme = GcpAuthProviderScheme(
    name="projects/`PROJECT_ID`/locations/`LOCATION`/connectors/`AUTH_PROVIDER_NAME`"
)

# Configure an MCP tool with the authentication scheme.
toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(url="https://YOUR_MCP_SERVER_URL"),
    auth_scheme=auth_scheme,
)

# Initialize the agent with the authenticated tools.
agent = LlmAgent(
    name="YOUR_AGENT_NAME",
    model="gemini-2.0-flash",
    instruction="YOUR_AGENT_INSTRUCTIONS",
    tools=[toolset],
)
```

### ADK

Reference the auth provider in your agent's code using an authenticated
function tool in the ADK.

```python
import httpx
from google.adk.agents.llm_agent import LlmAgent
from google.adk.auth.credential_manager import CredentialManager
from google.adk.integrations.agent_identity import GcpAuthProvider
from google.adk.integrations.agent_identity import GcpAuthProviderScheme
from google.adk.apps import App
from google.adk.auth.auth_credential import AuthCredential
from google.adk.auth.auth_tool import AuthConfig
from google.adk.tools.authenticated_function_tool import AuthenticatedFunctionTool
from vertexai import agent_engines

# First, register Google Cloud auth provider
CredentialManager.register_auth_provider(GcpAuthProvider())

# Create Auth Config
spotify_auth_config = AuthConfig(
    auth_scheme=GcpAuthProviderScheme(
        name="projects/PROJECT_ID/locations/LOCATION/connectors/AUTH_PROVIDER_NAME"
    )
)

# Use the Auth Config in Authenticated Function Tool
spotify_search_track_tool = AuthenticatedFunctionTool(
    func=spotify_search_track, auth_config=spotify_auth_config
)

# Sample function tool
async def spotify_search_track(credential: AuthCredential, query: str) -> str | list:
    token = None
    if credential.http and credential.http.credentials:
        token = credential.http.credentials.token

    if not token:
        return "Error: No authentication token available."

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.spotify.com/v1/search",
            headers={"Authorization": f"Bearer {token}"},
            params={"q": query, "type": "track", "limit": 1},
        )
        # Add your own logic here

agent = LlmAgent(
    name="YOUR_AGENT_NAME",
    model="YOUR_MODEL_NAME",
    instruction="YOUR_AGENT_INSTRUCTIONS",
    tools=[spotify_search_track_tool],
)

app = App(
    name="YOUR_APP_NAME",
    root_agent=agent,
)

vertex_app = agent_engines.AdkApp(app_name=app)
```

### ADK

Reference the auth provider in your agent's code using the
Agent Registry MCP toolset in the ADK.

```python
from google.adk.agents.llm_agent import LlmAgent
from google.adk.auth.credential_manager import CredentialManager
from google.adk.integrations.agent_identity import GcpAuthProvider
from google.adk.integrations.agent_identity import GcpAuthProviderScheme
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.auth.auth_tool import AuthConfig
from google.adk.integrations.agent_registry import AgentRegistry

# First, register Google Cloud auth provider
CredentialManager.register_auth_provider(GcpAuthProvider())

# Create Google Cloud auth provider scheme by providing Auth Provider full resource name
auth_scheme = GcpAuthProviderScheme(
    name="projects/PROJECT_ID/locations/LOCATION/connectors/AUTH_PROVIDER_NAME"
)

# Set Agent Registry
registry = AgentRegistry(project_id="PROJECT_ID", location="global")

toolset = registry.get_mcp_toolset(mcp_server_name="projects/PROJECT_ID/locations/global/mcpServers/agentregistry-00000000-0000-0000-0000-000000000000", auth_scheme=auth_scheme)

# Example MCP tool
toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(url="MCP_URL"),
    auth_scheme=auth_scheme,
)

agent = LlmAgent(
    name="YOUR_AGENT_NAME",
    model="YOUR_MODEL_NAME",
    instruction="YOUR_AGENT_INSTRUCTIONS",
    tools=[toolset],
)

  
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
            "requirements": ["google-cloud-aiplatform[agent_engines,adk]", "google-adk[agent-identity]"],
        },
    )

## What's next

- [Agent Identity overview](https://docs.cloud.google.com/iam/docs/agent-identity-overview)
- [Authenticate using 3-legged OAuth with auth manager](https://docs.cloud.google.com/iam/docs/auth-with-3lo)
- [Authenticate using 2-legged OAuth with auth manager](https://docs.cloud.google.com/iam/docs/auth-with-2lo)
- [Manage Agent Identity auth providers](https://docs.cloud.google.com/iam/docs/manage-auth-providers)
- [Troubleshoot Agent Identity auth manager](https://docs.cloud.google.com/iam/docs/troubleshoot-auth-manager)
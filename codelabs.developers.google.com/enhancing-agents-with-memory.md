# [Next ‘26 Developer Keynote: Enhancing Agents with Memory](https://codelabs.developers.google.com/next26/dev-keynote/enhancing-agents-with-memory)

## 1\. Introduction

In this codelab, you will take your ADK agents to the next level by adding persistent and specialized knowledge. You will learn how to manage conversation state with Agent Platform Sessions, enable long-term learning with Memory Bank, and integrate complex city rules data using Spark and AlloyDB for RAG (Retrieval-Augmented Generation).

## What you'll do

*   Configure **Agent Platform Sessions** for conversation persistence.
*   Implement a **Memory Bank** to allow agents to learn from previous interactions.
*   Use **Spark Lightning Engine** to ingest and process city rules documentation.
*   Build a **RAG** system using **AlloyDB** and vector search.
*   Deploy the enhanced agent to Agent Platform.

## What you'll need

*   A web browser such as [Chrome](https://www.google.com/chrome/)
*   A Google Cloud project with [billing enabled](https://docs.cloud.google.com/billing/docs/how-to/modify-project?utm_campaign=CDR_0x6cb6c9c7_default_b505354379&utm_medium=external&utm_source=lab)
*   Basic familiarity with Python and SQL

Estimated duration: 60 minutes

The resources created in this codelab should cost less than $5.

## 2\. Before you begin

### Create a Google Cloud Project

1.  In the [Google Cloud Console](https://console.cloud.google.com/), on the project selector page, [**select or create a Google Cloud project**](https://cloud.google.com/resource-manager/docs/creating-managing-projects).
2.  Make sure that billing is enabled for your Cloud project. Learn how to [check if billing is enabled on a project](https://cloud.google.com/billing/docs/how-to/verify-billing-enabled).

### Start Cloud Shell

**Cloud Shell** is a command-line environment running in Google Cloud that comes preloaded with necessary tools.

1.  Click **Activate Cloud Shell** at the top of the Google Cloud console.
2.  Once connected to Cloud Shell, verify your authentication:```
    gcloud auth list
    ```
    
3.  Confirm your project is configured:```
    gcloud config get project
    ```
    
4.  If your project is not set as expected, set it:```
    export PROJECT_ID=<YOUR_PROJECT_ID>
    gcloud config set project $PROJECT_ID
    ```
    

Verify authentication:

gcloud auth list

Confirm your project:

gcloud config get project

Set it if needed:

export PROJECT\_ID=<YOUR\_PROJECT\_ID>
gcloud config set project $PROJECT\_ID

### Enable APIs

Run this command to enable all the required APIs for session management, Spark processing, and AlloyDB:

gcloud services enable \\
  aiplatform.googleapis.com \\
  run.googleapis.com \\
  alloydb.googleapis.com \\
  dataproc.googleapis.com \\
  documentai.googleapis.com \\
  storage.googleapis.com \\
  secretmanager.googleapis.com
## 3\. Set up your environment

For this codelab, you will use the pre-configured environment in the keynote repository.

1.  Clone the repository and navigate to the project folder:

git clone https://github.com/GoogleCloudPlatform/next-26-keynotes
cd next-26-keynotes/devkey/enhancing-agents-with-memory

2.  Set up a Python virtual environment and install the required ADK packages:

uv venv
source .venv/bin/activate
uv sync

### Configure Environment Variables

The agent requires specific configuration to connect to Agent Platform and AlloyDB.

1.  Copy the sample environment file:

cp .env.example .env

2.  Open `.env` and update the following fields:
    *   `GOOGLE_CLOUD_PROJECT`: Your Project ID.
    *   `GOOGLE_CLOUD_LOCATION`: `us-central1`.
    *   `ALLOYDB_CLUSTER_ID`: `rules-db`.

GOOGLE\_CLOUD\_PROJECT=<YOUR\_PROJECT\_ID>
GOOGLE\_CLOUD\_LOCATION=global
GOOGLE\_GENAI\_USE\_VERTEXAI=TRUE
GOOGLE\_CLOUD\_REGION=us-central1
ALLOYDB\_CLUSTER\_ID=rules-db

3.  Run the following helper script to create an **Agent Engine instance** to be used for conversation sessions and long-term memory. This will automatically populate the `AGENT_ENGINE_ID` in your `.env` file:

uv run utils/setup\_agent\_engine.py

Once successful, you should see:

```
Creating Agent Engine instance...
Successfully created Agent Engine. ID: 1234567890
Updated .env with AGENT_ENGINE_ID=1234567890
```
## 4\. Create an agent with Session Management

In this step, you will initialize a **Marathon Planner Agent** that can maintain conversation history across multiple turns. This is achieved using the ADK `App` class and the **Agent Platform Sessions**.

## Initialize the Agent and Session Service

Open `planner_agent/agent.py`. You will see how we are adding an ADK class to integrate **Agent Platform Sessions**. This gives us the ability to make our agents stateful over time, and modify context as needed.

```
from google.adk.agents import LlmAgent
from google.adk.sessions import VertexAiSessionService
from vertexai.agent_engines import AdkApp

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
REGION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")

# Initialize Vertex AI for regional services
if PROJECT_ID:
    vertexai.init(project=PROJECT_ID, location=REGION)

# Define the agent logic
root_agent = LlmAgent(
    name="planner_agent",
    model="gemini-3-flash-preview",
    instruction="You are a helpful marathon planning assistant...",
    tools=[] # We will add tools in the next steps
)

def session_service_builder():
    """Builder for Agent Platform Sessions."""
    return VertexAiSessionService(project=PROJECT_ID, location=REGION)

# Wrap the agent in an AdkApp to manage stateful context
app = AdkApp(
    agent=root_agent,
    session_service_builder=session_service_builder
)
```
## 5\. Enable Long-Term Learning with Memory Bank

While session management tracks individual conversations, you can do the same thing for long-term memory. In this step, you will attach the agent to **Agent Platform's Memory Bank**, an enterprise-ready and fully managed memory service.

## Initialize Memory Bank Service

Memory Bank allows the agent to recall context across different sessions. Update `planner_agent/agent.py` to include the memory service:

```
from google.adk.memory import VertexAiMemoryBankService

def memory_service_builder():
    """Builder for Agent Platform Memory Bank."""
    return VertexAiMemoryBankService(
        project=PROJECT_ID,
        location=REGION,
        agent_engine_id=AGENT_ENGINE_ID
    )
```

## Implement Automatic Memory Ingestion

To ensure the agent learns from every turn, we add an `after_agent_callback`. This function is triggered after the agent completes a response, allowing it to "digest" the session and save relevant memories to the bank.

1.  Define the callback function:

```
async def auto_save_memories(callback_context):
    """Callback to ingest the session into the memory bank after the turn."""
    # In AdkApp, the memory service is available via the invocation context
    if hasattr(callback_context._invocation_context, 'memory_service') and callback_context._invocation_context.memory_service:
        await callback_context._invocation_context.memory_service.add_session_to_memory(
            callback_context._invocation_context.session
        )
```

2.  Attach the callback to the `LlmAgent`:

```
root_agent = LlmAgent(
    # ... other params
    after_agent_callback=[auto_save_memories],
)
```
## 6\. Setting up AlloyDB for RAG

Before we can ingest city rules data, we need a high-performance database to store it. In this step, you will create an AlloyDB cluster and initialize the database schema for vector search.

### 1\. Create the AlloyDB Cluster and Primary Instance

Run these commands in Cloud Shell to create your cluster and its primary instance:

\# Create the cluster
gcloud alloydb clusters create rules-db \\
  --password=postgres \\
  --region=us-central1

# Create the primary instance with IAM authentication enabled
gcloud alloydb instances create rules-db-primary \\
  --instance-type=PRIMARY \\
  --cpu-count=2 \\
  --region=us-central1 \\
  --cluster=rules-db \\
  --database-flags=alloydb.iam\_authentication=on

### 2\. Grant Required IAM Roles

To use the managed AlloyDB MCP server, your identity needs specific permissions. Run these commands to grant the required roles:

export USER\_EMAIL=$(gcloud config get-value account)

# Role to use MCP tools
gcloud projects add-iam-policy-binding $PROJECT\_ID \\
  --member="user:$USER\_EMAIL" \\
  --role="roles/mcp.toolUser"

# Role to execute SQL in AlloyDB
gcloud projects add-iam-policy-binding $PROJECT\_ID \\
  --member="user:$USER\_EMAIL" \\
  --role="roles/alloydb.admin"

# Role for IAM database authentication
gcloud projects add-iam-policy-binding $PROJECT\_ID \\
  --member="user:$USER\_EMAIL" \\
  --role="roles/alloydb.databaseUser"

# Create the IAM-based database user
gcloud alloydb users create "$USER\_EMAIL" \\
  --cluster=rules-db \\
  --region=us-central1 \\
  --type=IAM\_BASED

### 3\. Create Database and Tables via AlloyDB Studio

Since AlloyDB databases and tables are managed via SQL, we will use **AlloyDB Studio** in the Google Cloud Console to finalize the schema.

1.  Navigate to **AlloyDB > Clusters** and click on `rules-db`.
2.  In the left navigation menu, click **AlloyDB Studio**.
3.  Login using the **postgres** user and the password you set (`postgres`).
4.  Run the following SQL to create the database:```
    CREATE DATABASE city_rules;
    ```
    
5.  Switch your database connection to `city_rules` in AlloyDB Studio and run the following SQL to install extensions and create the `rules` table:```
    -- Install extensions for vector search and ML
    CREATE EXTENSION IF NOT EXISTS vector;
    CREATE EXTENSION IF NOT EXISTS google_ml_integration CASCADE;
    
    -- Create the rules table
    CREATE TABLE IF NOT EXISTS rules (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        text TEXT NOT NULL,
        city TEXT NOT NULL,
        embedding vector(3072) DEFAULT NULL
    );
    
    -- Grant your IAM user access to the table (replace with your email)
    GRANT ALL PRIVILEGES ON TABLE rules TO "YOUR_EMAIL_ADDRESS";
    ```
## 7\. Ingesting City Rules Data with Spark Lightning Engine

To provide truly accurate planning, an agent needs more than just a well-crafted prompt; it needs **grounding** in data and organizational context. In this step, you will use **Spark Lightning Engine** on Dataproc Serverless to process large city rules PDFs and ingest them into AlloyDB.

## Why Spark Lightning Engine?

Grounding agents at scale requires processing massive amounts of unstructured data. **Spark Lightning Engine** is a high-performance execution engine for Spark that significantly accelerates these workloads. We use it here to perform **semantic chunking** on documents using Google's **Document AI**.

## Explore the Spark Pipeline

The ingestion logic is defined in `spark-setup/spark_alloydb_processor.py`. The pipeline follows these steps:

1.  **List PDFs**: Retrieves document URIs from a Google Cloud Storage bucket.
2.  **Semantic Extraction**: Uses a UDF (User Defined Function) to call the Document AI API.
3.  **Write to AlloyDB**: Saves the extracted text chunks into the AlloyDB table named `rules`.

```
# Extract from spark_alloydb_processor.py
def process_document(gcs_uri: str):
    # ... calls Document AI to parse PDF ...
    return chunks

# Parallel processing with Spark Lightning Engine
process_udf = udf(process_document, chunk_schema)
chunked_df = uri_df.withColumn("chunks", process_udf(col("gcs_uri"))) \
                   .select(explode(col("chunks")).alias("chunk")) \
                   .select("chunk.*")

# Save to AlloyDB for Vector Search
chunked_df.write.format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", "rules") \
    .mode("append") \
    .save()
```

## Run the Ingestion Job

Trigger the ingestion process using the provided script:

./spark-setup/run\_dataproc.sh
## 8\. RAG with AlloyDB

Now that the city rules data is in AlloyDB, the agent can use it to perform **Retrieval-Augmented Generation (RAG)**. This ensures the marathon plan adheres to specific city codes.

## The Power of AlloyDB for RAG

AlloyDB excels at vector search, allowing us to store both structured data and vector embeddings in the same place. The agent can use the built-in `embedding` function in AlloyDB to find the most relevant rules information.

## Hybrid Recall with Vector Search

To give the agent access to this data, we provide a tool that queries AlloyDB using vector similarity. You can see this logic in `hybrid_recall.sql`, which demonstrates how to calculate the distance between a query and our stored rules:

```
SELECT
    text,
    (embedding <=> 
     embedding('gemini-embedding-001', 
               'Restrictions for running a race on the Las Vegas strip')::vector) 
    as distance
FROM
    rules
WHERE city = 'Las Vegas'
ORDER BY
    distance ASC
LIMIT 5;
```

## Ground the Agent in Local Rules with a RAG Tool

To make the tool available to the agent, you must define it in `planner_agent/tools.py` and then register it in `planner_agent/agent.py`. We'll use the **managed remote AlloyDB MCP server** from Google Cloud to connect to our database.

1.  Define the tool in `planner_agent/tools.py` using the "Hybrid Recall" pattern. We'll use the `streamable_http` protocol to connect to the managed AlloyDB MCP server:

```
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def get_local_and_traffic_rules(query: str) -> str:
    """Uses vector search in AlloyDB via managed MCP server."""
    # Vector search query using built-in AlloyDB embedding functions
    sql = f"SELECT text FROM rules WHERE city = 'Las Vegas' ORDER BY embedding <=> google_ml.embedding('gemini-embedding-001', '{query}')::vector ASC LIMIT 5;"
    
    # Establish a streamable HTTP connection to the MCP server
    async with streamablehttp_client(url, headers=get_auth_headers()) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool(
                "execute_sql",
                arguments={
                    "instance": full_instance_name,
                    "database": "city_rules",
                    "sqlStatement": sql
                }
            )
            return "\n".join([c.text for c in result.content if hasattr(c, 'text')])
```

2.  Register the tool and finalize `planner_agent/agent.py`:

```
# ... imports ...

# Assemble the Agent
root_agent = LlmAgent(
    name="planner_agent",
    model="gemini-3-flash-preview",
    instruction="You are a helpful marathon planning assistant...",
    tools=[
        get_local_and_traffic_rules,
    ],
    after_agent_callback=[auto_save_memories],
)

# 2. Wrap the agent in an AdkApp to manage the stateful lifecycle
app = AdkApp(
    agent=root_agent,
    session_service_builder=session_service_builder,
    memory_service_builder=memory_service_builder
)
```
## 9\. Expert Guidance with Agent Skills

**Agent Skills** are self-contained modules that provide specific instructions, guidance, and resources to help agents perform tasks more effectively. Instead of cluttering your system prompt with complex instructions for every tool, you can encapsulate that expertise into a Skill that is loaded only when needed.

Google provides **pre-built skills for Google products** (like AlloyDB and BigQuery) to ensure your agents follow industry best practices for querying data and managing resources. You can explore these and other specialized patterns at the [Google Skills Depot](https://github.com/google/skills). You will find AlloyDB base skills [here](https://github.com/google/skills/tree/main/cloud/products/alloydb/alloydb-basics).

## 1\. Explore the Skill File

Open the pre-configured skill file at `planner_agent/skills/get-local-and-traffic-rules/SKILL.md`. Here is what it looks like:

```
---
name: get-local-and-traffic-rules
description: Retrieve local rules and traffic information for a specific jurisdiction.
---
# get_local_and_traffic_rules Skill

This skill provides guidelines on how to effectively use the `get_local_and_traffic_rules` tool.

## Overview
The `get_local_and_traffic_rules` tool interfaces with an AlloyDB database to perform vector similarity searches on a corpus of rules and traffic information using a provided natural language query.

## Usage Guidelines
1. **Query Specificity**: When calling the tool, provide specific details in the `query` argument. For example, instead of querying "food rules", use "rules regarding food vendors during public events".
2. **Contextual Use**: Use the tool when planning events or activities that require adherence to local municipal or state rules (e.g., street closures, noise ordinances, environmental rules).
3. **Handling Results**: The tool returns a string containing the text of the top 5 most relevant rules. If no error occurs, parse the returned string to inform your planning tasks.
4. **Error Handling**: If an error string is returned (e.g., "Error querying rules: ..."), you must report this failure or attempt an alternative approach if applicable.

## Underlying Mechanism
- The tool uses `google_ml.embedding` to convert the query into a vector representation.
- It calculates distance (`<=>`) against the `embedding` column in the `rules` table on an AlloyDB instance.
- Results are fetched in descending order of similarity, limited to 5 results.
```

## 2\. How the Skill is Registered

In `planner_agent/agent.py`, the skill is loaded from the directory and added to the agent's tools. Here is what the code looks like:

```
import pathlib
from google.adk.skills import load_skill_from_dir
from google.adk.tools import skill_toolset

# Load the AlloyDB skill from its directory
alloydb_skill = load_skill_from_dir(pathlib.Path(__file__).parent / "skills" / "get-local-and-traffic-rules")

# Assemble the Agent with the Skill Toolset
root_agent = LlmAgent(
    name="planner_agent",
    model="gemini-3-flash-preview",
    instruction="You are a helpful marathon planning assistant...",
    tools=[
        get_local_and_traffic_rules,
        skill_toolset.SkillToolset(skills=[alloydb_skill])
    ],
    after_agent_callback=[auto_save_memories],
)
```

## 10\. Test the Agent

1.  Start the agent locally:

uv run adk run planner\_agent

2.  Ask a question about city rules: `[user]: What are the rules for running a race on the Las Vegas strip?`

The agent will call the `get_local_and_traffic_rules` tool, perform a vector search in AlloyDB, and return an answer based on the official rules chunks processed by Spark.

## 11\. Deploy the Agent

## Deploy to Agent Platform

uv run adk deploy agent\_engine \\
  --env\_file .env \\
  planner\_agent

## 12\. Clean up

To avoid ongoing charges, delete the resources created during this codelab.

## Delete the AlloyDB Cluster

\# Delete the AlloyDB Cluster
gcloud alloydb clusters delete rules-db --region=us-central1 --force

## Delete the Agent Runtime App

You can delete the Reasoning Engine instance via the console or using the `gcloud` command (if you have the resource name). For simplicity, use the console:

1.  Go to the **Agent Runtime** page.
2.  Select the `planner_agent` –> click the triple-dots button on the right side.
3.  Click **Delete**.

## 13\. Congratulations

Congratulations! You have successfully enhanced an ADK agent with advanced memory and data grounding capabilities.

## What you've learned

*   **Stateful Agents**: Integrating **Agent Platform Sessions** to maintain conversation context.
*   **Long-Term Learning**: Attaching an **Agent Platform Memory Bank** to allow the agent to learn from user interactions.
*   **Data Ingestion**: Using **Spark Lightning Engine** and **Document AI** to process unstructured documents.
*   **RAG**: Building a vector search system in **AlloyDB** to ground the agent in real-world rules.

## Next Steps

*   Explore [Agent Platform documentation](https://cloud.google.com/vertex-ai/docs/agents/overview?utm_campaign=CDR_0x6cb6c9c7_default_b505354379&utm_medium=external&utm_source=lab) to learn more about managed deployment.
*   Deep dive into [AlloyDB Vector Search](https://cloud.google.com/alloydb/docs/ai/vector-search?utm_campaign=CDR_0x6cb6c9c7_default_b505354379&utm_medium=external&utm_source=lab) for advanced RAG patterns.
*   Scale your ingestion pipelines with [Dataproc Serverless](https://cloud.google.com/dataproc-serverless/docs?utm_campaign=CDR_0x6cb6c9c7_default_b505354379&utm_medium=external&utm_source=lab).

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.
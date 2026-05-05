# [Develop and deploy agents on Agent Runtime](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/quickstart.md.txt)

Agent Runtime lets you host agents developed with various frameworks. This document explains how to create, deploy, and test an agent using LangGraph, LangChain, AG2, or LlamaIndex.

This quickstart guides you through the following steps:

- Set up your Google Cloud project.
- Install the Agent Platform SDK for Python and your chosen framework.
- Develop a currency exchange agent.
- Deploy the agent to Agent Runtime.
- Test the deployed agent.

For the quickstart using the Agent Development Kit (ADK), see [Develop and deploy agents on Agent Platform with Agent Development Kit](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/quickstart-adk).

## Before you begin

> [!NOTE]
> **Note:** To enable APIs, you need the `serviceusage.services.enable` permission. If you don't have this permission, ask your administrator to grant you the Service Usage Admin (`roles/serviceusage.serviceUsageAdmin`) role.


To get the permissions that
you need to use Agent Runtime,

ask your administrator to grant you the
following IAM roles on your project:

- [Agent Platform User](https://docs.cloud.google.com/iam/docs/roles-permissions/aiplatform#aiplatform.user) (`roles/aiplatform.user`)
- [Storage Admin](https://docs.cloud.google.com/iam/docs/roles-permissions/storage#storage.admin) (`roles/storage.admin`)


For more information about granting roles, see [Manage access to projects, folders, and organizations](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access).


You might also be able to get
the required permissions through [custom
roles](https://docs.cloud.google.com/iam/docs/creating-custom-roles) or other [predefined
roles](https://docs.cloud.google.com/iam/docs/roles-overview#predefined).

## Install and initialize the Agent Platform SDK for Python

1. Run the following command to install the [Agent Platform SDK for Python](https://docs.cloud.google.com/vertex-ai/docs/python-sdk/use-vertex-ai-python-sdk) and other
   required packages:

   ### LangGraph

       pip install --upgrade --quiet google-cloud-aiplatform[agent_engines,langchain]>=1.112

   ### LangChain

       pip install --upgrade --quiet google-cloud-aiplatform[agent_engines,langchain]>=1.112

   ### AG2

       pip install --upgrade --quiet google-cloud-aiplatform[agent_engines,ag2]>=1.112

   ### LlamaIndex

...

2. Authenticate as a user

   ### Colab

   Run the following code:

       from google.colab import auth

       auth.authenticate_user(project_id="PROJECT_ID")

   ### Cloud Shell

   No action required.

   ### Local Shell

   Run the following command:

       gcloud auth application-default login

3. Run the following code to import Agent Platform and
   initialize the SDK:

   1. (Optional) Before testing an [agent you develop](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/quickstart#develop-agent), you need to import Agent Platform and initialize the SDK as follows:

      ### Google Cloud project

          import https://docs.cloud.google.com/python/docs/reference/vertexai/latest

          https://docs.cloud.google.com/python/docs/reference/vertexai/latest.init(
              project="PROJECT_ID",               # Your project ID.
              location="LOCATION",                # Your cloud region.
          )

      Where:
      - `PROJECT_ID` is the Google Cloud [project ID](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/quickstart#project) under
        which you [develop](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/create-an-agent) and [deploy](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/deploy-an-agent) agents

      - `LOCATION` is one of the [supported regions](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime#supported-regions).

   2. Before [deploying an agent](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/quickstart#deploy-agent), you need to import Agent Platform and initialize the SDK as follows:

      ### Google Cloud project

          import https://docs.cloud.google.com/python/docs/reference/vertexai/latest

          client = https://docs.cloud.google.com/python/docs/reference/vertexai/latest.Client(
              project="PROJECT_ID",               # Your project ID.
              location="LOCATION",                # Your cloud region.
          )

      Where:
      - `PROJECT_ID` is the Google Cloud [project ID](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/quickstart#project) under
        which you [develop](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/create-an-agent) and [deploy](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/deploy-an-agent) agents

      - `LOCATION` is one of the [supported regions](https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/agent-locations).

## Develop an agent

1. Develop a currency exchange tool for your agent:

       def get_exchange_rate(
           currency_from: str = "USD",
           currency_to: str = "EUR",
           currency_date: str = "latest",
       ):
           """Retrieves the exchange rate between two currencies on a specified date."""
           import requests

           response = requests.get(
               f"https://api.frankfurter.app/{currency_date}",
               params={"from": currency_from, "to": currency_to},
           )
           return response.json()

2. Instantiate an agent:

   ### LangGraph

       from vertexai import agent_engines

       agent = agent_engines.LanggraphAgent(
           model="gemini-2.0-flash",
           tools=[get_exchange_rate],
           model_kwargs={
               "temperature": 0.28,
               "max_output_tokens": 1000,
               "top_p": 0.95,
           },
       )

   ### LangChain

       from vertexai import agent_engines

       agent = agent_engines.LangchainAgent(
           model="gemini-2.0-flash",
           tools=[get_exchange_rate],
           model_kwargs={
               "temperature": 0.28,
               "max_output_tokens": 1000,
               "top_p": 0.95,
           },
       )

   ### AG2

       from vertexai import agent_engines

       agent = agent_engines.AG2Agent(
           model="gemini-2.0-flash",
           runnable_name="Get Exchange Rate Agent",
           tools=[get_exchange_rate],
       )

   ### LlamaIndex

...

3. Test the agent locally:

   ### LangGraph

       agent.query(input={"messages": [
           ("user", "What is the exchange rate from US dollars to SEK today?"),
       ]})

   ### LangChain

       agent.query(
           input="What is the exchange rate from US dollars to SEK today?"
       )

   ### AG2

       agent.query(
           input="What is the exchange rate from US dollars to SEK today?"
       )

   ### LlamaIndex

...

## Deploy an agent

Deploy the agent by creating a [`reasoningEngine`](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/rest/v1/projects.locations.reasoningEngines) resource in Agent Platform:

### LangGraph

    remote_agent = client.agent_engines.create(
        agent,
        config={
            "requirements": ["google-cloud-aiplatform[agent_engines,langchain]"],
            "identity_type": types.IdentityType.AGENT_IDENTITY,
        },
    )

### LangChain

    remote_agent = client.agent_engines.create(
        agent,
        config={
            "requirements": ["google-cloud-aiplatform[agent_engines,langchain]"],
            "identity_type": types.IdentityType.AGENT_IDENTITY,
        },
    )

### AG2

    remote_agent = client.agent_engines.create(
        agent,
        config={
            "requirements": ["google-cloud-aiplatform[agent_engines,ag2]"],
            "identity_type": types.IdentityType.AGENT_IDENTITY,
        },
    )

### LlamaIndex

...

## Use an agent

Test the deployed agent by sending a query:

### LangGraph

    remote_agent.query(input={"messages": [
        ("user", "What is the exchange rate from US dollars to SEK today?"),
    ]})

### LangChain

    remote_agent.query(
        input="What is the exchange rate from US dollars to SEK today?"
    )

### AG2

    remote_agent.query(
        input="What is the exchange rate from US dollars to SEK today?"
    )

### LlamaIndex


...

## Clean up


To avoid incurring charges to your Google Cloud account for
the resources used on this page, follow these steps.

    remote_agent.delete(force=True)

## What's next

##### Guide

[Agent Platform Runtime setup](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/setup)


Set up your environment to use Agent Platform Runtime.

##### Guide

[Deploy agents](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/deploy-an-agent)


Learn the five ways to deploy an agent on Agent Platform Runtime based on your development needs.

##### Guide

[Manage deployed agents](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/manage-deployed-agents)


Learn how to manage agents that have been deployed to the Agent Platform managed runtime.

##### Guide

[Use an agent](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/use-an-agent)


Use an agent with Agent Platform Runtime.

##### Resource

[Get support](https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/agent-support)


Find resources and support for Google Agent Platform.
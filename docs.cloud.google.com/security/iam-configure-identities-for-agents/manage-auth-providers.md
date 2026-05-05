---
title: "Manage Agent Identity auth providers"
source: "https://docs.cloud.google.com/iam/docs/manage-auth-providers.md.txt"
sort: 6
---
# Manage Agent Identity auth providers

In Agent Identity auth manager, you manage auth providers by editing their
details, enabling or disabling them, or deleting them when they are no longer needed.

## Before you begin

1. [Verify that you have chosen the correct authentication method](https://docs.cloud.google.com/iam/docs/agent-identity-overview#auth-models).
2. [Verify that you have the roles required to complete this task](https://docs.cloud.google.com/iam/docs/manage-auth-providers#req-roles).

### Required roles


To get the permissions that
you need to manage Agent Identity auth providers,

ask your administrator to grant you the


[IAM Connector Editor](https://docs.cloud.google.com/iam/docs/roles-permissions/iamconnectors#iamconnectors.editor) (`roles/iamconnectors.editor`)
IAM role on the project.


For more information about granting roles, see [Manage access to projects, folders, and organizations](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access).


This predefined role contains

the permissions required to manage Agent Identity auth providers. To see the exact permissions that are
required, expand the **Required permissions** section:


#### Required permissions

The following permissions are required to manage Agent Identity auth providers:

- ` iamconnectors.connectors.update `
- ` iamconnectors.connectors.delete`


You might also be able to get
these permissions
with [custom roles](https://docs.cloud.google.com/iam/docs/creating-custom-roles) or
other [predefined roles](https://docs.cloud.google.com/iam/docs/roles-overview#predefined).

## Edit an auth provider

To update the description or authentication details of an auth provider, use the
Google Cloud console or the Google Cloud CLI.

### Console

1. In the Google Cloud console, go to the **Agent Registry** page.
   [Go to Agent Registry](https://console.cloud.google.com/agent-platform/agent-registry/agents)
2. Click the name of the agent whose auth provider that you want to manage.
3. Click **Identity**.
4. In the **Auth Providers** section, find the auth provider that you want to manage.
5. For your auth provider, click the **Actions** menu and select **Edit**.
6. Update the description or authentication details as needed.
7. Click **Save**.

### Google Cloud CLI

1. To update an auth provider, run the following command:

       gcloud alpha agent-identity connectors update AUTH_PROVIDER_NAME \
           --location="`LOCATION`" \
           --description="`NEW_DESCRIPTION`" \
           --three-legged-oauth-client-id="`NEW_CLIENT_ID`" \
           --three-legged-oauth-client-secret="`NEW_CLIENT_SECRET`" \
           --three-legged-oauth-authorization-url="`NEW_ENDPOINT`"

   Replace the following:
   - `AUTH_PROVIDER_NAME`: The name of the auth provider.
   - `LOCATION`: The location of the auth provider.
   - `NEW_DESCRIPTION`: A new description for the auth provider.
   - `NEW_CLIENT_ID`: A new client ID from your third-party application.
   - `NEW_CLIENT_SECRET`: A new client secret from your third-party application.
   - `NEW_ENDPOINT`: A new URL of the third-party authorization server.

## Enable or disable an auth provider

If you want to temporarily stop an agent from using an auth provider without deleting
the auth provider, you can disable the auth provider. You can enable it again at
any time.

### Console

1. In the Google Cloud console, go to the **Agent Registry** page.
   [Go to Agent Registry](https://console.cloud.google.com/agent-platform/agent-registry/agents)
2. Click the name of the agent whose auth provider that you want to manage.
3. Click **Identity**.
4. In the **Auth Providers** section, find the auth provider that you want to manage.
5. For your auth provider, click **Actions** and select **Enable** or **Disable**.
6. In the confirmation dialog, click **Enable** or **Disable**.

### Google Cloud CLI

1. To enable an auth provider, run the following command:

       gcloud alpha agent-identity connectors update AUTH_PROVIDER_NAME \
           --location="`LOCATION`" \
           --state=enabled

2. To disable an auth provider, run the following command:

       gcloud alpha agent-identity connectors update AUTH_PROVIDER_NAME \
           --location="`LOCATION`" \
           --state=disabled

Replace the following:

- `AUTH_PROVIDER_NAME`: The name of the auth provider.
- `LOCATION`: The location of the auth provider.

## Delete an auth provider

When you no longer need an auth provider, you can delete it. Deleting an auth provider
disables it and schedules it for deletion. You can restore a deleted
auth provider within 30 days.

### Console

1. In the Google Cloud console, go to the **Agent Registry** page.
   [Go to Agent Registry](https://console.cloud.google.com/agent-platform/agent-registry/agents)
2. Click the name of the agent whose auth provider that you want to manage.
3. Click **Identity**.
4. In the **Auth Providers** section, find the auth provider that you want to manage.
5. For your auth provider, click **Actions** and select **Delete**.
6. In the confirmation dialog, click **Delete**.

### gcloud

1. To delete an auth provider, run the following command:

       gcloud alpha agent-identity connectors delete AUTH_PROVIDER_NAME \
           --location="`LOCATION`"

Replace the following:

- `AUTH_PROVIDER_NAME`: The name of the auth provider.
- `LOCATION`: The location of the auth provider.

## Restore a deleted auth provider

If you accidentally delete an auth provider, you can restore it within 30 days of
deletion. After 30 days, the auth provider is permanently deleted.

### Console

1. In the Google Cloud console, go to the **Agent Registry** page.
   [Go to Agent Registry](https://console.cloud.google.com/agent-platform/agent-registry/agents)
2. Click the name of the agent whose auth provider that you want to manage.
3. Click **Identity**.
4. In the **Auth Providers** section, find the auth provider that you want to manage.
5. For your auth provider, click **Actions** and select **Restore**.
6. In the confirmation dialog, click **Restore**.

### gcloud

1. To restore an auth provider, run the following command:

       gcloud alpha agent-identity connectors undelete AUTH_PROVIDER_NAME \
           --location="`LOCATION`"

Replace the following:

- `AUTH_PROVIDER_NAME`: The name of the auth provider.
- `LOCATION`: The location of the auth provider.

## What's next

- [Authenticate using 2-legged OAuth with auth manager](https://docs.cloud.google.com/iam/docs/auth-with-2lo)
- [Authenticate using 3-legged OAuth with auth manager](https://docs.cloud.google.com/iam/docs/auth-with-3lo)
- [Authenticate using API key with auth manager](https://docs.cloud.google.com/iam/docs/auth-with-api-key)
- [Agent Identity overview](https://docs.cloud.google.com/iam/docs/agent-identity-overview)
- [Troubleshoot Agent Identity auth manager](https://docs.cloud.google.com/iam/docs/troubleshoot-auth-manager)
import { type ApiClients, createWorkflowsClient } from "@llamaindex/ui";

const deploymentName = process.env.NEXT_PUBLIC_LLAMA_DEPLOY_DEPLOYMENT_NAME

export const clients: ApiClients = {
  workflowsClient: createWorkflowsClient({
    baseUrl: `/deployments/${deploymentName}`,
  }),
};
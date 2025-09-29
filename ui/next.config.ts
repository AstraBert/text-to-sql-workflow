import type { NextConfig } from "next";

const basePath = process.env.LLAMA_DEPLOY_DEPLOYMENT_BASE_PATH || "";
const deploymentName = process.env.LLAMA_DEPLOY_DEPLOYMENT_NAME;
const projectId = process.env.LLAMA_DEPLOY_PROJECT_ID;

const nextConfig: NextConfig = {
  // Mount app under /deployments/<name>/ui
  basePath,
  // For assets when hosted behind a path prefix
  assetPrefix: basePath || undefined,
  // Enable static export for production
  output: "export",
  // Expose base path to browser for runtime URL construction
  env: {
    NEXT_PUBLIC_LLAMA_DEPLOY_DEPLOYMENT_BASE_PATH: basePath,
    NEXT_PUBLIC_LLAMA_DEPLOY_DEPLOYMENT_NAME: deploymentName,
    NEXT_PUBLIC_LLAMA_DEPLOY_PROJECT_ID: projectId,
  },
};

export default nextConfig;

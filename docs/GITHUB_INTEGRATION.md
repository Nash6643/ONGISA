# ONGISA Forge - GitHub Integration Guide

ONGISA Forge leverages the GitHub REST API and Webhooks to perform automated code smell detection, abstract syntax tree (AST) parsing, and automated refactoring suggestions directly on pull requests.

## Setup Instructions for Developers

1. **Register a GitHub App or OAuth App**:
   - Set the Homepage URL to your deployment URL.
   - Set the Webhook URL to `https://your-api-domain.com/api/webhooks/github`.
2. **Permissions Required**:
   - **Contents**: Read-only (to fetch source files and parse AST).
   - **Pull Requests**: Read & Write (to post automated refactoring diff suggestions).
   - **Metadata**: Read-only.
3. **Environment Variables**:
   ```env
   GITHUB_CLIENT_ID=your_client_id
   GITHUB_CLIENT_SECRET=your_client_secret
   WEBHOOK_SECRET=your_webhook_secret
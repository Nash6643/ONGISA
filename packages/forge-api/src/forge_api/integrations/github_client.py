"""GitHub API and Webhook integration client for ONGISA Forge."""

import httpx
from typing import Dict, Any, Optional

class GitHubIntegrationClient:
    def __init__(self, token: Optional[str] = None):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    async def get_repository_metadata(self, owner: str, repo: str) -> Dict[str, Any]:
        """Fetch target repository info to run automated architecture audits."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/repos/{owner}/{repo}", headers=self.headers)
            response.raise_for_status()
            return response.json()
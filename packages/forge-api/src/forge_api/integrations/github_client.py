"""GitHub API client for repository metadata and source file retrieval."""

import httpx
from typing import Dict, Any, List, Optional

class GitHubAPIError(Exception):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code

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
        """Fetch repository name, description, default branch, and visibility."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/repos/{owner}/{repo}", headers=self.headers)
            if response.status_code == 404:
                raise GitHubAPIError(f"Repository {owner}/{repo} not found.", 404)
            elif response.status_code == 403:
                raise GitHubAPIError("GitHub API rate limit exceeded or missing permissions.", 403)
            response.raise_for_status()
            
            data = response.json()
            return {
                "name": data.get("name"),
                "full_name": data.get("full_name"),
                "description": data.get("description"),
                "default_branch": data.get("default_branch", "main"),
                "private": data.get("private", False)
            }

    async def get_repository_contents(self, owner: str, repo: str, path: str = "") -> List[Dict[str, Any]]:
        """Retrieve file and folder contents from a repository path."""
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
            response = await client.get(url, headers=self.headers)
            if response.status_code != 200:
                raise GitHubAPIError(f"Failed to fetch contents for {owner}/{repo}", response.status_code)
            return response.json()

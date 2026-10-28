import os
import requests

class GitHubAPIClient:
    def __init__(self, token: str | None = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            **({"Authorization": f"Bearer {self.token}"} if self.token else {})
        }

    def get_repository_metadata(self, owner: str, repo: str) -> dict:
        url = f"{self.base_url}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
"""Service to import GitHub repositories into ONGISA analysis engine."""

from forge_api.integrations.github_client import GitHubIntegrationClient
from typing import Dict, Any

class GitHubImportService:
    def __init__(self, client: GitHubIntegrationClient):
        self.client = client

    async def prepare_repository_audit(self, owner: str, repo: str) -> Dict[str, Any]:
        """Fetch metadata and prepare repo context for AST smell analysis."""
        metadata = await self.client.get_repository_metadata(owner, repo)
        contents = await self.client.get_repository_contents(owner, repo)
        
        return {
            "repository": metadata,
            "root_files_count": len(contents),
            "status": "ready_for_analysis"
        }

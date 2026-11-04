import pytest
import httpx
from unittest.mock import AsyncMock, patch
from forge_api.integrations.github_client import GitHubIntegrationClient, GitHubAPIError

@pytest.mark.asyncio
async def test_get_repository_metadata_success():
    client = GitHubIntegrationClient(token="fake_token")
    mock_response = {
        "name": "ongisa",
        "full_name": "user/ongisa",
        "description": "AI Code Refactoring",
        "default_branch": "main",
        "private": False
    }
    
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = httpx.Response(200, json=mock_response)
        
        meta = await client.get_repository_metadata("user", "ongisa")
        assert meta["name"] == "ongisa"
        assert meta["default_branch"] == "main"

@pytest.mark.asyncio
async def test_get_repository_not_found():
    client = GitHubIntegrationClient()
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = httpx.Response(404)
        
        with pytest.raises(GitHubAPIError) as excinfo:
            await client.get_repository_metadata("user", "nonexistent")
        assert excinfo.value.status_code == 404

@pytest.mark.asyncio
async def test_rate_limit_exceeded():
    client = GitHubIntegrationClient()
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = httpx.Response(403)
        
        with pytest.raises(GitHubAPIError) as excinfo:
            await client.get_repository_metadata("user", "throttled-repo")
        assert excinfo.value.status_code == 403

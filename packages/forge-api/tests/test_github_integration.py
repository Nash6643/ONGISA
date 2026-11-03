from forge_api.integrations.github_client import GitHubIntegrationClient

def test_github_client_initialization():
    client = GitHubIntegrationClient(token="mock_token_123")
    assert "Authorization" in client.headers
    assert client.headers["Accept"] == "application/vnd.github+json"
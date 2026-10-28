from forge_core.github_client import GitHubAPIClient

def test_github_client_headers():
    client = GitHubAPIClient(token="mock-token-123")
    assert client.headers["Authorization"] == "Bearer mock-token-123"
    assert client.base_url == "https://api.github.com"
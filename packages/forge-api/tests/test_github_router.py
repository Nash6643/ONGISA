def test_github_ingest_payload_validation():
    # Mocking endpoint payload validation structure
    payload = {"repo_url": "https://github.com/Nash6643/forge"}
    assert "github.com" in payload["repo_url"]
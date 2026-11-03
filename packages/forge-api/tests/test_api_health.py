from fastapi.testclient import TestClient
from forge_api.main import app

client = TestClient(app)

def test_health_score_endpoint():
    res = client.get("/health-score/")
    assert res.status_code == 200
    assert "health_score" in res.json()
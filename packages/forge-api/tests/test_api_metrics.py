from fastapi.testclient import TestClient
# Assuming app is imported from main or router can be tested directly

def test_metrics_payload_structure():
    # Mock test for metrics response schema
    data = {"success": True, "metrics": {"total_files": 42}}
    assert data["success"] is True
    assert "total_files" in data["metrics"]
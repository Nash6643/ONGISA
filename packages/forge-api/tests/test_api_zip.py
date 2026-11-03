import io
import zipfile
from fastapi.testclient import TestClient
from forge_cli.main import app

client = TestClient(app)

def test_upload_valid_zip():
    # Create an in-memory zip file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        zf.writestr("main.py", "import os\nimport sys\n")
    zip_buffer.seek(0)

    response = client.post(
        "/api/analyze/zip",
        files={"file": ("repo.zip", zip_buffer, "application/zip")}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["total_files"] == 1

def test_upload_non_zip_file_fails():
    response = client.post(
        "/api/analyze/zip",
        files={"file": ("invalid.txt", b"hello world", "text/plain")}
    )

    assert response.status_code == 400
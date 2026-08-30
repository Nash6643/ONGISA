import os
import zipfile
import tempfile
import pytest
from forge_core.zip_handler import extract_zip_archive

def test_extract_valid_zip_archive():
    # Create a temporary dummy zip archive
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_zip:
        with zipfile.ZipFile(tmp_zip.name, 'w') as zf:
            zf.writestr("test_module.py", "def hello(): pass")
            zf.writestr("config.json", '{"name": "test"}')
        zip_path = tmp_zip.name

    extracted_dir = None
    try:
        extracted_dir = extract_zip_archive(zip_path)
        assert os.path.exists(extracted_dir)
        assert os.path.exists(os.path.join(extracted_dir, "test_module.py"))
        assert os.path.exists(os.path.join(extracted_dir, "config.json"))
    finally:
        if os.path.exists(zip_path):
            os.remove(zip_path)

def test_extract_invalid_zip_raises_error():
    # Create an invalid non-zip text file
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_zip:
        tmp_zip.write(b"not a real zip payload")
        zip_path = tmp_zip.name

    try:
        with pytest.raises(Exception):
            extract_zip_archive(zip_path)
    finally:
        if os.path.exists(zip_path):
            os.remove(zip_path)
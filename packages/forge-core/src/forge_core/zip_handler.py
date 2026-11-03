import os
import tempfile
import zipfile
from pathlib import Path


def extract_zip_archive(zip_path: str) -> str:
    """Extracts a .zip archive into a temporary directory and returns the path."""
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"Archive not found at path: {zip_path}")

    if not zip_path.endswith(".zip"):
        raise ValueError("File provided is not a .zip archive")

    temp_dir = tempfile.mkdtemp(prefix="ongisa_zip_")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)

    return temp_dir
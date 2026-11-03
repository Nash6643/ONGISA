import os
import tempfile
import zipfile
from pathlib import Path


class ZipValidator:
    """Validator utility for checking zip archive validity and presence."""
    @staticmethod
    def is_valid_zip(file_path: Path) -> bool:
        """Checks if the file has a .zip extension and is non-empty."""
        try:
            return file_path.suffix.lower() == ".zip" and file_path.stat().st_size > 0
        except Exception:
            return False


def extract_zip_archive(zip_path: str) -> str:
    """Extracts a .zip archive into a temporary directory and returns the path."""
    path_obj = Path(zip_path)
    
    if not path_obj.exists():
        raise FileNotFoundError(f"Archive not found at path: {zip_path}")

    if not ZipValidator.is_valid_zip(path_obj):
        raise ValueError("File provided is not a valid or non-empty .zip archive")

    temp_dir = tempfile.mkdtemp(prefix="ongisa_zip_")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)

    return temp_dir
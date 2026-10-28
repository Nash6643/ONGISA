import subprocess
import tempfile
import os

def clone_github_repository(owner: str, repo: str) -> str:
    temp_dir = tempfile.mkdtemp(prefix="ongisa_clone_")
    clone_url = f"https://github.com/{owner}/{repo}.git"
    result = subprocess.run(["git", "clone", "--depth", "1", clone_url, temp_dir], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to clone repository: {result.stderr}")
    return temp_dir
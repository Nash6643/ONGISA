import tempfile
import os
from git import Repo

class WorkspaceManager:
    def __init__(self, target_url_or_path: str):
        self.target = target_url_or_path
        self.temp_dir = None
        self.repo_path = None

    def setup_workspace(self) -> str:
        if os.path.exists(self.target):
            self.repo_path = self.target
        else:
            self.temp_dir = tempfile.TemporaryDirectory()
            Repo.clone_from(self.target, self.temp_dir.name, depth=1)
            self.repo_path = self.temp_dir.name
        return self.repo_path

    def cleanup(self):
        if self.temp_dir:
            self.temp_dir.cleanup()
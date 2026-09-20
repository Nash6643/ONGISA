import os
import tempfile
import shutil
import subprocess

from git import Repo
from git.exc import GitCommandError


class WorkspaceManager:
    """
    Creates a workspace for Forge to analyze.

    The target can be:
    - A local repository path
    - A public Git repository URL
    """

    def __init__(self, target_url_or_path: str):
        self.target = target_url_or_path
        self.temp_dir = None
        self.repo_path = None

    def setup_workspace(self) -> str:
        """
        Prepare the repository workspace.

        Returns:
            str: Path to the repository that Forge should analyze.
        """

        if not self.target or not self.target.strip():
            raise ValueError("Repository path or URL is required.")

        target = self.target.strip()

        # Local repository
        if os.path.exists(target):
            self.repo_path = os.path.abspath(target)
            return self.repo_path

        # Remote Git repository
        try:
            self.temp_dir = tempfile.TemporaryDirectory(
                prefix="forge_repo_"
            )

            Repo.clone_from(
                target,
                self.temp_dir.name,
                depth=1
            )

            self.repo_path = self.temp_dir.name

            return self.repo_path

        except GitCommandError as e:
            if self.temp_dir:
                self.temp_dir.cleanup()
                self.temp_dir = None

            raise RuntimeError(
                f"Failed to clone repository: {e}"
            ) from e

    def cleanup(self):
        """
        Remove the temporary workspace if one was created.
        """

        if self.temp_dir:
            self.temp_dir.cleanup()
            self.temp_dir = None

        self.repo_path = None

class GitCloner:
    @staticmethod
    def clone_repository(repo_url: str) -> str:
        """Clones a public git repository into a secure temporary directory and returns the path."""
        temp_dir = tempfile.mkdtemp(prefix="forge_repo_")
        try:
            subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, temp_dir],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return temp_dir
        except subprocess.CalledProcessError as e:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
            raise RuntimeError(f"Failed to clone repository: {e.stderr.strip()}")
import os
from typing import List
from forge_core.schemas import DependencyInfo

class DependencyAnalyzer:
    @staticmethod
    def extract_python_dependencies(repo_path: str) -> List[DependencyInfo]:
        """Parses requirements.txt for baseline dependency tracking."""
        req_path = os.path.join(repo_path, "requirements.txt")
        dependencies = []
        
        if os.path.exists(req_path):
            with open(req_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        parts = line.split("==")
                        pkg_name = parts[0].strip()
                        version = parts[1].strip() if len(parts) > 1 else None
                        dependencies.append(DependencyInfo(name=pkg_name, version=version))
        
        return dependencies
"""Strategy to remove unused imports from Python source files."""
from typing import List

class ImportCleanerStrategy:
    def refactor(self, source_code: str, unused_imports: List[str]) -> str:
        lines = source_code.splitlines()
        cleaned = [line for line in lines if not any(f"import {imp}" in line for imp in unused_imports)]
        return "\n".join(cleaned) + "\n"
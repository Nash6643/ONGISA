from typing import List, Dict, Set, Any
from pydantic import BaseModel
from forge_core.schemas import FileNode
from forge_analyzer.graph import DependencyGraph

class ArchitectureIssue(BaseModel):
    issue_type: str  # "Circular Dependency", "God Module", "Orphan Module", "High Coupling"
    severity: str    # "HIGH", "MEDIUM", "LOW"
    target: str
    description: str

class ArchitectureDetector:
    @staticmethod
    def detect_circular_dependencies(dep_graph: DependencyGraph) -> List[ArchitectureIssue]:
        """Detect circular import chains in the dependency graph."""
        issues = []
        visited: Set[str] = set()
        rec_stack: Set[str] = set()
        cycles: List[List[str]] = []

        def dfs(node: str, path: List[str]):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in dep_graph.imports.get(node, set()):
                if neighbor not in visited:
                    dfs(neighbor, path)
                elif neighbor in rec_stack:
                    # Found cycle
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:])

            rec_stack.remove(node)
            path.pop()

        for node in list(dep_graph.imports.keys()):
            if node not in visited:
                dfs(node, [])

        for cycle in cycles:
            cycle_str = " ➔ ".join(cycle) + f" ➔ {cycle[0]}"
            issues.append(
                ArchitectureIssue(
                    issue_type="Circular Dependency",
                    severity="HIGH",
                    target=cycle[0],
                    description=f"Circular dependency chain detected: {cycle_str}"
                )
            )

        return issues

    @staticmethod
    def detect_god_modules(files: List[FileNode], symbol_threshold: int = 20, size_kb_threshold: int = 50) -> List[ArchitectureIssue]:
        """Flag modules with excessive symbols or size as potential God Objects."""
        issues = []
        for file in files:
            symbol_count = len(file.symbols)
            size_kb = file.size_bytes / 1024

            if symbol_count >= symbol_threshold or size_kb >= size_kb_threshold:
                issues.append(
                    ArchitectureIssue(
                        issue_type="God Module",
                        severity="MEDIUM",
                        target=file.path,
                        description=f"Module contains {symbol_count} symbols and is {size_kb:.1f} KB in size."
                    )
                )
        return issues

    @staticmethod
    def detect_orphan_modules(files: List[FileNode], dep_graph: DependencyGraph) -> List[ArchitectureIssue]:
        """Flag internal non-root files that are never imported anywhere in the codebase."""
        issues = []
        all_imported_targets: Set[str] = set()
        for targets in dep_graph.imports.values():
            all_imported_targets.update(targets)

        for file in files:
            # Skip main/entrypoint files
            if file.name in {"main.py", "__init__.py", "app.py", "cli.py", "index.js", "index.ts", "lib.rs", "main.rs"}:
                continue

            if file.path not in all_imported_targets and file.path in dep_graph.imports:
                issues.append(
                    ArchitectureIssue(
                        issue_type="Orphan Module",
                        severity="LOW",
                        target=file.path,
                        description="Module is not imported by any other module in the analyzed codebase."
                    )
                )
        return issues
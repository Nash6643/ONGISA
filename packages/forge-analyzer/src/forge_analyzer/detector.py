from typing import List, Dict, Set, Any, Callable
from pydantic import BaseModel
from forge_core.schemas import FileNode
from forge_analyzer.graph import DependencyGraph

# Import new code smell rule detectors
from forge_analyzer.rules.long_method import LongMethodDetector
from forge_analyzer.rules.dead_code import DeadCodeDetector
from forge_analyzer.rules.complex_conditional import ComplexConditionalDetector
from forge_analyzer.rules.deep_nesting import DeepNestingDetector

COMMON_ENTRYPOINT_FILES = frozenset({
    "main.py", "__init__.py", "app.py", "cli.py", "index.js", "index.ts", "lib.rs", "main.rs"
})

class ArchitectureIssue(BaseModel):
    """Represents a detected architectural issue or code smell."""
    issue_type: str  # e.g., "Circular Dependency", "God Module", "Orphan Module", "Long Method", etc.
    severity: str    # e.g., "HIGH", "MEDIUM", "LOW"
    target: str
    description: str

class ArchitectureDetector:
    """
    A collection of static methods for detecting common architectural issues
    within a codebase represented by a dependency graph and file nodes.
    """

    @staticmethod
    def detect_circular_dependencies(dep_graph: DependencyGraph) -> List[ArchitectureIssue]:
        """
        Detects circular import chains in the provided dependency graph.

        Args:
            dep_graph: The dependency graph representing module imports.

        Returns:
            A list of ArchitectureIssue instances for each detected circular dependency.
        """
        issues: List[ArchitectureIssue] = []
        visited: Set[str] = set()
        rec_stack: Set[str] = set()
        cycles: List[List[str]] = []

        def dfs(node: str, path: List[str]) -> None:
            """
            Depth-first search helper to find cycles.
            """
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

        for node in dep_graph.imports:  # Optimized: Iterate directly over dict keys view
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
    def detect_god_modules(
        files: List[FileNode],
        symbol_threshold: int = 20,
        size_kb_threshold: int = 50
    ) -> List[ArchitectureIssue]:
        """
        Flags modules with excessive symbols or size as potential 'God Modules'.

        Args:
            files: A list of FileNode objects representing the files in the codebase.
            symbol_threshold: The minimum number of symbols a module must have to be considered a 'God Module'.
            size_kb_threshold: The minimum size in KB a module must have to be considered a 'God Module'.

        Returns:
            A list of ArchitectureIssue instances for each detected 'God Module'.
        """
        issues: List[ArchitectureIssue] = []
        for file in files:
            symbol_count: int = len(file.symbols)
            size_kb: float = file.size_bytes / 1024

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
    def detect_orphan_modules(
        files: List[FileNode],
        dep_graph: DependencyGraph
    ) -> List[ArchitectureIssue]:
        """
        Flags internal non-root files that are never imported anywhere in the codebase.

        Args:
            files: A list of FileNode objects representing the files in the codebase.
            dep_graph: The dependency graph representing module imports.

        Returns:
            A list of ArchitectureIssue instances for each detected orphan module.
        """
        issues: List[ArchitectureIssue] = []
        
        # Optimized: Use a set comprehension to build all_imported_targets more efficiently.
        all_imported_targets: Set[str] = {
            target
            for targets_set in dep_graph.imports.values()
            for target in targets_set
        }

        for file in files:
            # Optimized: Use the pre-defined COMMON_ENTRYPOINT_FILES frozenset for faster lookups.
            if file.name in COMMON_ENTRYPOINT_FILES:
                continue

            # A module is considered an orphan if it's not imported by any other module
            # but is present in the dependency graph's keys (meaning it has potential outgoing imports itself)
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


class SmellDetectorRegistry:
    """
    Registry that manages rule instances and runs both architecture and code smell detectors.
    """
    def __init__(self):
        self.rules = [
            LongMethodDetector(),
            DeadCodeDetector(),
            ComplexConditionalDetector(),
            DeepNestingDetector()
        ]

    def run_all(self, files: List[FileNode], dep_graph: DependencyGraph) -> List[ArchitectureIssue]:
        """
        Executes all architectural detectors and registered code smell rules,
        aggregating their findings into a single list of issues.
        """
        issues: List[ArchitectureIssue] = []

        # 1. Run core architectural checks
        issues.extend(ArchitectureDetector.detect_circular_dependencies(dep_graph))
        issues.extend(ArchitectureDetector.detect_god_modules(files))
        issues.extend(ArchitectureDetector.detect_orphan_modules(files, dep_graph))

        # 2. Run registered code smell detectors
        for rule in self.rules:
            if hasattr(rule, "detect"):
                rule_issues = rule.detect(files, dep_graph)
                if rule_issues:
                    issues.extend(rule_issues)

        return issues
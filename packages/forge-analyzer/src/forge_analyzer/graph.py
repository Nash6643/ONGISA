import json
from typing import Dict, List, Set

class DependencyGraph:
    def __init__(self):
        # file_path -> set of imported modules/files
        self.imports: Dict[str, Set[str]] = {}

    def add_import(self, source_file: str, target_module: str):
        if source_file not in self.imports:
            self.imports[source_file] = set()
        self.imports[source_file].add(target_module)

    def to_dict(self) -> Dict:
        """Export internal graph data to node-link JSON payload structure."""
        nodes = []
        links = []
        node_set: Set[str] = set()

        for source, targets in self.imports.items():
            node_set.add(source)
            for target in targets:
                node_set.add(target)
                links.append({
                    "source": source,
                    "target": target
                })

        for node in sorted(node_set):
            # Determine degree metrics
            out_degree = len(self.imports.get(node, []))
            in_degree = sum(1 for targets in self.imports.values() if node in targets)
            
            nodes.append({
                "id": node,
                "label": node.split("/")[-1],
                "in_degree": in_degree,
                "out_degree": out_degree,
                "is_internal": node in self.imports
            })

        return {
            "nodes": nodes,
            "edges": links
        }

    def to_json(self, indent: int = 2) -> str:
        """Serialize graph to a JSON string."""
        return json.dumps(self.to_dict(), indent=indent)
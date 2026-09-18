from typing import Dict, List, Any

def detect_circular_dependencies(edges: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    # Build adjacency list
    adj = {}
    for edge in edges:
        src, tgt = edge["source"], edge["target"]
        adj.setdefault(src, []).append(tgt)

    cycles = []
    visited = set()
    rec_stack = set()

    def dfs(node, path):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in adj.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, path)
            elif neighbor in rec_stack:
                cycle_start = path.index(neighbor)
                cycle_path = path[cycle_start:] + [neighbor]
                cycles.append({
                    "type": "circular_dependency",
                    "severity": "high",
                    "nodes": cycle_path,
                    "description": f"Circular dependency chain detected: {' -> '.join(cycle_path)}"
                })

        rec_stack.remove(node)
        path.pop()

    for node in list(adj.keys()):
        if node not in visited:
            dfs(node, [])

    return cycles

def analyze_code_smells(graph_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])
    issues = []

    # 1. Circular Dependencies
    issues.extend(detect_circular_dependencies(edges))

    # 2. God Object / High In-Degree Detection
    in_degree = {}
    for edge in edges:
        tgt = edge["target"]
        in_degree[tgt] = in_degree.get(tgt, 0) + 1

    for node_id, count in in_degree.items():
        if count >= 5:  # Threshold for high coupling
            issues.append({
                "type": "high_coupling",
                "severity": "medium",
                "node": node_id,
                "description": f"File '{node_id}' has {count} incoming dependencies (high coupling risk)."
            })

    return issues
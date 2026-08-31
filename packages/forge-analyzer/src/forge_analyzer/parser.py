import os
import re
from typing import Dict, List, Set, Any

PYTHON_IMPORT_RE = re.compile(
    r'^\s*(?:from\s+([\w\.]+)\s+import|import\s+([\w\.,\s]+))', re.MULTILINE
)
JS_TS_IMPORT_RE = re.compile(
    r'^\s*(?:import\s+.*?from\s+[\'"](.*?)[\'"]|require\([\'"](.*?)[\'"]\))', re.MULTILINE
)
RUST_USE_RE = re.compile(
    r'^\s*(?:use\s+([\w:]+)|mod\s+(\w+));', re.MULTILINE
)

def parse_imports(file_path: str, ext: str) -> List[str]:
    imports = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        if ext == ".py":
            matches = PYTHON_IMPORT_RE.findall(content)
            for mod_from, mod_imp in matches:
                if mod_from:
                    imports.append(mod_from.split(".")[0])
                if mod_imp:
                    for item in mod_imp.split(","):
                        imports.append(item.strip().split(".")[0])

        elif ext in [".js", ".jsx", ".ts", ".tsx"]:
            matches = JS_TS_IMPORT_RE.findall(content)
            for imp_from, req_from in matches:
                target = imp_from or req_from
                if target:
                    imports.append(target)

        elif ext == ".rs":
            matches = RUST_USE_RE.findall(content)
            for use_path, mod_name in matches:
                target = use_path or mod_name
                if target:
                    imports.append(target.split("::")[0])

    except Exception:
        pass

    return list(set(imports))

def build_dependency_graph(root_dir: str) -> Dict[str, Any]:
    nodes = []
    edges = []
    file_map: Dict[str, str] = {}

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build"}]
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, root_dir).replace("\\", "/")
            ext = os.path.splitext(f)[1].lower()

            nodes.append({
                "id": rel_path,
                "label": f,
                "extension": ext,
                "path": rel_path
            })
            file_map[rel_path] = full_path

    for node in nodes:
        source_id = node["id"]
        full_path = file_map[source_id]
        ext = node["extension"]
        detected_imports = parse_imports(full_path, ext)

        for imp in detected_imports:
            for target_node in nodes:
                target_id = target_node["id"]
                if target_id != source_id and (imp in target_id or target_id.endswith(f"/{imp}{ext}")):
                    edges.append({
                        "source": source_id,
                        "target": target_id
                    })

    return {
        "nodes": nodes,
        "edges": edges
    }
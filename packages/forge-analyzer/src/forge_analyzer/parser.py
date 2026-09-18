import os
import re
from typing import Dict, List, Any

class CodeParser:
    """Parses source files to extract raw imports and language metadata."""

    SUPPORTED_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".rs", ".cpp", ".c", ".h"}

    def parse_file_imports(self, file_path: str) -> List[str]:
        if not os.path.exists(file_path):
            return []

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in self.SUPPORTED_EXTENSIONS:
            return []

        imports = []
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            if ext == ".py":
                # Python imports: import pkg / from pkg import module
                matches = re.findall(r"^\s*(?:from|import)\s+([a-zA-Z0-9_\.]+)", content, re.MULTILINE)
                imports.extend(matches)
            elif ext in {".ts", ".tsx", ".js", ".jsx"}:
                # JS/TS imports: import ... from 'path' / require('path')
                matches = re.findall(r"from\s+['\"]([^'\"]+)['\"]|require\(['\"]([^'\"]+)['\"]\)", content)
                imports.extend([m[0] or m[1] for m in matches if m[0] or m[1]])
            elif ext == ".rs":
                # Rust imports: use crate::module / mod module
                matches = re.findall(r"^\s*(?:use|mod)\s+([a-zA-Z0-9_:]+)", content, re.MULTILINE)
                imports.extend(matches)
            elif ext in {".cpp", ".c", ".h"}:
                # C/C++ includes: #include "file.h"
                matches = re.findall(r'^\s*#include\s+["<]([^">]+)[">]', content, re.MULTILINE)
                imports.extend(matches)
        except Exception:
            pass

        return list(set(imports))


def parse_imports(file_path: str) -> List[str]:
    parser = CodeParser()
    return parser.parse_file_imports(file_path)


def build_dependency_graph(root_dir: str) -> Dict[str, Any]:
    parser = CodeParser()
    nodes = []
    edges = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in parser.SUPPORTED_EXTENSIONS:
                full_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(full_path, root_dir).replace("\\", "/")
                
                nodes.append({
                    "id": rel_path,
                    "label": filename,
                    "path": rel_path,
                    "extension": ext
                })

                detected_imports = parser.parse_file_imports(full_path)
                for imp in detected_imports:
                    edges.append({
                        "source": rel_path,
                        "target": imp
                    })

    return {"nodes": nodes, "edges": edges}
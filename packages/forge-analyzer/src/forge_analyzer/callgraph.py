import ast
from pathlib import Path

class CallGraphAnalyzer(ast.NodeVisitor):
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.calls = []
        self.defined_functions = set()

    def visit_FunctionDef(self, node):
        self.defined_functions.add(node.name)
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.calls.append({
                "caller_file": self.filepath,
                "callee": node.func.id,
                "line": node.lineno
            })
        elif isinstance(node.func, ast.Attribute):
            self.calls.append({
                "caller_file": self.filepath,
                "callee": node.func.attr,
                "line": node.lineno
            })
        self.generic_visit(node)

def analyze_directory_calls(root_dir: str) -> list:
    all_calls = []
    for path in Path(root_dir).rglob("*.py"):
        if ".venv" in path.parts or "node_modules" in path.parts:
            continue
        try:
            content = path.read_text(encoding="utf-8")
            tree = ast.parse(content)
            analyzer = CallGraphAnalyzer(str(path))
            analyzer.visit(tree)
            all_calls.extend(analyzer.calls)
        except Exception:
            pass
    return all_calls
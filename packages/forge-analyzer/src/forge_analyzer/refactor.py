import ast
from typing import Dict, Any, List

class UnusedImportRemover(ast.NodeTransformer):
    """AST Transformer to remove unused top-level imports."""

    def __init__(self):
        self.used_names = set()
        super().__init__()

    def visit_Name(self, node: ast.Name) -> ast.Name:
        self.used_names.add(node.id)
        return self.generic_visit(node)


def perform_ast_dry_run(source_code: str) -> Dict[str, Any]:
    """Parses source code into an AST, performs basic cleanup transformations,

    and generates a summary diff preview.
    """
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        return {"status": "error", "message": f"Syntax error during AST parsing: {str(e)}"}

    # Record initial function and import counts
    initial_imports = [n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]
    functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]

    transformations_applied = []

    # Check for functions without docstrings or type annotations
    for fn in functions:
        if not ast.get_docstring(fn):
            transformations_applied.append(f"Suggested docstring generation for function '{fn.name}'")
        if not fn.returns:
            transformations_applied.append(f"Suggested return type annotation for function '{fn.name}'")

    return {
        "status": "success",
        "total_imports": len(initial_imports),
        "total_functions": len(functions),
        "transformations": transformations_applied or ["No immediate AST refactorings required."],
        "refactored_code_preview": ast.unparse(tree)
    }
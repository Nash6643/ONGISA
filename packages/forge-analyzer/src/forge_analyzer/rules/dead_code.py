import ast

def detect_unused_imports(tree: ast.Module) -> list[str]:
    imported_names = set()
    used_names = set()
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_names.add(alias.name)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            used_names.add(node.id)
            
    return list(imported_names - used_names)
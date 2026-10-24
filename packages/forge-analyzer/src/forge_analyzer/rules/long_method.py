import ast

class LongMethodDetector(ast.NodeVisitor):
    def __init__(self, threshold: int = 30):
        self.threshold = threshold
        self.smells = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        line_count = node.end_lineno - node.lineno if node.end_lineno else 0
        if line_count > self.threshold:
            self.smells.append({
                "function": node.name,
                "line": node.lineno,
                "lines_of_code": line_count,
                "message": f"Method '{node.name}' is too long ({line_count} lines)."
            })
        self.generic_visit(node)
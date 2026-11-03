"""
Advanced Code Smell and Anti-Pattern Detection Engine for ONGISA.
"""

from typing import List, Dict, Any, Optional
import ast

class CodeSmellDetector(ast.NodeVisitor):
    def __init__(self, filepath: str, source_code: str):
        self.filepath = filepath
        self.source_code = source_code
        self.smells: List[Dict[str, Any]] = []
        self._current_depth = 0
        self._max_depth = 0

    def analyze(self) -> List[Dict[str, Any]]:
        try:
            tree = ast.parse(self.source_code, filename=self.filepath)
            self.visit(tree)
        except SyntaxError as e:
            self.smells.append({
                "type": "SyntaxError",
                "message": f"Failed to parse file: {e}",
                "line": e.lineno,
                "severity": "high"
            })
        return self.smells

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        # Check for Long Parameter Lists (> 5 parameters)
        args_count = len(node.args.args) + len(node.args.kwonlyargs)
        if args_count > 5:
            self.smells.append({
                "type": "LongParameterList",
                "message": f"Function '{node.name}' has {args_count} parameters (recommended max is 5).",
                "line": node.lineno,
                "severity": "medium"
            })

        # Check for Deep Nesting inside functions
        previous_max_depth = self._max_depth
        self._max_depth = 0
        self._current_depth = 0
        
        for child in node.body:
            self._check_nesting(child, depth=1)

        if self._max_depth > 3:
            self.smells.append({
                "type": "DeepNesting",
                "message": f"Function '{node.name}' contains deep control flow nesting (depth: {self._max_depth}).",
                "line": node.lineno,
                "severity": "high"
            })
            
        self._max_depth = previous_max_depth
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        # Check for Large Classes / God Objects (> 20 methods or > 300 lines)
        methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
        class_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') and node.end_lineno else 0
        
        if len(methods) > 20 or class_lines > 300:
            self.smells.append({
                "type": "GodClass",
                "message": f"Class '{node.name}' is too large ({len(methods)} methods, ~{class_lines} lines). Consider splitting responsibilities.",
                "line": node.lineno,
                "severity": "high"
            })
            
        self.generic_visit(node)

    def _check_nesting(self, node: ast.AST, depth: int) -> None:
        if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
            if depth > self._max_depth:
                self._max_depth = depth
            for child in ast.iter_child_nodes(node):
                self._check_nesting(child, depth + 1)
        else:
            for child in ast.iter_child_nodes(node):
                self._check_nesting(child, depth)

def detect_smells(filepath: str, source_code: str) -> List[Dict[str, Any]]:
    detector = CodeSmellDetector(filepath, source_code)
    return detector.analyze()
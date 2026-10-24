import ast
from forge_analyzer.metrics import calculate_cyclomatic_complexity

def test_complexity_simple_function():
    code = "def foo(x): return x + 1"
    tree = ast.parse(code)
    assert calculate_cyclomatic_complexity(tree) == 1
import ast
from forge_analyzer.rules.long_method import LongMethodDetector

def test_long_method_detection():
    code = "def large():\n" + "\n".join(["    x = 1"] * 35)
    tree = ast.parse(code)
    detector = LongMethodDetector(threshold=30)
    detector.visit(tree)
    assert len(detector.smells) == 1
    assert detector.smells[0]["function"] == "large"
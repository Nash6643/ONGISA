from forge_refactor.strategies.clean_imports import ImportCleanerStrategy

def test_clean_imports():
    code = "import os\nimport sys\nprint('hello')"
    strategy = ImportCleanerStrategy()
    result = strategy.refactor(code, ["os"])
    assert "import os" not in result
    assert "import sys" in result

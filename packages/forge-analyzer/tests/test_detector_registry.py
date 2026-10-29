from forge_analyzer.detector import SmellDetectorRegistry

def test_registry_initialization():
    registry = SmellDetectorRegistry()
    assert len(registry.rules) == 4

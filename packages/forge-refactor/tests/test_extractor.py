from forge_refactor.strategies.extractor import MethodExtractorStrategy

def test_method_extractor_suggestion():
    plan = MethodExtractorStrategy.suggest_extraction("process_order", (10, 45))
    assert plan["strategy"] == "extract_method"
    assert plan["line_range"] == (10, 45)
from forge_analyzer.rules.deep_nesting import DeepNestingDetector

def test_deep_nesting():
    detector = DeepNestingDetector(max_depth=3)
    assert detector.analyze_indentation(2, 10) is None
    res = detector.analyze_indentation(5, 12)
    assert res is not None and res["smell"] == "DeepNesting"

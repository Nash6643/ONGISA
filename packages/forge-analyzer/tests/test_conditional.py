from forge_analyzer.rules.complex_conditional import ComplexConditionalDetector

def test_complex_conditional_detection():
    detector = ComplexConditionalDetector(max_operators=2)
    assert detector.analyze_line("if a and b:", 1) is None
    res = detector.analyze_line("if a and b or c and d:", 2)
    assert res is not None and res["smell"] == "ComplexConditional"
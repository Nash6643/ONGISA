from forge_analyzer.refactor import perform_ast_dry_run

def test_ast_dry_run_analysis():
    sample_code = """
def calculate_metrics(data):
    x = 10
    return x * 2
"""
    result = perform_ast_dry_run(sample_code)
    assert result["status"] == "success"
    assert result["total_functions"] == 1
    assert len(result["transformations"]) > 0
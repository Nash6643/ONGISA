from forge_refactor.planner import RefactorPlanner

def test_refactor_planner():
    planner = RefactorPlanner()
    plan = planner.plan_refactoring({"smell": "LongMethod", "line": 42})
    assert len(plan) == 1
    assert plan[0]["action"] == "extract_method"

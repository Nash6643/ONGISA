from forge_ai.prompt_templates import REFACTOR_PROMPT_TEMPLATE

def test_refactor_prompt_formatting():
    formatted = REFACTOR_PROMPT_TEMPLATE.format(
        file_path="auth.py",
        line=42,
        smell_type="God Class",
        description="Too many methods"
    )
    assert "auth.py" in formatted
    assert "God Class" in formatted
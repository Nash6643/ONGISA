from forge_refactor.diff import generate_unified_diff

def test_diff_generator():
    orig = "a = 1\n"
    mod = "a = 2\n"
    diff = generate_unified_diff(orig, mod)
    assert "-a = 1" in diff
    assert "+a = 2" in diff
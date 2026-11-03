from forge_core.config import ForgeConfig

def test_forge_config_defaults():
    config = ForgeConfig(project_name="test-repo")
    assert config.project_name == "test-repo"
    assert config.max_line_length == 120
    assert ".git" in config.ignore_patterns
def test_cli_github_command_import():
    from forge_cli.commands.github import github_clone_command
    assert callable(github_clone_command)
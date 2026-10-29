from typer.testing import CliRunner
from forge_cli.main import app

runner = CliRunner()

def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "ONGISA Forge AI Code Analysis CLI" in result.output
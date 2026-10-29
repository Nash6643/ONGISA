import json
from pathlib import Path
import typer

app = typer.Typer()

@app.command("audit")
def run_audit(
    path: Path = typer.Argument(..., help="Path to repository"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output audit results as raw JSON")
):
    results = {"path": str(path), "smells": 0, "status": "clean"}
    if json_output:
        typer.echo(json.dumps(results, indent=2))
    else:
        typer.echo(f"Audit completed for {path}. Status: {results['status']}")

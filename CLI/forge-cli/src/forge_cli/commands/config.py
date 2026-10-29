from pathlib import Path
import typer

app = typer.Typer()

@app.command("show")
def show_config(config_path: Path = typer.Option(Path(".forge.yaml"), "--config", "-c")):
    if config_path.exists():
        typer.echo(f"Loaded config from {config_path}")
    else:
        typer.echo("Using default Forge configuration.")

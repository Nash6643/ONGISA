import sys
import os
from pathlib import Path

# Dynamically locate the 'forge' root folder by finding where 'packages' resides
CURRENT_FILE = Path(__file__).resolve()
FORGE_ROOT = next((p for p in CURRENT_FILE.parents if (p / "packages").exists()), CURRENT_FILE.parents[3])

sys.path.append(str(FORGE_ROOT / "packages" / "forge-core" / "src"))
sys.path.append(str(FORGE_ROOT / "packages" / "forge-analyzer" / "src"))

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree

from forge_core.cloner import WorkspaceManager
from forge_core.schemas import RepositoryData, FileNode
from forge_analyzer.parser import CodeParser
from forge_analyzer.dependencies import DependencyAnalyzer

app = typer.Typer(
    help="Forge CLI: Automated Repository Intelligence & Analysis Engine",
    no_args_is_help=True
)

def run_analysis(target: str):
    """Core scanner execution logic."""
    console = Console()
    console.print(Panel(f"[bold cyan]Forge Engine Scanning:[/bold cyan] [yellow]{target}[/yellow]"))

    manager = WorkspaceManager(target)
    try:
        repo_path = manager.setup_workspace()
        parser = CodeParser()
        
        files_data = []
        file_tree = Tree(f"[bold blue]📂 {os.path.basename(os.path.abspath(repo_path))}[/bold blue]")

        # Scan files in repo
        for root, dirs, files in os.walk(repo_path):
            # Exclude common meta/build folders
            dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", "node_modules", ".venv", "venv", ".idea", ".vscode"}]
                
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, repo_path)
                ext = os.path.splitext(file)[1]
                symbols = []

                # Parse Python files with Tree-Sitter
                if ext == ".py":
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            symbols = parser.parse_python_file(rel_path, f.read())
                    except Exception:
                        pass

                files_data.append(
                    FileNode(
                        path=rel_path,
                        name=file,
                        extension=ext,
                        size_bytes=os.path.getsize(full_path),
                        language="Python" if ext == ".py" else "Other",
                        symbols=symbols
                    )
                )

                # Add node to visual tree
                file_tree.add(f"[green]{rel_path}[/green] ({len(symbols)} symbols extracted)")

        # Render File Hierarchy
        console.print("\n[bold]Repository File Structure & Symbol Summary:[/bold]")
        console.print(file_tree)

        # Extract Dependencies
        deps = DependencyAnalyzer.extract_python_dependencies(repo_path)
        if deps:
            console.print("\n[bold]Dependencies Detected:[/bold]")
            dep_table = Table(show_header=True, header_style="bold magenta")
            dep_table.add_column("Package")
            dep_table.add_column("Version")
            
            for dep in deps:
                dep_table.add_row(dep.name, dep.version or "unspecified")
            
            console.print(dep_table)

    finally:
        manager.cleanup()

    console.print("\n[bold green]✓ v0.1 Analysis Complete![/bold green]\n")

@app.command(name="analyze")
def analyze_cmd(
    target: str = typer.Argument(..., help="Path to local folder or GitHub repository URL")
):
    """Analyze a local directory or remote Git repository."""
    run_analysis(target)

@app.command(name="version")
def version_cmd():
    """Print Forge version."""
    Console().print("[bold cyan]Forge CLI v0.1.0[/bold cyan]")

if __name__ == "__main__":
    app()
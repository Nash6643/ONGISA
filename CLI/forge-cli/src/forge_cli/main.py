import os
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree

from forge_core.cloner import WorkspaceManager
from forge_core.schemas import RepositoryData, FileNode
from forge_analyzer.parser import CodeParser
from forge_analyzer.dependencies import DependencyAnalyzer

app = typer.Typer(help="Forge CLI: Automated Repository Intelligence & Analysis Engine")
console = Console()

@app.command()
def analyze(
    target: str = typer.Argument(..., help="Path to local folder or GitHub repository URL")
):
    """
    Analyzes a repository and extracts tree structure, symbols, and dependencies.
    """
    console.print(Panel(f"[bold cyan]Forge Engine Scanning:[/bold cyan] [yellow]{target}[/yellow]"))

    manager = WorkspaceManager(target)
    try:
        repo_path = manager.setup_workspace()
        parser = CodeParser()
        
        files_data = []
        file_tree = Tree(f"[bold blue]📂 {os.path.basename(repo_path) or repo_path}[/bold blue]")

        # Scan files in repo
        for root, _, files in os.walk(repo_path):
            if ".git" in root or "__pycache__" in root or "node_modules" in root:
                continue
                
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
                    except Exception as e:
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

                # Add node to visual directory tree
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

if __name__ == "__main__":
    app()
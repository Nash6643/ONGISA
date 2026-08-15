import sys
from pathlib import Path

# Force Python to prefer local src folders over pip-cached site-packages
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(BASE_DIR / "packages" / "forge-analyzer" / "src"))
sys.path.insert(0, str(BASE_DIR / "packages" / "forge-core" / "src"))
sys.path.insert(0, str(BASE_DIR / "packages" / "forge-ai" / "src"))

import os
import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree
from rich.table import Table
from rich.prompt import Prompt

from forge_core.cloner import WorkspaceManager
from forge_core.schemas import FileNode
from forge_analyzer import CodeParser, DependencyGraph, DependencyAnalyzer
from forge_ai import CodebaseAgent, CodebaseVectorIndex

# Mapping file extensions to language names
LANGUAGE_MAP = {
    ".py": "Python",
    ".rs": "Rust",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript (React)",
    ".java": "Java",
    ".go": "Go",
    ".c": "C",
    ".cpp": "C++",
    ".h": "Header",
    ".json": "JSON",
    ".md": "Markdown"
}

app = typer.Typer(help="Forge CLI - Autonomous AI Software Architecture Engine")


def render_terminal_dependency_graph(console: Console, dep_graph: DependencyGraph):
    """Render a visual ASCII / Rich tree graph of module dependency connections."""
    if not dep_graph.imports:
        return

    graph_tree = Tree("[bold cyan]🌐 Dependency & Import Topology Map[/bold cyan]")
    
    for source_file, targets in dep_graph.imports.items():
        # Source node branch
        source_branch = graph_tree.add(f"[bold yellow]📄 {source_file}[/bold yellow]")
        
        for target in sorted(targets):
            # Differentiate local path imports vs external modules
            if target.startswith(".") or "/" in target or target.startswith("forge_"):
                source_branch.add(f"└── [green]🔗 {target}[/green] [dim](internal)[/dim]")
            else:
                source_branch.add(f"└── [magenta]📦 {target}[/magenta] [dim](external/lib)[/dim]")

    console.print(Panel(graph_tree, title="[bold white]Codebase Dependency Graph[/bold white]", border_style="cyan"))


def _parse_file_content(parser: CodeParser, file_path: str, content: str, ext: str):
    symbols = []
    imports = []
    if ext == ".py":
        symbols = parser.parse_python_symbols(content)
        imports = parser.parse_python_imports(content)
    return symbols, imports


def run_analysis(target: str, export_graph_path: Optional[str] = None):
    """Core scanner execution logic with Rich terminal visual rendering."""
    console = Console()
    console.print(Panel(f"[bold cyan]Forge Engine Scanning:[/bold cyan] [yellow]{target}[/yellow]"))

    manager = WorkspaceManager(target)
    dep_graph = DependencyGraph()

    try:
        repo_path = manager.setup_workspace()
        parser = CodeParser()
        
        files_data = []
        file_tree = Tree(f"[bold blue]📂 {os.path.basename(os.path.abspath(repo_path))}[/bold blue]")

        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", "node_modules", ".venv", "venv", ".idea", ".vscode"}]
                
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, repo_path)
                ext = os.path.splitext(file)[1].lower()
                symbols = []
                file_imports = []

                if ext in LANGUAGE_MAP:
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            symbols, file_imports = _parse_file_content(parser, rel_path, content, ext)
                            for imp in file_imports:
                                dep_graph.add_import(rel_path, imp.module)
                    except Exception:
                        pass

                files_data.append(
                    FileNode(
                        path=rel_path,
                        name=file,
                        extension=ext,
                        size_bytes=os.path.getsize(full_path),
                        language=LANGUAGE_MAP.get(ext, "Other"),
                        symbols=symbols
                    )
                )

                file_tree.add(f"[green]{rel_path}[/green] ({len(symbols)} symbols, {len(file_imports)} imports)")

        console.print("\n[bold]Repository Directory Structure:[/bold]")
        console.print(file_tree)

        # Render Visual Terminal Dependency Graph
        console.print()
        render_terminal_dependency_graph(console, dep_graph)

        # Export JSON graph if flag is active
        if export_graph_path:
            graph_data = dep_graph.to_json()
            with open(export_graph_path, "w", encoding="utf-8") as f:
                f.write(graph_data)
            console.print(f"\n[bold green]✓ Exported dependency graph payload to:[/bold green] [yellow]{export_graph_path}[/yellow]")

        deps = DependencyAnalyzer.extract_python_dependencies(repo_path)
        if deps:
            console.print("\n[bold]Detected Package Dependencies:[/bold]")
            dep_table = Table(show_header=True, header_style="bold magenta")
            dep_table.add_column("Package")
            dep_table.add_column("Version")
            
            for dep in deps:
                dep_table.add_row(dep.name, dep.version or "unspecified")
            
            console.print(dep_table)

    finally:
        manager.cleanup()

    console.print("\n[bold green]✓ Multi-Language Graph Analysis Complete![/bold green]\n")


@app.command(name="analyze")
def analyze_cmd(
    target: str = typer.Argument(".", help="Path to local codebase folder or GitHub repository URL"),
    export_graph: Optional[str] = typer.Option(None, "--export-graph", help="Path to export dependency graph JSON")
):
    """Analyze a codebase structure, symbols, dependencies, and import topology."""
    run_analysis(target, export_graph)


@app.command(name="chat")
def chat_cmd(
    target: str = typer.Argument(".", help="Path to local codebase folder or GitHub repository URL")
):
    """Start an interactive RAG-powered chat session with your codebase."""
    console = Console()
    console.print(Panel(f"[bold cyan]Forge AI RAG Session Initializing:[/bold cyan] [yellow]{target}[/yellow]"))

    manager = WorkspaceManager(target)
    
    try:
        repo_path = manager.setup_workspace()
        
        # Read codebase files for indexing
        console.print("[dim]Reading source files...[/dim]")
        file_contents = {}
        valid_extensions = set(LANGUAGE_MAP.keys())

        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build"}]
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in valid_extensions:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, repo_path)
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            if content.strip():
                                file_contents[rel_path] = content
                    except Exception:
                        pass

        if not file_contents:
            console.print("[bold red]No readable source files found in target repository.[/bold red]")
            return

        # Build vector index
        console.print(f"[dim]Indexing {len(file_contents)} files into local vector store...[/dim]")
        index = CodebaseVectorIndex()
        index.index_files(file_contents)
        console.print("[bold green]✓ RAG Vector Index Ready![/bold green]\n")

        agent = CodebaseAgent()

        # Interactive Chat Loop
        console.print("[bold cyan]Ask Forge AI any question about this codebase (type 'exit' or 'quit' to end):[/bold cyan]\n")
        while True:
            query = Prompt.ask("[bold green]Developer[/bold green]")
            if query.strip().lower() in {"exit", "quit"}:
                console.print("[yellow]Ending chat session. Goodbye![/yellow]")
                break
            
            if not query.strip():
                continue

            with console.status("[bold cyan]Searching code & generating response...[/bold cyan]"):
                relevant_chunks = index.search(query, top_k=3)
                response = agent.answer_with_rag(query, relevant_chunks)

            console.print(Panel(response, title="[bold magenta]Forge AI[/bold magenta]", border_style="magenta"))
            console.print()

    except Exception as e:
        console.print(f"[bold red]Error in chat session:[/bold red] {e}")
    finally:
        manager.cleanup()


if __name__ == "__main__":
    app()
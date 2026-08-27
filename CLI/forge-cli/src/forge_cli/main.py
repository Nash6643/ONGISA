import sys
from pathlib import Path

# Force Python to prefer local src folders over pip-cached site-packages
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(BASE_DIR / "packages" / "forge-analyzer" / "src"))
sys.path.insert(0, str(BASE_DIR / "packages" / "forge-core" / "src"))
sys.path.insert(0, str(BASE_DIR / "packages" / "forge-ai" / "src"))
sys.path.insert(0, str(BASE_DIR / "packages" / "forge-refactor" / "src"))

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
from forge_analyzer import (
    CodeParser,
    DependencyGraph,
    DependencyAnalyzer,
    MultiLangParser,
    ArchitectureDetector,
    ArchitectureIssue,
)
from forge_ai import CodebaseAgent, CodebaseVectorIndex
from forge_refactor import RefactorEngine

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

# Mapping extensions to tree-sitter language identifiers
TREESITTER_LANG_MAP = {
    ".py": "python",
    ".rs": "rust",
    ".js": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".java": "java",
    ".go": "go",
    ".c": "c",
    ".cpp": "cpp",
}

app = typer.Typer(help="ONGISA CLI - Omar Nashiru-deen GitHub Statistical Analyzer & Architecture Engine")


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
            if target.startswith(".") or "/" in target or target.startswith("forge_") or target.startswith("ongisa_"):
                source_branch.add(f"└── [green]🔗 {target}[/green] [dim](internal)[/dim]")
            else:
                source_branch.add(f"└── [magenta]📦 {target}[/magenta] [dim](external/lib)[/dim]")

    console.print(Panel(graph_tree, title="[bold white]Codebase Dependency Graph[/bold white]", border_style="cyan"))


def _parse_file_content(ts_parser: MultiLangParser, fallback_parser: CodeParser, file_path: str, content: str, ext: str):
    symbols = []
    imports = []
    
    # Use Tree-Sitter if language is supported
    if ext in TREESITTER_LANG_MAP:
        try:
            parsed = ts_parser.parse_code(content, TREESITTER_LANG_MAP[ext])
            symbols = parsed.get("symbols", [])
            imports = parsed.get("imports", [])
            return symbols, imports
        except Exception:
            pass

    # Fallback to python stdlib parser if Python file
    if ext == ".py":
        symbols = fallback_parser.parse_python_symbols(content)
        imports = fallback_parser.parse_python_imports(content)

    return symbols, imports


def run_analysis(target: str, export_graph_path: Optional[str] = None):
    """Core scanner execution logic with Rich terminal visual rendering."""
    console = Console()
    console.print(Panel(f"[bold cyan]ONGISA Engine Scanning:[/bold cyan] [yellow]{target}[/yellow]"))

    manager = WorkspaceManager(target)
    dep_graph = DependencyGraph()

    try:
        repo_path = manager.setup_workspace()
        fallback_parser = CodeParser()
        ts_parser = MultiLangParser()
        
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
                            symbols, file_imports = _parse_file_content(ts_parser, fallback_parser, rel_path, content, ext)
                            for imp in file_imports:
                                # Handle string vs object import representations
                                mod_name = getattr(imp, 'module', str(imp))
                                dep_graph.add_import(rel_path, mod_name)
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

        issues = []
        issues.extend(ArchitectureDetector.detect_circular_dependencies(dep_graph))
        issues.extend(ArchitectureDetector.detect_god_modules(files_data))
        issues.extend(ArchitectureDetector.detect_orphan_modules(files_data, dep_graph))

        if issues:
            console.print("\n[bold red]⚠️ Architectural Issues & Anti-Patterns Detected:[/bold red]")
            issue_table = Table(show_header=True, header_style="bold red")
            issue_table.add_column("Severity", width=10)
            issue_table.add_column("Type", width=22)
            issue_table.add_column("Target File", width=25)
            issue_table.add_column("Description")

            for issue in issues:
                color = "red" if issue.severity == "HIGH" else "yellow" if issue.severity == "MEDIUM" else "dim"
                issue_table.add_row(
                    f"[{color}]{issue.severity}[/{color}]",
                    issue.issue_type,
                    issue.target,
                    issue.description
                )

            console.print(issue_table)

    finally:
        manager.cleanup()

    console.print("\n[bold green]✓ ONGISA Analysis Complete![/bold green]\n")


@app.command(name="refactor")
def refactor_cmd(
    file_path: str = typer.Argument(..., help="Relative path to the file to refactor"),
    instruction: str = typer.Option(..., "--instruction", "-i", help="Refactoring instructions or goals"),
    apply: bool = typer.Option(False, "--apply", "-a", help="Automatically write changes to file without prompt")
):
    """Generate an AI-driven refactoring patch for a specific file and view the unified diff."""
    console = Console()
    if not os.path.exists(file_path):
        console.print(f"[bold red]Error:[/bold red] File not found at [yellow]{file_path}[/yellow]")
        return

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            original_content = f.read()

        console.print(Panel(f"[bold cyan]ONGISA Refactor Engine Target:[/bold cyan] [yellow]{file_path}[/yellow]\n[dim]Instruction: {instruction}[/dim]"))

        with console.status("[bold cyan]Analyzing code & generating refactoring patch...[/bold cyan]"):
            engine = RefactorEngine()
            result = engine.generate_refactor_patch(file_path, original_content, instruction)

        patch = result["patch"]
        if not patch:
            console.print("[yellow]No structural changes needed or proposed by engine.[/yellow]")
            return

        console.print("\n[bold white]Proposed Unified Diff Patch:[/bold white]")
        console.print(Panel(patch, border_style="magenta"))

        should_apply = apply
        if not apply:
            should_apply = Prompt.ask("Apply this patch directly to the file?", choices=["y", "n"], default="n") == "y"

        if should_apply:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(result["refactored_code"])
            console.print(f"[bold green]✓ Applied patch successfully to {file_path}[/bold green]")
        else:
            console.print("[dim]Patch discarded. No files were modified.[/dim]")

    except Exception as e:
        console.print(f"[bold red]Refactoring Error:[/bold red] {e}")


@app.command(name="analyze")
def analyze_cmd(
    target: str = typer.Argument(".", help="Path to local codebase folder or GitHub repository URL"),
    export_graph: Optional[str] = typer.Option(None, "--export-graph", help="Path to export dependency graph JSON")
):
    """Analyze codebase structure, symbols, dependencies, and import topology."""
    run_analysis(target, export_graph)


@app.command(name="chat")
def chat_cmd(
    target: str = typer.Argument(".", help="Path to local codebase folder or GitHub repository URL")
):
    """Start an interactive RAG-powered chat session with your codebase."""
    console = Console()
    console.print(Panel(f"[bold cyan]ONGISA AI Session Initializing:[/bold cyan] [yellow]{target}[/yellow]"))

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
        console.print("[bold cyan]Ask ONGISA AI any question about this codebase (type 'exit' or 'quit' to end):[/bold cyan]\n")
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

            console.print(Panel(response, title="[bold magenta]ONGISA AI[/bold magenta]", border_style="magenta"))
            console.print()

    except Exception as e:
        console.print(f"[bold red]Error in chat session:[/bold red] {e}")
    finally:
        manager.cleanup()


if __name__ == "__main__":
    app()
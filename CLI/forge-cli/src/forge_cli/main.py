import sys
import os
from pathlib import Path
from typing import List, Tuple, Optional

# Set up package import paths
CURRENT_FILE = Path(__file__).resolve()
FORGE_ROOT = next((p for p in CURRENT_FILE.parents if (p / "packages").exists()), CURRENT_FILE.parents[3])

sys.path.append(str(FORGE_ROOT / "packages" / "forge-core" / "src"))
sys.path.append(str(FORGE_ROOT / "packages" / "forge-analyzer" / "src"))
sys.path.append(str(FORGE_ROOT / "packages" / "forge-ai" / "src"))

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich.prompt import Prompt
from forge_ai import CodebaseAgent, CodebaseVectorIndex
from forge_core.cloner import WorkspaceManager

from forge_core.cloner import WorkspaceManager
from forge_core.schemas import RepositoryData, FileNode, SymbolNode, ImportNode
from forge_analyzer.parser import SymbolNode, ImportNode
from forge_analyzer.parser import CodeParser
from forge_analyzer.dependencies import DependencyAnalyzer
from forge_analyzer.graph import DependencyGraph
from forge_ai.agent import CodebaseAgent

app = typer.Typer(
    help="Forge CLI: Automated Repository Intelligence & Analysis Engine",
    no_args_is_help=True
)

LANGUAGE_MAP = {
    ".py": "Python",
    ".ts": "TypeScript",
    ".tsx": "TypeScript (TSX)",
    ".js": "JavaScript",
    ".jsx": "JavaScript (JSX)",
    ".rs": "Rust",
}

def _parse_file_content(
    parser: CodeParser, 
    rel_path: str, 
    content: str, 
    ext: str
) -> Tuple[List[SymbolNode], List[ImportNode]]:
    """Helper dispatcher to route file content to the corresponding CodeParser method."""
    ext = ext.lower()
    if ext == ".py":
        return parser.parse_python_file(rel_path, content)
    elif ext in [".ts", ".js"]:
        return parser.parse_typescript_file(rel_path, content, is_tsx=False)
    elif ext in [".tsx", ".jsx"]:
        return parser.parse_typescript_file(rel_path, content, is_tsx=True)
    elif ext == ".rs":
        return parser.parse_rust_file(rel_path, content)
    return [], []

def run_analysis(target: str, export_graph_path: Optional[str] = None):
    """Core scanner execution logic."""
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
                                # Standardize import target string
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

                file_tree.add(f"[green]{rel_path}[/green] ({len(symbols)} symbols, {len(file_imports)} imports extracted)")

        console.print("\n[bold]Repository File Structure & Symbol Summary:[/bold]")
        console.print(file_tree)

        if dep_graph.imports:
            console.print("\n[bold]Internal & External Module Import Graph:[/bold]")
            import_table = Table(show_header=True, header_style="bold cyan")
            import_table.add_column("File")
            import_table.add_column("Imports")

            for file_path, imports in dep_graph.imports.items():
                import_table.add_row(file_path, ", ".join(list(imports)[:3]) + ("..." if len(imports) > 3 else ""))

            console.print(import_table)

        # Export graph JSON if flag is set
        if export_graph_path:
            graph_data = dep_graph.to_json()
            with open(export_graph_path, "w", encoding="utf-8") as f:
                f.write(graph_data)
            console.print(f"\n[bold green]✓ Exported dependency graph to:[/bold green] [yellow]{export_graph_path}[/yellow]")

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

    console.print("\n[bold green]✓ Multi-Language Graph Analysis Complete![/bold green]\n")

@app.command(name="analyze")
def analyze_cmd(
    target: str = typer.Argument(..., help="Path to local folder or GitHub repository URL"),
    export_graph: Optional[str] = typer.Option(
        None, 
        "--export-graph", 
        "-g", 
        help="Path to export JSON dependency graph file (e.g. graph.json)"
    )
):
    """Analyze a local directory or remote Git repository."""
    run_analysis(target, export_graph)

@app.command(name="explain")
def explain_cmd(
    target: str = typer.Argument(..., help="Path to local folder or GitHub repository URL")
):
    """Generates an AI-powered architectural summary of the codebase."""
    console = Console()
    console.print(Panel(f"[bold cyan]Forge AI Engine Analyzing:[/bold cyan] [yellow]{target}[/yellow]"))

    manager = WorkspaceManager(target)
    dep_graph = DependencyGraph()

    try:
        repo_path = manager.setup_workspace()
        parser = CodeParser()
        tree_summary = []

        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", "node_modules", ".venv", "venv", ".idea", ".vscode"}]
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, repo_path)
                ext = os.path.splitext(file)[1].lower()

                if ext in LANGUAGE_MAP:
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            _, file_imports = _parse_file_content(parser, rel_path, content, ext)
                            for imp in file_imports:
                                dep_graph.add_import(rel_path, imp)
                    except Exception:
                        pass

                tree_summary.append(rel_path)

        agent = CodebaseAgent()
        summary = agent.explain_architecture("\n".join(tree_summary), dep_graph.imports)
        
        console.print("\n[bold green]Architectural Analysis:[/bold green]")
        console.print(Panel(summary))

    finally:
        manager.cleanup()

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
        valid_extensions = {".py", ".rs", ".js", ".ts", ".tsx", ".java", ".go", ".c", ".cpp", ".h", ".json", ".md"}

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
        console.print(f"[dim]Indexing {len(file_contents)} files into local ChromaDB vector store...[/dim]")
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

@app.command(name="version")
def version_cmd():
    """Print Forge version."""
    Console().print("[bold cyan]Forge CLI v0.4.0[/bold cyan]")

if __name__ == "__main__":
    app()
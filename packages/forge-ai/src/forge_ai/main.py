import os
import shutil
import tempfile

from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from forge_core.cloner import GitCloner

from forge_core.zip_handler import extract_zip_archive
from forge_core.schemas import FileNode
from forge_analyzer.parser import build_dependency_graph
from forge_analyzer.smells import analyze_code_smells
from forge_analyzer.refactor import perform_ast_dry_run
from forge_ai.agent import CodebaseAgent
from fastapi.responses import PlainTextResponsesss
from forge_analyzer.callgraph import analyze_directory_calls
from forge_refactor.planner import RefactoringPlanner

app = FastAPI(title="Forge API Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize the AI architecture agent once when the API starts.
agent = CodebaseAgent()


@app.post("/api/analyze/zip")
async def analyze_zip_upload(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        raise HTTPException(
            status_code=400,
            detail="Only .zip files are supported."
        )

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".zip"
    ) as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_zip_path = tmp_file.name

    extracted_dir = None

    try:
        extracted_dir = extract_zip_archive(tmp_zip_path)
        files_data = []

        for root, dirs, files in os.walk(extracted_dir):
            dirs[:] = [
                d
                for d in dirs
                if d not in {
                    ".git",
                    "__pycache__",
                    "node_modules",
                    ".venv",
                    "venv"
                }
            ]

            for f in files:
                full_path = os.path.join(root, f)

                rel_path = os.path.relpath(
                    full_path,
                    extracted_dir
                ).replace("\\", "/")

                ext = os.path.splitext(f)[1].lower()

                files_data.append(
                    FileNode(
                        path=rel_path,
                        name=f,
                        extension=ext,
                        size_bytes=os.path.getsize(full_path),
                        language=(
                            "Supported"
                            if ext in [
                                ".py",
                                ".ts",
                                ".tsx",
                                ".js",
                                ".rs",
                                ".java"
                            ]
                            else "Other"
                        ),
                        symbols=[]
                    )
                )

        graph_data = build_dependency_graph(extracted_dir)
        issues_data = analyze_code_smells(graph_data)

        return {
            "status": "success",
            "filename": file.filename,
            "total_files": len(files_data),
            "graph": graph_data,
            "issues": issues_data
        }

    finally:
        if os.path.exists(tmp_zip_path):
            os.remove(tmp_zip_path)

        if extracted_dir and os.path.exists(extracted_dir):
            shutil.rmtree(extracted_dir)


class ReportRequest(BaseModel):
    codebase_context: dict | None = None

@app.post("/api/export/report", response_class=PlainTextResponse)
async def export_architecture_report(req: ReportRequest):
    context = req.codebase_context or {}
    files = context.get("graph", {}).get("nodes", [])
    issues = context.get("issues", [])

    report = f"""# ONGISA Architecture & Code Audit Report
Generated automatically by ONGISA AI Engine.

## Overview
- **Total Tracked Files/Nodes**: {len(files)}
- **Detected Code Smells / Issues**: {len(issues)}

## Detected Issues & Smells
"""
    if issues:
        for idx, issue in enumerate(issues, 1):
            report += f"{idx}. **[{issue.get('severity', 'MEDIUM').upper()}]** {issue.get('description', 'General architectural coupling smell.')}\n"
    else:
        report += "No major architectural smells or circular dependencies detected.\n"

    report += """
## Recommendations
- Ensure modular boundaries are preserved between `forge-core`, `forge-analyzer`, and `forge-ai`.
- Regularly inspect high in-degree nodes via the React Flow topology dashboard.
"""
    return report

@app.post("/api/refactor/ast")
async def refactor_ast_endpoint(payload: dict = Body(...)):
    source_code = payload.get("source_code", "")

    if not source_code.strip():
        return {
            "status": "error",
            "message": "No source code provided for AST refactoring."
        }

    result = perform_ast_dry_run(source_code)

    return result

@app.post("/api/analyze/callgraph")
async def get_call_graph(req: ReportRequest):
    context = req.codebase_context or {}
    # If a root path is available, analyze calls; otherwise return mock/parsed links
    calls = []
    try:
        calls = analyze_directory_calls("./packages")
    except Exception:
        pass
    
    return {
        "status": "success",
        "total_calls": len(calls),
        "calls": calls[:50]  # Return top 50 sampled call references
    }

class RepoCloneRequest(BaseModel):
    repo_url: str

@app.post("/api/analyze/git")
async def analyze_git_repo(req: RepoCloneRequest):
    repo_path = None
    try:
        # Clone the repository using our GitCloner utility
        repo_path = GitCloner.clone_repository(req.repo_url)
        
        # Run call graph & analyzer over the cloned path
        calls = analyze_directory_calls(repo_path)
        
        return {
            "status": "success",
            "message": f"Successfully cloned and analyzed repository from {req.repo_url}",
            "repo_path": repo_path,
            "total_calls": len(calls),
            "calls": calls[:50]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        # Optional: cleanup repo_path directory after extraction if desired, 
        # or keep it cached for the session.
        if repo_path and os.path.exists(repo_path):
            shutil.rmtree(repo_path, ignore_errors=True)

refactor_planner = RefactoringPlanner()

class RefactorRequest(BaseModel):
    file_path: str
    code_content: str
    issue_description: str

@app.post("/api/refactor/plan")
async def create_refactoring_plan(req: RefactorRequest):
    plan = refactor_planner.generate_refactoring_plan(
        req.file_path, 
        req.code_content, 
        req.issue_description
    )
    return {
        "status": "success",
        "file_path": req.file_path,
        "refactoring_plan": plan
    }

    


class ChatQuery(BaseModel):
    question: str
    codebase_context: dict | None = None


@app.post("/api/chat/architecture")
async def architecture_chat_endpoint(query: ChatQuery):
    """
    Send architecture questions to Forge AI / Gemini.
    """

    try:
        answer = agent.query_architecture(
            query.question,
            query.codebase_context or {}
        )

        return {
            "status": "success",
            "question": query.question,
            "answer": answer
        }

    except Exception as e:
        return {
            "status": "error",
            "question": query.question,
            "answer": f"Forge AI error: {str(e)}"
        }
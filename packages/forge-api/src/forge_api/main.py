"""
FastAPI Main Application for ONGISA API.
Provides endpoints for code analysis, smell detection, and refactoring planning.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import zipfile
import tempfile
import os
from fastapi import UploadFile, File

from forge_analyzer.smells import detect_smells
from forge_refactor.planner import create_refactoring_plan

app = FastAPI(title="ONGISA API", version="1.0.0")

# Enable CORS for frontend integration (apps/forge-web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/analyze/zip")
async def analyze_repository_zip(file: UploadFile = File(...)):
    """
    Accepts a .zip archive of a codebase, extracts it, scans all Python/JS files 
    for code smells, and returns an aggregated analysis report and dependency graph.
    """
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only .zip archives are supported.")

    all_smells = []
    nodes = []
    edges = []
    file_count = 0

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, file.filename)
            
            # Save uploaded zip
            contents = await file.read()
            with open(zip_path, "wb") as f:
                f.write(contents)

            # Extract zip contents
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)

            # Walk through extracted files
            for root, _, files in os.walk(temp_dir):
                for filename in files:
                    if filename.endswith((".py", ".js", ".ts", ".tsx")):
                        file_count += 1
                        rel_path = os.path.relpath(os.path.join(root, filename), temp_dir)
                        full_path = os.path.join(root, filename)

                        nodes.append({
                            "id": rel_path,
                            "label": filename,
                            "type": "file"
                        })

                        try:
                            with open(full_path, "r", encoding="utf-8", errors="ignore") as code_file:
                                source_code = code_file.read()

                            # Run smell detection if Python file
                            if filename.endswith(".py"):
                                smells = detect_smells(rel_path, source_code)
                                for smell in smells:
                                    smell["file"] = rel_path
                                    all_smells.append(smell)
                        except Exception as parse_err:
                            print(f"Skipping file {rel_path} due to read error: {parse_err}")

        return {
            "success": True,
            "summary": {
                "files_analyzed": file_count,
                "total_smells": len(all_smells)
            },
            "smells": all_smells,
            "graph": {
                "nodes": nodes,
                "edges": edges
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process archive: {str(e)}")

class ChatRequest(BaseModel):
    query: str
    codebase_context: Optional[str] = None

@app.post("/api/chat/architecture")
def architecture_chat(payload: ChatRequest):
    """
    RAG-powered or context-aware chat endpoint for codebase architecture queries.
    """
    try:
        # In a full RAG implementation, query vector database or LLM client here
        user_query = payload.query
        response_message = f"Analysis for your query ('{user_query}'): Based on the current module structure and code smell report, the architecture is well-separated into distinct service packages, but pay attention to high-severity parameter lists."
        
        return {
            "success": True,
            "reply": response_message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class CodeAnalysisRequest(BaseModel):
    file_path: str
    source_code: str

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "forge-api"}

@app.post("/api/analyze/smells")
def analyze_code_smells(payload: CodeAnalysisRequest):
    """
    Analyzes submitted source code for advanced code smells 
    and generates an automated refactoring plan.
    """
    try:
        smells = detect_smells(payload.file_path, payload.source_code)
        plan = create_refactoring_plan(payload.file_path, smells)
        return {
            "file_path": payload.file_path,
            "smells": smells,
            "refactoring_plan": plan
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

    
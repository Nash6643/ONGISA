"""
FastAPI Main Application for ONGISA API.
Provides endpoints for code analysis, smell detection, and refactoring planning.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
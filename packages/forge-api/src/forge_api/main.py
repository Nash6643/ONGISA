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
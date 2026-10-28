from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from forge_core.repository.url_parser import parse_github_url
from forge_core.repository.cloner import clone_github_repository

router = APIRouter(prefix="/api/github", tags=["GitHub Integration"])

class GitHubIngestRequest(BaseModel):
    repo_url: str

@router.post("/analyze-url")
def analyze_github_url(payload: GitHubIngestRequest):
    try:
        owner, repo = parse_github_url(payload.repo_url)
        clone_path = clone_github_repository(owner, repo)
        return {
            "success": True,
            "owner": owner,
            "repo": repo,
            "message": f"Successfully cloned and queued repository for static analysis.",
            "local_path": clone_path
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
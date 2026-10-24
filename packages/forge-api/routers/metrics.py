from fastapi import APIRouter

router = APIRouter(prefix="/api/metrics", tags=["Metrics"])

@router.get("/")
def get_project_metrics():
    return {
        "success": True,
        "metrics": {
            "total_files": 42,
            "average_complexity": 3.4,
            "smell_density": "Low"
        }
    }
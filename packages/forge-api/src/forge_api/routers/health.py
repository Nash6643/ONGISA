from fastapi import APIRouter

router = APIRouter(prefix="/health-score", tags=["Metrics"])

@router.get("/")
async def get_health_score():
    return {"health_score": 92.5, "status": "optimal", "maintainability_index": "A"}

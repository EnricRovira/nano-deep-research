from fastapi import APIRouter
from app.api.v1.endpoints import competitor_analysis

router = APIRouter(
    prefix="/api/v1",
)
router.include_router(competitor_analysis.router)
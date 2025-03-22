from pydantic import BaseModel
from typing import List, Optional
from app.api.schemas.common import PaginatedResponse, SingleResponse
from app.api.schemas.competitor import Competitor
from app.api.schemas.report import Report


class CompetitorAnalysisResponse(BaseModel):
    """Response model for competitor analysis API endpoint."""
    competitor_analysis: list[Competitor]

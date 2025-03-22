from pydantic import BaseModel, HttpUrl
from typing import Dict, List, Optional
import uuid
from app.api.schemas.competitor import CompetitorBase, SocialMedia
from app.api.schemas.report import ReportBase



class CompetitorAnalysisRequest(BaseModel):
    """Request model for generating competitor analysis."""
    company_name: str
    website: str
    mission: str

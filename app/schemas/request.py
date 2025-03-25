from pydantic import BaseModel, Field

class CompetitorAnalysisRequest(BaseModel):
    website: str = Field(..., description="The website URL to analyze.")
    description: str = Field(..., description="A short description of the company to analyze.")
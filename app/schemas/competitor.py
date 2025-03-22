from pydantic import BaseModel, Field, HttpUrl
from typing import Dict, List, Optional, Union
from datetime import datetime
import uuid
from enum import Enum


class SocialMedia(BaseModel):
    linkedin: Optional[HttpUrl] = None
    twitter: Optional[HttpUrl] = None
    facebook: Optional[HttpUrl] = None


class PricingModel(str, Enum):
    SAAS = "SaaS"
    ONE_TIME = "one-time purchase"
    FREEMIUM = "freemium"
    ENTERPRISE = "enterprise-only"


class CompanySector(str, Enum):
    TECHNOLOGY = "Technology"
    FINANCE = "Finance"
    HEALTHCARE = "Healthcare"
    RETAIL = "Retail"
    EDUCATION = "Education"


class CompanySize(str, Enum):
    STARTUP = "Startup"
    SMALL = "Small Business"
    MEDIUM = "Medium Enterprise"
    LARGE = "Large Corporation"


class Language(str, Enum):
    ENGLISH = "English"
    SPANISH = "Spanish"
    FRENCH = "French"
    GERMAN = "German"
    CHINESE = "Chinese"


class PricingPlan(BaseModel):
    name: str
    price: float
    features: List[str]


class Pricing(BaseModel):
    model: PricingModel
    plans: Optional[List[PricingPlan]] = None
    discounts: Optional[List[str]] = None


class Product(BaseModel):
    features: Optional[List[str]] = None
    use_cases: Optional[List[str]] = None
    pricing: Optional[Pricing] = None


class TargetAudience(BaseModel):
    sectors: Optional[List[CompanySector]] = None
    company_size: Optional[List[CompanySize]] = None
    decision_maker: Optional[List[str]] = None


class MarketPresence(BaseModel):
    countries: Optional[List[str]] = None
    languages: Optional[List[Language]] = None


class Market(BaseModel):
    target_audience: Optional[TargetAudience] = None
    market_presence: Optional[MarketPresence] = None
    business_segments: Optional[List[str]] = None


class SwotAnalysis(BaseModel):
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None
    opportunities: Optional[List[str]] = None
    threats: Optional[List[str]] = None


class CompetitorBase(BaseModel):
    name: str
    website: str
    description: Optional[str] = None
    score_affinity: Optional[float] = Field(None, ge=0, le=10)
    product: Optional[Product] = None
    market: Optional[Market] = None
    swot_analysis: Optional[SwotAnalysis] = None


class CompetitorCreate(CompetitorBase):
    pass


class CompetitorUpdate(CompetitorBase):
    name: Optional[str] = None
    website: Optional[str] = None


class CompetitorInDB(CompetitorBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    class Config:
        orm_mode = True


class Competitor(CompetitorInDB):
    pass 
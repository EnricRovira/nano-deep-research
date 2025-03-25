from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid


class Insight(BaseModel):
    topic: str
    content: str


class ReportBase(BaseModel):
    title: str
    description: Optional[str] = None
    competitors: List[uuid.UUID]


class ReportCreate(ReportBase):
    pass


class ReportUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    competitors: Optional[List[uuid.UUID]] = None


class ReportInDB(ReportBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    insights: Optional[List[Insight]] = None

    class Config:
        from_attributes = True


class Report(ReportInDB):
    pass
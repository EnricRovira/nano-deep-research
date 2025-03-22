from pydantic import BaseModel
from typing import Generic, List, Optional, TypeVar

T = TypeVar('T')


class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 10


class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    total: int
    page: int
    page_size: int
    message: Optional[str] = None


class SingleResponse(BaseModel, Generic[T]):
    data: T
    message: Optional[str] = None 
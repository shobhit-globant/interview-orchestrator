from pydantic import BaseModel
from typing import Any, List, Optional, Generic, TypeVar
from datetime import datetime

T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    data: Optional[T] = None
    message: str
    success: bool = True
    timestamp: datetime = datetime.utcnow()
    errors: List[dict] = []
    code: str = "SUCCESS"

class PaginationMeta(BaseModel):
    page_index: int
    page_size: int
    total_count: int
    total_pages: int
    has_previous: bool
    has_next: bool

class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    pagination: PaginationMeta
    message: str = "Data retrieved successfully"
    success: bool = True
    timestamp: datetime = datetime.utcnow()
    errors: List[dict] = []
    code: str = "SUCCESS"

class ErrorDetail(BaseModel):
    field: Optional[str] = None
    message: str
    code: str

class BaseEntity(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    
    class Config:
        from_attributes = True

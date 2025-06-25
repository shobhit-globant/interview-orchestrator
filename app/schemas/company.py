from pydantic import BaseModel, validator
from typing import Optional, List
from .common import BaseEntity
from .user import User

class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    headquarters: Optional[str] = None
    founded_year: Optional[int] = None

class CompanyCreate(CompanyBase):
    slug: str
    
    @validator('slug')
    def validate_slug(cls, v):
        if not v.replace('-', '').replace('_', '').isalnum():
            raise ValueError('Slug must contain only alphanumeric characters, hyphens, and underscores')
        return v.lower()

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    headquarters: Optional[str] = None
    founded_year: Optional[int] = None
    logo_url: Optional[str] = None

class CompanyInDB(CompanyBase, BaseEntity):
    uuid: str
    slug: str
    logo_url: Optional[str] = None
    allow_public_applications: bool
    require_approval_for_jobs: bool

class Company(CompanyInDB):
    pass

class CompanyUserRole(BaseModel):
    role: str
    joined_at: Optional[datetime] = None
    invitation_accepted: bool = False

class CompanyWithUsers(Company):
    users: List[User] = []
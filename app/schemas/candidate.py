from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from .common import BaseEntity

class SkillBase(BaseModel):
    name: str
    description: Optional[str] = None

class SkillCreate(SkillBase):
    category_id: int
    aliases: Optional[List[str]] = None

class Skill(SkillBase, BaseEntity):
    category_id: int
    aliases: Optional[List[str]] = None

class SkillCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class SkillCategoryCreate(SkillCategoryBase):
    parent_id: Optional[int] = None

class SkillCategory(SkillCategoryBase, BaseEntity):
    parent_id: Optional[int] = None

class CandidateSkillBase(BaseModel):
    skill_id: int
    proficiency_level: str
    years_of_experience: Optional[float] = None
    is_primary: bool = False
    
    @validator('proficiency_level')
    def validate_proficiency(cls, v):
        allowed_levels = ['beginner', 'intermediate', 'advanced', 'expert']
        if v.lower() not in allowed_levels:
            raise ValueError(f'Proficiency level must be one of: {", ".join(allowed_levels)}')
        return v.lower()

class CandidateSkillCreate(CandidateSkillBase):
    pass

class CandidateSkill(CandidateSkillBase, BaseEntity):
    candidate_id: int
    last_used: Optional[datetime] = None
    source: Optional[str] = None
    confidence_score: Optional[float] = None
    skill: Skill

class CandidateBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    current_title: Optional[str] = None
    current_company: Optional[str] = None
    years_of_experience: Optional[float] = None
    expected_salary_min: Optional[int] = None
    expected_salary_max: Optional[int] = None
    preferred_locations: Optional[List[str]] = None
    remote_work_preference: Optional[str] = "any"
    summary: Optional[str] = None

class CandidateCreate(CandidateBase):
    skills: Optional[List[CandidateSkillCreate]] = []
    
    @validator('remote_work_preference')
    def validate_work_preference(cls, v):
        allowed_prefs = ['remote', 'hybrid', 'onsite', 'any']
        if v and v.lower() not in allowed_prefs:
            raise ValueError(f'Remote work preference must be one of: {", ".join(allowed_prefs)}')
        return v.lower() if v else 'any'

class CandidateUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    current_title: Optional[str] = None
    current_company: Optional[str] = None
    years_of_experience: Optional[float] = None
    expected_salary_min: Optional[int] = None
    expected_salary_max: Optional[int] = None
    preferred_locations: Optional[List[str]] = None
    remote_work_preference: Optional[str] = None
    summary: Optional[str] = None
    availability_status: Optional[str] = None

class CandidateInDB(CandidateBase, BaseEntity):
    uuid: str
    resume_url: Optional[str] = None
    resume_text: Optional[str] = None
    profile_completion_score: float
    availability_status: str
    preferred_contact_method: str
    consent_to_contact: bool
    data_retention_consent: bool

class Candidate(CandidateInDB):
    skills: List[CandidateSkill] = []

class CandidateSearch(BaseModel):
    query: Optional[str] = None
    skills: Optional[List[str]] = None
    min_experience: Optional[float] = None
    max_experience: Optional[float] = None
    locations: Optional[List[str]] = None
    remote_work_preference: Optional[str] = None
    availability_status: Optional[str] = None
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None

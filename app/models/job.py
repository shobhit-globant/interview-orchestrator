from sqlalchemy import Column, String, Text, Integer, ForeignKey, Float, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
from .base import BaseModel

class Job(BaseModel):
    __tablename__ = "jobs"
    
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    
    # Job Details
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    department = Column(String(100), nullable=True)
    employment_type = Column(String(50), nullable=False)  # full-time, part-time, contract, internship
    experience_level = Column(String(50), nullable=False)  # entry, mid, senior, executive
    
    # Location and Remote Work
    location = Column(String(255), nullable=True)
    is_remote = Column(Boolean, default=False)
    remote_work_type = Column(String(20), nullable=True)  # remote, hybrid, onsite
    
    # Compensation
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    salary_currency = Column(String(3), default="USD")
    
    # Requirements
    required_skills = Column(ARRAY(String), nullable=True)
    preferred_skills = Column(ARRAY(String), nullable=True)
    min_years_experience = Column(Float, nullable=True)
    max_years_experience = Column(Float, nullable=True)
    education_requirements = Column(Text, nullable=True)
    
    # Job Status
    status = Column(String(20), default="draft")  # draft, active, paused, closed
    posted_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    
    # AI/ML Features
    job_embedding = Column(Text, nullable=True)  # Store as JSON string
    
    # Relationships
    company = relationship("Company", back_populates="jobs")
    applications = relationship("JobApplication", back_populates="job")

class JobApplication(BaseModel):
    __tablename__ = "job_applications"
    
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    
    # Application Status
    status = Column(String(50), default="applied")  # applied, screening, interviewing, offered, hired, rejected
    applied_at = Column(DateTime, nullable=False)
    
    # Application Details
    cover_letter = Column(Text, nullable=True)
    resume_url = Column(String(500), nullable=True)
    additional_notes = Column(Text, nullable=True)
    
    # Scoring and Matching
    ai_match_score = Column(Float, nullable=True)
    recruiter_rating = Column(Integer, nullable=True)  # 1-5 scale
    
    # Relationships
    job = relationship("Job", back_populates="applications")
    candidate = relationship("Candidate", back_populates="applications")

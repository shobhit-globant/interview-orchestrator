from sqlalchemy import Column, String, Text, Integer, ForeignKey, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
from .base import BaseModel

class SkillCategory(BaseModel):
    __tablename__ = "skill_categories"
    
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey("skill_categories.id"), nullable=True)
    
    # Relationships
    skills = relationship("Skill", back_populates="category")
    parent = relationship("SkillCategory", remote_side="SkillCategory.id")

class Skill(BaseModel):
    __tablename__ = "skills"
    
    name = Column(String(100), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey("skill_categories.id"), nullable=False)
    description = Column(Text, nullable=True)
    aliases = Column(ARRAY(String), nullable=True)  # Alternative names for the skill
    
    # Relationships
    category = relationship("SkillCategory", back_populates="skills")
    candidate_skills = relationship("CandidateSkill", back_populates="skill")

class Candidate(BaseModel):
    __tablename__ = "candidates"
    
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    
    # Personal Information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), nullable=True)
    linkedin_url = Column(String(500), nullable=True)
    github_url = Column(String(500), nullable=True)
    portfolio_url = Column(String(500), nullable=True)
    
    # Professional Information
    current_title = Column(String(200), nullable=True)
    current_company = Column(String(200), nullable=True)
    years_of_experience = Column(Float, nullable=True)
    expected_salary_min = Column(Integer, nullable=True)
    expected_salary_max = Column(Integer, nullable=True)
    preferred_locations = Column(ARRAY(String), nullable=True)
    remote_work_preference = Column(String(20), nullable=True)  # remote, hybrid, onsite, any
    
    # Resume and Profile
    resume_url = Column(String(500), nullable=True)
    resume_text = Column(Text, nullable=True)  # Extracted text from resume
    summary = Column(Text, nullable=True)
    
    # Status and Scoring
    profile_completion_score = Column(Float, default=0.0)
    availability_status = Column(String(50), default="available")  # available, interviewing, hired, not_looking
    preferred_contact_method = Column(String(20), default="email")
    
    # Consent and Privacy
    consent_to_contact = Column(Boolean, default=True)
    data_retention_consent = Column(Boolean, default=True)
    
    # AI/ML Features
    embedding_vector = Column(Text, nullable=True)  # Store as JSON string
    last_embedding_update = Column(DateTime, nullable=True)
    
    # Relationships
    skills = relationship("CandidateSkill", back_populates="candidate")
    applications = relationship("JobApplication", back_populates="candidate")

class CandidateSkill(BaseModel):
    __tablename__ = "candidate_skills"
    
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    proficiency_level = Column(String(20), nullable=False)  # beginner, intermediate, advanced, expert
    years_of_experience = Column(Float, nullable=True)
    last_used = Column(DateTime, nullable=True)
    is_primary = Column(Boolean, default=False)  # Mark as primary/core skill
    source = Column(String(50), nullable=True)  # resume, manual, linkedin, etc.
    confidence_score = Column(Float, nullable=True)  # AI confidence in skill extraction
    
    # Relationships
    candidate = relationship("Candidate", back_populates="skills")
    skill = relationship("Skill", back_populates="candidate_skills")
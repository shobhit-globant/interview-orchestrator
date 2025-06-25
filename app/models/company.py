from sqlalchemy import Column, String, Text, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import BaseModel

class Company(BaseModel):
    __tablename__ = "companies"
    
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    website = Column(String(255), nullable=True)
    logo_url = Column(String(500), nullable=True)
    industry = Column(String(100), nullable=True)
    company_size = Column(String(50), nullable=True)  # startup, small, medium, large, enterprise
    headquarters = Column(String(255), nullable=True)
    founded_year = Column(Integer, nullable=True)
    
    # Settings
    allow_public_applications = Column(Boolean, default=True)
    require_approval_for_jobs = Column(Boolean, default=False)
    
    # Relationships
    users = relationship("CompanyUser", back_populates="company")
    jobs = relationship("Job", back_populates="company")

class CompanyUser(BaseModel):
    __tablename__ = "company_users"
    
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(50), nullable=False)  # admin, hr_manager, interviewer, viewer
    invited_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    joined_at = Column(DateTime, nullable=True)
    invitation_accepted = Column(Boolean, default=False)
    
    # Relationships
    company = relationship("Company", back_populates="users")
    user = relationship("User", back_populates="company_memberships")
    inviter = relationship("User", foreign_keys=[invited_by])

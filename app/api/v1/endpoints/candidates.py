from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.candidate import Candidate, CandidateSkill, Skill
from app.schemas.candidate import (
    Candidate as CandidateSchema,
    CandidateCreate,
    CandidateUpdate,
    CandidateSearch
)
from app.schemas.common import BaseResponse, PaginatedResponse, PaginationMeta

router = APIRouter()

@router.post("/", response_model=BaseResponse[CandidateSchema])
async def create_candidate(
    candidate_data: CandidateCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check if candidate email already exists
    existing_candidate = db.query(Candidate).filter(
        Candidate.email == candidate_data.email
    ).first()
    if existing_candidate:
        raise HTTPException(status_code=400, detail="Candidate email already exists")
    
    # Create candidate
    candidate_dict = candidate_data.dict(exclude={'skills'})
    db_candidate = Candidate(**candidate_dict)
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    
    # Add skills if provided
    if candidate_data.skills:
        for skill_data in candidate_data.skills:
            candidate_skill = CandidateSkill(
                candidate_id=db_candidate.id,
                **skill_data.dict()
            )
            db.add(candidate_skill)
        db.commit()
    
    # Calculate profile completion score
    db_candidate.profile_completion_score = calculate_profile_completion(db_candidate)
    db.commit()
    
    return BaseResponse(
        data=CandidateSchema.from_orm(db_candidate),
        message="Candidate created successfully",
        code="CANDIDATE_CREATED"
    )

@router.get("/", response_model=PaginatedResponse[CandidateSchema])
async def get_candidates(
    page: int = 1,
    size: int = 20,
    search: Optional[str] = Query(None, description="Search in name, email, or skills"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * size
    query = db.query(Candidate)
    
    if search:
        search_filter = or_(
            Candidate.first_name.ilike(f"%{search}%"),
            Candidate.last_name.ilike(f"%{search}%"),
            Candidate.email.ilike(f"%{search}%"),
            Candidate.current_title.ilike(f"%{search}%"),
            Candidate.current_company.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    candidates = query.offset(offset).limit(size).all()
    total_count = query.count()
    total_pages = (total_count + size - 1) // size
    
    pagination = PaginationMeta(
        page_index=page,
        page_size=size,
        total_count=total_count,
        total_pages=total_pages,
        has_previous=page > 1,
        has_next=page < total_pages
    )
    
    return PaginatedResponse(
        data=[CandidateSchema.from_orm(candidate) for candidate in candidates],
        pagination=pagination,
        message="Candidates retrieved successfully",
        code="CANDIDATES_RETRIEVED"
    )

@router.get("/{candidate_id}", response_model=BaseResponse[CandidateSchema])
async def get_candidate(
    candidate_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    return BaseResponse(
        data=CandidateSchema.from_orm(candidate),
        message="Candidate retrieved successfully",
        code="CANDIDATE_RETRIEVED"
    )

@router.put("/{candidate_id}", response_model=BaseResponse[CandidateSchema])
async def update_candidate(
    candidate_id: int,
    candidate_update: CandidateUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    update_data = candidate_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(candidate, field, value)
    
    # Recalculate profile completion score
    candidate.profile_completion_score = calculate_profile_completion(candidate)
    
    db.commit()
    db.refresh(candidate)
    
    return BaseResponse(
        data=CandidateSchema.from_orm(candidate),
        message="Candidate updated successfully",
        code="CANDIDATE_UPDATED"
    )

def calculate_profile_completion(candidate: Candidate) -> float:
    """Calculate profile completion score based on filled fields"""
    total_fields = 15
    completed_fields = 0
    
    # Check required fields
    if candidate.first_name: completed_fields += 1
    if candidate.last_name: completed_fields += 1
    if candidate.email: completed_fields += 1
    if candidate.phone_number: completed_fields += 1
    if candidate.current_title: completed_fields += 1
    if candidate.current_company: completed_fields += 1
    if candidate.years_of_experience: completed_fields += 1
    if candidate.summary: completed_fields += 1
    if candidate.linkedin_url: completed_fields += 1
    if candidate.github_url: completed_fields += 1
    if candidate.portfolio_url: completed_fields += 1
    if candidate.expected_salary_min: completed_fields += 1
    if candidate.expected_salary_max: completed_fields += 1
    if candidate.preferred_locations: completed_fields += 1
    if candidate.remote_work_preference: completed_fields += 1
    
    return round((completed_fields / total_fields) * 100, 2)
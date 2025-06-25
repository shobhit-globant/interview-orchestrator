from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.company import Company, CompanyUser
from app.schemas.company import (
    Company as CompanySchema, 
    CompanyCreate, 
    CompanyUpdate,
    CompanyWithUsers
)
from app.schemas.common import BaseResponse, PaginatedResponse, PaginationMeta

router = APIRouter()

@router.post("/", response_model=BaseResponse[CompanySchema])
async def create_company(
    company_data: CompanyCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check if company slug already exists
    existing_company = db.query(Company).filter(Company.slug == company_data.slug).first()
    if existing_company:
        raise HTTPException(status_code=400, detail="Company slug already exists")
    
    # Create company
    db_company = Company(**company_data.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    
    # Add current user as admin
    company_user = CompanyUser(
        company_id=db_company.id,
        user_id=current_user.id,
        role="admin",
        invitation_accepted=True
    )
    db.add(company_user)
    db.commit()
    
    return BaseResponse(
        data=CompanySchema.from_orm(db_company),
        message="Company created successfully",
        code="COMPANY_CREATED"
    )

@router.get("/", response_model=PaginatedResponse[CompanySchema])
async def get_companies(
    page: int = 1,
    size: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * size
    
    # Get companies where user is a member
    user_companies = db.query(Company).join(CompanyUser).filter(
        CompanyUser.user_id == current_user.id
    ).offset(offset).limit(size).all()
    
    total_count = db.query(Company).join(CompanyUser).filter(
        CompanyUser.user_id == current_user.id
    ).count()
    
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
        data=[CompanySchema.from_orm(company) for company in user_companies],
        pagination=pagination,
        message="Companies retrieved successfully",
        code="COMPANIES_RETRIEVED"
    )

@router.get("/{company_id}", response_model=BaseResponse[CompanySchema])
async def get_company(
    company_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Check if user has access to this company
    user_company = db.query(CompanyUser).filter(
        CompanyUser.company_id == company_id,
        CompanyUser.user_id == current_user.id
    ).first()
    
    if not user_company and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return BaseResponse(
        data=CompanySchema.from_orm(company),
        message="Company retrieved successfully",
        code="COMPANY_RETRIEVED"
    )

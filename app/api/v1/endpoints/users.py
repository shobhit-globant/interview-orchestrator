from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.user import User as UserSchema, UserUpdate
from app.schemas.common import BaseResponse, PaginatedResponse

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[UserSchema])
async def get_users(
    page: int = 1,
    size: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check if user has permission to view users
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    offset = (page - 1) * size
    users = db.query(User).offset(offset).limit(size).all()
    total_count = db.query(User).count()
    total_pages = (total_count + size - 1) // size
    
    from app.schemas.common import PaginationMeta
    pagination = PaginationMeta(
        page_index=page,
        page_size=size,
        total_count=total_count,
        total_pages=total_pages,
        has_previous=page > 1,
        has_next=page < total_pages
    )
    
    return PaginatedResponse(
        data=[UserSchema.from_orm(user) for user in users],
        pagination=pagination,
        message="Users retrieved successfully",
        code="USERS_RETRIEVED"
    )

@router.put("/me", response_model=BaseResponse[UserSchema])
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    update_data = user_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return BaseResponse(
        data=UserSchema.from_orm(current_user),
        message="User profile updated successfully",
        code="PROFILE_UPDATED"
    )

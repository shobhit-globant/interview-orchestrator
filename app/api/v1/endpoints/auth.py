from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.database import get_db
from app.core.security import (
    verify_password, 
    get_password_hash, 
    create_access_token,
    get_current_active_user
)
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema, Token, UserLogin
from app.schemas.common import BaseResponse

router = APIRouter()

@router.post("/register", response_model=BaseResponse[UserSchema])
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        username=user_data.username,
        phone_number=user_data.phone_number,
        timezone=user_data.timezone,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return BaseResponse(
        data=UserSchema.from_orm(db_user),
        message="User registered successfully",
        code="USER_REGISTERED"
    )

@router.post("/login", response_model=BaseResponse[Token])
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is disabled"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    
    token_data = Token(
        access_token=access_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserSchema.from_orm(user)
    )
    
    return BaseResponse(
        data=token_data,
        message="Login successful",
        code="LOGIN_SUCCESS"
    )

@router.get("/me", response_model=BaseResponse[UserSchema])
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    return BaseResponse(
        data=UserSchema.from_orm(current_user),
        message="User profile retrieved successfully",
        code="PROFILE_RETRIEVED"
    )

@router.post("/logout", response_model=BaseResponse[dict])
async def logout(current_user: User = Depends(get_current_active_user)):
    # In a production environment, you would invalidate the token here
    # For now, we'll just return a success message
    return BaseResponse(
        data={"message": "Logged out successfully"},
        message="Logout successful",
        code="LOGOUT_SUCCESS"
    )

from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from .common import BaseEntity

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    username: Optional[str] = None
    phone_number: Optional[str] = None
    timezone: str = "UTC"

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    timezone: Optional[str] = None
    profile_picture_url: Optional[str] = None

class UserInDB(UserBase, BaseEntity):
    uuid: str
    is_verified: bool
    is_superuser: bool
    profile_picture_url: Optional[str] = None

class User(UserInDB):
    pass

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: User

class TokenPayload(BaseModel):
    sub: Optional[str] = None

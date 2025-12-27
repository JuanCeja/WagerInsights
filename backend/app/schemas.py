from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# Base schema with common fields
class UserBase(BaseModel):
    email: EmailStr
    username: str

# Schema for creating a new user (registration)
class UserCreate(UserBase):
    password: str = Field(..., min_length = 8)

# Schema for user response (what API returns)
class UserResponse(UserBase):
    id: int
    balance: float
    created_at: datetime

    class Config:
        from_attributes = True

#Schema for user login
class UserLogin(BaseModel):
    username_or_email: str
    password: str

# Schema for JWT token response
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for token data
class TokenData(BaseModel):
    user_id: Optional[int] = None
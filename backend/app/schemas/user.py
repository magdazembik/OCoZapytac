"""
User schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a user"""
    pass


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    subscribed_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

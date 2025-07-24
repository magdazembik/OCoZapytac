"""
Contact message schemas
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class ContactMessageBase(BaseModel):
    """Base contact message schema"""
    name: str
    email: EmailStr
    subject: Optional[str] = None
    message: str


class ContactMessageCreate(ContactMessageBase):
    """Schema for creating a contact message"""
    pass


class ContactMessageResponse(ContactMessageBase):
    """Schema for contact message response"""
    id: int
    created_at: datetime
    is_read: bool
    
    class Config:
        from_attributes = True

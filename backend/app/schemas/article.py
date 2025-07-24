"""
Article schemas for request/response validation
"""

from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional
import re


class ArticleBase(BaseModel):
    """Base article schema"""
    title: str
    excerpt: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    category: Optional[str] = None
    author: Optional[str] = None
    read_time: Optional[str] = None


class ArticleCreate(ArticleBase):
    """Schema for creating an article"""
    slug: str
    is_published: bool = False
    
    @validator('slug')
    def validate_slug(cls, v):
        if not re.match(r'^[a-z0-9-]+$', v):
            raise ValueError('Slug must contain only lowercase letters, numbers, and hyphens')
        return v


class ArticleUpdate(ArticleBase):
    """Schema for updating an article"""
    title: Optional[str] = None
    is_published: Optional[bool] = None


class ArticleResponse(ArticleBase):
    """Schema for article response"""
    id: int
    slug: str
    published_at: Optional[datetime]
    is_published: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

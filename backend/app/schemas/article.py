"""
Article schemas for API requests and responses
Updated to support HTML file uploads
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ArticleBase(BaseModel):
    """Base article schema"""
    title: str = Field(..., max_length=500, description="Article title")
    slug: str = Field(..., max_length=500, description="URL-friendly slug")
    excerpt: Optional[str] = Field(None, description="Short article description")
    content: Optional[str] = Field(None, description="Article content in HTML format")
    content_file_path: Optional[str] = Field(None, description="Path to uploaded HTML file (alternative to content)")
    image_url: Optional[str] = Field(None, max_length=500, description="Article image URL")
    video_url: Optional[str] = Field(None, max_length=500, description="YouTube video URL")
    category: Optional[str] = Field(None, max_length=100, description="Article category")
    author: Optional[str] = Field(None, max_length=255, description="Article author")
    read_time: Optional[str] = Field(None, max_length=50, description="Estimated reading time")


class ArticleCreate(ArticleBase):
    """Schema for creating articles"""
    is_published: bool = Field(False, description="Whether the article is published")
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Przewodnik po podatkach dla mikroprzedsiębiorców",
                "slug": "przewodnik-podatki-mikroprzedsiebiorcy",
                "excerpt": "Kompletny przewodnik po najważniejszych aspektach podatkowych dla małych firm.",
                "content": "Leave empty if using content_file_path",
                "content_file_path": "uploaded_html_content/20241231_123456_abc123_my-article.html",
                "image_url": "https://example.com/image.jpg",
                "video_url": "https://www.youtube.com/watch?v=example123",
                "category": "Podatki",
                "author": "Jan Kowalski",
                "read_time": "8 min",
                "is_published": True
            }
        }


class ArticleUpdate(BaseModel):
    """Schema for updating articles"""
    title: Optional[str] = Field(None, max_length=500)
    slug: Optional[str] = Field(None, max_length=500)
    excerpt: Optional[str] = None
    content: Optional[str] = None
    content_file_path: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)
    video_url: Optional[str] = Field(None, max_length=500)
    category: Optional[str] = Field(None, max_length=100)
    author: Optional[str] = Field(None, max_length=255)
    read_time: Optional[str] = Field(None, max_length=50)
    is_published: Optional[bool] = None


class ArticleResponse(ArticleBase):
    """Schema for article responses"""
    id: int
    is_published: bool
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    # Add computed field for content
    def get_content(self) -> str:
        """Get the actual content, either from content field or file"""
        if self.content_file_path:
            try:
                with open(self.content_file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except FileNotFoundError:
                return self.content or "Content file not found"
        return self.content or ""

    class Config:
        from_attributes = True


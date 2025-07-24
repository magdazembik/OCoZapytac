"""
Article model for blog posts
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class Article(Base):
    """Article model for blog posts"""
    
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    slug = Column(String(500), unique=True, nullable=False, index=True)
    excerpt = Column(Text)
    content = Column(Text)
    image_url = Column(String(500))
    video_url = Column(String(500))
    category = Column(String(100), index=True)
    author = Column(String(255))
    read_time = Column(String(50))
    published_at = Column(DateTime(timezone=True))
    is_published = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )
    
    def __repr__(self) -> str:
        return f"<Article(id={self.id}, title='{self.title}')>"

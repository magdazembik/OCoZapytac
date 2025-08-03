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
    content = Column(Text)  # This will now store either HTML content directly OR a file path
    content_file_path = Column(String(500))  # NEW: Path to uploaded HTML file
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
    
    def get_content(self):
        """
        Get the article content, either from the content field or from the file path
        """
        if self.content_file_path:
            try:
                with open(self.content_file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except FileNotFoundError:
                return self.content or "Content file not found"
        return self.content or ""
    
    def __repr__(self) -> str:
        return f"<Article(id={self.id}, title='{self.title}')>"


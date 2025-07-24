"""
Article endpoints - This file handles all article-related API operations
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.article import Article
from app.models.user import User
from app.schemas.article import ArticleCreate, ArticleUpdate, ArticleResponse
from app.services.email_service import EmailService

router = APIRouter()
email_service = EmailService()


@router.get("/", response_model=List[ArticleResponse])
async def get_articles(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get published articles with pagination and filtering"""
    query = db.query(Article).filter(Article.is_published == True)
    
    if category:
        query = query.filter(Article.category == category)
    
    articles = query.order_by(Article.published_at.desc()).offset(skip).limit(limit).all()
    return articles


@router.get("/featured", response_model=List[ArticleResponse])
async def get_featured_articles(db: Session = Depends(get_db)):
    """Get 3 most recent published articles for homepage"""
    articles = db.query(Article).filter(Article.is_published == True)\
                 .order_by(Article.published_at.desc()).limit(3).all()
    return articles


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article_by_id(article_id: int, db: Session = Depends(get_db)):
    """Get single article by ID"""
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.is_published == True
    ).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Artykuł nie został znaleziony")
    
    return article


@router.get("/slug/{slug}", response_model=ArticleResponse)
async def get_article_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get single article by slug"""
    article = db.query(Article).filter(
        Article.slug == slug,
        Article.is_published == True
    ).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Artykuł nie został znaleziony")
    
    return article


@router.post("/", response_model=ArticleResponse)
async def create_article(
    article: ArticleCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Create new article - THIS IS THE ENDPOINT YOU'LL USE TO CREATE ARTICLES
    
    Example usage:
    POST /api/v1/articles/
    {
        "title": "Mój pierwszy artykuł",
        "slug": "moj-pierwszy-artykul",
        "excerpt": "Krótki opis artykułu...",
        "content": "<p>Pełna treść artykułu w HTML...</p>",
        "category": "Podatki",
        "author": "Jan Kowalski",
        "read_time": "5 min",
        "is_published": true
    }
    """
    # Check if slug already exists
    existing_article = db.query(Article).filter(Article.slug == article.slug).first()
    if existing_article:
        raise HTTPException(status_code=400, detail="Artykuł z tym slug już istnieje")
    
    # Create article
    article_data = article.dict()
    if article.is_published:
        article_data["published_at"] = datetime.utcnow()
    
    db_article = Article(**article_data)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    
    # Send notification to subscribers if published
    if article.is_published:
        subscribers = db.query(User.email).filter(User.is_active == True).all()
        subscriber_emails = [sub.email for sub in subscribers]
        background_tasks.add_task(
            email_service.send_new_article_notification,
            subscriber_emails,
            db_article
        )
    
    return db_article


@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: int,
    article_update: ArticleUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Update existing article"""
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Artykuł nie został znaleziony")
    
    # Track if article is being published for the first time
    was_published = db_article.is_published
    
    # Update article
    update_data = article_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_article, field, value)
    
    # Set published_at if article is being published
    if not was_published and article_update.is_published:
        db_article.published_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_article)
    
    # Send notification if article was just published
    if not was_published and article_update.is_published:
        subscribers = db.query(User.email).filter(User.is_active == True).all()
        subscriber_emails = [sub.email for sub in subscribers]
        background_tasks.add_task(
            email_service.send_new_article_notification,
            subscriber_emails,
            db_article
        )
    
    return db_article


@router.delete("/{article_id}")
async def delete_article(article_id: int, db: Session = Depends(get_db)):
    """Delete article (admin only)"""
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Artykuł nie został znaleziony")
    
    db.delete(db_article)
    db.commit()
    
    return {"message": "Artykuł został usunięty"}

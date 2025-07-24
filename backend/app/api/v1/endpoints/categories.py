"""
Categories endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict

from app.core.database import get_db
from app.models.article import Article

router = APIRouter()


@router.get("/", response_model=List[Dict[str, str]])
async def get_categories(db: Session = Depends(get_db)):
    """Get all article categories"""
    categories = db.query(Article.category).filter(
        Article.is_published == True,
        Article.category.isnot(None)
    ).distinct().all()
    
    return [{"name": cat.category} for cat in categories if cat.category]


@router.get("/stats")
async def get_category_stats(db: Session = Depends(get_db)):
    """Get article count per category"""
    from sqlalchemy import func
    
    stats = db.query(
        Article.category,
        func.count(Article.id).label('count')
    ).filter(
        Article.is_published == True,
        Article.category.isnot(None)
    ).group_by(Article.category).all()
    
    return [{"category": stat.category, "count": stat.count} for stat in stats]

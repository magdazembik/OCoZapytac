"""
Main API router that includes all endpoint routers
"""

from fastapi import APIRouter

from app.api.v1.endpoints import articles, users, contact, categories

api_router = APIRouter()

api_router.include_router(articles.router, prefix="/articles", tags=["articles"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(contact.router, prefix="/contact", tags=["contact"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])

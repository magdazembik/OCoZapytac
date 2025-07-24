"""
User/Newsletter endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.email_service import EmailService

router = APIRouter()
email_service = EmailService()


@router.post("/subscribe", response_model=UserResponse)
async def subscribe_newsletter(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Subscribe user to newsletter"""
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        if db_user.is_active:
            raise HTTPException(status_code=400, detail="Email już jest zapisany do newslettera")
        else:
            # Reactivate subscription
            db_user.is_active = True
            db.commit()
            db.refresh(db_user)
            return db_user
    
    # Create new user
    db_user = User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Send welcome email in background
    background_tasks.add_task(email_service.send_welcome_email, user.email)
    
    return db_user


@router.post("/unsubscribe")
async def unsubscribe_newsletter(email: str, db: Session = Depends(get_db)):
    """Unsubscribe user from newsletter"""
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Email nie został znaleziony")
    
    db_user.is_active = False
    db.commit()
    
    return {"message": "Pomyślnie wypisano z newslettera"}


@router.get("/subscribers", response_model=List[UserResponse])
async def get_subscribers(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get newsletter subscribers (admin only)"""
    query = db.query(User)
    
    if active_only:
        query = query.filter(User.is_active == True)
    
    subscribers = query.offset(skip).limit(limit).all()
    return subscribers

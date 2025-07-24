"""
Contact form endpoints
"""

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.contact import ContactMessage
from app.schemas.contact import ContactMessageCreate, ContactMessageResponse
from app.services.email_service import EmailService

router = APIRouter()
email_service = EmailService()


@router.post("/", response_model=ContactMessageResponse)
async def submit_contact_form(
    contact: ContactMessageCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Submit contact form"""
    db_contact = ContactMessage(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    
    # Send notification email to admin
    background_tasks.add_task(
        email_service.send_contact_notification,
        contact.dict()
    )
    
    return db_contact


@router.get("/messages", response_model=List[ContactMessageResponse])
async def get_contact_messages(
    skip: int = 0,
    limit: int = 50,
    unread_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get contact messages (admin only)"""
    query = db.query(ContactMessage)
    
    if unread_only:
        query = query.filter(ContactMessage.is_read == False)
    
    messages = query.order_by(ContactMessage.created_at.desc())\
                   .offset(skip).limit(limit).all()
    return messages


@router.put("/messages/{message_id}/read")
async def mark_message_as_read(message_id: int, db: Session = Depends(get_db)):
    """Mark contact message as read"""
    db_message = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if not db_message:
        raise HTTPException(status_code=404, detail="Wiadomość nie została znaleziona")
    
    db_message.is_read = True
    db.commit()
    
    return {"message": "Wiadomość oznaczona jako przeczytana"}

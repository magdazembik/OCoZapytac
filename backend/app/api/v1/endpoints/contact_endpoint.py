"""
Contact form endpoint for FastAPI application
Add this to your main.py or create a separate router
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

# Contact form data model
class ContactForm(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    subject: str
    message: str
    newsletter: Optional[bool] = False

# Email configuration - you'll need to set these environment variables
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": os.getenv("SENDER_EMAIL", "your-email@gmail.com"),  # Your Gmail address
    "sender_password": os.getenv("SENDER_APP_PASSWORD", "your-app-password"),  # Gmail app password
    "recipient_email": "magdalenka@gmail.com"
}

def send_contact_email(form_data: ContactForm):
    """Send contact form email using Gmail SMTP"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Kontakt ze strony: {form_data.subject}"
        msg['From'] = EMAIL_CONFIG["sender_email"]
        msg['To'] = EMAIL_CONFIG["recipient_email"]
        msg['Reply-To'] = form_data.email

        # Create HTML email content
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2563eb; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px;">
                    Nowa wiadomość ze strony O Co Zapytać
                </h2>
                
                <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #1e293b;">Dane kontaktowe:</h3>
                    <p><strong>Imię:</strong> {form_data.name or 'Nie podano'}</p>
                    <p><strong>Email:</strong> {form_data.email}</p>
                    <p><strong>Temat:</strong> {form_data.subject}</p>
                    <p><strong>Newsletter:</strong> {'Tak' if form_data.newsletter else 'Nie'}</p>
                    <p><strong>Data:</strong> {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
                </div>
                
                <div style="background-color: #ffffff; padding: 20px; border: 1px solid #e2e8f0; border-radius: 8px;">
                    <h3 style="margin-top: 0; color: #1e293b;">Wiadomość:</h3>
                    <div style="white-space: pre-wrap; line-height: 1.6;">
{form_data.message}
                    </div>
                </div>
                
                <div style="margin-top: 20px; padding: 15px; background-color: #dbeafe; border-radius: 8px; font-size: 14px;">
                    <p style="margin: 0;"><strong>Uwaga:</strong> To jest automatyczna wiadomość ze strony ocozapytac.pl. 
                    Aby odpowiedzieć, użyj adresu: {form_data.email}</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Create plain text version
        text_content = f"""
Nowa wiadomość ze strony O Co Zapytać

Dane kontaktowe:
Imię: {form_data.name or 'Nie podano'}
Email: {form_data.email}
Temat: {form_data.subject}
Newsletter: {'Tak' if form_data.newsletter else 'Nie'}
Data: {datetime.now().strftime('%d.%m.%Y %H:%M')}

Wiadomość:
{form_data.message}

---
To jest automatyczna wiadomość ze strony ocozapytac.pl.
Aby odpowiedzieć, użyj adresu: {form_data.email}
        """

        # Attach parts
        part1 = MIMEText(text_content, 'plain', 'utf-8')
        part2 = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(part1)
        msg.attach(part2)

        # Send email
        with smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"]) as server:
            server.starttls()
            server.login(EMAIL_CONFIG["sender_email"], EMAIL_CONFIG["sender_password"])
            server.send_message(msg)
            
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

# FastAPI router
router = APIRouter()

@router.post("/contact/")
async def submit_contact_form(
    form_data: ContactForm,
    background_tasks: BackgroundTasks
):
    """
    Handle contact form submission
    """
    try:
        # Send email in background
        background_tasks.add_task(send_contact_email, form_data)
        
        return {
            "status": "success",
            "message": "Dziękujemy za wiadomość! Odpowiemy w ciągu 24-48 godzin.",
            "html": """
            <div class="alert alert-success" style="padding: 15px; background-color: #d1edff; border: 1px solid #0ea5e9; border-radius: 6px; color: #0369a1; margin-top: 15px;">
                <strong>✓ Wiadomość wysłana!</strong><br>
                Dziękujemy za kontakt. Odpowiemy w ciągu 24-48 godzin.
            </div>
            """
        }
        
    except Exception as e:
        print(f"Contact form error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Wystąpił błąd podczas wysyłania wiadomości. Spróbuj ponownie później."
        )

# Add this to your main.py:
# from your_contact_module import router as contact_router
# app.include_router(contact_router, prefix="/api/v1")

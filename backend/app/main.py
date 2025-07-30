from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.config import settings
from app.core.database import engine, get_db
from app.models import Base
from app.api.v1.api import api_router
from app.api.v1.endpoints import pages
from app.models.article import Article
from sqlalchemy.orm import Session
from fastapi import Depends

# Contact form imports
from pydantic import BaseModel, EmailStr
from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


# Set up Jinja2 templates
TEMPLATES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../templates"))
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Contact form data model
class ContactForm(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    subject: str
    message: str
    newsletter: Optional[bool] = False

# Email configuration - SET THESE ENVIRONMENT VARIABLES
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

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    pass

def create_application() -> FastAPI:
    """Create FastAPI application with all configurations"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="Professional API for Polish entrepreneur tax blog",
        version="1.0.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan,
    )

    # Set all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    # # Include static pages router
    # app.include_router(pages.router)

    # Serve static files (if present)
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../static"))
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")

    return app

app = create_application()

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root(request: Request, db: Session = Depends(get_db)):
    # Get featured articles for the homepage
    featured_articles = db.query(Article).filter(Article.is_published == True)\
                         .order_by(Article.published_at.desc()).limit(3).all()
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "featured_articles": featured_articles
    })

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "tax-blog-backend"}

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@app.get("/articles", response_class=HTMLResponse)
async def articles(request: Request, db: Session = Depends(get_db)):
    # Get all published articles for the articles page
    all_articles = db.query(Article).filter(Article.is_published == True)\
                    .order_by(Article.published_at.desc()).all()
    return templates.TemplateResponse("articles.html", {
        "request": request, 
        "articles": all_articles
    })

@app.get("/categories", response_class=HTMLResponse)
async def categories(request: Request):
    return templates.TemplateResponse("categories.html", {"request": request})

# HTMX endpoints for dynamic content
@app.get("/htmx/featured-articles", response_class=HTMLResponse)
async def htmx_featured_articles(request: Request, db: Session = Depends(get_db)):
    """Return rendered HTML for featured articles (for HTMX)"""
    articles = db.query(Article).filter(Article.is_published == True)\
                .order_by(Article.published_at.desc()).limit(3).all()
    return templates.TemplateResponse("partials/article_card.html", {
        "request": request, 
        "articles": articles
    })

@app.get("/htmx/all-articles", response_class=HTMLResponse)
async def htmx_all_articles(request: Request, db: Session = Depends(get_db)):
    """Return rendered HTML for all articles (for HTMX)"""
    articles = db.query(Article).filter(Article.is_published == True)\
                .order_by(Article.published_at.desc()).all()
    return templates.TemplateResponse("partials/article_card.html", {
        "request": request, 
        "articles": articles
    })

# Contact form endpoint
@app.post("/api/v1/contact/")
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

# NEW: Single article page endpoint
@app.get("/artykul/{slug}", response_class=HTMLResponse)
async def single_article(request: Request, slug: str, db: Session = Depends(get_db)):
    """Display single article by slug"""
    # Get article by slug
    article = db.query(Article).filter(
        Article.slug == slug,
        Article.is_published == True
    ).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Artykuł nie został znaleziony")
    
    return templates.TemplateResponse("single_article.html", {
        "request": request,
        "article": article
    })

# HTMX endpoints for dynamic content
@app.get("/htmx/featured-articles", response_class=HTMLResponse)
async def htmx_featured_articles(request: Request, db: Session = Depends(get_db)):
    """Return rendered HTML for featured articles (for HTMX)"""
    articles = db.query(Article).filter(Article.is_published == True)\
                .order_by(Article.published_at.desc()).limit(3).all()
    return templates.TemplateResponse("partials/article_card.html", {
        "request": request, 
        "articles": articles
    })

# HTMX endpoint for related articles
@app.get("/htmx/related-articles/{category}/{article_id}", response_class=HTMLResponse)
async def htmx_related_articles(request: Request, category: str, article_id: int, db: Session = Depends(get_db)):
    """Return rendered HTML for related articles"""
    # Get 3 related articles from the same category, excluding current article
    related_articles = db.query(Article).filter(
        Article.category == category,
        Article.is_published == True,
        Article.id != article_id
    ).order_by(Article.published_at.desc()).limit(3).all()
    
    return templates.TemplateResponse("partials/related_articles.html", {
        "request": request,
        "articles": related_articles
    })
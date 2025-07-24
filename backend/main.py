from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@localhost/tax_blog_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI app
app = FastAPI(
    title="O co zapytam księgowego API",
    description="API for Polish entrepreneur tax blog",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://ocozapytamksiegowego.pl"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    subscribed_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    slug = Column(String(500), unique=True, nullable=False)
    excerpt = Column(Text)
    content = Column(Text)
    image_url = Column(String(500))
    video_url = Column(String(500))
    category = Column(String(100))
    author = Column(String(255))
    read_time = Column(String(50))
    published_at = Column(DateTime)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ContactMessage(Base):
    __tablename__ = "contact_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    subject = Column(String(500))
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class UserCreate(BaseModel):
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    email: str
    subscribed_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class ArticleCreate(BaseModel):
    title: str
    slug: str
    excerpt: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    category: Optional[str] = None
    author: Optional[str] = None
    read_time: Optional[str] = None
    is_published: bool = False

class ArticleResponse(BaseModel):
    id: int
    title: str
    slug: str
    excerpt: Optional[str]
    content: Optional[str]
    image_url: Optional[str]
    video_url: Optional[str]
    category: Optional[str]
    author: Optional[str]
    read_time: Optional[str]
    published_at: Optional[datetime]
    is_published: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class ContactMessageCreate(BaseModel):
    name: str
    email: EmailStr
    subject: Optional[str] = None
    message: str

class ContactMessageResponse(BaseModel):
    id: int
    name: str
    email: str
    subject: Optional[str]
    message: str
    created_at: datetime
    is_read: bool
    
    class Config:
        from_attributes = True

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Email service
class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.email_user = os.getenv("EMAIL_USER")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.from_email = os.getenv("FROM_EMAIL", self.email_user)
    
    def send_welcome_email(self, to_email: str):
        """Send welcome email to new subscriber"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = "Witamy w O co zapytam księgowego!"
            
            body = """
            <html>
            <body>
                <h2>Dziękujemy za zapisanie się do naszego newslettera!</h2>
                <p>Witaj w społeczności przedsiębiorców, którzy chcą być na równi ze swoimi księgowymi.</p>
                <p>Będziesz otrzymywać:</p>
                <ul>
                    <li>Najnowsze zmiany w prawie podatkowym</li>
                    <li>Praktyczne porady dotyczące optymalizacji podatkowej</li>
                    <li>Listę pytań do zadania księgowemu</li>
                    <li>Analizy przypadków z życia przedsiębiorców</li>
                </ul>
                <p>Pierwszy artykuł otrzymasz już wkrótce!</p>
                <br>
                <p>Pozdrawiamy,<br>Zespół O co zapytam księgowego</p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            text = msg.as_string()
            server.sendmail(self.from_email, to_email, text)
            server.quit()
            
            return True
        except Exception as e:
            logging.error(f"Failed to send welcome email: {str(e)}")
            return False
    
    def send_new_article_notification(self, subscribers: List[str], article: Article):
        """Send new article notification to all subscribers"""
        try:
            for subscriber_email in subscribers:
                msg = MIMEMultipart()
                msg['From'] = self.from_email
                msg['To'] = subscriber_email
                msg['Subject'] = f"Nowy artykuł: {article.title}"
                
                body = f"""
                <html>
                <body>
                    <h2>Nowy artykuł na O co zapytam księgowego</h2>
                    <h3>{article.title}</h3>
                    <p>{article.excerpt}</p>
                    <p><strong>Kategoria:</strong> {article.category}</p>
                    <p><strong>Czas czytania:</strong> {article.read_time}</p>
                    <a href="https://ocozapytamksiegowego.pl/artykul/{article.id}" 
                       style="background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%); 
                              color: white; padding: 12px 24px; text-decoration: none; 
                              border-radius: 25px; display: inline-block; margin: 20px 0;">
                        Czytaj pełny artykuł
                    </a>
                    <br><br>
                    <p>Pozdrawiamy,<br>Zespół O co zapytam księgowego</p>
                </body>
                </html>
                """
                
                msg.attach(MIMEText(body, 'html'))
                
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.email_user, self.email_password)
                text = msg.as_string()
                server.sendmail(self.from_email, subscriber_email, text)
                server.quit()
            
            return True
        except Exception as e:
            logging.error(f"Failed to send article notification: {str(e)}")
            return False

email_service = EmailService()

# API Routes

@app.get("/")
async def root():
    return {"message": "O co zapytam księgowego API"}

# Newsletter subscription endpoints
@app.post("/api/subscribe", response_model=UserResponse)
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
            db_user.updated_at = datetime.utcnow()
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

@app.post("/api/unsubscribe")
async def unsubscribe_newsletter(email: str, db: Session = Depends(get_db)):
    """Unsubscribe user from newsletter"""
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Email nie został znaleziony")
    
    db_user.is_active = False
    db_user.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Pomyślnie wypisano z newslettera"}

# Article endpoints
@app.get("/api/articles", response_model=List[ArticleResponse])
async def get_articles(
    skip: int = 0, 
    limit: int = 10, 
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get published articles"""
    query = db.query(Article).filter(Article.is_published == True)
    
    if category:
        query = query.filter(Article.category == category)
    
    articles = query.order_by(Article.published_at.desc()).offset(skip).limit(limit).all()
    return articles

@app.get("/api/articles/featured", response_model=List[ArticleResponse])
async def get_featured_articles(db: Session = Depends(get_db)):
    """Get 3 most recent published articles"""
    articles = db.query(Article).filter(Article.is_published == True)\
                 .order_by(Article.published_at.desc()).limit(3).all()
    return articles

@app.get("/api/articles/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: int, db: Session = Depends(get_db)):
    """Get single article by ID"""
    article = db.query(Article).filter(
        Article.id == article_id, 
        Article.is_published == True
    ).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Artykuł nie został znaleziony")
    
    return article

@app.get("/api/articles/slug/{slug}", response_model=ArticleResponse)
async def get_article_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get single article by slug"""
    article = db.query(Article).filter(
        Article.slug == slug, 
        Article.is_published == True
    ).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Artykuł nie został znaleziony")
    
    return article

@app.post("/api/articles", response_model=ArticleResponse)
async def create_article(
    article: ArticleCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create new article (admin only)"""
    # Check if slug already exists
    existing_article = db.query(Article).filter(Article.slug == article.slug).first()
    if existing_article:
        raise HTTPException(status_code=400, detail="Artykuł z tym slug już istnieje")
    
    db_article = Article(**article.dict())
    if article.is_published:
        db_article.published_at = datetime.utcnow()
    
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

# Contact form endpoints
@app.post("/api/contact", response_model=ContactMessageResponse)
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
    background_tasks.add_task(send_contact_notification, contact.dict())
    
    return db_contact

async def send_contact_notification(contact_data: dict):
    """Send contact form notification to admin"""
    try:
        admin_email = os.getenv("ADMIN_EMAIL", "admin@ocozapytamksiegowego.pl")
        
        msg = MIMEMultipart()
        msg['From'] = email_service.from_email
        msg['To'] = admin_email
        msg['Subject'] = f"Nowa wiadomość kontaktowa: {contact_data.get('subject', 'Brak tematu')}"
        
        body = f"""
        <html>
        <body>
            <h2>Nowa wiadomość kontaktowa</h2>
            <p><strong>Imię:</strong> {contact_data['name']}</p>
            <p><strong>Email:</strong> {contact_data['email']}</p>
            <p><strong>Temat:</strong> {contact_data.get('subject', 'Brak tematu')}</p>
            <p><strong>Wiadomość:</strong></p>
            <p>{contact_data['message']}</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(email_service.smtp_server, email_service.smtp_port)
        server.starttls()
        server.login(email_service.email_user, email_service.email_password)
        text = msg.as_string()
        server.sendmail(email_service.from_email, admin_email, text)
        server.quit()
        
    except Exception as e:
        logging.error(f"Failed to send contact notification: {str(e)}")

# Categories endpoint
@app.get("/api/categories")
async def get_categories(db: Session = Depends(get_db)):
    """Get all article categories"""
    categories = db.query(Article.category).filter(
        Article.is_published == True,
        Article.category.isnot(None)
    ).distinct().all()
    
    return [{"name": cat.category} for cat in categories if cat.category]

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

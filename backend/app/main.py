from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.config import settings
from app.core.database import engine
from app.models import Base
from app.api.v1.api import api_router
from app.api.v1.endpoints import pages

# Set up Jinja2 templates
TEMPLATES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../templates"))
templates = Jinja2Templates(directory=TEMPLATES_DIR)

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
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

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
async def articles(request: Request):
    return templates.TemplateResponse("articles.html", {"request": request})

@app.get("/categories", response_class=HTMLResponse)
async def categories(request: Request):
    return templates.TemplateResponse("categories.html", {"request": request})
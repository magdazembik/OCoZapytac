"""
Main FastAPI application entry point
"""

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

    # Serve static files
    if os.path.exists("static"):
        app.mount("/static", StaticFiles(directory="static"), name="static")

    return app


app = create_application()


templates = Jinja2Templates(directory=os.path.abspath(os.path.join(os.path.dirname(__file__), "../../templates")))

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root(request: Request):
    template = "index.html"
    response = templates.TemplateResponse(template, {"request": request})
    return response


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "tax-blog-backend"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.ENVIRONMENT == "development" else False,
    )

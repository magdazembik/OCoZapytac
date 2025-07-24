"""
Application configuration settings
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Project
    PROJECT_NAME: str = "O Co Zapytać"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "mysql+pymysql://user:password@localhost/ocozapytac"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    EMAIL_USER: Optional[str] = None
    EMAIL_PASSWORD: Optional[str] = None
    FROM_EMAIL: Optional[str] = None
    ADMIN_EMAIL: Optional[str] = None
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://ocozapytac.pl"
    ]
    
    # Redis (for caching and background tasks)
    REDIS_URL: str = "redis://localhost:6379"
    
    # File uploads
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

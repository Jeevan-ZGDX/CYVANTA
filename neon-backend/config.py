import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Neon by Ascertn Backend"
    VERSION: str = "2.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Database: defaults to SQLite async so it runs zero-config out of the box
    # Can be overridden with PostgreSQL (e.g. postgresql+asyncpg://user:pass@localhost:5432/neondb)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./neon.db")
    
    # Gemini AI
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Redis for distributed queues (optional)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Allowed CORS Origins for Vite frontend & production
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://localhost:3001",
        "https://tryneonai.com",
        "*"
    ]
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

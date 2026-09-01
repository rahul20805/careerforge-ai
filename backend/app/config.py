import os
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PROJECT_NAME: str = "CareerForge AI"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "careerforge-production-super-secret-key-32-chars-min"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # CORS
    CORS_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    @field_validator("CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        import json
        try:
            return json.loads(v)
        except Exception:
            return ["*"]

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./careerforge.db"
    SYNC_DATABASE_URL: str = "sqlite:///./careerforge.db"

    # Storage
    STORAGE_PROVIDER: str = "local"
    STORAGE_DIR: str = "./uploads"
    GENERATED_DOCS_DIR: str = "./generated_docs"

    # AI Configuration
    AI_PROVIDER: str = "gemini"  # gemini, openai, fallback
    AI_CLASSIFICATION_MODEL: str = "gemini-1.5-flash"
    AI_EXTRACTION_MODEL: str = "gemini-1.5-flash"
    AI_DOCUMENT_MODEL: str = "gemini-1.5-pro"
    AI_EMBEDDING_MODEL: str = "text-embedding-004"
    
    # Keys
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    HUNTER_API_KEY: str = ""

    # Scheduler & Limits
    SCHEDULED_SEARCH_INTERVAL_HOURS: int = 24
    DEADLINE_ALERT_DAYS: List[int] = [7, 3, 1, 0]
    MAX_DAILY_OUTREACH_EMAILS: int = 20

    # Default weights for matching
    MATCH_WEIGHTS: dict = {
        "required_skills": 0.30,
        "experience": 0.20,
        "education": 0.15,
        "semantic": 0.15,
        "research": 0.10,
        "location_eligibility": 0.05,
        "preferences": 0.05,
    }


settings = Settings()

# Ensure storage directories exist
os.makedirs(settings.STORAGE_DIR, exist_ok=True)
os.makedirs(settings.GENERATED_DOCS_DIR, exist_ok=True)

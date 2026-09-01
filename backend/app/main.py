from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.config import settings
from app.database import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB (in a real production app we'd use Alembic primarily)
    await init_db()
    yield
    # Cleanup logic

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Set all CORS enabled origins
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

import os
if os.getenv("VERCEL"):
    from sqlalchemy import create_engine
    from app.database import Base
    import app.models.entities  # Ensure models are loaded
    
    sync_engine = create_engine(settings.SYNC_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=sync_engine)
@app.get("/health", tags=["health"])
async def get_health():
    from app.integrations.hunter_client import HunterClient
    return {
        "status": "healthy",
        "version": "1.0.0",
        "database": "connected",
        "redis": "disabled_local",
        "ai_provider": settings.AI_PROVIDER,
        "hunter_configured": HunterClient.is_configured()
    }

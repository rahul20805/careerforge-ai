from typing import Generic, TypeVar, Optional, Any, Dict
from pydantic import BaseModel, Field

T = TypeVar("T")


class APIErrorDetails(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    error: Optional[APIErrorDetails] = None
    message: Optional[str] = None


class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str = "1.0.0"
    database: str = "connected"
    redis: str = "disabled_local"
    ai_provider: str = "gemini"
    ai_configured: bool = False
    hunter_configured: bool = False

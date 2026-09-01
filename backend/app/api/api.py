from fastapi import APIRouter
from app.api.endpoints import auth, profile
from app.ai import router as ai_router

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])
api_router.include_router(ai_router.router, prefix="/ai", tags=["ai"])

from app.api.endpoints import opportunities, resumes, applications, contacts, documents

# Optional includes - but we actually want them to be required now
api_router.include_router(opportunities.router, prefix="/opportunities", tags=["opportunities"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])

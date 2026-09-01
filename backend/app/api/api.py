from fastapi import APIRouter
from app.api.endpoints import auth, profile
from app.ai import router as ai_router

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])
api_router.include_router(ai_router.router, prefix="/ai", tags=["ai"])

# Optional includes
try:
    api_router.include_router(opportunities.router, prefix="/opportunities", tags=["opportunities"])
    api_router.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
    api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
except NameError:
    pass

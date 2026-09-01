from fastapi import APIRouter
from app.api.endpoints import auth, profile
# We will import other endpoints as they are built, mock them for now if missing
try:
    from app.api.endpoints import opportunities, resumes, applications
except ImportError:
    pass

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])

# Optional includes
try:
    api_router.include_router(opportunities.router, prefix="/opportunities", tags=["opportunities"])
    api_router.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
    api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
except NameError:
    pass

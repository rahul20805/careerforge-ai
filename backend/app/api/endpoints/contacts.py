from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Any, List

from app.database import get_db
from app.models.entities import User
from app.schemas.contacts import ContactResponse
from app.security.auth import get_current_user
from app.integrations.professor_discovery import ProfessorDiscovery

router = APIRouter()

@router.get("/professors/search")
async def search_professors(
    institution: str = Query(...),
    department: str = Query(None),
    research_area: str = Query(None),
    current_user: User = Depends(get_current_user),
) -> Any:
    results = await ProfessorDiscovery.search_professors(
        institution=institution,
        department=department,
        research_area=research_area
    )
    return results

@router.get("/", response_model=List[ContactResponse])
async def get_contacts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    return []

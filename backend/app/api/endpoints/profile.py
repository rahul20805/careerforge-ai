from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select

from app.database import get_db
from app.models.entities import User, Profile, Education, Experience, Project, Skill
from app.schemas.profile import (
    ProfileResponse, ProfileUpdate, EducationCreate, EducationResponse,
    ExperienceCreate, ExperienceResponse, ProjectCreate, ProjectResponse,
    SkillCreate, SkillResponse
)
from app.security.auth import get_current_user

router = APIRouter()

async def get_current_profile(db: AsyncSession, current_user: User) -> Profile:
    stmt = (
        select(Profile)
        .where(Profile.user_id == current_user.id)
        .options(
            selectinload(Profile.educations),
            selectinload(Profile.experiences),
            selectinload(Profile.projects),
            selectinload(Profile.skills),
            selectinload(Profile.certifications),
            selectinload(Profile.publications),
            selectinload(Profile.achievements),
            selectinload(Profile.preferences),
        )
    )
    result = await db.execute(stmt)
    profile = result.scalars().first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.get("/", response_model=ProfileResponse)
async def read_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    return await get_current_profile(db, current_user)

@router.put("/", response_model=ProfileResponse)
async def update_profile(
    *,
    db: AsyncSession = Depends(get_db),
    profile_in: ProfileUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    profile = await get_current_profile(db, current_user)
    update_data = profile_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    await db.commit()
    await db.refresh(profile)
    return await get_current_profile(db, current_user)

# Example sub-routes for projects
@router.post("/projects", response_model=ProjectResponse)
async def add_project(
    *,
    db: AsyncSession = Depends(get_db),
    project_in: ProjectCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    profile = await get_current_profile(db, current_user)
    project = Project(**project_in.model_dump(), profile_id=profile.id)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project

@router.delete("/projects/{id}")
async def delete_project(
    *,
    db: AsyncSession = Depends(get_db),
    id: str,
    current_user: User = Depends(get_current_user),
) -> Any:
    profile = await get_current_profile(db, current_user)
    stmt = select(Project).where(Project.id == id, Project.profile_id == profile.id)
    result = await db.execute(stmt)
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    await db.delete(project)
    await db.commit()
    return {"success": True}

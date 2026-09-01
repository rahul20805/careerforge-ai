from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Dict, Any, Optional

from app.database import get_db
from app.models.entities import Profile, User, Skill, Experience, Education, Project
from app.schemas.profile import ProfileUpdate, ProfileResponse
from app.security.auth import get_current_user

router = APIRouter()

async def get_current_profile(db: AsyncSession, current_user: User) -> Profile:
    stmt = (
        select(Profile)
        .where(Profile.user_id == current_user.id)
        .options(
            selectinload(Profile.skills),
            selectinload(Profile.experiences),
            selectinload(Profile.educations),
            selectinload(Profile.projects),
        )
    )
    result = await db.execute(stmt)
    profile = result.scalars().first()
    
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
        
    return profile

@router.get("/", response_model=ProfileResponse)
async def get_profile(
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    profile = await get_current_profile(db, current_user)
    return profile

@router.post("/", response_model=ProfileResponse)
async def update_profile(
    profile_data: ProfileUpdate, 
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    profile = await get_current_profile(db, current_user)
    
    update_data = profile_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
        
    await db.commit()
    await db.refresh(profile)
    
    # Reload with relationships
    stmt = (
        select(Profile)
        .where(Profile.id == profile.id)
        .options(
            selectinload(Profile.skills),
            selectinload(Profile.experiences),
            selectinload(Profile.educations),
            selectinload(Profile.projects),
        )
    )
    result = await db.execute(stmt)
    return result.scalars().first()

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.entities import User, Application, Opportunity
from app.schemas.application import ApplicationResponse, ApplicationCreate, ApplicationUpdate
from app.security.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ApplicationResponse])
async def get_applications(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    stmt = (
        select(Application)
        .where(Application.user_id == current_user.id)
        .options(selectinload(Application.opportunity))
    )
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/", response_model=ApplicationResponse)
async def create_application(
    *,
    db: AsyncSession = Depends(get_db),
    app_in: ApplicationCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    db_app = Application(**app_in.model_dump(), user_id=current_user.id)
    db.add(db_app)
    await db.commit()
    await db.refresh(db_app)
    
    # Reload with opportunity
    stmt = select(Application).where(Application.id == db_app.id).options(selectinload(Application.opportunity))
    result = await db.execute(stmt)
    return result.scalars().first()

@router.put("/{id}", response_model=ApplicationResponse)
async def update_application(
    *,
    db: AsyncSession = Depends(get_db),
    id: str,
    app_in: ApplicationUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    result = await db.execute(select(Application).where(Application.id == id, Application.user_id == current_user.id))
    db_app = result.scalars().first()
    if not db_app:
        raise HTTPException(status_code=404, detail="Application not found")
        
    update_data = app_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_app, field, value)
        
    await db.commit()
    await db.refresh(db_app)
    
    stmt = select(Application).where(Application.id == db_app.id).options(selectinload(Application.opportunity))
    result = await db.execute(stmt)
    return result.scalars().first()

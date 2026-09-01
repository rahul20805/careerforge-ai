from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Any, List
import uuid
from datetime import datetime

from app.database import get_db
from app.models.entities import User
from app.schemas.sop_lor_email import (
    SOPGenerateRequest, SOPResponse,
    LORGenerateRequest, LORResponse,
    EmailGenerateRequest, EmailDraftResponse
)
from app.security.auth import get_current_user
from app.ai.gemini_provider import GeminiProvider
from app.api.endpoints.profile import get_current_profile

router = APIRouter()

@router.post("/sop/generate", response_model=SOPResponse)
async def generate_sop(
    request: SOPGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    profile = await get_current_profile(db, current_user)
    # Convert profile to dict for AI prompt
    profile_data = {
        "headline": profile.headline,
        "summary": profile.summary,
        "skills": [s.name for s in profile.skills],
        "experiences": [{"organization": e.organization, "position": e.position} for e in profile.experiences],
        "educations": [{"degree": e.degree, "institution": e.institution} for e in profile.educations]
    }
    
    provider = GeminiProvider()
    result = await provider.generate_sop(
        master_profile=profile_data,
        target_details=request.model_dump(),
        tone=request.tone
    )
    
    return SOPResponse(
        id=str(uuid.uuid4()),
        user_id=str(current_user.id),
        opportunity_id=request.opportunity_id,
        target_program=request.target_program,
        target_lab=request.target_lab,
        target_professor=request.target_professor,
        tone=request.tone,
        content=result.get("content", ""),
        fact_sources=result.get("fact_sources", []),
        created_at=datetime.utcnow()
    )

@router.post("/lor/generate", response_model=LORResponse)
async def generate_lor(
    request: LORGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    profile = await get_current_profile(db, current_user)
    profile_data = {
        "headline": profile.headline,
        "summary": profile.summary,
    }
    provider = GeminiProvider()
    result = await provider.generate_lor_draft(
        master_profile=profile_data,
        recommender_info={"name": request.recommender_name, "title": request.recommender_title, "relationship": request.relationship_type},
        target_details={"institution": request.target_institution_or_company, "role": request.target_role_or_program}
    )
    
    return LORResponse(
        id=str(uuid.uuid4()),
        user_id=str(current_user.id),
        opportunity_id=request.opportunity_id,
        recommender_name=request.recommender_name,
        recommender_title=request.recommender_title,
        relationship_type=request.relationship_type,
        content=result.get("content", ""),
        is_draft_notice=True,
        created_at=datetime.utcnow()
    )

@router.post("/email/generate", response_model=EmailDraftResponse)
async def generate_email(
    request: EmailGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    profile = await get_current_profile(db, current_user)
    profile_data = {
        "headline": profile.headline,
        "summary": profile.summary,
    }
    provider = GeminiProvider()
    result = await provider.generate_email(
        master_profile=profile_data,
        target_details={"recipient": request.recipient_name, "organization": request.recipient_organization, "role": request.recipient_role},
        email_type=request.email_type,
        tone=request.tone
    )
    
    return EmailDraftResponse(
        id=str(uuid.uuid4()),
        user_id=str(current_user.id),
        application_id=request.application_id,
        email_type=request.email_type,
        recipient_name=request.recipient_name,
        recipient_email=request.recipient_email,
        subject=result.get("subject", "Follow up"),
        body=result.get("body", ""),
        tone=request.tone,
        is_sent=False,
        created_at=datetime.utcnow()
    )

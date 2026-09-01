from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.entities import User, Opportunity, OpportunityRequirement
from app.schemas.opportunity import (
    OpportunityResponse, OpportunityCreate, OpportunityParseRequest,
    OpportunitySearchRequest, OpportunityMatchResponse
)
from app.security.auth import get_current_user
from app.parsers.jd_parser import JDParser
from app.matching.engine import MatchingEngine
from app.api.endpoints.profile import get_current_profile

router = APIRouter()

@router.post("/parse", response_model=OpportunityCreate)
async def parse_opportunity(
    request: OpportunityParseRequest,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Parses an opportunity from text or URL using the AI engine.
    """
    if request.url:
        parsed_data = await JDParser.parse_url(request.url)
    elif request.text:
        parsed_data = await JDParser.parse_text(request.text)
    else:
        raise HTTPException(status_code=400, detail="Must provide text or url")

    # The AI provider returns dict matching the schema structure
    # We construct the response object
    reqs = []
    for skill in parsed_data.get("required_skills", []):
        reqs.append({"category": "skill", "requirement_text": skill, "is_mandatory": True, "weight": 1.0})
    for skill in parsed_data.get("preferred_skills", []):
        reqs.append({"category": "skill", "requirement_text": skill, "is_mandatory": False, "weight": 0.5})

    return OpportunityCreate(
        title=parsed_data.get("title", "Unknown Title"),
        company_name=parsed_data.get("company_name"),
        opportunity_type=parsed_data.get("opportunity_type", "Software Engineering"),
        work_mode=parsed_data.get("work_mode", "remote"),
        location=parsed_data.get("location"),
        country=parsed_data.get("country"),
        salary_or_stipend=parsed_data.get("salary_or_stipend"),
        description=parsed_data.get("description", ""),
        start_date=parsed_data.get("start_date"),
        end_date=parsed_data.get("end_date"),
        deadline=None,
        status="OPEN",
        status_source="Parser",
        source_url=parsed_data.get("source_url"),
        official_url=parsed_data.get("official_url"),
        source_name=request.source_type,
        source_type=request.source_type,
        verification_status="UNVERIFIED",
        requirements=reqs
    )

@router.post("/", response_model=OpportunityResponse)
async def create_opportunity(
    *,
    db: AsyncSession = Depends(get_db),
    opportunity_in: OpportunityCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    # Basic creation for now
    op_data = opportunity_in.model_dump(exclude={"requirements"})
    db_obj = Opportunity(**op_data)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)

    for req in opportunity_in.requirements:
        db_req = OpportunityRequirement(**req.model_dump(), opportunity_id=db_obj.id)
        db.add(db_req)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

@router.post("/{id}/match", response_model=OpportunityMatchResponse)
async def match_opportunity(
    *,
    db: AsyncSession = Depends(get_db),
    id: str,
    current_user: User = Depends(get_current_user),
) -> Any:
    result = await db.execute(select(Opportunity).where(Opportunity.id == id))
    opportunity = result.scalars().first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
        
    profile = await get_current_profile(db, current_user)
    return MatchingEngine.calculate_match(profile, opportunity)

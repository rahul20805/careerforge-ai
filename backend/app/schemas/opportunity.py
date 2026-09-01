from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class RequirementBase(BaseModel):
    category: str = "skill"  # skill, education, experience, research, responsibility, visa
    requirement_text: str
    is_mandatory: bool = True
    weight: float = 1.0


class RequirementResponse(RequirementBase):
    id: str
    opportunity_id: str

    class Config:
        from_attributes = True


class OpportunityBase(BaseModel):
    title: str
    company_name: Optional[str] = None
    opportunity_type: str = "Software Engineering"
    work_mode: str = "remote"  # remote, hybrid, onsite
    location: Optional[str] = None
    country: Optional[str] = None
    salary_or_stipend: Optional[str] = None
    description: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    deadline: Optional[datetime] = None
    status: str = "OPEN"  # NEW, OPEN, CLOSING_SOON, CLOSED, EXPIRED, UPDATED, PAUSED, UNKNOWN
    status_source: str = "Official Website"
    source_url: Optional[str] = None
    official_url: Optional[str] = None
    source_name: str = "Official Page"
    source_type: str = "OFFICIAL"  # OFFICIAL, PUBLIC_BOARD, MANUAL, DEMO
    verification_status: str = "VERIFIED"  # VERIFIED, UNVERIFIED, THIRD_PARTY


class OpportunityCreate(OpportunityBase):
    requirements: List[RequirementBase] = Field(default_factory=list)


class OpportunityUpdate(BaseModel):
    title: Optional[str] = None
    company_name: Optional[str] = None
    opportunity_type: Optional[str] = None
    work_mode: Optional[str] = None
    location: Optional[str] = None
    country: Optional[str] = None
    salary_or_stipend: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    status: Optional[str] = None
    verification_status: Optional[str] = None


class OpportunityResponse(OpportunityBase):
    id: str
    company_id: Optional[str] = None
    institution_id: Optional[str] = None
    last_verified: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    requirements: List[RequirementResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True


class OpportunitySearchRequest(BaseModel):
    query: Optional[str] = None
    opportunity_types: Optional[List[str]] = None
    work_modes: Optional[List[str]] = None
    countries: Optional[List[str]] = None
    source_type: Optional[str] = None
    verification_status: Optional[str] = None
    deadline_before: Optional[datetime] = None
    min_salary: Optional[float] = None
    page: int = 1
    page_size: int = 20


class OpportunityParseRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None
    source_type: str = "MANUAL"


class RequirementMatch(BaseModel):
    requirement: str
    category: str
    is_mandatory: bool
    status: str  # MATCHED, PARTIAL, MISSING
    matched_profile_items: List[str] = Field(default_factory=list)
    note: Optional[str] = None


class OpportunityMatchResponse(BaseModel):
    opportunity_id: str
    overall_match_score: float  # 0 to 100
    category_scores: Dict[str, float]  # skills, experience, education, semantic, research, preferences
    matched_requirements: List[RequirementMatch] = Field(default_factory=list)
    missing_requirements: List[RequirementMatch] = Field(default_factory=list)
    eligibility_concerns: List[str] = Field(default_factory=list)
    recommendation: str
    truthful_advice: str

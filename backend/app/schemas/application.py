from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.opportunity import OpportunityResponse


class ApplicationBase(BaseModel):
    opportunity_id: str
    status: str = "DISCOVERED"  # DISCOVERED, SHORTLISTED, RESUME_READY, EMAIL_READY, APPLIED, SCREENING, INTERVIEW, OFFER, REJECTED, WITHDRAWN, CLOSED
    match_score: float = 0.0
    ats_score: float = 0.0
    resume_version_id: Optional[str] = None
    sop_version_id: Optional[str] = None
    lor_version_id: Optional[str] = None
    applied_date: Optional[datetime] = None
    follow_up_date: Optional[datetime] = None
    notes: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    match_score: Optional[float] = None
    ats_score: Optional[float] = None
    resume_version_id: Optional[str] = None
    sop_version_id: Optional[str] = None
    lor_version_id: Optional[str] = None
    applied_date: Optional[datetime] = None
    follow_up_date: Optional[datetime] = None
    notes: Optional[str] = None


class ApplicationResponse(ApplicationBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    opportunity: Optional[OpportunityResponse] = None

    class Config:
        from_attributes = True


class KanbanColumn(BaseModel):
    id: str
    title: str
    count: int
    applications: List[ApplicationResponse] = Field(default_factory=list)


class AnalyticsSummaryResponse(BaseModel):
    total_applications: int
    applied_count: int
    interview_count: int
    offer_count: int
    rejected_count: int
    response_rate: float
    interview_rate: float
    offer_rate: float
    average_ats_score: float
    average_match_score: float
    applications_by_role: Dict[str, int]
    applications_by_country: Dict[str, int]

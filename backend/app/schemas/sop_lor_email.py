from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class SOPGenerateRequest(BaseModel):
    opportunity_id: Optional[str] = None
    target_program: str
    target_institute: str
    target_lab: Optional[str] = None
    target_professor: Optional[str] = None
    research_topics: List[str] = Field(default_factory=list)
    tone: str = "Academic"  # Academic, Research-focused, Professional, Concise


class SOPResponse(BaseModel):
    id: str
    user_id: str
    opportunity_id: Optional[str] = None
    target_program: Optional[str] = None
    target_lab: Optional[str] = None
    target_professor: Optional[str] = None
    tone: str
    content: str
    fact_sources: List[Dict[str, str]] = Field(default_factory=list)
    created_at: datetime

    class Config:
        from_attributes = True


class LORGenerateRequest(BaseModel):
    opportunity_id: Optional[str] = None
    recommender_name: str
    recommender_title: str
    relationship_type: str  # Professor, Research Advisor, Department Head, Engineering Manager
    target_institution_or_company: str
    target_role_or_program: str
    shared_course_or_project: Optional[str] = None
    key_qualities: List[str] = Field(default_factory=list)


class LORResponse(BaseModel):
    id: str
    user_id: str
    opportunity_id: Optional[str] = None
    recommender_name: str
    recommender_title: str
    relationship_type: str
    content: str
    is_draft_notice: bool = True
    created_at: datetime

    class Config:
        from_attributes = True


class EmailGenerateRequest(BaseModel):
    opportunity_id: Optional[str] = None
    application_id: Optional[str] = None
    email_type: str = "HR internship"  # HR internship, HR full-time, Recruiter, Professor, Cold outreach, Follow-up, Thank you
    recipient_name: Optional[str] = None
    recipient_email: Optional[str] = None
    recipient_role: Optional[str] = None
    recipient_organization: Optional[str] = None
    tone: str = "Professional"  # Professional, Warm, Direct, Academic, Recruiter-friendly


class EmailDraftResponse(BaseModel):
    id: str
    user_id: str
    application_id: Optional[str] = None
    email_type: str
    recipient_name: Optional[str] = None
    recipient_email: Optional[str] = None
    subject: str
    body: str
    tone: str
    is_sent: bool
    sent_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

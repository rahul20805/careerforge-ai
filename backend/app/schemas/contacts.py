from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class ContactResponse(BaseModel):
    id: str
    name: str
    email: str
    role: Optional[str] = None
    company_name: Optional[str] = None
    confidence_score: float = 0.0
    source: str = "Hunter.io"
    verification_status: str = "unverified"
    last_verified: Optional[datetime] = None

    class Config:
        from_attributes = True


class HunterDomainSearchRequest(BaseModel):
    domain: str
    company_name: Optional[str] = None
    department: Optional[str] = None  # hr, engineering, executive, etc.


class HunterEmailFinderRequest(BaseModel):
    domain: str
    first_name: str
    last_name: str


class HunterVerificationResponse(BaseModel):
    email: str
    status: str  # deliverable, risky, undeliverable, unverified
    score: float
    is_deliverable: bool
    source: str


class ProfessorSearchRequest(BaseModel):
    institution: Optional[str] = None
    research_area: Optional[str] = None
    department: Optional[str] = None


class ProfessorResponse(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    institution_name: Optional[str] = None
    department: Optional[str] = None
    lab_name: Optional[str] = None
    lab_url: Optional[str] = None
    profile_url: Optional[str] = None
    research_areas: List[str] = Field(default_factory=list)
    recent_papers: List[Dict[str, Any]] = Field(default_factory=list)
    is_accepting_students: bool = True
    match_score: Optional[float] = None
    match_reasons: List[str] = Field(default_factory=list)

    class Config:
        from_attributes = True

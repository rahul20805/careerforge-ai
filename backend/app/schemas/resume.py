from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.ats import ATSScoreResponse


class TailoredBullet(BaseModel):
    text: str
    source_reference: str  # e.g., "profile.experience[0].responsibilities[1]"
    keywords_highlighted: List[str] = Field(default_factory=list)


class TailoredExperience(BaseModel):
    organization: str
    position: str
    location: Optional[str] = None
    dates: str
    bullets: List[TailoredBullet]
    technologies: List[str] = Field(default_factory=list)


class TailoredProject(BaseModel):
    title: str
    description: str
    technologies: List[str]
    bullets: List[TailoredBullet]
    github_url: Optional[str] = None
    demo_url: Optional[str] = None


class TailoredResumeContent(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    links: Dict[str, str] = Field(default_factory=dict)
    summary: str
    skills_by_category: Dict[str, List[str]] = Field(default_factory=dict)
    experiences: List[TailoredExperience] = Field(default_factory=list)
    projects: List[TailoredProject] = Field(default_factory=list)
    educations: List[Dict[str, Any]] = Field(default_factory=list)
    certifications: List[Dict[str, Any]] = Field(default_factory=list)
    publications: List[Dict[str, Any]] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)
    section_order: List[str] = Field(
        default_factory=lambda: ["summary", "skills", "experience", "projects", "education", "certifications", "publications", "achievements"]
    )


class ResumeGenerateRequest(BaseModel):
    opportunity_id: Optional[str] = None
    target_job_title: Optional[str] = None
    target_job_description: Optional[str] = None
    template_name: str = "ATS Classic"  # ATS Classic, Technical, Research, Academic CV, Quant/Finance, SWE, One-page Internship, International Research


class ResumeResponse(BaseModel):
    id: str
    user_id: str
    opportunity_id: Optional[str] = None
    version_number: int
    template_name: str
    title: str
    tailored_content: TailoredResumeContent
    ats_score: float
    ats_breakdown: Optional[Dict[str, Any]] = None
    match_score: float
    truth_verified: bool
    unsupported_claims_found: List[str] = Field(default_factory=list)
    docx_file_path: Optional[str] = None
    pdf_file_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class EducationBase(BaseModel):
    degree: str
    institution: str
    department: Optional[str] = None
    field_of_study: Optional[str] = None
    gpa: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    coursework: List[str] = Field(default_factory=list)
    is_verified: bool = True


class EducationCreate(EducationBase):
    pass


class EducationResponse(EducationBase):
    id: str
    profile_id: str

    class Config:
        from_attributes = True


class ExperienceBase(BaseModel):
    organization: str
    position: str
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_current: bool = False
    responsibilities: List[str] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)
    is_research: bool = False
    is_verified: bool = True


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceResponse(ExperienceBase):
    id: str
    profile_id: str

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    title: str
    description: str
    technologies: List[str] = Field(default_factory=list)
    contributions: List[str] = Field(default_factory=list)
    results: List[str] = Field(default_factory=list)
    metrics: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    is_verified: bool = True


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: str
    profile_id: str

    class Config:
        from_attributes = True


class SkillBase(BaseModel):
    name: str
    category: str = "Technical"  # Programming, Frameworks, Cloud, ML, Finance, Tools, etc.
    proficiency: str = "Intermediate"  # Beginner, Intermediate, Advanced, Expert
    years_experience: Optional[float] = None
    is_verified: bool = True


class SkillCreate(SkillBase):
    pass


class SkillResponse(SkillBase):
    id: str
    profile_id: str

    class Config:
        from_attributes = True


class CertificationBase(BaseModel):
    name: str
    issuer: str
    issue_date: Optional[str] = None
    expiration_date: Optional[str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None
    is_verified: bool = True


class CertificationCreate(CertificationBase):
    pass


class CertificationResponse(CertificationBase):
    id: str
    profile_id: str

    class Config:
        from_attributes = True


class PublicationBase(BaseModel):
    title: str
    authors: List[str] = Field(default_factory=list)
    venue: Optional[str] = None
    publication_date: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    status: str = "Published"
    is_verified: bool = True


class PublicationCreate(PublicationBase):
    pass


class PublicationResponse(PublicationBase):
    id: str
    profile_id: str

    class Config:
        from_attributes = True


class AchievementBase(BaseModel):
    title: str
    issuer: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None
    is_verified: bool = True


class AchievementCreate(AchievementBase):
    pass


class AchievementResponse(AchievementBase):
    id: str
    profile_id: str

    class Config:
        from_attributes = True


class PreferenceBase(BaseModel):
    target_roles: List[str] = Field(default_factory=list)
    preferred_countries: List[str] = Field(default_factory=list)
    work_modes: List[str] = Field(default_factory=lambda: ["remote", "hybrid", "onsite"])
    opportunity_types: List[str] = Field(default_factory=lambda: ["full_time", "internship", "research_internship"])
    preferred_companies: List[str] = Field(default_factory=list)
    preferred_institutes: List[str] = Field(default_factory=list)
    preferred_research_areas: List[str] = Field(default_factory=list)
    min_salary: Optional[float] = None
    currency: str = "USD"
    start_availability: Optional[str] = None
    requires_visa: bool = False


class PreferenceCreate(PreferenceBase):
    pass


class PreferenceResponse(PreferenceBase):
    id: str
    profile_id: str

    class Config:
        from_attributes = True


class ProfileUpdate(BaseModel):
    phone: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    website_url: Optional[str] = None
    headline: Optional[str] = None
    summary: Optional[str] = None


class ProfileResponse(BaseModel):
    id: str
    user_id: str
    phone: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    website_url: Optional[str] = None
    headline: Optional[str] = None
    summary: Optional[str] = None
    completeness_score: float = 0.0
    truth_verified_at: Optional[datetime] = None
    
    educations: List[EducationResponse] = Field(default_factory=list)
    experiences: List[ExperienceResponse] = Field(default_factory=list)
    projects: List[ProjectResponse] = Field(default_factory=list)
    skills: List[SkillResponse] = Field(default_factory=list)
    certifications: List[CertificationResponse] = Field(default_factory=list)
    publications: List[PublicationResponse] = Field(default_factory=list)
    achievements: List[AchievementResponse] = Field(default_factory=list)
    preferences: Optional[PreferenceResponse] = None

    class Config:
        from_attributes = True

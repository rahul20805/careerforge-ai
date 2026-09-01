import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    Column, String, Text, Integer, Float, Boolean, DateTime, ForeignKey, JSON, Enum
)
from sqlalchemy.orm import relationship
from app.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default="user")  # user, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")
    resumes = relationship("ResumeVersion", back_populates="user", cascade="all, delete-orphan")
    sops = relationship("SOPVersion", back_populates="user", cascade="all, delete-orphan")
    lors = relationship("LORVersion", back_populates="user", cascade="all, delete-orphan")
    emails = relationship("EmailDraft", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    search_runs = relationship("SearchRun", back_populates="user", cascade="all, delete-orphan")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), unique=True, nullable=False)
    phone = Column(String(50), nullable=True)
    country = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    linkedin_url = Column(String(255), nullable=True)
    github_url = Column(String(255), nullable=True)
    portfolio_url = Column(String(255), nullable=True)
    website_url = Column(String(255), nullable=True)
    headline = Column(String(255), nullable=True)
    summary = Column(Text, nullable=True)
    completeness_score = Column(Float, default=0.0)
    truth_verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="profile")
    educations = relationship("Education", back_populates="profile", cascade="all, delete-orphan")
    experiences = relationship("Experience", back_populates="profile", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="profile", cascade="all, delete-orphan")
    skills = relationship("Skill", back_populates="profile", cascade="all, delete-orphan")
    certifications = relationship("Certification", back_populates="profile", cascade="all, delete-orphan")
    publications = relationship("Publication", back_populates="profile", cascade="all, delete-orphan")
    achievements = relationship("Achievement", back_populates="profile", cascade="all, delete-orphan")
    preferences = relationship("Preference", back_populates="profile", uselist=False, cascade="all, delete-orphan")


class Education(Base):
    __tablename__ = "education"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    profile_id = Column(String(36), ForeignKey("profiles.id"), nullable=False)
    degree = Column(String(255), nullable=False)
    institution = Column(String(255), nullable=False)
    department = Column(String(255), nullable=True)
    field_of_study = Column(String(255), nullable=True)
    gpa = Column(String(50), nullable=True)
    start_date = Column(String(50), nullable=True)
    end_date = Column(String(50), nullable=True)
    coursework = Column(JSON, default=list)  # list of strings
    is_verified = Column(Boolean, default=True)

    profile = relationship("Profile", back_populates="educations")


class Experience(Base):
    __tablename__ = "experience"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    profile_id = Column(String(36), ForeignKey("profiles.id"), nullable=False)
    organization = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True)
    start_date = Column(String(50), nullable=True)
    end_date = Column(String(50), nullable=True)
    is_current = Column(Boolean, default=False)
    responsibilities = Column(JSON, default=list)  # list of bullet points
    achievements = Column(JSON, default=list)
    technologies = Column(JSON, default=list)
    is_research = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=True)

    profile = relationship("Profile", back_populates="experiences")


class Project(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    profile_id = Column(String(36), ForeignKey("profiles.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    technologies = Column(JSON, default=list)
    contributions = Column(JSON, default=list)
    results = Column(JSON, default=list)
    metrics = Column(String(255), nullable=True)
    start_date = Column(String(50), nullable=True)
    end_date = Column(String(50), nullable=True)
    github_url = Column(String(255), nullable=True)
    demo_url = Column(String(255), nullable=True)
    is_verified = Column(Boolean, default=True)

    profile = relationship("Profile", back_populates="projects")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    profile_id = Column(String(36), ForeignKey("profiles.id"), nullable=False)
    name = Column(String(100), nullable=False, index=True)
    category = Column(String(100), default="Technical")  # Programming, Frameworks, Cloud, ML, Finance, Tools, etc.
    proficiency = Column(String(50), default="Intermediate")  # Beginner, Intermediate, Advanced, Expert
    years_experience = Column(Float, nullable=True)
    is_verified = Column(Boolean, default=True)

    profile = relationship("Profile", back_populates="skills")


class Certification(Base):
    __tablename__ = "certifications"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    profile_id = Column(String(36), ForeignKey("profiles.id"), nullable=False)
    name = Column(String(255), nullable=False)
    issuer = Column(String(255), nullable=False)
    issue_date = Column(String(50), nullable=True)
    expiration_date = Column(String(50), nullable=True)
    credential_id = Column(String(255), nullable=True)
    credential_url = Column(String(255), nullable=True)
    is_verified = Column(Boolean, default=True)

    profile = relationship("Profile", back_populates="certifications")


class Publication(Base):
    __tablename__ = "publications"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    profile_id = Column(String(36), ForeignKey("profiles.id"), nullable=False)
    title = Column(String(255), nullable=False)
    authors = Column(JSON, default=list)
    venue = Column(String(255), nullable=True)  # Conference/Journal
    publication_date = Column(String(50), nullable=True)
    doi = Column(String(255), nullable=True)
    url = Column(String(255), nullable=True)
    status = Column(String(50), default="Published")  # Published, Accepted, Under Review, Preprint
    is_verified = Column(Boolean, default=True)

    profile = relationship("Profile", back_populates="publications")


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    profile_id = Column(String(36), ForeignKey("profiles.id"), nullable=False)
    title = Column(String(255), nullable=False)
    issuer = Column(String(255), nullable=True)
    date = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    is_verified = Column(Boolean, default=True)

    profile = relationship("Profile", back_populates="achievements")


class Preference(Base):
    __tablename__ = "preferences"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    profile_id = Column(String(36), ForeignKey("profiles.id"), unique=True, nullable=False)
    target_roles = Column(JSON, default=list)
    preferred_countries = Column(JSON, default=list)
    work_modes = Column(JSON, default=lambda: ["remote", "hybrid", "onsite"])
    opportunity_types = Column(JSON, default=lambda: ["full_time", "internship", "research_internship"])
    preferred_companies = Column(JSON, default=list)
    preferred_institutes = Column(JSON, default=list)
    preferred_research_areas = Column(JSON, default=list)
    min_salary = Column(Float, nullable=True)
    currency = Column(String(10), default="USD")
    start_availability = Column(String(50), nullable=True)
    requires_visa = Column(Boolean, default=False)

    profile = relationship("Profile", back_populates="preferences")


class Company(Base):
    __tablename__ = "companies"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), unique=True, index=True, nullable=False)
    domain = Column(String(255), nullable=True)
    website_url = Column(String(255), nullable=True)
    career_page_url = Column(String(255), nullable=True)
    industry = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    is_verified = Column(Boolean, default=True)

    opportunities = relationship("Opportunity", back_populates="company")
    contacts = relationship("Contact", back_populates="company")


class Institution(Base):
    __tablename__ = "institutions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), unique=True, index=True, nullable=False)
    domain = Column(String(255), nullable=True)
    country = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    website_url = Column(String(255), nullable=True)
    is_verified = Column(Boolean, default=True)

    professors = relationship("Professor", back_populates="institution")
    opportunities = relationship("Opportunity", back_populates="institution")


class Professor(Base):
    __tablename__ = "professors"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    institution_id = Column(String(36), ForeignKey("institutions.id"), nullable=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=True)
    department = Column(String(255), nullable=True)
    lab_name = Column(String(255), nullable=True)
    lab_url = Column(String(255), nullable=True)
    profile_url = Column(String(255), nullable=True)
    research_areas = Column(JSON, default=list)
    recent_papers = Column(JSON, default=list)
    is_accepting_students = Column(Boolean, default=True)
    verified_at = Column(DateTime, nullable=True)

    institution = relationship("Institution", back_populates="professors")


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    role = Column(String(255), nullable=True)  # HR, Recruiter, Engineering Manager, etc.
    linkedin_url = Column(String(255), nullable=True)
    confidence_score = Column(Float, default=0.0)
    source = Column(String(100), default="Hunter.io")
    verification_status = Column(String(50), default="unverified")  # verified, unverified, invalid
    last_verified = Column(DateTime, nullable=True)

    company = relationship("Company", back_populates="contacts")


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False, index=True)
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=True)
    institution_id = Column(String(36), ForeignKey("institutions.id"), nullable=True)
    company_name = Column(String(255), nullable=True)
    opportunity_type = Column(String(100), nullable=False, index=True)  # Software Engineering, AI/ML, Research Internship, etc.
    work_mode = Column(String(50), default="remote")  # remote, hybrid, onsite
    location = Column(String(255), nullable=True)
    country = Column(String(100), nullable=True, index=True)
    salary_or_stipend = Column(String(100), nullable=True)
    description = Column(Text, nullable=False)
    
    # Dates & Deadlines
    start_date = Column(String(50), nullable=True)
    end_date = Column(String(50), nullable=True)
    deadline = Column(DateTime, nullable=True, index=True)
    
    # Status
    status = Column(String(50), default="OPEN", index=True)  # NEW, OPEN, CLOSING_SOON, CLOSED, EXPIRED, UPDATED, PAUSED, UNKNOWN
    status_source = Column(String(100), default="Official Website")
    
    # Source tracking & Ethical verification
    source_url = Column(String(500), nullable=True)
    official_url = Column(String(500), nullable=True)
    source_name = Column(String(255), default="Official Page")
    source_type = Column(String(50), default="OFFICIAL")  # OFFICIAL, PUBLIC_BOARD, MANUAL, DEMO
    verification_status = Column(String(50), default="VERIFIED")  # VERIFIED, UNVERIFIED, THIRD_PARTY
    last_verified = Column(DateTime, default=datetime.utcnow)
    
    # Changes snapshot
    snapshot_hash = Column(String(64), nullable=True)
    last_changes = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="opportunities")
    institution = relationship("Institution", back_populates="opportunities")
    requirements = relationship("OpportunityRequirement", back_populates="opportunity", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="opportunity")


class OpportunityRequirement(Base):
    __tablename__ = "opportunity_requirements"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    opportunity_id = Column(String(36), ForeignKey("opportunities.id"), nullable=False)
    category = Column(String(50), default="skill")  # skill, education, experience, research, responsibility, visa
    requirement_text = Column(Text, nullable=False)
    is_mandatory = Column(Boolean, default=True)
    weight = Column(Float, default=1.0)

    opportunity = relationship("Opportunity", back_populates="requirements")


class Application(Base):
    __tablename__ = "applications"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    opportunity_id = Column(String(36), ForeignKey("opportunities.id"), nullable=False)
    
    # Kanban Status
    status = Column(String(50), default="DISCOVERED", index=True)
    # DISCOVERED, SHORTLISTED, RESUME_READY, EMAIL_READY, APPLIED, SCREENING, INTERVIEW, OFFER, REJECTED, WITHDRAWN, CLOSED

    match_score = Column(Float, default=0.0)
    ats_score = Column(Float, default=0.0)
    
    resume_version_id = Column(String(36), ForeignKey("resume_versions.id"), nullable=True)
    sop_version_id = Column(String(36), ForeignKey("sop_versions.id"), nullable=True)
    lor_version_id = Column(String(36), ForeignKey("lor_versions.id"), nullable=True)
    
    applied_date = Column(DateTime, nullable=True)
    follow_up_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="applications")
    opportunity = relationship("Opportunity", back_populates="applications")
    resume_version = relationship("ResumeVersion", foreign_keys=[resume_version_id])
    sop_version = relationship("SOPVersion", foreign_keys=[sop_version_id])
    lor_version = relationship("LORVersion", foreign_keys=[lor_version_id])
    emails = relationship("EmailDraft", back_populates="application")


class ResumeVersion(Base):
    __tablename__ = "resume_versions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    opportunity_id = Column(String(36), ForeignKey("opportunities.id"), nullable=True)
    version_number = Column(Integer, default=1)
    template_name = Column(String(100), default="ATS Classic")  # ATS Classic, Technical, Research, Academic CV, Quant/Finance, etc.
    
    title = Column(String(255), nullable=False)
    tailored_content = Column(JSON, nullable=False)  # Complete verified structured sections
    
    ats_score = Column(Float, default=0.0)
    ats_breakdown = Column(JSON, default=dict)
    match_score = Column(Float, default=0.0)
    truth_verified = Column(Boolean, default=True)
    unsupported_claims_found = Column(JSON, default=list)
    
    docx_file_path = Column(String(500), nullable=True)
    pdf_file_path = Column(String(500), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="resumes")


class SOPVersion(Base):
    __tablename__ = "sop_versions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    opportunity_id = Column(String(36), ForeignKey("opportunities.id"), nullable=True)
    target_program = Column(String(255), nullable=True)
    target_lab = Column(String(255), nullable=True)
    target_professor = Column(String(255), nullable=True)
    tone = Column(String(50), default="Academic")
    content = Column(Text, nullable=False)
    fact_sources = Column(JSON, default=list)  # Internal trace citations
    
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sops")


class LORVersion(Base):
    __tablename__ = "lor_versions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    opportunity_id = Column(String(36), ForeignKey("opportunities.id"), nullable=True)
    recommender_name = Column(String(255), nullable=False)
    recommender_title = Column(String(255), nullable=False)
    relationship_type = Column(String(100), nullable=False)  # Professor, Research Advisor, Manager
    content = Column(Text, nullable=False)
    is_draft_notice = Column(Boolean, default=True)  # Clearly marked as Draft for recommender review
    
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="lors")


class EmailDraft(Base):
    __tablename__ = "email_drafts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    application_id = Column(String(36), ForeignKey("applications.id"), nullable=True)
    email_type = Column(String(100), nullable=False)  # HR internship, Recruiter, Professor, Follow-up
    recipient_name = Column(String(255), nullable=True)
    recipient_email = Column(String(255), nullable=True)
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    tone = Column(String(50), default="Professional")
    is_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="emails")
    application = relationship("Application", back_populates="emails")


class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)  # pdf, docx, txt
    file_size = Column(Integer, nullable=False)
    file_path = Column(String(500), nullable=False)
    document_category = Column(String(50), default="resume")  # resume, transcript, certificate, sop
    created_at = Column(DateTime, default=datetime.utcnow)


class DeadlineEvent(Base):
    __tablename__ = "deadline_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    opportunity_id = Column(String(36), ForeignKey("opportunities.id"), nullable=False)
    deadline_date = Column(DateTime, nullable=False)
    days_remaining = Column(Integer, nullable=False)
    notification_triggered = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), default="DEADLINE")  # DEADLINE, OPPORTUNITY_UPDATE, MATCH_ALERT, SYSTEM
    link = Column(String(255), nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")


class SearchRun(Base):
    __tablename__ = "search_runs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    query = Column(String(255), nullable=False)
    filters = Column(JSON, default=dict)
    total_found = Column(Integer, default=0)
    new_opportunities_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="search_runs")


class VerificationRecord(Base):
    __tablename__ = "verification_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    entity_type = Column(String(50), nullable=False)  # opportunity, contact, resume_claim
    entity_id = Column(String(36), nullable=False)
    source = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)  # VERIFIED, REJECTED, UNVERIFIED
    details = Column(JSON, default=dict)
    verified_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    entity_name = Column(String(100), nullable=False)
    entity_id = Column(String(36), nullable=True)
    ip_address = Column(String(50), nullable=True)
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="audit_logs")


class ApiIntegration(Base):
    __tablename__ = "api_integrations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    provider_name = Column(String(100), nullable=False, unique=True)  # openai, gemini, hunter
    is_configured = Column(Boolean, default=False)
    last_tested_at = Column(DateTime, nullable=True)
    status_message = Column(String(255), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ModelRun(Base):
    __tablename__ = "model_runs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    task_type = Column(String(100), nullable=False)  # classification, extraction, resume_customization, sop_generation
    provider = Column(String(50), nullable=False)
    model_name = Column(String(100), nullable=False)
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    duration_ms = Column(Float, default=0.0)
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import json

from app.database import get_db
from app.models.entities import User, Opportunity, ResumeVersion
from app.schemas.resume import ResumeGenerateRequest, ResumeResponse
from app.schemas.ats import ATSScoreRequest, ATSScoreResponse
from app.security.auth import get_current_user
from app.api.endpoints.profile import get_current_profile
from app.ai.router import ai_service
from app.truth.engine import TruthEngine
from app.ats.scorer import ATSScorer
from app.documents.generator import DocumentGenerator

router = APIRouter()

@router.post("/generate", response_model=ResumeResponse)
async def generate_resume(
    *,
    db: AsyncSession = Depends(get_db),
    request: ResumeGenerateRequest,
    current_user: User = Depends(get_current_user),
) -> Any:
    profile = await get_current_profile(db, current_user)
    
    job_details = {}
    if request.opportunity_id:
        result = await db.execute(select(Opportunity).where(Opportunity.id == request.opportunity_id))
        opportunity = result.scalars().first()
        if opportunity:
            job_details = {
                "title": opportunity.title,
                "description": opportunity.description,
                "required_skills": [r.requirement_text for r in opportunity.requirements if r.category == "skill" and r.is_mandatory],
                "preferred_skills": [r.requirement_text for r in opportunity.requirements if r.category == "skill" and not r.is_mandatory]
            }
    elif request.target_job_description:
        # Fallback to provided description
        job_details = await ai_service.extract_job_details(request.target_job_description)
        if request.target_job_title:
            job_details["title"] = request.target_job_title
    
    # Extract truth vocabulary from profile
    profile_vocab = TruthEngine.extract_truth_vocabulary(profile)
    
    # Generate Tailored Content (strictly truthful)
    # Serialize profile for the AI service
    profile_dict = {
        "full_name": current_user.full_name,
        "email": current_user.email,
        "phone": profile.phone,
        "city": profile.city,
        "country": profile.country,
        "linkedin_url": profile.linkedin_url,
        "github_url": profile.github_url,
        "portfolio_url": profile.portfolio_url,
        "summary": profile.summary,
        "skills": [{"name": s.name} for s in profile.skills],
        "experiences": [{"organization": e.organization, "position": e.position, "start_date": e.start_date, "end_date": e.end_date, "responsibilities": e.responsibilities, "technologies": e.technologies} for e in profile.experiences],
        "projects": [{"title": p.title, "description": p.description, "technologies": p.technologies, "contributions": p.contributions} for p in profile.projects],
        "educations": [{"degree": e.degree, "institution": e.institution, "gpa": e.gpa} for e in profile.educations]
    }
    
    tailored_content = await ai_service.tailor_resume_content(
        master_profile=profile_dict,
        job_details=job_details,
        target_template=request.template_name
    )
    
    # Calculate ATS Score
    ats_evaluation = ATSScorer.evaluate_resume(tailored_content, job_details, profile_vocab)
    
    # Generate Files
    docx_path = DocumentGenerator.generate_docx(tailored_content, request.template_name)
    pdf_path = DocumentGenerator.generate_pdf(tailored_content, request.template_name)
    
    resume_version = ResumeVersion(
        user_id=current_user.id,
        opportunity_id=request.opportunity_id,
        version_number=1,
        template_name=request.template_name,
        title=f"Resume - {job_details.get('title', 'Target Role')}",
        tailored_content=tailored_content,
        ats_score=ats_evaluation.overall_score,
        ats_breakdown=ats_evaluation.model_dump(),
        match_score=0.0,
        truth_verified=ats_evaluation.is_truthful,
        unsupported_claims_found=ats_evaluation.unsupported_claims_detected,
        docx_file_path=docx_path,
        pdf_file_path=pdf_path
    )
    
    db.add(resume_version)
    await db.commit()
    await db.refresh(resume_version)
    
    return resume_version

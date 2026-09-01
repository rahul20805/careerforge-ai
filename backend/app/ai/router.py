from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import google.generativeai as genai
import os
import json
import fitz  # PyMuPDF
from bs4 import BeautifulSoup
import httpx
from pydantic import BaseModel
from typing import Optional

from app.api.endpoints.profile import get_current_user
from app.db.models import User, Profile, Opportunity
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

router = APIRouter()

# Initialize Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "mock-key"))
model = genai.GenerativeModel('gemini-1.5-pro')

class JDRequest(BaseModel):
    url: str

@router.post("/parse-resume")
async def parse_resume(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Read PDF
    content = await file.read()
    try:
        doc = fitz.open(stream=content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {str(e)}")
    
    # Call Gemini
    prompt = f"""
    Extract the following information from this resume text into a strict JSON format.
    Do NOT include markdown formatting or backticks in your response, just raw JSON.
    Format:
    {{
      "first_name": "string",
      "last_name": "string",
      "skills": ["string"],
      "experience": [
        {{"company": "string", "role": "string", "duration": "string", "description": "string"}}
      ],
      "education": [
        {{"institution": "string", "degree": "string", "year": "string"}}
      ]
    }}
    
    Resume Text:
    {text}
    """
    
    try:
        response = model.generate_content(prompt)
        # Parse JSON
        result_text = response.text.replace('```json', '').replace('```', '').strip()
        parsed_data = json.loads(result_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI parsing failed: {str(e)}")
        
    # Update Profile
    result = await db.execute(select(Profile).where(Profile.user_id == current_user.id))
    profile = result.scalars().first()
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.add(profile)
        
    profile.first_name = parsed_data.get("first_name", profile.first_name)
    profile.last_name = parsed_data.get("last_name", profile.last_name)
    
    # Merge skills uniquely
    existing_skills = set(profile.skills or [])
    new_skills = set(parsed_data.get("skills", []))
    profile.skills = list(existing_skills.union(new_skills))
    
    profile.experience = parsed_data.get("experience", profile.experience)
    profile.education = parsed_data.get("education", profile.education)
    
    await db.commit()
    
    return {"status": "success", "data": parsed_data}

@router.post("/parse-jd")
async def parse_jd(req: JDRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # 1. Scrape URL
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(req.url, follow_redirects=True, timeout=10.0)
            soup = BeautifulSoup(resp.text, 'lxml')
            jd_text = soup.get_text(separator=' ', strip=True)
            # Limit text length to avoid token limits
            jd_text = jd_text[:15000] 
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to scrape URL: {str(e)}")
        
    # 2. Get User Profile
    result = await db.execute(select(Profile).where(Profile.user_id == current_user.id))
    profile = result.scalars().first()
    profile_data = profile.skills if profile else []
    
    # 3. Match with AI
    prompt = f"""
    Analyze this Job Description and the candidate's skills.
    Generate a JSON response with:
    1. company: The name of the company
    2. role: The job title
    3. ats_score: A match score from 0 to 100
    4. missing_keywords: List of skills in the JD that the candidate lacks
    
    Candidate Skills: {json.dumps(profile_data)}
    
    Job Description Text:
    {jd_text}
    
    Respond ONLY with raw JSON.
    """
    
    try:
        response = model.generate_content(prompt)
        result_text = response.text.replace('```json', '').replace('```', '').strip()
        parsed = json.loads(result_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail="AI JD Match failed")
        
    # 4. Save to DB
    opp = Opportunity(
        user_id=current_user.id,
        company=parsed.get("company", "Unknown"),
        role=parsed.get("role", "Unknown"),
        url=req.url,
        ats_score=parsed.get("ats_score", 0)
    )
    db.add(opp)
    await db.commit()
    
    return {"status": "success", "data": parsed}

@router.post("/truth-engine")
async def run_truth_engine(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Profile).where(Profile.user_id == current_user.id))
    profile = result.scalars().first()
    if not profile or not profile.experience or not profile.skills:
        return {"status": "error", "message": "Incomplete profile data"}
        
    prompt = f"""
    You are the CareerForge Truth-Engine. Analyze the user's claimed skills and cross-reference them against their work experience.
    Identify any skills that seem exaggerated or are missing from the work descriptions.
    
    Skills: {json.dumps(profile.skills)}
    Experience: {json.dumps(profile.experience)}
    
    Return a JSON object:
    {{
        "verified_skills": ["skill1", "skill2"],
        "flagged_skills": [
            {{"skill": "skill3", "reason": "Not mentioned in any job description"}}
        ]
    }}
    Respond ONLY with raw JSON.
    """
    
    try:
        response = model.generate_content(prompt)
        result_text = response.text.replace('```json', '').replace('```', '').strip()
        parsed = json.loads(result_text)
        return {"status": "success", "validation": parsed}
    except Exception:
        raise HTTPException(status_code=500, detail="Truth-Engine processing failed")

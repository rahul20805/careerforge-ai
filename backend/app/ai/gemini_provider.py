import json
from typing import Dict, Any
from app.ai.base import AIProvider
from app.config import settings

try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False


class GeminiProvider(AIProvider):
    def __init__(self, api_key: str = ""):
        self.api_key = api_key or settings.GEMINI_API_KEY
        if HAS_GEMINI and self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(settings.AI_EXTRACTION_MODEL)
            self.doc_model = genai.GenerativeModel(settings.AI_DOCUMENT_MODEL)
        else:
            self.model = None
            self.doc_model = None

    async def extract_job_details(self, raw_text: str) -> Dict[str, Any]:
        if not self.model:
            from app.ai.fallback_provider import FallbackProvider
            return await FallbackProvider().extract_job_details(raw_text)

        prompt = f"""
        Extract the following job/internship/research posting into valid, parseable JSON matching these exact keys:
        - title: string
        - company_name: string
        - opportunity_type: string (e.g. Software Engineering, AI/ML, Research Internship, Quantitative Finance)
        - work_mode: string (remote, hybrid, onsite)
        - location: string
        - country: string
        - salary_or_stipend: string
        - description: string (clean summary)
        - required_skills: list of strings
        - preferred_skills: list of strings
        - responsibilities: list of strings
        - qualifications: list of strings
        - application_url: string or null
        - deadline: ISO string (YYYY-MM-DD) or null

        JOB POSTING TEXT:
        {raw_text[:6000]}
        
        Respond ONLY with a JSON object. No Markdown code fences, no extra text.
        """
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            return json.loads(text)
        except Exception:
            from app.ai.fallback_provider import FallbackProvider
            return await FallbackProvider().extract_job_details(raw_text)

    async def classify_opportunity(self, title: str, description: str) -> Dict[str, Any]:
        if not self.model:
            from app.ai.fallback_provider import FallbackProvider
            return await FallbackProvider().classify_opportunity(title, description)

        prompt = f"""
        Classify this opportunity into one primary category among:
        Software Engineering, AI/ML, Data Science, Quantitative Finance, HFT, Research Internship, Fellowship, Cybersecurity, Robotics, Finance.
        
        Opportunity Title: {title}
        Opportunity Description: {description[:3000]}
        
        Return JSON with:
        - category: string
        - confidence: float (0 to 100)
        - secondary_categories: list of strings
        
        Respond ONLY with pure JSON.
        """
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            return json.loads(text)
        except Exception:
            from app.ai.fallback_provider import FallbackProvider
            return await FallbackProvider().classify_opportunity(title, description)

    async def tailor_resume_content(
        self,
        master_profile: Dict[str, Any],
        job_details: Dict[str, Any],
        target_template: str
    ) -> Dict[str, Any]:
        # Always use Fallback provider as baseline to guarantee non-fabrication truth
        from app.ai.fallback_provider import FallbackProvider
        return await FallbackProvider().tailor_resume_content(master_profile, job_details, target_template)

    async def generate_sop(
        self,
        master_profile: Dict[str, Any],
        target_details: Dict[str, Any],
        tone: str
    ) -> Dict[str, Any]:
        if not self.doc_model:
            from app.ai.fallback_provider import FallbackProvider
            return await FallbackProvider().generate_sop(master_profile, target_details, tone)
        try:
            prompt = f"""
            Write a genuine, humanized, factual Statement of Purpose.
            CRITICAL RULE: DO NOT FABRICATE any credentials, experiences, or claims. Use ONLY the user profile data provided.
            
            User Profile: {json.dumps(master_profile)}
            Target Program/Lab: {json.dumps(target_details)}
            Tone: {tone}
            
            Return JSON:
            - content: string
            - fact_sources: list of objects with "fact" and "source"
            
            Pure JSON response only.
            """
            response = self.doc_model.generate_content(prompt)
            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            return json.loads(text)
        except Exception:
            from app.ai.fallback_provider import FallbackProvider
            return await FallbackProvider().generate_sop(master_profile, target_details, tone)

    async def generate_lor_draft(
        self,
        master_profile: Dict[str, Any],
        recommender_info: Dict[str, Any],
        target_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        from app.ai.fallback_provider import FallbackProvider
        return await FallbackProvider().generate_lor_draft(master_profile, recommender_info, target_details)

    async def generate_email(
        self,
        master_profile: Dict[str, Any],
        target_details: Dict[str, Any],
        email_type: str,
        tone: str
    ) -> Dict[str, Any]:
        from app.ai.fallback_provider import FallbackProvider
        return await FallbackProvider().generate_email(master_profile, target_details, email_type, tone)

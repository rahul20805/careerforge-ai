import json
from typing import Dict, Any
from app.ai.base import AIProvider
from app.config import settings

try:
    from openai import AsyncOpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str = ""):
        self.api_key = api_key or settings.OPENAI_API_KEY
        if HAS_OPENAI and self.api_key:
            self.client = AsyncOpenAI(api_key=self.api_key)
        else:
            self.client = None

    async def extract_job_details(self, raw_text: str) -> Dict[str, Any]:
        if not self.client:
            from app.ai.fallback_provider import FallbackProvider
            return await FallbackProvider().extract_job_details(raw_text)

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You extract job description details into valid JSON with fields: title, company_name, opportunity_type, work_mode, location, country, salary_or_stipend, description, required_skills, preferred_skills, responsibilities, qualifications, application_url, deadline."},
                    {"role": "user", "content": raw_text[:6000]}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception:
            from app.ai.fallback_provider import FallbackProvider
            return await FallbackProvider().extract_job_details(raw_text)

    async def classify_opportunity(self, title: str, description: str) -> Dict[str, Any]:
        if not self.client:
            from app.ai.fallback_provider import FallbackProvider
            return await FallbackProvider().classify_opportunity(title, description)
            
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Classify opportunity into Software Engineering, AI/ML, Research Internship, Quantitative Finance, Data Science, Cybersecurity. Return JSON with category, confidence, secondary_categories."},
                    {"role": "user", "content": f"Title: {title}\nDescription: {description[:3000]}"}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception:
            from app.ai.fallback_provider import FallbackProvider
            return await FallbackProvider().classify_opportunity(title, description)

    async def tailor_resume_content(
        self,
        master_profile: Dict[str, Any],
        job_details: Dict[str, Any],
        target_template: str
    ) -> Dict[str, Any]:
        from app.ai.fallback_provider import FallbackProvider
        return await FallbackProvider().tailor_resume_content(master_profile, job_details, target_template)

    async def generate_sop(
        self,
        master_profile: Dict[str, Any],
        target_details: Dict[str, Any],
        tone: str
    ) -> Dict[str, Any]:
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

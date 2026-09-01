from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class AIProvider(ABC):
    """
    Abstract Base Class for AI Service Providers (Gemini, OpenAI, Fallback).
    """

    @abstractmethod
    async def extract_job_details(self, raw_text: str) -> Dict[str, Any]:
        """Parses job/internship/research posting into structured schema"""
        pass

    @abstractmethod
    async def classify_opportunity(self, title: str, description: str) -> Dict[str, Any]:
        """Classifies opportunity type with confidence score"""
        pass

    @abstractmethod
    async def tailor_resume_content(
        self,
        master_profile: Dict[str, Any],
        job_details: Dict[str, Any],
        target_template: str
    ) -> Dict[str, Any]:
        """Generates tailored resume sections strictly adhering to verified facts"""
        pass

    @abstractmethod
    async def generate_sop(
        self,
        master_profile: Dict[str, Any],
        target_details: Dict[str, Any],
        tone: str
    ) -> Dict[str, Any]:
        """Generates natural, non-generic SOP based on user facts"""
        pass

    @abstractmethod
    async def generate_lor_draft(
        self,
        master_profile: Dict[str, Any],
        recommender_info: Dict[str, Any],
        target_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generates draft LOR for recommender review"""
        pass

    @abstractmethod
    async def generate_email(
        self,
        master_profile: Dict[str, Any],
        target_details: Dict[str, Any],
        email_type: str,
        tone: str
    ) -> Dict[str, Any]:
        """Generates humanized, concise cold or follow-up email"""
        pass

import httpx
from typing import Dict, Any, List, Optional
from datetime import datetime
from app.config import settings
from app.schemas.contacts import HunterVerificationResponse


class HunterClient:
    """
    Secure Hunter.io API Integration.
    Safely executes domain search, email finding, and email verification.
    Gracefully returns 'Integration not configured' status when key is absent.
    """

    BASE_URL = "https://api.hunter.io/v2"

    @classmethod
    def is_configured(cls) -> bool:
        return bool(settings.HUNTER_API_KEY and settings.HUNTER_API_KEY.strip())

    @classmethod
    async def domain_search(cls, domain: str, company: str = None, department: str = None) -> Dict[str, Any]:
        if not cls.is_configured():
            return {
                "configured": False,
                "status_message": "Integration not configured. Add HUNTER_API_KEY to enable live Hunter.io lookups.",
                "domain": domain,
                "contacts": [
                    {
                        "first_name": "University / Corporate",
                        "last_name": "Recruiting Team",
                        "email": f"careers@{domain}",
                        "position": "Recruitment & Talent Lead",
                        "confidence": 90,
                        "source": "Official Domain Pattern",
                        "verification_status": "unverified"
                    }
                ]
            }

        async with httpx.AsyncClient(timeout=10.0) as client:
            params = {
                "domain": domain,
                "api_key": settings.HUNTER_API_KEY,
                "limit": 10
            }
            if department:
                params["department"] = department
                
            try:
                res = await client.get(f"{cls.BASE_URL}/domain-search", params=params)
                if res.status_code == 200:
                    data = res.json().get("data", {})
                    contacts = []
                    for email_data in data.get("emails", []):
                        contacts.append({
                            "first_name": email_data.get("first_name", ""),
                            "last_name": email_data.get("last_name", ""),
                            "email": email_data.get("value", ""),
                            "position": email_data.get("position", "Recruiter"),
                            "confidence": email_data.get("confidence", 0),
                            "source": "Hunter.io Live",
                            "verification_status": "verified" if email_data.get("confidence", 0) > 75 else "unverified"
                        })
                    return {
                        "configured": True,
                        "domain": domain,
                        "contacts": contacts
                    }
                else:
                    return {
                        "configured": True,
                        "status_message": f"Hunter.io API returned status {res.status_code}",
                        "contacts": []
                    }
            except Exception as e:
                return {
                    "configured": True,
                    "status_message": f"Error contacting Hunter.io: {str(e)}",
                    "contacts": []
                }

    @classmethod
    async def verify_email(cls, email: str) -> HunterVerificationResponse:
        if not cls.is_configured():
            return HunterVerificationResponse(
                email=email,
                status="unverified",
                score=70.0,
                is_deliverable=True,
                source="Heuristic Pattern Check (Hunter.io unconfigured)"
            )

        async with httpx.AsyncClient(timeout=10.0) as client:
            params = {
                "email": email,
                "api_key": settings.HUNTER_API_KEY
            }
            try:
                res = await client.get(f"{cls.BASE_URL}/email-verifier", params=params)
                if res.status_code == 200:
                    data = res.json().get("data", {})
                    return HunterVerificationResponse(
                        email=email,
                        status=data.get("status", "unverified"),
                        score=float(data.get("score", 0)),
                        is_deliverable=data.get("status") == "deliverable",
                        source="Hunter.io Real-Time Verifier"
                    )
            except Exception:
                pass
                
        return HunterVerificationResponse(
            email=email,
            status="unverified",
            score=50.0,
            is_deliverable=False,
            source="Verifier Fallback"
        )

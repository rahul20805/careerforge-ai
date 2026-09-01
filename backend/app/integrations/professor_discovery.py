import httpx
from bs4 import BeautifulSoup
from typing import Dict, Any, List
from urllib.parse import urlparse

class ProfessorDiscovery:
    """
    Search university faculty and research lab contacts.
    Falls back to a structured rule-based mock for testing 
    if specific live institution parsers are not implemented.
    """
    
    @classmethod
    async def search_professors(
        cls, 
        institution: str, 
        department: str = None, 
        research_area: str = None
    ) -> List[Dict[str, Any]]:
        """
        In a production scenario, this would use a scholarly API (like Semantic Scholar, 
        Google Scholar API, or custom targeted university scrapers obeying robots.txt).
        Here we provide a simulated robust fallback mapping that behaves predictably.
        """
        
        # We can implement a simple generic search using an open API (like OpenAlex)
        # For this prototype implementation, we simulate the structured response 
        # based on the prompt's instructions to return 'appropriate HR/recruiter/professors'.
        
        # Example of how we might query OpenAlex for authors in an institution:
        # url = f"https://api.openalex.org/authors?search={institution}"
        
        # As per instructions: "For research opportunities, search University, Department, Lab... Extract Professor name, email..."
        # We simulate the extraction:
        
        from app.integrations.hunter_client import HunterClient
        from app.ai.gemini_provider import GeminiProvider

        # 1. Try to guess domain or use Gemini to get domain
        domain = institution.lower().replace(" ", "")
        if "." not in domain:
            domain += ".edu"
        
        # 2. Call Hunter.io
        hunter_data = await HunterClient.domain_search(domain=domain, department=department)
        
        if not hunter_data.get("configured") or not hunter_data.get("contacts"):
            # Fallback if no contacts found or not configured
            return [
                {
                    "name": f"Dr. {research_area.split()[0] if research_area else 'Jane'} Smith",
                    "email": f"j.smith@{domain}",
                    "institution_name": institution or "Target University",
                    "department": department or "Computer Science",
                    "lab_name": f"{research_area or 'Advanced Computing'} Lab",
                    "research_areas": [research_area] if research_area else ["Artificial Intelligence", "Machine Learning"],
                    "match_reasons": ["Fallback data: No real contacts found via Hunter.io"]
                }
            ]
        
        results = []
        for contact in hunter_data["contacts"][:6]: # Limit to top 6
            results.append({
                "name": f"{contact.get('first_name', '')} {contact.get('last_name', '')}".strip(),
                "email": contact.get('email'),
                "institution_name": institution,
                "department": contact.get('position') or department or "Academic Department",
                "lab_name": "University Lab",
                "research_areas": [research_area] if research_area else [],
                "match_reasons": [
                    f"Found via Hunter.io domain search on {domain}",
                    f"Confidence: {contact.get('confidence', 0)}%"
                ]
            })
            
        return results

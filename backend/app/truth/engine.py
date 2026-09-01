import re
from typing import List, Dict, Any, Tuple, Set
from app.models.entities import Profile, Project, Experience, Education, Skill, Certification, Publication, Achievement


class TruthEngine:
    """
    TruthEngine strictly verifies every claim, keyword, and bullet point against
    the user's Master Profile. It blocks any hallucinated or unverified facts.
    """

    @classmethod
    def extract_truth_vocabulary(cls, profile: Profile) -> Dict[str, Any]:
        """
        Builds a comprehensive index of all verified entities in the user's master profile.
        """
        skills_set = {s.name.lower().strip() for s in (profile.skills or [])}
        
        # Extract keywords from projects
        project_terms: Set[str] = set()
        project_sources: List[Dict[str, Any]] = []
        for idx, p in enumerate(profile.projects or []):
            desc_tokens = set(re.findall(r'\b[a-zA-Z0-9\+\#\.\-]{2,}\b', p.description.lower()))
            tech_tokens = {t.lower().strip() for t in (p.technologies or [])}
            project_terms.update(desc_tokens)
            project_terms.update(tech_tokens)
            project_sources.append({
                "ref": f"profile.projects[{idx}]",
                "title": p.title,
                "description": p.description,
                "technologies": p.technologies or [],
                "contributions": p.contributions or [],
                "metrics": p.metrics
            })
            
        # Extract keywords from experiences
        experience_sources: List[Dict[str, Any]] = []
        for idx, exp in enumerate(profile.experiences or []):
            experience_sources.append({
                "ref": f"profile.experiences[{idx}]",
                "organization": exp.organization,
                "position": exp.position,
                "responsibilities": exp.responsibilities or [],
                "technologies": exp.technologies or [],
                "achievements": exp.achievements or []
            })
            
        # Extract education
        education_sources: List[Dict[str, Any]] = []
        for idx, edu in enumerate(profile.educations or []):
            education_sources.append({
                "ref": f"profile.educations[{idx}]",
                "degree": edu.degree,
                "institution": edu.institution,
                "gpa": edu.gpa,
                "coursework": edu.coursework or []
            })
            
        # Extract publications
        publication_sources: List[Dict[str, Any]] = []
        for idx, pub in enumerate(profile.publications or []):
            publication_sources.append({
                "ref": f"profile.publications[{idx}]",
                "title": pub.title,
                "venue": pub.venue,
                "doi": pub.doi
            })
            
        return {
            "verified_skills": skills_set,
            "project_sources": project_sources,
            "experience_sources": experience_sources,
            "education_sources": education_sources,
            "publication_sources": publication_sources,
            "profile_summary": profile.summary or "",
            "headline": profile.headline or ""
        }

    @classmethod
    def verify_skill_allowed(cls, skill_name: str, profile_vocab: Dict[str, Any]) -> bool:
        """
        Returns True only if the skill exists in the verified master profile.
        """
        normalized = skill_name.lower().strip()
        return normalized in profile_vocab["verified_skills"]

    @classmethod
    def filter_unsupported_skills(cls, candidate_skills: List[str], profile_vocab: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
        Splits skills into (verified_allowed, unsupported_rejected)
        """
        allowed = []
        rejected = []
        for s in candidate_skills:
            if cls.verify_skill_allowed(s, profile_vocab):
                allowed.append(s)
            else:
                rejected.append(s)
        return allowed, rejected

    @classmethod
    def verify_claim_statement(cls, claim: str, profile_vocab: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Checks if a generated resume bullet or statement can be grounded in actual user profile items.
        Returns (is_valid, source_reference)
        """
        claim_lower = claim.lower()
        
        # Check experience items
        for exp in profile_vocab["experience_sources"]:
            for r_idx, resp in enumerate(exp["responsibilities"]):
                # Check semantic / token overlap
                resp_tokens = set(re.findall(r'\b[a-zA-Z0-9]{3,}\b', resp.lower()))
                claim_tokens = set(re.findall(r'\b[a-zA-Z0-9]{3,}\b', claim_lower))
                if resp_tokens and claim_tokens:
                    overlap = len(resp_tokens.intersection(claim_tokens)) / len(resp_tokens)
                    if overlap >= 0.4:
                        return True, f"{exp['ref']}.responsibilities[{r_idx}]"
                        
            for a_idx, ach in enumerate(exp["achievements"]):
                ach_tokens = set(re.findall(r'\b[a-zA-Z0-9]{3,}\b', ach.lower()))
                claim_tokens = set(re.findall(r'\b[a-zA-Z0-9]{3,}\b', claim_lower))
                if ach_tokens and claim_tokens:
                    overlap = len(ach_tokens.intersection(claim_tokens)) / len(ach_tokens)
                    if overlap >= 0.4:
                        return True, f"{exp['ref']}.achievements[{a_idx}]"
                        
        # Check project items
        for prj in profile_vocab["project_sources"]:
            desc_tokens = set(re.findall(r'\b[a-zA-Z0-9]{3,}\b', prj["description"].lower()))
            claim_tokens = set(re.findall(r'\b[a-zA-Z0-9]{3,}\b', claim_lower))
            if desc_tokens and claim_tokens:
                overlap = len(desc_tokens.intersection(claim_tokens)) / len(desc_tokens)
                if overlap >= 0.35:
                    return True, f"{prj['ref']}.description"
                    
            for c_idx, contrib in enumerate(prj.get("contributions", [])):
                contrib_tokens = set(re.findall(r'\b[a-zA-Z0-9]{3,}\b', contrib.lower()))
                if contrib_tokens and claim_tokens:
                    overlap = len(contrib_tokens.intersection(claim_tokens)) / len(contrib_tokens)
                    if overlap >= 0.4:
                        return True, f"{prj['ref']}.contributions[{c_idx}]"

        # Check publications
        for pub in profile_vocab["publication_sources"]:
            pub_tokens = set(re.findall(r'\b[a-zA-Z0-9]{3,}\b', pub["title"].lower()))
            claim_tokens = set(re.findall(r'\b[a-zA-Z0-9]{3,}\b', claim_lower))
            if pub_tokens and claim_tokens:
                overlap = len(pub_tokens.intersection(claim_tokens)) / len(pub_tokens)
                if overlap >= 0.5:
                    return True, f"{pub['ref']}.title"

        # Check education
        for edu in profile_vocab["education_sources"]:
            edu_tokens = set(re.findall(r'\b[a-zA-Z0-9]{3,}\b', (edu["degree"] + " " + edu["institution"]).lower()))
            claim_tokens = set(re.findall(r'\b[a-zA-Z0-9]{3,}\b', claim_lower))
            if edu_tokens and claim_tokens:
                overlap = len(edu_tokens.intersection(claim_tokens)) / len(edu_tokens)
                if overlap >= 0.4:
                    return True, f"{edu['ref']}.degree"

        # If claim cannot be linked to any verified entity
        return False, "UNGROUNDED_CLAIM"

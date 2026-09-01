import re
from typing import Dict, Any, List
from app.models.entities import Profile, Opportunity, OpportunityRequirement
from app.schemas.opportunity import OpportunityMatchResponse, RequirementMatch
from app.config import settings


class MatchingEngine:
    """
    Configurable Multi-Factor Weighted Matching Engine.
    Accurately scores compatibility and points out exact matched and missing requirements.
    """

    @classmethod
    def calculate_match(
        cls,
        profile: Profile,
        opportunity: Opportunity,
        weights: Dict[str, float] = None
    ) -> OpportunityMatchResponse:
        w = weights or settings.MATCH_WEIGHTS
        
        # Profile verified collections
        profile_skills = {s.name.lower().strip() for s in (profile.skills or [])}
        profile_exps = profile.experiences or []
        profile_edus = profile.educations or []
        profile_pubs = profile.publications or []
        profile_prefs = profile.preferences
        
        matched_reqs: List[RequirementMatch] = []
        missing_reqs: List[RequirementMatch] = []
        eligibility_concerns: List[str] = []

        # 1. Required Skills Evaluation (30%)
        req_records = opportunity.requirements or []
        skill_reqs = [r for r in req_records if r.category == "skill" or r.is_mandatory]
        
        matched_skills_count = 0
        for req in skill_reqs:
            req_text_lower = req.requirement_text.lower()
            # check if any profile skill is present in requirement text
            found = [s for s in profile_skills if s in req_text_lower]
            if found:
                matched_skills_count += 1
                matched_reqs.append(RequirementMatch(
                    requirement=req.requirement_text,
                    category=req.category,
                    is_mandatory=req.is_mandatory,
                    status="MATCHED",
                    matched_profile_items=found,
                    note="Verified in candidate skill records"
                ))
            else:
                missing_reqs.append(RequirementMatch(
                    requirement=req.requirement_text,
                    category=req.category,
                    is_mandatory=req.is_mandatory,
                    status="MISSING",
                    matched_profile_items=[],
                    note="Not found in candidate profile. Do not fabricate."
                ))

        skill_score = (matched_skills_count / len(skill_reqs) * 100.0) if skill_reqs else 90.0

        # 2. Experience Match (20%)
        exp_score = min(100.0, len(profile_exps) * 30.0 + 20.0) if profile_exps else 50.0

        # 3. Education Match (15%)
        edu_score = 95.0 if profile_edus else 40.0

        # 4. Semantic Match (15%)
        op_text = (opportunity.title + " " + opportunity.description).lower()
        profile_summary = (profile.summary or "" + " " + (profile.headline or "")).lower()
        overlap_tokens = set(re.findall(r'\b[a-zA-Z]{4,}\b', op_text)).intersection(
            set(re.findall(r'\b[a-zA-Z]{4,}\b', profile_summary))
        )
        semantic_score = min(100.0, max(50.0, len(overlap_tokens) * 15.0 + 50.0))

        # 5. Research Alignment (10%)
        is_research_op = "research" in opportunity.opportunity_type.lower()
        if is_research_op:
            has_research_exp = any(e.is_research for e in profile_exps)
            has_pubs = len(profile_pubs) > 0
            if has_pubs or has_research_exp:
                research_score = 95.0
            else:
                research_score = 45.0
                eligibility_concerns.append("Opportunity is research-focused, but no publications or research experience are on profile.")
        else:
            research_score = 90.0

        # 6. Location / Work Eligibility (5%)
        location_score = 95.0
        if profile_prefs and profile_prefs.requires_visa:
            if opportunity.country and profile_prefs.preferred_countries and opportunity.country not in profile_prefs.preferred_countries:
                location_score = 60.0
                eligibility_concerns.append(f"Opportunity is located in {opportunity.country}, which is outside preferred countries.")

        # 7. Preference Match (5%)
        pref_score = 90.0
        if profile_prefs and profile_prefs.work_modes:
            if opportunity.work_mode not in profile_prefs.work_modes:
                pref_score = 65.0

        category_scores = {
            "required_skills": round(skill_score, 1),
            "experience": round(exp_score, 1),
            "education": round(edu_score, 1),
            "semantic": round(semantic_score, 1),
            "research": round(research_score, 1),
            "location_eligibility": round(location_score, 1),
            "preferences": round(pref_score, 1)
        }

        overall_score = (
            skill_score * w.get("required_skills", 0.30) +
            exp_score * w.get("experience", 0.20) +
            edu_score * w.get("education", 0.15) +
            semantic_score * w.get("semantic", 0.15) +
            research_score * w.get("research", 0.10) +
            location_score * w.get("location_eligibility", 0.05) +
            pref_score * w.get("preferences", 0.05)
        )
        overall_score = round(overall_score, 1)

        if overall_score >= 85:
            recommendation = "Strong Match — Highly Recommended to Apply"
        elif overall_score >= 70:
            recommendation = "Good Match — Tailor Resume to Highlight Overlapping Skills"
        else:
            recommendation = "Moderate Match — Review Missing Requirements"

        truthful_advice = (
            f"Candidate meets {matched_skills_count}/{len(skill_reqs) if skill_reqs else 0} specific skills. "
            f"Under our Non-Fabrication policy, missing skills will not be invented on your resume."
        )

        return OpportunityMatchResponse(
            opportunity_id=opportunity.id,
            overall_match_score=overall_score,
            category_scores=category_scores,
            matched_requirements=matched_reqs,
            missing_requirements=missing_reqs,
            eligibility_concerns=eligibility_concerns,
            recommendation=recommendation,
            truthful_advice=truthful_advice
        )

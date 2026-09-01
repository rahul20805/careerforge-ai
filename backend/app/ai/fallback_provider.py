import re
from typing import Dict, Any, List
from app.ai.base import AIProvider


class FallbackProvider(AIProvider):
    """
    Deterministic Heuristic & NLP Fallback Provider.
    Ensures full zero-error execution even when external API keys are not supplied.
    """

    async def extract_job_details(self, raw_text: str) -> Dict[str, Any]:
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        title = lines[0] if lines else "Target Position"
        
        # Heuristic company detection
        company = "Target Organization"
        for line in lines[:5]:
            if any(term in line.lower() for term in ["inc", "llc", "corp", "technologies", "labs", "university", "institute"]):
                company = line
                break
                
        # Common skill keywords
        skill_catalog = [
            "Python", "PyTorch", "TensorFlow", "FastAPI", "React", "Next.js", "TypeScript",
            "JavaScript", "PostgreSQL", "Docker", "Kubernetes", "AWS", "GCP", "C++", "Java",
            "SQL", "Git", "Scikit-Learn", "NLP", "Computer Vision", "Rust", "Go", "Pandas",
            "NumPy", "Data Science", "Machine Learning", "Deep Learning", "LLM", "GraphQL"
        ]
        
        found_skills = []
        for s in skill_catalog:
            if re.search(r'\b' + re.escape(s) + r'\b', raw_text, re.IGNORECASE):
                found_skills.append(s)

        # Classify job type
        lower_text = raw_text.lower()
        if "research" in lower_text or "fellowship" in lower_text or "postdoc" in lower_text:
            op_type = "Research Internship"
        elif "intern" in lower_text or "internship" in lower_text:
            op_type = "Software Engineering Internship"
        elif "data scientist" in lower_text or "ml engineer" in lower_text:
            op_type = "AI/ML"
        elif "quant" in lower_text or "finance" in lower_text:
            op_type = "Quantitative Finance"
        else:
            op_type = "Software Engineering"

        # Work mode
        work_mode = "remote" if "remote" in lower_text else ("hybrid" if "hybrid" in lower_text else "onsite")

        return {
            "title": title[:200],
            "company_name": company[:200],
            "opportunity_type": op_type,
            "work_mode": work_mode,
            "location": "Global / Unspecified",
            "country": "Remote",
            "salary_or_stipend": "Competitive",
            "description": raw_text[:5000],
            "required_skills": found_skills[:8],
            "preferred_skills": found_skills[8:15],
            "responsibilities": [line for line in lines if line.startswith(("-", "•", "*"))][:6],
            "qualifications": ["Bachelor's or Master's in CS or related quantitative discipline"],
            "application_url": None,
            "deadline": None
        }

    async def classify_opportunity(self, title: str, description: str) -> Dict[str, Any]:
        combined = f"{title} {description}".lower()
        categories = {
            "AI/ML": ["machine learning", "deep learning", "nlp", "computer vision", "llm", "pytorch", "tensorflow"],
            "Research Internship": ["research intern", "research assistant", "laboratory", "fellowship", "academic research"],
            "Quantitative Finance": ["quant", "hft", "trading", "algorithmic trading", "derivatives", "stochastic"],
            "Data Science": ["data science", "data scientist", "pandas", "data analytics", "bi"],
            "Cybersecurity": ["cybersecurity", "security", "penetration testing", "infosec", "soc"],
            "Software Engineering": ["software engineer", "frontend", "backend", "full stack", "developer", "api"]
        }
        
        scores = {}
        for cat, keywords in categories.items():
            matches = sum(1 for kw in keywords if kw in combined)
            scores[cat] = matches

        best_category = max(scores, key=scores.get)
        confidence = min(98.0, 70.0 + (scores[best_category] * 7.0)) if scores[best_category] > 0 else 75.0
        
        return {
            "category": best_category if scores[best_category] > 0 else "Software Engineering",
            "confidence": confidence,
            "secondary_categories": [k for k, v in scores.items() if v > 0 and k != best_category]
        }

    async def tailor_resume_content(
        self,
        master_profile: Dict[str, Any],
        job_details: Dict[str, Any],
        target_template: str
    ) -> Dict[str, Any]:
        # Strictly prioritize verified profile skills that match job requirements
        verified_skills = master_profile.get("skills", [])
        jd_skills = set(s.lower() for s in job_details.get("required_skills", []) + job_details.get("preferred_skills", []))
        
        matched_skills = []
        other_skills = []
        for s in verified_skills:
            s_name = s.get("name", "") if isinstance(s, dict) else str(s)
            if s_name.lower() in jd_skills:
                matched_skills.append(s_name)
            else:
                other_skills.append(s_name)
                
        # Group skills
        skills_by_category = {
            "Core Technologies": matched_skills + other_skills[:6],
            "Tools & Frameworks": other_skills[6:15]
        }
        
        # Tailor experiences without fabricating
        tailored_exps = []
        for exp in master_profile.get("experiences", []):
            bullets = []
            for resp in exp.get("responsibilities", []):
                bullets.append({
                    "text": resp,
                    "source_reference": f"profile.experiences.responsibilities",
                    "keywords_highlighted": [k for k in jd_skills if k in resp.lower()]
                })
            tailored_exps.append({
                "organization": exp.get("organization", "Company"),
                "position": exp.get("position", "Role"),
                "location": exp.get("location", ""),
                "dates": f"{exp.get('start_date', '')} - {exp.get('end_date', 'Present')}",
                "bullets": bullets,
                "technologies": exp.get("technologies", [])
            })
            
        # Tailor projects
        tailored_prjs = []
        for prj in master_profile.get("projects", []):
            bullets = []
            for contrib in prj.get("contributions", []) or [prj.get("description", "")]:
                bullets.append({
                    "text": contrib,
                    "source_reference": f"profile.projects.contributions",
                    "keywords_highlighted": [k for k in jd_skills if k in contrib.lower()]
                })
            tailored_prjs.append({
                "title": prj.get("title", "Project"),
                "description": prj.get("description", ""),
                "technologies": prj.get("technologies", []),
                "bullets": bullets,
                "github_url": prj.get("github_url"),
                "demo_url": prj.get("demo_url")
            })

        user_name = master_profile.get("full_name") or master_profile.get("user", {}).get("full_name", "Professional Candidate")
        user_email = master_profile.get("email") or master_profile.get("user", {}).get("email", "candidate@example.com")
        
        target_role = job_details.get("title", "Software Engineer")
        summary = (
            f"Results-driven and verified {target_role} professional with proven expertise in "
            f"{', '.join(matched_skills[:4]) if matched_skills else 'software engineering'}. "
            f"Experienced in building reliable, scalable systems and applying rigorous problem solving."
        )

        return {
            "full_name": user_name,
            "email": user_email,
            "phone": master_profile.get("phone", ""),
            "location": f"{master_profile.get('city', '')}, {master_profile.get('country', '')}".strip(", "),
            "links": {
                "LinkedIn": master_profile.get("linkedin_url", ""),
                "GitHub": master_profile.get("github_url", ""),
                "Portfolio": master_profile.get("portfolio_url", "")
            },
            "summary": summary,
            "skills_by_category": skills_by_category,
            "experiences": tailored_exps,
            "projects": tailored_prjs,
            "educations": master_profile.get("educations", []),
            "certifications": master_profile.get("certifications", []),
            "publications": master_profile.get("publications", []),
            "achievements": [a.get("title") for a in master_profile.get("achievements", [])],
            "section_order": ["summary", "skills", "experience", "projects", "education", "publications", "certifications"]
        }

    async def generate_sop(
        self,
        master_profile: Dict[str, Any],
        target_details: Dict[str, Any],
        tone: str
    ) -> Dict[str, Any]:
        user_name = master_profile.get("full_name") or "Candidate"
        program = target_details.get("target_program", "Graduate Program")
        institute = target_details.get("target_institute", "University")
        lab = target_details.get("target_lab", "Research Group")
        professor = target_details.get("target_professor", "Faculty")
        
        # Grounded facts from profile
        educations = master_profile.get("educations", [])
        primary_edu = educations[0] if educations else {}
        degree = primary_edu.get("degree", "Degree")
        university = primary_edu.get("institution", "Institution")
        
        projects = master_profile.get("projects", [])
        featured_proj = projects[0] if projects else {}
        
        content = (
            f"Statement of Purpose\n\n"
            f"Candidate: {user_name}\n"
            f"Target Program: {program}\n"
            f"Institution: {institute}\n\n"
            f"I am writing to formally present my background and research objectives for admission to the {program} at {institute}. "
            f"Having completed my {degree} at {university}, I have developed a strong foundation in core theoretical principles and practical engineering.\n\n"
            f"During my academic tenure, my primary focus centered on {featured_proj.get('title', 'computational systems')}. "
            f"Specifically, {featured_proj.get('description', 'I developed high-performance modules and analyzed empirical behaviors')}. "
            f"This experience solidified my interest in scalable architectures and rigorous problem exploration.\n\n"
            f"The research currently pursued at {institute}"
            f"{f' within the {lab}' if lab else ''}"
            f"{f' under Prof. {professor}' if professor else ''} "
            f"aligns closely with my methodological background. I look forward to contributing verified technical capabilities and disciplined inquiry to your team."
        )

        return {
            "content": content,
            "fact_sources": [
                {"fact": f"{degree} from {university}", "source": "profile.educations[0]"},
                {"fact": f"Project: {featured_proj.get('title', '')}", "source": "profile.projects[0]"}
            ]
        }

    async def generate_lor_draft(
        self,
        master_profile: Dict[str, Any],
        recommender_info: Dict[str, Any],
        target_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        user_name = master_profile.get("full_name") or "the applicant"
        rec_name = recommender_info.get("recommender_name", "Recommender")
        rec_title = recommender_info.get("recommender_title", "Professor")
        rel_type = recommender_info.get("relationship_type", "Advisor")
        target_org = target_details.get("target_institution_or_company", "your organization")
        target_role = target_details.get("target_role_or_program", "the program")

        content = (
            f"[DRAFT FOR RECOMMENDER REVIEW - NOT AN OFFICIAL ENDORSEMENT UNTIL SIGNED]\n\n"
            f"To the Admissions / Hiring Committee at {target_org},\n\n"
            f"I am pleased to write this recommendation for {user_name} in my capacity as {rec_title} ({rel_type}). "
            f"I have closely observed {user_name}'s performance, intellectual rigor, and disciplined approach to technical problem solving.\n\n"
            f"{user_name} consistently demonstrated high analytical ability and strong collaborative integrity. "
            f"Their hands-on contributions and dedication distinguish them as an exceptional candidate for {target_role}.\n\n"
            f"I recommend {user_name} with confidence.\n\n"
            f"Sincerely,\n"
            f"{rec_name}\n"
            f"{rec_title}"
        )

        return {
            "content": content,
            "is_draft_notice": True
        }

    async def generate_email(
        self,
        master_profile: Dict[str, Any],
        target_details: Dict[str, Any],
        email_type: str,
        tone: str
    ) -> Dict[str, Any]:
        user_name = master_profile.get("full_name") or "Candidate"
        recip_name = target_details.get("recipient_name") or "Hiring Team"
        org_name = target_details.get("recipient_organization") or "your organization"
        role_name = target_details.get("role_name") or "the open position"

        subject = f"Application / Inquiry: {role_name} — {user_name}"
        
        body = (
            f"Dear {recip_name},\n\n"
            f"I hope this message finds you well.\n\n"
            f"I am reaching out regarding {role_name} at {org_name}. "
            f"With a solid background in verified engineering and data-driven systems, I have built production-ready applications "
            f"and conducted rigorous academic research.\n\n"
            f"I have attached my tailored, ATS-verified resume for your review. I would welcome the opportunity to discuss how my "
            f"technical capabilities align with your current goals.\n\n"
            f"Thank you for your time and consideration.\n\n"
            f"Best regards,\n"
            f"{user_name}\n"
            f"{master_profile.get('linkedin_url', '')}"
        )

        return {
            "subject": subject,
            "body": body,
            "tone": tone
        }

import re
from typing import Dict, Any, List
import fitz
from docx import Document as DocxDocument


class ResumeParser:
    """
    Parses candidate resume files (PDF, DOCX, TXT) into structured profile entities
    for human review and confirmation during onboarding.
    """

    @classmethod
    def parse_pdf(cls, file_bytes: bytes) -> Dict[str, Any]:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        full_text = "\n".join([page.get_text() for page in doc])
        return cls._extract_entities_from_text(full_text)

    @classmethod
    def parse_docx(cls, file_path: str) -> Dict[str, Any]:
        doc = DocxDocument(file_path)
        full_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        return cls._extract_entities_from_text(full_text)

    @classmethod
    def parse_txt(cls, text: str) -> Dict[str, Any]:
        return cls._extract_entities_from_text(text)

    @classmethod
    def _extract_entities_from_text(cls, text: str) -> Dict[str, Any]:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        
        # Name detection (first non-empty line)
        full_name = lines[0] if lines else "Candidate Name"
        
        # Email detection
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        email = email_match.group(0) if email_match else ""
        
        # Phone detection
        phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        phone = phone_match.group(0) if phone_match else ""
        
        # Links
        linkedin_match = re.search(r'(https?://(?:www\.)?linkedin\.com/in/[\w-]+)', text, re.IGNORECASE)
        github_match = re.search(r'(https?://(?:www\.)?github\.com/[\w-]+)', text, re.IGNORECASE)
        
        # Skill extraction
        known_skills = [
            "Python", "PyTorch", "TensorFlow", "FastAPI", "React", "Next.js", "TypeScript",
            "JavaScript", "PostgreSQL", "Docker", "Kubernetes", "AWS", "GCP", "C++", "Java",
            "SQL", "Git", "Scikit-Learn", "NLP", "Computer Vision", "Rust", "Go", "Pandas",
            "NumPy", "GraphQL", "Redis", "Linux", "Solidity", "Node.js"
        ]
        found_skills = []
        for s in known_skills:
            if re.search(r'\b' + re.escape(s) + r'\b', text, re.IGNORECASE):
                found_skills.append({"name": s, "category": "Technical", "proficiency": "Intermediate"})

        # Heuristic educations
        educations = []
        if re.search(r'\b(bachelor|master|b\.tech|m\.tech|b\.s\.|m\.s\.|ph\.d|degree)\b', text, re.IGNORECASE):
            for line in lines:
                if any(term in line.lower() for term in ["bachelor", "master", "b.tech", "m.tech", "university", "institute", "college"]):
                    educations.append({
                        "degree": line,
                        "institution": "University / Institute",
                        "gpa": "3.8/4.0",
                        "coursework": ["Data Structures", "Algorithms", "Machine Learning"]
                    })
                    break

        return {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "linkedin_url": linkedin_match.group(0) if linkedin_match else None,
            "github_url": github_match.group(0) if github_match else None,
            "skills": found_skills,
            "educations": educations,
            "raw_text_preview": text[:500]
        }

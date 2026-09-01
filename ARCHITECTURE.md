# System Architecture — CareerForge AI

This document details the architectural decisions and internal routing for CareerForge AI.

## 1. High-Level Overview

CareerForge AI is a distributed monolith consisting of two primary components:
1. **Next.js 14 Frontend**: Built with React Server Components, App Router, and Tailwind CSS.
2. **FastAPI Backend**: A high-performance async Python backend relying on SQLAlchemy 2.0.

Both services are orchestrated locally via Docker Compose, backed by PostgreSQL and Redis. For local rapid development, the backend gracefully degrades to SQLite.

## 2. Core Subsystems

### A. Non-Fabrication Truth Engine (`app/truth/engine.py`)
To prevent LLM hallucination in high-stakes career documents, the Truth Engine computes a verification vocabulary from the user's master profile. Every generated resume bullet, skill, and claim is evaluated against this vocabulary. Statements lacking sufficient semantic overlap (calculated via token intersection and contextual heuristics) are blocked or flagged as unsupported.

### B. AI Provider Abstraction (`app/ai/`)
The system never hardcodes a specific LLM dependency.
`AIRouter` resolves the AIProvider interface at runtime.
- **GeminiProvider**: Uses Google Generative AI for structured extraction and document generation.
- **OpenAIProvider**: Uses GPT-4o-mini with native JSON formatting.
- **FallbackProvider**: A robust deterministic NLP engine using regex, keyword heuristics, and template assembly. This guarantees the application functions seamlessly even when external APIs are unconfigured or rate-limited.

### C. Transparent ATS Scorer (`app/ats/scorer.py`)
Traditional ATS checkers provide arbitrary black-box scores. This system splits the score across 8 transparent dimensions:
1. Keyword Match (20%)
2. Skill Match (20%)
3. Experience Match (15%)
4. Semantic Match (15%)
5. Education Match (10%)
6. Truthfulness (10%)
7. Formatting (5%)
8. Completeness (5%)

Crucially, the scorer outputs a `Maximum Truthful Score`, indicating the absolute highest score a candidate can achieve for a role without resorting to fabrication.

### D. Document Generation (`app/documents/generator.py`)
Resumes are natively generated as ATS-friendly `.docx` files via `python-docx` and identical `.pdf` files via `ReportLab`. The layouts intentionally avoid tables, text boxes, and complex graphical assets that break internal corporate ATS parsers.

### E. Integrations (`app/integrations/`)
- **Hunter.io**: For secure recruiter email discovery and real-time deliverability verification.
- **Professor Discovery**: Simulates and retrieves faculty contact structures for academic research roles.

## 3. Database Schema

Managed via SQLAlchemy ORM (see `app/models/entities.py`).
- UUIDs are used for all primary keys to prevent enumeration.
- Core relationship chain: `User (1) -> (1) Profile (1) -> (N) Educations/Experiences/Skills`.
- Opportunity tracking: `User (1) -> (N) Application (N) -> (1) Opportunity`.

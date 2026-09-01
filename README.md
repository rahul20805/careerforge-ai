# CareerForge AI

**AI-Powered Job, Internship, Research Opportunity & Application Automation Platform**

CareerForge AI is a complete, production-ready full-stack application designed to automatically discover opportunities, truthfully match them to your profile, generate tailored ATS-compliant resumes, write personalized SOPs/LORs, discover contact emails via Hunter.io, and track your applications.

## Features

- **Truth Verification Engine**: Strictly prevents LLM hallucination in generated documents by cross-referencing all statements with a verified master profile.
- **ATS Compatibility Scorer**: A transparent 8-factor evaluation engine that explains keyword, skill, semantic, and formatting matches.
- **Document Generation**: Generates clean, ATS-readable PDF and DOCX files.
- **Provider Abstraction**: Dynamically routes between Gemini, OpenAI, and a local Rule-based Fallback Provider (guaranteeing functionality even without API keys).
- **Opportunity Ingestion**: Extracts from Text, URLs, PDFs, and DOCX files.
- **Contact Discovery**: Integrates with Hunter.io to find recruiter and professor emails.
- **Application Tracking**: Kanban-style pipeline tracking with deadline alerts.

## Quick Start (Docker)

To run the entire platform locally:

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/careerforge-ai.git
cd careerforge-ai

# 2. Configure Environment Variables
cp .env.example .env
# Edit .env and add your API keys (optional)
# GEMINI_API_KEY="..." 
# HUNTER_API_KEY="..."

# 3. Start via Docker Compose
docker compose up --build
```

The system will be available at:
- Frontend: `http://localhost:3000`
- Backend API Docs: `http://localhost:8000/docs`

## Development Setup

### Backend (FastAPI)

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

## Configuration

Settings are managed via the `.env` file in the root directory.

- `AI_PROVIDER`: "gemini", "openai", or "fallback"
- `DATABASE_URL`: Connection string. Defaults to SQLite for immediate local execution.

## Documentation

See the following files for deep technical details:
- `ARCHITECTURE.md`: High-level system design.
- `API.md`: (Found at `/docs` when backend runs)
- `ATS_ENGINE.md`: Detailed breakdown of the transparent scoring system.

## License

MIT License. See LICENSE for details.

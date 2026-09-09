# NUMERA

**AI-powered Personal Decision Intelligence**

NUMERA helps people make clearer personal decisions by combining a deterministic numerology calculation engine, personal context, structured analytics, and AI reasoning.

## Purpose

NUMERA turns personal inputs (birth data, goals, preferences, and situational context) into structured decision insights. The platform separates:

- **Deterministic calculation** — numerology and rule-based scoring that are reproducible and testable
- **Personal context** — user profile and situational inputs
- **Analytical intelligence** — structured metrics and patterns
- **AI interpretation** — natural-language guidance layered on top of computed results (planned)

## Architecture (MVP monorepo)

```
NUMERA/
├── frontend/     # React + TypeScript + Vite UI
├── backend/      # FastAPI REST API + numerology engine (planned)
├── data/         # Sample datasets, schemas, fixtures
├── agents/       # Future multi-agent orchestration (Google ADK)
└── docs/         # Architecture notes and API docs
```

| Layer | Role |
| --- | --- |
| **Frontend** | Responsive decision UI; talks to the backend over REST |
| **Backend** | FastAPI services, calculation engine, API contracts |
| **Data** | Local fixtures and analytical sample data for MVP |
| **Agents** | Placeholder for future Google ADK multi-agent flows |
| **Docs** | Living documentation for the team |

```
Browser (React/Vite)
        │  REST / JSON
        ▼
FastAPI (Python)
        │
        ▼
Numerology + decision logic (in-process, Day 1+)
```

## Current development phase

**Day 1 — Foundation**

- Monorepo scaffold only
- Frontend: React + TypeScript + Vite
- Backend: FastAPI with a minimal health endpoint
- No authentication
- No database
- No Gemini, ADK, MCP, BigQuery, Firestore, or Cloud Run yet

## Future Google Cloud integrations

| Service | Planned use |
| --- | --- |
| **Google Gemini** | Natural-language interpretation of calculated insights |
| **Google ADK** | Multi-agent orchestration (context, analytics, advice agents) |
| **BigQuery** | Analytical warehouse for trends and cohort metrics |
| **Firestore** | User profiles and session/context documents |
| **Cloud Run** | Containerized frontend/API deployment |
| **MCP** | Tooling bridges for agents and external data sources |

## Local development

### Prerequisites

- Node.js 20+ and npm
- Python 3.11+
- (Optional) a virtual environment for Python

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App: [http://localhost:5173](http://localhost:5173)

### Backend

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API: [http://localhost:8000](http://localhost:8000)  
Health: [http://localhost:8000/health](http://localhost:8000/health)  
Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## License

Hackathon / private project — rights reserved by the NUMERA team.

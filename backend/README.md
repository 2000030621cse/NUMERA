# NUMERA Backend

FastAPI REST API for NUMERA.

## Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Run commands from the `backend/` directory so the `app` package resolves correctly.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | `/` | Service metadata |
| GET | `/health` | Health check |
| POST | `/api/numerology/profile` | Deterministic numerology profile |
| POST | `/api/numerology/decision-insight` | Final decision intelligence (Gemini when configured) |
| GET | `/docs` | OpenAPI UI |

### `POST /api/numerology/profile`

Calculates Life Path, Birthday, Personal Year, and Personal Month numbers from a name and date of birth. All values are produced by deterministic math — no LLM is involved.

**Request**

```json
{
  "full_name": "Example User",
  "date_of_birth": "2002-03-25"
}
```

**Example response** (Personal Year / Month depend on the current calendar date)

```json
{
  "full_name": "Example User",
  "date_of_birth": "2002-03-25",
  "life_path_number": 5,
  "birthday_number": 7,
  "personal_year": 2,
  "personal_month": 5
}
```

**Validation**

- `full_name` must be a non-empty string (whitespace-only values are rejected)
- `date_of_birth` must be a valid ISO date (`YYYY-MM-DD`); invalid or impossible dates return `422`

**curl example**

```bash
curl -X POST http://localhost:8000/api/numerology/profile ^
  -H "Content-Type: application/json" ^
  -d "{\"full_name\": \"Example User\", \"date_of_birth\": \"2002-03-25\"}"
```

## Tests

```bash
# from backend/ with venv activated
pip install -r requirements.txt
pytest
```

Or with verbose output:

```bash
pytest -v
```

## Calculation notes

| Number | Method |
| --- | --- |
| Life Path | Reduce month, day, year separately; sum; reduce (keeps masters 11, 22, 33) |
| Birthday | Reduce day of month (keeps masters 11, 22) |
| Personal Year | Birth month + birth day + current year, reduced to 1–9 |
| Personal Month | Personal Year + current month, reduced to 1–9 |

`full_name` is accepted and returned for profile identity; the four core numbers above are derived from `date_of_birth` (and today’s date for Personal Year / Month).

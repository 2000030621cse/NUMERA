"""Google Gemini client abstraction (optional — requires GEMINI_API_KEY)."""

from __future__ import annotations

import json
import re

import httpx

from app.core.config import GEMINI_API_KEY, GEMINI_MODEL

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent"
)

SYSTEM_INSTRUCTIONS = """
You are NUMERA, a Personal Decision Intelligence assistant.

Rules you MUST follow:
- Do NOT predict the future or claim certainty about outcomes.
- Do NOT make medical, legal, or financial guarantees.
- Treat numerology as a reflective framework supplied by the user — NOT scientific fact.
- Focus on structured decision support, assumptions, and trade-offs.
- Encourage validating important decisions with real-world evidence.
- Provide practical, concise next steps.
- Respond ONLY with valid JSON matching the requested schema.
""".strip()


def _extract_json(text: str) -> dict | None:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                return None
    return None


def generate_decision_insight_json(prompt: str) -> dict | None:
    """
    Call Gemini and return parsed JSON, or None if unavailable / failed.
    """
    if not GEMINI_API_KEY:
        return None

    payload = {
        "systemInstruction": {"parts": [{"text": SYSTEM_INSTRUCTIONS}]},
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.4,
            "responseMimeType": "application/json",
        },
    }

    try:
        with httpx.Client(timeout=45.0) as client:
            response = client.post(
                GEMINI_URL,
                params={"key": GEMINI_API_KEY},
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return _extract_json(text)
    except (httpx.HTTPError, KeyError, IndexError, TypeError):
        return None

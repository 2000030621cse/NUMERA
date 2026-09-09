"""Decision insight orchestration — Gemini with structured fallback."""

from __future__ import annotations

from app.schemas.decision_insight import (
    DecisionInsightRequest,
    DecisionInsightResponse,
)
from app.services.gemini_service import generate_decision_insight_json

LIFE_PATH_THEMES: dict[int, str] = {
    1: "independence, initiative and self-direction",
    2: "cooperation, diplomacy and balance",
    3: "expression, creativity and communication",
    4: "structure, discipline and building foundations",
    5: "change, adaptability and exploration",
    6: "responsibility, care and meaningful choices",
    7: "analysis, depth and inner clarity",
    8: "ambition, stewardship and practical outcomes",
    9: "completion, perspective and broader impact",
    11: "intuition and inspirational leadership (master number)",
    22: "large-scale building and disciplined vision (master number)",
    33: "compassionate service and nurturing impact (master number)",
}


def _life_path_theme(n: int) -> str:
    return LIFE_PATH_THEMES.get(n, "personal rhythm and self-awareness")


def build_gemini_prompt(request: DecisionInsightRequest) -> str:
    numerology = request.numerology
    possibilities_text = "\n".join(
        f"- {p.name}: benefit={p.expected_benefit}; trade-off={p.possible_tradeoff}; "
        f"alignment={p.alignment_notes or 'not specified'}"
        for p in request.possibilities
    ) or "None provided"

    priorities = ", ".join(request.priorities) if request.priorities else "not specified"

    return f"""
Generate a decision intelligence report for NUMERA.

User profile:
- Name: {request.full_name}
- Date of birth: {request.date_of_birth}
- Primary goal: {request.primary_goal}

Numerology snapshot (reflective framework only — NOT predictions):
- Life Path: {numerology.life_path_number}
- Birthday Number: {numerology.birthday_number}
- Personal Year: {numerology.personal_year}
- Personal Month: {numerology.personal_month}

Decision:
- Area: {request.decision_area}
- Question: {request.decision_question}
- Context: {request.decision_context or "not provided"}
- Priorities: {priorities}
- Time horizon: {request.time_horizon or "not specified"}

Possible paths:
{possibilities_text}

Return JSON with exactly these keys:
{{
  "summary": "2-3 sentence overview",
  "signals": [
    "Life Path relevance (1 sentence)",
    "Birthday Number relevance (1 sentence)",
    "Personal Year relevance (1 sentence)",
    "Personal Month relevance (1 sentence)"
  ],
  "considerations": ["3-5 concise bullet considerations"],
  "recommended_next_steps": ["3 practical numbered actions as strings"]
}}
""".strip()


def build_fallback_response(request: DecisionInsightRequest) -> DecisionInsightResponse:
    """Structured fallback when Gemini is not configured or fails."""
    n = request.numerology
    theme = _life_path_theme(n.life_path_number)
    priorities = ", ".join(request.priorities) if request.priorities else "your stated priorities"

    return DecisionInsightResponse(
        summary=(
            f"A structured reflection on your {request.decision_area.lower()} decision, "
            f"grounded in your {request.primary_goal} focus and numerology baseline — "
            "offered as a framework for thinking, not a forecast."
        ),
        signals=[
            f"Life Path {n.life_path_number} may highlight themes of {theme} — "
            "consider how this lens shapes your decision, not what it guarantees.",
            f"Birthday Number {n.birthday_number} reflects a natural approach to choices — "
            "use it as a reflective prompt, not a verdict.",
            f"Personal Year {n.personal_year} suggests pacing for this calendar year — "
            "timing is a signal to reflect on, not a prediction.",
            f"Personal Month {n.personal_month} adds near-term emphasis — "
            "pair it with evidence from your current situation.",
        ],
        considerations=[
            "What evidence would make one option clearly stronger than the others?",
            "What is the downside if this decision does not work as hoped?",
            "What is reversible versus difficult to undo?",
            f"Which priority matters most over the next 6–12 months: {priorities}?",
            "What assumptions are you making that deserve validation?",
        ],
        recommended_next_steps=[
            "Gather the missing information that would reduce uncertainty.",
            "Compare the strongest option against your top two priorities.",
            "Choose a low-risk first step before making an irreversible commitment.",
        ],
        is_development_preview=True,
    )


def _normalize_gemini_payload(raw: dict) -> DecisionInsightResponse | None:
    try:
        return DecisionInsightResponse(
            summary=str(raw["summary"]),
            signals=[str(s) for s in raw["signals"]],
            considerations=[str(c) for c in raw["considerations"]],
            recommended_next_steps=[str(s) for s in raw["recommended_next_steps"]],
            is_development_preview=False,
        )
    except (KeyError, TypeError, ValueError):
        return None


def generate_decision_insight(request: DecisionInsightRequest) -> DecisionInsightResponse:
    """Produce decision insight via Gemini when configured, else structured fallback."""
    prompt = build_gemini_prompt(request)
    raw = generate_decision_insight_json(prompt)
    if raw:
        parsed = _normalize_gemini_payload(raw)
        if parsed:
            return parsed
    return build_fallback_response(request)

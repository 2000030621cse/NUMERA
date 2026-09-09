"""Optional Gemini enrichment for final report — contextualizes deterministic Decision Compass."""

from __future__ import annotations

import json

from app.schemas.decision_session import (
    CompassConfidence,
    CurrentlyStrongestOption,
    FinalReportRequest,
    FinalReportResponse,
)
from app.services.gemini_service import generate_decision_insight_json

SYSTEM_RULES = """
You are NUMERA, a Personal Decision Intelligence assistant.

Rules you MUST follow:
- Never invent user facts not in the payload.
- Never predict the future or claim certainty about outcomes.
- Never say "you should definitely choose X" or "the correct answer is".
- Never present numerology as scientific fact or use it to rank options.
- The deterministic Decision Compass already computed alignment — explain and contextualize it, do NOT replace it with a different ranking.
- Use language like "currently shows the strongest alignment" and "this assessment could change if".
- Distinguish reflective numerology from practical decision analysis.
- Ground everything in the user's stated context, options, and Screen 03 analysis.
- If a field is empty or "not stated", do not fill it in with assumptions.
- Return ONLY valid JSON matching the schema provided.
"""


def _session_payload(
    request: FinalReportRequest,
    compass_payload: dict | None = None,
) -> str:
    d = request.decision
    p = request.profile
    a = request.analysis
    options = request.options or a.options
    compass = compass_payload

    payload = {
        "profile": {
            "full_name": p.full_name,
            "primary_goal": p.primary_goal,
            "numerology_reflective_only": {
                "life_path": p.life_path_number,
                "birthday": p.birthday_number,
                "personal_year": p.personal_year,
                "personal_month": p.personal_month,
            },
        },
        "decision": {
            "area": d.decision_area,
            "question": d.decision_question,
            "why_considering": d.why_considering or "not stated",
            "biggest_concern": d.biggest_concern or "not stated",
            "priorities": d.priorities or [],
            "constraints": d.constraints or "not stated",
            "risk_tolerance": d.risk_tolerance or "not stated",
            "time_horizon": d.time_horizon or "not stated",
            "context": d.context or "not stated",
        },
        "options": [{"id": o.id, "title": o.title, "source": o.source} for o in options],
        "screen_03_analysis": {
            "summary": a.summary,
            "key_tension": a.key_tension,
            "tension_headline": a.tension_headline,
            "decision_synthesis": a.decision_synthesis,
            "source_label": a.source_label,
        },
    }

    if compass:
        payload["decision_compass"] = {
            "scoring_formula": compass.get("scoring_formula", ""),
            "strongest": compass.get("strongest", {}),
            "confidence": compass.get("confidence", {}),
            "scores": [
                {
                    "title": s.get("option_title", s.get("title", "")),
                    "numera_alignment": s.get("numera_alignment", 0),
                    "alignment_label": s.get("alignment_label", ""),
                }
                for s in compass.get("scores", [])
            ],
            "what_could_change": compass.get("what_could_change", []),
        }

    return json.dumps(payload, indent=2)


def enrich_final_report_with_gemini(
    request: FinalReportRequest,
    base: FinalReportResponse,
) -> FinalReportResponse:
    """Attempt Gemini enrichment; return context-aware base if unavailable."""
    strongest_json = "null"
    if base.currently_strongest_option:
        strongest_json = json.dumps(base.currently_strongest_option.model_dump())

    compass_payload = base.decision_compass.model_dump() if base.decision_compass else None

    prompt = f"""
{SYSTEM_RULES}

Complete DecisionSession with deterministic Decision Compass (interpret — do not invent facts or re-rank):
{_session_payload(request, compass_payload)}

Deterministic base report (preserve compass ranking and scores; refine prose only):
- decision_summary: {base.decision_summary}
- key_tension: {base.key_tension}
- ai_intelligence_summary: {base.ai_intelligence_summary}
- currently_strongest_option: {strongest_json}
- confidence: {base.confidence.model_dump()}

Return JSON with exactly these keys:
{{
  "decision_summary": "...",
  "key_tension": "...",
  "currently_strongest_option": {{"option_id": "...", "title": "...", "reason": "..."}} or null,
  "confidence": {{"level": "High|Moderate|Exploratory", "reason": "..."}},
  "numerology_reflection": [
    {{"signal": "...", "reflection": "...", "decision_relevance": "...", "numerology_lens": "..."}}
  ],
  "numerology_lens_summary": "...",
  "option_analysis": [
    {{"option": "...", "upside": "...", "tradeoffs": "...", "unknowns": "...", "evidence_to_check": "...", "numera_alignment": 0, "alignment_label": "...", "main_strength": "...", "main_tradeoff": "..."}}
  ],
  "what_could_change": ["3-5 concrete items from user context"],
  "key_considerations": ["..."],
  "next_steps": ["3 practical actions"],
  "ai_intelligence_summary": "Explain and contextualize the deterministic compass — not a new recommendation",
  "derivation_notes": ["..."]
}}
"""

    raw = generate_decision_insight_json(prompt)
    if not raw:
        return base

    try:
        from app.schemas.decision_session import NumerologyReflection, OptionAnalysis

        numerology = [
            NumerologyReflection(**item)
            for item in raw.get("numerology_reflection", [])
        ] or base.numerology_reflection

        option_analysis = [
            OptionAnalysis(**item) for item in raw.get("option_analysis", [])
        ] or base.option_analysis

        currently_raw = raw.get("currently_strongest_option")
        currently = base.currently_strongest_option
        if currently_raw is None:
            currently = None
        elif isinstance(currently_raw, dict) and currently_raw.get("title"):
            currently = CurrentlyStrongestOption(**currently_raw)

        conf_raw = raw.get("confidence", {})
        confidence = CompassConfidence(
            level=str(conf_raw.get("level", base.confidence.level)),
            reason=str(conf_raw.get("reason", base.confidence.reason)),
        )

        return FinalReportResponse(
            decision_summary=str(raw.get("decision_summary", base.decision_summary)),
            key_tension=str(raw.get("key_tension", base.key_tension)),
            tension_headline=base.tension_headline,
            numerology_reflection=numerology,
            numerology_lens_summary=str(
                raw.get("numerology_lens_summary", base.numerology_lens_summary)
            ),
            option_analysis=option_analysis,
            decision_compass=base.decision_compass,
            currently_strongest_option=currently,
            confidence=confidence,
            what_could_change=[
                str(x) for x in raw.get("what_could_change", base.what_could_change)
            ],
            key_considerations=[
                str(c) for c in raw.get("key_considerations", base.key_considerations)
            ],
            next_steps=[str(s) for s in raw.get("next_steps", base.next_steps)],
            ai_intelligence_summary=str(
                raw.get("ai_intelligence_summary", base.ai_intelligence_summary)
            ),
            derivation_notes=[
                str(n) for n in raw.get("derivation_notes", base.derivation_notes)
            ],
            synthesis_source="gemini",
            source_label="NUMERA AI synthesis (Gemini)",
            is_development_preview=False,
            preview_label="",
        )
    except (TypeError, ValueError, KeyError):
        return base

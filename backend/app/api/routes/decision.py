"""Decision analysis API — Screen 03 intelligence + Decision Compass."""

from fastapi import APIRouter

from app.schemas.decision_session import (
    AnalyzeDecisionRequest,
    AnalyzeDecisionResponse,
    CompassRequest,
    DecisionCompass,
)
from app.services.decision_engine import analyze_decision
from app.services.decision_compass import build_decision_compass

router = APIRouter(prefix="/api/decision", tags=["decision"])


@router.post("/analyze", response_model=AnalyzeDecisionResponse)
def create_decision_analysis(
    payload: AnalyzeDecisionRequest,
) -> AnalyzeDecisionResponse:
    """Context-aware decision intelligence from the unified DecisionSession."""
    return analyze_decision(payload.profile, payload.decision)


@router.post("/compass", response_model=DecisionCompass)
def create_decision_compass(payload: CompassRequest) -> DecisionCompass:
    """Explainable NUMERA Alignment for the current options (Screen 04 refresh)."""
    options = payload.options
    if not options:
        from app.services.decision_engine import generate_options

        options = generate_options(payload.decision)
    return build_decision_compass(options, payload.decision)

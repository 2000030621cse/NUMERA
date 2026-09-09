"""Decision insight API routes."""

from fastapi import APIRouter

from app.schemas.decision_insight import (
    DecisionInsightRequest,
    DecisionInsightResponse,
)
from app.services.decision_insight import generate_decision_insight

router = APIRouter(prefix="/api/numerology", tags=["decision-insight"])


@router.post("/decision-insight", response_model=DecisionInsightResponse)
def create_decision_insight(
    payload: DecisionInsightRequest,
) -> DecisionInsightResponse:
    """Generate structured decision intelligence (Gemini when configured)."""
    return generate_decision_insight(payload)

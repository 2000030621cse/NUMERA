"""Final report API — Screen 05 decision intelligence report."""

from fastapi import APIRouter

from app.schemas.decision_session import FinalReportRequest, FinalReportResponse
from app.services.decision_engine import build_final_report
from app.services.decision_insight_gemini import enrich_final_report_with_gemini

router = APIRouter(prefix="/api/numerology", tags=["final-report"])


@router.post("/decision-insight", response_model=FinalReportResponse)
def create_decision_insight_report(
    payload: FinalReportRequest,
) -> FinalReportResponse:
    """Synthesize final report from Screen 03 analysis artifact + full session."""
    base = build_final_report(payload)
    enriched = enrich_final_report_with_gemini(payload, base)
    return enriched

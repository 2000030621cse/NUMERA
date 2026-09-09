"""Numerology API routes."""

from fastapi import APIRouter

from app.schemas.numerology import NumerologyProfileRequest, NumerologyProfileResponse
from app.services.numerology import build_numerology_profile

router = APIRouter(prefix="/api/numerology", tags=["numerology"])


@router.post("/profile", response_model=NumerologyProfileResponse)
def create_numerology_profile(
    payload: NumerologyProfileRequest,
) -> NumerologyProfileResponse:
    """Calculate a deterministic numerology profile from name and date of birth."""
    profile = build_numerology_profile(payload.full_name, payload.date_of_birth)
    return NumerologyProfileResponse(**profile)

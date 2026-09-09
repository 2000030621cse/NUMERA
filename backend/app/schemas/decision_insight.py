"""Pydantic schemas for decision insight API."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class NumerologySnapshot(BaseModel):
    life_path_number: int
    birthday_number: int
    personal_year: int
    personal_month: int


class PossibilityInput(BaseModel):
    name: str = Field(..., min_length=1)
    assumption: str = ""
    expected_benefit: str = ""
    possible_tradeoff: str = ""
    alignment_notes: str = ""


class DecisionInsightRequest(BaseModel):
    """Structured payload for final decision intelligence report."""

    model_config = ConfigDict(str_strip_whitespace=True)

    full_name: str = Field(..., min_length=1)
    date_of_birth: date
    numerology: NumerologySnapshot
    primary_goal: str = Field(..., min_length=1)
    decision_question: str = Field(..., min_length=1)
    decision_area: str = Field(..., min_length=1)
    decision_context: str = ""
    priorities: list[str] = Field(default_factory=list)
    time_horizon: str = ""
    possibilities: list[PossibilityInput] = Field(default_factory=list)


class DecisionInsightResponse(BaseModel):
    summary: str
    signals: list[str] = Field(..., min_length=1)
    considerations: list[str] = Field(..., min_length=1)
    recommended_next_steps: list[str] = Field(..., min_length=1)
    is_development_preview: bool = False

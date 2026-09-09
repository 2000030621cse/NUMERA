"""Pydantic schemas for numerology API contracts."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator


class NumerologyProfileRequest(BaseModel):
    """Input for building a numerology profile."""

    model_config = ConfigDict(str_strip_whitespace=True)

    full_name: str = Field(..., min_length=1, description="Person's full name")
    date_of_birth: date = Field(..., description="Birth date in ISO format (YYYY-MM-DD)")

    @field_validator("full_name")
    @classmethod
    def full_name_must_not_be_blank(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("full_name must not be empty")
        return value.strip()


class NumerologyProfileResponse(BaseModel):
    """Calculated numerology profile."""

    full_name: str
    date_of_birth: date
    life_path_number: int
    birthday_number: int
    personal_year: int
    personal_month: int

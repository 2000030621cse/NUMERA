"""Deterministic numerology calculations (no LLM)."""

from __future__ import annotations

from datetime import date


MASTER_NUMBERS_LIFE_PATH = frozenset({11, 22, 33})
MASTER_NUMBERS_BIRTHDAY = frozenset({11, 22})


def digit_sum(value: int) -> int:
    """Sum the decimal digits of a non-negative integer."""
    return sum(int(digit) for digit in str(abs(value)))


def reduce_number(value: int, *, masters: frozenset[int] | None = None) -> int:
    """
    Reduce a number by repeatedly summing digits.

    When ``masters`` is provided, values in that set are preserved and not reduced further.
    """
    n = abs(value)
    preserve = masters or frozenset()
    while n > 9 and n not in preserve:
        n = digit_sum(n)
    return n


def life_path_number(date_of_birth: date) -> int:
    """
    Life Path Number from birth date.

    Month, day, and year are reduced separately (keeping 11/22/33), then summed and reduced.
    """
    month = reduce_number(date_of_birth.month, masters=MASTER_NUMBERS_LIFE_PATH)
    day = reduce_number(date_of_birth.day, masters=MASTER_NUMBERS_LIFE_PATH)
    year = reduce_number(digit_sum(date_of_birth.year), masters=MASTER_NUMBERS_LIFE_PATH)
    return reduce_number(month + day + year, masters=MASTER_NUMBERS_LIFE_PATH)


def birthday_number(date_of_birth: date) -> int:
    """Birthday Number from the day of month (keeps master numbers 11 and 22)."""
    return reduce_number(date_of_birth.day, masters=MASTER_NUMBERS_BIRTHDAY)


def personal_year_number(date_of_birth: date, as_of: date | None = None) -> int:
    """
    Personal Year Number for calendar year ``as_of.year`` (defaults to today).

    Timing numbers are fully reduced to 1–9 (no master numbers).
    """
    ref = as_of or date.today()
    month = reduce_number(date_of_birth.month)
    day = reduce_number(date_of_birth.day)
    year = reduce_number(digit_sum(ref.year))
    return reduce_number(month + day + year)


def personal_month_number(date_of_birth: date, as_of: date | None = None) -> int:
    """
    Personal Month Number for ``as_of`` month (defaults to today).

    Personal Month = Personal Year + calendar month, reduced to 1–9.
    """
    ref = as_of or date.today()
    year_number = personal_year_number(date_of_birth, as_of=ref)
    return reduce_number(year_number + ref.month)


def build_numerology_profile(
    full_name: str,
    date_of_birth: date,
    *,
    as_of: date | None = None,
) -> dict:
    """Assemble a numerology profile dict for API responses."""
    ref = as_of or date.today()
    return {
        "full_name": full_name,
        "date_of_birth": date_of_birth.isoformat(),
        "life_path_number": life_path_number(date_of_birth),
        "birthday_number": birthday_number(date_of_birth),
        "personal_year": personal_year_number(date_of_birth, as_of=ref),
        "personal_month": personal_month_number(date_of_birth, as_of=ref),
    }

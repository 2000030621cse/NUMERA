"""Unit tests for deterministic numerology calculations."""

from datetime import date

from app.services.numerology import (
    birthday_number,
    build_numerology_profile,
    digit_sum,
    life_path_number,
    personal_month_number,
    personal_year_number,
    reduce_number,
)


def test_digit_sum() -> None:
    assert digit_sum(2002) == 4
    assert digit_sum(25) == 7
    assert digit_sum(0) == 0


def test_reduce_number_basic() -> None:
    assert reduce_number(14) == 5
    assert reduce_number(29) == 2  # 2+9=11 → 1+1=2 when masters are not kept
    assert reduce_number(10) == 1


def test_reduce_number_keeps_masters() -> None:
    assert reduce_number(11, masters=frozenset({11, 22, 33})) == 11
    assert reduce_number(22, masters=frozenset({11, 22, 33})) == 22
    assert reduce_number(33, masters=frozenset({11, 22, 33})) == 33


def test_life_path_number_example() -> None:
    # 2002-03-25 → month 3, day 7, year 4 → 14 → 5
    assert life_path_number(date(2002, 3, 25)) == 5


def test_life_path_number_master_eleven() -> None:
    # 1980-01-01 → 1 + 1 + 9 = 11 (master preserved)
    assert life_path_number(date(1980, 1, 1)) == 11


def test_life_path_number_another_case() -> None:
    # 2000-01-01 → 1 + 1 + 2 = 4
    assert life_path_number(date(2000, 1, 1)) == 4


def test_birthday_number() -> None:
    assert birthday_number(date(2002, 3, 25)) == 7
    assert birthday_number(date(1990, 5, 11)) == 11
    assert birthday_number(date(1990, 5, 22)) == 22
    assert birthday_number(date(1990, 5, 29)) == 11  # 2+9=11 kept


def test_personal_year_and_month_fixed_reference() -> None:
    dob = date(2002, 3, 25)
    as_of = date(2026, 3, 15)
    # month 3 + day 7 + year 2026→10→1 → 11 → 2 (no masters for timing)
    assert personal_year_number(dob, as_of=as_of) == 2
    # personal month = 2 + 3 = 5
    assert personal_month_number(dob, as_of=as_of) == 5


def test_build_numerology_profile() -> None:
    profile = build_numerology_profile(
        "Example User",
        date(2002, 3, 25),
        as_of=date(2026, 3, 15),
    )
    assert profile == {
        "full_name": "Example User",
        "date_of_birth": "2002-03-25",
        "life_path_number": 5,
        "birthday_number": 7,
        "personal_year": 2,
        "personal_month": 5,
    }

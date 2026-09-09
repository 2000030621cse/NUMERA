"""API tests for numerology profile endpoint and validation."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_numerology_profile_success() -> None:
    response = client.post(
        "/api/numerology/profile",
        json={
            "full_name": "Example User",
            "date_of_birth": "2002-03-25",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Example User"
    assert data["date_of_birth"] == "2002-03-25"
    assert data["life_path_number"] == 5
    assert data["birthday_number"] == 7
    assert isinstance(data["personal_year"], int)
    assert isinstance(data["personal_month"], int)
    assert 1 <= data["personal_year"] <= 9
    assert 1 <= data["personal_month"] <= 9


def test_numerology_profile_rejects_empty_name() -> None:
    response = client.post(
        "/api/numerology/profile",
        json={
            "full_name": "   ",
            "date_of_birth": "2002-03-25",
        },
    )
    assert response.status_code == 422


def test_numerology_profile_rejects_missing_name() -> None:
    response = client.post(
        "/api/numerology/profile",
        json={"date_of_birth": "2002-03-25"},
    )
    assert response.status_code == 422


def test_numerology_profile_rejects_invalid_date() -> None:
    response = client.post(
        "/api/numerology/profile",
        json={
            "full_name": "Example User",
            "date_of_birth": "not-a-date",
        },
    )
    assert response.status_code == 422


def test_numerology_profile_rejects_impossible_date() -> None:
    response = client.post(
        "/api/numerology/profile",
        json={
            "full_name": "Example User",
            "date_of_birth": "2002-02-30",
        },
    )
    assert response.status_code == 422


def test_numerology_profile_strips_name_whitespace() -> None:
    response = client.post(
        "/api/numerology/profile",
        json={
            "full_name": "  Example User  ",
            "date_of_birth": "2002-03-25",
        },
    )
    assert response.status_code == 200
    assert response.json()["full_name"] == "Example User"

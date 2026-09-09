"""API tests for decision analyze and final report endpoints."""



from fastapi.testclient import TestClient



from app.main import app



client = TestClient(app)



SESSION = {

    "profile": {

        "full_name": "Alex Chen",

        "date_of_birth": "1995-06-15",

        "life_path_number": 6,

        "birthday_number": 6,

        "personal_year": 3,

        "personal_month": 5,

        "primary_goal": "Career",

    },

    "decision": {

        "decision_area": "Career",

        "decision_question": "Should I switch to a new company this year?",

        "why_considering": "I feel stagnant in my current role.",

        "biggest_concern": "Leaving a stable team",

        "priorities": ["Growth", "Stability"],

        "constraints": "Mortgage obligations",

        "risk_tolerance": "Moderate",

        "time_horizon": "Next few months",

        "context": "Promotion path is unclear.",

        "user_options": [

            {"id": "opt-a", "title": "Stay in current role"},

            {"id": "opt-b", "title": "Switch to new company"},

        ],

    },

}





def test_analyze_decision_endpoint() -> None:

    response = client.post("/api/decision/analyze", json=SESSION)

    assert response.status_code == 200

    data = response.json()

    assert "contextual_signals" in data

    assert len(data["options"]) >= 2

    assert data["options"][0]["source"] == "user"

    assert data["options"][0]["title"] == "Stay in current role"

    assert data["is_development_preview"] is False

    assert data["analysis_source"] == "deterministic"





def test_final_report_endpoint_requires_analysis() -> None:

    analyze = client.post("/api/decision/analyze", json=SESSION).json()

    payload = {

        **SESSION,

        "options": analyze["options"],

        "analysis": {

            "summary": analyze["summary"],

            "key_tension": analyze["key_tension"],

            "decision_synthesis": analyze["decision_synthesis"],

            "goal_alignment": analyze["goal_alignment"],

            "contextual_signals": analyze["contextual_signals"],

            "decision_questions": analyze["decision_questions"],

            "considerations": analyze["considerations"],

            "options": analyze["options"],

            "analysis_source": analyze["analysis_source"],

            "source_label": analyze["source_label"],

        },

    }

    response = client.post("/api/numerology/decision-insight", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "decision_summary" in data

    assert "ai_intelligence_summary" in data

    assert "derivation_notes" in data

    assert len(data["option_analysis"]) >= 2

    assert data["key_tension"] == analyze["key_tension"]





def test_final_report_rejects_missing_analysis() -> None:

    payload = {**SESSION, "options": []}

    response = client.post("/api/numerology/decision-insight", json=payload)

    assert response.status_code == 422


"""Tests for context-aware decision analysis engine."""



from app.services.decision_engine import (

    analyze_decision,

    analysis_to_snapshot,

    build_final_report,

)

from app.schemas.decision_session import (

    DecisionInput,

    FinalReportRequest,

    ProfileSnapshot,

    UserOptionInput,

)





def _career_profile() -> ProfileSnapshot:

    return ProfileSnapshot(

        full_name="Alex Chen",

        date_of_birth="1995-06-15",

        life_path_number=6,

        birthday_number=6,

        personal_year=3,

        personal_month=5,

        primary_goal="Career",

    )





def _career_decision() -> DecisionInput:

    return DecisionInput(

        decision_area="Career",

        decision_question="Should I switch to a new company this year?",

        why_considering="I feel stagnant and a recruiter reached out with an interesting role.",

        biggest_concern="Uncertainty about leaving a stable team",

        priorities=["Growth", "Stability"],

        constraints="Mortgage payments limit how long I can go without income",

        risk_tolerance="Moderate",

        time_horizon="Next few months",

        context="Current role is stable but promotion path is unclear.",

        user_options=[

            UserOptionInput(id="opt-a", title="Stay in current role"),

            UserOptionInput(id="opt-b", title="Switch to the new company"),

            UserOptionInput(id="opt-c", title="Negotiate internally first"),

        ],

    )





def _education_decision() -> DecisionInput:

    return DecisionInput(

        decision_area="Education",

        decision_question="Should I pursue a master's degree now?",

        why_considering="I want to transition into data science.",

        biggest_concern="Cost and time away from earning",

        priorities=["Learning", "Financial outcome"],

        time_horizon="Within a year",

        user_options=[

            UserOptionInput(id="opt-a", title="Enroll in a master's program"),

            UserOptionInput(id="opt-b", title="Take online certifications instead"),

        ],

    )





def test_career_analysis_is_contextual() -> None:

    result = analyze_decision(_career_profile(), _career_decision())

    assert "switch" in result.summary.lower() or "company" in result.summary.lower()

    assert "uncertainty" in result.key_tension.lower() or "stable" in result.key_tension.lower()

    assert len(result.contextual_signals) == 4

    assert any("career" in s.decision_relevance.lower() for s in result.contextual_signals)

    assert result.options[0].source == "user"

    assert result.options[0].title == "Stay in current role"

    assert result.is_development_preview is False

    assert result.analysis_source == "deterministic"





def test_education_differs_from_career() -> None:

    career = analyze_decision(_career_profile(), _career_decision())

    education = analyze_decision(_career_profile(), _education_decision())

    assert career.options[0].title != education.options[0].title

    assert career.summary != education.summary

    assert "master" in education.summary.lower() or "degree" in education.summary.lower()





def test_engine_suggested_fallback_when_few_user_options() -> None:

    decision = _career_decision().model_copy(update={"user_options": []})

    result = analyze_decision(_career_profile(), decision)

    assert result.options[0].source == "engine_suggested"

    assert result.options[0].title == "Stay in your current role"





def test_final_report_uses_stored_analysis_not_recompute() -> None:

    analysis = analyze_decision(_career_profile(), _career_decision())

    snapshot = analysis_to_snapshot(analysis)

    report = build_final_report(

        FinalReportRequest(

            profile=_career_profile(),

            decision=_career_decision(),

            options=analysis.options,

            analysis=snapshot,

        )

    )

    assert report.key_tension == analysis.key_tension

    assert report.decision_summary == analysis.decision_synthesis

    assert len(report.numerology_reflection) == 4

    assert len(report.option_analysis) >= 2

    assert len(report.next_steps) >= 3

    assert report.ai_intelligence_summary

    assert "switch" in report.ai_intelligence_summary.lower() or "company" in report.ai_intelligence_summary.lower()

    assert any("Stay in current role" in n for n in report.derivation_notes)

    assert report.is_development_preview is True





def test_relationship_scenario_differs() -> None:

    rel = DecisionInput(

        decision_area="Relationships",

        decision_question="Should I continue investing in this relationship?",

        biggest_concern="We keep having the same arguments",

        priorities=["Peace of mind", "Relationships"],

        user_options=[

            UserOptionInput(id="a", title="Continue with couples therapy"),

            UserOptionInput(id="b", title="Take a break to reassess"),

        ],

    )

    result = analyze_decision(_career_profile(), rel)

    assert "relationship" in result.summary.lower()

    assert result.options[0].title == "Continue with couples therapy"





def test_finance_scenario_differs() -> None:

    fin = DecisionInput(

        decision_area="Finance",

        decision_question="Should I make a major financial commitment?",

        biggest_concern="Reduced savings buffer",

        priorities=["Financial outcome", "Stability"],

        time_horizon="Next few months",

        user_options=[

            UserOptionInput(id="a", title="Proceed with the purchase"),

            UserOptionInput(id="b", title="Wait and save more"),

        ],

    )

    result = analyze_decision(_career_profile(), fin)

    assert "financial" in result.summary.lower() or "commitment" in result.summary.lower()

    assert "Reduced savings" in result.key_tension or "savings" in str(result.considerations).lower()


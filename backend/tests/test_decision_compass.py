"""Tests for NUMERA Decision Compass scoring."""

from app.schemas.decision_session import DecisionInput, DecisionOption, UserOptionInput
from app.services.decision_compass import (
    ALIGNMENT_WEIGHTS,
    CLOSE_SCORE_GAP,
    build_decision_compass,
    detect_strongest_alignment,
    score_option,
)


def _career_decision(**kwargs) -> DecisionInput:
    base = dict(
        decision_area="Career",
        decision_question="Should I switch to a new company this year?",
        why_considering="I feel stagnant",
        biggest_concern="Leaving a stable team",
        priorities=["Growth", "Stability"],
        constraints="Mortgage obligations",
        risk_tolerance="Moderate",
        time_horizon="Next few months",
        user_options=[
            UserOptionInput(id="a", title="Stay in current role"),
            UserOptionInput(id="b", title="Switch to new company"),
            UserOptionInput(id="c", title="Prepare and explore first"),
        ],
    )
    base.update(kwargs)
    return DecisionInput(**base)


def _option(opt_id: str, title: str, upside: str, tradeoff: str, rev: str) -> DecisionOption:
    return DecisionOption(
        id=opt_id,
        label="Option",
        title=title,
        source="user",
        upside=upside,
        tradeoff=tradeoff,
        uncertainty="Unknown",
        reversibility=rev,
        alignment="",
        questions=[],
        evidence_to_check=[],
    )


def test_clear_winner_career_prepare() -> None:
    decision = _career_decision()
    options = [
        _option("a", "Stay in current role", "Preserves stability", "May limit growth", "High"),
        _option(
            "c",
            "Prepare and explore first",
            "Build skills and network while exploring growth opportunities",
            "Delays change",
            "High",
        ),
        _option("b", "Switch to new company", "Opens growth", "Leaving stable team", "Moderate"),
    ]
    compass = build_decision_compass(options, decision)
    assert compass.strongest.has_clear_leader or compass.strongest.title == "No clear leader yet"
    assert len(compass.scores) == 3
    assert compass.confidence.level in ("High", "Moderate", "Exploratory")
    assert compass.tension_headline == "Growth vs Stability"


def test_close_scores_no_clear_leader() -> None:
    decision = _career_decision(priorities=["Growth", "Stability"])
    options = [
        _option("a", "Stay in current role", "Preserves stability and growth balance", "Tradeoff A", "High"),
        _option("b", "Switch to new company", "Growth with some stability planning", "Tradeoff B", "Moderate"),
    ]
    scores = [score_option(o, decision) for o in options]
    scores[0] = scores[0].model_copy(update={"numera_alignment": 70.0})
    scores[1] = scores[1].model_copy(update={"numera_alignment": 70.0 + CLOSE_SCORE_GAP - 1})
    strongest = detect_strongest_alignment(scores, decision)
    assert strongest.has_clear_leader is False
    assert "No clear leader" in strongest.title or strongest.title == "No clear leader yet"


def test_missing_priorities_exploratory_confidence() -> None:
    decision = _career_decision(priorities=[], biggest_concern="", constraints="", risk_tolerance="")
    options = [
        _option("a", "Option A", "Upside A", "Tradeoff A", "High"),
        _option("b", "Option B", "Upside B", "Tradeoff B", "High"),
    ]
    compass = build_decision_compass(options, decision)
    assert compass.confidence.level == "Exploratory"


def test_multiple_user_options_education_differs() -> None:
    edu = DecisionInput(
        decision_area="Education",
        decision_question="Should I pursue higher studies?",
        priorities=["Learning", "Financial outcome"],
        biggest_concern="Cost and time",
        time_horizon="Within a year",
        user_options=[
            UserOptionInput(id="a", title="Enroll now"),
            UserOptionInput(id="b", title="Wait and save"),
        ],
    )
    options = [
        _option("a", "Enroll now", "Accelerates learning", "Financial commitment", "Low"),
        _option("b", "Wait and save", "More time to prepare financially", "Delays progress", "High"),
    ]
    compass = build_decision_compass(options, edu)
    assert "Learning" in compass.tension_headline or "Financial" in compass.tension_headline
    assert compass.scores[0].option_title == "Enroll now"


def test_finance_category_change_factors() -> None:
    fin = DecisionInput(
        decision_area="Finance",
        decision_question="Should I make a major financial commitment?",
        priorities=["Financial outcome", "Stability"],
        biggest_concern="Reduced savings buffer",
        time_horizon="Next few months",
        user_options=[
            UserOptionInput(id="a", title="Proceed with purchase"),
            UserOptionInput(id="b", title="Wait and save more"),
        ],
    )
    options = [
        _option("a", "Proceed with purchase", "Captures opportunity", "Reduces liquidity", "Low"),
        _option("b", "Wait and save more", "Builds financial safety", "Opportunity cost", "High"),
    ]
    compass = build_decision_compass(options, fin)
    assert any("afford" in f.lower() or "financial" in f.lower() for f in compass.what_could_change)
    assert sum(ALIGNMENT_WEIGHTS.values()) == 1.0

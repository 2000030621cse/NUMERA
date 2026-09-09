"""NUMERA Decision Compass — explainable option alignment scoring (not predictive)."""

from __future__ import annotations

from app.schemas.decision_session import (
    AlignmentBreakdown,
    CompassConfidence,
    DecisionCompass,
    DecisionInput,
    DecisionOption,
    OptionCompassScore,
    StrongestAlignment,
)

# Documented, configurable weights (not scientifically validated)
ALIGNMENT_WEIGHTS: dict[str, float] = {
    "priority": 0.40,
    "risk": 0.25,
    "constraint": 0.20,
    "time_horizon": 0.15,
}

# If top two options are within this many points, no clear leader
CLOSE_SCORE_GAP = 8.0

SCORING_FORMULA_DOC = (
    "NUMERA Alignment = 40% priority fit + 25% risk fit + 20% constraint fit + "
    "15% time-horizon fit. This reflects how well each option matches the criteria "
    "you provided — not a prediction of future outcomes."
)

TRANSPARENCY_NOTE = (
    "NUMERA Alignment reflects how well each option matches the priorities and "
    "constraints you provided. It is not a prediction of future outcomes."
)

NUMEROLOGY_NOTE = (
    "Numerology is used as a reflective framework, not as a scientific prediction. "
    "It does not determine alignment scores."
)

# Keyword maps for explainable scoring
PRIORITY_KEYWORDS: dict[str, tuple[str, ...]] = {
    "growth": ("growth", "explore", "advance", "progress", "develop", "switch", "new", "opportunity"),
    "stability": ("stay", "stable", "stability", "current", "preserve", "maintain", "security"),
    "financial outcome": ("financial", "save", "savings", "income", "cost", "money", "budget", "invest"),
    "learning": ("learn", "study", "education", "skill", "certification", "enroll", "degree", "training"),
    "time": ("time", "quick", "delay", "defer", "wait", "pace", "soon", "prepare"),
    "location": ("location", "relocate", "move", "remote", "commute"),
    "relationships": ("relationship", "partner", "family", "communicate", "together", "connect"),
    "independence": ("independ", "autonomy", "self", "freedom", "own"),
    "impact": ("impact", "contribute", "purpose", "meaning", "difference"),
    "peace of mind": ("peace", "calm", "balance", "stress", "wellbeing", "reassur"),
}

RISK_PROFILES: dict[str, dict[str, tuple[str, ...]]] = {
    "low": {
        "positive": ("stay", "maintain", "prepare", "delay", "defer", "wait", "stable", "pause", "scale down"),
        "negative": ("switch", "explore", "proceed", "commit", "leaving", "disruption"),
    },
    "moderate": {
        "positive": ("prepare", "explore", "communicate", "boundaries", "alternative", "integrate"),
        "negative": (),
    },
    "high": {
        "positive": ("explore", "switch", "proceed", "commit", "change", "enroll", "continue"),
        "negative": ("wait", "defer", "stay", "pause", "delay"),
    },
}

TIME_HORIZON_PROFILES: dict[str, tuple[str, ...]] = {
    "now": ("now", "proceed", "commit", "switch", "explore", "continue", "enroll"),
    "next few months": ("prepare", "explore", "communicate", "switch", "plan"),
    "within a year": ("prepare", "enroll", "defer", "plan", "save", "research"),
    "long term": ("prepare", "defer", "build", "foundation", "integrate", "save"),
}

AREA_CHANGE_FACTORS: dict[str, list[str]] = {
    "Career": [
        "Compensation and total package compared to your current role",
        "Career growth potential and learning opportunities",
        "Financial runway if a transition takes longer than expected",
        "Team culture and manager quality at the new opportunity",
        "Whether your current role could still meet your priorities with changes",
    ],
    "Education": [
        "Program fit and return on investment",
        "Cost, financing options and impact on earnings",
        "Time commitment versus your stated horizon",
        "Whether alternative credentials could achieve the same goal",
        "Admission outcomes or cohort quality",
    ],
    "Relationships": [
        "Whether both parties share willingness to change",
        "Patterns in recurring conflicts and whether they are shifting",
        "Impact on your wellbeing and stated priorities",
        "Clarity from an honest conversation or professional support",
        "Whether boundaries you set are respected over time",
    ],
    "Finance": [
        "Actual affordability after all obligations",
        "Emergency fund buffer after the commitment",
        "Interest rates, terms or prices changing",
        "Income stability over your decision horizon",
        "Whether a smaller scope could meet the core need",
    ],
    "Personal Growth": [
        "Whether the direction still fits your values after exploration",
        "Time and energy available alongside existing responsibilities",
        "Evidence from a low-risk trial of the path",
        "Feedback from people who know your situation",
        "A shift in what you said matters most",
    ],
    "Other": [
        "New information that reduces your biggest uncertainty",
        "A change in your stated priorities or constraints",
        "Evidence from someone who made a similar choice",
        "Timeline pressure becoming more or less urgent",
        "An option becoming clearly more or less reversible",
    ],
}


def infer_tension_headline(decision: DecisionInput) -> str:
    """Short tension label derived from user context."""
    if len(decision.priorities) >= 2:
        return f"{decision.priorities[0]} vs {decision.priorities[1]}"
    if decision.priorities and decision.biggest_concern.strip():
        return f"{decision.priorities[0]} vs protecting against your concern"
    if decision.priorities:
        p = decision.priorities[0].lower()
        if p == "growth":
            return "Growth vs stability"
        if p == "stability":
            return "Short-term certainty vs long-term opportunity"
        return f"Pursuing {decision.priorities[0].lower()} vs managing uncertainty"
    area_defaults = {
        "Career": "Stability vs career growth",
        "Education": "Immediate commitment vs keeping options open",
        "Relationships": "Continued investment vs creating space for clarity",
        "Finance": "Capturing opportunity vs preserving financial safety",
        "Personal Growth": "Full commitment vs gradual integration",
    }
    return area_defaults.get(decision.decision_area, "Competing priorities vs uncertainty")


def _option_text(option: DecisionOption) -> str:
    return " ".join(
        [
            option.title,
            option.upside,
            option.tradeoff,
            option.uncertainty,
            option.reversibility,
        ]
    ).lower()


def score_priority_fit(option: DecisionOption, decision: DecisionInput) -> float:
    if not decision.priorities:
        return 50.0
    text = _option_text(option)
    total = 0.0
    weight_sum = 0.0
    for i, priority in enumerate(decision.priorities[:3]):
        w = 1.0 if i == 0 else 0.6 if i == 1 else 0.3
        weight_sum += w
        keywords = PRIORITY_KEYWORDS.get(priority.lower(), (priority.lower(),))
        hits = sum(1 for kw in keywords if kw in text)
        total += min(100.0, 40.0 + hits * 20.0) * w
    return round(total / weight_sum, 1) if weight_sum else 50.0


def score_risk_fit(option: DecisionOption, decision: DecisionInput) -> float:
    tolerance = (decision.risk_tolerance or "Moderate").lower()
    profile = RISK_PROFILES.get(tolerance, RISK_PROFILES["moderate"])
    text = _option_text(option)
    score = 55.0
    for kw in profile["positive"]:
        if kw in text:
            score += 12.0
    for kw in profile.get("negative", ()):
        if kw in text:
            score -= 10.0
    if "high" in option.reversibility.lower() and tolerance == "low":
        score += 8.0
    if "low" in option.reversibility.lower() and tolerance == "high":
        score += 5.0
    return round(max(0.0, min(100.0, score)), 1)


def score_constraint_fit(option: DecisionOption, decision: DecisionInput) -> float:
    constraints = decision.constraints.strip().lower()
    if not constraints:
        return 55.0
    text = _option_text(option)
    score = 50.0
    constraint_tokens = [t for t in constraints.replace(",", " ").split() if len(t) > 3]
    for token in constraint_tokens[:6]:
        if token in text:
            score += 8.0
    if any(w in constraints for w in ("financial", "money", "mortgage", "debt", "save")):
        if any(w in text for w in ("save", "delay", "prepare", "scale", "stable", "stay")):
            score += 15.0
        if any(w in text for w in ("proceed", "commit", "switch", "explore")):
            score -= 8.0
    if decision.biggest_concern.strip():
        concern = decision.biggest_concern.lower()
        if any(w in concern for w in ("stability", "stable", "security")) and "stay" in text:
            score += 10.0
        if any(w in concern for w in ("stability", "leaving")) and "prepare" in text:
            score += 12.0
    return round(max(0.0, min(100.0, score)), 1)


def score_time_horizon_fit(option: DecisionOption, decision: DecisionInput) -> float:
    horizon = (decision.time_horizon or "").lower()
    if not horizon:
        return 55.0
    text = _option_text(option)
    keywords = TIME_HORIZON_PROFILES.get(horizon, ())
    hits = sum(1 for kw in keywords if kw in text)
    return round(max(20.0, min(100.0, 45.0 + hits * 15.0)), 1)


def _alignment_label(score: float) -> str:
    if score >= 70:
        return "Strong fit"
    if score >= 50:
        return "Moderate fit"
    return "Exploratory fit"


def score_option(option: DecisionOption, decision: DecisionInput) -> OptionCompassScore:
    priority = score_priority_fit(option, decision)
    risk = score_risk_fit(option, decision)
    constraint = score_constraint_fit(option, decision)
    time_h = score_time_horizon_fit(option, decision)

    total = round(
        priority * ALIGNMENT_WEIGHTS["priority"]
        + risk * ALIGNMENT_WEIGHTS["risk"]
        + constraint * ALIGNMENT_WEIGHTS["constraint"]
        + time_h * ALIGNMENT_WEIGHTS["time_horizon"],
        1,
    )

    top_priority = decision.priorities[0] if decision.priorities else "your stated goal"
    strengths = (
        f"Aligns with your focus on {top_priority} (priority fit: {priority}/100). "
        f"{option.upside[:160]}{'…' if len(option.upside) > 160 else ''}"
    )
    tradeoffs = option.tradeoff
    if decision.biggest_concern:
        tradeoffs = (
            f"{option.tradeoff} Main tension with your concern "
            f'("{decision.biggest_concern}"): weigh this explicitly.'
        )

    return OptionCompassScore(
        option_id=option.id,
        option_title=option.title,
        numera_alignment=total,
        alignment_label=_alignment_label(total),
        breakdown=AlignmentBreakdown(
            priority_score=priority,
            risk_score=risk,
            constraint_score=constraint,
            time_horizon_score=time_h,
            weights=dict(ALIGNMENT_WEIGHTS),
        ),
        strengths=strengths,
        tradeoffs=tradeoffs,
        unknowns=option.uncertainty,
        evidence_to_check=option.evidence_to_check[:3]
        or [f"Gather evidence specific to: {option.title}"],
    )


def calculate_confidence(decision: DecisionInput, scores: list[OptionCompassScore]) -> CompassConfidence:
    fields = [
        bool(decision.priorities),
        bool(decision.biggest_concern.strip()),
        bool(decision.time_horizon),
        bool(decision.risk_tolerance),
        bool(decision.constraints.strip()),
        bool(decision.why_considering.strip() or decision.context.strip()),
    ]
    filled = sum(fields)
    if filled >= 5 and decision.priorities:
        return CompassConfidence(
            level="High",
            reason=(
                "You provided priorities, concern, timing and context — "
                "alignment reflects a relatively complete picture of what matters to you. "
                "This is not predictive confidence."
            ),
        )
    if filled >= 3 and decision.priorities:
        return CompassConfidence(
            level="Moderate",
            reason=(
                "You provided core decision criteria, but some context is still thin. "
                "Alignment may shift as you add detail. This is not predictive confidence."
            ),
        )
    return CompassConfidence(
        level="Exploratory",
        reason=(
            "Limited decision context was provided — treat alignment as a starting "
            "framework for exploration, not a conclusion. This is not predictive confidence."
        ),
    )


def detect_strongest_alignment(
    scores: list[OptionCompassScore],
    decision: DecisionInput,
) -> StrongestAlignment:
    if not scores:
        return StrongestAlignment(
            option_id="",
            title="",
            reason="No options available to compare.",
            has_clear_leader=False,
            no_leader_reason="Add at least two paths to compare.",
        )

    ranked = sorted(scores, key=lambda s: s.numera_alignment, reverse=True)
    top = ranked[0]
    second = ranked[1] if len(ranked) > 1 else None

    if second and (top.numera_alignment - second.numera_alignment) < CLOSE_SCORE_GAP:
        gap_note = (
            f'"{top.option_title}" ({top.numera_alignment}) and '
            f'"{second.option_title}" ({second.numera_alignment}) are closely matched.'
        )
        missing = []
        if not decision.biggest_concern.strip():
            missing.append("your biggest concern")
        if not decision.constraints.strip():
            missing.append("specific constraints")
        if not decision.time_horizon:
            missing.append("a clear time horizon")
        info_gap = (
            f" Clarify {', '.join(missing)}." if missing else " Gather option-specific evidence."
        )
        return StrongestAlignment(
            option_id="",
            title="No clear leader yet",
            reason=(
                f"{gap_note} Based on the priorities and context you provided, "
                f"no option shows a clearly stronger alignment yet.{info_gap} "
                "This is a reflection, not a prediction."
            ),
            has_clear_leader=False,
            no_leader_reason=gap_note,
        )

    priority_text = (
        f"your stated priorities ({', '.join(decision.priorities)})"
        if decision.priorities
        else "your decision criteria"
    )
    concern_text = (
        f' Your biggest concern is "{decision.biggest_concern}".'
        if decision.biggest_concern
        else ""
    )
    reason = (
        f'Based on the priorities and context you provided, "{top.option_title}" '
        f"currently shows the strongest NUMERA Alignment ({top.numera_alignment}/100). "
        f"It best matches {priority_text}.{concern_text} "
        f"The main trade-off to weigh: {top.tradeoffs[:200]}. "
        "This assessment could change if new information shifts how well this path "
        "fits what you said matters. This is a reflection, not a prediction."
    )

    return StrongestAlignment(
        option_id=top.option_id,
        title=top.option_title,
        reason=reason,
        has_clear_leader=True,
        no_leader_reason="",
    )


def generate_change_factors(decision: DecisionInput, strongest: StrongestAlignment) -> list[str]:
    factors = list(AREA_CHANGE_FACTORS.get(decision.decision_area, AREA_CHANGE_FACTORS["Other"]))
    if decision.biggest_concern.strip():
        factors.insert(
            0,
            f'New information that directly addresses your concern: "{decision.biggest_concern}"',
        )
    if decision.priorities:
        factors.append(f"A shift in how much you weight {decision.priorities[0]} relative to other priorities")
    if strongest.has_clear_leader:
        factors.append(f"Evidence that weakens the case for \"{strongest.title}\"")
        factors.append("Evidence that strengthens a currently lower-ranked option")
    else:
        factors.append("Side-by-side comparison using your top two priorities as a scoring lens")
    return factors[:5]


def build_decision_compass(
    options: list[DecisionOption],
    decision: DecisionInput,
) -> DecisionCompass:
    """Build explainable Decision Compass for Screen 04/05."""
    scores = [score_option(opt, decision) for opt in options]
    strongest = detect_strongest_alignment(scores, decision)
    confidence = calculate_confidence(decision, scores)
    what_could_change = generate_change_factors(decision, strongest)

    return DecisionCompass(
        scores=scores,
        strongest=strongest,
        confidence=confidence,
        what_could_change=what_could_change,
        transparency_note=TRANSPARENCY_NOTE,
        numerology_note=NUMEROLOGY_NOTE,
        scoring_formula=SCORING_FORMULA_DOC,
        tension_headline=infer_tension_headline(decision),
    )

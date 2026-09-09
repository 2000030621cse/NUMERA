"""Context-aware decision intelligence engine — deterministic synthesis + Gemini hook."""

from __future__ import annotations

from app.schemas.decision_session import (
    AnalyzeDecisionResponse,
    CompassConfidence,
    ContextualSignal,
    CurrentlyStrongestOption,
    DecisionInput,
    DecisionOption,
    FinalReportRequest,
    FinalReportResponse,
    NumerologyReflection,
    OptionAnalysis,
    ProfileSnapshot,
    StoredAnalysisSnapshot,
    UserOptionInput,
)
from app.services.decision_compass import (
    build_decision_compass,
    infer_tension_headline,
)
from app.services.numerology_interpretation import (
    contextualize_signal,
    get_signal_metadata,
)

DETERMINISTIC_LABEL = "NUMERA deterministic analysis"
PREVIEW_LABEL = "NUMERA Preview — deterministic synthesis (AI unavailable)"

# Engine-suggested option templates keyed by decision area (fallback only)
OPTION_TEMPLATES: dict[str, list[dict[str, str]]] = {
    "Career": [
        {
            "id": "stay",
            "label": "Option A",
            "title": "Stay in your current role",
            "upside": "Preserves stability, known relationships, and accumulated expertise.",
            "tradeoff": "May limit growth if the current path no longer matches your ambitions.",
            "uncertainty": "Whether the current role can evolve to meet your priorities.",
            "reversibility": "High — staying is the default; you can revisit later.",
        },
        {
            "id": "explore",
            "label": "Option B",
            "title": "Explore external opportunities",
            "upside": "Opens potential for growth, new skills, and better alignment with goals.",
            "tradeoff": "Introduces transition risk, uncertainty, and short-term disruption.",
            "uncertainty": "Quality and timing of available opportunities.",
            "reversibility": "Moderate — leaving may be hard to undo quickly.",
        },
        {
            "id": "prepare",
            "label": "Option C",
            "title": "Prepare first, then switch",
            "upside": "Reduces risk by building skills, savings, or network before moving.",
            "tradeoff": "Delays change; opportunity cost if the market shifts.",
            "uncertainty": "How long preparation will take and whether conditions will hold.",
            "reversibility": "High — preparation phase keeps current options open.",
        },
    ],
    "Education": [
        {
            "id": "enroll",
            "label": "Option A",
            "title": "Enroll or commit now",
            "upside": "Accelerates learning and credential progress toward your goal.",
            "tradeoff": "Financial and time commitment before outcomes are certain.",
            "uncertainty": "Fit of the program and return on investment.",
            "reversibility": "Low to moderate — dropping out has sunk costs.",
        },
        {
            "id": "defer",
            "label": "Option B",
            "title": "Defer and prepare",
            "upside": "More time to save, research programs, and clarify goals.",
            "tradeoff": "Delays progress; momentum may fade.",
            "uncertainty": "Whether waiting improves your position.",
            "reversibility": "High — no commitment yet.",
        },
        {
            "id": "alternative",
            "label": "Option C",
            "title": "Pursue an alternative path",
            "upside": "Self-study, certifications, or experience may achieve goals differently.",
            "tradeoff": "May lack formal recognition or structured support.",
            "uncertainty": "Whether alternative paths meet your actual requirements.",
            "reversibility": "Moderate — depends on the path chosen.",
        },
    ],
    "Relationships": [
        {
            "id": "continue",
            "label": "Option A",
            "title": "Continue investing in this relationship",
            "upside": "Deepens connection and addresses issues with commitment.",
            "tradeoff": "May prolong unproductive patterns if fundamentals don't change.",
            "uncertainty": "Whether both parties share the same willingness to grow.",
            "reversibility": "Moderate — emotional investment increases over time.",
        },
        {
            "id": "pause",
            "label": "Option B",
            "title": "Pause and reassess",
            "upside": "Creates space for clarity without an immediate irreversible choice.",
            "tradeoff": "May feel like avoidance; partner may interpret it differently.",
            "uncertainty": "Whether distance brings clarity or drift.",
            "reversibility": "High — pause is inherently reversible.",
        },
        {
            "id": "boundaries",
            "label": "Option C",
            "title": "Set clear boundaries and communicate",
            "upside": "Addresses concerns directly while keeping the relationship active.",
            "tradeoff": "Requires difficult conversations; outcomes depend on response.",
            "uncertainty": "How the other person will respond to boundaries.",
            "reversibility": "Moderate — boundaries can be adjusted.",
        },
    ],
    "Finance": [
        {
            "id": "proceed",
            "label": "Option A",
            "title": "Proceed with the financial commitment",
            "upside": "Captures opportunity, locks in terms, or achieves a needed goal.",
            "tradeoff": "Reduces liquidity and increases exposure if circumstances change.",
            "uncertainty": "Future income stability and unexpected expenses.",
            "reversibility": "Low — major financial commitments are hard to unwind.",
        },
        {
            "id": "scale",
            "label": "Option B",
            "title": "Scale down the scope",
            "upside": "Achieves part of the goal with less risk and lower commitment.",
            "tradeoff": "May not fully satisfy the original objective.",
            "uncertainty": "Whether a smaller commitment is sufficient.",
            "reversibility": "Moderate — smaller commitments are easier to adjust.",
        },
        {
            "id": "delay",
            "label": "Option C",
            "title": "Delay and build reserves first",
            "upside": "More savings and information reduce financial stress.",
            "tradeoff": "Opportunity cost if prices rise or terms worsen.",
            "uncertainty": "Whether waiting improves your position materially.",
            "reversibility": "High — no commitment made yet.",
        },
    ],
    "Personal Growth": [
        {
            "id": "commit",
            "label": "Option A",
            "title": "Commit fully to this direction",
            "upside": "Focused effort accelerates personal development.",
            "tradeoff": "Less room for other pursuits; burnout risk if overextended.",
            "uncertainty": "Whether this direction truly fits your values.",
            "reversibility": "Moderate — time invested is not recoverable.",
        },
        {
            "id": "explore",
            "label": "Option B",
            "title": "Explore before committing",
            "upside": "Low-risk experimentation reveals fit before major investment.",
            "tradeoff": "Slower progress; may feel unfocused.",
            "uncertainty": "How much exploration is enough to decide.",
            "reversibility": "High — exploration preserves options.",
        },
        {
            "id": "integrate",
            "label": "Option C",
            "title": "Integrate gradually alongside current life",
            "upside": "Balances growth with existing responsibilities.",
            "tradeoff": "Progress may be slower than a full commitment.",
            "uncertainty": "Whether partial integration satisfies your goal.",
            "reversibility": "High — gradual changes are adjustable.",
        },
    ],
    "Other": [
        {
            "id": "stay",
            "label": "Option A",
            "title": "Maintain the current path",
            "upside": "Preserves stability and avoids unnecessary disruption.",
            "tradeoff": "May miss opportunities for improvement.",
            "uncertainty": "Whether the status quo remains viable.",
            "reversibility": "High.",
        },
        {
            "id": "change",
            "label": "Option B",
            "title": "Pursue the change you're considering",
            "upside": "Addresses the motivation behind your question directly.",
            "tradeoff": "Introduces uncertainty and transition costs.",
            "uncertainty": "Outcomes depend on factors you may not control.",
            "reversibility": "Varies — assess before acting.",
        },
        {
            "id": "wait",
            "label": "Option C",
            "title": "Gather more information first",
            "upside": "Reduces decision pressure; clarity may emerge with time.",
            "tradeoff": "Delay has its own costs — missed timing or momentum.",
            "uncertainty": "What information would actually change your mind.",
            "reversibility": "High — waiting keeps options open.",
        },
    ],
}

_OPTION_LABELS = ("Option A", "Option B", "Option C")


def _question_snippet(decision: DecisionInput, max_len: int = 100) -> str:
    q = decision.decision_question.strip()
    if len(q) <= max_len:
        return q
    return q[:max_len] + "…"


def _infer_key_tension(decision: DecisionInput) -> str:
    headline = infer_tension_headline(decision)
    priorities = decision.priorities
    concern = decision.biggest_concern.strip()
    question = _question_snippet(decision)

    if len(priorities) >= 2:
        detail = (
            f"a trade-off between {priorities[0].lower()} and {priorities[1].lower()}"
        )
    elif priorities:
        detail = (
            f"tension between pursuing {priorities[0].lower()} "
            f"and managing uncertainty"
        )
    else:
        detail = "weighing competing factors without a single clear priority"

    base = (
        f'What\'s really in tension: **{headline}**. '
        f'Regarding "{question}", this decision involves {detail}.'
    )
    if concern:
        return f'{base} Your primary concern — "{concern}" — sits at the center of this tension.'
    return base


def _build_contextual_signals(
    profile: ProfileSnapshot,
    decision: DecisionInput,
) -> list[ContextualSignal]:
    signals = []
    for signal_type, number in [
        ("life_path", profile.life_path_number),
        ("birthday", profile.birthday_number),
        ("personal_year", profile.personal_year),
        ("personal_month", profile.personal_month),
    ]:
        meta = get_signal_metadata(signal_type, number)
        ctx = contextualize_signal(
            meta,
            decision.decision_area,
            decision.decision_question,
            decision.priorities,
            decision.biggest_concern,
        )
        signals.append(
            ContextualSignal(
                signal=ctx["signal"],
                number=number,
                traditional_theme=ctx["traditional_theme"],
                reflection=ctx["reflection"],
                decision_relevance=ctx["decision_relevance"],
                why_it_matters_here=ctx["why_it_matters_here"],
            )
        )
    return signals


def _build_decision_questions(decision: DecisionInput) -> list[str]:
    question = _question_snippet(decision)
    items = [
        f"What evidence would most reduce uncertainty about: \"{question}\"?",
    ]
    if decision.biggest_concern:
        items.append(
            f'What would need to be true for your concern ("{decision.biggest_concern}") to be addressed?'
        )
    if decision.priorities:
        items.append(
            f"Which option best honors your top priority ({decision.priorities[0]}) without sacrificing what matters second?"
        )
    if decision.time_horizon:
        items.append(
            f'Given your time horizon of "{decision.time_horizon}", what is the minimum information needed before deciding?'
        )
    for opt in decision.user_options[:2]:
        items.append(f'What would make "{opt.title}" clearly stronger or weaker than the alternatives?')
    return items[:5]


def _score_alignment(option_title: str, option_upside: str, priorities: list[str]) -> str:
    if not priorities:
        return "Moderate"
    title_lower = option_title.lower()
    upside_lower = option_upside.lower()
    score = 0
    for p in priorities:
        pl = p.lower()
        if pl in title_lower or pl in upside_lower:
            score += 2
        if pl == "growth" and ("growth" in upside_lower or "explore" in title_lower):
            score += 1
        if pl == "stability" and ("stability" in upside_lower or "stay" in title_lower):
            score += 1
        if pl == "financial outcome" and ("financial" in upside_lower or "save" in title_lower):
            score += 1
    if score >= 3:
        return "High"
    if score >= 1:
        return "Moderate"
    return "Low"


def _contextualize_option_text(
    decision: DecisionInput,
    title: str,
    base_upside: str,
    base_tradeoff: str,
    base_uncertainty: str,
) -> tuple[str, str, str]:
    """Ground option evaluation in the user's actual decision."""
    question = _question_snippet(decision, 80)
    upside = (
        f'For your decision ("{question}"), choosing "{title}" could mean: {base_upside}'
    )
    tradeoff = base_tradeoff
    if decision.biggest_concern:
        tradeoff = (
            f'{base_tradeoff} Consider how this interacts with your concern: '
            f'"{decision.biggest_concern}".'
        )
    uncertainty = base_uncertainty
    if decision.constraints.strip():
        uncertainty = (
            f'{base_uncertainty} Your stated constraints may affect viability: '
            f'"{decision.constraints.strip()[:80]}".'
        )
    return upside, tradeoff, uncertainty


def _enrich_option(
    decision: DecisionInput,
    *,
    id: str,
    label: str,
    title: str,
    source: str,
    upside: str,
    tradeoff: str,
    uncertainty: str,
    reversibility: str,
) -> DecisionOption:
    c_upside, c_tradeoff, c_uncertainty = _contextualize_option_text(
        decision, title, upside, tradeoff, uncertainty
    )
    alignment = _score_alignment(title, upside, decision.priorities)
    questions = [
        f'How does "{title}" specifically address: "{_question_snippet(decision, 60)}"?',
        f"What is the biggest unknown about this path?",
    ]
    if decision.biggest_concern:
        questions.append(
            f'How does this option address your concern: "{decision.biggest_concern}"?'
        )
    evidence = [
        f'Compare "{title}" against your top priority: '
        f"{decision.priorities[0] if decision.priorities else 'your stated goal'}.",
        "Identify one person who has made a similar choice and ask what they learned.",
    ]
    return DecisionOption(
        id=id,
        label=label,
        title=title,
        source=source,
        upside=c_upside,
        tradeoff=c_tradeoff,
        uncertainty=c_uncertainty,
        reversibility=reversibility,
        alignment=alignment,
        questions=questions,
        evidence_to_check=evidence,
    )


def _options_from_user_input(decision: DecisionInput) -> list[DecisionOption]:
    options: list[DecisionOption] = []
    for i, user_opt in enumerate(decision.user_options[:3]):
        label = _OPTION_LABELS[i] if i < len(_OPTION_LABELS) else f"Option {i + 1}"
        options.append(
            _enrich_option(
                decision,
                id=user_opt.id,
                label=label,
                title=user_opt.title,
                source="user",
                upside="Potential benefit depends on how well this path fits your stated priorities and situation.",
                tradeoff="Every path involves trade-offs — weigh against your concerns and constraints.",
                uncertainty="What evidence would confirm or challenge this path?",
                reversibility="Assess based on how reversible this choice would be in your situation.",
            )
        )
    return options


def _options_from_templates(decision: DecisionInput) -> list[DecisionOption]:
    templates = OPTION_TEMPLATES.get(decision.decision_area, OPTION_TEMPLATES["Other"])
    options: list[DecisionOption] = []
    for tmpl in templates:
        options.append(
            _enrich_option(
                decision,
                id=tmpl["id"],
                label=tmpl["label"],
                title=tmpl["title"],
                source="engine_suggested",
                upside=tmpl["upside"],
                tradeoff=tmpl["tradeoff"],
                uncertainty=tmpl["uncertainty"],
                reversibility=tmpl["reversibility"],
            )
        )
    return options


def generate_options(decision: DecisionInput) -> list[DecisionOption]:
    """Use user-provided options when available; otherwise engine suggestions."""
    user_opts = [o for o in decision.user_options if o.title.strip()]
    if len(user_opts) >= 2:
        return _options_from_user_input(
            decision.model_copy(update={"user_options": user_opts})
        )
    return _options_from_templates(decision)


def _build_considerations(decision: DecisionInput) -> list[str]:
    items: list[str] = []
    question = _question_snippet(decision)
    items.append(f'Your decision — "{question}" — deserves evidence before commitment.')

    if decision.biggest_concern:
        items.append(
            f'Your stated concern — "{decision.biggest_concern}" — deserves explicit '
            "evidence before you commit."
        )
    if decision.constraints.strip():
        items.append(
            f'Your constraints ("{decision.constraints.strip()[:100]}") may eliminate '
            "some options — verify which paths remain viable."
        )
    if decision.time_horizon:
        items.append(
            f'With a time horizon of "{decision.time_horizon}", assess whether each '
            "option can deliver within that window."
        )
    if decision.risk_tolerance:
        items.append(
            f"Given your {decision.risk_tolerance.lower()} risk tolerance, weigh "
            "reversibility against potential upside for each option."
        )
    if decision.priorities:
        items.append(
            f"Your priorities ({', '.join(decision.priorities)}) should be the lens for comparing options."
        )
    items.extend([
        "What evidence would make one option clearly stronger than the others?",
        "What is reversible versus difficult to undo?",
    ])
    return items[:6]


def _build_synthesis(decision: DecisionInput, key_tension: str) -> str:
    parts = [key_tension]
    why = decision.why_considering.strip()
    if why:
        parts.append(f'You noted you are considering this because: "{why}".')
    if decision.context.strip():
        parts.append(decision.context.strip())
    user_titles = [o.title for o in decision.user_options if o.title.strip()]
    if user_titles:
        parts.append(f"You are comparing: {'; '.join(user_titles)}.")
    return " ".join(parts)


def analyze_decision(
    profile: ProfileSnapshot,
    decision: DecisionInput,
) -> AnalyzeDecisionResponse:
    """Generate context-aware Screen 03 intelligence from the DecisionSession."""
    signals = _build_contextual_signals(profile, decision)
    key_tension = _infer_key_tension(decision)
    options = generate_options(decision)
    compass = build_decision_compass(options, decision)
    headline = infer_tension_headline(decision)

    return AnalyzeDecisionResponse(
        summary=(
            f"Structured analysis of your {decision.decision_area.lower()} decision: "
            f'"{_question_snippet(decision, 120)}"'
        ),
        key_tension=key_tension,
        tension_headline=headline,
        decision_synthesis=_build_synthesis(decision, key_tension),
        goal_alignment=(
            f"This exploration is oriented around your primary goal of {profile.primary_goal}. "
            f"Evaluate each option against that focus alongside your stated priorities: "
            f"{', '.join(decision.priorities) if decision.priorities else 'not specified'}."
        ),
        contextual_signals=signals,
        decision_questions=_build_decision_questions(decision),
        considerations=_build_considerations(decision),
        options=options,
        decision_compass=compass,
        analysis_source="deterministic",
        source_label=DETERMINISTIC_LABEL,
        is_development_preview=False,
        preview_label="",
    )


def analysis_to_snapshot(analysis: AnalyzeDecisionResponse) -> StoredAnalysisSnapshot:
    return StoredAnalysisSnapshot(
        summary=analysis.summary,
        key_tension=analysis.key_tension,
        tension_headline=analysis.tension_headline,
        decision_synthesis=analysis.decision_synthesis,
        goal_alignment=analysis.goal_alignment,
        contextual_signals=analysis.contextual_signals,
        decision_questions=analysis.decision_questions,
        considerations=analysis.considerations,
        options=analysis.options,
        decision_compass=analysis.decision_compass,
        analysis_source=analysis.analysis_source,
        source_label=analysis.source_label,
    )


def _build_derivation_notes(
    profile: ProfileSnapshot,
    decision: DecisionInput,
    analysis: StoredAnalysisSnapshot,
    options: list[DecisionOption],
) -> list[str]:
    notes = [
        f'Decision analyzed: "{_question_snippet(decision)}"',
        f"Primary goal: {profile.primary_goal}",
    ]
    if decision.priorities:
        notes.append(f"Priorities used: {', '.join(decision.priorities)}")
    if decision.biggest_concern:
        notes.append(f'Concern referenced: "{decision.biggest_concern}"')
    if decision.time_horizon:
        notes.append(f'Time horizon: "{decision.time_horizon}"')
    user_opts = [o.title for o in options if o.source == "user"]
    suggested = [o.title for o in options if o.source == "engine_suggested"]
    if user_opts:
        notes.append(f"User-defined options: {'; '.join(user_opts)}")
    if suggested:
        notes.append(f"Engine-suggested options (fallback): {'; '.join(suggested)}")
    notes.append(f"Screen 03 analysis source: {analysis.source_label}")
    return notes


def _build_ai_intelligence_summary(
    profile: ProfileSnapshot,
    decision: DecisionInput,
    analysis: StoredAnalysisSnapshot,
    options: list[DecisionOption],
) -> str:
    """Deterministic journey conclusion — not generic horoscope text."""
    question = _question_snippet(decision)
    option_list = ", ".join(f'"{o.title}"' for o in options[:3])
    concern_part = (
        f' Your primary concern is "{decision.biggest_concern}".'
        if decision.biggest_concern
        else ""
    )
    horizon_part = (
        f' You indicated a decision horizon of "{decision.time_horizon}".'
        if decision.time_horizon
        else ""
    )
    priority_part = (
        f" Your stated priorities ({', '.join(decision.priorities)}) should guide comparison."
        if decision.priorities
        else ""
    )
    signal_part = (
        f" Your numerology baseline (Life Path {profile.life_path_number}, "
        f"Personal Year {profile.personal_year}) offers reflective lenses — "
        "not predictions — for examining timing and values."
    )
    return (
        f'This report concludes your exploration of "{question}". '
        f"{analysis.key_tension}{concern_part}{horizon_part}{priority_part} "
        f"The paths under review are: {option_list}.{signal_part} "
        "Use the option comparison and next steps below to gather evidence before committing."
    )


def build_final_report(request: FinalReportRequest) -> FinalReportResponse:
    """Generate Screen 05 from stored Screen 03 analysis — do NOT recompute analyze_decision."""
    profile = request.profile
    decision = request.decision
    analysis = request.analysis
    options = request.options if request.options else analysis.options

    compass = build_decision_compass(options, decision)
    strongest = compass.strongest

    numerology_themes = [
        s.traditional_theme for s in analysis.contextual_signals[:2]
    ]
    numerology_lens = (
        f"Your numerology profile provides a reflective lens around "
        f"{', '.join(numerology_themes) if numerology_themes else 'personal themes'}. "
        f"In this {decision.decision_area.lower()} decision about "
        f'"{_question_snippet(decision)}", those themes may be useful when considering '
        f"how each option fits your values and timing — not which option will succeed."
    )

    numerology_reflection = [
        NumerologyReflection(
            signal=s.signal,
            reflection=s.reflection,
            decision_relevance=s.decision_relevance,
            numerology_lens=s.why_it_matters_here or s.decision_relevance,
        )
        for s in analysis.contextual_signals
    ]

    score_by_title = {s.option_title: s for s in compass.scores}
    option_analysis = []
    for opt in options:
        cs = score_by_title.get(opt.title)
        option_analysis.append(
            OptionAnalysis(
                option=opt.title,
                upside=opt.upside,
                tradeoffs=opt.tradeoff,
                unknowns=opt.uncertainty,
                evidence_to_check="; ".join(opt.evidence_to_check[:2]),
                numera_alignment=cs.numera_alignment if cs else 0.0,
                alignment_label=cs.alignment_label if cs else "",
                main_strength=cs.strengths[:200] if cs else opt.upside[:200],
                main_tradeoff=cs.tradeoffs[:200] if cs else opt.tradeoff[:200],
            )
        )

    next_steps = [
        (
            f'Gather the missing information that could change alignment — start with: '
            f"{compass.what_could_change[0]}"
            if compass.what_could_change
            else f'List facts you are uncertain about regarding: "{_question_snippet(decision)}"'
        ),
        (
            f"Compare options using your top priority ({decision.priorities[0]}) "
            f"and concern as explicit scoring criteria."
            if decision.priorities
            else f"Compare options against your primary goal ({profile.primary_goal})."
        ),
        (
            f'Set a decision checkpoint aligned with your horizon '
            f'("{decision.time_horizon}").'
            if decision.time_horizon
            else "Set a decision checkpoint to revisit once you have new evidence."
        ),
    ]

    currently = None
    if strongest.has_clear_leader:
        currently = CurrentlyStrongestOption(
            option_id=strongest.option_id,
            title=strongest.title,
            reason=strongest.reason,
        )

    ai_summary = _build_compass_ai_summary(profile, decision, analysis, compass, options)
    derivation_notes = _build_derivation_notes(profile, decision, analysis, options)
    derivation_notes.append(f"NUMERA Alignment formula: {compass.scoring_formula}")
    if strongest.has_clear_leader:
        derivation_notes.append(f"Currently strongest alignment: {strongest.title}")
    else:
        derivation_notes.append("No clear alignment leader — scores too close or context incomplete")

    return FinalReportResponse(
        decision_summary=analysis.decision_synthesis,
        key_tension=analysis.key_tension,
        tension_headline=analysis.tension_headline or infer_tension_headline(decision),
        numerology_reflection=numerology_reflection,
        numerology_lens_summary=numerology_lens,
        option_analysis=option_analysis,
        decision_compass=compass,
        currently_strongest_option=currently,
        confidence=compass.confidence,
        what_could_change=compass.what_could_change,
        key_considerations=analysis.considerations,
        next_steps=next_steps,
        ai_intelligence_summary=ai_summary,
        derivation_notes=derivation_notes,
        synthesis_source="deterministic",
        source_label=PREVIEW_LABEL,
        is_development_preview=True,
        preview_label=PREVIEW_LABEL,
    )


def _build_compass_ai_summary(
    profile: ProfileSnapshot,
    decision: DecisionInput,
    analysis: StoredAnalysisSnapshot,
    compass,
    options: list[DecisionOption],
) -> str:
    """Deterministic intelligence summary grounded in Decision Compass."""
    question = _question_snippet(decision)
    strongest = compass.strongest
    if strongest.has_clear_leader:
        leader_part = (
            f'Based on the priorities and context you provided, "{strongest.title}" '
            f"currently shows the strongest NUMERA Alignment. {strongest.reason[:280]}"
        )
    else:
        leader_part = (
            f"No option shows a clearly stronger alignment yet. {strongest.reason[:280]}"
        )
    return (
        f'This report synthesizes your journey exploring "{question}". '
        f"{leader_part} "
        f"Confidence in this assessment is {compass.confidence.level.lower()} — "
        f"{compass.confidence.reason[:200]} "
        "Numerology adds a reflective lens only; it did not determine rankings. "
        "This is a reflection, not a prediction."
    )

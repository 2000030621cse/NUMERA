"""Structured numerology interpretation metadata — reflective, not predictive."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SignalMetadata:
    number: int
    signal_name: str
    traditional_theme: str
    strengths: str
    reflection_points: str
    relevant_contexts: tuple[str, ...]


LIFE_PATH: dict[int, SignalMetadata] = {
    1: SignalMetadata(
        1, "Life Path", "independence and initiative",
        "self-direction, starting new paths, leading change",
        "How much autonomy does each option give you?",
        ("Career", "Personal Growth", "Finance"),
    ),
    2: SignalMetadata(
        2, "Life Path", "cooperation and balance",
        "partnership, diplomacy, harmonizing competing needs",
        "Who is affected by this decision besides you?",
        ("Relationships", "Career", "Education"),
    ),
    3: SignalMetadata(
        3, "Life Path", "expression and communication",
        "creativity, visibility, articulating what matters",
        "Does each option let you express what you truly value?",
        ("Career", "Education", "Personal Growth"),
    ),
    4: SignalMetadata(
        4, "Life Path", "structure and foundations",
        "discipline, building steadily, practical planning",
        "Which option builds the most durable foundation?",
        ("Finance", "Career", "Education"),
    ),
    5: SignalMetadata(
        5, "Life Path", "change and exploration",
        "adaptability, variety, recalibrating when stuck",
        "Are you choosing growth through change or stability through continuity?",
        ("Career", "Personal Growth", "Relationships"),
    ),
    6: SignalMetadata(
        6, "Life Path", "responsibility and meaningful choice",
        "care for others, balance, long-term commitments",
        "How does each option affect your responsibilities and relationships?",
        ("Relationships", "Career", "Finance"),
    ),
    7: SignalMetadata(
        7, "Life Path", "analysis and inner clarity",
        "depth, research, understanding before acting",
        "What do you still need to understand before committing?",
        ("Education", "Career", "Finance"),
    ),
    8: SignalMetadata(
        8, "Life Path", "ambition and practical outcomes",
        "achievement, resource stewardship, tangible results",
        "Which option best aligns with measurable outcomes you care about?",
        ("Career", "Finance", "Education"),
    ),
    9: SignalMetadata(
        9, "Life Path", "perspective and completion",
        "broader impact, letting go, seeing the full picture",
        "What would you regret not considering five years from now?",
        ("Relationships", "Personal Growth", "Career"),
    ),
    11: SignalMetadata(
        11, "Life Path", "intuition and inspirational direction",
        "sensitivity to timing, visionary thinking, inner guidance",
        "What does your intuition say — and what evidence supports it?",
        ("Personal Growth", "Career", "Relationships"),
    ),
    22: SignalMetadata(
        22, "Life Path", "building at scale",
        "large ambitions, disciplined execution, lasting structures",
        "Is this decision a step toward something you want to build long-term?",
        ("Career", "Finance", "Education"),
    ),
    33: SignalMetadata(
        33, "Life Path", "compassionate service",
        "nurturing impact, purpose beyond self, meaningful contribution",
        "How does each option serve both you and those who depend on you?",
        ("Relationships", "Career", "Personal Growth"),
    ),
}

BIRTHDAY: dict[int, SignalMetadata] = {
    1: SignalMetadata(1, "Birthday Number", "initiative in daily action", "starting, leading, acting first", "How do you typically begin when facing uncertainty?", ("Career", "Personal Growth")),
    2: SignalMetadata(2, "Birthday Number", "collaborative approach", "partnering, listening, finding middle ground", "Who could you consult before deciding?", ("Relationships", "Career")),
    3: SignalMetadata(3, "Birthday Number", "expressive approach", "communicating, connecting, sharing ideas", "Have you articulated this decision clearly to yourself?", ("Education", "Career")),
    4: SignalMetadata(4, "Birthday Number", "methodical approach", "planning, organizing, step-by-step progress", "What concrete plan would make each option feel real?", ("Finance", "Education")),
    5: SignalMetadata(5, "Birthday Number", "adaptive approach", "flexibility, trying alternatives, embracing change", "Are you avoiding change — or rushing into it?", ("Career", "Personal Growth")),
    6: SignalMetadata(6, "Birthday Number", "responsible approach", "caring for obligations, choosing thoughtfully", "Who relies on your decision — and have you weighed their needs?", ("Relationships", "Finance")),
    7: SignalMetadata(7, "Birthday Number", "analytical approach", "researching, reflecting, seeking depth", "What research would reduce your uncertainty?", ("Education", "Finance")),
    8: SignalMetadata(8, "Birthday Number", "results-oriented approach", "achieving, managing resources, executing", "What measurable outcome would define success?", ("Career", "Finance")),
    9: SignalMetadata(9, "Birthday Number", "big-picture approach", "perspective, completion, broader meaning", "Does this decision fit the larger story you want for your life?", ("Personal Growth", "Relationships")),
    11: SignalMetadata(11, "Birthday Number", "intuitive daily style", "sensing timing, reading situations", "What is your gut saying — and what facts confirm or challenge it?", ("Personal Growth", "Relationships")),
    22: SignalMetadata(22, "Birthday Number", "builder's daily style", "practical execution of big ideas", "What is the smallest concrete step toward your preferred option?", ("Career", "Finance")),
}

PERSONAL_YEAR: dict[int, SignalMetadata] = {
    1: SignalMetadata(1, "Personal Year", "new beginnings", "fresh starts, self-definition, planting seeds", "Is this year a natural time to initiate change?", ("Career", "Personal Growth")),
    2: SignalMetadata(2, "Personal Year", "patience and partnership", "waiting, collaborating, pacing decisions", "Should you decide now — or allow more time for clarity?", ("Relationships", "Career")),
    3: SignalMetadata(3, "Personal Year", "expression and expansion", "visibility, communication, social growth", "Would sharing your thinking with others help?", ("Career", "Education")),
    4: SignalMetadata(4, "Personal Year", "foundation-building", "structure, consistency, hard work", "Does this decision strengthen your foundation?", ("Finance", "Education")),
    5: SignalMetadata(5, "Personal Year", "change and movement", "transition, recalibration, breaking routines", "Is your discomfort a signal to change — or to stabilize?", ("Career", "Personal Growth")),
    6: SignalMetadata(6, "Personal Year", "responsibility and choice", "commitments, family, duty", "How do your obligations shape the timing of this decision?", ("Relationships", "Finance")),
    7: SignalMetadata(7, "Personal Year", "reflection and refinement", "introspection, study, inner work", "Would more reflection change your answer?", ("Education", "Personal Growth")),
    8: SignalMetadata(8, "Personal Year", "results and authority", "achievement, material focus, stepping up", "Is this the year to push for tangible outcomes?", ("Career", "Finance")),
    9: SignalMetadata(9, "Personal Year", "completion and transition", "closing chapters, preparing for what's next", "Are you finishing something before starting anew?", ("Relationships", "Career")),
}

PERSONAL_MONTH: dict[int, SignalMetadata] = {
    1: SignalMetadata(1, "Personal Month", "initiative", "starting, acting, defining direction", "What small action could you take this month?", ("Career", "Personal Growth")),
    2: SignalMetadata(2, "Personal Month", "collaboration", "partnership, patience, dialogue", "Who should you talk to before deciding?", ("Relationships", "Career")),
    3: SignalMetadata(3, "Personal Month", "communication", "expressing, sharing, connecting", "Can you write down the pros and cons clearly?", ("Education", "Career")),
    4: SignalMetadata(4, "Personal Month", "structure", "planning, organizing, building", "What plan would make your preferred option concrete?", ("Finance", "Education")),
    5: SignalMetadata(5, "Personal Month", "flexibility", "change, exploration, adaptation", "Is there a low-risk way to test your preferred direction?", ("Career", "Personal Growth")),
    6: SignalMetadata(6, "Personal Month", "responsibility", "duty, care, thoughtful choice", "Have you considered who else is affected?", ("Relationships", "Finance")),
    7: SignalMetadata(7, "Personal Month", "analysis", "research, reflection, depth", "What one question, if answered, would clarify things?", ("Education", "Finance")),
    8: SignalMetadata(8, "Personal Month", "execution", "results, accountability, progress", "What outcome would you track this month?", ("Career", "Finance")),
    9: SignalMetadata(9, "Personal Month", "perspective", "release, completion, seeing clearly", "What would you advise a friend in your situation?", ("Personal Growth", "Relationships")),
}


def get_signal_metadata(signal_type: str, number: int) -> SignalMetadata:
    tables = {
        "life_path": LIFE_PATH,
        "birthday": BIRTHDAY,
        "personal_year": PERSONAL_YEAR,
        "personal_month": PERSONAL_MONTH,
    }
    table = tables.get(signal_type, LIFE_PATH)
    if number in table:
        return table[number]
    return SignalMetadata(
        number, signal_type.replace("_", " ").title(), "personal awareness",
        "self-reflection", "What does your situation tell you beyond the numbers?",
        ("Personal Growth",),
    )


def contextualize_signal(
    meta: SignalMetadata,
    decision_area: str,
    decision_question: str,
    priorities: list[str] | None = None,
    biggest_concern: str = "",
) -> dict[str, str]:
    """Connect a numerology signal to the user's specific decision."""
    area_lower = decision_area.lower()
    question_snippet = decision_question[:80] + ("…" if len(decision_question) > 80 else "")
    priority_text = priorities[0] if priorities else "your stated goal"
    reflection_q = meta.reflection_points.rstrip("?").lower()

    why_it_matters = (
        f'Your current decision involves "{question_snippet}" and your stated priority '
        f"is {priority_text}. This makes questions around {reflection_q} useful to examine."
    )
    if biggest_concern.strip():
        why_it_matters += (
            f' Your concern about "{biggest_concern.strip()}" adds weight to how you '
            f"weigh {meta.traditional_theme} in this choice."
        )

    reflection = (
        "Consider whether the option you choose supports both your desired outcome "
        "and the responsibilities or values you are trying to preserve. "
        "This is reflection, not prediction."
    )

    decision_relevance = (
        f"Your {meta.signal_name} {meta.number} is a reflective lens around "
        f"{meta.traditional_theme} — traditionally associated with {meta.strengths}. "
        f"In your {area_lower} decision, use it to examine {reflection_q}, not to predict an outcome."
    )

    return {
        "signal": f"{meta.signal_name} {meta.number}",
        "traditional_theme": meta.traditional_theme,
        "reflection": reflection,
        "why_it_matters_here": why_it_matters,
        "decision_relevance": decision_relevance,
    }

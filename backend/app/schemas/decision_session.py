"""Unified DecisionSession schemas — data contract for the full NUMERA journey."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ProfileSnapshot(BaseModel):
    full_name: str
    date_of_birth: date
    life_path_number: int
    birthday_number: int
    personal_year: int
    personal_month: int
    primary_goal: str


class UserOptionInput(BaseModel):
    """User-defined path from Screen 02."""

    model_config = ConfigDict(str_strip_whitespace=True)

    id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)


class DecisionInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    decision_area: str = Field(..., min_length=1)
    decision_question: str = Field(..., min_length=1)
    why_considering: str = ""
    biggest_concern: str = ""
    priorities: list[str] = Field(default_factory=list)
    constraints: str = ""
    risk_tolerance: str = ""
    time_horizon: str = ""
    context: str = ""
    user_options: list[UserOptionInput] = Field(default_factory=list)


class DecisionOption(BaseModel):
    id: str
    label: str
    title: str
    source: str = "engine_suggested"  # user | engine_suggested | user_custom
    upside: str
    tradeoff: str
    uncertainty: str = ""
    reversibility: str = ""
    alignment: str = ""
    questions: list[str] = Field(default_factory=list)
    evidence_to_check: list[str] = Field(default_factory=list)


class ContextualSignal(BaseModel):
    signal: str
    number: int
    traditional_theme: str
    reflection: str
    decision_relevance: str
    why_it_matters_here: str = ""


class AlignmentBreakdown(BaseModel):
    priority_score: float
    risk_score: float
    constraint_score: float
    time_horizon_score: float
    weights: dict[str, float] = Field(default_factory=dict)


class OptionCompassScore(BaseModel):
    option_id: str
    option_title: str
    numera_alignment: float
    alignment_label: str
    breakdown: AlignmentBreakdown
    strengths: str
    tradeoffs: str
    unknowns: str
    evidence_to_check: list[str] = Field(default_factory=list)


class StrongestAlignment(BaseModel):
    option_id: str = ""
    title: str = ""
    reason: str = ""
    has_clear_leader: bool = False
    no_leader_reason: str = ""


class CompassConfidence(BaseModel):
    level: str  # High | Moderate | Exploratory
    reason: str


class DecisionCompass(BaseModel):
    scores: list[OptionCompassScore] = Field(default_factory=list)
    strongest: StrongestAlignment
    confidence: CompassConfidence
    what_could_change: list[str] = Field(default_factory=list)
    transparency_note: str = ""
    numerology_note: str = ""
    scoring_formula: str = ""
    tension_headline: str = ""


class AnalyzeDecisionRequest(BaseModel):
    """Full session payload for Screen 03 analysis."""

    profile: ProfileSnapshot
    decision: DecisionInput


class AnalyzeDecisionResponse(BaseModel):
    summary: str
    key_tension: str
    tension_headline: str = ""
    decision_synthesis: str
    goal_alignment: str
    contextual_signals: list[ContextualSignal]
    decision_questions: list[str] = Field(default_factory=list)
    considerations: list[str]
    options: list[DecisionOption]
    decision_compass: DecisionCompass | None = None
    analysis_source: str = "deterministic"
    source_label: str = "NUMERA deterministic analysis"
    is_development_preview: bool = False
    preview_label: str = ""


class StoredAnalysisSnapshot(BaseModel):
    """Screen 03 artifact passed to Screen 05 — must not be recomputed silently."""

    summary: str
    key_tension: str
    tension_headline: str = ""
    decision_synthesis: str
    goal_alignment: str
    contextual_signals: list[ContextualSignal]
    decision_questions: list[str] = Field(default_factory=list)
    considerations: list[str]
    options: list[DecisionOption]
    decision_compass: DecisionCompass | None = None
    analysis_source: str = "deterministic"
    source_label: str = "NUMERA deterministic analysis"


class CompassRequest(BaseModel):
    profile: ProfileSnapshot
    decision: DecisionInput
    options: list[DecisionOption] = Field(default_factory=list)


class NumerologyReflection(BaseModel):
    signal: str
    reflection: str
    decision_relevance: str
    numerology_lens: str = ""


class OptionAnalysis(BaseModel):
    option: str
    upside: str
    tradeoffs: str
    unknowns: str
    evidence_to_check: str
    numera_alignment: float = 0.0
    alignment_label: str = ""
    main_strength: str = ""
    main_tradeoff: str = ""


class CurrentlyStrongestOption(BaseModel):
    option_id: str = ""
    title: str = ""
    reason: str = ""


class FinalReportRequest(BaseModel):
    profile: ProfileSnapshot
    decision: DecisionInput
    options: list[DecisionOption] = Field(default_factory=list)
    analysis: StoredAnalysisSnapshot


class FinalReportResponse(BaseModel):
    decision_summary: str
    key_tension: str
    tension_headline: str = ""
    numerology_reflection: list[NumerologyReflection]
    numerology_lens_summary: str = ""
    option_analysis: list[OptionAnalysis]
    decision_compass: DecisionCompass
    currently_strongest_option: CurrentlyStrongestOption | None = None
    confidence: CompassConfidence
    what_could_change: list[str] = Field(default_factory=list)
    key_considerations: list[str]
    next_steps: list[str]
    ai_intelligence_summary: str = ""
    derivation_notes: list[str] = Field(default_factory=list)
    synthesis_source: str = "deterministic"
    source_label: str = ""
    is_development_preview: bool = False
    preview_label: str = ""

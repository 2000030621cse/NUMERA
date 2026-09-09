export const PRIMARY_GOALS = [

  "Career",

  "Relationships",

  "Finance",

  "Education",

  "Personal Growth",

  "Other",

] as const;



export type PrimaryGoal = (typeof PRIMARY_GOALS)[number];

export type DecisionArea = PrimaryGoal;



export const PRIORITIES = [

  "Growth",

  "Stability",

  "Financial outcome",

  "Learning",

  "Time",

  "Location",

  "Relationships",

  "Independence",

  "Impact",

  "Peace of mind",

] as const;



export type Priority = (typeof PRIORITIES)[number];



export const TIME_HORIZONS = [

  "Now",

  "Next few months",

  "Within a year",

  "Long term",

] as const;



export type TimeHorizon = (typeof TIME_HORIZONS)[number];



export const RISK_TOLERANCES = ["Low", "Moderate", "High"] as const;

export type RiskTolerance = (typeof RISK_TOLERANCES)[number];



export type HealthState = "checking" | "ok" | "down";



export type Screen =

  | "landing"

  | "profile"

  | "profile-results"

  | "decision"

  | "intelligence"

  | "what-if"

  | "final-report";



export type NumerologyProfile = {

  full_name: string;

  date_of_birth: string;

  life_path_number: number;

  birthday_number: number;

  personal_year: number;

  personal_month: number;

  primary_goal: PrimaryGoal;

};



export type UserOption = {

  id: string;

  title: string;

};



/** Unified decision input — flows through screens 02–05 */

export type DecisionContext = {

  decision_area: DecisionArea;

  decision_question: string;

  why_considering: string;

  biggest_concern: string;

  priorities: Priority[];

  constraints: string;

  risk_tolerance: RiskTolerance | "";

  time_horizon: TimeHorizon | "";

  context: string;

  user_options: UserOption[];

};



export type ContextualSignal = {
  signal: string;
  number: number;
  traditional_theme: string;
  reflection: string;
  decision_relevance: string;
  why_it_matters_here?: string;
};

export type AlignmentBreakdown = {
  priority_score: number;
  risk_score: number;
  constraint_score: number;
  time_horizon_score: number;
  weights: Record<string, number>;
};

export type OptionCompassScore = {
  option_id: string;
  option_title: string;
  numera_alignment: number;
  alignment_label: string;
  breakdown: AlignmentBreakdown;
  strengths: string;
  tradeoffs: string;
  unknowns: string;
  evidence_to_check: string[];
};

export type StrongestAlignment = {
  option_id: string;
  title: string;
  reason: string;
  has_clear_leader: boolean;
  no_leader_reason: string;
};

export type CompassConfidence = {
  level: string;
  reason: string;
};

export type DecisionCompass = {
  scores: OptionCompassScore[];
  strongest: StrongestAlignment;
  confidence: CompassConfidence;
  what_could_change: string[];
  transparency_note: string;
  numerology_note: string;
  scoring_formula: string;
  tension_headline: string;
};

export type CurrentlyStrongestOption = {
  option_id: string;
  title: string;
  reason: string;
};



export type OptionSource = "user" | "engine_suggested" | "user_custom";



export type DecisionOption = {

  id: string;

  label: string;

  title: string;

  source: OptionSource;

  upside: string;

  tradeoff: string;

  uncertainty: string;

  reversibility: string;

  alignment: string;

  questions: string[];

  evidence_to_check: string[];

};



/** Compatible with DirectionCard component */

export type PossibleDirection = Pick<

  DecisionOption,

  "id" | "label" | "title" | "upside" | "tradeoff" | "questions"

>;



/** Screen 03 analysis artifact — passed to Screen 05 */

export type StoredAnalysisSnapshot = {
  summary: string;
  key_tension: string;
  tension_headline?: string;
  decision_synthesis: string;
  goal_alignment: string;
  contextual_signals: ContextualSignal[];
  decision_questions: string[];
  considerations: string[];
  options: DecisionOption[];
  decision_compass?: DecisionCompass | null;
  analysis_source: string;
  source_label: string;
};

/** Screen 03 analysis from backend decision engine */
export type DecisionAnalysis = StoredAnalysisSnapshot & {
  is_development_preview?: boolean;
  preview_label?: string;
};



/** Screen 04 scenario — derived from DecisionOption */

export type WhatIfScenario = DecisionOption & {

  name: string;

  assumption: string;

  expected_benefit: string;

  possible_tradeoff: string;

};



export type NumerologyReflection = {
  signal: string;
  reflection: string;
  decision_relevance: string;
  numerology_lens?: string;
};

export type OptionAnalysis = {
  option: string;
  upside: string;
  tradeoffs: string;
  unknowns: string;
  evidence_to_check: string;
  numera_alignment?: number;
  alignment_label?: string;
  main_strength?: string;
  main_tradeoff?: string;
};

/** Screen 05 final report */
export type DecisionInsightReport = {
  decision_summary: string;
  key_tension: string;
  tension_headline?: string;
  numerology_reflection: NumerologyReflection[];
  numerology_lens_summary?: string;
  option_analysis: OptionAnalysis[];
  decision_compass?: DecisionCompass;
  currently_strongest_option?: CurrentlyStrongestOption | null;
  confidence?: CompassConfidence;
  what_could_change?: string[];
  key_considerations: string[];
  next_steps: string[];
  ai_intelligence_summary: string;
  derivation_notes: string[];
  synthesis_source: string;
  source_label: string;
  is_development_preview?: boolean;
  preview_label?: string;
};



export const PRODUCT_PILLARS = [

  {

    title: "Know your patterns",

    body: "Deterministic numbers reveal personal patterns that can provide a structured starting point for reflection.",

  },

  {

    title: "Understand your context",

    body: "Combine personal goals, priorities and timing with your personal baseline.",

  },

  {

    title: "Explore your possibilities",

    body: "Use AI to examine options, trade-offs and potential next steps.",

  },

] as const;



export const HOW_IT_WORKS = [
  { step: "01", title: "Build your reflective baseline" },
  { step: "02", title: "Frame your decision and options" },
  { step: "03", title: "Understand tension and signals" },
  { step: "04", title: "Explore possibilities with Decision Compass" },
  { step: "05", title: "Read your Decision Report" },
] as const;



export const NUMBER_INSIGHTS = {

  life_path_number: {

    label: "Life Path Number",

    blurb: "Your core trajectory — reflective themes for long-horizon decisions.",

  },

  birthday_number: {

    label: "Birthday Number",

    blurb: "A native talent signature that colors how you approach choices.",

  },

  personal_year: {

    label: "Personal Year",

    blurb: "This year's timing signal for focus, momentum, and pacing.",

  },

  personal_month: {

    label: "Personal Month",

    blurb: "Near-term rhythm — what this month may ask you to emphasize.",

  },

} as const;



export const JOURNEY_STEPS = [

  { id: 1, label: "Profile" },

  { id: 2, label: "Decision" },

  { id: 3, label: "Intelligence" },

  { id: 4, label: "Possibilities" },

  { id: 5, label: "Report" },

] as const;



export type JourneyStep = 1 | 2 | 3 | 4 | 5;



export const EMPTY_DECISION: DecisionContext = {

  decision_area: "Career",

  decision_question: "",

  why_considering: "",

  biggest_concern: "",

  priorities: [],

  constraints: "",

  risk_tolerance: "",

  time_horizon: "",

  context: "",

  user_options: [

    { id: "opt-a", title: "" },

    { id: "opt-b", title: "" },

    { id: "opt-c", title: "" },

  ],

};



export function optionToScenario(option: DecisionOption): WhatIfScenario {

  return {

    ...option,

    name: option.title.toUpperCase(),

    assumption: option.title,

    expected_benefit: option.upside,

    possible_tradeoff: option.tradeoff,

  };

}



/** Fingerprint decision inputs that affect analysis — used for session invalidation */

export function decisionInputKey(decision: DecisionContext): string {

  const opts = (decision.user_options ?? [])

    .map((o) => o.title.trim())

    .filter(Boolean)

    .join("|");

  return JSON.stringify({

    q: decision.decision_question.trim(),

    area: decision.decision_area,

    why: decision.why_considering.trim(),

    concern: decision.biggest_concern.trim(),

    priorities: decision.priorities,

    constraints: decision.constraints.trim(),

    risk: decision.risk_tolerance,

    horizon: decision.time_horizon,

    context: decision.context.trim(),

    options: opts,

  });

}



export function analysisToSnapshot(analysis: DecisionAnalysis): StoredAnalysisSnapshot {
  return {
    summary: analysis.summary,
    key_tension: analysis.key_tension,
    tension_headline: analysis.tension_headline,
    decision_synthesis: analysis.decision_synthesis,
    goal_alignment: analysis.goal_alignment,
    contextual_signals: analysis.contextual_signals,
    decision_questions: analysis.decision_questions,
    considerations: analysis.considerations,
    options: analysis.options,
    decision_compass: analysis.decision_compass,
    analysis_source: analysis.analysis_source,
    source_label: analysis.source_label,
  };
}

export function normalizeDecisionCompass(raw: Partial<DecisionCompass> | null | undefined): DecisionCompass | null {
  if (!raw || !raw.strongest || !raw.confidence) return null;
  return {
    scores: Array.isArray(raw.scores) ? raw.scores : [],
    strongest: raw.strongest,
    confidence: raw.confidence,
    what_could_change: toStringList(raw.what_could_change),
    transparency_note: raw.transparency_note ?? "",
    numerology_note: raw.numerology_note ?? "",
    scoring_formula: raw.scoring_formula ?? "",
    tension_headline: raw.tension_headline ?? "",
  };
}



export function normalizeDecisionOption(
  opt: Partial<DecisionOption> & Pick<DecisionOption, "id" | "label" | "title">,
): DecisionOption {
  return {
    id: opt.id,
    label: opt.label,
    title: opt.title,
    source: opt.source ?? "engine_suggested",
    upside: opt.upside ?? "",
    tradeoff: opt.tradeoff ?? "",
    uncertainty: opt.uncertainty ?? "",
    reversibility: opt.reversibility ?? "",
    alignment: opt.alignment ?? "Moderate",
    questions: toStringList(opt.questions),
    evidence_to_check: toStringList(opt.evidence_to_check),
  };
}

/** Coerce API/session values that may be strings into string arrays. */
export function toStringList(value: unknown): string[] {
  if (Array.isArray(value)) {
    return value.map(String).filter((s) => s.trim().length > 0);
  }
  if (typeof value === "string" && value.trim()) {
    return [value.trim()];
  }
  return [];
}

/** Normalize analyze API / sessionStorage payloads to prevent render crashes. */
export function normalizeDecisionAnalysis(
  raw: Partial<DecisionAnalysis>,
): DecisionAnalysis {
  const options = (raw.options ?? []).map((opt) =>
    normalizeDecisionOption(
      opt as Partial<DecisionOption> & Pick<DecisionOption, "id" | "label" | "title">,
    ),
  );

  return {
    summary: raw.summary ?? "",
    key_tension: raw.key_tension ?? "",
    tension_headline: raw.tension_headline ?? "",
    decision_synthesis: raw.decision_synthesis ?? raw.key_tension ?? "",
    goal_alignment: raw.goal_alignment ?? "",
    contextual_signals: raw.contextual_signals ?? [],
    decision_questions: toStringList(raw.decision_questions),
    considerations: toStringList(raw.considerations),
    options,
    decision_compass: normalizeDecisionCompass(raw.decision_compass),
    analysis_source: raw.analysis_source ?? "deterministic",
    source_label: raw.source_label ?? "NUMERA deterministic analysis",
    is_development_preview: raw.is_development_preview ?? false,
    preview_label: raw.preview_label ?? "",
  };
}

export function normalizeDecisionContext(
  decision: Partial<DecisionContext> | undefined,
): DecisionContext {
  if (!decision) return EMPTY_DECISION;
  return {
    ...EMPTY_DECISION,
    ...decision,
    user_options:
      decision.user_options && decision.user_options.length > 0
        ? decision.user_options
        : EMPTY_DECISION.user_options,
    priorities: decision.priorities ?? [],
  };
}

/** Normalize final report API / sessionStorage payloads to prevent render crashes. */
export function normalizeDecisionInsightReport(
  raw: Partial<DecisionInsightReport>,
  fallback?: Pick<DecisionAnalysis, "decision_synthesis" | "key_tension">,
): DecisionInsightReport {
  const decision_summary =
    raw.decision_summary ?? fallback?.decision_synthesis ?? "";
  const key_tension = raw.key_tension ?? fallback?.key_tension ?? "";

  return {
    decision_summary,
    key_tension,
    tension_headline: raw.tension_headline ?? fallback?.key_tension ?? "",
    numerology_reflection: Array.isArray(raw.numerology_reflection)
      ? raw.numerology_reflection
      : [],
    numerology_lens_summary: raw.numerology_lens_summary ?? "",
    option_analysis: Array.isArray(raw.option_analysis) ? raw.option_analysis : [],
    decision_compass: normalizeDecisionCompass(raw.decision_compass) ?? undefined,
    currently_strongest_option: raw.currently_strongest_option ?? null,
    confidence: raw.confidence,
    what_could_change: toStringList(raw.what_could_change),
    key_considerations: toStringList(raw.key_considerations),
    next_steps: toStringList(raw.next_steps),
    ai_intelligence_summary:
      (typeof raw.ai_intelligence_summary === "string" &&
      raw.ai_intelligence_summary.trim()
        ? raw.ai_intelligence_summary.trim()
        : "") ||
      decision_summary ||
      key_tension,
    derivation_notes: toStringList(raw.derivation_notes),
    synthesis_source: raw.synthesis_source ?? "deterministic",
    source_label: raw.source_label ?? raw.preview_label ?? "",
    is_development_preview: raw.is_development_preview ?? false,
    preview_label: raw.preview_label ?? "",
  };
}

